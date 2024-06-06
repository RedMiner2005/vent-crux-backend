from os import getenv
from pathlib import Path
from dotenv import load_dotenv

class Consts:
    PROCESS_INPUT_KEY="prompt"
    SEND_USER_KEY="toUser"
    SEND_MSG_KEY="message"
    PROMPT_PROPORTION=0.7
    SEED=20102005
    ENV_FILE=".env"
    IS_DEBUG=None
    GROQ_API_KEY=None
    PORT=None

    def __init__(self) -> None:
        env_path = Path.cwd().joinpath(f"{self.ENV_FILE}")
        load_dotenv(dotenv_path=env_path)
        self.IS_DEBUG=getenv("IS_DEBUG")
        print(type(self.IS_DEBUG))
        self.GROQ_API_KEY=getenv("GROQ_API_KEY")
        self.PORT=getenv("PORT")
