import random
import statistics
import sys
import time
from bisect import bisect_left
from math import exp

"""
این ماژول توانای این که یک کراس اور هم داشته باشه رو داره منتها هنوز به مرحله ای از کورس نرسیده بودم که 
به ماژول ما یک کراس اور اضافه میشود . 
"""

class Chromosome:
    Genes = None
    Fitness = None
    Age = 0

    def __init__(self, genes, fitness):
        self.Fitness = fitness
        self.Genes = genes
"""
به کمک این تابع یک کرموزم جدید میسازیم .

"""
def _geerate_parent(length, geneSet, get_fitness):
    genes = []

    while len(genes) < length:
        sampleSize = min(length - len(genes), len(geneSet))
        genes.extend(random.sample(geneSet, sampleSize))
    fitness = get_fitness(genes)
    return Chromosome(genes, fitness)

"""
 براساس این تابع دوخونه از ژن رو با هم عوض میکنه .
 و براساس فیتنس جدید یک کرومزم جدید رو ایجاد میکنه .
"""
def _mutate(parent, geneSet, get_fitness):

    childGenes = parent.Genes[:]
    index = random.randrange(0, len(parent.Genes))
    newGenes, alternate = random.sample(geneSet, 2)
    childGenes[index] = alternate if newGenes == childGenes[index] else newGenes
    fitness = get_fitness(childGenes)
    return Chromosome(childGenes, fitness)


def _mutate_custom(parent, custom_mutate, get_fitness):
    childGenes = parent.Genes[:]
    custom_mutate(childGenes)
    fitness = get_fitness(childGenes)
    return Chromosome(childGenes, fitness)


"""
به کمک این تابع یهترین کرموزم که بهترین فیتنس فانکشن دارد رو پیدا میکنیم. 
و مداوم به بهبود بخشیدنش اقدام میکنیم . 

"""
def get_best(get_fitness, targetLen, optimalFitness, geneSet, display,
             custom_mutate=None, custom_create=None, maxAge=None):
    if custom_mutate is None:

        def fnMutate(parent):
            return _mutate(parent, geneSet, get_fitness)
    else:
        def fnMutate(parent):
            return _mutate_custom(parent, custom_mutate, get_fitness)

    if custom_create is None:
        def fnGenerateParent():
            return _geerate_parent(targetLen, geneSet, get_fitness)
    else:
        def fnGenerateParent():
            genes = custom_create()
            return Chromosome(genes, get_fitness(genes))

    for improvement in _get_improvement(fnMutate, fnGenerateParent, maxAge):

        display(improvement)
        if not optimalFitness > improvement.Fitness:
            return improvement


"""
 این تابع تا زمانی که برنامه ما درحال اجرا هست به دنبال کرومزوم فیتنس فانکش بهتر میگرده 
   در این تابع از simulate annuling نیز در زمانی که سالجوردگی داشته باشیم به عنوان یکی از پارمترهای ورودی 
   استفاده میکنیم که کمک شایانی به حل پازل ما میکنه .
   
    
"""

def _get_improvement(new_child, generate_parent, maxAge):
    parent = bestParent = generate_parent()
    yield bestParent
    historicalFitnesses = [bestParent.Fitness]
    while True:
        child = new_child(parent)
        if parent.Fitness > child.Fitness:
            if maxAge is None:
                continue
            parent.Age += 1
            if maxAge > parent.Age:
                continue

            index = bisect_left(historicalFitnesses, child.Fitness, 0, len(historicalFitnesses))
            proportionSimilar = index / len(historicalFitnesses)
            if random.random() < exp(-proportionSimilar):
                parent = child
                continue
            parent = bestParent
            parent.Age = 0
            continue

        if not child.Fitness > parent.Fitness:
            child.Age = parent.Age + 1
            parent = child
            continue
        parent = child
        parent.Age = 0
        if child.Fitness > bestParent.Fitness:
            yield child
            bestParent = child
            historicalFitnesses.append(child.Fitness)


class Benchmark:

    @staticmethod
    def run(function):

        timings = []
        stdout = sys.stdout

        for i in range(100):

            sys.stdout = None
            startTime = time.time()
            function()
            seconds = time.time() - startTime
            sys.stdout = stdout
            timings.append(seconds)
            mean = statistics.mean(timings)
            if i < 10 or i % 10 == 9:
                print("{} {:3.2f} {:3.2f}".format(
                    1 + i, mean,
                    statistics.stdev(timings, mean) if i > 1 else 0))
