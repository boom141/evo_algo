import pygame, sys, time, random, math, json
from particle_system import particle_main
from pygame.locals import*

pygame.init()

SCREEN_DIMENSION = (500,500)

SCREEN = pygame.display.set_mode(SCREEN_DIMENSION,0,32)
ALPHA_SURFACE = pygame.Surface(SCREEN_DIMENSION)
FPS = pygame.time.Clock()
pygame.display.set_caption("Evolution Algorithm")



class DNA:
    def __init__(self):
        """
        class DNA contains method for processing genes realted data

        """

        self.genes = []
        self.length = 100
        self.mutation_rate = 0.01

    def generate_genes(self):
        """
        method to generate random genes

        """

        for _ in range(self.length):
            self.genes.append([random.uniform(-2,2),random.uniform(-2,2)])

        return self.genes

    def crossover(self,parent_A,parent_B):
        """
        method for processing the genes form previous generation

        :param: list
        :param: list

        :return: list

        """

        new_genes = []
        break_point = random.randint(1,100)
        for i in range(self.length):
            if i > break_point:
                new_genes.append(parent_A[i])
            else:
                new_genes.append(parent_B[i])
        
        return self.mutation(new_genes)
    
    def mutation(self,genes):
        """
        method that mutates the new generated genes

        :param: list

        :return: list

        """

        for i in range(self.length):
            if random.uniform(0,1) < self.mutation_rate:
                genes[i] = [random.uniform(-2,2),random.uniform(-2,2)]

        return genes


class evolution:
    def __init__(self):
        """
        class evolution contains method for processing the cycle of genrations

        """

        self.population = []
        self.matingpool = []
        self.length = 30

    def selection(self):
        """
        method to select the suitable and best parent genetics 
        for the next generation
        
        """

        new_population = []
        for _ in range(self.length):
            parent_A = random.choice(self.matingpool).dna
            parent_B = random.choice(self.matingpool).dna

            current_genes = DNA().crossover(parent_A,parent_B)
            new_population.append(test_subject(current_genes))
        
        self.population = new_population

    def evaluate_fitness(self):
        """
        method to evaluate the fitness of each test subject
        and populate the mating pool in accordance to the fitness cap
        
        """

        fitness_cap = None
        filter_subject = []
        if self.population:
            for subject in self.population:
                if subject.fitness != None:
                    if subject.fitness < 500:
                        fitness_cap = subject.fitness
                        filter_subject.append(subject)
                        
            self.matingpool = []
            for subject in filter_subject:
                multiplier = 0
                if subject.fitness == fitness_cap:
                    multiplier = 10
                else:
                    multiplier = 1
                for _ in range(multiplier):
                    self.matingpool.append(subject)

            if self.matingpool:
                self.selection()
            else:
                self.population = []

    def generate_population(self):
        """
        methos to generate random population 
        if there is no population existing yet

        """

        if not self.population:
            for _ in range(self.length):
                self.population.append(test_subject())

    def run_population(self,target):
        """
        method to iterate each test subject and run 

        """
        for test in self.population:
            test.update()
            test.calculate_fitness(target)
            test.render(SCREEN)


