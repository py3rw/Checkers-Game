from graphics import *
import game

DARK  = "#4A2E1B"   # mahogany
WHEAT = "#F5DEB3"   # wheat
RED_PIECE  = "#c0392b"
BLACK_PIECE = "#2c2c2a"


def draw_start_screen():
    win = GraphWin("Checkers", 600, 600)
    win.setBackground(WHEAT)

    letters   = list("CHECKERS")
    sq_size   = 60          # px per square
    gap       = 4           # gap between squares
    total_w   = len(letters) * sq_size + (len(letters) - 1) * gap
    start_x   = (600 - total_w) // 2   # centre horizontally
    title_y   = 140                     # top edge of the row of squares

    for i, letter in enumerate(letters):
        x1 = start_x + i * (sq_size + gap)
        y1 = title_y
        x2 = x1 + sq_size
        y2 = y1 + sq_size

        is_dark = (i % 2 == 0)
        fill  = DARK  if is_dark else WHEAT
        text_color = WHEAT if is_dark else DARK
        outline_color = DARK if not is_dark else DARK

        sq = Rectangle(Point(x1, y1), Point(x2, y2))
        sq.setFill(fill)
        sq.setOutline(outline_color)
        sq.setWidth(1)
        sq.draw(win)

        lbl = Text(Point(x1 + sq_size // 2, y1 + sq_size // 2), letter)
        lbl.setSize(28)
        lbl.setStyle("bold")
        lbl.setTextColor(text_color)
        lbl.draw(win)

    subtitle = Text(Point(300, 225), "TWO PLAYERS  ·  BY RYAN WU")
    subtitle.setSize(11)
    subtitle.setTextColor("#888780")
    subtitle.draw(win)

    piece_y   = 285
    spacing   = 28
    divider_x = 300

    red_xs   = [divider_x - spacing * 3 + spacing * j for j in range(3)]
    black_xs = [divider_x + spacing       + spacing * j for j in range(3)]

    for x in red_xs:
        p = Circle(Point(x, piece_y), 9)
        p.setFill(RED_PIECE)
        p.setOutline("white")
        p.setWidth(1)
        p.draw(win)

    for x in black_xs:
        p = Circle(Point(x, piece_y), 9)
        p.setFill(BLACK_PIECE)
        p.setOutline("white")
        p.setWidth(1)
        p.draw(win)

    div = Line(Point(divider_x, piece_y - 14), Point(divider_x, piece_y + 14))
    div.setFill("#B4B2A9")
    div.setWidth(1)
    div.draw(win)

    btn1 = Rectangle(Point(200, 340), Point(400, 385))
    btn1.setFill(DARK)
    btn1.setOutline(DARK)
    btn1.draw(win)

    btn1_lbl = Text(Point(300, 362), "New Game")
    btn1_lbl.setSize(14)
    btn1_lbl.setStyle("bold")
    btn1_lbl.setTextColor(WHEAT)
    btn1_lbl.draw(win)

    btn2 = Rectangle(Point(200, 400), Point(400, 445))
    btn2.setFill(WHEAT)
    btn2.setOutline(DARK)
    btn2.setWidth(2)
    btn2.draw(win)

    btn2_lbl = Text(Point(300, 422), "How to Play")
    btn2_lbl.setSize(14)
    btn2_lbl.setTextColor(DARK)
    btn2_lbl.draw(win)

    btn3 = Rectangle(Point(200, 460), Point(400, 505))
    btn3.setFill(WHEAT)
    btn3.setOutline(DARK)
    btn3.setWidth(2)
    btn3.draw(win)

    btn3_lbl = Text(Point(300, 482), "Settings")
    btn3_lbl.setSize(14)
    btn3_lbl.setTextColor(DARK)
    btn3_lbl.draw(win)

    while True:
        click = win.getMouse()
        cx, cy = click.getX(), click.getY()

        if 200 <= cx <= 400 and 340 <= cy <= 385:
            win.close()
            return "new_game"

        if 200 <= cx <= 400 and 400 <= cy <= 445:
            win.close()
            return "how_to_play"

        if 200 <= cx <= 400 and 460 <= cy <= 505:
            win.close()
            return "settings"


def show_how_to_play():
    win = GraphWin("How to Play", 600, 600)
    win.setBackground(WHEAT)

    title = Text(Point(300, 60), "How to Play")
    title.setSize(22)
    title.setStyle("bold")
    title.setTextColor(DARK)
    title.draw(win)

    rules = [
        "Red moves first, then players alternate turns.",
        "Pieces move diagonally on dark squares only.",
        "Capture an enemy by jumping over them.",
        "Chain jumps are allowed in one turn.",
        "Reach the far end to become a King.",
        "Kings can move in any diagonal direction.",
        "Win by capturing all opponent pieces.",
    ]

    for i, rule in enumerate(rules):
        bullet = Text(Point(300, 130 + i * 46), f"·  {rule}")
        bullet.setSize(12)
        bullet.setTextColor(DARK)
        bullet.draw(win)

    back_btn = Rectangle(Point(200, 520), Point(400, 565))
    back_btn.setFill(DARK)
    back_btn.setOutline(DARK)
    back_btn.draw(win)

    back_lbl = Text(Point(300, 542), "Back")
    back_lbl.setSize(14)
    back_lbl.setStyle("bold")
    back_lbl.setTextColor(WHEAT)
    back_lbl.draw(win)

    while True:
        click = win.getMouse()
        cx, cy = click.getX(), click.getY()
        if 200 <= cx <= 400 and 520 <= cy <= 565:
            win.close()
            return


def show_settings(current_settings=None):
    COLOR_PRESETS = ["Default", "Tournament", "Cyberpunk", "Ocean", "Autumn", "Minimalist"]
    MUSIC_TRACKS  = ["Wet Hands", "Pigstep", "Cereal", "Chill Lo-fi", "Mountains", "Clair de Lune"]

    if current_settings is None:
        current_settings = {
            "show_moves": 0,   # index into options list
            "req_jumps":  0,
            "color":      0,   # index into COLOR_PRESETS
            "music":      0,   # index into MUSIC_TRACKS
        }

    # each row: (label, options_list, settings_key)
    rows = [
        ("Show valid moves", ["OFF", "ON"],   "show_moves"),
        ("Require jumps",    ["OFF", "ON"],   "req_jumps"),
        ("Color theme",      COLOR_PRESETS,   "color"),
        ("Music",            MUSIC_TRACKS,    "music"),
    ]

    ROW_Y      = [175, 240, 305, 370]   # y centre of each row
    VALUE_X    = 460                    # x for the value text
    HIT_LEFT   = 100                    # clickable zone x bounds
    HIT_RIGHT  = 500

    win = GraphWin("Settings", 600, 600)
    win.setBackground(WHEAT)

    title = Text(Point(300, 55), "Settings")
    title.setSize(22)
    title.setStyle("bold")
    title.setTextColor(DARK)
    title.draw(win)

    section = Text(Point(300, 115), "GAME OPTIONS")
    section.setSize(10)
    section.setTextColor("#888780")
    section.draw(win)

    Line(Point(100, 130), Point(500, 130)).draw(win)

    for i, (label, options, key) in enumerate(rows):
        y = ROW_Y[i]

        lbl = Text(Point(175, y), label)
        lbl.setSize(13)
        lbl.setTextColor(DARK)
        lbl.draw(win)

        # arrow hint so the user knows it's clickable
        arrow = Text(Point(VALUE_X + 28, y), "›")
        arrow.setSize(14)
        arrow.setTextColor("#888780")
        arrow.draw(win)

        Line(Point(100, y + 25), Point(500, y + 25)).draw(win)

    value_texts = []
    for i, (label, options, key) in enumerate(rows):
        y = ROW_Y[i]
        idx = current_settings[key]
        txt = Text(Point(VALUE_X, y), options[idx])
        txt.setSize(13)
        txt.setStyle("bold")
        txt.setTextColor(DARK)
        txt.draw(win)
        value_texts.append(txt)

    back_btn = Rectangle(Point(200, 520), Point(400, 565))
    back_btn.setFill(DARK)
    back_btn.setOutline(DARK)
    back_btn.draw(win)

    back_lbl = Text(Point(300, 542), "Back")
    back_lbl.setSize(14)
    back_lbl.setStyle("bold")
    back_lbl.setTextColor(WHEAT)
    back_lbl.draw(win)

    while True:
        click = win.getMouse()
        cx, cy = click.getX(), click.getY()

        # back button
        if 200 <= cx <= 400 and 520 <= cy <= 565:
            win.close()
            return current_settings

        # check each row's hit zone (full width, ±25px around row centre)
        for i, (label, options, key) in enumerate(rows):
            y = ROW_Y[i]
            if HIT_LEFT <= cx <= HIT_RIGHT and y - 25 <= cy <= y + 25:
                # advance to next option, wrapping around
                current_settings[key] = (current_settings[key] + 1) % len(options)

                # undraw old value text and draw new one
                value_texts[i].undraw()
                new_txt = Text(Point(VALUE_X, y), options[current_settings[key]])
                new_txt.setSize(13)
                new_txt.setStyle("bold")
                new_txt.setTextColor(DARK)
                new_txt.draw(win)
                value_texts[i] = new_txt
                break


if __name__ == "__main__":
    saved_settings = None
    while True:
        result = draw_start_screen()
        if result == "new_game":
            print("Starting game...")
            print("Settings in use:", saved_settings)
            game.start_game(saved_settings)
        elif result == "how_to_play":
            show_how_to_play()
        elif result == "settings":
            saved_settings = show_settings(saved_settings)
        # all screens loop back to start screen automatically