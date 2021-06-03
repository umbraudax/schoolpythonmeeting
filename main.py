from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import json
from os import path


opt = Options()
opt.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1,
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.notifications": 1
  })



def stayExc():
    while True:
        time.sleep(1)

def choices():

    autoJoin = input("Would you like to auto join once a meet has been found? [y/n] ")
    cameraOnDefault = input("Camera on? [y/n] ")
    micOn = input("Mic on? [y/n] ")
    return autoJoin, cameraOnDefault, micOn


def main(autoJoin, cameraOn, micOn):
    driver = webdriver.Chrome(options=opt, executable_path="chromedriver.exe")
    driver.get("https://www.classroom.google.com")
    time.sleep(2)
    classroomButton = driver.find_element_by_xpath('//*[@id="gfe-main-content"]/section[1]/div/div/div/ul/li[2]/a')

    if path.exists("cookies.txt"):
        cookies = open("cookies.txt", 'r').read()
        cookies = json.loads(cookies)
        for cookie in cookies:
            driver.add_cookie(cookie)

    classroomButton.click()
    #print(driver.window_handles)

    if not path.exists("cookies.txt"):
        input("Please login inside of the opened window. Type anything when done. ")
        cookies = driver.get_cookies()
        open("cookies.txt", 'w').write(json.dumps(cookies))

    currentWindowStore = 0
    input("Open up meeting to join. Type anything when done. ")
    #print(driver.window_handles)
    driver.switch_to.window(driver.window_handles[0])
    while (len(driver.window_handles) > 1):
        if currentWindowStore > len(driver.window_handles) - 1:
            currentWindowStore = 0
        if not driver.title == "Something went wrong":
            if not "Meet" in driver.title:
                driver.close()
        driver.switch_to.window(driver.window_handles[currentWindowStore])
        currentWindowStore += 1

    time.sleep(1)

    while True:
        if driver.title == "Something went wrong":
            driver.refresh()
        else:
            break
        time.sleep(5)

    muteButton = driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[2]/div/div[1]/div[1]/div[1]/div/div[4]/div[1]/div/div/div')
    cameraButton = driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[2]/div/div[1]/div[1]/div[1]/div/div[4]/div[2]/div/div')
    joinButton = driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]')

    if cameraOn == 'n':
        cameraButton.click()
    if micOn == 'n':
        muteButton.click()
    if autoJoin == 'y':
        joinButton.click()

    print("If the program ran successfully, it will sit in a running state throughout the duration of your meet. "
          "Please do not close or stop the execution of the program, until your meet is complete, "
          "or else it will close out of the meet.")

    stayExc()

main(*choices())
