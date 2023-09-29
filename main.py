
import pygame
import random
import math
pygame.init()               #pygame initization  it start pygame

class DrawInformation:
	BLACK = 0, 0, 0
	WHITE = 255, 255, 255
	GREEN = 0, 255, 0
	RED = 255, 0, 0
	BACKGROUND_COLOR = WHITE

	GRADIENTS = [                      # shades of grey giving to our bar
		(128, 128, 128),
		(160, 160, 160),
		(192, 192, 192)
	]

	FONT = pygame.font.SysFont('comicsans', 30)
	LARGE_FONT = pygame.font.SysFont('comicsans', 40)

	SIDE_PAD = 100             # 100px padding 
	TOP_PAD = 150

	def __init__(self, width, height, lst):
		self.width = width
		self.height = height

		self.window = pygame.display.set_mode((width, height),pygame.RESIZABLE)
		pygame.display.set_caption("Sorting Algorithm Visualization")
		self.set_list(lst)

	def set_list(self, lst):
		self.lst = lst
		self.min_val = min(lst)
		self.max_val = max(lst)

		self.block_width = round((self.width - self.SIDE_PAD) / len(lst))                         ## area available divied by number of item in list so that every block get equal width .        NOte: that both block height and width give value for per value of height and width. . if value 2 then it mul with 2*block_width 
		self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))         # area available divied by how much range of number is there eg. 1 to 100  then we have 99 num.
		self.start_x = self.SIDE_PAD // 2          # itstart from x axis , we divide by 2 becz we want 50 side pading from x axis 

def draw(draw_info):
	draw_info.window.fill(draw_info.BACKGROUND_COLOR )
	##title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.RED)   #1 is  sharpeness value
	#draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))   #blit put on screen   in pygmae every thig is in different layer []

	controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
	draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 45))

	sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort", 1, draw_info.BLACK)
	draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 75))

	draw_list(draw_info)
	pygame.display.update()
                                                       
def draw_list(draw_info,color_positions={},clear_bg=False):
	if clear_bg:
		clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
						draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)         # rect to erase
		pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)
#                             on             colorbackgroung to erase      at         
	lst=draw_info.lst
	for i, val in enumerate(lst):            # enumarate give value of index(i), value  from our list for eg. 1st item --> index 0  & 1 st item value.
		x=draw_info.start_x+ i* draw_info.block_width         #  here  we are drawing on x co-ordant   eg.(from line 41 we get starting point + position of block in list for (eg. 1st element postion i=0 i.e start from staring position, 2nd position mean i=1) 
		y=draw_info.height- ( val - draw_info.min_val ) * draw_info.block_height
		#      total height   -   val- minimum value basically 1 or 0 that give real height * block_height (i.e per value of height)
		      
		color=draw_info.GRADIENTS[i % 3 ] # 0 1 2  go throught all three value of grays we declare so that every list color is different.
		
		if i in color_positions:
			color=color_positions[i]
		pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))
    
	if clear_bg:
	    pygame.display.update()           

def generate_starting_list(n, min_val, max_val):             # n=no. of element in staring list   , min_val is minimum possible value
	lst = []

	for _ in range(n):
		val = random.randint(min_val, max_val)   # give random  number between (including) min and max value.
		lst.append(val)     
    
	return lst

def bubble_sort(draw_info,ascending=True):
	lst=draw_info.lst

	for i in range(len(lst)-1):
		for j in range(len(lst)-1-i):
			num1=lst[j]
			num2=lst[j+1]

			if(num1>num2 and ascending) or(num1<num2 and not ascending):
				lst[j],lst[j+1]= lst[j+1], lst[j]
				draw_list(draw_info,{j:draw_info.GREEN,j+1:draw_info.RED})
				yield True

def main():
	run = True
	clock = pygame.time.Clock()              #regulate how quickly it will run

	n=50
	min_val=0
	max_val=100

	lst=generate_starting_list(n,min_val,max_val)
	draw_info= DrawInformation(800,600,lst)
	sorting= False
	ascending=True
	sorting_algorithm=bubble_sort
	sorting_algo_name="Bubble Sorthong"
	sorting_algorithm_generater=None

	while run:
		clock.tick(60)             # 60 FPS      max no. of time this loop run
		draw(draw_info)
		            # it will update the display
 		
		for event in pygame.event.get():            #pygame.event.get() : give list of all event have occur since last loop in our event.
			if event.type==pygame.QUIT:             # this condection occur when it hit the red X button .
				run=False
			if event.type!=pygame.KEYDOWN:          #until we not press anything it will continue to next event
				continue
            
			if event.key == pygame.K_r: 
				lst=generate_starting_list(n,min_val,max_val)     #   again generaate new list values
				draw_info.set_list(lst)           #give new values to set_list function
				sorting=False 
			elif event.key== pygame.K_SPACE and sorting==False:
				sorting= True
			    sorting_algorithm_generater=sorting_algorithm(draw_info,ascending)

				
			elif event.key == pygame.K_a and not sorting:      # and not sorting  is use becz  make sure we cannot do this while sorting.
				ascending = True
			elif event.key == pygame.K_d and not sorting:
				ascending = False
	pygame.quit ()

	

if __name__=="__main__":                  # it make sure that this is actuall runing this modual  / when we are importing this code it will run above code before implementing main function
	main()
