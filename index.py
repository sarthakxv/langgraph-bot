from dotenv import load_dotenv
import getpass
import os

load_dotenv()

def _set_env(var: str):
  if not os.environ.get(var):
    print(os.environ)
    os.environ[var] = getpass.getpass(f"Enter {var}: ")
  else :
    print(f"{var} already set")

_set_env("OPENAI_API_KEY")
