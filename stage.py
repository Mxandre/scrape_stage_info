import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium.webdriver.support.ui import Select
import traceback


def initialize_driver():
    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    )
    # options.add_argument("--headless")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.binary_location = (
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    )
    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        return driver
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        return None


def load_cache(file_path):
    if os.path.exists(file_path):
        cache_data = pd.read_csv(file_path)
        return cache_data
    else:
        return pd.DataFrame(columns=["name", "courriel"])


if __name__ == "__main__":

    if True:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "stage.csv")
        cached_data = load_cache(file_path)
        names = cached_data["name"].tolist()
        url = "https://demeter.utc.fr/portal//pls/portal30/STAGES.HISTORIQUE_STAGES_DYN.show"
        driver = initialize_driver()
        driver.get(url)
        name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        name.send_keys("qiudongc")
        password = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        )
        password.send_keys("13570346377Qiu!")
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="fm1"]/button'))
        )
        button.click()
        niveau_stage = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "select#niveau_stage"))
        )
        select = Select(niveau_stage)
        select.select_by_value("ST")
        spec = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "select#spec"))
        )
        select = Select(spec)
        select.select_by_value("GI")
        recherche = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="form_histo"]/div[6]/input[8]')
            )
        )
        recherche.click()
        affich = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="form_histo"]/center[2]/input')
            )
        )
        affich.click()
        # impair_class = WebDriverWait(driver, 10).until(
        #     EC.presence_of_all_elements_located(
        #         (By.CSS_SELECTOR, "tr.impair.txt_actif")
        #     )
        # )
        # pair_class = WebDriverWait(driver, 10).until(
        #     EC.presence_of_all_elements_located(
        #         (By.CSS_SELECTOR, "tr.impair.txt_actif")
        #     )
        # )
        data = {
            "name": [],
            "courriel": [],
            "job": [],
        }
        i = 95

while True:
    try:
        # 等待元素存在并点击
        classe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//*[@id="tbl_body"]/tr[{i}]'))
        )
        # classe = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, ".pair.txt_actif"))
        # )
        classe.click()

        # 等待并获取名字
        name = (
            WebDriverWait(driver, 10)
            .until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="form_histo"]/div[3]/p/span[1]')
                )
            )
            .text
        )

        job = (
            WebDriverWait(driver, 10)
            .until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="form_histo"]/div[1]/h3')
                )
            )
            .text
        )

        # 等待并获取 courriel
        courriel = (
            WebDriverWait(driver, 10)
            .until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="form_histo"]/div[3]/p/span[2]/a')
                )
            )
            .text
        )

        # 等待 retour 按钮
        retour = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="form_histo"]/div[5]/input')
            )
        )
        # if name in names:
        #     i += 1
        #     print(i)
        #     retour.click()
        #     continue
        print(courriel)
        print(name)

        # 点击 retour 按钮
        retour.click()

        # 存储数据
        data["name"].append(name)
        data["courriel"].append(courriel)
        data["job"].append(job)

        # 增加循环变量
        i += 1
        print(i)

    except Exception as e:
        print(f"An error occurred: {e}")
        break

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "stage_with_jobs.csv")
cached_data = load_cache(file_path)
new_data = pd.DataFrame(data)
combined_data = pd.concat([cached_data, new_data], ignore_index=True)
# new_data.to_csv(file_path, index=False)
combined_data.to_csv(file_path, index=False)
print(f"Data saved to {file_path}")
