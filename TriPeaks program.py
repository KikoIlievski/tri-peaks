import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image
from PIL import ImageTk

width = 0.08  # Card scaling
height = 0.2  # card scaling

active_instances = []  # holding running instances of the Application mainloop
active_log = []  # holding running instances of the User mainloop

all_cards = [  # master copy of all cards
    '1c', '1d', '1h', '1s',
    '2c', '2d', '2h', '2s',
    '3c', '3d', '3h', '3s',
    '4c', '4d', '4h', '4s',
    '5c', '5d', '5h', '5s',
    '6c', '6d', '6h', '6s',
    '7c', '7d', '7h', '7s',
    '8c', '8d', '8h', '8s',
    '9c', '9d', '9h', '9s',
    '10c', '10d', '10h', '10s',
    '11c', '11d', '11h', '11s',
    '12c', '12d', '12h', '12s',
    '13c', '13d', '13h', '13s',
]


# when invoked, handles all data clearing and quitting of game
def quit_game():
    TopFrame.local_score = 0
    TopFrame.score_frame = None
    TopFrame.score_widget = None
    active_instances[0].destroy()
    del active_instances[0]


# when invoked, handles all data clearing and logging out
def restart_game():
    CreateCard.num_cards_paired = 0
    MidFrame.cards_in_hand = []
    MidFrame.all_cards_bottom = {}
    active_instances[0].destroy()
    active_instances[0] = Application()


