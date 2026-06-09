def preset_colors(choice):
    color_preset_default = {
        "w_piece":"red",
        "b_piece": "black",
        "light_square":"#F5DEB3", # Light brown
        "dark_square":"#4A2E1B" # Chocolate
    }

    color_preset_tournament = {
        "w_piece": "#FFFFFF",       # White pieces
        "b_piece": "#B22222",       # Firebrick red pieces
        "light_square": "#F0E68C",  # Khaki / Buff
        "dark_square": "#006400"    # Dark Green
    }

    color_preset_cyberpunk = {
        "w_piece": "#00FFFF",       # Neon Cyan pieces
        "b_piece": "#FF00FF",       # Neon Magenta pieces
        "light_square": "#1A1A24",  # Very dark slate
        "dark_square": "#0D0D13"    # Near black
    }

    color_preset_ocean = {
        "w_piece": "#E0F7FA",       # Ice blue pieces
        "b_piece": "#006064",       # Deep teal pieces
        "light_square": "#B2EBF2",  # Soft light teal
        "dark_square": "#00838F",  # Muted dark teal
    }

    color_preset_autumn = {
        "w_piece": "#F4A460",       # Sandy brown pieces
        "b_piece": "#8B0000",       # Dark red pieces
        "light_square": "#D2B48C",   # Tan
        "dark_square": "#5C4033"     # Dark brown
    }

    color_preset_minimalist = {
        "w_piece": "#FAFAFA",       # Off-white pieces
        "b_piece": "#1A1A1A",       # Matte black pieces
        "light_square": "#E0E0E0",  # Light grey
        "dark_square": "#424242"    # Charcoal grey
    }

    themes = {
        1: color_preset_default,
        2: color_preset_tournament,
        3: color_preset_cyberpunk,
        4: color_preset_ocean,
        5: color_preset_autumn,
        6: color_preset_minimalist
    }

    return themes.get(choice, color_preset_default)

def preset_music(music_number): # random music I had downloaded for previous projects
    choices = {
    1:"music/wethands.mp3",
    2:"music/pigstep.mp3",
    3:"music/cereal.mp3",
    4:"music/chilllofi.mp3",
    5:"music/mountains.mp3",
    6:"music/clairedelune.mp3"
    }

    # Looks up the number, defaults to "wethands.mp3" if the number isn't found
    return choices.get(music_number, "music/wethands.mp3")