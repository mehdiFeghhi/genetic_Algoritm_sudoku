import unittest
import datetime
import genetic
import random
"""
 الگوریتم یاد گرفته شده در فرادارس جهت پر کردن یک سودکوی خالی
 این الگوریتم از فایل پایتون کمکی به نام ژنتیک استفاده میکنه که ساختارش توضیح داده شده
 در این الگوریتم که برباپه الگوریتم ژنتیک است ما هر کدوم از خانه های این سودکو را یک ژنوم در نظر میگیریم و هدف این است که یک جدول سودکو را بدون عیب پر کنیم
  الگوریتم برپایه انجام mutation است بر روی parent های مختلف
 والدین مختلف بعد از موندن در اینجا دوجار سال خوردگی میشن و به کمک الگوریتم simulate annuling در قسمت ژنتیک که در تابع بهبود هستش به وضعیت مطلوب تری می رسیم
"""

class SudokuTest(unittest.TestCase):

    def test(self):
        genset = [i for i in range(1, 10)] # مشخص میکنه چه اعدادی میتونن gen های باشن
        strtTime = datetime.datetime.now()
        optimalValue = 100  # هدف ما رسیدن به عدد ۱۰۰ در فیت نس فانکشن هست

        def fnDisplay(candidate):
            display(candidate, strtTime) #در به کمک این تابع بهترین کاندید ما نشان داده خواهد شدا

        validationRules = build_validation_rules() # وضعیت genum های کرومزم های ما رو مشخص میکنه

        def fnGetFitness(genes): # تابع فیتنس رو صدا میزنه
            return get_fitness(genes, validationRules)

        best = genetic.get_best(fnGetFitness, 81, optimalValue, genset, fnDisplay, maxAge=5000) # بهترین حاصل براساس fitness فانکشن به ما بر میگردونه

        self.assertEqual(best.Fitness, optimalValue) # اگر به مقدار ۱۰۰ رسیدیم تابع تست ما به خوبی عمل کرده است


'''
یک نمونه تابع فیتنس فانکش بود که در این تابع براساس اینکه چه تعداد از سطر و ستون ها و مربع های ما براساس قوانین سودکو درست کار میکنن 
یک عدد به ما میداد . 
عدد تکمیل فرایند برابر با ۲۷ بود که برابر این بود که ۹ سطر و ۹ ستون و ۹ تا مربع کلی همه درست هستند و اعداد ۱ تا ۹ را دارهستند.  
'''

# def get_fitness(candidate):
#
#     rows = [set() for _ in range(9)]
#     columns = [set() for _ in range(9)]
#     sections = [set() for _ in range(9)]
#
#     for row in range(9):
#
#         for column in range(9):
#
#             value = candidate[row * 9 + column]
#             rows[row].add(value)
#             columns[column].add(value)
#             sections[int(row/3) * 3 + int(column/3)].add(value)
#
#     fitness = sum(len(row) == 9 for row in rows) + \
#               sum(len(column) == 9 for column in columns) + \
#               sum(len(sections) == 9 for section in sections)
#
#     return fitness

'''
 در این جا تابع فیتنس فانکشن ما تکامل یافت و به شکل زیر که می بینید در آمد 

در اینجا نگاه میکنیم که اولین خونه ای در کل سودکو که قانون ما رو نقض کرده کدام یک از خانه ها است 
و عدد فیتنس فانکش برابر میشه با شماره اون خونه به جوری که بین عدد ۱۱ تا ۹۹ map میکنیم 
سطر را به اضافه یک ضرب در ۱۰ میکنیم به اضافه ستون به اضافه ۱ می نماییم .     
     اگر لیست خالی باشه یعنی هیچ کدوم از ژنوم های ما تداخل نداشته باشن 
    fitness عدد ۱۰۰ را به عنوان 
انتخاب مینماییم .      
'''

def get_fitness(genes, validationRules):
    try:
        firstFailingRule = next(rule for rule in validationRules
                                if genes[rule.Index] == genes[rule.OtherIndex])
    except StopIteration:
        fitness = 100

    else:
        fitness = (1+index_row(firstFailingRule.OtherIndex)) * 10 \
                    +(1+index_column(firstFailingRule.OtherIndex))

    return fitness

"""

    روش انجام mutate در این تابع به این شکل هست که 
    یک ژنوم انتخاب میکنیم از انجا که لیست از ژنوم ها با حال بد داریم 
    اونی که بدترین حال رو داره انتخاب میکنیم .
    و جاش رو با یک رندوم ژنوم عوض میکنیم .
    
"""


def mutate(genes, validationRules):
    selectedRule = next(rule for rule in validationRules
                            if genes[rule.Index] == genes[rule.OtherIndex])

    if selectedRule is None:
        return
    row = index_row(selectedRule.OtherIndex)
    start = row * 9

    index_A = selectedRule.OtherIndex
    index_B = random.randrange(start, len(genes))
    genes[index_A], genes[index_B] = genes[index_B], genes[index_A]



def display(candidate, startTime):
    timeDiff = datetime.datetime.now() - startTime

    for row in range(9):

        line = ' | '.join(
            ' '.join(str(i)
                     for i in candidate.Genes[row * 9 + i: row * 9 + i + 3])
            for i in [0, 3, 6])

        print("", line)

        if row < 8 and row % 3 == 2:
            print("----- + ----- + -----")

    print(" - = -  - = -   - = - {0}\t{1}\n".format(candidate.Fitness, str(timeDiff)))


class Rule:
    Index = None
    OtherIndex = None

    def __init__(self, it, other):
        if it > other:
            it, other = other, it

        self.Index = it
        self.OtherIndex = other

    def __eq__(self, other):
        return self.Index == other.Index and \
               self.OtherIndex == other.OtherIndex

    def __hash__(self):
        return self.Index * 100 + self.OtherIndex


def build_validation_rules():
    rules = []
    for index in range(80):
        itsRow = index_row(index)
        itsColumn = index_column(index)
        itsSection = row_column_section(itsRow, itsColumn)

        for index2 in range(index + 1, 81):
            otherRow = index_row(index2)
            otherColumn = index_column(index2)
            otherSection = row_column_section(otherRow, otherColumn)
            if itsRow == otherRow or \
                itsColumn == otherColumn or \
                itsSection == otherSection:

                    rules.append(Rule(index, index2))

    rules.sort(key=lambda x: x.OtherIndex * 100 + x.Index)

    return rules


def index_row(index):
    return int(index / 9)


def index_column(index):
    return index % 9


def row_column_section(row, column):
    return int(row / 3) * 3 + int(column / 3)


def index_section(index):
    return row_column_section(index_row(index), index_column(index))


def section_start(index):
    return int((index_row(index) % 9) / 3) * 27 + \
           int(index_column(index) / 3) * 3


if __name__ == '__main__':
    unittest.main()