# automation of creating cards, making it automatic rather than manual
class CreateCard(tk.Frame):
    num_cards_paired = 0
    card_clicked = None

    # takes parameter's to define nature of all cards created by class
    def __init__(self, parent,
                 card_type='blue_back',
                 flipped=False,
                 exist=True,
                 label_card=False,
                 **kwargs):
        super().__init__(parent, **kwargs)

        self.card_type = card_type
        self.exist = exist
        self.card_state = {self.card_type: ['PNG/' + self.card_type +'.png', 'PNG/blue_back.png']}
        self.label_card = label_card

        # determining function of card depending on flipped or not
        if not flipped:
            self.card = Image.open(self.card_state[self.card_type][1])

            self.function = lambda: self.flip()
        if flipped:
            self.card = Image.open(self.card_state[self.card_type][0])
            self.function = lambda: self.check_cards()

        self.card = self.card.resize((int(Application.cards_scale_width),
                                      int(Application.cards_scale_height)), Image.ANTIALIAS)
        self._photo_image = ImageTk.PhotoImage(self.card)

        if flipped and not label_card:
            self.card_button = tk.Button(self, image=self._photo_image,
                                         relief='flat', bg='light gray',
                                         highlightthickness=0, bd=0, command=self.function)
        else:
            self.card_button = tk.Label(self, image=self._photo_image,
                                        relief='flat', bg='light gray',
                                        highlightthickness=0, bd=0)
        self.card_button.place(relwidth=1, relheight=1)

    # switches cards from buttons to labels and vice versa
    def switch(self):
        self.card = Image.open('PNG/' + MidFrame.current_card + '.png')
        self.card = self.card.resize(
            (int(Application.cards_scale_width), int(Application.cards_scale_height)),
            Image.ANTIALIAS)
        self._photo_image = ImageTk.PhotoImage(self.card)
        self.card_button = tk.Label(self, image=self._photo_image,
                                    relief='flat', bg='light gray',
                                    highlightthickness=0, bd=0)
        self.card_button.place(relheight=1, relwidth=1)

    # switches cards from face down to face up and vice versa
    def flip(self):
        if self.label_card:
            self.card_button.forget()

            self.card = Image.open('PNG/' + CreateCard.card_clicked + '.png')
            self.card = self.card.resize((int(Application.cards_scale_width), int(Application.cards_scale_height)),
                                         Image.ANTIALIAS)
            self._photo_image = ImageTk.PhotoImage(self.card)
            self.card_button = tk.Label(self, image=self._photo_image,
                                        relief='flat', bg='light gray',
                                        highlightthickness=0, bd=0, border=0)

            self.card_button.place(relwidth=1, relheight=1)
        else:
            self.card_button.destroy()

            self.card = Image.open(self.card_state[self.card_type][0])
            self.card = self.card.resize((int(Application.cards_scale_width), int(Application.cards_scale_height)),
                                         Image.ANTIALIAS)
            self._photo_image = ImageTk.PhotoImage(self.card)
            self.card_button = tk.Button(self, image=self._photo_image,
                                         relief='flat', bg='light gray',
                                         border=0, command=lambda: self.check_cards())

            self.card_button.place(relwidth=1, relheight=1)

    # checks if card clicked on screen is within 1 value to card in hand
    def check_cards(self):
        _correct_pair = False
        if len(MidFrame.local_current) == 2:
            _held_number = int(MidFrame.local_current[0])
        else:
            _held_number = int(MidFrame.local_current[0:2])

        if len(self.card_type) == 2:
            _number_clicked = int(self.card_type[0])
        else:
            _number_clicked = int(self.card_type[0:2])

        if _held_number + 1 == _number_clicked or _held_number - 1 == _number_clicked:
            _correct_pair = True
        elif _held_number == 13 and _number_clicked == 1:
            _correct_pair = True
        elif _held_number == 1 and _number_clicked == 13:
            _correct_pair = True

        if _correct_pair:

            TopFrame.local_score += MidFrame.score_multiplier*200 + 300
            MidFrame.score_multiplier += 1
            _score_var = tk.StringVar()
            _score_var.set('Score: ' + str(TopFrame.local_score))
            TopFrame.score_widget.destroy()
            TopFrame.score_widget = tk.Label(TopFrame.score_frame, textvariable=_score_var, bg='white', font="16")
            TopFrame.score_widget.place(relwidth=1, relheight=1)

            self.exist = False
            self.label_card = True
            CreateCard.num_cards_paired += 1
            CreateCard.card_clicked = self.card_type

            MidFrame.all_cards_bottom[MidFrame.current_card].flip()

            MidFrame.local_current = self.card_type

            if list(MidFrame.cards_placed.keys())[list(MidFrame.cards_placed.values()).index(self)][0] == '4':
                for i in range(1, 10):
                    if not MidFrame.cards_placed['4 ' + str(i)].exist \
                            and not MidFrame.cards_placed['4 ' + str(i + 1)].exist:
                        MidFrame.cards_placed['3 ' + str(i)].flip()
                        self.place_forget()
                    else:
                        self.place_forget()

            elif list(MidFrame.cards_placed.keys())[list(MidFrame.cards_placed.values()).index(self)][0] == '3':
                for i in range(1, 7):
                    if i <= 2:
                        if not MidFrame.cards_placed['3 ' + str(i)].exist\
                                and not MidFrame.cards_placed['3 ' + str(i + 1)].exist:
                            MidFrame.cards_placed['2 ' + str(i)].flip()
                            self.place_forget()
                        else:
                            self.place_forget()
                    elif 2 < i <= 4:
                        if not MidFrame.cards_placed['3 ' + str(i+1)].exist \
                                and not MidFrame.cards_placed['3 ' + str(i + 2)].exist:
                            MidFrame.cards_placed['2 ' + str(i)].flip()
                            self.place_forget()
                        else:
                            self.place_forget()
                    elif 4 < i <= 6:
                        if not MidFrame.cards_placed['3 ' + str(i + 2)].exist \
                                and not MidFrame.cards_placed['3 ' + str(i + 3)].exist:
                            MidFrame.cards_placed['2 ' + str(i)].flip()
                            self.place_forget()
                        else:
                            self.place_forget()

            elif list(MidFrame.cards_placed.keys())[list(MidFrame.cards_placed.values()).index(self)][0] == '2':
                for i in range(1, 4):
                    if i == 1:
                        if not MidFrame.cards_placed['2 ' + str(i)].exist \
                                and not MidFrame.cards_placed['2 ' + str(i + 1)].exist:
                            MidFrame.cards_placed['1 ' + str(i)].flip()
                            self.place_forget()
                        else:
                            self.place_forget()
                    elif i == 2:
                        if not MidFrame.cards_placed['2 ' + str(i+1)].exist \
                                and not MidFrame.cards_placed['2 ' + str(i + 2)].exist:
                            MidFrame.cards_placed['1 ' + str(i)].flip()
                            self.place_forget()
                        else:
                            self.place_forget()
                    elif i <= 3:
                        if not MidFrame.cards_placed['2 ' + str(i+2)].exist \
                                and not MidFrame.cards_placed['2 ' + str(i + 3)].exist:
                            MidFrame.cards_placed['1 ' + str(i)].flip()
                            self.place_forget()
                        else:
                            self.place_forget()
            else:
                for i in range(1, 4):
                    if i == 1:
                        if not MidFrame.cards_placed['2 ' + str(i)].exist \
                                and not MidFrame.cards_placed['2 ' + str(i + 1)].exist:
                            MidFrame.cards_placed['1 ' + str(i)].flip()
                            self.place_forget()
                        else:
                            self.place_forget()
                    elif i == 2:
                        if not MidFrame.cards_placed['2 ' + str(i + 1)].exist \
                                and not MidFrame.cards_placed['2 ' + str(i + 2)].exist:
                            MidFrame.cards_placed['1 ' + str(i)].flip()
                            self.place_forget()
                        else:
                            self.place_forget()
                    elif i <= 3:
                        if not MidFrame.cards_placed['2 ' + str(i + 2)].exist \
                                and not MidFrame.cards_placed['2 ' + str(i + 3)].exist:
                            MidFrame.cards_placed['1 ' + str(i)].flip()
                            self.place_forget()
                        else:
                            self.place_forget()
        if CreateCard.num_cards_paired == 28:
            tk.messagebox.showinfo('Board Cleared!',
                                   'Next round...')
            restart_game()


