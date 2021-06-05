from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import requests
import smtplib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from bs4 import BeautifulSoup
import time
from email.message import EmailMessage
import datetime
import os
from selenium.webdriver.chrome.options import Options


app = Flask(__name__)

MY_EMAIL = "hasankarahasanolu@gmail.com"
MY_PASSWORD = "hasan@123"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def get_about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def get_contact():
    if request.method == "POST":
        data = request.form
        print(data["username"])
        print(data["email"])
        print(data["mobile_number"])
        print(data["message"])
        connection = smtplib.SMTP("smtp.gmail.com", 587)
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=MY_EMAIL,
                            msg=f"\n Name : {data['username']}\n Mob No:{data['mobile_number']} \n Message: {data['message']}")
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


@app.route("/automate")
def webscrap():
    chrome_options = Options()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)


    GOOGLE_FORM_LINK = "https://forms.gle/u4VijuqdJdbtYjVN9"

    response = requests.get(
        "https://www.zillow.com/sk/rentals/?searchQueryState=%7B%22mapBounds%22%3A%7B%22west%22%3A-120.20908978125001%2C%22east%22%3A-91.16123821875001%2C%22south%22%3A47.4626585290426%2C%22north%22%3A61.133971108582095%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A5%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A404369%2C%22regionType%22%3A2%7D%5D%2C%22usersSearchTerm%22%3A%22Saskatchewan%22%2C%22schoolId%22%3Anull%7D",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "X-Http-Proto": "HTTP/1.1",
            "X-Real-Ip": "47.9.71.117"})
    all_link = []
    all_price = []
    all_address = []
    soup = BeautifulSoup(response.text, "html.parser")

    link = soup.find_all(name="a", class_="list-card-link")
    for _ in link:
        all_link.append(_.get("href"))

    price = soup.find_all(name="div", class_="list-card-price")
    for _ in price:
        all_price.append(_.text)

    address = soup.find_all(name="address")
    for _ in address:
        all_address.append(_.text)

    print(all_price)
    print(all_link)
    print(all_address)


    driver.get(GOOGLE_FORM_LINK)
    time.sleep(5)

    for _ in range(8):
        input_address = driver.find_element_by_xpath(
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
        input_price = driver.find_element_by_xpath(
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
        input_link = driver.find_element_by_xpath(
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
        submit = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span')

        input_address.send_keys(all_address[_])
        input_price.send_keys(all_price[_])
        input_link.send_keys(all_link[_])
        submit.click()
        driver.get(GOOGLE_FORM_LINK)
        time.sleep(3)

    return render_template("index.html")


@app.route("/automate2")
def instabot():
    chrome_options = Options()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")


    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver_path = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    SIMILAR_ACCOUNT = "burakozcivit"
    USERNAME = "9889602245"
    PASSWORD = "aliraqqu"

    class InstaFollower:

        def __init__(self, path):
            self.driver = path

        def login(self):
            self.driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(5)

            facebook = self.driver.find_element_by_css_selector(".KPnG0")
            facebook.click()
            password = self.driver.find_element_by_id("pass")
            username = self.driver.find_element_by_id("email")

            username.send_keys(USERNAME)
            password.send_keys(PASSWORD)

            time.sleep(2)
            password.send_keys(Keys.ENTER)
            time.sleep(10)

        def find_followers(self):
            time.sleep(5)
            self.driver.get(f"https://www.instagram.com/{SIMILAR_ACCOUNT}")

            time.sleep(2)
            followers = self.driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')
            followers.click()

            time.sleep(2)
            modal = self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]')
            for i in range(10):
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
                time.sleep(2)

        def follow(self):
            all_buttons = self.driver.find_elements_by_css_selector("li button")
            for button in all_buttons:
                try:
                    button.click()
                    time.sleep(1)
                except ElementClickInterceptedException:
                    cancel_button = self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[2]')
                    cancel_button.click()

    bot = InstaFollower(driver_path)
    bot.login()
    bot.find_followers()
    bot.follow()

    return render_template("index.html")


@app.route("/automate3")
def auto_email():
    listner = sr.Recognizer()
    engine = pyttsx3.init()

    def talk(text):
        engine.say(text)
        engine.runAndWait()

    def get_email():
        try:
            with sr.Microphone() as source:
                print('Listening...')
                listner.adjust_for_ambient_noise(source, duration=0.2)
                voice = listner.listen(source, phrase_time_limit=5)
                info = listner.recognize_google(voice)
                print(info)
                return info.lower()

        except:
            pass

    def send_email(receiver, subject, message):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login('ayanrizvi786786@gmail.com', 'ayanrizvi39')
        email = EmailMessage()
        email['From'] = 'ayanrizvi786786@gmail.com'
        email['To'] = receiver
        email['Subject'] = subject
        email.set_content(message)
        server.send_message(email)
        talk('Hey handsome dude your email is send')
        talk('Do you want to send more email')
        send_more = get_email()
        if send_more == "yes":
            get_email_info()
        elif send_more == "no":
            talk("Bye bye have a good day")

    email_list = {
        'aman': 'basilcrouch10@gmail.com',
        'brando': 'brandsonjohnson6@gamil.com'
    }

    def get_email_info():
        talk('To whom you want to send email')

        try:
            name = get_email()
            receiver = email_list[name]
            print(receiver)
            talk('What is the subject of your info')
            subject = get_email()
            talk('Tell me the content of your email')
            message = get_email()
            send_email(receiver, subject, message)

        except:
            pass

    get_email_info()

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

