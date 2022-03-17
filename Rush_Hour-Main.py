# ==============================================================================
"""RUSH HOUR : Create the Rush Hour game"""
# ==============================================================================
__author__  = "Tristan Gonçalves"
__version__ = "3.0"         # operational RUSH HOUR game 
__date__    = "2019-04-10"
# ------------------------------------------------------------------------------
from ezTK import *
from ezCLI import read_ini
#===============================================================================

dictionnaire = {'.':0,'A':1,'B':2,'C': 3,'D':4,'E': 5,'F':6,'G': 7 ,'H': 8,
                'I': 9,'J': 10,'K': 11,'L': 12,'M': 13,'Z':  14}
# ======================================================================
def level_selector( size = 64 ):
    """Player selects a level, then level is displayed"""
    global selected_level, levels
    levels = read_ini('rush.ini') #read INI file
    print('\nNOTE : If you want a level less than 09, write it like this : 0X \n')
    selected_level = input("Choose a level between 01 and 40:") #ask the user to chose a level
    if selected_level not in levels :
        print ("\n<> The chosen level is not available, please try another one.<>")
        on_restart()
    # -------------------------------------------------------------------------
    label = win.label
    win.label['text'] = ('Level',selected_level)

# ========================================================================
def on_reset():
    """Callback function for the RESET button"""
    board = win.board
    for i in range ( len( levels[selected_level])):
        n = levels[selected_level][i]
        
        if i == 6 or i == 13 or i == 20 or i == 27 or i == 34 or i == 41 :
            continue
        if i <6 : l = 0 
        elif i > 6 and i < 13 : l = 1
        elif i >13 and i < 20 : l = 2
        elif i >20 and i < 27 : l = 3
        elif i >27 and i < 34 : l = 4
        elif i >34 and i < 41 : l = 5

        if i==0 or i%7 ==0 : k = 0
        elif i%7 == 1 : k = 1
        elif i%7 == 2 : k = 2
        elif i%7 == 3 : k = 3
        elif i%7 == 4 : k = 4
        elif i%7 == 5 : k = 5

        board[k][l].state = dictionnaire[n] #change colors of Bricks with chosen level
# ========================================================================
def on_click(widget, code, mods):
    board, n = win.board, widget.index
    if widget.master != board or n is None:
        return  #nothing to do if the mouse click is not on a car
    # ---------------------------------------------
    if widget.state != 0 :
        if n[1]!=5: 
            if board[n[0]][n[1]-1].state == board[n[0]][n[1]].state :          #car goes down
                if n[1] == 5 or board[n[0]][n[1]+1].state != 0: return  
                elif n[1] > 1:
                    if board[n[0]][n[1]-2].state == board[n[0]][n[1]].state:
                        board[n[0]][n[1]+1].state, board[n[0]][n[1]-2].state = board[n[0]][n[1]].state,0
                    else:
                        board[n[0]][n[1]+1].state, board[n[0]][n[1]-1].state = board[n[0]][n[1]].state, 0
                else:
                    board[n[0]][n[1]+1].state, board[n[0]][n[1]-1].state = board[n[0]][n[1]].state, 0

                
            elif board[n[0]][n[1]+1].state == board[n[0]][n[1]].state :         #car goes up
                if n[1] == 0 or  board[n[0]][n[1]-1].state != 0: return
                elif n[1] < 4 :                           #avoid IndexError : list index out of range
                    if board[n[0]][n[1]+2].state == board[n[0]][n[1]].state:
                        board[n[0]][n[1]-1].state, board[n[0]][n[1]+2].state = board[n[0]][n[1]].state,0
                    else:
                        board[n[0]][n[1]-1].state, board[n[0]][n[1]+1].state = board[n[0]][n[1]].state,0
                else:
                    board[n[0]][n[1]-1].state, board[n[0]][n[1]+1].state = board[n[0]][n[1]].state,0

        if n[0] !=5:          
            if board[n[0]-1][n[1]].state == board[n[0]][n[1]].state :         #car goes right
                if n[0] == 5 or  board[n[0]+1][n[1]].state != 0: return
                elif n[0]>1 :
                    if board[n[0]-2][n[1]].state == board[n[0]][n[1]].state:
                        board[n[0]+1][n[1]].state, board[n[0]-2][n[1]].state = board[n[0]][n[1]].state,0
                    else:
                        board[n[0]+1][n[1]].state, board[n[0]-1][n[1]].state = board[n[0]][n[1]].state,0
                else:
                    board[n[0]+1][n[1]].state, board[n[0]-1][n[1]].state = board[n[0]][n[1]].state,0
                    
            elif board[n[0]+1][n[1]].state == board[n[0]][n[1]].state :         #car goes left
                if n[0] == 0 or  board[n[0]-1][n[1]].state != 0: return
                if n[0]<4 :
                    if board[n[0]+2][n[1]].state == board[n[0]][n[1]].state :
                        board[n[0]-1][n[1]].state, board[n[0]+2][n[1]].state = board[n[0]][n[1]].state,0
                    else:
                        board[n[0]-1][n[1]].state, board[n[0]+1][n[1]].state = board[n[0]][n[1]].state,0
                else:
                    board[n[0]-1][n[1]].state, board[n[0]+1][n[1]].state = board[n[0]][n[1]].state,0

    # -------------------------------------------------------------------
    if board[5][2].state == 14:
      on_popup()
      