# all widgets belonging in the MidFrame + logic of the game
class MidFrame(tk.Frame):
    cards_placed = {}  # Dictionary to track all placed cards
    card_pool = []  # Declaring list with all cards, however this list will be the one we alter

    current_card = None
    local_current = None
    all_cards_bottom = {}
    cards_in_hand = []

    score_multiplier = 0

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        MidFrame.cards_placed = {}
        MidFrame.cards_placed = {}
        MidFrame.card_pool = []

        MidFrame.current_card = None
        MidFrame.local_current = None
        MidFrame.all_cards_bottom = {}
        MidFrame.cards_in_hand = []

        MidFrame.score_multiplier = 0

        if User.current_user.replace(' ', '').lower() == 'gordonramsey':
            self._background = Image.open("PNG/EEbackground.png")
        else:
            self._background = Image.open("PNG/SMOOTHbackground.png")

        self._background = self._background.resize((Application.root_width, Application.root_height), Image.ANTIALIAS)
        self._photo_image = ImageTk.PhotoImage(self._background)

        _cover = tk.Label(self, image=self._photo_image)
        _cover.place(relwidth=1, relheight=1)

        for cards in all_cards:  # Populating card_pool list to be copy of all_cards parent
            MidFrame.card_pool.append(cards)

        self.card_pool = MidFrame.card_pool

        for i in range(4):
            if i < 4:
                k = (i+1) * 3
            else:
                k = 10
            for j in range(k):
                self.choice = random.choice(self.card_pool)
                card_pos = str(i+1) + ' ' + str(j+1)

                if int(card_pos[2:]) < 11:
                    if i < 3:
                        self.cards_placed[card_pos] = CreateCard(self, card_type=self.choice, flipped=False)
                    else:
                        self.cards_placed[card_pos] = CreateCard(self, card_type=self.choice, flipped=True)
                    self.card_pool.remove(self.choice)
                else:
                    break

        count = 1

        for widget in self.cards_placed:
            # first Row of cards
            if count <= 3:
                y = 0.1
                self.cards_placed[widget].place(relheight=height, relwidth=width,
                                                relx=-0.08+0.27*count, rely=y)
                count += 1
            # second row:
            elif 3 < count <= 9:
                y = 0.2
                if count % 2 == 0:
                    self.cards_placed[widget].place(relheight=height, relwidth=width,
                                                    relx=-0.125+0.27*((count-2)/2), rely=y)
                else:
                    self.cards_placed[widget].place(relheight=height, relwidth=width,
                                                    relx=-0.035+0.27*((count-3)/2), rely=y)
                count += 1
            # third row:
            elif 9 < count <= 18:
                y = 0.3
                if count == 10:
                    self.cards_placed[widget].place(relheight=height, relwidth=width,
                                                    relx=0.1, rely=y)
                else:
                    self.cards_placed[widget].place(relheight=height, relwidth=width,
                                                    relx=0.1+0.09*(count-10), rely=y)
                count += 1
            # fourth row:
            elif 18 < count <= 28:
                y = 0.4
                if count == 19:
                    self.cards_placed[widget].place(relheight=height, relwidth=width,
                                                    relx=0.055, rely=y)
                else:
                    self.cards_placed[widget].place(relheight=height, relwidth=width,
                                                    relx=0.055+0.09*(count-19), rely=y)
                count += 1

        # bottom Section:
        self.cards_in_hand = []
        for i in range(len(self.card_pool)):
            _choice = random.choice(self.card_pool)
            self.cards_in_hand.append(_choice)
            MidFrame.cards_in_hand.append(_choice)
            self.card_pool.remove(_choice)

        _relx_count = 0.35
        _count = 1
        for card in self.cards_in_hand:
            if _count < 24:
                MidFrame.all_cards_bottom[card] = CreateCard(self, card_type=card, label_card=True)
                MidFrame.all_cards_bottom[card].place(relwidth=width, relheight=height,
                                                      relx=_relx_count, rely=0.7)
                _relx_count += 0.0015
            else:
                MidFrame.all_cards_bottom[card] = CreateCard(self, card_type=card, flipped=True, label_card=True)
                MidFrame.all_cards_bottom[card].place(relwidth=width, relheight=height,
                                                      relx=0.55, rely=0.7)
            _count += 1

        current_card = self.cards_in_hand[-1]
        MidFrame.current_card = current_card
        MidFrame.local_current = current_card
        self.cards_in_hand.remove(self.cards_in_hand[-1])

        # cycle button:
        self.cycle_button = Image.open("PNG/cycle_icon.png")
        self.cycle_button = self.cycle_button.resize((int(Application.root_width*0.04),
                                                      int(Application.root_height*0.06)), Image.ANTIALIAS)
        self.cycle_image = ImageTk.PhotoImage(self.cycle_button)
        cycle_button = tk.Button(self, bg='#bbbbbb', image=self.cycle_image, command=self.cycle, bd=1,
                                 activebackground='#bbbbbb')
        cycle_button.place(relwidth=0.05, relheight=0.08,
                           rely=0.75, relx=0.475)

        # quit button:
        self.exit = Image.open("PNG/quit_button.png")
        self.exit = self.exit.resize((int(Application.root_width*0.05),
                                      int(Application.root_height*0.07)), Image.ANTIALIAS)
        self.exit_image = ImageTk.PhotoImage(self.exit)
        quit_button = tk.Button(self, bg='#bbbbbb', image=self.exit_image, command=lambda: self.quit_confirmation(),
                                activebackground='light gray', bd=1)
        quit_button.place(relwidth=0.08, relheight=0.09,
                          relx=0.8, rely=0.78)

        # log out button
        self.logout = Image.open("PNG/exit_icon.png")
        self.logout = self.logout.resize((int(Application.root_width*0.05),
                                          int(Application.root_height*0.07)), Image.ANTIALIAS)
        self.logout_image = ImageTk.PhotoImage(self.logout)
        logout_button = tk.Button(self, bg='#bbbbbb', image=self.logout_image, command=lambda: self.logout_confirm(),
                                  activebackground='light gray', bd=1)
        logout_button.place(relwidth=0.08, relheight=0.09,
                            relx=0.12, rely=0.78)

    # confirming whether user intends to quit
    @staticmethod
    def quit_confirmation():
        confirm_quit = tk.messagebox.askquestion('Confirm', 'Are you sure you want to quit?')
        if confirm_quit == 'yes':
            if TopFrame.local_score != 0:
              try: 
                _file = open("scores.txt", "a")
              except IOError:
                _file = open('scores.txt', 'w')
              _file.write('\n' + str(User.current_user) + ':' + str(TopFrame.local_score))
              _file.close()
            quit_game()
        else:
            pass

    # confirming whether user intends to log out
    @staticmethod
    def logout_confirm():
        confirm_logout = tk.messagebox.askquestion('Confirm', 'Are you sure you want to log out?')
        if confirm_logout == 'yes':
            if TopFrame.local_score != 0:
                _file = open("scores.txt", "a")
                _file.write('\n' + str(User.current_user) + ':' + str(TopFrame.local_score))
                _file.close()

            quit_game()
            active_log.append(User())
            active_log[0].mainloop()
        else:
            pass

    # function to cycle to next card in dealt hand
    @staticmethod
    def cycle():
        MidFrame.score_multiplier = 0
        if len(MidFrame.cards_in_hand) != 1:
            MidFrame.all_cards_bottom[MidFrame.current_card].destroy()
            del MidFrame.all_cards_bottom[MidFrame.cards_in_hand[-1]]
            MidFrame.cards_in_hand.remove(MidFrame.current_card)

            MidFrame.current_card = MidFrame.cards_in_hand[-1]
            MidFrame.local_current = MidFrame.current_card
            MidFrame.all_cards_bottom[MidFrame.current_card].switch()

            MidFrame.all_cards_bottom[MidFrame.current_card].place(relwidth=width, relheight=height,
                                                                   relx=0.55, rely=0.7)
        else:
            MidFrame.all_cards_bottom[MidFrame.current_card].destroy()
            del MidFrame.all_cards_bottom[MidFrame.cards_in_hand[0]]
            MidFrame.cards_in_hand.remove(MidFrame.current_card)
            if TopFrame.local_score != 0:
                _file = open("scores.txt", "a")
                _file.write('\n' + str(User.current_user) + ':' + str(TopFrame.local_score))
                _file.close()
            TopFrame.local_score = 0
            TopFrame.score_frame = None
            TopFrame.score_widget = None
            over_notif = tk.messagebox.askquestion('Better luck next time!',
                                                   'Would you like to restart?')
            if over_notif == 'yes':
                TopFrame.local_score = 0
                restart_game()
            else:
                tk.messagebox.showinfo('Thanks for playing...', 'Come back and visit soon?')
                quit_game()


