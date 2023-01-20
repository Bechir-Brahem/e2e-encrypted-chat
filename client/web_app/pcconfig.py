import pynecone as pc


config = pc.Config(
    app_name="web_app",
    api_url="http://localhost:8001",
    port="3001",

    env=pc.Env.DEV,
)
