import pygame, random, time

pygame.init()

dt = 0
prevTime = time.time()

fps = 300
clock = pygame.time.Clock()

screen_width = 700
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))

class Player:
    def __init__(self):
        self.width = 65
        self.height = 50
        self.x = (screen_width / 2) - (self.width / 2) 
        self.y = (screen_height / 2) - self.height

        self.velocity = 0
        self.birdRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.birdImg = pygame.image.load('images/bird.png')
        self.birdImg = pygame.transform.scale(self.birdImg, (self.width, self.height))

        self.moving = True
        self.score = 0

    def move(self):
        keys = pygame.key.get_pressed()

        #gravity 
        gravity = -9.81 *250
        self.velocity += gravity * dt   
        self.y -= self.velocity * dt

        #jump
        if keys[pygame.K_SPACE] and self.moving: 
            self.velocity = 500 

    def collision(self):
        keys = pygame.key.get_pressed()

        if self.birdRect.colliderect(ground.groundRect): #collision with ground
            self.velocity = 0
            self.y = ground.groundRect.top - self.height

        if (self.birdRect.colliderect(pipe1.upperPipe) 
        or self.birdRect.colliderect(pipe1.lowerPipe) 
        or self.birdRect.colliderect(pipe2.upperPipe) 
        or self.birdRect.colliderect(pipe2.lowerPipe) 
        or self.birdRect.colliderect(pipe3.upperPipe) 
        or self.birdRect.colliderect(pipe3.lowerPipe)):
            self.moving = False

            if keys[pygame.K_SPACE]:
                pipe1.resetPipe()
                pipe2.resetPipe()
                pipe3.resetPipe()

                self.moving = True
                self.score = 0
        else:
            self.score +=1
    def draw(self):
        self.birdRect = pygame.Rect(self.x, self.y, self.width, self.height)
        screen.blit(self.birdImg, (self.x, self.y)) 
 
class Pipe:
    def __init__(self, offset):
        self.width = 100
        self.height = 700

        self.gapSpace = 200
        self.speed = 250
        self.range = 250

        self.offset = offset

        self.x = screen_width + self.offset
        self.y = (screen_height /2) + random.randint(-self.range, self.range)

        self.upperPipe = pygame.Rect(self.x, self.y - self.height - self.gapSpace, self.width, self.height)
        self.lowerPipe = pygame.Rect(self.x, self.y + self.gapSpace, self.width, self.height)

        self.pipeImgUpper = pygame.image.load('images/pipe.png')
        self.pipeImgUpper = pygame.transform.scale(self.pipeImgUpper, (self.width, self.height))
        self.pipeImgUpper = pygame.transform.rotate(self.pipeImgUpper, 180)

        self.pipeImgLower = pygame.image.load('images/pipe.png')
        self.pipeImgLower = pygame.transform.scale(self.pipeImgLower, (self.width, self.height))

    def move(self):
        if bird.moving :
            self.x -= self.speed * dt

            if self.x < 0 - self.width:
                self.x = screen_width + 250
                self.y = (screen_height / 2) + random.randint(-self.range, self.range) #respawn pipe with a different y


    def draw(self):
        self.upperPipe = pygame.Rect(self.x, self.y - self.height - self.gapSpace, self.width, self.height)
        self.lowerPipe = pygame.Rect(self.x, self.y + self.gapSpace, self.width, self.height)

        screen.blit(self.pipeImgUpper, (self.x, self.y - self.height - self.gapSpace))
        screen.blit(self.pipeImgLower, (self.x, self.y + self.gapSpace))

    def resetPipe(self):
        self.x = screen_width + self.offset
        self.y = (screen_height /2) + random.randint(-self.range, self.range)
 
class Ground:
    def __init__(self):
        self.width = screen_width * 2
        self.height = 200

        self.x = 0
        self.y = screen_height - self.height + 50

        self.groundRect = pygame.Rect(self.x, self.y, self.width, self.height)

        groundImg = pygame.image.load('images/base.png') 
        self.groudnImg = pygame.transform.scale(groundImg, (self.width / 2, self.height))

    def move(self):
        if bird.moving:

            self.x -= 250 * dt

            if self.x < 0 - (self.width /2):
                self.x = 0

    def draw(self):
        self.groundRect = pygame.Rect(self.x, self.y, self.width, self.height)
        screen.blit(self.groudnImg, (self.x, self.y))
        screen.blit(self.groudnImg, (self.x + (self.width / 2), self.y))
        
bird = Player()
ground = Ground()

pipe1 = Pipe(0)
pipe2 = Pipe(350)
pipe3 = Pipe(700)

bg = pygame.image.load('images/bg.jpg')
bg = pygame.transform.scale(bg, (screen_width, screen_height))
font = pygame.font.SysFont(None, 100)

def draw():
    #draws all objects in scene
    screen.blit(bg, (0,0)) 

    pipe1.draw()
    pipe1.move()
    pipe2.draw()
    pipe2.move()
    pipe3.draw()
    pipe3.move()

    ground.move()
    ground.draw()
    
    bird.draw()
    bird.move()
    bird.collision()

    scoreText = font.render(str(bird.score), True, (0,0,0))
    screen.blit(scoreText, (screen_width / 2, screen_height / 2 - 400))

running = True
while running:
    now = time.time()
    dt = now - prevTime
    prevTime = now
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw()

    pygame.display.update()
    clock.tick(fps)


