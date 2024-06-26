"""
This module contains the GUI class which is used to create the GUI window and display the game.
"""

import tkinter as tk  # Importing the tkinter module for the GUI window
import os  # Importing the os module to get the current directory
import CE as ce  # Importing the chess engine module
import C2M as c2m  # Importing the camera to moves module
import DrDRA as dr  # Importing the arm module
import webbrowser  # Importing the webbrowser module to open webpages

cwd = os.getcwd()  # Getting the current directory
cwd = cwd + "/.."  # Going up one directory to the main folder

stockfish_path = (
    cwd + "/stockfish/stockfish-windows-2022-x86-64-avx2.exe"
)  # Setting the path to the stockfish engine

cell_coordinates_path = (
    cwd + "/Calibration Files/Calibration.xml"
)  # Setting the path to the cell coordinates file

DRLCE_weights_path = (
    cwd + "/DRLCE/weights/AlphaZeroNet_20x256.pt"
)  # Setting the path to the DRLCE weights file

motherboard_path = (
    cwd + "/Images/Motherboard.jpg"
)  # Setting the path to the motherboard image

gui_logo_path = cwd + "/Images/icon.ico"  # Setting the path to the GUI logo image

fen_csv_path = cwd + "/FEN Data/chess_games_fen.csv"  # Setting the path to the fen csv

bg_color = "#302e2b"  # Setting the background color of the GUI window
player_txt_color = (
    "#9cdc5b"  # Setting the text color of the GUI window if the timer is for the player
)
engine_txt_color = (
    "#fa732c"  # Setting the text color of the GUI window if the timer is for the engine
)
btn_bg_color = "#7c766f"  # Setting the background color of the button
btn_bg_active_color = (
    "#999691"  # Setting the background color of the button when active
)
main_txt_color = "#e4e2dd"  # Setting the text color of the button
link_txt_color = "#159acd"  # Setting the text color of the link
entry_bg_color = "#c3c2c2"  # Setting the background color of the entry


