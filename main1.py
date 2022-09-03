
import random

import copy

"""
این نخستین ورژن از کد من برای حل این مسئله بود 
بدون استفاده از هیچ گونه از کورسی نمونه اولیه که ۲ هفته پیش تکمیل شد.
در این ورژن از کد ابتدا ۰۰ا سودکو به وجود میاریم 
در مرحله بعد این 85 درصد از  سودکو را باهم دیگر 
کراس اور مینماییم .

در مرحله بعد ۱۵ درصد از اعضای جدید را mutate میکنیم و سعی میکنیم که بهتر از حالت قبل بشن 

از لیست بدست آماده اگر بیشتر از نصف آیتم ها مشابه بهترین آیتم باشن این تعداد را کاهش داده و دوباره لیست جدیدی از اعضا را بوجود میاوریم به اضافه 
لیست قبلی از اعضا بدون اون سری از آیتم .

این روند رو اینقدر ادامه میدهیم تا به فیتنس ۱ برسیم 

طبق بررسی های انجام شده این تابع بعد از چند دقیقه به پیشرفت ۶۴ درصدی میرسه 

ولی تا الان نتونستم به کمک این سری کل جدول را بسازم .
مطابق خواست سوال توانایی این را دارد که از کاربر یک سری 
اعضا رو بگیره و بعنوان که همیشه جاشون ثابت باشه و به کمک اون مسئله رو حل کنه .
  

"""


