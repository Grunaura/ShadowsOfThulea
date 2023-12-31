from math import sin,cos,sqrt,atan2,pi
import pygame
pygame.init()

class Planet:
    dt = 1/100
    G = 6.67428e-11 #G constant
    scale = 1/(1409466.667) #1 m = 1/1409466.667 pixlar
    def __init__(self,x=0,y=0,radius=0,color=(0,0,0),mass=0,vx=0,vy=0):
        self.x = x #x-coordinate pygame-window
        self.y = y #y-coordinate pygame-window
        self.radius = radius
        self.color = color
        self.mass = mass
        self.vx = vx #velocity in the x axis
        self.vy = vy #velocity in the y axis
        
    def draw(self,screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
    
    def orbit(self,trace):
        pygame.draw.rect(trace, self.color, (self.x, self.y, 2, 2))
        
    def update_vel(self,Fnx,Fny):
        ax = Fnx/self.mass #Calculates acceleration in x- and y-axis for body 1.
        ay = Fny/self.mass
        self.vx -= ((ax * Planet.dt)/Planet.scale)
        self.vy -= ((ay * Planet.dt)/Planet.scale)
        self.update_pos()
     
    def update_pos(self):
        self.x += ((self.vx * Planet.dt)) #changes position considering each body's velocity.
        self.y += ((self.vy * Planet.dt))
        
    def move(self,body):
        dx = (self.x - body.x) #Calculates difference in x- and y-axis between the bodies
        dy = (self.y - body.y)
        r = (sqrt((dy**2)+(dx**2))) #Calculates the distance between the bodies
        angle = atan2(dy, dx) #Calculates the angle between the bodies with atan2!
        if r < self.radius: #Checks if the distance between the bodies is less than the radius of the bodies. Uses then Gauss gravitational law to calculate force.
            F = 4/3 * pi * r
            Fx = cos(angle) * F
            Fy = sin(angle) * F
        else:  
            F = (Planet.G*self.mass*body.mass)/((r/Planet.scale)**2) #Newtons gravitational formula.
            Fx = cos(angle) * F
            Fy = sin(angle) * F
        return Fx,Fy

def motion():
    for i in range(0,len(bodies)):
        Fnx = 0 #net force
        Fny = 0
        for j in range(0,len(bodies)):
            if bodies[i] != bodies[j]:
                Fnx += (bodies[i].move(bodies[j]))[0]
                Fny += (bodies[i].move(bodies[j]))[1]
            elif bodies[i] == bodies[j]:
                continue
        bodies[i].update_vel(Fnx,Fny)
        bodies[i].draw(screen)
        bodies[i].orbit(trace)
        Fnx,Fny=0,0 

screen = pygame.display.set_mode([900,650]) #width - height
trace = pygame.Surface((900, 650))
pygame.display.set_caption("Moon simulation")
FPS = 60 #how quickly/frames per second our game should update. Change?

earth = Planet(450,325,30,(0,0,255),5.97219*10**(24),-24.947719394204714/2) #450= xpos,325=ypos,30=radius
luna = Planet(450,(575/11),10,(128,128,128),7.349*10**(22),1023)
moon = Planet() #the second moon
bodies = [earth,luna]

running = True
clock = pygame.time.Clock()

while running: #if user clicks close window
    clock.tick(FPS)    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill((0,0,0))
    pygame.Surface.blit(screen, trace, (0, 0))
    motion()

    pygame.display.flip() #update? flip? 

pygame.quit()