from database.manager import DBManager
from api.headhunter import HeadHunterAPI
from settings import EMPLOYERS_NAMES


hh_api = HeadHunterAPI()
db_manager = DBManager()

employers = [
    hh_api.get_employer(search_text=text)
    for text in EMPLOYERS_NAMES
]

for employer in employers:
    print(employer.name)
