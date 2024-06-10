from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time

# Tentukan path ke ChromeDriver
    service = Service('$HOME/dasbor/chromedriver')

    # Tambahkan opsi untuk mengabaikan error sertifikat dan insecure content
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--unsafely-treat-insecure-origin-as-secure=http://10.1.86.28/')
    options.add_argument('--disable-features=InsecureDownloadWarnings')

# Menggunakan DesiredCapabilities untuk mengabaikan kesalahan SSL
capabilities = options.to_capabilities()
capabilities['acceptInsecureCerts'] = True
capabilities['goog:loggingPrefs'] = {'browser': 'ALL'}  # Enable browser logging

# Inisialisasi driver dengan menggunakan service dan opsi
driver = webdriver.Chrome(service=service, options=options)

# Buka halaman
driver.get("http://10.1.86.28/HEAT/")
driver.maximize_window()

wait = WebDriverWait(driver, 30)

# Masukkan username
username_box = driver.find_element(By.NAME, "UserName")
username_box.send_keys("ahmad.rusydi_icon")

# Masukkan password
password_box = driver.find_element(By.NAME, "Password")
password_box.send_keys("Pln@123")

# Pilih tenant dari dropdown
dropdown = Select(driver.find_element(By.ID, "Tenant"))
dropdown.select_by_value("itsm.pln.co.id")

# Klik tombol submit
driver.find_element(By.XPATH, "//button[@type='submit']").click()

# Tunggu beberapa detik
time.sleep(3)

# Klik elemen form div
driver.find_element(By.XPATH, "//form/div[3]").click()

# Klik tombol submit
driver.find_element(By.XPATH, "//button[@type='submit']").click()

# Tunggu beberapa detik
time.sleep(5)

# Klik tombol Incident
driver.find_element(By.XPATH, "(//button[normalize-space()='Incident'])[1]").click()

# Tunggu beberapa detik
time.sleep(10)

try:
    # Debugging: print the page source to check if the iframe is present
    page_source = driver.page_source
    with open("page_source.html", "w", encoding="utf-8") as file:
        file.write(page_source)

    # Check if the iframe is present in the page source
    if 'iframe' in page_source:
        print("Iframe found in the page source")
    else:
        print("Iframe not found in the page source")

    # Increase wait time
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//div[2]/div/div/iframe")))

    # Check if the iframe is switched
    print("Switched to iframe")

    # Perform actions inside the iframe
    driver.find_element(By.XPATH, "//button[@id='ext-gen143']").click()
    print("Button clicked inside iframe")
    time.sleep(5)

    incident_button = driver.find_element(By.XPATH, "//a[@id='ext-comp-1055']")
    action = ActionChains(driver)
    action.move_to_element(incident_button).perform()
    # time.sleep(5)  # Tambahkan waktu tunggu jika diperlukan untuk melihat efek hover
    # driver.find_element(By.XPATH, "//li[@id='x-menu-el-ext-comp-1058']").click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//li[@id='x-menu-el-ext-comp-1058']"))).click()
    print("Hovered and clicked on Incident button")
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "(//button[normalize-space()='Yes'])[1]"))).click()
    # time.sleep(5)
    # driver.find_element(By.XPATH, "(//button[normalize-space()='Yes'])[1]").click()
    print("berhasil download")
    # Switch back to default content
    driver.switch_to.default_content()
    print("Back to default content")
    
except TimeoutException as e:
    print("TimeoutException: iframe not found within the specified time")
    print(e)

# Tunggu beberapa detik
time.sleep(10)

# Tutup browser
driver.quit()