# ========================================================================
def on_popup():
  """callback for the "POPUP" when level won """    
  popup = Win(win, title='Victory !', flow='E', op=2)
  Label(popup, text='Congratulations, you WIN ! :)', font = 'Arial 48', bg = '#0F0')
  popup.wait()      #wait until the popup has been closed
  popup_restart()   #call the function popup_restart
# ========================================================================   
def popup_restart():
    """callback for the 'START NEW LEVEL' button and when level is finished"""
    #create the ending popup, to start a new level
    popup_start_again = Win(win, title='NEW GAME ?', op = 2, bg = 'black', grow = False)
    Label(popup_start_again, text='Restart a new game ?', font = 'Elephant 48', fg='#FFF', bg = 'black')
    frame_buttons = Frame(popup_start_again)
    Button(frame_buttons, text = 'YES',  command = on_restart, font = 'Elephant 30', bg = 'green', fg='#FFF')
    Button(frame_buttons, text = 'NO' ,  command = win.exit  , font = 'Elephant 30', bg = 'red'  , fg='#FFF')

# ========================================================================   
def on_restart():
    """callback for the 'START NEW LEVEL' button and when level is finished"""
    win.exit()  
    main()
# ========================================================================   
def main(rows=6, cols=6, size = 64):
  """create the main window and pack the widgets"""
  global win
  win = Win(title='RUSH HOUR',grow= False, op = 0, flow = 'SE', click = on_click)
  colors = ('#FFF','#FFFF00','#0F0' ,'#FF00FF','#00F','#00BFFF',
            '#FF8C00','#FFC0CB','#808080','#B22222','#808000',
            '#6a2d20','#123','#33CCCC','#F00')
  # --------------------------------------------------------------------
  frame  = Frame (win, border = 2, relief = 'groove')
  label  = Label(frame, text = '', font = 'Elephant 20 bold')
  # --------------------------------------------------------------------
  board = Frame(win, fold = 6, flow = 'SE')
  #create the Brick board
  for loop in range (rows*cols):
      Brick(board, bg = colors, height = size,width = size, border = 1)
  Button(win, grow=False, text='RESET', command=on_reset)
  Button(win, grow=False, text='START NEW LEVEL', command=on_restart)

  #create border with EXIT
  for i in range (6):
      if i == 2 : Label (board, text= 'EXIT', bg = '#FFF')
      else :      Label (board, text= None, bg = '#000', border = 0)

  # --------------------------------------------------------------------
  win.label = label
  win.board = board
  level_selector(); on_reset(); win.loop()
# ------------------------------------------------------------------------ 
 
if __name__ == '__main__':
  main()
# ========================================================================