class Sudokou:

    def __init__(self, list_item_define, list_number_I_see):

        self.Sudokou_surface = [[[[0, True], [0, True], [0, True]] for i in range(3)] for j in range(9)]
        self.other_see_surface = [[[0, True] for i in range(9)] for j in range(9)]
        for item in list_item_define:
            self.Sudokou_surface[item[0] - 1][item[1][0] - 1][item[1][1] - 1] = [item[2], False]

        self.convert_surface_main_to_other()
        self.how_much_each_number_rapid = list_number_I_see
        self.fitness = 0

    '''
    به کمک این تابع یک سودکو را به صورت شانسی پر میکنه سعی در این داره که اعداد موجود در سودکو به گونه ای باشه که از تمامی اعداد
    ۱ تا ۹ را ۹ بار داشته باشد .
    '''

    def find_random_sitution(self):
        list_helper = [i for i in range(1, 10)] * 9
        helper = copy.deepcopy(self)
        # for i in helper.Sudokou_surface:
        #
        #     for j in i:
        #
        #         for k in j:
        #
        #             if k[1]:
        #
        #                 random_number = random.randrange(0, len(list_helper))
        #                 number = list_helper[random_number]
        #                 list_helper = list_helper[:random_number] + list_helper[random_number + 1:]
        #                 if helper.how_much_each_number_rapid[number - 1] < 9:
        #                     helper.how_much_each_number_rapid[number - 1] += 1
        #                     k[0] = number
        # for i in self.Sudokou_surface:
        #     print(i)
        for i in range(9):

            list_number_can_use = [i for i in range(1, 10)]
            for j in range(9):

                if helper.other_see_surface[i][j][1]:

                    random_number = random.randrange(0, len(list_number_can_use))

                    helper.other_see_surface[i][j][0] = list_number_can_use[random_number]

                    list_number_can_use = list_number_can_use[:random_number] + list_number_can_use[random_number + 1:]


                else:

                    list_number_can_use = list_number_can_use[
                                          :helper.other_see_surface[i][j][0] - 1] + list_number_can_use[
                                                                                    helper.other_see_surface[i][j][
                                                                                        0] - 1 + 1:]

        helper.convert_other_to_surface_main()

        # print(helper)
        # # helper.convert_surface_main_to_other()
        # for i in helper.Sudokou_surface:
        #     for j in i:
        #         print(j)
        #     print("______________________")
        # input()
        helper.find_Fitness()

        return helper

    '''
    به کمک این تابع میتونیم مقدار فیتنس بین ۱ تا صفر به یک سودکو اختصاص بدیم 
    روش این کار این گونه است که تعداد آیتم های تکرار هاس سطر و ستون و تعداد تکراری های هر
    مربع را میشماریم .                                              
    یک مقدار آماری از هر کدوم بدست میاریم و درنهایت fitness را از حاصل ضرب 
    مقدار آماری اشتباهات سطر و مربع ها را بدست میاریم و در هم دیگر ضرب میکنیم .
    
    '''

    def find_Fitness(self):

        row_wrong = 0

        for i in range(9):
            list_see_one = [0 for i in range(9)]
            for j in range(9):
                # if list_see_one[k[0] - 1] == 1:
                #
                #     Wrong += 1
                # else:

                list_see_one[self.other_see_surface[i][j][0] - 1] += 1

            row_wrong += (1.0 / len(set(list_see_one))) / 9

        column_wrong = 0
        # Wrong = 0
        for i in range(9):
            list_see_one = [0 for i in range(9)]
            for j in range(9):
                # if list_see_one[self.other_see_surface[i][j][0] - 1] == 1:
                #
                #     Wrong += 1
                # else:
                list_see_one[self.other_see_surface[j][i][0] - 1] += 1

            column_wrong += (1.0 / len(set(list_see_one))) / 9

        # wrongy1 = Wrong / 81

        # Wrong = 0
        wrong_in_block = 0
        for squre in self.Sudokou_surface:
            list_see_one = [0 for i in range(9)]

            for i in range(3):
                for j in range(3):
                    list_see_one[squre[i][j][0] - 1] += 1

            wrong_in_block += (1.0 / len(set(list_see_one))) / 9

        if int(row_wrong) == 1 and int(column_wrong) == 1 and int(wrong_in_block) == 1:
            self.fitness = 1.0

        else:

            self.fitness = column_wrong * wrong_in_block

    """
    ما به چند شکل میتونیم یک سودکو را ببینیم 
    مجموعه ای از مربع ها 
    یک ماترینس دو در دو به عرض و سطر ۹ 
    برای اینکه در هر قسمت از یکی از این شکل ها استفاده میکنیم و 
    در مراحل مختلف ممکن هست که آپدیتی در یکی بوجود بیاوریم 
    باید آپدیت مقدار مذکور را در شکل دیداری ما از تابع را ببینیم .
    
    دو تابع پایین اینکار را برای ما انجام میدهند .
    یکی را به دیگری تبدیل میکنیم .
    و دیگر را به کمک تابع پایینی به اون یکی  
    
    
    """


    def convert_other_to_surface_main(self):

        for i in range(11):

            for j in range(3):

                for k in range(3):
                    if i == 0:
                        self.Sudokou_surface[i][j][k] = self.other_see_surface[j][k].copy()

                    elif i == 1:
                        self.Sudokou_surface[i][j][k] = self.other_see_surface[j][3 + k].copy()

                    elif i == 2:
                        self.Sudokou_surface[i][j][k] = self.other_see_surface[j][6 + k].copy()

                    elif i == 3:
                        self.Sudokou_surface[i][j][k] = self.other_see_surface[3 + j][k].copy()

                    elif i == 4:
                         self.Sudokou_surface[i][j][k] = self.other_see_surface[3 + j][3 + k].copy()

                    elif i == 5:
                          self.Sudokou_surface[i][j][k] = self.other_see_surface[3 + j][6 + k].copy()

                    elif i == 6:
                        self.Sudokou_surface[i][j][k] = self.other_see_surface[6 + j][k].copy()

                    elif i == 7:
                        self.Sudokou_surface[i][j][k] = self.other_see_surface[6 + j][3 + k].copy()

                    elif i == 8:
                         self.Sudokou_surface[i][j][k] = self.other_see_surface[6 + j][6 + k].copy()



    def convert_surface_main_to_other(self):

        for i in range(11):

            for j in range(3):

                for k in range(3):
                    if i == 0:
                        self.other_see_surface[j][k] = self.Sudokou_surface[i][j][k].copy()

                    elif i == 1:
                        self.other_see_surface[j][3 + k] = self.Sudokou_surface[i][j][k].copy()

                    elif i == 2:
                        self.other_see_surface[j][6 + k] = self.Sudokou_surface[i][j][k].copy()

                    elif i == 3:
                        self.other_see_surface[3 + j][k] = self.Sudokou_surface[i][j][k].copy()

                    elif i == 4:
                        self.other_see_surface[3 + j][3 + k] = self.Sudokou_surface[i][j][k].copy()

                    elif i == 5:
                        self.other_see_surface[3 + j][6 + k] = self.Sudokou_surface[i][j][k].copy()

                    elif i == 6:
                        self.other_see_surface[6 + j][k] = self.Sudokou_surface[i][j][k].copy()

                    elif i == 7:
                        self.other_see_surface[6 + j][3 + k] = self.Sudokou_surface[i][j][k].copy()

                    elif i == 8:
                        self.other_see_surface[6 + j][6 + k] = self.Sudokou_surface[i][j][k].copy()

    """
    به کمک این تابع عمل cross over 
    را روی دوتا سودکو را انجام میدهیم .
    یک عدد بین صفر و ۱۱ انتخاب میکنیم و تصمیمم میگیریم به یکی از شکل های زیر عمل را انجام بدیم .
    
    
    ۱.مربع ۱ پدر را با مربع ۱ مادر عوض کنیم 
    و برعکس و حاصل دوتا فرزند را بر میگردانیم .
    ۲. مربع دوم پدر و مادر را عوض میکنیم .
    .
    .
    .
    .
    .
    .
    ۱۰. بعد اینکه تصمیم گرفتیم که کدوم یک از مربع ها را باهمدیگر عوض کینم .
    می تونیم به عنوان یک از گزینه های کراس آور به این گونه عمل کنیم که 
    چند خط از پدر و مادر را باهم دیگه عوض کنیم 
    مثلا به صورت رندوم خط های ۲و ۴و ۶ و ۸ 
    شان را با همدیگر عوض کنیم و 
    دوتا فرزند را به عنوان خروجی بیرون بدهیم . 

    
    """

    def Marriage(self, other):

        first_child = copy.deepcopy(self)
        secend_child = copy.deepcopy(other)
        x = random.randrange(11)

        if x == 0:

            first_child.Sudokou_surface[0] = secend_child.Sudokou_surface[0].copy()
            secend_child.Sudokou_surface[0] = self.Sudokou_surface[0].copy()

        elif x == 1:

            first_child.Sudokou_surface[1] = secend_child.Sudokou_surface[1].copy()
            secend_child.Sudokou_surface[1] = self.Sudokou_surface[1].copy()

        elif x == 2:

            first_child.Sudokou_surface[2] = secend_child.Sudokou_surface[2].copy()
            secend_child.Sudokou_surface[2] = self.Sudokou_surface[2].copy()

        elif x == 3:

            first_child.Sudokou_surface[3] = secend_child.Sudokou_surface[3].copy()
            secend_child.Sudokou_surface[3] = self.Sudokou_surface[3].copy()

        elif x == 4:

            first_child.Sudokou_surface[4] = secend_child.Sudokou_surface[4].copy()
            secend_child.Sudokou_surface[4] = self.Sudokou_surface[4].copy()

        elif x == 5:

            first_child.Sudokou_surface[5] = secend_child.Sudokou_surface[5].copy()
            secend_child.Sudokou_surface[5] = self.Sudokou_surface[5].copy()

        elif x == 6:

            first_child.Sudokou_surface[6] = secend_child.Sudokou_surface[6].copy()
            secend_child.Sudokou_surface[6] = self.Sudokou_surface[6].copy()

        elif x == 7:

            first_child.Sudokou_surface[7] = secend_child.Sudokou_surface[7].copy()
            secend_child.Sudokou_surface[7] = self.Sudokou_surface[7].copy()

        elif x == 8:

            first_child.Sudokou_surface[8] = secend_child.Sudokou_surface[8].copy()
            secend_child.Sudokou_surface[8] = self.Sudokou_surface[8].copy()

        elif x == 9:

            random_number = random.randrange(0, 3)

            random_number2 = random.randrange(5, 8)

            random_number3_step = random.randrange(1, random_number2 - random_number)

            for k in range(random_number, random_number2, random_number3_step):
                first_child.other_see_surface[k] = secend_child.other_see_surface[k].copy()
                secend_child.other_see_surface[k] = self.other_see_surface[k].copy()

            first_child.convert_other_to_surface_main()
            secend_child.convert_other_to_surface_main()


        elif x == 10:

            random_number_select = random.randrange(10, 20)
            list_crossover = []
            for k in range(random_number_select):

                tuple_k = (random.randrange(9), random.randrange(9))

                if tuple_k not in list_crossover:
                    list_crossover.append(tuple_k)

            for x in list_crossover:
                first_child.other_see_surface[x[0]][x[1]] = secend_child.other_see_surface[x[0]][x[1]].copy()
                secend_child.other_see_surface[x[0]][x[1]] = self.other_see_surface[x[0]][x[1]].copy()

            first_child.convert_other_to_surface_main()
            secend_child.convert_other_to_surface_main()

        first_child.convert_surface_main_to_other()
        first_child.find_its_how_much_each_number_rapid()
        first_child.find_Fitness()
        # print(first_child.fitness)
        # print(first_child)
        # print("______________________________")

        secend_child.convert_surface_main_to_other()
        secend_child.find_its_how_much_each_number_rapid()
        secend_child.find_Fitness()
        # print(secend_child.fitness)
        # print(secend_child)
        # print("______________________________")

        return first_child, secend_child

    def make_better(self):
        list_Item_much_9 = []
        list_Item_less_9 = []
        for i in range(9):

            if self.how_much_each_number_rapid[i] > 9:

                k = [i + 1] * (self.how_much_each_number_rapid[i] - 9)
                list_Item_much_9 += k
            elif i < 9:

                k = [i + 1] * (9 - self.how_much_each_number_rapid[i])
                list_Item_less_9 += k

        for i in self.Sudokou_surface:

            for j in i:

                for k in j:

                    if k[1]:

                        if list_Item_much_9:

                            if k[0] == list_Item_much_9[0]:
                                list_Item_much_9.pop()
                                k[1] = list_Item_less_9.pop()
        self.convert_surface_main_to_other()

    '''
    به صورت رندوم یک سری از خانه های سودکو را باهم دیگه عوض میکنیم با این شرط که ثابت نباشن 
    یعنی توسط کاربر مقدار دهی اولیه نشده باشن .
    
    '''
    def mutation(self):

        helper = copy.deepcopy(self)
        random_k = random.randrange(3)

        random_number = random.randrange(1, 30)

        for number in range(random_number):

            random_number2 = random.randrange(0, 8)
            random_number3 = random.randrange(0, 8)
            if helper.other_see_surface[random_number2][random_number3][1]:

                e = random.randrange(1, 9)

                add_to_i = e % (9 - random_number2) + random_number2
                add_to_j = e % (9 - random_number3) + random_number3

                if helper.other_see_surface[add_to_i][add_to_j][1]:
                    switch = helper.other_see_surface[add_to_i][add_to_j][0]

                    helper.other_see_surface[add_to_i][add_to_j][0] = \
                        helper.other_see_surface[random_number2][random_number3][0]

                    helper.other_see_surface[random_number2][random_number3][0] = switch
        helper.convert_other_to_surface_main()

        if random_k != 1:
            helper.make_better()
            random_number4 = random.randrange(0, 9)

        return helper

    """
    به ما میگه چه تعداد هر کدوم از اعداد ۱ تا ۹ تکرار شده اند در سودکو 
    """
    def find_its_how_much_each_number_rapid(self):

        list_how_much = [0 for i in range(9)]

        for i in self.Sudokou_surface:

            for j in i:

                for k in j:
                    list_how_much[k[0] - 1] += 1

        self.how_much_each_number_rapid = list_how_much

    def is_row_dupliccate(self, row, value):
        """ Check whether there is a duplicate of a fixed/given value in a row. """
        for column in range(9):
            if self.other_see_surface[row][column] == value:
                return True
        return False

    def is_column_duplicate(self, column, value):

        """ Check whether there is a duplicate of a fixed/given value in a column. """
        for row in range(9):
            if self.other_see_surface[row][column] == value:
                return True
        return False

    def is_block_duplicate(self, row, column, value):

        find_squre = self.find_squre(row, column)

        for s in self.Sudokou_surface[find_squre]:

            for item in s:

                if item[0] == value:
                    return True

        else:

            return False

    def find_squre(self, row, column):

        if 0 <= row <= 2 and 0 <= column <= 2:
            return 0

        elif 0 <= row <= 2 and 3 <= column <= 5:

            return 1

        elif 0 <= row <= 2 and 6 <= column <= 8:

            return 2

        elif 3 <= row <= 5 and 0 <= column <= 2:

            return 3

        elif 3 <= row <= 5 and 3 <= column <= 5:

            return 4

        elif 3 <= row <= 5 and 6 <= column <= 8:

            return 5

        elif 6 <= row <= 8 and 0 <= column <= 2:

            return 6

        elif 6 <= row <= 8 and 3 <= column <= 5:

            return 7

        elif 6 <= row <= 8 and 6 <= column <= 8:

            return 8

    def __str__(self):
        Str = ""
        for i in range(9):
            for j in range(9):
                Str += " " + str(self.other_see_surface[i][j][0]) + " " + "|"
            Str += "\n"
        return Str


