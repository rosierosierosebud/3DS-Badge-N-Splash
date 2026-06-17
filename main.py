import pygame
import pygame_textinput
print("import success!")
#https://www.marcrobledo.com/smdh-creator/ smdh creator for future use
import os
import sys
import time
from PIL import Image
from tkinter import Tk, filedialog
Tk().withdraw()
pygame.init()

t_i = pygame_textinput.TextInputVisualizer()

run = True
#setup
w, h = 600, 600
screen = pygame.display.set_mode((w, h))
txtin = pygame_textinput.TextInputVisualizer()
path = os.path.dirname(__file__)
outputpath = os.path.join(path, "Output/") 
bg = pygame.image.load(os.path.join(path, "assets/bg.png")).convert_alpha() 
font = pygame.font.Font(os.path.join(path, "assets/font.ttf"), 36)
font_s = pygame.font.Font(os.path.join(path, "assets/font.ttf"), 19)

s_button = pygame.image.load(os.path.join(path, "assets/splash_button.png")).convert_alpha()
b_button = pygame.image.load(os.path.join(path, "assets/badge_button.png")).convert_alpha()
h_button = pygame.image.load(os.path.join(path, "assets/helpicon.png")).convert_alpha()
i_button = pygame.image.load(os.path.join(path, "assets/import.png")).convert_alpha()

mode = 0
helpmenu = False
fa = (font.size("Badge/Splash Maker!")[0]/2)
fh = (font.get_height())
fhs = (font_s.get_height())
YEL = (255, 255, 0)
RED = (255, 0, 0)
BLU = (0, 0, 255)
BLU2 = (0, 60, 50)
WHI = (255, 255, 255)

class Button():
    def __init__(self, x, y, image, scale):
        self.width = image.get_width()
        self.height = image.get_height()
        self.scale = scale
        self.image = pygame.transform.scale(image, (int(self.width*scale), int(self.height*scale)))
        self.original = self.image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.image = pygame.transform.scale(self.image, (int(self.width*self.scale*1.1), int(self.height*self.scale*1.1)))
            if pygame.mouse.get_pressed()[0]== 1 and self.clicked == False:
                self.clicked = True
                action = True
        else:
            self.image = self.original
        if pygame.mouse.get_pressed()[0]== 0:
            self.clicked = False
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action
    
splash_button = Button(w/2-135, h/3, s_button, 1)
badge_button = Button(w/2-135, h/1.8, b_button,1)
help_button = Button(w/3-fa, h/7+(font_s.get_height()*2), h_button, .5)
import_button = Button(w/2-i_button.get_width()/2, h/2, i_button, 1)
import_button_2 = Button(w/2-i_button.get_width()/2, h/2-i_button.get_height()-10, i_button, 1)

clock = pygame.time.Clock
fps = 60

def txt(text, font, col, x, y):
    renderedtext = font.render(text, True, col)
    screen.blit(renderedtext, (x, y))

pygame.display.flip()
pygame.display.set_caption("3DS SPLASH SCREEN & BADGE MAKER")

#actual like program
def text_input_badge():
    global run
    inputtingtext = True
    while inputtingtext == True:
        events = pygame.event.get()
        t_i.update(events)
        screen.blit(bg, (0,0))
        txt("This is the Badge Creator! Please note that this program ", font_s, BLU2, w/3-fa, h/9)
        txt("does require an external image editor.", font_s, BLU2, w/3-fa, h/9+font_s.get_height())
        txt("Export Name:", font_s, BLU, w/3-(fa/2), h/9+font_s.get_height()*2)
        help_button.draw()
        screen.blit(t_i.surface, (w/2, h/9+font_s.get_height()*2))
        if [ev for ev in events if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN]:
            inputtingtext = False
        pygame.display.flip()
    return t_i.value
