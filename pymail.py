
from imap_tools import MailBox
import configparser, os

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
# Get date, subject and body len of all emails from INBOX folder
print("InByte v1.0")
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
		elif num == -2:
			setup()
			continue
		print(f"You have chosen message {str(num)}. Body text is:")
		try:
			print(mail[num].text)
			pause()
		except:
			print("Error: Please enter a listed email number.")
			pause()