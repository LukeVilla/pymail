# pymail
Pymail is a simple Python email program that allows you to read your email.

# Setup
On the first run, you will need to enter your email and its server.
Example:
```
$ python3 pymail.py
Enter email address: me@example.com
Enter server URL: mail.example.com
```
This will save the configuration info in a file called pymail.ini in the directory you are in.

# Login
After that (and every time the program runs), it will ask you for your password. Enter it to log in.
Example:
```
Enter password: myPa$$
```
# Inbox
When you have logged in, you will see your inbox. It consists of a numbered list of emails. You can only see the subjects of the emails in that view, but you can view the body and sender by typing in the email's number.
Example:
```
0: Link
1: Email Configuration Settings
Enter message number (-1 to exit, -2 to setup): 0
You have chosen message 0 from john.doe@example.com.
Subject: Link
Body text is:
Here's the link you wanted. example.com
Press Enter to exit...
0: Link
1: Email Configuration Settings
Enter message number (-1 to exit, -2 to setup):
```
You can also type -1 to exit or -2 to reconfigure the email connection settings. Example:
```
Enter message number (-1 to exit, -2 to setup): -2
Enter email address: me@example.net
Enter server URL: mail.example.net
0: Email Configuration Settings
Enter message number (-1 to exit, -2 to setup): -1
Exiting...
```
