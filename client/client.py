import logging
import sys
from threading import Thread

from .client_service import ClientService

service = ClientService()
choice = int(input('do you want to:\n 1) signup \n 2) login\n type 1 or 2: '))
if choice == 2:
    authenticated = False
    while (not authenticated):
        username = input('please type your username: ')
        password = input('please type your password: ')
        result = service.authenticate(username, password)
        if result == 0:
            print('[X] Login Successful')
            authenticated = True
        else:
            logging.error('Login Failed: Invalid Credentials')

elif choice == 1:
    success = False
    while not success:
        username = input('please type your username: ')
        password = input('please type your password: ')
        result = service.register(username, password)
        if result == 2:
           logging.error('user already exists')
        elif result == 1:
            print('SERVER ERROR')
        elif result == 0:
            success = True
            print('[X] signup successful')
else:
    sys.exit(4)
service.setClientDistination(None, username)

refresh = True
while refresh:
    users = service.getOnlineUsers()
    print('here is a list of all the connected users:\n')

    for i, name in enumerate(users):
        tmp = ' (YOU)' if name == username else ''
        print(f'{i + 1}) {name}')
    print('type the user\'s number (OR PRESS R TO REFERSH) : ')
    choice = input()
    if choice != 'R':
        refresh = False
choice = int(choice)
dest = users[choice - 1]
service.setClientDistination(dest, username)


def display_incoming(message):
    print('[X] message received:')
    print(message)


service.enterChat(display_incoming)


def read_input():
    while True:
        message = input('\n type in your message: \n')
        service.sendMessage(message)


input_thread = Thread(target=read_input())
input_thread.start()
