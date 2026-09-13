import os

base_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(base_dir, "index.html"), "r", encoding="utf-8") as f:
    html_content = f.read()

with open(os.path.join(base_dir, "dance_practice_player.html"), "w", encoding="utf-8") as f:
    f.write(html_content)

print("Synchronized dance_practice_player.html from index.html successfully.")
