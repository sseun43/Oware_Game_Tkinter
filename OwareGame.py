
from cProfile import label
from tkinter import *
from tkinter import ttk
import tkinter
from turtle import title


class Hole:
    """
    Class Hole represents hole/pit of the game.
    Initially there are 4 seeds/balls in each hole.
    """
    def __init__(self, n):
        self.__seeds = 4
        self.__id = n

    def update(self):
        """
        Method increases amount of seeds in the hole by 1.
        """
        self.__seeds += 1

    def take_seeds(self):
        """
        Method takes the seeds from the hole to hand. So hole becomes empty.
        :return: hand: int, amount of seeds taken from hole.
        """
        hand = self.__seeds
        self.__seeds = 0
        return hand

    def take_to_score(self, board, player):
        """
        Method updates the score of the player,
        if his move satisfies the criteria.
        :param board: board object, game board.
        :param player: int, player who is making turn.
        :return: bool, True if succeed.
        """
        if board.last_hole(player):
            return False
        elif self.__seeds == 2 or self.__seeds == 3:
            board.set_score(player, self.take_seeds())
            return True
        else:
            return False

    def get_seeds(self):
        """
        Get method.
        :return: int, amount of seeds in the given hole.
        """
        return self.__seeds


class Board:
    """
    Class board represents the logic of game board. Initiates 12 hole objects.
    """
    def __init__(self):
        self.__holes = []
        for id in range(0, 12):
            id = Hole(id)
            self.__holes.append(id)
        self.__player_one_score = 0
        self.__player_two_score = 0

    def player(self, player, id):
        """
        Method represents the player moves after he has selected the hole
        from which he picks the seeds.
        :param player: int, player who is making turn.
        :param id: int, number representation of selected hole.
        """
        turns = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        if player == 1:
            player_field = (0, 1, 2, 3, 4, 5)
            opponent_field = (6, 7, 8, 9, 10, 11)
        else:
            player_field = (6, 7, 8, 9, 10, 11)
            opponent_field = (0, 1, 2, 3, 4, 5)
        if id in player_field:
            hand = self.__holes[id].take_seeds()
            for n in range(1, hand+1):
                self.__holes[turns[id+n]].update()
                if n == hand and (turns[id+n] in opponent_field):
                    result = self.__holes[turns[id+n]].take_to_score(self, player)
                    while result and (turns[id+n-1] in opponent_field):
                        n -= 1
                        result = self.__holes[turns[id + n]].take_to_score(
                            self, player)

    def set_score(self, player, score):
        """
        Set method for given player.
        :param player: int, player who gets the score
        :param score: int, amount of point to score
        """
        if player == 1:
            self.__player_one_score += score
        elif player == 2:
            self.__player_two_score += score

    def player_win(self):
        """
        Method checks if one of the players won (scored 24).
        :return: str, color code of the player, who won.
        """
        if self.__player_one_score >= 24:
            return "red"
        elif self.__player_two_score >= 24:
            return "blue"
        else:
            return False

    def get_current_board_state(self):
        """
        Method creates two lists with seeeds in each hole.
        One list per player's side.
        :return: tuple, lists with amount of seeds (int) in each hole.
        """
        red = []
        for n in range(0, 6):
            red.append(self.__holes[n].get_seeds())
        blue = []
        for n in range(11, 5, -1):
            blue.append(self.__holes[n].get_seeds())
        return red, blue

    def get_current_score(self):
        """
        Get method for players scores
        :return: tuple, integers with score for player one and player two
        """
        return self.__player_one_score, self.__player_two_score

    def last_hole(self, player):
        """
        Method checks if give player has the last hole with seeds.
        :param player: int, player who's side of the board is checked.
        :return: bool, True if player has only one hole with seeds left.
        """
        count = 0
        if player == 1:
            for n in range(11, 5, -1):
                if self.__holes[n].get_seeds() > 0:
                    count += 1
        if player == 2:
            for n in range(0, 6):
                if self.__holes[n].get_seeds() > 0:
                    count += 1
        if count == 1:
            return True


