#!/usr/bin/env python3
"""
Wordle clone with GUI

Wordle clone implemented with pySimpleGUI.

Args:
    None

Returns:
    None

Author: Dennis Byington
Email:  dennisbyington@mac.com
Date:   20 June 2022
"""

import argparse
import json
from datetime import datetime

import matplotlib.pyplot as plt
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --------------------------------------------------------------------


def get_args():
    """Get command-line arguments

    Parses and packages command line arugments into a argparse object based
    on the flags & options initialized within this function.  In this instance, no
    options/flags are set except the default [-h] (help)

    Args:
        None

    Returns:
        parser.parse_args(): An argparse object with members that corrolate to any
        options/flags that are initialized in this function
    """

    parser = argparse.ArgumentParser(
        description="wordle clone",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    return parser.parse_args()


# ---------------------------------------------------------------------


def char_input_box(value, location):
    """Creates a PySimpleGUI text input box

    Creates a PySimpleGUI text input box that with options that are ideal for a grid.
    Uses grid location tuple as key: (row, column))

    Args:
        value:
            String that is the default value for the input box
        location:
            Tuple of the grid location of the text box instance (row, column)

    Returns:
        PySimpleGUI text input box
    """

    return sg.Input(
        value,
        key=location,  # location: (row, column)
        font="Calibri 40",
        text_color="white",
        size=(2, 1),
        border_width=1,
        disabled_readonly_background_color="#1a1a1a",
        background_color="#1a1a1a",
        justification="center",
        pad=2,
        disabled=True,
        enable_events=True,
    )


# ---------------------------------------------------------------------


def keyboard_text_box(letter):
    """Creates a PySimpleGUI text box

    Creates a PySImpleGui text box that with  options that are ideal for a keyboard layout.
    Uses grid location tuple as key: (row, column))

    Args:
        letter:
            String that represents the letter of the keyboard

    Returns:
        PySimpleGUI text input box
    """

    return sg.Text(
        text=letter,
        key=letter,
        font="Calibri 30",
        text_color="white",
        size=(2, 1),
        border_width=0,
        background_color="gray",
        justification="center",
        pad=2,
    )


# ---------------------------------------------------------------------


def get_colors(answer, guess, keyboard):
    """Determines letter colors for guess and keyboard

    Uses the dupe detection algo below to determine the letter colors for both the
    current guess and the keyboard based on the word provided by the user.
    Note: colors = 'green', '#C9B359' (yellow), '#333333' (gray)

    Dupe detection algo (for guess):
        Makes 2 passes over guess:
            1st pass:
                if letter in correct spot: color = green, replace letter with '*'
                Note: this prevents inaccurate coloring during 2nd pass
            2nd pass:
                if letter == '*', skip (has already been set as green)
                if letter in wrong spot: color = yellow, removes this instance from answer
                    Note: this prevents inaccurate coloring if more than 1 remaning instance
                if letter not in answer: color = gray

    Dupe detection algo (for keyboard):
        Makes 1 pass over guess:
                if letter not in answer: color = gray
                if letter in correct spot: color = green
                if letter in wrong spot: color = yellow
        Note: never downgrades (green->yellow or yellow->gray), but can upgrade (yellow->green)

    Inspiration:
        https://stackoverflow.com/questions/71324956/wordle-implementation-dealing-with-duplicate-letters-edge-case


    Args:
        answer:
            String that is the correct word
        guess:
            String that is the guess provided by the user
        keyboard:
            Dictionary that represents the keyboard {letter: color}
            Example: {A: green, B: yellow, C: gray, ...}

    Returns:
        colors:
            List of background colors for guess based on dupe detection algo
        keyboard:
            Updated keyboard dictionary that represents the keyboard {letter: color}
    """

    colors = ["", "", "", "", ""]
    answer_copy = list(answer)  # copy guess and answer into lists (working copies)
    guess_copy = list(guess)

    for i, letter in enumerate(guess_copy):  # 1st guess pass
        if guess_copy[i] == answer_copy[i]:
            colors[i] = "green"
            answer_copy[i] = "*"
            guess_copy[i] = "*"

    for i, letter in enumerate(guess_copy):  # 2nd guess pass
        if letter == "*":
            continue
        elif letter in answer_copy:
            colors[i] = "#C9B359"
            answer_copy.remove(letter)
        else:
            colors[i] = "#333333"

    answer_copy = list(answer)  # re-init variables for keyboard update
    guess_copy = list(guess)

    for i, letter in enumerate(guess_copy):  # update keyboard
        if letter not in answer_copy:
            keyboard[letter] = "#333333"
        elif letter == answer_copy[i]:
            keyboard[letter] = "green"
        elif (letter in answer_copy) and (keyboard[letter] != "green"):
            keyboard[letter] = "#C9B359"

    return colors, keyboard


# ---------------------------------------------------------------------


def update_stats_win(stats, guesses):
    """update game stats after win

    Updates all applicable game statistics if user wins & saves to file

    Args:
        stats:
            Dictionary of statistics: {'tot_games_played': 0,
                                       'tot_games_won': 0,
                                       'win_percent': 0,
                                       'current_streak': 0,
                                       'max_streak': 0,
                                       'guess_distro': [0, 0, 0, 0, 0, 0],
                                       'word_tracker': 0}
        guesses:
            List of Strings: all guesses provided by user so far

    Returns:
        stats:
            Updated dictionary of statistics
    """

    stats["tot_games_played"] += 1

    stats["tot_games_won"] += 1

    stats["win_percent"] = round(
        stats["tot_games_won"] / stats["tot_games_played"] * 100
    )

    if stats["max_streak"] == stats["current_streak"]:
        stats["max_streak"] += 1

    stats["current_streak"] += 1

    stats["guess_distro"][len(guesses) - 1] += 1

    with open("data_files/stats.txt", "w") as f:
        json.dump(stats, f)

    return stats


# ---------------------------------------------------------------------


def update_stats_lose(stats, guesses):
    """update game stats after lose

    Updates all applicable game statistics if user loses & saves to file

    Args:
        stats:
            Dictionary of statistics: {'tot_games_played': 0,
                                       'tot_games_won': 0,
                                       'win_percent': 0,
                                       'current_streak': 0,
                                       'max_streak': 0,
                                       'guess_distro': [0, 0, 0, 0, 0, 0],
                                       'word_tracker': 0}
        guesses:
            List of Strings: all guesses provided by user so far

    Returns:
        stats:
            Updated dictionary of statistics
    """

    stats["tot_games_played"] += 1

    stats["win_percent"] = round(
        stats["tot_games_won"] / stats["tot_games_played"] * 100
    )

    stats["current_streak"] = 0

    with open("data_files/stats.txt", "w") as f:
        json.dump(stats, f)

    return stats


# ---------------------------------------------------------------------


def display_stats(stats, message):
    """Display statistics in secondary window

    Displays the updated statistics in a secondary window after a win or loss.
    Uses drawfigure() to invoke create_bar_graph() to display a graph of the
      guess distro on the canvas portion of the window

    Args:
        stats:
            Dictionary of statistics: {'tot_games_played': 0,
                                       'tot_games_won': 0,
                                       'win_percent': 0,
                                       'current_streak': 0,
                                       'max_streak': 0,
                                       'guess_distro': [0, 0, 0, 0, 0, 0],
                                       'word_tracker': 0}
        message:
            String that indicates win or loss (and correct word if loss)
    """

    def create_bar_graph(stats):
        """Create bar graph

        Creates a pyplot bar graph based on stats argument

        Args:
            stats:
                Dictionary of stats (see above description)

        Returns:
            plt.gcf(): a matplotlib.pyplot object
        """

        plt.figure(figsize=(3.5, 4), facecolor="#1a1a1a")  # create figure
        plt.rc("axes", edgecolor="#1a1a1a")  # black axes
        ax = plt.axes()
        ax.set_facecolor("#1a1a1a")  # black facecolor
        plt.bar(
            [1, 2, 3, 4, 5, 6], stats["guess_distro"], color="green", width=0.5
        )  # bar graph
        plt.title("GUESS DISTRIBUTION", fontsize=14, color="white", pad=20)
        plt.tick_params(bottom=False)  # removes little 'ticks'
        plt.xticks(ticks=[1, 2, 3, 4, 5, 6], color="white")  # numbers for x-axis
        plt.yticks([])  # remove y-ticks

        for i in range(0, 6):  # add y-values to top of each bar
            plt.text(
                i + 1,
                stats["guess_distro"][i],
                stats["guess_distro"][i],
                ha="center",
                color="white",
            )

        return plt.gcf()

    def draw_figure(canvas, figure):
        """Draws bar graph onto canvas

        Unclear how this operates.  Need to research more and update

        Args:
            canvas:
            figure:

        Returns:
            figure_canvas_agg:
        """

        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)

        return figure_canvas_agg

    sg.theme("Default 1")
    sg.theme_background_color(color="#1a1a1a")
    sg.theme_element_background_color(color="#1a1a1a")
    sg.theme_text_element_background_color(color="#1a1a1a")

    # create columns for layout
    first_column = [
        [sg.Text(stats["tot_games_played"], font="Calibri 20", text_color="white")],
        [sg.Text("Played", font="Calibri 16")],
    ]

    second_column = [
        [sg.Text(stats["win_percent"], font="Calibri 20", text_color="white")],
        [sg.Text("Win %", font="Calibri 16")],
    ]

    third_column = [
        [sg.Text(stats["current_streak"], font="Calibri 20", text_color="white")],
        [sg.Text("Current Streak", font="Calibri 16")],
    ]

    fourth_column = [
        [sg.Text(stats["max_streak"], font="Calibri 20", text_color="white")],
        [sg.Text("Max Streak", font="Calibri 16")],
    ]

    layout = [
        [sg.Text(message, font="Calibri 20", text_color="white", pad=20)],
        [
            sg.Column(first_column, element_justification="center"),
            sg.Column(second_column, element_justification="center"),
            sg.Column(third_column, element_justification="center"),
            sg.Column(fourth_column, element_justification="center"),
        ],
        [sg.Text("")],
        [sg.Canvas(size=(1000, 1000), key="-CANVAS-")],
        [sg.Exit()],
    ]

    window = sg.Window(
        "",
        layout,
        finalize=True,
        background_color="#1a1a1a",
        element_justification="center",
        modal=True,
    )

    window.move_to_center()

    draw_figure(window["-CANVAS-"].TKCanvas, create_bar_graph(stats))

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Exit":
            break

    window.close()


