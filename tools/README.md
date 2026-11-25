# Gym Coach recovery kit
- `gif-generators/`: Python (Pillow) scripts that draw the muscle-glow exercise GIFs. Run from a folder that has an `img/` subfolder: `python3 make_shoulder.py` writes `img/*.gif` and a contact sheet in /tmp. `make_six.py` holds the shared helpers (mkimg, newov, el, finish, run); other scripts exec its top part. Needs: pip install pillow.
- Session pages are in `sessions/<class>-<date>/index.html` (self-contained, data inside `const EX=[...]` and `const SUM=[...]`).
- Landing page: `index.html` + `class.html` read `sessions.json`.
- Rules, history and skill text: see the Claude project "GYM CLASSES" and the local folder "Claude GYM Sessions DB".
