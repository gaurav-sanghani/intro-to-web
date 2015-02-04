VENV ?= venv

build: ${VENV}

${VENV}:
	virtualenv ${VENV}
	. ${VENV}/bin/activate; pip install -r requirements.txt

start: build
	. ${VENV}/bin/activate; python server.py --host 0.0.0.0