'''
سودکو اولیه را از کاربر میگیرد و سعی میکند خودش حل کند .
از کاربر میخواهد که بگوید چند تا از خانه ها را میخواهد مقدار دهی کند .
در مرحله بعد از کاربر میخواهد که بگوید در کدام یک از ۱ تا ۹ مربع هست 
و در چه طول و عرضی از این مربع هست .
'''

def give_Sudokou():
    number_item_in_table_we_know_their_amount = int(input("Pleease ENter number item that in table we know : "))
    list_number_I_see = [0 for i in range(1, 10)]
    list_item_define = []
    for i in range(number_item_in_table_we_know_their_amount):
        number_square = int(input("Please Enter the number of square : "))
        x, y = tuple(map(int, input("Please give Coordinates : ").split()))
        number = int(input("Please give number item between 1 _ 9 :"))

        list_number_I_see[number - 1] += 1

        list_item_define.append([number_square, (x, y), number])

    return Sudokou(list_item_define, list_number_I_see)

"""
از لیست سودکوها ۸۵ درصد تعداد را برمیدارد با ادغامشان میکند.
به غیر از این موارد همواره بهترین سودکو و بدترین 
بهترین سودکو و سودکوی قبلی که بهترین وضعیت را دارد رو نیز crass over می دهد .
"""

