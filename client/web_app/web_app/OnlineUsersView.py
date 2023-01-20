import pynecone as pc

from .ChatView import ChatState
from .State import State
from .client import ClientService


class OnlineUsersState(State):
    users = ['a', 'v', 'v', 'd']

    def click(self, username):
        print('clicked')
        service = ClientService()
        if username==self.username+' (You)':
            username=self.username
        service.setClientDistination(username, self.username)
        service.enterChat(ChatState.add_message)
        return pc.redirect('/chat')

    @pc.var
    def getUsers(self) -> list[str]:
        service = ClientService()
        result = service.getOnlineUsers()
        shownResults = {}
        for i, username in enumerate(result):
            if username == self.username:
                shownResults[username] = self.username + ' (You)'
            else:
                shownResults[username] = self.username

        return list(shownResults.values())


def onlineUsers():
    styles = {
        "login_page": {"padding_top": "10em", "text_align": "top", "position": "relative", "background_image": "bg.svg",
                       "background_size": "100% auto", "width": "100%", "height": "100vh", }
    }

    return pc.box(pc.vstack(pc.center(pc.vstack(
        pc.heading('Connected Users:'),
        pc.foreach(OnlineUsersState.getUsers,
                   lambda user: pc.vstack(
                       pc.hstack(
                           pc.avatar(
                               pc.avatar_badge(
                                   box_size="1.25em",
                                   bg="green.500",
                                   border_color="green.500",
                               )
                               , name=user),
                           pc.heading(user),
                       )
                       , pc.divider()
                       , on_click=lambda: OnlineUsersState.click(user)
                   )
                   ),

    ))), style=styles["login_page"])
