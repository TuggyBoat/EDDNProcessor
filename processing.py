import datetime

from eddn import main
from csv_processing import *

enable_fleet_carrier = True
commodity_file_name = 'commodity.csv'
station_file_name = 'station.csv'

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
        update_value = f'Updated at {time} on {date}'

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
                    fleet_carrier = True

        except KeyError:
            economies = 'No Economies'

        if fleet_carrier and not enable_fleet_carrier:
            continue

        # Build Station List
        station_info = [station_name, market_id, system_name, update_value]

        # Call for Check

        check = csv_value_check(station_file_name, market_id, 2)

        if not check:

            # Write
            check = csv_write_line(station_info, station_file_name)

            if type(check) is int:
                print(f'{station_name} inserted into CSV file, row {check}')


        else:
            check = update_timestamp(station_file_name, market_id, update_value, 2, 4)
            if check:
                print(f'Updated timestamp for {station_name}. ({market_id})')

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
            check = csv_value_check(commodity_file_name, c_name, 2)

            if not check:
                # Call for Write
                check = csv_write_line(commodity_info_list, commodity_file_name)

                if type(check) is int:
                    print(f'{c_name} inserted into CSV file, row {check}')

        print(f'Message received at {time} on {date}')
        print(commodities)
        print(economies)
