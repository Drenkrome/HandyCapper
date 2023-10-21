from time import sleep
from module import build_data

import undetected_chromedriver as uc
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#                      Webdriver settings
# Define a custom user agent
my_user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
# Set up Chrome options
options = uc.ChromeOptions()

options.headless = False
options.add_argument("--window-size=1280,1000")
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-headless")
options.add_argument('--disable-popup-blocking')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--user-agent='+my_user_agent)
# Initialize Chrome WebDriver with the specified magic
driver = uc.Chrome(driver_executable_path="chromedriver", options=options, use_subprocess=True)
driver.set_window_size(900, 1200)
# driver.set_window_position(0, 0)
actions = ActionChains(driver)


def runtest(UI):
    # Echo test
    # driver.get("http://scooterlabs.com/echo.json")
    # print(driver.find_element(By.XPATH, "/html/body").text)
    # Try to get fonbet
    try:
        driver.get("https://www.fon.bet")
        sleep(0.3)
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "header__logo"))
        )
        UI.fon_txt.setText("Stable")
        pass
    except:
        print("Website is unreachable, please check internet connection.")
        UI.fon_txt.setText("Unstable")
    # Try to get betboom
    try:
        driver.get("https://www.betboom.ru/")
        sleep(0.3)
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "Logo__LogoNoLink-sc-1rcsjt6-2"))
        )
        UI.boom_txt.setText("Stable")
    except:
        print("Website is unreachable, please check internet connection.")
        UI.boom_txt.setText("Unstable")
    # Try to get winline
    try:
        driver.get("https://winline.ru/")
        sleep(0.3)
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "header__logo"))
        )
        UI.win_txt.setText("Stable")
    except:
        print("Website is unreachable, please check internet connection.")
        UI.win_txt.setText("Unstable")


def makeurl(UI_STATUS, sport, room):
    build_data.sport = sport
    if room == "fonbet":
        url = "https://www.fon.bet/sports/" + sport
        parse_fonbet(url, UI_STATUS)
    elif room == "betboom":
        url = "https://betboom.ru/sport/" + sport
        parse_betboom(url, UI_STATUS, sport)
    elif room == "winline":
        if sport == "football":
            sport = "futbol"
        elif sport == "hockey":
            sport = "xokkej"
        elif sport == "handball":
            sport = "gandbol"
        url = "https://winline.ru/stavki/sport/" + sport
        parse_winline(url, UI_STATUS)


def parse_fonbet(url, UI):
    # Get sport page
    driver.get(url)
    sleep(5)
    # Focus element for scrolling
    focus = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[4]/div[1]/div/div/div[2]/div"
                                          "/div/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[3]")
    focus.click()
    unfocus = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[4]/div[1]/div/div/div[2]/div"
                                            "/div/div[1]/div/div/div/div[2]/div[2]/div[1]/div/div[1]"
                                            "/div[1]/div[2]/div[3]")
    unfocus.click()
    sleep(2)

    # Scrap full page
    names = []
    count = 0
    errcount = 0
    memory = 0
    while True:
        try:
            name = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[4]/div[1]/div/div/div[2]"
                                                 "/div/div/div[1]/div/div/div/div[2]/div[2]/div[1]/"
                                                 "div/div[1]/div[1]/div[" + str(count) + "]/div[3]/div[1]/a")
            date = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[4]/div[1]/div/div/div[2]"
                                                 "/div/div/div[1]/div/div/div/div[2]/div[2]/div[1]/div/"
                                                 "div[1]/div[1]/div[" + str(count) + "]/div[3]/div[2]/div/span")
            team1 = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[4]/div[1]/div/div/div[2]/"
                                                  "div/div/div[1]/div/div/div/div[2]/div[2]/div[1]/div/"
                                                  "div[1]/div[1]/div[" + str(count) + "]/div[4]")
            both = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[4]/div[1]/div/div/div[2]"
                                                 "/div/div/div[1]/div/div/div/div[2]/div[2]/div[1]/div"
                                                 "/div[1]/div[1]/div[" + str(count) + "]/div[5]")
            team2 = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[4]/div[1]/div/div/div[2]"
                                                  "/div/div/div[1]/div/div/div/div[2]/div[2]/div[1]/div"
                                                  "/div[1]/div[1]/div[" + str(count) + "]/div[6]")

            count += 1
            if (name.text != "" and date.text != "" and team1.text + "|" + both.text + "|" + team2.text != "-|-|-" and
                    "Хозяева" not in name.text):
                names.append("$@$" + name.text + "$@$" + date.text + "$@$" + team1.text +
                             "$@$" + both.text + "$@$" + team2.text + "$@$")
        except:
            count += 1
            errcount += 1
            if errcount > 100:
                if len(names) - memory == 0:
                    print("COMPLETE!")
                    break
                memory = len(names)
                actions.send_keys(Keys.SPACE).perform()
                count = 0
                errcount = 0
                sleep(0.3)
    # Make clear output without doubles etc.
    # List comprehension
    clean_fon = [names[i] for i in range(len(names)) if i == names.index(names[i])]
    UI.statusbar_txt.setText("Fonbet events loading complete!")
    # Send to builder
    build_data.makecsv("fon", clean_fon)


