from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException, JavascriptException, NoSuchElementException

from contextlib import contextmanager
from typing import Final
import traceback
import time

from config import config


NET: Final[list[str]] = [
    config.network.name,
    config.network.rpc_url,
    config.network.chain_id,
    config.network.currency_symbol,
    config.network.block_explorer_url
]


@contextmanager
def wait_for_new_window(driver):
    handles_before = driver.window_handles
    yield
    WebDriverWait(driver, config.driver.delay).until(
        lambda x: len(handles_before) != len(x.window_handles)
    )


@contextmanager
def wait_for_new_element(driver, path):
    yield
    try:
        WebDriverWait(driver, config.driver.delay).until(
            expected_conditions.presence_of_element_located((By.XPATH, path))
        )
    except TimeoutException as error:
        traceback.print_exception(error)
        quit()


def main():
    options = webdriver.ChromeOptions()
    options.add_extension(config.driver.extension_path)
    driver = webdriver.Chrome(options=options)
    time.sleep(1)

    driver.switch_to.window(driver.window_handles[0])

    driver.find_element(by=By.XPATH, value='//button[text()="Get Started"]').click()
    driver.find_element(by=By.XPATH, value='//button[text()="Import wallet"]').click()
    driver.find_element(by=By.XPATH, value='//button[text()="No Thanks"]').click()

    for i in range(len(config.wallet.phrase)):
        driver.find_element(by=By.XPATH, value=f'//*[@id="import-srp__srp-word-{i}"]').send_keys(config.wallet.phrase[i])

    driver.find_element(by=By.XPATH, value='//*[@id="password"]').send_keys(config.wallet.password)
    driver.find_element(by=By.XPATH, value='//*[@id="confirm-password"]').send_keys(config.wallet.password)
    driver.find_element(by=By.XPATH, value='//*[@id="create-new-vault__terms-checkbox"]').click()
    driver.find_element(by=By.XPATH, value='//button[text()="Import"]').click()

    try:
        WebDriverWait(driver, config.driver.delay).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//button[text()="All Done"]'))
        ).click()
    except TimeoutException:
        driver.close()
        quit()

    try:
        div = driver.find_element(by=By.XPATH, value='//div[@id="popover-content"]')
        driver.execute_script('var element = arguments[0]; element.parentNode.removeChild(element);', div)
    except JavascriptException or NoSuchElementException:
        pass

    driver.find_element(by=By.XPATH, value='//span[text()="Ethereum Mainnet"]').click()
    driver.find_element(by=By.XPATH, value='//button[text()="Add Network"]').click()

    fields = driver.find_elements(by=By.XPATH, value='//input[@class="form-field__input"]')
    for i in range(len(fields)):
        fields[i].send_keys(NET[i])

    driver.find_element(by=By.XPATH, value='//button[text()="Save"]').click()

    main_window = driver.current_window_handle

    driver.get(config.faucet.url)

    with wait_for_new_window(driver):
        driver.find_element(by=By.XPATH, value='//span[text()="Connect Wallet"]').click()

    driver.switch_to.window(driver.window_handles[-1])

    try:
        WebDriverWait(driver, config.driver.delay).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//button[text()="Next"]'))
        ).click()
    except TimeoutException:
        driver.close()
        quit()

    driver.find_element(by=By.XPATH, value='//button[text()="Connect"]').click()

    driver.switch_to.window(main_window)

    try:
        WebDriverWait(driver, config.driver.delay).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//div[@class="tg-form__amount"]//div//div'))
        ).click()
    except TimeoutException:
        driver.close()
        quit()

    try:
        WebDriverWait(driver, config.driver.delay).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, f'//img[@alt="{config.faucet.token}"]/parent::div/parent::div')
            )
        ).click()
    except TimeoutException:
        driver.close()
        quit()

    driver.find_element(by=By.XPATH, value='//div[@class="tg-form__amount"]//input').send_keys(config.faucet.amount)

    while True:
        try:
            WebDriverWait(driver, config.driver.delay).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, '//div[text()="test airdrop"]'))
            ).click()
        except TimeoutException:
            driver.close()
            quit()
        time.sleep(65)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
