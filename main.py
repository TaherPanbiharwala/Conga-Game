import pygame 
from pygame.locals import * #lets you import some global variables ex KEYDOWN 
import random
import time


SIZE = 40 #size of block
BACKGROUND_COLOR = (160, 219, 121)
class Apple:
    def __init__(self , parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple.jpg").convert() 
        self.x=120
        self.y=120

    def draw(self):
        self.parent_screen.blit(self.image,(self.x,self.y)) #draws your character on your surface
        pygame.display.flip() #updates the window
    
    def move(self):
        self.x = random.randint(1,23)*SIZE
        self.y = random.randint(1,18)*SIZE

class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.sprite_sheet = pygame.image.load("resources/character_sheet.png").convert_alpha()
        self.direction = 'down'

        # Size of each sprite in the sprite sheet
        self.sprite_size = 40  # Assuming each sprite is 40x40 pixels
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.length = 1

        # Dictionary mapping directions to their respective sprite positions in the sprite sheet
        self.sprite_positions = {
            'down': (0, 0),  # Coordinates for the 'down' sprite
            'up': (1, 0),  # Adjust these values based on your sprite sheet's layout
            'left': (2, 0),
            'right': (3, 0)
        }
    
    def get_sprite(self, direction):
        # Get the position of the sprite for the current direction
        position = self.sprite_positions[direction]
        # Calculate the area of the sprite sheet to extract
        x = position[0] * self.sprite_size
        y = position[1] * self.sprite_size
        return self.sprite_sheet.subsurface(pygame.Rect(x, y, self.sprite_size, self.sprite_size))

    
    def move_left(self):
        self.direction = 'left'
    
    def move_right(self):
        self.direction = 'right'
    
    def move_up(self):
        self.direction = 'up'
    
    def move_down(self):
        self.direction = 'down'
    
    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE 
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        
        self.draw()

    def draw(self):
        self.parent_screen.fill(BACKGROUND_COLOR)
        for i in range(self.length):
            # Use the get_sprite method to get the correct sprite based on the current direction
            sprite = self.get_sprite(self.direction)
            self.parent_screen.blit(sprite, (self.x[i], self.y[i]))  # Draws the sprite
        pygame.display.flip()  # Updates the window
    

    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)



class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Conga Game")
        self.surface=pygame.display.set_mode((1000,800)) # initializing size of the window
        self.snake = Snake(self.surface,1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def reset(self):
        self.snake = Snake(self.surface,1)
        self.apple = Apple(self.surface)

    
    def is_collision(self ,x1,y1,x2,y2):
        if x1 >= x2 and x1< x2 + SIZE:
            if  y1>= y2 and y1< y2 + SIZE:
                return True
        return False
    
    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Followers: {self.snake.length-1}",True,(0,0,0))
        self.surface.blit(score , (450,750))
    
    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            self.snake.increase_length()
            self.apple.move()
        
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise Exception("Collision Occured")

            
    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your followers are {self.snake.length}", True, (0, 0, 0))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (0, 0, 0))
        self.surface.blit(line2, (200, 350))

        pygame.display.flip()



    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    
                    if event.key == K_RETURN:
                        pause = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        if event.key == K_LEFT:
                            self.snake.move_left()


                elif event.type == QUIT:
                    running = False
                
            try:
                if not pause:
                    self.play()
    
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            
            time.sleep(0.25)


if __name__=="__main__":
    game=Game()
    game.run()




    

