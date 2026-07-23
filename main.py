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
    link_card_button = (By.XPATH, "//*[contains(text(),'Vincular')]")
    message_input = (By.ID, "comment")
    blanket_checkbox = (By.XPATH, "//*[contains(text(),'Manta y pañuelos')]")
    ice_cream_plus_button = (By.XPATH, "//div[contains(text(),'Helado')]/following::div[contains(@class,'counter-plus')][1]")

    phone_button = (By.XPATH, "//div[contains(text(),'Número de teléfono')]")
    phone_input = (By.ID, "phone")
    phone_confirm_button = (By.XPATH, "//button[contains(text(),'Siguiente')]")
    code_confirm_button = (By.XPATH, "//button[contains(text(),'Confirmar')]")
    code_input = (By.ID, "code")

    def __init__(self, driver):
        self.driver = driver

    def select_comfort(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.comfort_button)
        )
        self.driver.find_element(*self.comfort_button).click()

    def click_order_taxi(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.order_taxi_button)
        )
        self.driver.find_element(*self.order_taxi_button).click()

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
            expected_conditions.visibility_of_element_located(self.code_input)
        )

        self.driver.find_element(*self.code_input).send_keys(code)

        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.code_confirm_button)
        )

        self.driver.find_element(*self.code_confirm_button).click()

    def click_payment_method(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.payment_button)
        )

        self.driver.find_element(*self.payment_button).click()

    def add_card(self, card_number, card_code):
        # Abrir Método de pago
        self.click_payment_method()

        # Esperar botón Agregar una tarjeta
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                self.add_card_button
            )
        )

        self.driver.find_element(
            *self.add_card_button
        ).click()

        import time
        time.sleep(2)

        inputs = self.driver.find_elements(By.TAG_NAME, "input")

        for i in inputs:
            print(
                "INPUT:",
                i.get_attribute("id"),
                "CLASS:",
                i.get_attribute("class"),
                "VISIBLE:",
                i.is_displayed()
            )

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



class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        from selenium.webdriver.chrome.options import Options

        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})

        cls.driver = webdriver.Chrome(options=options)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_select_comfort(self):
        self.driver.get(data.urban_routes_url)

        routes_page = UrbanRoutesPage(self.driver)

        routes_page.set_route(
            data.address_from,
            data.address_to
        )

        routes_page.click_order_taxi()

        routes_page.select_comfort()

        routes_page.add_phone(data.phone_number)

        routes_page.enter_phone_code()

        routes_page.add_card(
            data.card_number,
            data.card_code
        )

        routes_page.add_message(
            data.message_for_driver
        )

        routes_page.select_blanket()

        routes_page.add_ice_cream()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
