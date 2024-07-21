VENV_DIR = env

PIP = $(VENV_DIR)/Scripts/pip
PYTHON = $(VENV_DIR)/Scripts/python

setup: $(VENV_DIR)/Scripts/activate
	$(PIP) install -r requirements.txt
	$(VENV_DIR)/Scripts/deactivate

launch: $(VENV_DIR)/Scripts/activate
	$(PYTHON) app.py
	$(VENV_DIR)/Scripts/deactivate

clean:
	rm -rf $(VENV_DIR)
