import pynecone as pc
class State(pc.State):


    username: str = ""


    def set_username(self, username):
        self.username = username