def crossover(list_of_Initial_Population):
    size_of_list = len(list_of_Initial_Population)

    list_result = []

    how_much_have_marige = int(0.85 * size_of_list)

    best_child_we_think_one, best_child_we_think_two = list_of_Initial_Population[0].Marriage(
        list_of_Initial_Population[1])
    list_result.append(best_child_we_think_one)
    list_result.append(best_child_we_think_two)
    strange_child1, strange_child2 = list_of_Initial_Population[0].Marriage(list_of_Initial_Population[-1])
    list_result.append(strange_child1)
    list_result.append(strange_child2)
    for ma in range(how_much_have_marige):

        random_item = random.randrange(size_of_list)

        father_Sudokou = list_of_Initial_Population[random_item]

        random_item2 = random.randrange(size_of_list)
        while random_item == random_item2:
            random_item2 = random.randrange(size_of_list)

        mother_Sudokou = list_of_Initial_Population[random_item2]

        first_child, secend_child = father_Sudokou.Marriage(mother_Sudokou)

        list_result.append(first_child)
        list_result.append(secend_child)

    list_result += list_of_Initial_Population
    return list_result

"""
به کمک این تابع ۱۵ درصد از لیست اصلی را جهش میدهیم .
"""
def mutation(list_of_Initial_Population):
    size_of_list = len(list_of_Initial_Population)

    how_much_have_marige = int(0.15 * size_of_list)
    list_of_Initial_Population[1].make_better()

    for ma in range(how_much_have_marige):
        random_item = random.randrange(size_of_list)

        list_of_Initial_Population.append(list_of_Initial_Population[random_item].mutation())
