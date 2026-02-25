#!/usr/bin/env python3
import atexit
import subprocess

import rumps
import Quartz

JIGGLE_INTERVAL_SECONDS = 30
CAFFEINATE_CMD = ["/usr/bin/caffeinate", "-d", "-i"]

# Menu bar icons
IDLE_ICON = "😴"  # Sleeping face
AWAKE_ICON = "☀️"  # Sun


class KeepAwakeApp(rumps.App):
    def __init__(self):
        super().__init__("Stay Awake", title=IDLE_ICON, menu=[], quit_button=None)
        self._enabled = False
        self._proc = None
        self._timer = rumps.Timer(self._jiggle, JIGGLE_INTERVAL_SECONDS)

        self._enable_item = rumps.MenuItem("Enable", callback=self._on_enable)
        self._disable_item = rumps.MenuItem("Disable", callback=self._on_disable)
        self.menu = [
            self._enable_item,
            self._disable_item,
            None,
            rumps.MenuItem("Quit", callback=rumps.quit_application),
        ]

        self._check_accessibility()
        atexit.register(self._stop)
        
        # Enable by default
        self._enable()

    def _check_accessibility(self):
        checker = getattr(Quartz, "AXIsProcessTrusted", None)
        if checker is None:
            return
        if checker():
            return
        rumps.alert(
            "Accessibility permission is required to post synthetic mouse events. "
            "Open System Settings > Privacy & Security > Accessibility and enable it "
            "for the app (or Terminal while developing)."
        )

    def _toggle(self, _):
        if self._enabled:
            self._disable()
        else:
            self._enable()

    def _on_enable(self, _):
        if not self._enabled:
            self._enable()

    def _on_disable(self, _):
        if self._enabled:
            self._disable()

    def _enable(self):
        if not self._proc or self._proc.poll() is not None:
            self._proc = subprocess.Popen(CAFFEINATE_CMD)
        if not self._timer.is_alive():
            self._timer.start()
        self._enabled = True
        self.title = AWAKE_ICON
        self._enable_item.title = "Enabled"
        self._enable_item.state = 1
        self._disable_item.title = "Disable"
        self._disable_item.state = 0

    def _disable(self):
        if self._timer.is_alive():
            self._timer.stop()
        if self._proc and self._proc.poll() is None:
            self._proc.terminate()
            self._proc.wait()
        self._proc = None
        self._enabled = False
        self.title = IDLE_ICON
        self._enable_item.title = "Enable"
        self._enable_item.state = 0
        self._disable_item.title = "Disabled"
        self._disable_item.state = 1

    def _stop(self):
        if self._enabled:
            self._disable()

    def _jiggle(self, _):
        if not self._enabled:
            return
        loc = Quartz.CGEventGetLocation(Quartz.CGEventCreate(None))
        move = Quartz.CGEventCreateMouseEvent(
            None, Quartz.kCGEventMouseMoved, loc, Quartz.kCGMouseButtonLeft
        )
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, move)


if __name__ == "__main__":
    KeepAwakeApp().run()
