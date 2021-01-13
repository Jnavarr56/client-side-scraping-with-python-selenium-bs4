from os import remove, mkdir, path
from subprocess import Popen
from pathlib import Path
from zipfile import ZipFile
from time import sleep
from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import requests

# ==== BORING CONFIG STUFF STARTS HERE ===:

CHROMEDRIVER_DOWNLOAD_URL = "https://chromedriver.storage.googleapis.com/87.0.4280.88/chromedriver_mac64.zip"
CHROMEDRIVER_FILE_NAME = "chromedriver"
CHROMEDRIVER_FILE_PATH = f'./{CHROMEDRIVER_FILE_NAME}'

chromedriver_missing = not path.exists(CHROMEDRIVER_FILE_PATH)
if chromedriver_missing:

    # Download the chromedriver file contents.
    download_request = requests.get(CHROMEDRIVER_DOWNLOAD_URL)
    downloaded_zipped_file_contents = download_request.content
    # Write the zipped file contents to a zip file.
    zip_file_path = f'./{CHROMEDRIVER_FILE_NAME}.zip'
    zip_file = open(zip_file_path, "wb+")
    zip_file.write(downloaded_zipped_file_contents)
    zip_file.close()
    # Unzip the zip file.
    unzippable_file = ZipFile(zip_file_path)
    unzippable_file.extractall()
    unzippable_file.close()
    # Delete the unneeded zip file.
    remove(zip_file_path)
    # Give the unzipped file executable permission.
    Popen(["chmod", "+x", CHROMEDRIVER_FILE_PATH])


# ==== WEB SCRAPING STUFF STARTS HERE ===:

browser = webdriver.Chrome(CHROMEDRIVER_FILE_PATH)

results_folder_already_exists = path.exists("./results")
if not results_folder_already_exists:
    mkdir("./results")

results_file_name = datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
results_file_path = f'./results/{results_file_name}.csv'
results_file = open(results_file_path, "w+")

results_header_row_vals = [
    "time_(yyyy-m-d)",
    "max_temp_deg_f",
    "avg_temp_deg_f",
    "min_temp_deg_f",
    "max_dew_point_deg_f",
    "avg_dew_point_deg_f",
    "min_dew_point_deg_f",
    "max_dew_humidity_pct",
    "avg_dew_humidity_pct",
    "min_dew_humidity_pct",
    "max_wind_speed_mph",
    "avg_wind_speed_mph",
    "min_wind_speed_mph",
    "max_pressure_hg",
    "avg_pressure_hg",
    "min_pressure_hg",
    "tot_precipitation_in",
]
results_header_row_vals_as_csv = ",".join(results_header_row_vals)
results_file.write(results_header_row_vals_as_csv)


weather_site_base_url = "https://www.wunderground.com/history/monthly/KMSY/date"
year_month_dates = ["2020-11", "2020-12", "2021-1"]


for date in year_month_dates:

    monthly_data_url = f'{weather_site_base_url}/{date}'
    browser.get(monthly_data_url)

    sleep(2)

    monthly_data_page_html_text = browser.page_source
    bsoup = BeautifulSoup(monthly_data_page_html_text, 'html.parser')

    html_table_container = bsoup.find(attrs={"class": "observation-table"})
    html_table = html_table_container.findChild("table")
    html_table_body = html_table.findChild("tbody")
    html_table_columns = html_table_body.findChild(
        "tr").findChildren("td", recursive=False)

    num_rows = len(html_table_columns[0].find_all("tr"))
    row_index = 1

    while row_index < num_rows:

        new_row = ""

        for html_column in html_table_columns:

            html_column_rows = html_column.find_all("tr")
            html_current_column_row = html_column_rows[row_index]

            html_current_column_cells = html_current_column_row.findChildren(
                "td", recursive=False)

            for html_cell in html_current_column_cells:

                is_first_cell_in_row = len(new_row) == 0

                html_cell_content = html_cell.contents[0].strip()

                if is_first_cell_in_row:
                    result_cell_content = f'{date}-{html_cell_content}'
                else:
                    result_cell_content = html_cell_content

                new_row += f'{result_cell_content},'

        new_row = f'\n{new_row[:-1]}'
        results_file.write(new_row)

        row_index += 1

Popen(["open", results_file_path])
results_file.close()
