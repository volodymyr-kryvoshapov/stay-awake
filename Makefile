PYTHON ?= python3
VENV_DIR ?= .venv
PIP := $(VENV_DIR)/bin/pip
PY := $(VENV_DIR)/bin/python

.PHONY: venv install run build verify clean

venv:
	@if [ ! -f "$(PIP)" ]; then \
		echo "Creating virtual environment..."; \
		rm -rf $(VENV_DIR); \
		$(PYTHON) -m venv $(VENV_DIR); \
	fi

install: venv
	$(PIP) install -r requirements.txt

run: install
	$(PY) stay_awake.py

build: install
	@echo "Cleaning dist folder..."
	rm -rf dist
	$(PIP) install py2app
	$(PY) setup.py py2app
	@echo "Creating DMG staging area..."
	mkdir -p dmg_staging
	cp -r dist/Stay\ Awake.app dmg_staging/
	ln -sf /Applications dmg_staging/Applications
	@echo "Creating DMG..."
	hdiutil create -volname "Stay Awake" -srcfolder dmg_staging -ov -format UDZO dist/Stay\ Awake.dmg
	@echo "Cleaning up..."
	rm -rf dmg_staging dist/Stay\ Awake.app

verify:
	pmset -g assertions

clean:
	rm -rf $(VENV_DIR) build dist *.egg-info
