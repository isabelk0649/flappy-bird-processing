import random
import os
import json
import pickle
from datetime import datetime

config = 'config.json'
        
add_library("minim")
    
class Wall:
    def __init__(self, img, gap=100, x=0, y=0, horizontal=5):
        self.img = img
        self.gap = gap
        self.x = x
        self.y = y
        self.horizontal = horizontal

    def move(self):
        self.x -= self.horizontal

    def center(self):        
        self.x = 0
        self.y = height/2

        
    def display(self):
        imageMode(CENTER)
        image(self.img, self.x, self.y - (self.img.height/2 + self.gap)) # top wall
        image(self.img, self.x, self.y + (self.img.height/2 + self.gap)) # bottom wall 
        

class Dog:
    def __init__(self, img, x=0, y=0, horizontal=4, vertical=12, name=None):
        self.img = img
        self.x = x
        self.y = y
        self.horizontal = horizontal
        self.vertical = -vertical
        self.name = name
        self.score = 0
        self.scores = []
        
    def jump(self, h):
        self.vertical = -h
    
    def center(self):
        self.x = 0
        self.y = height/2
        
    def move(self):
        self.x -= self.horizontal
        self.vertical +=1
        self.y += self.vertical
        
    def highscore(self):
        return max(self.scores)
    
    def display(self, xscore=10, yscore=40):
        imageMode(CENTER)
        image(self.img, width/2, self.y)
        text("Score: "+ str(self.score), xscore, yscore)
        
#class Game:
#    def __init__(self):
#        self._data={}
#        
#    def addBackground(self, img):
#        self._data['background'] = {'img' : img, 'buttons': {}}
#        
#    def addHelp(self, img, buttons={}):
#        self._data['help'] = {'img' : img, 'buttons': {}}
        
def setup():
    
    global background_img
    global start_screen_img
    global gameover_img
    global help_img
    global input_name_img
    global scores_img
    
    global scores
    global speed

    global mode
    global start_button, replay_button, help_button, scores_button, back_button, menu_button
        
    global walls
    global dog
    global fontsize
    global config
    global jump_height
    global play_starttime
    global chase
    
    size(600,800)
    fill(0,0,0)
    
    # read configuration from json file.
    # name of the json file depend on the option (1,2)
    setup_info = json.load(open(config))

    mode='start'
    if os.path.isfile('scores.pkl'):
        with open('scores.pkl', 'rb') as fh:
            scores = pickle.load(fh)
    else:
        # if not initialize scores dict
        scores = {}
    
    dog = Dog(loadImage("flappy_doge.png"), -200, 0)
    
    keyp =""    

    # img
    background_img=loadImage("background_screen.png")
    start_screen_img=loadImage("start_screen.png")
    scores_img=loadImage("scores.png")
    help_img=loadImage("help.png")
    input_name_img=loadImage("input_name.png")
    gameover_img=loadImage("gameover.png")
    
    minim = Minim(this)
    chase = minim.loadFile("chase.mp3")
        

    # window size
    window_size = setup_info['window_size']
    
    #buttons
    start_button = setup_info['start_button']
    replay_button = setup_info['replay_button']
    help_button = setup_info['help_button']
    scores_button = setup_info['scores_button']
    back_button = setup_info['back_button']
    menu_button = setup_info['menu_button']
    
    #fontsize
    fontsize = setup_info['fontsize']
    textSize(fontsize)
    
    #speed
    speed = setup_info['speed']
    #jump_height
    jump_height = setup_info['jump_height']
    #wall_gap
    wall_gap = setup_info['wall_gap']
    
    wall1 = Wall(loadImage("wall.jpg"), wall_gap, width, height/2)
    wall2 = Wall(loadImage("wall.jpg"), wall_gap, 3*width/2, 3*height/2)
    walls = [wall1, wall2]

    #scores area
    scores_rect = setup_info['scores_rect']
    
    cdir=os.path.curdir

    
def draw():
    global mode, window_size
    global fontsize, scores_rect
    global walls, dog
    global speed
    global fontsize
    global scores
    global play_starttime
    
    background(0)
    
    chase.play()
    
    if mode == 'play':
        # if mode is 0 then game is on
        # display background image (1800x600 pixels) relative to top-left corner of the window (600,800)

        #ms = milliseconds()
        #print(ms, "Dog starts at: (", dog.x, dog.y)
        imageMode(CORNER)
        image(background_img, dog.x, 0);
        image(background_img, dog.x + background_img.width, 0);
        
        # move the dog relative to the background image
        dog.move()
        
        #print(ms, "Dog moved to: (", dog.x, dog.y)
        # reset x if we are off limits
        if dog.x == -(background_img.width):
            dog.x = 0
        
        for i,wall in enumerate(walls):
            #print(ms, "Wall", i, " starts at: ", wall.x, wall.y)
            wall.display()
            
            if wall.x < 0:
                #reposition the wall
                wall.x = width;
                wall.y = random.randint(200,height-200)
                
            if dog.y>height or dog.y<0 or (abs(width/2-wall.x)<wall.img.width/2 and abs(dog.y-wall.y)>wall.gap):
                # if the dog got out of the window on (an y-axis) or the dog has hit the walls (either the top wall or the bottom wall)
                mode='gameover'
                update_scores()

            if wall.x == width/2:
                # the dog made it unharmed through the gap in the walls
                dog.score+=1
                
            # shift the walls to the left (at center)
            wall.move()
            #print(ms, "Wall", i, " moved to: ", wall.x, wall.y)
            
        # display dog with the center of the image located in the middle of the window at height y 
        dog.display()
        
    elif mode == 'getname':
        # if mode is 'getname' -> display text
        imageMode(CENTER);
        image(input_name_img, width/2, height/2)
        text(dog.name, 35, 300)
        
    elif mode == 'start':
        imageMode(CENTER);
        image(start_screen_img, width/2, height/2)
        
    elif mode =='gameover':
        # game is over display start screen 
        imageMode(CENTER);
        image(gameover_img, width/2, height/2)
        text(str(dog.score), 380, 280)
        
    elif mode =='help':
        # game is over display start screen 
        imageMode(CENTER);
        image(help_img, width/2, height/2)
        
    elif mode =='scores':
        # display scores screen
        imageMode(CENTER);
        image(scores_img, width/2, height/2)
        
        y0 = 220
        ydelta = fontsize + 5
        for pname,pscores in scores.items():
            text(pname + " : " + str(max(pscores)), 75, y0)
            y0+=ydelta
        
