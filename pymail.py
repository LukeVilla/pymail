from textual.app import App
from textual.widgets import Footer, Label, Welcome, ListItem, Button, ListView, Placeholder
import configparser, os
from imap_tools import MailBox
from render_html import render_in_browser as render
try:
    from getpass_asterisk.getpass_asterisk import getpass_asterisk as getpass
except ImportError:
    print("Warning: getpass_asterisk not found. Defaulting to getpass.")
    from getpass import getpass

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
password = getpass("Enter password: ")
if not os.path.exists("pymail.ini"):
    setup()
# conffil = open("pymail.ini", "r")
conf.read("pymail.ini")
addr = conf["account"]["addr"]
serv = conf["account"]["serv"]
with MailBox(serv).login(addr, password) as mailbox:
    mail = list(mailbox.fetch())
class PyMail(App):
    CSS_PATH = "pymail.tcss"
    def update_label_if_exists(self, widget, new_text, new_id = None):
        if self.query(widget):
            dispwidget = self.query_one(widget)
            dispwidget.update(new_text)
        else:
            self.mount(Label(new_text, id=new_id))
    def handle_select(self,index):
        currmail = mail[index]
        self.log(currmail)
        self.update_label_if_exists("Label#subject", f"Subject: {currmail.subject}", "subject")
        self.update_label_if_exists("Label#from", f"From: {currmail.from_}", "from")
        self.update_label_if_exists("Label#body", f"{currmail.text}", "body")
        if self.query("Button#html"):
            button = self.query_one("Button#html")
            if not currmail.html:
                button.mount(Button("View HTML email", id="html", disabled=True))
        else:
            self.mount(Button("View HTML email", id="html"))
    def on_mount(self):
        pass
    def compose(self):
        subs = []
        # subs = [ListItem(Label("1")),ListItem(Label("2")),ListItem(Label("3"))]
        for msg in mail:
            subs.append(ListItem(Label(msg.subject)))
        print(subs)
        yield ListView(*subs, id="emails")
        yield Label("Press Ctrl-Q to exit.", id="exit")
        # yield Welcome()
    def on_button_pressed(self):
        self.exit()
    def on_list_view_selected(self, event):
        view = self.query_one(ListView)
        self.log(f"Email selected: {view.index}")
        self.handle_select(view.index)
    # def on_mount(self):
    #     pass
app = PyMail()
app.run()
    # while True:
    #     i = 0
    #     for msg in mail:
    #         print(f"{str(i)}: {msg.subject}")
    #         i += 1
    #     try:
    #         num = int(input("Enter message number (-1 to exit, -2 to setup): "))
    #     except ValueError:
    #         print("Error: Please enter a number.")
    #         pause()
    #         continue
    #     except KeyboardInterrupt:
    #         print("\nExiting...")
    #         break
    #     if num == -1:
    #         print("\nExiting...")
    #         break
    #     if num == -2:
    #         setup()
    #         continue
    #     if not num <= len(mail) - 1:
    #         print("Error: Please enter a listed email number.")
    #         pause()
    #     currmail = mail[num]
    #     print(f"You have chosen message {str(num)} from {currmail.from_}.")
    #     print(f"Subject: {currmail.subject}")
    #     if currmail.html:
    #         print("HTML detected. Attempting to render.")
    #         try:
    #             render(currmail.html)
    #         except Exception as e:
    #             print(f"Error rendering HTML: {e}")
    #             print(currmail.html)
    #     elif currmail.text:
    #         print("Body text: ")
    #         print(currmail.text)
    #     pause()
