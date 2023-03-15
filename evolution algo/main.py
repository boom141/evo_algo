import pygame, sys, time, random, math, json
from pygame.locals import*

pygame.init()

SCREEN_DIMENSION = (500,500)

SCREEN = pygame.display.set_mode(SCREEN_DIMENSION,0,32)
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


            print(len(self.population))
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

        self.subject = None
        self.position = [250,485]
        self.velocity = [0,0]
        self.acceleration = [0,0]
        if dna != None:
            self.dna = dna
        else:
            self.dna = DNA().generate_genes()
        
        self.dna_counter = 0
        self.fitness = None
        self.alive = True
        self.target_reached = False

    def check_status(self):
        """
        method to handle test subjects that touched the edges
        
        """

        if self.position[0] >= 500 or self.position[0] <= 0:
            self.alive = False        
        if self.position[1] >= 500 or self.position[1] <= 0:
            self.alive = False 
    
    def calculate_fitness(self, target):
        """
        calculates the fitness of the test subjects

        :param: rect object
        
        """
        if self.subject != None:
            if target.colliderect(self.subject):
                self.target_reached = True

        distance = math.hypot(target.centerx - self.position[0], target.centery - self.position[1]) 
        
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

                self.acceleration[0] = 0
                self.acceleration[1] = 0

        if self.dna_counter < len(self.dna)-1:
            self.dna_counter += 1
        else:
            self.dna_counter = 0

    def render(self, surface):
        """
        renders the test subject onto the screen

        """
        self.subject = pygame.draw.circle(surface, 'blue', (self.position[0],self.position[1]),10)


def main():
    """
    main game loop
    
    generation_life_span- keeps tracks of the life span of each generation
    target- target destination of test subjects
    evolution_manager- instance of class evolution 
    
    """
    last_time = time.time()
    
    generation_life_span = 0
    target = pygame.Rect(225, 10, 50,50)

    evolution_manager = evolution()
    while 1:
        delta_time = time.time() - last_time
        delta_time *= 60
        last_time = time.time()

        SCREEN.fill((0,0,0))

        pygame.draw.rect(SCREEN, 'green', target, 1,100)

        if generation_life_span == 0:
            evolution_manager.evaluate_fitness()
            evolution_manager.generate_population()
        
        generation_life_span += 1
        if generation_life_span >= 400:
            generation_life_span = 0

        evolution_manager.run_population(target)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        FPS.tick(60)
        pygame.display.update()


if __name__ == '__main__':
    main()