# holds widgets in TopFrame; help button and score
class TopFrame(tk.Frame):
    local_score = 0
    score_frame = None
    score_widget = None

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._background = Image.open("PNG/TOPbackground.png")
        self._background = self._background.resize((Application.root_width,
                                                    int(Application.root_height*0.12)), Image.ANTIALIAS)
        self._photo_image = ImageTk.PhotoImage(self._background)

        _cover = tk.Label(self, image=self._photo_image)
        _cover.place(relwidth=1, relheight=1)

        self.help_button = tk.Button(self, text="Help...", command=self.instructions, bd=1, bg='white',
                                     font="16")
        self.help_button.place(relx=0.2, rely=0.25, relwidth=0.1, relheight=0.5)
        TopFrame.score_frame = tk.Frame(self)
        TopFrame.score_frame.place(relx=0.7, rely=0.25, relwidth=0.1, relheight=0.5)

        _score_var = tk.StringVar()
        _score_var.set('Score: ' + str(TopFrame.local_score))
        TopFrame.score_widget = tk.Label(TopFrame.score_frame, textvariable=_score_var, bg='white', font="16")
        TopFrame.score_widget.place(relwidth=1, relheight=1)

    # function invokes message box describing instructions of how to play TriPeaks
    @staticmethod
    def instructions():
        tk.messagebox.showinfo('How to play:',
                               'The object of Tri-Peaks is to transfer all the cards from the tableau to the '
                               'waste pile, uncovering cards further up the peaks, making them available for '
                               'play. You win the game when you’ve removed all the cards from the tableau to '
                               'the waste pile, demolishing the three peaks.')


