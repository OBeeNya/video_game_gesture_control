VENV_DIR = env

PIP = $(VENV_DIR)/Scripts/pip
PYTHON = $(VENV_DIR)/Scripts/python

setup: $(VENV_DIR)/Scripts/activate
	$(PIP) install -r requirements.txt

launch: $(VENV_DIR)/Scripts/activate
	@nohup $(PYTHON) app.py > /dev/null 2>&1 &

clean:
	rm -rf $(VENV_DIR)