nameset = False
Exname = "a"
def import_process():
    if not os.path.exists(outputpath):
        os.makedirs(outputpath)
    if not os.path.exists(os.path.join(outputpath, f"{Exname}/")):
        os.makedirs(os.path.join(outputpath, f"{Exname}/"))
    file = filedialog.askopenfilename(
        title="Select a file to import.",
        filetypes=[("PNG Files", "*.png")]
    )
    if file:
        num = 0
        print(str(file))
        with Image.open(file) as img:
            img_width, img_height = img.size
            ts = 64
            for top in range(0, img_height, ts):
                for side in range(0, img_width, ts):
                    o_side = min(side + ts, img_width)
                    bo = min(top + ts, img_height)
                    box = (side, top, o_side, bo)
                    tile = img.crop(box)
                    num += 1
                    tile.save(os.path.join(outputpath, f"{Exname}/{Exname}_{num}.png"))

def convert2bin(screen, s_path):
    try:
        if screen == "top":
            ideal_dimensions = (400, 240)
            op_name = "splash.bin"
        elif screen == "bottom":
            ideal_dimensions = (320, 240)
            op_name = "splash_bottom.bin"
        else:
            raise ValueError("Error! Not a screen type, must be \"top\" or \"bottom\". This is probably not your fault, please contact the developer.")
        with Image.open(s_path) as img_s:
            wid, hei = img_s.size
            if wid > ideal_dimensions[0] or hei > ideal_dimensions[1]:
                raise ValueError("Error! Image is too large, must be within confines: Top Screen- Width 400, Height 240. Bottom Screen- Width 320, Height 240. One of these is wrong in your image!")
        c_img = Image.open(s_path).convert("RGB")
        c_img = c_img.rotate(-90, expand=True)
        r, g, b = c_img.split()
        c_img = Image.merge("RGB", (b, g, r))
        o_path = os.path.join(outputpath, f"{Exname}/{op_name}")
        if not os.path.exists(f"{outputpath}/{Exname}"):
            os.makedirs(f"{outputpath}/{Exname}")
        with open(o_path, "wb") as outputfile:
            outputfile.write(c_img.tobytes())
        print(f"Success! Generated: " + op_name + f", you can find it in the Output/{Exname} folder.")
    except AttributeError:
        pass

def import_splash(screen):
    if not os.path.exists(outputpath):
        os.makedirs(outputpath)
    if not os.path.exists(os.path.join(outputpath, f"{Exname}/")):
        os.makedirs(os.path.join(outputpath, f"{Exname}/"))
    file = filedialog.askopenfilename(
        title="Select a file to import.",
        filetypes=[("PNG Files", "*.png")]
    )
    convert2bin(screen, file)

def mainloop_badgemakr():
    global run
    global helpmenu
    global nameset
    global Exname
    events = pygame.event.get()
    if [ev for ev in events if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN]:
        Exname = text_input_badge()
        nameset= True
    try:
         val
    except NameError:
         val = "(Press Enter)"
    if nameset == True:
        val = Exname
    txt("This is the Badge Creator! Please note that this program ", font_s, BLU2, w/3-fa, h/9)
    txt("does require an external image editor.", font_s, BLU2, w/3-fa, h/9+font_s.get_height())
    txt("Export Name: "+ val, font_s, BLU, w/3-(fa/2), h/9+font_s.get_height()*2)
    if import_button.draw() and helpmenu == False:
        import_process()
    if help_button.draw():
        helpmenu = True
    if helpmenu == True:
        h_r = pygame.Rect(50, 50, 500, 500)
        pygame.draw.rect(screen, BLU2, h_r)
        txt("Help Menu-- ESC to exit", font, WHI, 60, 60)
        txt("1. Enter the export name", font, WHI, 60, 65+fh)
        txt("2. Click the import button.", font, WHI, 60, 65+(fh*2))
        txt("3. Select a PNG image.", font, WHI, 60, 65+(fh*3))
        txt("Image must be divisible", font, WHI, 60, 65+(fh*4))
        txt("by 64! Badges are 64x64!", font, WHI, 60, 65+(fh*5))
        txt("4. Locate Output folder.", font, WHI, 60, 65+(fh*6))
        txt("5. Zip the project folder.", font, WHI, 60, 65+(fh*7))
        txt("6. Put zip in 'Badges' folder ", font, WHI, 60, 65+(fh*8))
        txt("on 3DS SD card.", font, WHI, 60, 65+(fh*9))
        txt("7. Boot Anenome and install!", font, WHI, 60, 65+(fh*10))
        if [ev for ev in events if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE]:
            helpmenu = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()
