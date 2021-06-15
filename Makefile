venv: venv/touchfile

venv/touchfile: requirements.txt
	test -d .venv || python -m venv .venv
	. .venv/bin/activate; pip install -Ur requirements.txt
	. .venv/bin/activate; pip install -Ur requirements-dev.txt
	touch .venv/touchfile

test:
	. .venv/bin/activate; python -m pytest tests

clean:
	rm -rf .venv
	find -iname "*.pyc" -delete
	. .venv/bin/activate; \
	export FLASK_APP=api; \
	export FLASK_ENV=development; \
	export SQLALCHEMY_DATABASE_URI=mysql+pymysql://${username}:${password}@${host}/${database}; \
	flask remove-db;

fix: venv ## Automatically fix style issues
	. .venv/bin/activate; python -m autoflake -ri --remove-all-unused-imports api/ htmlparser/ tests/
	. .venv/bin/activate; python -m isort api/ htmlparser/ tests/
	. .venv/bin/activate; python -m black api/ htmlparser/ tests/

setup:
	. .venv/bin/activate; \
	export FLASK_APP=api; \
	export FLASK_ENV=development; \
	export SQLALCHEMY_DATABASE_URI=mysql+pymysql://${username}:${password}@${host}/${database}; \
	flask init-db;

run:
	. .venv/bin/activate; \
	export FLASK_APP=api; \
	export FLASK_ENV=development; \
	export SQLALCHEMY_DATABASE_URI=mysql+pymysql://${username}:${password}@${host}/${database}; \
	flask run & xterm -e bash -c "mitmproxy -s proxy.py";