class chess_game:
    def __init__(self, master: tk.Tk):
        self.player_turn = (
            True  # Creating a boolean variable to keep track of whose turn it is
        )
        self.time_left_engine = (
            10 * 60000  # Creating a variable to keep track of the engine's time left
        )
        self.time_left_player = (
            10 * 60000  # Creating a variable to keep track of the player's time left
        )
        self.update_every_ms = (
            1  # Creating a variable to keep track of how often to update the clock
        )

        self.cam_id = 0  # Setting the camera id

        self.cam_id_tk = (
            tk.StringVar()
        )  # Creating a tkinter string variable to keep track of the camera id

        self.fen_string = (
            "8/6N1/4Q3/8/7q/3K2k1/8/8 w - - 0 1"  # Setting the fen string of the board
        )

        self.random_fen = (
            True  # Creating a boolean variable to keep track of the random fen option
        )

        self.fen_tk = (
            tk.StringVar()
        )  # Creating a tkinter string variable to keep track of the fen string

        self.dobot_cam = c2m.init_cam(self.cam_id)  # Initializing the camera

        # self.arm = dr.init_arm(cell_coordinates_path)  # Initializing the arm # Test

        self.homography_matrix = (
            []
        )  # Creating a variable to keep track of the homography matrix

        self.player_move = ""  # Creating a variable to keep track of the player's move

        self.engine_move = ""  # Creating a variable to keep track of the engine's move

        self.difficulty = 0  # Creating a variable to keep track of the difficulty level

        self.engine = ce.init_stockfish(stockfish_path)  # Initializing the engine

        self.board = (
            ce.init_board()
        )  # Creating a chess board object to keep track of the board

        self.chess_move_indicators = (
            False,
            False,
            False,
        )  # Creating a variable to keep track of the chess move indicators (kill, enpassant, castling)

        self.game_state = 0  # 0 = in progress, 1 = black won, 2 = white won, 3 = draw

        self.master = master  # Creating a master window object

        self.master.title("Hikaru Nakarmsen")  # Setting the title of the GUI window

        self.master.resizable(False, False)  # Making the GUI non-resizable

        self.master.configure(bg=bg_color)  # Set the background color of the window

        # Making the GUI window fullscreen
        self.master.attributes("-fullscreen", True)

        self.game_logo_tk = c2m.cv2_to_tk(
            gui_logo_path  # type: ignore
        )  # Convert the logo image to a tkinter image

        self.sound = True  # Creating a boolean variable to keep track of the sound

        self.master.iconbitmap(
            gui_logo_path
        )  # Setting the icon of the GUI window if the timer is for the engine

        self.init_widgets()  # Calling the init_widgets method to initialize the widgets

        self.init_fen()  # Calling the init_fen method to initialize the fen string

        self.display_main_menu()  # Calling the display_main_menu method to display the main menu

    def init_widgets(self):
        self.title_label = tk.Label(
            self.master,
            text="Hikaru Nakarmsen",
            font=("Courier", 50, "bold"),
            bg=bg_color,
            fg=main_txt_color,
        )  # Creating a label to display the title of the game

        self.difficulty_label = tk.Label(
            self.master,
            text="Empty the Chessboard,\nthen Select the Difficulty ",
            font=("Courier", 40, "bold"),
            bg=bg_color,
            fg=main_txt_color,
        )  # Creating a label to display the difficulty level

        self.instructions_label = tk.Label(
            self.master,
            text="Instructions:",
            font=("Courier", 40, "bold"),
            bg=bg_color,
            fg=main_txt_color,
        )  # Creating a label to display the instructions title

        self.settings_label = tk.Label(
            self.master,
            text="Settings:",
            font=("Courier", 40, "bold"),
            bg=bg_color,
            fg=main_txt_color,
        )  # Creating a label to display the settings title

        self.initial_position_label = tk.Label(
            self.master,
            text="Daily Puzzle's\nInitial Board Position",
            font=("Courier", 20, "bold"),
            bg=bg_color,
            fg=main_txt_color,
        )  # Creating a label to display the text "Initial Board Position"

        self.start_game_label = tk.Label(
            self.master,
            text="Place the Pieces on the Board,\nthen Press Start Game",
            font=("Courier", 35, "bold"),
            bg=bg_color,
            fg=main_txt_color,
        )  # Creating a label to display the start game instructions

        # Creating 5 labels to display the difficulty description
        self.difficulty_easy_desc = tk.Label(
            self.master,
            text="Easy:\nDepth = 5\nSkill Level = 5",
            font=("Courier", 15, "bold"),
            bg=bg_color,
            fg=main_txt_color,
        )

        self.difficulty_meduim_desc = tk.Label(
            self.master,
            text="Medium:\nDepth = 10\nSkill Level = 10",
            font=("Courier", 15, "bold"),
            bg=bg_color,
            fg=main_txt_color,
        )

        self.difficulty_hard_desc = tk.Label(
            self.master,
            text="Hard:\nDepth = 15\nSkill Level = 15",
            font=("Courier", 15, "bold"),
            bg=bg_color,
            fg=main_txt_color,
        )

        self.difficulty_souls_desc = tk.Label(
            self.master,
            text="Souls:\nDepth = 20\nSkill Level = 20",
            font=("Courier", 15, "bold"),
            bg=bg_color,
            fg=main_txt_color,
        )

        self.difficulty_DRLCE_desc = tk.Label(
            self.master,
            text="DRLCE:\nDeep Reinforcement\nLearning Chess Engine",
            font=("Courier", 15, "bold"),
            bg=bg_color,
            fg=main_txt_color,
        )

        self.label_player = tk.Label(
            self.master,
            text="Time Left for\nThe Player",
            font=("Courier", 20, "bold"),
            bg=bg_color,
            fg=player_txt_color,
        )  # Creating a label to display the text "Player Time Left"

        self.label_time_player = tk.Label(
            self.master,
            text="",
            font=("Courier", 20, "bold"),
            bg=bg_color,
            fg=player_txt_color,
        )  # Creating a label to display the player's time left

        self.label_engine = tk.Label(
            self.master,
            text="Time Left for\nThe Engine",
            font=("Courier", 20, "bold"),
            bg=bg_color,
            fg=engine_txt_color,
        )  # Creating a label to display the text "Engine Time Left"

        self.label_time_engine = tk.Label(
            self.master,
            text="",
            font=("Courier", 20, "bold"),
            bg=bg_color,
            fg=engine_txt_color,
        )  # Creating a label to display the engine's time left

        self.prev_img_label = tk.Label(
            self.master,
            text="Previous Board Image",
            font=("Courier", 20, "bold"),
            bg=bg_color,
            fg=main_txt_color,
        )  # Creating a label to display the text "Previous Board Image"

        self.curr_img_label = tk.Label(
            self.master,
            text="Current Board Image",
            font=("Courier", 20, "bold"),
            bg=bg_color,
            fg=main_txt_color,
        )  # Creating a label to display the text "Current Board Image"

        self.virtual_img_label = tk.Label(
            self.master,
            text="Virtual Board Image",
            font=("Courier", 20, "bold"),
            bg=bg_color,
            fg=main_txt_color,
        )  # Creating a label to display the text "Virtual Board Image"

        self.youssef_label = tk.Label(
            self.master,
            text="Mohamed Youssef's\nGithub",
            font=("Courier", 20, "bold", "underline"),
            bg=bg_color,
            fg=link_txt_color,
            cursor="hand2",
        )  # Creating a label to display the text "Mohamed Youssef's Github"

        self.youssef_label.bind(
            "<Button-1>", lambda e: webbrowser.open_new("https://github.com/Momad-Y")
        )  # Binding the label to open the github page when clicked

        self.hazem_label = tk.Label(
            self.master,
            text="Hazem Abdelghafar's\nGithub",
            font=("Courier", 20, "bold", "underline"),
            bg=bg_color,
            fg=link_txt_color,
            cursor="hand2",
        )  # Creating a label to display the text "Hazem Mohamed's Github"

        self.hazem_label.bind(
            "<Button-1>",
            lambda e: webbrowser.open_new("https://github.com/HazemAbdelghafar"),
        )  # Binding the label to open the github page when clicked

        self.raheem_label = tk.Label(
            self.master,
            text="Mohamed Abdulrahim's\nGithub",
            font=("Courier", 20, "bold", "underline"),
            bg=bg_color,
            fg=link_txt_color,
            cursor="hand2",
        )  # Creating a label to display the text "Mohamed Abdelraheem's Github"

        self.raheem_label.bind(
            "<Button-1>", lambda e: webbrowser.open_new("https://github.com/vdyy24")
        )  # Binding the label to open the github page when clicked

        self.input_fen_label = tk.Label(
            self.master,
            text="Load Chessboard from custom FEN",
            font=("Courier", 20, "bold"),
            bg=bg_color,
            fg=main_txt_color,
        )  # Creating a label to display the text "Load Chessboard from custom FEN"

        self.input_cam_id_label = tk.Label(
            self.master,
            text="Input the Camera ID:",
            font=("Courier", 20, "bold"),
            bg=bg_color,
            fg=main_txt_color,
        )  # Creating a label to display the text "Input the Camera ID"

        self.input_cam_btn = tk.Button(
            self.master,
            text="Submit Camera ID",
            command=self.submit_cam,
            background=btn_bg_color,
            foreground=main_txt_color,
            activebackground=btn_bg_active_color,
            activeforeground=main_txt_color,
            height=1,
            width=18,
            border=0,
            cursor="hand2",
            font=("Courier", 14, "bold"),
        )  # Creating a button to submit the camera id

        self.input_fen_btn = tk.Button(
            self.master,
            text="Submit Custom FEN",
            command=self.submit_fen,
            background=btn_bg_color,
            foreground=main_txt_color,
            activebackground=btn_bg_active_color,
            activeforeground=main_txt_color,
            height=1,
            width=20,
            border=0,
            cursor="hand2",
            font=("Courier", 14, "bold"),
        )  # Creating a button to submit the fen string

        self.change_turn_btn = tk.Button(
            self.master,
            text="Switch Turn",
            command=self.switch_turn,
            background=btn_bg_color,
            foreground=main_txt_color,
            activebackground=btn_bg_active_color,
            activeforeground=main_txt_color,
            width=17,
            border=0,
            cursor="hand2",
            font=("Courier", 20, "bold"),
        )
        # Creating a button to switch turns

        self.resign_btn = tk.Button(
            self.master,
            text="Resign",
            command=self.resign,
            background=btn_bg_color,
            foreground=main_txt_color,
            activebackground=btn_bg_active_color,
            activeforeground=main_txt_color,
            width=17,
            border=0,
            cursor="hand2",
            font=("Courier", 20, "bold"),
        )  # Creating a button to resign

        self.exit_btn = tk.Button(
            self.master,
            text="Exit",
            command=self.exit,
            background=btn_bg_color,
            foreground=main_txt_color,
            activebackground=btn_bg_active_color,
            activeforeground=main_txt_color,
            height=1,
            width=10,
            border=0,
            cursor="hand2",
            font=("Courier", 20, "bold"),
        )

        # Creating 5 buttons to set the difficulty level
        self.difficulty_easy_btn = tk.Button(
            self.master,
            text="Easy",
            command=lambda: self.set_difficulty(1),
            background=btn_bg_color,
            foreground=main_txt_color,
            activebackground=btn_bg_active_color,
            activeforeground=main_txt_color,
            width=16,
            height=1,
            border=0,
            cursor="hand2",
            font=("Courier", 20, "bold"),
        )

        self.difficulty_meduim_btn = tk.Button(
            self.master,
            text="Medium",
            command=lambda: self.set_difficulty(2),
            background=btn_bg_color,
            foreground=main_txt_color,
            activebackground=btn_bg_active_color,
            activeforeground=main_txt_color,
            width=16,
            height=1,
            border=0,
            cursor="hand2",
            font=("Courier", 20, "bold"),
        )

        self.difficulty_hard_btn = tk.Button(
            self.master,
            text="Hard",
            command=lambda: self.set_difficulty(3),
            background=btn_bg_color,
            foreground=main_txt_color,
            activebackground=btn_bg_active_color,
            activeforeground=main_txt_color,
            width=16,
            height=1,
            border=0,
            cursor="hand2",
            font=("Courier", 20, "bold"),
        )

        self.difficulty_souls_btn = tk.Button(
            self.master,
            text="Souls",
            command=lambda: self.set_difficulty(4),
            background=btn_bg_color,
            foreground=main_txt_color,
            activebackground=btn_bg_active_color,
            activeforeground=main_txt_color,
            width=16,
            height=1,
            border=0,
            cursor="hand2",
            font=("Courier", 20, "bold"),
        )

        self.difficulty_DRLCE_btn = tk.Button(
            self.master,
            text="DRLCE",
            command=lambda: self.set_difficulty(5),
            background=btn_bg_color,
            foreground=main_txt_color,
            activebackground=btn_bg_active_color,
            activeforeground=main_txt_color,
            width=16,
            height=1,
            border=0,
            cursor="hand2",
            font=("Courier", 20, "bold"),
        )

        self.back_btn = tk.Button(
            self.master,
            text="Back",
            command=self.display_main_menu,
            background=btn_bg_color,
            foreground=main_txt_color,
            activebackground=btn_bg_active_color,
            activeforeground=main_txt_color,
            width=13,
            height=1,
            border=0,
            cursor="hand2",
            font=("Courier", 20, "bold"),
        )  # Creating a button to go to the main menu

        self.start_game_btn = tk.Button(
            self.master,
            text="Start Game",
            command=self.display_game,
            background=btn_bg_color,
            foreground=main_txt_color,
            activebackground=btn_bg_active_color,
            activeforeground=main_txt_color,
            width=30,
            border=0,
            cursor="hand2",
            font=("Courier", 25, "bold"),
        )  # Creating a button to start the game

        self.select_difficulty_btn = tk.Button(
            self.master,
            text="Select Difficulty",
            command=self.display_difficulty,
            background=btn_bg_color,
            foreground=main_txt_color,
            activebackground=btn_bg_active_color,
            activeforeground=main_txt_color,
            width=30,
            border=0,
            cursor="hand2",
            font=("Courier", 25, "bold"),
        )  # Creating a button select the difficulty

        self.instructions_btn = tk.Button(
            self.master,
            text="Instructions (Important!)",
            command=self.display_instructions,
            background=btn_bg_color,
            foreground=main_txt_color,
            activebackground=btn_bg_active_color,
            activeforeground=main_txt_color,
            width=30,
            border=0,
            cursor="hand2",
            font=("Courier", 25, "bold"),
        )  # Creating a button to display the instructions

        self.settings_btn = tk.Button(
            self.master,
            text="Settings",
            command=self.display_settings,
            background=btn_bg_color,
            foreground=main_txt_color,
            activebackground=btn_bg_active_color,
            activeforeground=main_txt_color,
            width=30,
            border=0,
            cursor="hand2",
            font=("Courier", 25, "bold"),
        )  # Creating a button to display the settings

        self.sound_btn = tk.Button(
            self.master,
            text="Set Sound Off",
            command=self.toggle_sound,
            background=btn_bg_color,
            foreground=main_txt_color,
            activebackground=btn_bg_active_color,
            activeforeground=main_txt_color,
            width=20,
            border=0,
            cursor="hand2",
            font=("Courier", 18, "bold"),
        )  # Creating a button to toggle the sound

        self.fulscreen_btn = tk.Button(
            self.master,
            text="Set Fullscreen Off",
            command=self.toggle_fullscreen,
            background=btn_bg_color,
            foreground=main_txt_color,
            activebackground=btn_bg_active_color,
            activeforeground=main_txt_color,
            height=1,
            width=20,
            border=0,
            cursor="hand2",
            font=("Courier", 18, "bold"),
        )  # Creating a button to toggle the fullscreen

        self.virtual_board_img_canvas = tk.Canvas(
            self.master,
            width=400,
            height=400,
            borderwidth=0,
            highlightthickness=0,
        )  # Creating a canvas to display the virtual board image

        self.prev_board_img_canvas = tk.Canvas(
            self.master,
            width=400,
            height=400,
            borderwidth=0,
            highlightthickness=0,
        )  # Creating a canvas to display the cropped board image

        self.curr_board_img_canvas = tk.Canvas(
            self.master,
            width=400,
            height=400,
            borderwidth=0,
            highlightthickness=0,
        )  # Creating a canvas to display the cropped board image

        self.game_logo_canvas = tk.Canvas(
            self.master,
            bg=bg_color,
            width=250,
            height=200,
            borderwidth=0,
            highlightthickness=0,
        )  # Creating a canvas to display the game logo

        self.input_fen = tk.Entry(
            self.master,
            width=50,
            borderwidth=0,
            highlightthickness=0,
            font=("Courier", 15, "bold"),
            textvariable=self.fen_tk,
            bg=entry_bg_color,
        )  # Creating an entry to input the fen string

        self.input_cam_id = tk.Entry(
            self.master,
            width=5,
            borderwidth=0,
            highlightthickness=0,
            font=("Courier", 15, "bold"),
            textvariable=self.cam_id_tk,
            bg=entry_bg_color,
        )  # Creating an entry to input the camera id

    def init_fen(self):
        # Getting a random fen string from the fen csv file and setting the fen string to it if it's the first time the game is run
        if self.random_fen == True:
            self.fen_string = ce.get_random_fen(fen_csv_path)

        # Try to set the board from the fen string and if it fails, set the fen string to the default fen string
        try:
            self.board = ce.set_board_from_fen(
                self.board,
                self.fen_string,
            )
        except:
            pass

        # Creating an image object for the board
        self.board_img = ce.get_board_img(self.board)

        self.virtual_board_img_canvas.create_image(
            0,
            0,
            anchor=tk.NW,
            image=self.board_img,
        )  # Creating a canvas to display the virtual board image

        self.random_fen = False

    def display_main_menu(self):
        self.remove_visible_widgets()  # Remove the visible widgets

        self.game_logo_canvas.create_image(
            0,
            0,
            anchor=tk.NW,
            image=self.game_logo_tk,
        )  # Display the game logo in the GUI window

        self.game_logo_canvas.place(
            relx=0.275, rely=0.3, anchor=tk.CENTER
        )  # Placing the game logo in the GUI window
        self.title_label.place(
            relx=0.575, rely=0.325, anchor=tk.CENTER
        )  # Placing the title label in the GUI window
        self.select_difficulty_btn.place(
            relx=0.5, rely=0.625, anchor=tk.CENTER
        )  # Placing the start game button in the GUI window
        self.instructions_btn.place(
            relx=0.5, rely=0.75, anchor=tk.CENTER
        )  # Placing the instructions button in the GUI window
        self.settings_btn.place(
            relx=0.5, rely=0.875, anchor=tk.CENTER
        )  # Placing the settings button in the GUI window

        self.exit_btn.place(
            relx=0.93, rely=0.95, anchor=tk.CENTER
        )  # Placing the exit button in the GUI window

    def display_instructions(self):
        self.remove_visible_widgets()  # Remove the visible widgets

        self.instructions_label.place(
            relx=0.5, rely=0.15, anchor=tk.CENTER
        )  # Placing the instructions label in the GUI window

        self.back_btn.place(
            relx=0.5, rely=0.9, anchor=tk.CENTER
        )  # Placing the go to main menu button in the GUI window

        self.exit_btn.place(
            relx=0.93, rely=0.95, anchor=tk.CENTER
        )  # Placing the exit button in the GUI window

    def display_settings(self):
        self.remove_visible_widgets()  # Remove the visible widgets

        self.settings_label.place(
            relx=0.5, rely=0.15, anchor=tk.CENTER
        )  # Placing the settings label in the GUI window

        self.back_btn.place(
            relx=0.5, rely=0.9, anchor=tk.CENTER
        )  # Placing the go to main menu button in the GUI window

        self.initial_position_label.place(
            relx=0.8, rely=0.25, anchor=tk.CENTER
        )  # Placing the initial virtual board position label in the GUI window

        self.virtual_board_img_canvas.place(
            relx=0.8, rely=0.55, anchor=tk.CENTER
        )  # Placing the virtual board image canvas in the GUI window

        self.input_fen_label.place(
            relx=0.25, rely=0.3, anchor=tk.CENTER
        )  # Placing the input fen label in the GUI window

        self.input_fen.place(
            relx=0.25, rely=0.35, anchor=tk.CENTER
        )  # Placing the fen input in the GUI window

        self.input_fen_btn.place(
            relx=0.25, rely=0.41, anchor=tk.CENTER
        )  # Placing the fen submit button in the GUI window

        self.input_cam_id_label.place(
            relx=0.23, rely=0.53, anchor=tk.CENTER
        )  # Placing the input camera id label in the GUI window

        self.input_cam_id.place(
            relx=0.36, rely=0.53, anchor=tk.CENTER
        )  # Placing the camera id input in the GUI window

        self.input_cam_btn.place(
            relx=0.25, rely=0.59, anchor=tk.CENTER
        )  # Placing the camera id submit button in the GUI window

        self.sound_btn.place(
            relx=0.145, rely=0.73, anchor=tk.CENTER
        )  # Placing the sound button in the GUI window

        self.fulscreen_btn.place(
            relx=0.352, rely=0.73, anchor=tk.CENTER
        )  # Placing the fullscreen button in the GUI window

        self.exit_btn.place(
            relx=0.93, rely=0.95, anchor=tk.CENTER
        )  # Placing the exit button in the GUI window

    def submit_fen(self):
        self.fen_string = self.fen_tk.get()  # Getting the fen string from the input
        self.input_fen.delete(0, tk.END)  # Clearing the fen input
        self.initial_position_label["text"] = "Selected Fen's\nInitial Board Position"
        self.init_fen()  # Calling the init_fen method to initialize the fen string

    def submit_cam(self):
        # If the camera id is the same as the current camera id, clear the input and return
        if int(self.cam_id_tk.get()) == self.cam_id:
            self.input_cam_id.delete(0, tk.END)  # Clearing the camera id input
            return

        self.cam_id = int(self.cam_id_tk.get())  # Getting the camera id from the input

        self.input_cam_id.delete(0, tk.END)  # Clearing the camera id input

        if self.cam_id < 0:  # If the camera id is negative, set it to 0
            self.cam_id = 0

        self.dobot_cam = c2m.init_cam(self.cam_id)  # Initializing the camera

        if (
            self.dobot_cam is None
        ):  # If the camera couldn't be initialized, set the camera id to 0
            self.cam_id = 0
            self.dobot_cam = c2m.init_cam(self.cam_id)  # Initializing the camera

    def toggle_sound(self):
        self.sound = not self.sound  # Toggle the sound

        # If the text of the sound button is "Sound On", change it to "Sound Off"
        if self.sound_btn["text"] == "Set Sound Off":
            self.sound_btn["text"] = "Set Sound On"
        # If the text of the sound button is "Sound Off", change it to "Sound On"
        else:
            self.sound_btn["text"] = "Set Sound Off"

    def toggle_fullscreen(self):
        # If the GUI window is fullscreen, make it non-fullscreen
        if self.master.attributes("-fullscreen") == True:
            self.master.attributes("-fullscreen", False)
            self.master.geometry(
                "{}x{}+0+0".format(
                    self.master.winfo_screenwidth(), self.master.winfo_screenheight()
                )
            )  # Set the size of the GUI window to the size of the screen
            self.master.resizable(True, True)  # Make the GUI resizable
            self.fulscreen_btn["text"] = "Set Fullscreen On"
        # If the GUI window is non-fullscreen, make it fullscreen
        else:
            self.master.attributes("-fullscreen", True)
            self.fulscreen_btn["text"] = "Set Fullscreen Off"

    def display_difficulty(self):
        self.remove_visible_widgets()  # Remove the visible widgets

        self.back_btn.place(
            relx=0.5, rely=0.9, anchor=tk.CENTER
        )  # Placing the go to main menu button in the GUI window

        self.difficulty_label.place(
            relx=0.5, rely=0.275, anchor=tk.CENTER
        )  # Placing the difficulty label in the GUI window

        # Placing the difficulty buttons in the GUI window
        self.difficulty_easy_btn.place(relx=0.2, rely=0.5, anchor=tk.CENTER)
        self.difficulty_meduim_btn.place(relx=0.4, rely=0.5, anchor=tk.CENTER)
        self.difficulty_hard_btn.place(relx=0.6, rely=0.5, anchor=tk.CENTER)
        self.difficulty_souls_btn.place(relx=0.8, rely=0.5, anchor=tk.CENTER)
        self.difficulty_DRLCE_btn.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        # Placing the difficulty description in the GUI window
        self.difficulty_easy_desc.place(relx=0.1, rely=0.75, anchor=tk.CENTER)
        self.difficulty_meduim_desc.place(relx=0.3, rely=0.75, anchor=tk.CENTER)
        self.difficulty_hard_desc.place(relx=0.5, rely=0.75, anchor=tk.CENTER)
        self.difficulty_souls_desc.place(relx=0.7, rely=0.75, anchor=tk.CENTER)
        self.difficulty_DRLCE_desc.place(relx=0.9, rely=0.75, anchor=tk.CENTER)

        self.exit_btn.place(
            relx=0.93, rely=0.95, anchor=tk.CENTER
        )  # Placing the exit button in the GUI window

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty  # Setting the difficulty level

        # Remove the visible widgets
        self.remove_visible_widgets()

        # Setting the difficulty of the engine
        self.engine = ce.set_engine_difficulty(self.engine, self.difficulty)

        # Calling the start_game method to start the game
        self.init_game()

    def init_game(self):
        self.remove_visible_widgets()  # Remove the visible widgets

        self.start_game_label.place(
            relx=0.5, rely=0.3, anchor=tk.CENTER
        )  # Placing the start game label in the GUI window

        self.start_game_btn.place(
            relx=0.5, rely=0.55, anchor=tk.CENTER
        )  # Placing the start game button in the GUI window

        self.youssef_label.place(
            relx=0.5, rely=0.75, anchor=tk.CENTER
        )  # Placing Youssef's label in the GUI window

        self.hazem_label.place(
            relx=0.2, rely=0.75, anchor=tk.CENTER
        )  # Placing Hazem's label in the GUI window

        self.raheem_label.place(
            relx=0.8, rely=0.75, anchor=tk.CENTER
        )  # Placing Raheem's label in the GUI window

        self.exit_btn.place(
            relx=0.93, rely=0.95, anchor=tk.CENTER
        )  # Placing the exit button in the GUI window

        # dr.go_to_calibration(
        #     self.arm
        # )  # Move the arm to the calibration position # Test

        # dr.go_to_home(self.arm)  # Move the arm to the home position # Test
        # dr.go_to_home(self.arm)  # Move the arm to the home position again # Test

        self.filler_img = c2m.grab_img(
            self.dobot_cam  # type: ignore
        )  # Take a filler picture to make sure the camera is focused

        self.empty_img = c2m.grab_img(
            self.dobot_cam  # type: ignore
        )  # Take a picture of the empty board

        self.empty_img = c2m.read_img(cwd + "/Test/Live Previous.jpg")  # Test

        # If the camera couldn't take a picture, set the game state to 2 (Player wins)
        if self.empty_img is None:
            self.game_state = 2  # Set the game state to 2 (Player wins)
            self.check_result()  # Check the game state to display the result of the game

        self.homography_matrix = c2m.get_homography_matrix(
            self.empty_img, motherboard_path  # type: ignore
        )  # Find the homography matrix between the empty board image and the reference board image

        if self.homography_matrix.any() == None:  # type: ignore
            self.game_state = 2  # Set the game state to 2 (Player wins)
            self.check_result()  # Check the game state to display the result of the game

    def display_game(self):
        self.remove_visible_widgets()  # Remove the visible widgets

        self.label_player.place(
            relx=0.4, rely=0.725, anchor=tk.CENTER
        )  # Placing the player label in the GUI window

        self.label_time_player.place(
            relx=0.4, rely=0.8, anchor=tk.CENTER
        )  # Placing the player time label in the GUI window

        self.label_engine.place(
            relx=0.6, rely=0.725, anchor=tk.CENTER
        )  # Placing the engine label in the GUI window

        self.label_time_engine.place(
            relx=0.6, rely=0.8, anchor=tk.CENTER
        )  # Placing the engine time label in the GUI window

        self.change_turn_btn.place(
            relx=0.2, rely=0.75, anchor=tk.CENTER
        )  # Placing the change turn button in the GUI window

        self.resign_btn.place(
            relx=0.8, rely=0.75, anchor=tk.CENTER
        )  # Placing the resign button in the GUI window

        self.virtual_board_img_canvas.place(
            relx=0.2, rely=0.35, anchor=tk.CENTER
        )  # Placing the virtual board image canvas in the GUI window

        self.prev_board_img_canvas.place(
            relx=0.5, rely=0.35, anchor=tk.CENTER
        )  # Placing the previous board image canvas in the GUI window

        self.curr_board_img_canvas.place(
            relx=0.8, rely=0.35, anchor=tk.CENTER
        )  # Placing the current board image canvas in the GUI window

        self.virtual_img_label.place(
            relx=0.2, rely=0.065, anchor=tk.CENTER
        )  # Placing the virtual board image label in the GUI window

        self.prev_img_label.place(
            relx=0.5, rely=0.065, anchor=tk.CENTER
        )  # Placing the previous board image label in the GUI window

        self.curr_img_label.place(
            relx=0.8, rely=0.065, anchor=tk.CENTER
        )  # Placing the current board image label in the GUI window

        self.youssef_label.place(
            relx=0.5, rely=0.91, anchor=tk.CENTER
        )  # Placing Youssef's label in the GUI window

        self.hazem_label.place(
            relx=0.2, rely=0.91, anchor=tk.CENTER
        )  # Placing Hazem's label in the GUI window

        self.raheem_label.place(
            relx=0.8, rely=0.91, anchor=tk.CENTER
        )  # Placing Raheem's label in the GUI window

        self.filler_img = c2m.grab_img(
            self.dobot_cam  # type: ignore
        )  # Take a filler picture to make sure the camera is focused

        self.prev_img = c2m.grab_img(
            self.dobot_cam  # type: ignore
        )  # Take a picture of the board with the pieces on it befor the move is made

        self.prev_img = c2m.read_img(cwd + "/Test/Live Previous.jpg")  # Test

        # If the camera couldn't take a picture, set the game state to 2 (Player wins)
        if self.prev_img is None:
            self.game_state = 2  # Set the game state to 2 (Player wins)
            self.check_result()  # Check the game state to display the result of the game

        self.prev_img, flip = c2m.warp_img(
            self.prev_img, self.homography_matrix  # type: ignore
        )  # Warp the image to a top-down view

        self.prev_img = c2m.flip_img(
            self.prev_img, flip
        )  # Flip the image if it is upside down

        self.prev_img_tk = c2m.cv2_to_tk(
            self.prev_img
        )  # Convert the numpy array to a tkinter image

        # Display the virtual board image in the GUI window
        self.virtual_board_img_canvas.create_image(
            0,
            0,
            anchor=tk.NW,
            image=self.board_img,
        )

        # Display the previous board image in the GUI window
        self.prev_board_img_canvas.create_image(
            0,
            0,
            anchor=tk.NW,
            image=self.prev_img_tk,
        )

        # Display the current board image in the GUI window
        self.curr_board_img_canvas.create_image(
            0,
            0,
            anchor=tk.NW,
            image=self.prev_img_tk,
        )

        # Calling the game_loop method to start the game loop
        self.game_loop()

    def game_loop(self):
        # Check if the game is over
        if self.check_result() == 1:
            # give the player 5 seconds to see the result
            # dr.go_to_home(self.arm)  # Move the arm to the home position # Test
            # dr.disconnect(self.arm)  # Disconnect the arm # Test
            self.master.after(5000, self.master.destroy)
            return

        # Update the clock every ms based on whose turn it is
        if self.player_turn:
            self.time_left_player -= 1
        else:
            self.time_left_engine -= 1

        time_ms_player = (
            self.time_left_player
        )  # Getting the player time left in milliseconds as an integer
        time_sec_player = (
            time_ms_player // 1000
        )  # Getting the player time left in seconds as an integer
        time_min_player = (
            time_sec_player // 60
        )  # Getting the player time left in minutes as an integer

        # Formatting the player time string to display in the GUI window
        time_str_player = f"{time_min_player:02d}:{time_sec_player % 60:02d}:{time_ms_player % 100:02d}"

        self.label_time_player.config(
            text=time_str_player
        )  # Displaying the player time left in the GUI window

        time_ms_engine = (
            self.time_left_engine
        )  # Getting the engine time left in milliseconds as an integer
        time_sec_engine = (
            time_ms_engine // 1000
        )  # Getting the engine time left in seconds as an integer
        time_min_engine = (
            time_sec_engine // 60
        )  # Getting the engine time left in minutes as an integer

        # Formatting the engine time string to display in the GUI window
        time_str_engine = f"{time_min_engine:02d}:{time_sec_engine % 60:02d}:{time_ms_engine % 100:02d}"

        self.label_time_engine.config(
            text=time_str_engine
        )  # Displaying the engine time left in the GUI window

        # Calling the update_clock method again after the specified time
        self.master.after(self.update_every_ms, self.game_loop)

    def switch_turn(self):
        # Check the game state to display the result of the game
        if self.check_result() == 1:
            return

        self.filler_img = c2m.grab_img(
            self.dobot_cam  # type: ignore
        )  # Take a filler picture to make sure the camera is focused

        self.cur_img = c2m.grab_img(
            self.dobot_cam  # type: ignore
        )  # Take a picture of the board with the pieces on it after the move is made

        self.cur_img = c2m.read_img(cwd + "/Test/Live Current.jpg")  # Test

        # If the camera couldn't take a picture, set the game state to 2 (Player wins)
        if self.cur_img is None:
            self.game_state = 2  # Set the game state to 2 (Player wins)
            self.check_result()  # Check the game state to display the result of the game

        self.cur_img, flip = c2m.warp_img(
            self.cur_img, self.homography_matrix  # type: ignore
        )  # Warp the image to a top-down view

        self.cur_img = c2m.flip_img(
            self.cur_img, flip
        )  # Flip the image if it is upside down

        self.cur_img_tk = c2m.cv2_to_tk(
            self.cur_img
        )  # Convert the numpy array to a tkinter image

        self.player_moves_list, _ = c2m.find_moves(
            self.prev_img, self.cur_img  # type: ignore
        )  # Get the player's moves from the images

        if self.player_moves_list == None:
            self.game_state = 2  # Set the game state to 2 (Player wins)
            self.check_result()  # Check the game state to display the result of the game

        self.player_move = ce.moves_to_ACN(
            self.board, self.player_moves_list  # type: ignore
        )  # Get the player's move

        print("Player Moves List:", self.player_moves_list)  # Test
        print("Player Move:", self.player_move)  # Test

        self.prev_board_img_canvas.create_image(
            0, 0, anchor=tk.NW, image=self.prev_img_tk
        )  # Display the previous board image in the GUI window

        self.curr_board_img_canvas.create_image(
            0, 0, anchor=tk.NW, image=self.cur_img_tk
        )  # Display the current board image in the GUI window

        # Check the move and return if it is invalid
        if not ce.check_move(self.board, self.player_move):
            self.game_state = 1  # Set the game state to 1 (Engine wins)
            self.check_result()  # Check the game state to display the result of the game
            return  # Return if the move is invalid

        # Make the move on the board
        self.board.push_san(self.player_move)

        # Get the tkinter img of the board after the player's move
        self.board_img = ce.get_board_img(self.board)

        self.virtual_board_img_canvas.create_image(
            0, 0, anchor=tk.NW, image=self.board_img
        )  # Display the virtual board image in the GUI window

        # Disabling the button to switch turns
        self.change_turn_btn.config(state=tk.DISABLED, cursor="arrow")

        self.player_turn = not self.player_turn  # Toggling the value of player_turn

        self.get_engine_move()  # Calling the get_engine_move method to get the engine's move

    def get_engine_move(self):
        # Get the best move from the engine based on the difficulty level
        if self.difficulty == 5:
            self.engine_move = ce.get_DRLCE_move(DRLCE_weights_path, self.board)
        else:
            self.engine_move = ce.get_stockfish_move(self.engine, self.board)

        # Check the move and return if it is invalid
        if not ce.check_move(self.board, self.engine_move):  # type: ignore
            self.game_state = 2  # Set the game state to 2 (Player wins)
            self.check_result()  # Check the game state to display the result of the game
            return  # Return if the move is invalid

        # Check if the move is a kill, castling or enpassant
        self.chess_move_indicators = ce.check_indicators(self.board, self.engine_move)  # type: ignore

        print("Engine Move:", self.engine_move)  # Test

        # dr.apply_move(
        #     self.arm,
        #     self.engine_move,  # type: ignore
        #     self.chess_move_indicators,
        # )  # Apply the move to the arm # Test

        # dr.go_to_home(self.arm)  # Move the arm to the home position # Test

        # Make the move on the board
        self.board.push_san(self.engine_move)  # type: ignore

        # Get the tkinter img of the board after the engine's move
        self.board_img = ce.get_board_img(self.board)

        # Display the board image in the GUI window
        self.virtual_board_img_canvas.create_image(
            0, 0, anchor=tk.NW, image=self.board_img
        )

        self.filler_img = c2m.grab_img(
            self.dobot_cam  # type: ignore
        )  # Take a filler picture to make sure the camera is focused

        self.prev_img = c2m.grab_img(
            self.dobot_cam  # type: ignore
        )  # Take a picture of the board with the pieces on it befor the move is made

        self.prev_img, flip = c2m.warp_img(
            self.prev_img, self.homography_matrix  # type: ignore
        )  # Warp the image to a top-down view

        self.prev_img = c2m.flip_img(
            self.prev_img, flip
        )  # Flip the image if it is upside down

        self.prev_img_tk = c2m.cv2_to_tk(
            self.prev_img
        )  # Convert the numpy array to a tkinter image

        self.prev_board_img_canvas.create_image(
            0, 0, anchor=tk.NW, image=self.prev_img_tk
        )  # Display the previous board image in the GUI window

        # Check the game state to display the result of the game
        if self.check_result() == 1:
            return

        # Enabling the button to switch turns
        self.change_turn_btn.config(state=tk.NORMAL, cursor="hand2")

        self.player_turn = not self.player_turn  # Toggling the value of player_turn

    def resign(self):
        """
        Resigns the game, sets the game state to 1 (Engine wins) and displays the result of the game.
        """
        if self.game_state != 0:
            return

        self.game_state = 1
        self.check_result()

    def check_result(self):
        """
        Checks the result of the game based on the time left for each player and the game state on the board.

        If the time left for the player is zero, the game state is set to 1 (Engine wins).
        If the time left for the engine is zero, the game state is set to 2 (Player wins).
        If the game state on the board is 1, the game state is set to 1 (Engine wins).
        If the game state on the board is 2, the game state is set to 2 (Player wins).
        If the game state on the board is 3, the game state is set to 3 (Draw).

        Returns:
        -   The result of the game as displayed on the board.
        """
        if self.time_left_player <= 0:
            self.game_state = 1  # Set the game state to 1 (Engine wins)

        elif self.time_left_engine <= 0:
            self.game_state = 2  # Set the game state to 2 (Player wins)

        if ce.check_game_state(self.board) == 1:
            self.game_state = 1  # Set the game state to 1 (Engine wins)

        elif ce.check_game_state(self.board) == 2:
            self.game_state = 2  # Set the game state to 2 (Player wins)

        elif ce.check_game_state(self.board) == 3:
            self.game_state = 3  # Set the game state to 3 (Draw)

        return self.display_result()  # Display the result of the game

    def display_result(self):
        """
        Displays the result of the game in the GUI window based on the game state.

        Returns:
        -   int: 1 if the game is over, 0 otherwise.
        """
        if self.game_state == 1:  # If the engine wins
            self.change_turn_btn.config(
                state=tk.DISABLED, cursor="arrow"
            )  # Disable the button to switch turns

            self.resign_btn.config(
                state=tk.DISABLED, cursor="arrow"
            )  # Disable the button to resign

            # Display the result of the game in the GUI window
            self.label_time_player.config(text="You Lose!")
            self.label_time_engine.config(text="You Win!")
            return 1

        elif self.game_state == 2:  # If the player wins
            self.change_turn_btn.config(
                state=tk.DISABLED, cursor="arrow"
            )  # Disable the button to switch turns

            self.resign_btn.config(
                state=tk.DISABLED, cursor="arrow"
            )  # Disable the button to resign

            # Display the result of the game in the GUI window
            self.label_time_player.config(text="You Win!")
            self.label_time_engine.config(text="You Lose!")
            return 1

        elif self.game_state == 3:  # If the game is a draw
            self.change_turn_btn.config(
                state=tk.DISABLED, cursor="arrow"
            )  # Disable the button to switch turns

            self.resign_btn.config(
                state=tk.DISABLED, cursor="arrow"
            )  # Disable the button to resign

            # Display the result of the game in the GUI window
            self.label_time_player.config(text="Draw!")
            self.label_time_engine.config(text="Draw!")
            return 1

        return 0

    def remove_visible_widgets(self):
        """
        Removes all visible widgets from the master window.
        """
        for widget in self.master.winfo_children():
            widget.pack_forget()
            widget.place_forget()
            widget.grid_forget()

    def exit(self):
        """
        Exits the game.
        """
        # dr.go_to_home(self.arm)  # Move the arm to the home position # Test
        # dr.disconnect(self.arm)  # Disconnect the arm # Test
        self.master.destroy()  # Destroy the master window
