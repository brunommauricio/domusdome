from tkinter import *
from tkinter import ttk
import serial

#
# Data describing rooms blueprint
#
ROOMS = 3 # total number of defined rooms
FLOOR_OFFSET = ('2c', '1c', 0)  # displace floor for easier viewing
FLOOR_COLORS = {} # colors for various levels, walls and rooms
FLOOR_SHAPE = {} # polygon coordinates for basic shape of floor
FLOOR_OUTLINE = {} # line coordinates to draw outline around floor
FLOOR_WALLS = {}# line coordinates to draw walls within the floor
FLOOR_ROOMS = {} # data order: polygon, label position, room number
#
# Colour definitions
#
FLOOR_COLORS = {'bg': ('#a9c1da', '#9ab0c6','#8ba0b3'),
        'outline': ('#77889a', '#687786', '#596673'),
        'offices': 'black',
        'active': '#c4d1df'}
#
# First floor data
#
FLOOR_SHAPE[0] = 
FLOOR_OUTLINE[0] = ()
FLOOR_WALLS[0] = ()
FLOOR_ROOMS[0] = ()
#
# Second floor data
#
FLOOR_SHAPE[1]
FLOOR_OUTLINE[1]
FLOOR_WALLS[1]
FLOOR_ROOMS[1]
#
# Third floor data
#
FLOOR_SHAPE[2]
FLOOR_OUTLINE[2]
FLOOR_WALLS[2]
FLOOR_ROOMS[2]
# ======================================================================================
# Main Class
# ======================================================================================
class DomusDomeGui(ttk.Frame):
    
  def __init__(self, isapp=True, name='domusdomegui'):
    ttk.Frame.__init__(self, name=name)
    self.pack(expand=Y, fill=BOTH)
    self.master.title('domusdomegui')
    self.isapp = isapp
    self._create_widgets()
      
  def _create_widgets(self):
    if self.isapp:
      f = ttk.Frame(self)
      f.pack(side=TOP, expand=Y, fill=X)
          
      msgtxt = ["This window contains a canvas widget showing the floorplan ",
              "of Digital Equipment Corporation's Western Research Laboratory. ",
              "It has three levels.   At any given time one of the levels is ",
              "active, meaning that you can see its room structure.   ",
              "To activate a level, click the left mouse button anywhere on it.   ",
              "As the mouse moves over the active level, the room under the mouse ",
              "lights up and its room number appears in the \"Room:\" entry.   ",
              "You can also type a room number in the entry and the room will light up."]
        
      msg = ttk.Label(f, wraplength=900, justify=CENTER, anchor=CENTER, name='msgpanelmsg')
      msg['text'] = ''.join(msgtxt)
      msg.pack(expand=Y, fill=X, padx=5, pady=5)
      ttk.Separator(f, orient=HORIZONTAL).pack(side=TOP, expand=Y, fill=X)
  
        
      SeeDismissPanel(self)
      
    self._create_demo_panel()
      
  def _create_demo_panel(self):
    demoPanel = ttk.Frame(self, name='demo')
    demoPanel.pack(side=TOP, fill=BOTH, expand=Y)
      
    self._create_attrib_vars()       # variables used throughout
    self.__base = self._create_canvas_panel(demoPanel)
      
    self._load_floor_data(NUM_FLOORS)     # get all floor data
    self._draw_floors(NUM_FLOORS)
    self._add_bindings()
    self.__activeFloor = self.__floorTags[NUM_FLOORS-1]
    self._display_floor(None, NUM_FLOORS-1) # display top floor
          
  def _create_attrib_vars(self):    
    # create and set default values for internal variables  
    self.__activeFloor = ""        
    self.__floorData = {}
    self.__floors = {}           # floor widgets
    self.__floorTags = {}           # floor name tags
    self.__floorLabels = {}       # room names
    self.__floorItems = {}         # handles to rooms
    self.__currentRoom = StringVar()       # value of current room
    self.__entry = None         # display/capture current room
      
  def _create_canvas_panel(self,parent):
    f = ttk.Frame(parent)
    f.pack(side=TOP, fill=BOTH, expand=Y, padx=1, pady=1)
    f.grid_rowconfigure(0, weight=1, minsize=0)
    f.grid_columnconfigure(0, weight=1, minsize=0)
      
    hscroll = ttk.Scrollbar(f, orient=HORIZONTAL)
    vscroll = ttk.Scrollbar(f, orient=VERTICAL)
      
    f1 = ttk.Frame(f, relief=SUNKEN)
    base = Canvas(f1, width=900, height=500,
              highlightthickness=0,
              xscrollcommand=hscroll.set,
              yscrollcommand=vscroll.set)
    vscroll.configure(command=base.yview)
    hscroll.configure(command=base.xview)
      
    base.pack(side=TOP, expand=Y, fill=BOTH)
      
    f1.grid(padx=1, pady=1, row=0, column=0,
        rowspan=1, columnspan=1, sticky='news')
    vscroll.grid(padx=1, pady=1, row=0, column=1,
            rowspan=1, columnspan=1, sticky='news')
    hscroll.grid(pady=1, row=1, column=0,
            rowspan=1, columnspan=1, sticky='news')
  
    # Create an entry for displaying and typing in the current room.
    self.__entry = ttk.Entry(base, width=20, textvariable=self.__currentRoom)
    base.create_window(600,100, anchor='w', window=self.__entry)
    base.create_text(600,100, anchor='e', text='Room: ')
      
    return base
  # ======================================================================================