"""
از بین تمام عناصری که ساخته شده 
بهترین ۳۵ تا سودکو را انتخاب میکند .
۱۰۰ تا سودکو دیگر هم به صورت رندوم میسازد و حاصل را به لیست اصلی اضافه میکنه .
در نهایت از بین لیست موجود ۲۰۰ مورد را به صورت رندوم انتخاب میکند و 
۳۵ مورد  عالی قبلی را نیز به لیست جدید اضافه میکند .
 
"""

def selection(list_of_Initial_Population, Sudokou):
    for i in range(100):
        helper = copy.deepcopy(Sudokou)
        list_of_Initial_Population.append(helper.find_random_sitution())

    list_of_Initial_Population.sort(reverse=True, key=lambda x: x.fitness)
    list_result = list_of_Initial_Population[:35]
    size = len(list_of_Initial_Population)
    list_see = [0 for i in range(size)]
    for i in range(35):
        list_see[i] = 1

    list_see[0] += 1

    while sum(list_see) != 200:

        random_number = random.randrange(size)

        if list_see[random_number] == 0:
            list_see[random_number] += 1

            list_result.append(list_of_Initial_Population[random_number])
    list_result.sort(reverse=True, key=lambda x: x.fitness)
    return list_result


def how_much_is_rapidly(list_of_Initial_Population, Sudokou):
    best = list_of_Initial_Population[0]
    how_much = 1
    for i in range(1, len(list_of_Initial_Population)):

        if list_of_Initial_Population[i] == best:
            how_much += 1

    if how_much > len(list_of_Initial_Population) * 5 / 8:
        list_of_Initial_Population = list_of_Initial_Population[len(list_of_Initial_Population) * 5 / 8:]

        for i in range(how_much):
            helper = copy.deepcopy(Sudokou)
            list_of_Initial_Population.append(helper.find_random_sitution())

        one_can_be_good = copy.deepcopy(best)
        list_of_Initial_Population.append(best)

        list_of_Initial_Population.sort(reverse=True, key=lambda x: x.fitness)

        return list_of_Initial_Population

    else:

        return list_of_Initial_Population

