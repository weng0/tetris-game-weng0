# Tetris Game
Tetris-game ist ein Spiel, das man auf der Konsole eines Computers ausführen kann.

## Installation
Das Klonen dieses Repository mit dem Befehl 'git clone' und der Web-URL funktioniert sowohl unter Windows als auch unter Linux.

Suche zunächst einen passenden Speicherort für das Repository und erstelle dort einen neuen Ordner.
Anschließend wechsle über die Konsole, wie etwa die Windows-Eingabeaufforderung (CMD) oder Bash, mit dem Befehl 'cd' in das gewünschte Verzeichnis.

<img src="https://github.com/weng0/tetris-game-weng0/blob/main/bilder/neue_Ordner.JPG" width=30%>

Für Windows-Nutzern könnte das per CMD so aussehen:

<img src="https://github.com/weng0/tetris-game-weng0/blob/main/bilder/cmd_ordner_gewechselt.JPG" width=40%>

Klone das Repository, indem du das eingibst:
```bash
git clone https://github.com/weng0/tetris-game-weng0.git
```

### Fehlende Curses-Modul nachinstallieren
Das Tetris Spiel funktioniert erst, wenn das entsprechende Modul installiert ist. Insbesondere Windows-Nutzern müssen diesen Schritt ausführen. Gib dazu in der CMD folgenden Befehl ein:
```bash
pip install windows-curses
```

### Issues
Erscheint beim Ausführen des Tetris Spiels diese Fehlermeldung, so muss man den Konsolfenster maximieren:
<img src="https://github.com/weng0/tetris-game-weng0/blob/main/bilder/cmd_fenster_vergroe%C3%9Fern.JPG" width=60%>


## Spiel starten
Um das Spiel zu starten, wechsle in den Ordner tetris-game-weng0 und führe diesen Befehl aus:
```bash
py ./tetris-game.py
```
<img src="https://github.com/weng0/tetris-game-weng0/blob/main/bilder/spiel_beginn.JPG" width=30%>

### Spielregeln

Bei Tetris geht es darum, unterschiedlich geformte Blöcke

<img src="https://github.com/weng0/tetris-game-weng0/blob/main/bilder/formen.JPG" width=40%>

nacheinander auf das Spielfeld fallen zu lassen.
Ziel ist es, zu verhindern, dass sich die Blöcke bis zum oberen Rand des Spielfelds auftürmen.
Dies gelingt, indem man die Blöcke nach links oder rechts bewegt, um passende Lücken zu füllen.

<img src="https://github.com/weng0/tetris-game-weng0/blob/main/bilder/L_R_pfeiltaste.JPG" width=15%>


Sobald man eine passende Lücke gefunden hat, kann man den Block mit der Pfeiltaste nach unten schneller fallen lassen.

<img src="https://github.com/weng0/tetris-game-weng0/blob/main/bilder/U_pfeiltaste.JPG" width=15%>



Wenn durch das Platzieren eines Blocks eine Reihe vollständig gefüllt ist, wird diese aufgelöst und man erhält einen Punkt.
Passt ein Block nicht in die Lücke, kann man ihn rotieren, bis er die richtige Form hat. Zum Rotieren verwende die Taste R.

<img src="https://github.com/weng0/tetris-game-weng0/blob/main/bilder/rotationen.JPG" width=40%>


Will man das Spiel verlassen, so drückt man die Taste 'q'.

## Kommende Updates
- 90° Rotationen bei einigen Blöcken möglich machen (vorhanden am 17.11.2025)
- Einbezug von Gameover, wenn die Blöcke über dem Spielrand hinausragen (vorhanden am 18.11.2025)
- Eingabemöglichkeit für Spielername (vorhanden am 13.01.2026)
- Blöcke fallen automatisch in gleichmäßiger Geschwindigkeit nach unten
- Clean coding