# ---------------------------------------------------------------------


def main():
    """Main loop for wordle game

    Handles all internal logic for wordle game.
    Load statistics, loads answers and allow words, inits game variables,
        sets up PySimpleGUI theme, layout and window, and runs event loop.

    Event loop:
        Steps are detailed by comments

    Notes:
        values:
            Dictionary {event: key} --> {(0,0): 'r', (0,1): 'a' ... }

    """

    # ---------------------------------------------------------------------
    # get command line args
    args = get_args()

    # ---------------------------------------------------------------------
    # load stats
    try:
        with open("data_files/stats.txt", "r") as f:
            stats = json.load(f)
    # if no-file and/or invalid-json error: log error and re-init stats
    except (FileNotFoundError, json.decoder.JSONDecodeError) as error:
        with open("data_files/error-log.txt", "a") as f:
            date = datetime.now().strftime("%d-%b-%Y")
            f.write(f"{date}\nstats error: {str(error)}\n\n")
            stats = {
                "tot_games_played": 0,
                "tot_games_won": 0,
                "win_percent": 0,
                "current_streak": 0,
                "max_streak": 0,
                "guess_distro": [0, 0, 0, 0, 0, 0],
                "word_tracker": 0,
            }

            with open("data_files/stats.txt", "w") as f:  # save stats
                json.dump(stats, f)

    # ---------------------------------------------------------------------
    # load answers and allowed words

    all_answers = []
    with open("data_files/all_answers.txt", "r") as f:
        [all_answers.append(line.upper().rstrip()) for line in f]

    allowed_words = []
    with open("data_files/allowed_words.txt", "r") as f:
        [allowed_words.append(line.upper().rstrip()) for line in f]

    # ---------------------------------------------------------------------

    # variables for game play
    current_row = 0  # to track if all five letters entered
    guesses = []  # list of guesses
    keyboard = dict.fromkeys(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
    answer = all_answers[stats["word_tracker"]]

    # inc tracker# if > 2315, reset tracker
    stats["word_tracker"] += 1
    if stats["word_tracker"] > 2314:
        stats["word_tracker"] = 0

    # ---------------------------------------------------------------------
    # game setup

    # set theme (system default)
    sg.theme("Default 1")

    # concatenate the layout
    layout = [
        [
            [char_input_box("", (row, col)) for col in range(0, 5)]
            for row in range(0, 6)
        ],
        [sg.Text(background_color="#1a1a1a")],
        [keyboard_text_box(letter) for letter in "QWERTYUIOP"],
        [keyboard_text_box(letter) for letter in "ASDFGHJKL"],
        [keyboard_text_box(letter) for letter in "ZXCVBNM"],
        [sg.Text(background_color="#1a1a1a")],
        [sg.B("Enter", visible=False, bind_return_key=True)],
    ]

    # create window, enable first row, bind backspace key
    window = sg.Window(
        "WORDLE CLONE v1.0",
        layout,
        margins=(20, 20),
        finalize=True,
        element_justification="center",
        background_color="#1a1a1a",
    )

    window.move_to_center()

    [window[(0, col)].update(disabled=False) for col in range(0, 5)]
    window.bind("<BackSpace>", "-BACKSPACE-")

    # ---------------------------------------------------------------------
    # event loop

    while True:

        event, values = window.read()

        # if event is in an input box, event will be tuple of grid location: (row, column)
        if isinstance(event, tuple):

            # get location data from event
            row, col = event

            # if input is letter and in columns 1-3: uppercase & move focus to next block
            if (values[row, col].isalpha()) and (col in range(0, 4)):
                window[row, col].update(values[row, col].upper())
                window[row, col + 1].set_focus()

            # if input is letter and in column 4: keep current letter (uppercase) and don't move
            elif (values[row, col].isalpha()) and (col == 4):
                window[row, col].update(
                    values[row, col][0].upper()
                )  # convert to uppercase, delete all but first letter

            # if input is not letter: delete it and stay in current block
            elif not (values[row, col].isalpha()):
                window[row, col].update("")

        # elif enter and do have five letters: join into string and check if valid
        elif (event == "Enter") and (values[current_row, 4] != ""):
            guess = "".join(values[current_row, col] for col in range(0, 5))

            # if not valid word: send error, blank row, reset focus to first column
            if (guess not in all_answers) and (guess not in allowed_words):
                [window[current_row, col].update("") for col in range(0, 5)]
                window[current_row, 0].set_focus()
                sg.popup(
                    "Word not recognized",
                    font="Calibri 30",
                    auto_close=True,
                    auto_close_duration=1,
                )

            # if correct, color row green, update keyboard, & display win message
            elif guess == answer:
                guesses.append(guess)
                colors, keyboard = get_colors(answer, guess, keyboard)
                [
                    window[current_row, col].update(
                        background_color="green", text_color="white"
                    )
                    for col in range(0, 5)
                ]
                [
                    window[letter.upper()].update(background_color=keyboard[letter])
                    for letter in keyboard
                ]
                update_stats_win(stats, guesses)
                display_stats(stats, "YOU WIN!")
                break

            # if wrong, get letter colors and update backgrounds and keyboard
            else:
                guesses.append(guess)
                colors, keyboard = get_colors(answer, guess, keyboard)
                [
                    window[current_row, column].update(background_color=colors[column])
                    for column, color in enumerate(colors)
                ]
                [
                    window[letter.upper()].update(background_color=keyboard[letter])
                    for letter in keyboard
                ]

                # if guesses left: move to next row
                if current_row < 5:
                    current_row += 1
                    [
                        window[(current_row, col)].update(disabled=False)
                        for col in range(0, 5)
                    ]
                    window[current_row, 0].set_focus()

                # if no gueses left: end game
                else:
                    update_stats_lose(stats, guesses)
                    display_stats(stats, "YOU LOSE!  The answer was: " + answer)
                    break

        # if enter and do not have five letters: send error
        elif (event == "Enter") and (values[current_row, 4] == ""):
            sg.popup(
                "Not enough letters",
                font="Calibri 25",
                auto_close=True,
                auto_close_duration=1,
            )

        # if backspace, delete letters in row and start over
        elif event == "-BACKSPACE-":
            [window[current_row, i].update("") for i in range(0, 5)]
            window[current_row, 0].set_focus()

        # if red close button
        elif event == sg.WIN_CLOSED:
            break

    window.close()


# ---------------------------------------------------

if __name__ == "__main__":
    main()
