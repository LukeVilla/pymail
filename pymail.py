from textual.app import App
from textual import log
from textual.widgets import Footer, Label, TextArea, Welcome, ListItem, Button, ListView, Placeholder
import configparser, os, sys, string
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
def sanitize(localstring):
    out = []
    for char in localstring:
        if char in string.printable:
            out.append(char)
        else:
            log(f"Warning: Character {char} invalid.")
    return "".join(out)
conf = configparser.ConfigParser()
if sys.argv[1] == "-p":
    password = sys.argv[2]
else:
    password = getpass("Enter password: ")
if not os.path.exists("pymail.ini"):
    setup()
conf.read("pymail.ini")
addr = conf["account"]["addr"]
serv = conf["account"]["serv"]
with MailBox(serv).login(addr, password) as mailbox:
    mail = list(mailbox.fetch())
class PyMail(App):
    CSS_PATH = "pymail.tcss"
    def action_html(self):
        self.sanitized_html = sanitize(self.current_html)
        # self.log(self.current_html)
        render(self.sanitized_html)
    def update_label_if_exists(self, widget, new_text, new_id = None):
        if self.query(widget):
            dispwidget = self.query_one(widget)
            dispwidget.update(new_text)
        else:
            self.mount(Label(new_text, id=new_id))
    def handle_select(self,index):
        currmail = mail[index]
        # self.log(currmail.text)
        # self.log(currmail.html)
        self.update_label_if_exists("Label#subject", f"Subject: {currmail.subject}", "subject")
        self.update_label_if_exists("Label#from", f"From: {currmail.from_}\n", "from")
        self.current_html = currmail.html
        if self.query("Button#html"):
            button = self.query_one("Button#html")
            button.disabled = not currmail.html
        else:
            self.mount(Button("View HTML email", id="html", action=f"app.html", disabled=not currmail.html))
        if self.query("TextArea#body"):
            body = self.query_one("TextArea#body")
            if currmail.text:
                body.text = currmail.text
            else:
                body.text = "Only HTML content was found in this email."
        else:
            if currmail.text:
                self.mount(TextArea(text=f"\n{currmail.text}", read_only=True, id="body"))
            else:
                self.mount(TextArea(text=f"\nOnly HTML content was found in this email.", read_only=True, id="body"))
    def on_mount(self):
        pass
    def compose(self):
        subs = []
        for msg in mail:
            subs.append(ListItem(Label(msg.subject)))
        print(subs)
        yield ListView(*subs, id="emails")
        yield Label("Press Ctrl-Q to exit.", id="exit")
    def on_button_pressed(self):
        self.exit()
    def on_list_view_selected(self, event):
        view = self.query_one(ListView)
        self.log(f"Email selected: {view.index}")
        self.handle_select(view.index)
app = PyMail()
app.run()
