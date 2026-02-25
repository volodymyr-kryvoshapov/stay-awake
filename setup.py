from setuptools import setup

OPTIONS = {
    "argv_emulation": True,
    "plist": {"LSUIElement": True},
    "packages": ["rumps", "Quartz"],
    "iconfile": "stay_awake.icns",
}

setup(
    app=["stay_awake.py"],
    name="Stay Awake",
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
