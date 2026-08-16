from selenium import webdriver


def create_driver(browser="firefox"):
    try:
        if browser.lower() == "firefox":
            options = webdriver.FirefoxOptions()
            options.add_argument("--start-maximized")
            options.set_preference("intl.accept_languages", "en-US, en")
            return webdriver.Firefox(options=options)
        elif browser.lower() == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            return webdriver.Chrome(options=options)
        else:
            raise ValueError(f"Unsupported browser: {browser}")
    except Exception as e:
        raise RuntimeError(f"Failed to create {browser} driver : {e}")