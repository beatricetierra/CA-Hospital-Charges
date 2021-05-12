from selenium import webdriver

driver_path = r"C:\Users\Beatrice Tierra\Downloads\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(driver_path)
driver.get('https://google.com')

element = driver.find_element_by_name("q")
element.send_keys("Adventist Health Lodi Memorial")
element.submit()

results = driver.find_elements_by_xpath("//div[@class='g']//div[@class='r']//a[not(@class)]");
for result in results:
    print(result.get_attribute("href"))