def parse_betboom(url, UI, sport):
    # Get sport page
    driver.get(url)
    driver.set_window_size(1200, 1080)
    sleep(5)
    driver.switch_to.frame(driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/main/div/iframe"))  # iframe
    driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/ul/li[6]").click()  # calendar
    sleep(1.5)
    driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div[2]/div/div[1]/div[2]"  # dropdown
                                  "/div[11]/div/div/div[2]/div[1]/div[2]/div[1]/div[3]/div").click()
    count = 1
    for i in range(0, 50):
        item = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div[2]/div/div[1]/div[2]"
                                             "/div[11]/div/div/div[2]/div[1]/div[2]/div[1]/div[3]"
                                             "/div/div/div[2]/div[1]/div[" + str(count) + "]")
        if sport == "hockey" and item.text == "Хоккей":
            item.click()
            break
        elif sport == "handball" and item.text == "Гандбол":
            item.click()
            break
        elif sport == "football" and item.text == "Футбол":
            item.click()
            break
        else:
            count += 1
    sleep(0.3)
    # Scrap all clickable iframe elements
    count_date = 1
    count_error = 0
    names = []
    lastpage = False
    mem = ""
    for i in range(0, 5):
        if not lastpage:
            # Paneldate
            date = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div[2]/div/div[1]/div[2]/div[11]"
                                                 "/div/div/div[1]/div/div[" + str(count_date) + "]")
            date.click()
            count_time = 1
            for x in range(0, 4):
                try:
                    # Paneltime
                    driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div[2]/div/div[1]/div[2]/div[11]"
                                                  "/div/div/div[2]/div[" + str(count_date) + "]"
                                                  "/div[1]/div[" + str(count_time) + "]").click()
                    count_time += 1
                except:
                    count_time += 1
                # Get line
                sleep(1)
                scrap = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div[2]/div/div[1]/div[2]"
                                                      "/div[11]/div/div/div[2]/div[" + str(count_date) + "]"
                                                      "/div[2]/div[2]/div[1]").text
                if mem != scrap:
                    if "нет данных" in scrap:
                        count_error += 1
                    else:
                        names.append("$@$" + date.text + "\n" + scrap)
                        count_error = 0
                    if count_error >= 5:
                        lastpage = True
                        break
                mem = scrap
            count_date += 1
        else:
            break
    driver.set_window_size(500, 1080)
    # Clean output
    rows = []
    fullrow = ""
    first = False
    # Aggregate raw page to strings
    for page in names:
        elements = page.split("\n")
        for element in elements:
            if ":" in element and first or "$@$" in element and first:
                rows.append(fullrow)
                fullrow = ""
            first = True
            fullrow += element
    # Get events with availible CFs
    clean_boom = []
    for i in rows:
        if i[-3:] != "---" and i[-3:] != "--¥" and i[-3:] != "--Ð" and i[-3:] != "-¥Ð":
            clean_boom.append(i)
    print("COMPLETE!")
    UI.statusbar_txt.setText("Betboom events loading complete!")
    # Send to builder
    build_data.makecsv("boom", clean_boom)