class test_subject:
    def __init__(self,dna=None):

        """
        class test subjects that takes dna list

        :param: list

        """

        self.rocket_img = pygame.image.load('./rocket_ast1.png').convert()
        self.rocket_rect = None
        self.position = [250,450]
        self.velocity = [0,0]
        self.acceleration = [0,0]
        self.angle = 0

        if dna != None:
            self.dna = dna
        else:
            self.dna = DNA().generate_genes()
        
        self.dna_counter = 0
        self.fitness = None
        self.alive = True
        self.target_reached = False
        self.particles = []

    def check_status(self):
        """
        method to handle test subjects that touched the edges
        
        """

        if self.position[0] >= 468 or self.position[0] <= 0:
            self.alive = False        
        if self.position[1] >= 460 or self.position[1] <= 0:
            self.alive = False 
    
    def render_particles(self,length=10):
        for _ in range(length):
            self.particles.append(particle_main(position=[self.rocket_rect.midbottom[0] ,self.rocket_rect.midbottom[1] - 5],velocity=[random.uniform(-2,2) * 0.5,random.uniform(-3,3)],
            speed=2,radius=5,gravity=True,color=random.choice(['red','orange','yellow'])))

        for particle in self.particles:
            particle.apply_force(force=[0,0.3])
            particle.update()
            particle.render(ALPHA_SURFACE)

            if particle.is_finished():
                self.particles.remove(particle)

    def calculate_fitness(self, target):
        """
        calculates the fitness of the test subjects

        :param: rect object
        
        """
        if self.rocket_rect != None:
            if target.colliderect(self.rocket_rect):
                self.target_reached = True

        distance = math.hypot(self.position[0] - target.centerx ,self.position[1] - target.centery) 
        self.angle = math.degrees(math.atan2(self.position[0] - target.centerx ,self.position[1] - target.centery))

        
        if self.alive:
            self.fitness = distance // 10
        else:
            self.fitness = None

    def apply_force(self,force):
        """
        to make the test subjects move
        """

        self.acceleration[0] = force[0]
        self.acceleration[1] = force[1]

    def update(self, delta_time=None):
        """
        updates the current movements of the test subjects

        """
        self.check_status()

        if self.target_reached != True:
            if self.alive != False:
                self.apply_force(self.dna[self.dna_counter])

                self.velocity[0] += self.acceleration[0] 
                self.velocity[1] += self.acceleration[1]

                self.position[0] += self.velocity[0] // 10
                self.position[1] += self.velocity[1] // 10

                # self.acceleration[0] = 0
                # self.acceleration[1] = 0

 
        if self.dna_counter < len(self.dna)-1:
            self.dna_counter += 1
        else:
            self.dna_counter = 0

    def render(self, surface):
        """
        renders the test subject onto the screen

        """
        
        #self.rocket_rotate = pygame.transform.rotate(self.rocket_img, self.angle)
        self.rocket_img.set_colorkey((0,0,0))

        self.rocket_rect = surface.blit(self.rocket_img, (self.position[0],self.position[1]))
        if self.target_reached != True:
            if self.alive != False:
                self.render_particles(length=5)

def draw_text(surface,position=(0,0),font=None,font_size=15,font_color=(255,255,255),text='hello world!'):
    font = pygame.font.Font(font,font_size)
    message = font.render(text,False,font_color)
    surface.blit(message,position)

def main():
    """
    main game loop
    
    generation_life_span- keeps tracks of the life span of each generation
    target- target destination of test subjects
    evolution_manager- instance of class evolution 
    
    """
    last_time = time.time()
    
    generation_life_span = 0
    generation = 0

    evolution_manager = evolution()

    moon_img = pygame.image.load('./moon_ast2.png').convert()
    moon_img = pygame.transform.scale(moon_img,(40,40))
    moon_rect = moon_img.get_rect(center=(255,50))

    while 1:
        delta_time = time.time() - last_time
        delta_time *= 60
        last_time = time.time()


        SCREEN.fill((0,0,0))
        ALPHA_SURFACE.fill((0,0,0))
        ALPHA_SURFACE.set_colorkey((0,0,0))

        SCREEN.blit(moon_img,moon_rect)

        if generation_life_span == 0:
            generation += 1
            evolution_manager.evaluate_fitness()
            evolution_manager.generate_population()
        
        generation_life_span += 1
        if generation_life_span >= 450:
            generation_life_span = 0

        evolution_manager.run_population(moon_rect)
        SCREEN.blit(ALPHA_SURFACE,(0,0),special_flags=BLEND_RGBA_ADD)
        draw_text(SCREEN,position=(35,250),font='./Minecraft.ttf',font_size=30,text=f'CURRENT GENERATION: {generation}')
        draw_text(SCREEN,position=(5,10),font='./Minecraft.ttf',font_size=15,font_color=(0,255,0),text=f"FPS: {'{:.2f}'.format(FPS.get_fps())}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        FPS.tick(60)
        pygame.display.update()


if __name__ == '__main__':
    main()