# Simple Python Chat

A very simple chat program in Python that uses UDP broadcasting to send messages between computers on the same network.

Intended purely for educational purposes.

## Content

* `chat.py` - This module contains the main logic of the program and is intended to be created/edited by the student.

* `client.py` - Utility module that hides some of the complexity of Python networking.
* `terminal.py` - Utilities module that hides some of the complexity of the curses library.
* `main.py` - Entry point script that invokes `chat.py` inside a curses wrapper to perform set-up and tear-down.

To run:

    python3 main.py
