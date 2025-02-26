import time
import csv

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


chrome_options = uc.ChromeOptions()
chrome_options.add_argument("--start-maximized")
driver = uc.Chrome(options=chrome_options)

driver.get(
    "https://www.accuweather.com/en/ng/akure/254733/daily-weather-forecast/254733"
)

# Find Weekly Forecast wrapper
weekly_forecast = driver.find_element(
    By.XPATH, ".//div[@class='page-content content-module']"
)
# Scroll to element
driver.execute_script("arguments[0].scrollIntoView(true);", weekly_forecast)

# Find all days
dayily_wrappers = weekly_forecast.find_elements(
    By.XPATH, ".//div[@class='daily-wrapper']"
)

with open("weather.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(
        [
            "Day",
            "Date",
            "High",
            "Low",
            "Precipitation",
            "RealFeel",
            "RealFeel Shade",
            "Max UV Index",
            "Wind",
        ]
    )

for wrapper in dayily_wrappers:
    # Find Info
    date_object = wrapper.find_element(
        By.XPATH, ".//div[@class='info']//h2[@class='date']"
    )
    # Scroll to element
    driver.execute_script("arguments[0].scrollIntoView(true);", date_object)
    day = date_object.find_element(
        By.XPATH, ".//span[@class='module-header dow date']"
    ).text
    date = date_object.find_element(
        By.XPATH, ".//span[@class='module-header sub date']"
    ).text
    temp_object = wrapper.find_element(
        By.XPATH, ".//div[@class='info']//div[@class='temp']"
    )
    temp_high = temp_object.find_element(By.XPATH, ".//span[@class='high']").text
    temp_low = temp_object.find_element(By.XPATH, ".//span[@class='low']").text
    precip = wrapper.find_element(By.XPATH, ".//div[@class='precip']").text

    # Find RealFeel, RealFeel Shade, Max UV Index, Wind from Panel object
    panel = wrapper.find_element(By.XPATH, ".//div[@class='panels']")

    # Dealing with left panel
    left_panel_objects = panel.find_elements(
        By.XPATH, ".//div[@class='left']/p[@class='panel-item']"
    )
    left_panel_text = []
    for obj in left_panel_objects:
        obj_span = obj.find_element(By.XPATH, ".//span[@class='value']")
        left_panel_text.append(obj_span.text)
    real_feel = left_panel_text[0]
    real_feel_shade = left_panel_text[1]

    # Dealing with right panel
    right_panel_objects = panel.find_elements(
        By.XPATH, ".//div[@class='right']/p[@class='panel-item']"
    )
    right_panel_text = []
    for obj in right_panel_objects:
        obj_span = obj.find_element(By.XPATH, ".//span[@class='value']")
        right_panel_text.append(obj_span.text)
    max_uv_index = right_panel_text[0]
    wind = right_panel_text[1]

    with open("weather.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                day,
                date,
                temp_high,
                temp_low,
                precip,
                real_feel,
                real_feel_shade,
                max_uv_index,
                wind,
            ]
        )

    print(f"Extracted data for {day}, {date}")


driver.quit()
