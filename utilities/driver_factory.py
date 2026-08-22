from selenium import webdriver


def create_driver(browser="firefox"):
    """
    Create and return a Selenium WebDriver instance.

    Supports Firefox and Chrome browsers.

    :param browser: Browser name to launch.
    :return: Configured Selenium WebDriver instance.
    :raises ValueError: If an unsupported browser is provided.
    :raises RuntimeError: If WebDriver creation fails.
    """

    browser = browser.lower()

    try:
        # Step 1: Create Firefox WebDriver
        if browser == "firefox":
            options = webdriver.FirefoxOptions()
            options.add_argument("--start-maximized")
            options.set_preference(
                "intl.accept_languages",
                "en-US, en"
            )

            return webdriver.Firefox(options=options)

        # Step 2: Create Chrome WebDriver
        elif browser == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")

            return webdriver.Chrome(options=options)

        # Step 3: Reject unsupported browsers
        else:
            raise ValueError(f"Unsupported browser: {browser}")

    except ValueError:
        # Step 4: Preserve the original ValueError
        raise

    except Exception as e:
        # Step 5: Convert WebDriver initialization failure
        # into a framework-specific RuntimeError
        raise RuntimeError(
            f"Failed to create {browser} driver: {e}"
        ) from e