import gntp.notifier
import requests
from bs4 import BeautifulSoup
from time import sleep

# More complete example

growl = gntp.notifier.GrowlNotifier(
        applicationName = "Cricket Scores",
        notifications = ["New Updates","New Messages"],
        defaultNotifications = ["New Messages"],
        # hostname = "computer.example.com", # Defaults to localhost
        # password = "abc123" # Defaults to a blank password
)
growl.register()

def show_message(score):
    # Send one message
    image = open('C:\Users\Naqushab\Desktop\cricket\cric.jpg', 'rb').read()
    growl.notify(
            noteType = "New Messages",
            title = "Match Scores",
            description = score,
            icon = image,
            sticky = False,
            priority = 1,
    )
    return

url = "http://static.cricinfo.com/rss/livescores.xml"
while True:
    r = requests.get(url)
    while r.status_code is not 200:
            r = requests.get(url)
    soup = BeautifulSoup(r.text)
    data = soup.find_all("description")
    score = data[1].text
    show_message(str(score))
    sleep(10)

