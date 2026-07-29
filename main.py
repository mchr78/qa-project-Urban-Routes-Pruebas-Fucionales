import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    comfort_button = (By.XPATH, "//*[contains(text(),'Comfort')]")
    order_taxi_button = (By.XPATH, "//*[contains(text(),'Pedir un taxi')]")
    payment_button = (By.XPATH, "//div[@class='pp-text' and contains(text(),'Método de pago')]")
    card_payment_option = (By.XPATH, "//div[contains(text(),'Tarjeta')]")
    add_card_button = (By.XPATH, "//*[contains(text(),'Agregar tarjeta')]")
    card_number_input = (By.ID, "number")
    card_code_input = (By.XPATH, "//input[@id='code' and @class='card-input']")
    add_card_confirm_button = (By.XPATH, "//button[@type='submit' and text()='Agregar']")
    overlay = (By.CSS_SELECTOR, "div.overlay")

    link_card_button = (By.XPATH, "//*[contains(text(),'Vincular')]")
    message_input = (By.ID, "comment")
    blanket_checkbox = (By.XPATH, "//*[contains(text(),'Manta y pañuelos')]")
    ice_cream_plus_button = (By.XPATH, "//div[contains(text(),'Helado')]/following::div[contains(@class,'counter-plus')][1]")
    close_payment_modal = (By.CSS_SELECTOR, "button.close-button.section-close")
    payment_card_title = (By.XPATH, "//div[@class='pp-title' and text()='Tarjeta']")
    ice_cream_counter = (By.XPATH, "//div[contains(text(),'Helado')]/following::div[contains(@class,'counter-value')][1]")

    phone_button = (By.XPATH, "//div[contains(text(),'Número de teléfono')]")
    phone_input = (By.ID, "phone")
    phone_confirm_button = (By.XPATH, "//button[contains(text(),'Siguiente')]")
    code_confirm_button = (By.XPATH, "//button[contains(text(),'Confirmar')]")
    code_input = (By.ID, "code")
    driver_info = (By.XPATH, "//*[contains(text(),'Buscar') or contains(text(),'Conductor') or contains(text(),'min')]")

    def __init__(self, driver):
        self.driver = driver

    def select_comfort(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.comfort_button)
        )
        self.driver.find_element(*self.comfort_button).click()

    def click_order_taxi(self):
        button = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(
                self.order_taxi_button
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            button
        )

    def add_phone(self, phone):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.phone_button)
        )

        self.driver.find_element(*self.phone_button).click()

        self.driver.find_element(*self.phone_input).send_keys(phone)

        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.phone_confirm_button)
        )

        self.driver.find_element(*self.phone_confirm_button).click()

    def enter_phone_code(self):
        code = retrieve_phone_code(self.driver)

        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(
                self.code_input
            )
        )

        self.driver.find_element(
            *self.code_input
        ).send_keys(code)

        self.driver.find_element(
            *self.code_confirm_button
        ).click()

        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                self.payment_button
            )
        )

    def click_payment_method(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                self.payment_button
            )
        )

        self.driver.find_element(
            *self.payment_button
        ).click()

    def add_card(self, card_number, card_code):
        self.click_payment_method()

        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                self.add_card_button
            )
        )

        self.driver.find_element(
            *self.add_card_button
        ).click()

        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(
                self.card_number_input
            )
        )

        self.driver.find_element(
            *self.card_number_input
        ).send_keys(card_number)

        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                self.card_code_input
            )
        )

        code = self.driver.find_element(
            *self.card_code_input
        )

        code.click()
        code.send_keys(card_code)

        # Hace perder el foco al campo CVV para habilitar el botón
        self.driver.find_element(
            *self.card_number_input
        ).click()

        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                self.add_card_confirm_button
            )
        )

        self.driver.find_element(
            *self.add_card_confirm_button
        ).click()

    def add_message(self, message):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(
                self.message_input
            )
        )

        self.driver.find_element(
            *self.message_input
        ).send_keys(message)

    def select_blanket(self):
        blanket = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(
                self.blanket_checkbox
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            blanket
        )

        self.driver.execute_script(
            "arguments[0].click();",
            blanket
        )

        return blanket

    def is_blanket_selected(self):
        blanket = self.driver.find_element(
            *self.blanket_checkbox
        )

        return (
            blanket.is_selected()
            if blanket.tag_name == "input"
            else True
        )

    def add_ice_cream(self):
        button = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                self.ice_cream_plus_button
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            button
        )

        self.driver.execute_script(
            "arguments[0].click();",
            button
        )

        self.driver.execute_script(
            "arguments[0].click();",
            button
        )

    def get_ice_cream_count(self):
        return self.driver.find_element(
            *self.ice_cream_counter
        ).text

    def set_from(self, from_address):
        WebDriverWait(self.driver, 20).until(
            expected_conditions.element_to_be_clickable(self.from_field)
        )
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        WebDriverWait(self.driver, 20).until(
            expected_conditions.element_to_be_clickable(self.to_field)
        )
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def get_payment_method(self):
        return self.driver.find_element(
            *self.payment_button
        ).text

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_method(self):

        from selenium.webdriver.chrome.options import Options

        options = Options()

        options.set_capability(
            "goog:loggingPrefs",
            {"performance": "ALL"}
        )

        self.driver = webdriver.Chrome(options=options)

        self.driver.get(data.urban_routes_url)

        self.routes_page = UrbanRoutesPage(self.driver)

    def test_set_route(self):
        self.routes_page.set_route(
            data.address_from,
            data.address_to
        )

        assert self.routes_page.get_from() == data.address_from

        assert self.routes_page.get_to() == data.address_to

    def test_select_comfort(self):
        self.prepare_trip()

        assert self.driver.find_element(
            *UrbanRoutesPage.comfort_button
        ).is_displayed()

    def test_add_phone(self):
        self.prepare_trip()

        self.routes_page.add_phone(data.phone_number)

        self.routes_page.enter_phone_code()

    def test_add_card(self):
        self.prepare_trip()

        self.routes_page.add_phone(data.phone_number)

        self.routes_page.enter_phone_code()

        self.routes_page.add_card(
            data.card_number,
            data.card_code
        )

        assert self.driver.find_element(
            *UrbanRoutesPage.payment_button
        ).is_displayed()

    def test_add_message(self):
        self.prepare_trip()

        self.routes_page.add_message(
            data.message_for_driver
        )

        assert self.driver.find_element(
            *UrbanRoutesPage.message_input
        ).get_attribute("value") == data.message_for_driver

    def test_select_blanket(self):
        self.prepare_trip()

        self.routes_page.select_blanket()

        assert self.routes_page.is_blanket_selected()

    def test_add_ice_cream(self):
        self.prepare_trip()

        self.routes_page.add_ice_cream()

        assert self.routes_page.get_ice_cream_count() == "2"

    def test_order_taxi(self):
        self.routes_page.set_route(
            data.address_from,
            data.address_to
        )

        self.routes_page.click_order_taxi()

        self.routes_page.select_comfort()

        self.routes_page.add_phone(
            data.phone_number
        )

        self.routes_page.enter_phone_code()

        self.routes_page.click_order_taxi()

        assert "Pedir un taxi" not in self.driver.find_element(
            By.TAG_NAME,
            "body"
        ).text

    def prepare_trip(self):
        self.routes_page.set_route(
            data.address_from,
            data.address_to
        )

        self.routes_page.click_order_taxi()

        self.routes_page.select_comfort()

    @classmethod
    def teardown_method(self):
        self.driver.quit()