"""
مراحل 
crass over 
mutation
,selection 
را در تابعی که سعی داره این مسئله را حل کند می بینید .

در فایل پایتون SudokuTest 
مشاهده کردیم که اگر همام mutation 
را بهتر تعریف کنیم به تنهایی مسئله قابل حل میباشد .

"""

def find_Solution(Sudokou):
    list_of_Initial_Population = []
    for i in range(100):
        helper = copy.deepcopy(Sudokou)
        list_of_Initial_Population.append(helper.find_random_sitution())

    list_of_Initial_Population.sort(reverse=True, key=lambda x: x.fitness)
    print(list_of_Initial_Population[0].fitness)
    print(list_of_Initial_Population[50].fitness)
    print(list_of_Initial_Population[-1].fitness)
    print(list_of_Initial_Population[0])
    print("__________________________")
    print(list_of_Initial_Population[1])
    y = list_of_Initial_Population[0].fitness
    how_much_do_random = 0
    while y < 1:
        list_of_Initial_Population = crossover(list_of_Initial_Population)
        mutation(list_of_Initial_Population)
        list_of_Initial_Population = selection(list_of_Initial_Population, Sudokou)

        y = list_of_Initial_Population[0].fitness
        x = list_of_Initial_Population[-1].fitness
        how_much_do_random += 1
        list_of_Initial_Population = how_much_is_rapidly(list_of_Initial_Population, Sudokou)
        print("__________________________")
        print(y)
        print(list_of_Initial_Population[50].fitness)
        print(x)
        print(how_much_do_random)
        print()
        print(list_of_Initial_Population[0])
        print("__________________________")

    return list_of_Initial_Population[0]


def main():
    Sudokou = give_Sudokou()

    solution_of_problem = find_Solution(Sudokou)
    print(solution_of_problem)


if __name__ == '__main__':
    main()
