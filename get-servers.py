import csv
import requests
import json
import time

city_pairs_file = 'country_city_pairs.csv'
json_file_path = 'speedtest_servers.json'
csv_file_path = 'speedtest_servers.csv'


def read_csv_to_set(csv_file_path):
    country_city_set = set()

    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header
        for row in reader:
            country_city_set.add(tuple(row))

    return country_city_set


def call_speedtest_api_for_pairs(pairs):
    filtered_servers = []
    seen_server_ids = set()

    for country, city in pairs:
        print(f"Fetching data for {country}, {city}")

        url = f"https://www.speedtest.net/api/js/servers?engine=js&https_functional=true&limit=100&search={city}"
        response = requests.get(url)
        if response.status_code == 200:
            servers = response.json()
            

            for server in servers:
                server_id = server.get('id')
                if server_id and server_id not in seen_server_ids:
                    seen_server_ids.add(server_id)
                    filtered_servers.append(server)

        else:
            print(f"Failed to fetch data for {country}, {city}")

        time.sleep(5)  # Wait for 1 minute before making the next call

    return filtered_servers

def json_to_csv(servers, csv_file_path):
    # Open a CSV file for writing
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file)
        header_written = False

        for server in servers:
            if not header_written:
                # Write the header
                header = server.keys()
                csv_writer.writerow(header)
                header_written = True
            # Write the data rows
            csv_writer.writerow(server.values())



# Replace 'sorted_country_city_pairs.csv' with your actual CSV file path
country_city_pairs = read_csv_to_set(city_pairs_file)

# Call the Speedtest API and store the results
speedtest_results = call_speedtest_api_for_pairs(country_city_pairs)

# Saving the results to a JSON file with UTF-8 encoding
with open(json_file_path, 'w', encoding='utf-8') as f:
    json.dump(speedtest_results, f, ensure_ascii=False, indent=4)

# Convert the results to CSV and save it
json_to_csv(speedtest_results, csv_file_path)