def mainloop_splashscreen():
    global run
    global helpmenu
    global nameset
    global Exname
    events = pygame.event.get()
    if [ev for ev in events if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN]:
        Exname = text_input_badge()
        nameset= True
    try:
         val
    except NameError:
         val = "(Press Enter)"
    if nameset == True:
        val = Exname
    txt("This is the Splash Creator! Please note that this program ", font_s, BLU2, w/3-fa, h/9)
    txt("does require an external image editor.", font_s, BLU2, w/3-fa, h/9+font_s.get_height())
    txt("Export Name: "+ val, font_s, BLU, w/3-(fa/2), h/9+font_s.get_height()*2)
    txt("Top:", font_s, BLU2, w/2-i_button.get_width()/1.5, h/2-i_button.get_height()-10)
    txt("Bottom:", font_s, BLU2, w/2-i_button.get_width()/1.4, h/2-10)
    if import_button.draw() and helpmenu == False:
        import_splash("bottom")
    if import_button_2.draw() and helpmenu == False:
        import_splash("top")
    if help_button.draw():
        helpmenu = True
    if helpmenu == True:
        h_r = pygame.Rect(50, 50, 500, 500)
        pygame.draw.rect(screen, BLU2, h_r)
        txt("Help Menu-- ESC to exit", font_s, WHI, 60, 60)
        txt("1. Enter the export name", font_s, WHI, 60, 65+fhs)
        txt("2. Import Top & Bottom Screens, MUST be ", font_s, WHI, 60, 65+(fhs*2))
        txt("400x240 and 320x240, respectively.", font_s, WHI, 60, 65+(fhs*3))
        txt("3. The two images will be exported as ", font_s, WHI, 60, 65+(fhs*4))
        txt("splash.bin and splashbottom.bin, in Output/[export]. ", font_s, WHI, 60, 65+(fhs*5))
        txt("4. Then, go to this website to create info.smdh:", font_s, WHI, 60, 65+(fhs*6))
        txt("https://www.marcrobledo.com/smdh-creator/", font_s, BLU, 60, 65+(fhs*7))
        txt("5. Put it into the folder with the .bin files,", font_s, WHI, 60, 65+(fhs*8))
        txt("and rename it to info.smdh, and zip the folder.", font_s, WHI, 60, 65+(fhs*9))
        txt("6. Put it into the 'Splashes' folder ", font_s, WHI, 60, 65+(fhs*10))
        txt("on your 3ds SD card.", font_s, WHI, 60, 65+(fhs*11))
        txt("7. Load it in Anenome.", font_s, WHI, 60, 65+(fhs*12))
        txt("And then you're all done! :)", font_s, WHI, 60, 65+(fhs*13))
        if [ev for ev in events if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE]:
            helpmenu = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()

def choose():
    global mode
    txt("Badge/Splash Maker!", font, BLU2, w/2-fa, h/5)
    if splash_button.draw():
        print("Splash Mode")
        mode = 1
        pygame.time.delay(400)
    if badge_button.draw():
        print("Badge Mode")
        mode = 2
        pygame.time.delay(200)


while run:
    screen.blit(bg, (0,0))
    if mode == 0:
        choose()
    elif mode == 1:
        mainloop_splashscreen()
    elif mode == 2:
        mainloop_badgemakr()
    else:
        raise ValueError("Error! Mode must be 0 (Menu), 1 (Splash Screen Creator), or 2 (Badge Maker). Most likely, this is not your fault and is a program error. Please contact the developer!")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            sys.exit()
            pygame.quit()
    pygame.display.update()
pygame.quit()