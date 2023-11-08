init_db:
	python ./setub_db.py

db_interactive: ./db_user_interact.py
	./db_user_interact.py $(ARGS)  # make db_interactive ARGS="-h"
