"""
This type stub file was generated by pyright.
"""

import threading

"""Graphical monitor of Celery events using curses."""
__all__ = ("CursesMonitor", "evtop")
BORDER_SPACING = ...
LEFT_BORDER_OFFSET = ...
UUID_WIDTH = ...
STATE_WIDTH = ...
TIMESTAMP_WIDTH = ...
MIN_WORKER_WIDTH = ...
MIN_TASK_WIDTH = ...
STATUS_SCREEN = ...

class CursesMonitor:
    """A curses based Celery task monitor."""

    keymap = ...
    win = ...
    screen_delay = ...
    selected_task = ...
    selected_position = ...
    selected_str = ...
    foreground = ...
    background = ...
    online_str = ...
    help_title = ...
    help = ...
    greet = ...
    info_str = ...
    def __init__(self, state, app, keymap=...) -> None: ...
    def format_row(self, uuid, task, worker, timestamp, state): ...
    @property
    def screen_width(self): ...
    @property
    def screen_height(self): ...
    @property
    def display_width(self): ...
    @property
    def display_height(self): ...
    @property
    def limit(self): ...
    def find_position(self): ...
    def move_selection_up(self): ...
    def move_selection_down(self): ...
    def move_selection(self, direction=...): ...
    keyalias = ...
    def handle_keypress(self): ...
    def alert(self, callback, title=...): ...
    def selection_rate_limit(self): ...
    def alert_remote_control_reply(self, reply): ...
    def readline(self, x, y): ...
    def revoke_selection(self): ...
    def selection_info(self): ...
    def selection_traceback(self): ...
    def selection_result(self): ...
    def display_task_row(self, lineno, task): ...
    def draw(self): ...
    def safe_add_str(self, y, x, string, *args, **kwargs): ...
    def init_screen(self): ...
    def resetscreen(self): ...
    def nap(self): ...
    @property
    def tasks(self): ...
    @property
    def workers(self): ...

class DisplayThread(threading.Thread):
    def __init__(self, display) -> None: ...
    def run(self): ...

def capture_events(app, state, display): ...
def evtop(app=...):  # -> None:
    """Start curses monitor."""
    ...

if __name__ == "__main__": ...