# root window for game
class Application(tk.Tk):
    root_width = None
    root_height = None

    cards_scale_width = None
    cards_scale_height = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title('TriPeaks')
        self.attributes("-fullscreen", True)
        self.resizable(False, False)

        self.update()
        Application.root_width = int(self.winfo_width())
        Application.root_height = int(self.winfo_height())

        Application.cards_scale_width = int(Application.root_width * width) + 2
        Application.cards_scale_height = int(Application.root_height * height) - 2

        top_frame = TopFrame(self, bg='black')
        top_frame.place(relheight=0.05, relwidth=1)

        mid_frame = MidFrame(self, bg='green')
        mid_frame.place(rely=0.05, relheight=0.95, relwidth=1)


# root window for login screen
class User(tk.Tk):
    current_user = None
    all_usernames = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        usernames = []
        _score_list = []
        user_scores = {}
        _score_vars = []

        self.title('Login: ')
        self.geometry('600x600')
        self.resizable(False, False)

        self._login_frame = tk.Frame(self, bg='green')
        self._login_frame.place(relheight=.6, relwidth=1)

        self.scores_frame = tk.Frame(self, bg='dark green')
        self.scores_frame.place(relheight=0.4, relwidth=1,
                                rely=0.6)
        self.score_title = tk.Label(self.scores_frame, text='Highscores:', bg='dark green', fg='white',
                                    justify='center', font='arial 16 bold')
        self.score_title.place(relwidth=0.2, relheight=0.1,
                               relx=0.4, rely=0.1)

        score_1_var_name = tk.StringVar()
        score_1_var_name.set('-')
        self.score_1 = tk.Label(self.scores_frame, textvariable=score_1_var_name, bg='dark green', fg='white',
                                justify='right', anchor='e', font='arial 12 bold')
        self.score_1.place(relwidth=0.4, relheight=0.1,
                           relx=0.05, rely=0.25)

        score_2_var_name = tk.StringVar()
        score_2_var_name.set('-')
        self.score_2 = tk.Label(self.scores_frame, textvariable=score_2_var_name, bg='dark green', fg='white',
                                justify='left', anchor='w', font='arial 12 bold')
        self.score_2.place(relwidth=0.4, relheight=0.1,
                           relx=0.55, rely=0.25)

        score_3_var_name = tk.StringVar()
        score_3_var_name.set('-')
        self.score_3 = tk.Label(self.scores_frame, textvariable=score_3_var_name, bg='dark green', fg='white',
                                justify='right', anchor='e', font='arial 12 bold')
        self.score_3.place(relwidth=0.4, relheight=0.1,
                           relx=0.05, rely=0.35)

        score_4_var_name = tk.StringVar()
        score_4_var_name.set('-')
        self.score_4 = tk.Label(self.scores_frame, textvariable=score_4_var_name, bg='dark green', fg='white',
                                justify='left', anchor='w', font='arial 12 bold')
        self.score_4.place(relwidth=0.4, relheight=0.1,
                           relx=0.55, rely=0.35)

        score_5_var_name = tk.StringVar()
        score_5_var_name.set('-')
        self.score_5 = tk.Label(self.scores_frame, textvariable=score_5_var_name, bg='dark green', fg='white',
                                justify='right', anchor='e', font='arial 12 bold')
        self.score_5.place(relwidth=0.4, relheight=0.1,
                           relx=0.05, rely=0.45)

        score_6_var_name = tk.StringVar()
        score_6_var_name.set('-')
        self.score_6 = tk.Label(self.scores_frame, textvariable=score_6_var_name, bg='dark green', fg='white',
                                justify='left', anchor='w', font='arial 12 bold')
        self.score_6.place(relwidth=0.4, relheight=0.1,
                           relx=0.55, rely=0.45)

        score_7_var_name = tk.StringVar()
        score_7_var_name.set('-')
        self.score_7 = tk.Label(self.scores_frame, textvariable=score_7_var_name, bg='dark green', fg='white',
                                justify='right', anchor='e', font='arial 12 bold')
        self.score_7.place(relwidth=0.4, relheight=0.1,
                           relx=0.05, rely=0.55)

        score_8_var_name = tk.StringVar()
        score_8_var_name.set('-')
        self.score_8 = tk.Label(self.scores_frame, textvariable=score_8_var_name, bg='dark green', fg='white',
                                justify='left', anchor='w', font='arial 12 bold')
        self.score_8.place(relwidth=0.4, relheight=0.1,
                           relx=0.55, rely=0.55)

        score_9_var_name = tk.StringVar()
        score_9_var_name.set('-')
        self.score_9 = tk.Label(self.scores_frame, textvariable=score_9_var_name, bg='dark green', fg='white',
                                justify='right', anchor='e', font='arial 12 bold')
        self.score_9.place(relwidth=0.4, relheight=0.1,
                           relx=0.05, rely=0.65)

        score_10_var_name = tk.StringVar()
        score_10_var_name.set('-')
        self.score_10 = tk.Label(self.scores_frame, textvariable=score_10_var_name, bg='dark green', fg='white',
                                 justify='left', anchor='w', font='arial 12 bold')
        self.score_10.place(relwidth=0.4, relheight=0.1,
                            relx=0.55, rely=0.65)

        try:
          _file = open("scores.txt", 'r')
        except IOError:
          print("cant find file")
        contents = _file.readlines()
        print('this is the contents')
        print(contents)
        for data in contents:
            item = data.strip('\n')
            try:
                user_scores[item.split(':')[0]].append(int(item.split(":")[1]))
            except KeyError:
                # user_scores[item.split(':')[0]] = [int(item.split(':')[1])]
                pass

        for key in user_scores:
            user_scores[key] = sorted(user_scores[key], reverse=True)
            usernames.append(key)
            _score_list.append(user_scores[key][0])

        User.all_usernames = usernames

        for i in range(5):
            try:
                _score_vars.append(_score_list.index(sorted(_score_list, reverse=True)[i]))

            except IndexError:
                pass

        try:
            score_1_var_name.set(usernames[_score_vars[0]])
            score_2_var_name.set(_score_list[_score_vars[0]])
        except IndexError:
            pass
        try:
            score_3_var_name.set(usernames[_score_vars[1]])
            score_4_var_name.set(_score_list[_score_vars[1]])
        except IndexError:
            pass
        try:
            score_5_var_name.set(usernames[_score_vars[2]])
            score_6_var_name.set(_score_list[_score_vars[2]])
        except IndexError:
            pass
        try:
            score_7_var_name.set(usernames[_score_vars[3]])
            score_8_var_name.set(_score_list[_score_vars[3]])
        except IndexError:
            pass
        try:
            score_9_var_name.set(usernames[_score_vars[4]])
            score_10_var_name.set(_score_list[_score_vars[4]])
        except IndexError:
            pass
        _file.close()

        self._back_image = Image.open("PNG/honors_spade-14.png")
        self._back_image = self._back_image.resize((500, 210), Image.ANTIALIAS)
        self._photo_image = ImageTk.PhotoImage(self._back_image)
        self._background = tk.Label(self._login_frame, image=self._photo_image, bg='green')
        self._background.place(relheight=.65, relwidth=1,
                               rely=0.05)

        _user_label = tk.Label(self._login_frame, text='Username:', bg='green', font='Arial 20 bold',
                               fg='white', justify='center')
        _user_label.place(relheight=0.1, relwidth=0.4,
                          rely=0.7, relx=0.3)

        self._login = tk.Entry(self._login_frame, justify='center', font='20', bd=1)
        self._login.bind('<Return>', self.check_name)
        self._login.place(relheight=0.08, relwidth=0.5,
                          rely=0.8, relx=0.25)

    # checks if name input to username entry box is valid (doesn't consist of only empty space)
    def check_name(self, event):
        if self._login.get().strip(' ') == '':
            self._login.configure(bg='indian red')
            tk.messagebox.showinfo('Error', 'Please enter a valid username!')
        elif self._login.get() in User.all_usernames:
            tk.messagebox.showinfo('Welcome back', 'You are playing as existing user: ' + self._login.get())
            User.current_user = self._login.get()
            self.destroy()
            del active_log[0]
            active_instances.append(Application())
            active_instances[0].mainloop()
        else:
            User.current_user = self._login.get()
            self.destroy()
            del active_log[0]
            active_instances.append(Application())
            active_instances[0].mainloop()


# checks if the program is being run from an external file or directly
if __name__ == '__main__':
    active_log.append(User())
    active_log[0].mainloop()
