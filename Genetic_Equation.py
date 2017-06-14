import random
import math
import PSA, PSA_2


class GeneticEquationProblem(PSA.Problem):
    def get_random_initial_state(self):
        return random.uniform(0.2, 3.14)

    def is_goal(self, x):
        if math.sin(x) == math.pow(x, 2) - x:
            return True
        return False

    def get_state_fitness(self, x):
        return -1 * math.fabs((math.pow(x, 2) - x) - math.sin(x))

    def crossover(self, parent1, parent2):
        return (parent1 + parent2) / 2

    def mutate(self, child):
        mutated = child + random.normalvariate(0, 0.01)
        if mutated < 0.2:
            mutated = 0.2
        elif mutated > 3.14:
            mutated = 3.14
        return mutated

b = PSA_2.PSA_2(GeneticEquationProblem())
a = b.genetic_algorithm(20)
print("\nFinal Result: ", a[0], "    |    Fitness: ", a[1])
