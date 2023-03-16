import pygame


class particle_main:
    def __init__(self,position=[0,0],velocity=[0,0],radius=8,speed=10,gravity=False,color=(255,255,255)):
        self.position = position
        self.velocity = velocity
        self.acceleration = [0,0]
        self.gravity = gravity
        self.gravity_value = 0
        self.radius = radius
        self.speed = speed
        self.color = color

    def is_finished(self):
        return self.radius <= 0
    
    def apply_force(self,force=[0,0]):
        
        self.acceleration[0] = force[0]
        self.acceleration[1] = force[1]

    def update(self,delta_time=None):
        self.velocity[0] += self.acceleration[0] 
        self.velocity[1] += self.acceleration[1]

        self.position[0] += self.velocity[0] // self.speed
        self.position[1] += self.velocity[1] // self.speed

        if self.gravity:
            self.position[1] += self.gravity_value
            self.gravity_value += self.acceleration[1]
        
        self.acceleration[0] = 0
        self.acceleration[1] = 0

        self.radius -= 0.5

    def render(self,surface):
        pygame.draw.circle(surface, self.color, (self.position[0],self.position[1]), self.radius)
        
