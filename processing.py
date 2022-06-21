from eddn import main
from csv_processing import csv_value_check, csv_write_commodity

while True:
    message = next(main())

    # Filter only commodities
    if 'commodity' in message['$schemaRef']:
        # Debug info
        header_info = message['header']
        timestamp = header_info['gatewayTimestamp']

        # Time and Date
        data_separator = str(timestamp).split('T')
        time = data_separator[1]
        date = data_separator[0]

        # Main Content
        message_content = message['message']

        # Location Info
        system_name = message_content['systemName']
        station_name = message_content['stationName']
        market_id = message_content['marketId']  # Not sure what this references

        # Commodities
        commodities = message_content['commodities']

        # Economy and Fleet Carrier Check
        fleet_carrier = False
        try:
            economies = message_content['economies']
            for e in economies:
                name = e['name']
                if name == 'Carrier':
                    print('Skipping Fleet Carrier...')
                    fleet_carrier = True

        except KeyError:
            economies = 'No Economies'

        if fleet_carrier:
            continue

        # Commodity Processing

        for commodity in commodities:

            # Commodity Info
            c_name = commodity['name']
            mean_price = commodity['meanPrice']
            buy_price = commodity['buyPrice']
            stock = commodity['stock']
            sell_price = commodity['sellPrice']
            demand = commodity['demand']

            # Build List

            commodity_info_list = [None, c_name, mean_price, buy_price, stock, sell_price, demand]

            # Call for Check
            check = csv_value_check(c_name, 1)

            if not check:
                # Call for Write
                check = csv_write_commodity(commodity_info_list)

                if type(check) is int:
                    print(f'{c_name} inserted into CSV file, row {check}')

            else:
                print('Commodity already in CSV, skipping...')

        print(f'Message received at {time} on {date}')
        print(commodities)
        print(economies)
