import requests


def get_sst_data(latitude, longitude, start_date, end_date):
    base_url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data"
    token = "<your_api_token>"  # Replace with your API token from NOAA
    headers = {"token": token}
    dataset_id = "OISST-V2-NOAA"
    data_type_id = "SST"
    location_id = f"POINT({longitude} {latitude})"
    params = {
        "datasetid": dataset_id,
        "datatypeid": data_type_id,
        "locationid": location_id,
        "startdate": start_date,
        "enddate": end_date,
        "units": "metric",
        "limit": 1000  # Adjust limit as per your needs
    }

    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        return response.json()
    except requests.exceptions.HTTPError as e:
        print("HTTP Error:", e)
    except Exception as e:
        print("Error:", e)
    return None


# Example usage
latitude = 40.7128  # Latitude of New York City
longitude = -74.0060  # Longitude of New York City
start_date = "2024-01-01"
end_date = "2024-01-31"

sst_data = get_sst_data(latitude, longitude, start_date, end_date)
print(sst_data)
