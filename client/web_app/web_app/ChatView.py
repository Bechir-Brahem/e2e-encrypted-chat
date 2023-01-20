import pynecone as pc

from .State import State
from .client import ClientService


class ChatState(State):
    messages: list[str] = []
    message: str

    def click(self):
        print('chatview CLICK')
        self.messages = self.messages + list([self.message])
        service=ClientService()
        service.sendMessage(self.message)

    def set_message(self, message):
        self.message = message

    def add_message(self, message):
        print('IN CALLBACK')
        self.messages = self.messages + list([message])


styles = {
    "login_page": {"padding_top": "10em", "text_align": "top", "position": "relative", "background_image": "bg.svg",
                   "background_size": "100% auto", "width": "100%", "height": "100vh", },
    "login_input": {"shadow": "lg", "padding": "1em", "border_radius": "lg", "background": "white", },
    "chat_box": {"width": "40vw", "border": "black solid 2px", "border-radius": "2px"}

}


def chat():
    return pc.box(pc.vstack(pc.center(
        pc.vstack(
            pc.span(
                pc.foreach(ChatState.messages, lambda message: pc.vstack(
                    pc.text(message),
                    pc.divider()
                )
                           ), ),
            pc.input(on_blur=ChatState.set_message, placeholder="Message", width="100%"),
            pc.button("send message", on_click=ChatState.click),

            style=styles["login_input"], ), ), ), style=styles["login_page"], )
