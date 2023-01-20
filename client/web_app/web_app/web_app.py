"""Welcome to Pynecone! This file outlines the steps to create a basic app."""
import pynecone as pc

from .AuthView import login, signup
from .ChatView import chat
from .OnlineUsersView import onlineUsers
from .State import State

app = pc.App(state=State)
app.add_page(login, path='/')
app.add_page(signup)
app.add_page(onlineUsers, path='users')
app.add_page(chat)
app.compile()