class OwareGame:
    """
    Class OwareGame represents the game UI using Tkinter canvas widget. 
    It integrate and make visible the logic written in class Board and Hole.
    """

    def __init__(self):
        """
        Initiate the game board and the canvas widget, fills it with necessary canvas items.
        """
        self.__redKey = "red"
        self.__blueKey = "blue"
        self.__bluePosition = []
        self.__redPosition = []
        self.__window = Tk()
        self.__window.title("Oware Game")
        self.__window.option_add("*Font", "Verdana 16")
        self.__canvas = tkinter.Canvas(self.__window, width=1000, height=1000, bg="white")
        self.__blueFillColor = "#00ddff"
        self.__redFillColor = "#ff9600"
        self.__board_logic = Board()

        self.create_tutorial_btn()

        self.__canvas.create_rectangle(200, 350, 800, 550, width=5, outline="green")

        self.create_multiple_oval_based_on_position(215, 365, 6, self.__blueKey, "white")
        self.create_multiple_oval_based_on_position(215, 465, 6, self.__redKey, self.__redFillColor)

        self.__announcementBox = self.__canvas.create_rectangle(400, 250, 600, 300, width=3, outline="green")
        self.__announcementText = self.__canvas.create_text(500, 275, text="Red's Turn", font="Verdana 20 bold", fill=self.__redKey)
        
        self.create_score_board()

        self.create_refresh_btn()

        self.set_initial_seeds()
        self.__isRedPlaying = True

        self.__canvas.pack()
        self.__window.mainloop()

    def create_tutorial_btn(self):
        """
        Method creates an artificial canvas button for tutorial.
        """
        self.__canvas.create_rectangle(400, 100, 600, 150, width=3, outline="green", activefill="yellow", tags="tutorial")
        self.__canvas.create_text(500, 125, text="Tutorial", font="Verdana 16", fill="green")
        self.__canvas.tag_bind("tutorial", "<Button-1>", self.open_instructions)

    def create_score_board(self):
        """
        Method creates score board.
        """
        self.__canvas.create_rectangle(400, 300, 600, 350, width=3, outline="green")
        self.blueScoreText = self.__canvas.create_text(450, 325, text="Blue: 0", font="Verdana 16", fill=self.__blueKey)
        self.redScoreText = self.__canvas.create_text(550, 325, text="Red: 0", font="Verdana 16", fill=self.__redKey)

    def create_refresh_btn(self):
        """
        Method creates an artificial canvas button for refresh.
        """
        self.__canvas.create_rectangle(400, 600, 600, 650, width=3, outline="green", activefill="yellow", tags="restart")
        self.__canvas.create_text(500, 625, text="Restart!", font="Verdana 16", fill="green")
        self.__canvas.tag_bind("restart", "<Button-1>", self.restart_game)

    def create_oval_based_on_position(self, x, y, color, size, activefill, fill, tags=''):
        """
        Method creates the holes UI rendered in the canvas.
        :param x: int, x coordinate of the center of the oval
        :param y: int, y coordinate of the center of the oval
        :param color: str, color of the oval
        :param size: int, size of the oval
        :param activefill: str, color of the oval when mouse is over it
        :param fill: str, color of the oval when it is not active
        :param tags: str, tags of the oval
        """
        self.__canvas.create_oval(x, y, x+size, y+size, width=3, outline=color, tags = tags, fill=fill, activefill=activefill)


    def create_multiple_oval_based_on_position(self, x, y, number, color, activefill, distance=100, size=75):
        """
        Method loops though a given number (6) and creates the holes UI rendered in the canvas.
        :param x: int, x coordinate of the center of the oval
        :param y: int, y coordinate of the center of the oval
        :param number: int, number of holes to be created
        :param color: str, color of the oval
        :param activefill: str, color of the oval when mouse is over it
        :param distance: int, distance between the center of the first and the last hole
        :param size: int, width of the rectangle that surrounds the oval
        """
        for i in range(number):
            self.create_oval_based_on_position(x, y, color, size, activefill, "white", tags=color + "_" + str(i))
            self.__canvas.tag_bind(color + "_" + str(i), "<Button-1>", self.on_click)
            if(color == self.__blueKey):
                self.__bluePosition.append((x, y, 4))
            elif(color == self.__redKey):
                self.__redPosition.append((x, y, 4))
            x += distance

    def create_seed_based_on_position(self,x, y, color="black", distance=15, size=5,shouldOffset=True):
        """
        Method creates the seeds (black dots) UI rendered in the canvas.
        :param x: int, x coordinate of the center of the oval
        :param y: int, y coordinate of the center of the oval
        :param color: str, color of the oval
        :param distance: int, distance between the center of the first and the last seed
        :param size: int, width of the rectangle that surrounds the oval
        :param shouldOffset: bool, if True, the seed will be offset from the center of the hole
        """
        initialPosition = (x, y)
        if shouldOffset:
            initialPosition = (x + distance + 10 , y + distance)        
        spacing = 20
        self.__canvas.create_oval(initialPosition[0], initialPosition[1], initialPosition[0] + size, initialPosition[1]+size, width=3, outline=color, fill=color)
        self.__canvas.create_oval(initialPosition[0] + spacing, initialPosition[1], initialPosition[0] + spacing + size, initialPosition[1]+size, width=3, outline=color, fill=color)
        return initialPosition

    def fill_hole(self, x, y, amount=1, verticalSpacing = 12):
        """
        Method fills the holes with seeds (black dots) based on the amount given in the arguement.
        :param x: int, x coordinate of the center of the oval
        :param y: int, y coordinate of the center of the oval
        :param amount: int, amount of seeds to be filled
        :param verticalSpacing: int, distance between the center of the first and the last seed
        """
        dynamicPosition = (x, y)
        numberOfEvenSeeds = amount // 2
        numberOfOddSeeds = amount % 2
        if amount == 1: 
            dynamicPosition = (dynamicPosition[0] + 36, dynamicPosition[1] + 36) # force it to be in the center
            self.create_oval_based_on_position(dynamicPosition[0], dynamicPosition[1], "black", size=5, activefill="black", fill="black")
            return

        for i in range(numberOfEvenSeeds):
            if i == 0:
                dynamicPosition = self.create_seed_based_on_position(dynamicPosition[0], dynamicPosition[1])
            else:
                dynamicPosition = (dynamicPosition[0], dynamicPosition[1] + verticalSpacing)
                self.create_seed_based_on_position(dynamicPosition[0], dynamicPosition[1], shouldOffset=False)

        if numberOfOddSeeds > 0:
            dynamicPosition = (dynamicPosition[0], dynamicPosition[1] + verticalSpacing)
            self.create_oval_based_on_position(dynamicPosition[0], dynamicPosition[1], "black", size=5, activefill="black", fill="black")

    def set_initial_seeds(self):
        """
        Method sets the initial seeds (black dots) in the game to render the first stage of the game.
        """
        for position in self.__bluePosition:
            self.fill_hole(position[0], position[1], position[2])

        for position in self.__redPosition:
            self.fill_hole(position[0], position[1], position[2])

    def renderLatestGameState(self):
        """
        Method is called everytime there is a player action to render the latest state of the Game.
        """
        boardState = self.__board_logic.get_current_board_state()
        for i in range(len(self.__redPosition)):
            self.__redPosition[i] = (self.__redPosition[i][0], self.__redPosition[i][1], boardState[0][i])
        
        for i in range(len(self.__bluePosition)):
            self.__bluePosition[i] = (self.__bluePosition[i][0], self.__bluePosition[i][1], boardState[1][i])
        self.update_score(self.__board_logic.get_current_score())
        self.set_initial_seeds()


    def set_ovals_Active_color(self, activecolor, listOfOvals, ovalColor):
        """
        Method sets the color of the hole to the active color, to help the players know that the hole is clickable.
        :param activecolor: str, color of the oval when mouse is over it
        :param listOfOvals: list, list of the ovals to be set to the active color
        :param ovalColor: str, color of the oval when it is not active
        """
        for i in range(len(listOfOvals)):
            item = self.__canvas.find_withtag((ovalColor + "_" + str(i)))
            self.__canvas.itemconfig(item, activefill=activecolor)

    def update_score(self, score):
        """
        Method updates the score UI rendered in the canvas.
        """
        self.__canvas.itemconfig(self.redScoreText, text="Red: " + str(score[0]))        
        self.__canvas.itemconfig(self.blueScoreText, text="Blue: " + str(score[1]))

    def get_position_number_from_tag(self, tag):
        """
        Method gets the position number from the string tag of the oval.
        :param tag: str, tag of the oval
        :return: int, position number of the oval
        """
        return int(tag.split()[0].split("_")[1])

    def refresh_board(self, turn, fillColor):
        """
        Method refreshes the board UI rendered in the canvas.
        :param turn: str, the next player (red or blue) that should be playing
        :param fillColor: str, color of the oval when it is not active
        """
        self.__canvas.delete("all")

        self.__bluePosition = []
        self.__redPosition = []

        self.create_tutorial_btn()

        self.__canvas.create_rectangle(200, 350, 800, 550, width=5, outline="green")

        if fillColor == self.__redKey:
            self.create_multiple_oval_based_on_position(215, 365, 6, self.__blueKey, "white")
            self.create_multiple_oval_based_on_position(215, 465, 6, self.__redKey, self.__redFillColor)
        else:
            self.create_multiple_oval_based_on_position(215, 365, 6, self.__blueKey, self.__blueFillColor)
            self.create_multiple_oval_based_on_position(215, 465, 6, self.__redKey, "white")

        self.__announcementBox = self.__canvas.create_rectangle(400, 250, 600, 300, width=3, outline="green")

        if self.__board_logic.player_win() and self.__board_logic.player_win() == "red":
            self.__announcementText = self.__canvas.create_text(500, 275, text="Red Won!", font="Verdana 20 bold", fill=self.__redKey)
        elif self.__board_logic.player_win() and self.__board_logic.player_win() == "blue":
            self.__announcementText = self.__canvas.create_text(500, 275, text="Blue Won!", font="Verdana 20 bold", fill=self.__blueKey)
        else:       
            self.__announcementText = self.__canvas.create_text(500, 275, text=turn, font="Verdana 20 bold", fill=fillColor)
        
        self.create_score_board()

        self.create_refresh_btn()
        self.renderLatestGameState()
            

    def on_click(self, event):
        """
        Method is called when the user clicks on a hole in the canvas.
        :param event: tkinter event, the event that triggered the method
        """
        item = event.widget.find_closest(event.x, event.y)
        tag = self.__canvas.itemcget(item, "tags")
        if self.__isRedPlaying and 'red' in tag:
                # call method to pick the red seeds
                self.__board_logic.player(1, self.get_position_number_from_tag(tag))
                self.refresh_board("Blue's Turn!", self.__blueKey)
                self.__isRedPlaying = not self.__isRedPlaying
        elif not self.__isRedPlaying and 'blue' in tag:
                self.__board_logic.player(2, (11 - self.get_position_number_from_tag(tag))) # have to refactor this api
                self.refresh_board("Red's Turn!",self.__redKey)
                self.__isRedPlaying = not self.__isRedPlaying


    def restart_game(self, event):
        """
        Method refreshes the game state and UI.
        :param event: tkinter event, the event that triggered the method
        """
        self.__board_logic = Board()
        self.__isRedPlaying = True
        self.refresh_board("Red's Turn!",self.__redKey)

    def open_instructions(self, event):
        """
        Method opens the tutorial window.
        :param event: tkinter event, the event that triggered the method
        """
        t = Toplevel(self.__window, bg="white")
        t.attributes("-alpha", 0.9)
        t.title("Tutorial")
        t.geometry("500x500")
        text = Text(t, bg = "#f0b3ff",font=("Helvetica", 14),width=400, height=400, padx=10, pady=10,wrap="word")
        
        text.insert("1.0", "1. The game starts with four seeds in each hole.\n")
        text.insert("2.0", "2. The objective of the game is to capture more seeds than one's opponent.\n")
        text.insert("3.0", "3. Players take turns moving the seeds.\n")
        text.insert("4.0", "4. On a turn, a player chooses one of the six holes under their color (control).\n")
        text.insert("5.0", "5. The player removes all seeds from that hole, and distributes them.\n")
        text.insert("6.0", "6. The distribution is done automatically by dropping one seed in each hole counter-clockwise in a process called sowing.\n")
        text.insert("7.0", "7. Capturing occurs only when a player brings the count of an opponent's hole to exactly two or three with the final seed he sowed in that turn.\n")
        text.insert("8.0", "8. This always captures the seeds in the corresponding hole, and possibly more.\n")
        text.insert("9.0", "9. The first side to Capture 24 seeds win the game.\n")
        text.insert("10.0", "10. For more info : https://en.wikipedia.org/wiki/Oware.\n")
        text.pack()
        

def main():
    OwareGame()


if __name__ == "__main__":
    main()