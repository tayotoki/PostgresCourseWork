from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path(__file__).resolve().parent.parent / ".env"

if dotenv_path.exists():
    load_dotenv(dotenv_path)