# Bindings and bound routines
# ======================================================================================
  def _add_bindings(self):
    # bind left mouse button click to all floors
    for floor in range(NUM_FLOORS):
      tagid = self.__floorTags[floor]
      self.__base.tag_bind(tagid,'<1>',
                lambda e, f=floor: self._display_floor(e, f))
        
    # bind rooms to mouse Enter/Leave events
    self.__base.tag_bind('room', '<Enter>', self._enter_room)
    self.__base.tag_bind('room', '<Leave>', self._leave_room)
      
    # bind room labels to mouse Enter/Leave events
    self.__base.tag_bind('label', '<Enter>', self._enter_room)
    self.__base.tag_bind('label', '<Leave>', self._leave_room)
  
    # bind to entry to catch user room selection
    self.__entry.bind('<KeyRelease>', self._user_sel_room)
                                                                    
  def _user_sel_room(self, *args):
    # triggered when the user enters a valid room
    # number for the active floor
    self._turn_off_highlight()
    room = self.__currentRoom.get()
      
    if room in self.__floorItems.keys():
      wid = self.__floorItems[room]
      self.__base.addtag_withtag('highlight', wid)
      self._enter_room(None, wid=wid)
        
  def _turn_off_highlight(self):
    # turn off highlight on any previous
    # user selected rooms
    sel = self.__base.find_withtag('highlight')
  
    if sel:
      self.__base.dtag(sel[0], 'highlight')
      self.__base.itemconfigure(sel[0], fill='')
          
  def _enter_room(self, evt, wid=None):
    # triggered when the mouse pointer enters a room
    # or the user has entered a new room number
    if not wid:
      wid = self._get_room_id()
      self._turn_off_highlight()  
        
    # set 'Room entry' to room number
    self.__currentRoom.set(self.__floorLabels[wid])
      
    # turn on room's highlight
    self.__base.itemconfigure(wid, fill=FLOOR_COLORS['active'])
    self.update_idletasks()
    
  def _leave_room(self, evt):
    # triggered when the mouse pointer leaves a room
    wid = self._get_room_id()
      
    # turn off the room highlight
    self.__base.itemconfigure(wid, fill='')
      
    # reset current room
    self.__currentRoom.set('')
      
  def _get_room_id(self):
    # get the wid of the active room
    wid = self.__base.find_withtag(CURRENT)[0]
    tags = self.__base.gettags(CURRENT)
    
    if 'label' in tags: # in a label, get it's room
      wid = self.__base.find_below(wid)[0]
      
    return wid
          
  def _display_floor(self, evt, level):
    # triggered when the user selects a floor
      
    # hide all the floors
    for floor in self.__floorTags.values():
      self.__base.itemconfigure(floor, state=HIDDEN)
      
    # turn on all backgrounds
    self.__base.itemconfigure('bg', state=NORMAL)
    self.__base.itemconfigure('outline', state=NORMAL)
      
    # reset the new active floor
    self.__activeFloor = self.__floorTags[level]
  
    # show all features for the active floor
    self.__base.itemconfigure(self.__activeFloor, state=NORMAL)
          
    # put all floors back in order
    for tagid in self.__floorTags.values():
      self.__base.tag_raise(tagid)
      
    # raise the active floor to the top
    self.__base.tag_raise(self.__activeFloor)
  # ======================================================================================
# Routines to load and draw the floors
# ======================================================================================
  def _load_floor_data(self, numFloors):
    for num in range(numFloors):
      self.__floorData[num] = {"bg": {"shape": FLOOR_SHAPE[num],
                      "outline": FLOOR_OUTLINE[num]},
                    "wall": FLOOR_WALLS[num],
                    "room": FLOOR_ROOMS[num]}
  
  def _draw_floors(self, numFloors):
      
    for item in range(numFloors):
      floorTag = 'floor{}'.format(item+1)
        
      # draw the floor's shape and outline
      tags = (floorTag, 'bg')
        
      for p in self.__floorData[item]['bg']['shape']:
        self.__base.create_polygon(p, tags=tags,
                          fill=FLOOR_COLORS['bg'][item])
        
      for l in self.__floorData[item]['bg']['outline']:
        self.__base.create_line(l, tags=tags,
                    fill=FLOOR_COLORS['outline'][item])
    
      # create a text label and 'highlight' polygon for the room
      for room, lblPos, name in self.__floorData[item]['room']:            
        rm = self.__base.create_polygon(room, fill='',
                        tags=(floorTag, 'room'))
                  
        self.__base.create_text(lblPos, text=name, fill=FLOOR_COLORS['offices'],
                    tags=(floorTag, 'label'), anchor='c')                    
                  
        self.__floorLabels[rm] = name       # save the room's name
        self.__floorItems[name] = rm   # save a handle to the room's highlight polygon
                
      # draw the room's walls
      tags = (floorTag, 'wall')
      for w in self.__floorData[item]['wall']:
        self.__base.create_line(w, tags=tags,
                      fill=FLOOR_COLORS['offices'])
          
      # offset the floor for easier viewing
      self.__base.move(floorTag, FLOOR_OFFSET[item], FLOOR_OFFSET[item])
                
      # hide the floor
      self.__base.itemconfigure(floorTag, state=HIDDEN)
        
      # same the floor's tag
      self.__floorTags[item] = floorTag
          
if __name__ == '__main__':
  FloorPlanDemo().mainloop()























