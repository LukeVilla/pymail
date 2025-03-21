
import configparser, os
from imap_tools import MailBox

def setup():
    addr = input("Enter email address: ")
    serv = input("Enter server URL: ")
    conf["account"] = {"addr":addr, "serv":serv}
    with open("pymail.ini", "w") as mconf:
        conf.write(mconf)
def pause():
    print("Press Enter to exit.")
    _ = input("")
conf = configparser.ConfigParser()
password = input("Enter password: ")
if not os.path.exists("pymail.ini"):
    setup()
# conffil = open("pymail.ini", "r")
conf.read("pymail.ini")
addr = conf["account"]["addr"]
serv = conf["account"]["serv"]
with MailBox(serv).login(addr, password) as mailbox:
    mail = list(mailbox.fetch())
    while True:
        i = 0
        for msg in mail:
            print(f"{str(i)}: {msg.subject}")
            i += 1
        try:
            num = int(input("Enter message number (-1 to exit, -2 to setup): "))
        except ValueError:
            print("Error: Please enter a number.")
            pause()
            continue
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        if num == -1:
            print("\nExiting...")
            break
        if num == -2:
            setup()
            continue
        if not num <= len(mail) - 1:
            print("Error: Please enter a listed email number.")
            pause()
        print(f"You have chosen message {str(num)} from {mail[num].from_}.")
        print(f"Subject: {mail[num].subject}")
        print("Body text: ")
        if mail[num].text:
            print(mail[num].text)
        elif mail[num].html:
            print(mail[num].html)
        pause()
