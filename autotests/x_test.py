import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

@pytest.fixture
def browser():
    driver = webdriver.Chrome()  # Убедитесь, что у вас установлен ChromeDriver
    yield driver
    driver.quit()

def test_logo_navigation(browser):
    try:
        # 1. Открываем страницу https://welltory.com/plans/
        browser.get("https://welltory.com/plans/")

        # 2. Находим ссылку на логотип
        logo_link = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'ALink_link__cECDm.Header_logoLink__smJHy'))
        )

        # 3. Получаем URL ссылки на логотип
        logo_url = logo_link.get_attribute('href')

        # 4. Проверяем, что URL ссылки на логотип соответствует ожидаемому
        expected_url = "https://welltory.com/"
        assert logo_url == expected_url, f"URL логотипа {logo_url} не соответствует ожидаемому {expected_url}"

        # 5. Кликаем по ссылке на логотип
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'ALink_link__cECDm.Header_logoLink__smJHy'))
        )
        logo_link.click()

        # Добавляем отладочную информацию
        current_url_after_click = browser.current_url
        print(f"Current URL after click: {current_url_after_click}")

        # 6. Проверяем, что переход выполнен успешно и мы находимся на странице авторизации
        expected_auth_url = "https://welltory.com/auth/signin/"
        WebDriverWait(browser, 20).until(EC.url_to_be(expected_auth_url))

        # Повторная проверка текущего URL
        final_url = browser.current_url
        print(f"Final URL after wait: {final_url}")
        assert final_url == expected_auth_url, f"Текущий URL {final_url} не соответствует ожидаемому {expected_auth_url}"

    except TimeoutException as e:
        current_url = browser.current_url
        pytest.fail(f"Test failed due to TimeoutException. Current URL: {current_url}. Exception: {str(e)}")
    except WebDriverException as e:
        pytest.fail(f"Test failed due to WebDriverException: {str(e)}")
    except Exception as e:
        pytest.fail(f"Test failed due to an unexpected exception: {str(e)}")
    finally:
        # 7. Закрываем браузер
        browser.quit()

def test_authorization(browser):
    try:
        # 1. Открываем страницу авторизации
        browser.get("https://app.welltory.com/auth/signin/")

        # 2. Находим поле ввода логина и вводим данные пользователя
        email_field = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, 'email'))
        )
        email_field.send_keys("ilyasoveduard@gmail.com")

        # 3. Находим поле ввода пароля и вводим данные пользователя
        password_field = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, 'password'))
        )
        password_field.send_keys("Erik20041984")

        # 4. Находим кнопку "log in" и кликаем по ней
        login_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'Button_button___CNLX.Button_medium__7YPKB.Button_primary__eweQg.AuthForm_button__SAdqO.mb-8.cy-login-button'))
        )
        login_button.click()

        # 5. Проверяем успешную авторизацию (например, по наличию элемента на странице после авторизации)
        account_icon = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'DesktopMenu_email__dlrsx'))  # Обновите селектор на правильный
        )
        assert account_icon is not None, "Авторизация не выполнена успешно."

    except TimeoutException as e:
        current_url = browser.current_url
        pytest.fail(f"Test failed due to TimeoutException. Current URL: {current_url}. Exception: {str(e)}")
    except WebDriverException as e:
        pytest.fail(f"Test failed due to WebDriverException: {str(e)}")
    except Exception as e:
        pytest.fail(f"Test failed due to an unexpected exception: {str(e)}")
    finally:
        # Закрываем браузер
        browser.quit()