def parse_winline(url, UI):
    # Get sport page
    driver.get(url)
    sleep(5)

    # Focus scroll
    driver.find_element(By.XPATH, "/html/body/ww-desktop-app/div/div[2]/div[1]/div[1]/ww-feature-eventpage-dsk/div[2]"
                                  "/div/ww-feature-block-sport-dsk/div[1]").click()
    # Load dynamic content
    if url[-6:] == "futbol":
        for i in range(0, 25):
            actions.send_keys(Keys.SPACE).perform()
            sleep(0.1)
        sleep(3)
        for i in range(0, 25):
            actions.send_keys(Keys.SPACE).perform()
            sleep(0.1)
        sleep(3)
    else:
        for i in range(0, 50):
            actions.send_keys(Keys.SPACE).perform()
        sleep(3)

    # Get raw
    count_row = 1
    count_error = 0
    raw_output = ""
    while True:
        try:
            raw = driver.find_element(By.XPATH, "/html/body/ww-desktop-app/div/div[2]/div[1]/div[1]"
                                                "/ww-feature-eventpage-dsk/div[2]/div/ww-feature-block-sport-dsk"
                                                "/div[2]/div[" + str(count_row) + "]/ww-feature-block-tournament-dsk"
                                                                                  "/div/div[2]").text
            if "Пер." not in raw and "1Т" not in raw and "2Т" not in raw and "3Т" not in raw:
                raw_output = raw_output + raw + "\n"
            count_row += 1
        except:
            count_error += 1
            if count_error >= 5:
                break
    # Get clean array
    raw_array = raw_output.split("\n")
    count = 0
    clean_winline = []
    for i in raw_array:
        if "Матч" in i:
            t1 = raw_array[count-4]
            t2 = raw_array[count-3]
            if "." in t1 or t1 == "-":
                t1 = raw_array[count-3]
                t2 = raw_array[count-2]
            name = t1 + "-" + t2
            date = raw_array[count-2]
            if ":" not in date:
                date = raw_array[count-1]
            res = [name, date, raw_array[count+1], raw_array[count+2], raw_array[count+3]]
            clean_winline.append(res)
        count += 1
    UI.statusbar_txt.setText("Winline events loading complete!")
    # Send to builder
    build_data.makecsv("win", clean_winline)


def parse_archive(UI, sport, days):
    driver.get("https://www.flashscore.com.ua/")
    driver.set_window_size(1100, 1200)
    sleep(5)
    if sport == "hockey":
        driver.find_element(By.XPATH, "/html/body/nav/div/div[1]/a[2]").click()
        sleep(1)
        driver.find_element(By.XPATH,
                            "/html/body/div[3]/div[1]/div/div/main/div[4]/div[2]/div/div[1]/div[1]/div[5]").click()
    elif sport == "handball":
        driver.find_element(By.XPATH, "/html/body/nav/div/div[1]/a[6]").click()
        sleep(1)
        driver.find_element(By.XPATH,
                            "/html/body/div[3]/div[1]/div/div/main/div[4]/div[2]/div/div[1]/div[1]/div[5]").click()
    elif sport == "football":
        driver.find_element(By.XPATH, "/html/body/nav/div/div[1]/a[1]").click()
        sleep(1)
        driver.find_element(By.XPATH,
                            "/html/body/div[3]/div[1]/div/div/main/div[4]/div[2]/div/div[1]/div[1]/div[5]").click()
    # Grab to archive
    raw_archive = []
    for i in range(0, 10):
        actions.send_keys(Keys.SPACE).perform()
    for i in range(0, 10):
        actions.send_keys(Keys.PAGE_UP).perform()
    for i in range(0, days):
        rows = driver.find_elements(By.XPATH, '//*[@title="Подробности матча!"]')
        # Make links and get raw
        links = []
        for i in rows:
            link = ("https://www.flashscore.com.ua/match/" + i.get_attribute("id")[4:] + "/#/h2h/overall")
            links.append(link)
            actions.send_keys(Keys.ARROW_DOWN).perform()

        mainwindow = driver.current_window_handle
        driver.switch_to.new_window('tab')
        for i in links:
            driver.get(i)
            sleep(0.5)
            # Printing the whole body text
            pagetext = driver.find_element(By.XPATH, "/html").text
            raw_archive.append(pagetext)
            sleep(0.1)
        driver.close()
        sleep(0.2)
        driver.switch_to.window(mainwindow)
        sleep(0.2)
        driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div/div/main/div[4]/div[2]/div/div[1]/div["
                                      "2]/div/button[3]").click()
        sleep(1)
    build_data.make_archive(raw_archive, sport, days)
    UI.statusbar_txt.setText("Archive saved! " + sport + " " + str(days) + " days.")
