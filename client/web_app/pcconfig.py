import pynecone as pc


config = pc.Config(
    app_name="web_app",
    port="5000",

    env=pc.Env.PROD,
)