def update_scores():
    global scores
    if dog.name in scores:
        # add the score to the list of scores
        scores[dog.name].append(dog.score)
    else:
        # set the fist score in the list
        scores[dog.name] = [dog.score]
        
def clicked_on_start_button():
    global start_button
    if start_button[0][0] <= mouseX <= start_button[1][0]:
        if start_button[0][1] <= mouseY <= start_button[1][1]:
            return True
    return False
     
def clicked_on_replay_button():
    global replay_button
    if replay_button[0][0] <= mouseX <= replay_button[1][0]:
        if replay_button[0][1] <= mouseY <= replay_button[1][1]:
            return True
    return False
    
def clicked_on_help_button():
    global help_button
    if help_button[0][0] <= mouseX <= help_button[1][0]:
        if help_button[0][1] <= mouseY <= help_button[1][1]:
            return True
    return False

def clicked_on_scores_button():
    global scores_button
    if scores_button[0][0] <= mouseX <= scores_button[1][0]:
        if scores_button[0][1] <= mouseY <= scores_button[1][1]:
            return True
    return False

def clicked_on_back_button():
    global back_button
    if back_button[0][0] <= mouseX <= back_button[1][0]:
        if back_button[0][1] <= mouseY <= back_button[1][1]:
            return True
    return False
    
def clicked_on_menu_button():
    global menu_button
    if menu_button[0][0] <= mouseX <= menu_button[1][0]:
        if menu_button[0][1] <= mouseY <= menu_button[1][1]:
            return True
    return False

# returns the elapsed milliseconds since the start of the program
def milliseconds():
    dt = datetime.now() - play_starttime
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    return ms

def mousePressed():
    global mode, walls, dog, jump_height
    # if mouse is pressed anywhere withing the window (600x800)
    # jumps the dog up 15 pixels along the y axis with each click
    
    #vertical = -(jump_height)
    dog.jump(jump_height)
    
    # if game is over
    #print('-----mousePressed------')
    #print('Mouse clicked at: ', (mouseX, mouseY))
    if mode=='start':
        if clicked_on_start_button():
            dog.name = ""
            mode = 'getname'
        elif clicked_on_scores_button():
            if len(scores) > 0:
                with open('scores.pkl', 'wb') as fh:
                    pickle.dump(scores, fh)
            mode = 'scores'
            
        elif clicked_on_help_button():
            mode = 'help'
        elif clicked_on_replay_button():
            # can replay only if we have a name
            if dog.name:
                dog.score = 0
                # set starting wall coordinates
                # first wall at (600,400) 
                # second wall at (900,600)
                walls[0].x = 600
                walls[0].y = height/2  #400
                walls[1].x = 900
                walls[1].y = 600
                # set the starting location for the dog (0, 400)
                #sets dog location to (0, height/2)
                dog.center()
                # and start the game
                mode = 'play'
                play_starttime = datetime.now()
    elif mode == 'gameover':
        if clicked_on_menu_button():
            mode = 'start'
    elif mode == 'help':
        if clicked_on_back_button():
            mode = 'start'
    elif mode == 'scores':
        if clicked_on_back_button():
            mode = 'start'
    #print('-----mousePressed------')
    #loop()
    

def keyReleased():
    global keyp, mode, dog
    global scores
    global play_starttime
    keyp = key
    if mode == 'getname':
        if keyp != ENTER:
            dog.name+= keyp.upper()
        else:
            #print('keyReleased: ', 'ENTER')
            print('Player name: ', dog.name)
            # change mode to from 'getname -> 'play'
            dog.score = 0
            # set starting wall coordinates
            # first wall at (600,400) 
            # second wall at (900,600)
            walls[0].x = 600
            walls[0].y = height/2  #400
            walls[1].x = 900
            walls[1].y = 600
            # set the starting location for the dog (0, 400)
            #location = [0, height/2]
            dog.center()
            # and start the game
            mode = 'play'
            #print('>>> game started >>>')
            fill(0,0,0)
            # delay for 1 second 
            delay(1000)
            play_starttime = datetime.now()

    #loop()    
