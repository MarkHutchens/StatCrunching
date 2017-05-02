__author__ = 'mark'

#from combo_without_replace import * #Cut out and put all the functions down below.
import csv
import random
random.seed("Phonology is absolutely fantastic!")
import math
import statistics
import ast

#csvfile.close()
class Language():
    def __init__(self, name, family, secondary, duration, pitch, intensity):
        self.name = name
        self.family = family
        self.secondary = secondary

        #In case there are blanks.
        try:
            self.duration = int(duration)
        except:
            self.duration = None
        try:
            self.pitch = int(pitch)
        except:
            self.pitch = None
        try:
            self.intensity = int(intensity)
        except:
            self.intensity = None

    def __str__(self):
        return(self.name + ": " +  str(self.duration) + " " +  str(self.pitch) + " " + str(self.intensity))

    def d(self):
        if self.duration == 2:  #Annoying hacky way around empty ones.
            #print("I'm a bad person")
            return
        return self.duration
    def p(self):
        if self.pitch == 2:
            #print("I'm a bad person")
            return
        return self.pitch
    def i(self):
        if self.i == 2:
            #print("I'm a bad person")
            return
        return self.intensity
    def fam(self):
        return self.family

    def __eq__(self, other):
        return str(self) == str(other)

    def __lt__(self, other):
        return str(self) < str(other)

    def __gt__(self, other):
        return str(self) > str(other)

class LangDict(dict):
    def __init__(self):
        self = {}

    def fam(self, fam_name):
        l = []
        k = self.keys()
        for i in k:
            if self[i].fam() == fam_name:
                l.append(self[i])
        return l

    def all(self):
        l = []
        k = self.keys()
        for i in k:
            l.append(self[i])
        return l

    def fam_list(self):
        #Returns a list of all language families in the dictionary
        l = []
        for lang in self:
            if self[lang].fam() not in l:
                l.append(self[lang].fam())
        return l

    def fam_quant_list(self):
        #returns a list of the FREQUENCIES of language families. This'll get shuffled later.
        f_list = self.fam_list()
        to_return = [0] * len(f_list)
        count = 0
        for family in f_list:
            for l in self:
                #I'm a bad boy who nests loops for convenience, not speed. Sue me.
                if self[l].fam() == family:
                    to_return[count] += 1
            count += 1
        return to_return

    def get_feature_frequencies(self, feature):
        #return the number of durations, pitches, etc. Not implemented.
        sum = 0
        pos = 0
        for l in self.all():
            #skip counting if the item is none
            if feature == 'd':
                if l.d() == 1:
                    sum += 1
                    pos += 1
                elif l.d() == 0:
                    sum += 1
            elif feature == 'p':
                if l.p():
                    sum += 1
                    pos += 1
                elif l.p() == 0:
                    sum += 1
            elif feature == 'i':
                if l.i():
                    sum += 1
                    pos += 1
                elif l.i() == 0:
                    sum += 1
        return(sum,pos)

def num_sets(size, sub):
    #Calculates the number of subsets of a particular size you can make
    size_fac = (math.factorial(size) / math.factorial(size - sub)) / math.factorial(sub)
    return size_fac

def num_sets_of_features_for_specific_num(size, feature_size, sub, num):
    #size is the total sample size (141)
    #feature_size is how many languages have the feature (83)
    #sub is the size of the subset we are generating (20)
    #num is the target number we're checking
    sum = 0.0
    if((size - feature_size) < sub - num):  #Can't possibly make that size of thing, yo.
        pass
    else:
        sum += num_sets(feature_size, num) * num_sets(size - feature_size, sub - num)
                                                            #44-35,
    #print(sum)
    return sum

def s_chance(total, pos, per, target, over_under):
    sum_chance = 0
    #0 to target+1 if you're looking for odds of below, target to max+1 (21) if you're looking for odds of above.
    if (over_under == "o"):
        for i in range(target, per + 1):
            sum_chance += num_sets_of_features_for_specific_num(total,pos,per,i) / num_sets(total,per)
        #print("Chance of having exactly this many or more: ", sum_chance)
    elif (over_under == "u"):
        for i in range(0, target + 1):
            sum_chance += num_sets_of_features_for_specific_num(total,pos,per,i) / num_sets(total,per)
        #print("Chance of having exactly this many or less: ", sum_chance)
    return sum_chance


class Enormous_Iterable:
    #Enables me to make an enormous iterable object. Will take forever to get through.
    def __init__(self, l = []):
        self.l = l
        self.current_num = 0
        self.inner = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_num >= len(self.l):
            self.current_num = 0
            self.inner = 0
            raise StopIteration
        elif self.inner >= self.l[self.current_num]:
            self.current_num += 1
            self.inner = 0
        self.inner += 1
        return self.current_num

    def append(self,to_append):
        self.l.append(to_append)

    def get_list(self):
        s = "["
        for i in self.l:
            s += str(i) + ","
        s += "]"
        return self.l

'''
def calc_std_dev(total, pos, per):
    #sets = num_sets(total, per)
    avg_sum = 0
    avg_count = 0
    stupidly_long_list = Enormous_Iterable([])
    for x in range(0,per + 1):
        sub_chance = num_sets_of_features_for_specific_num(total, pos, per, x)
        #print("The chance for", x, "is", sub_chance)
        #chance = sub_chance/sets
        avg_sum += (sub_chance * x)
        avg_count += sub_chance
        stupidly_long_list.append(sub_chance / (2.0 ** 60))
    #for x in stupidly_long_list:
        #print(x)
    #for i in stupidly_long_list:
        #print(i)
    #print(stupidly_long_list.get_list())
    return (statistics.stdev(stupidly_long_list), avg_sum/avg_count)
'''

def calc_std_dev(total_pos, per):
    #sets = num_sets(total, per)
    total = total_pos[0]
    pos = total_pos[1]
    avg_sum = 0
    avg_count = 0
    stupidly_long_list = Enormous_Iterable([])
    for x in range(0,per + 1):
        sub_chance = num_sets_of_features_for_specific_num(total, pos, per, x)
        #print("The chance for", x, "is", sub_chance)
        #chance = sub_chance/sets
        avg_sum += (sub_chance * x)
        avg_count += sub_chance
        stupidly_long_list.append(sub_chance / (2.0 ** 60))
    #for x in stupidly_long_list:
        #print(x)
    #for i in stupidly_long_list:
        #print(i)
    #print(stupidly_long_list.get_list())
    return (statistics.stdev(stupidly_long_list), avg_sum/avg_count)



def print_dict(d: {}):
    l = d.keys()
    for lang in l:
        print (d[lang])

def total(d: {}):
    return len(d.keys())

def average(l: []):
    #Just returns the arithmetic mean of a list.
    #It looks like arithmetic mean is the correct type of average to use, no harmonic or geometric nonsense.
    sum = 0.0
    for i in l:
        sum += i
    return sum / len(l)

#d, p, i
#7, 8, 9


"""
(stddev_d, avd) = calc_std_dev(143,84,20)
(stddev_p, avp) = calc_std_dev(143,94,20)
(stddev_i, avi) = calc_std_dev(143,88,20)
print("The Standard Deviation for duration is", stddev_d , "with avg of", avd)
print("The Standard Deviation for pitch is", stddev_p , "with avg of", avp)
print("The Standard Deviation for intensity is", stddev_i , "with avg of", avi)

#The Standard Deviation for duration is 2.049164318670745 with avg of 11.748251748251748
#The Standard Deviation for pitch is 1.9755309101362408 with avg of 13.14685314685315
#The Standard Deviation for intensity is 2.025071924745733 with avg of 12.307692307692308
"""



def get_list_string(l):
    s1 = "["
    s2 = "["
    for i in l:
        s1 += "{0:.2f}".format(i[0]) + ","
        s2 += "{0:.2f}".format(i[1]) + ","
    s1 += "]"
    s2 += "]"
    #print(s1)
    #print(s2)
    #print()
    s1 = s1.replace(',]',']')
    s1 = ast.literal_eval(s1)
    s2 = s2.replace(',]',']')
    s2 = ast.literal_eval(s2)
    return (s1,s2)



stddev_d = None
stddev_p = None
stddev_i = None
avd = None
avp = None
avi = None


#csvfile = open('Mar19Random.csv', 'r', encoding='latin-1')
#csvfile = open('Mar19Acoustic2.csv', 'r', encoding='latin-1')
#csvfile = open('Langs.csv', 'r', encoding='latin-1')
#csvfile = open('Mar27Langs.csv', 'r', encoding='latin-1')
#csvfile = open('Mar27LangsExtreme.csv', 'r', encoding='latin-1')
csvfile = open('Mar27FINAL.csv', 'r', encoding='latin-1')



langreader = csv.reader(csvfile, delimiter = ',')

lang_dict = LangDict() #I'm a bad person.

for row in langreader:
    if row[0] == "Language" or row[0] == "": #Easy way to remove those two lines.
        continue
    newlang = Language(row[0],row[1],row[2],row[7],row[8],row[9])
    lang_dict[row[0]] = newlang


#Make stddev and averages for langs.

# stddev_d = [calc_std_dev(lang_dict.get_feature_frequencies('d'),n) for n in range(22)]
# stddev_p = [calc_std_dev(lang_dict.get_feature_frequencies('p'),n) for n in range(22)]
# stddev_i = [calc_std_dev(lang_dict.get_feature_frequencies('i'),n) for n in range(22)]
#
# temp_thing = get_list_string(stddev_d)
# stddev_d = temp_thing[0]
# avd = temp_thing[1]
# temp_thing = get_list_string(stddev_p)
# stddev_p = temp_thing[0]
# avp = temp_thing[1]
# temp_thing = get_list_string(stddev_i)
# stddev_i = temp_thing[0]
# avi = temp_thing[1]
#
# print('stddev_d = ', stddev_d)
# print('stddev_p = ', stddev_p)
# print('stddev_i = ', stddev_i)
# print('avd = ', avd)
# print('avp = ', avp)
# print('avi = ', avi)

# stddev_d =  [0.71, 1.0, 1.29, 1.58, 1.87, 2.16, 2.45, 2.74, 3.03, 3.32, 3.61, 3.89, 4.18, 4.47, 4.49, 3.01, 2.11, 1.94, 1.96, 2.0, 2.04, 2.08]
# stddev_p =  [0.71, 1.0, 1.29, 1.58, 1.87, 2.16, 2.45, 2.74, 3.03, 3.32, 3.61, 3.89, 4.18, 4.47, 4.76, 3.42, 2.2, 1.89, 1.87, 1.9, 1.94, 1.98]
# stddev_i =  [0.71, 1.0, 1.29, 1.58, 1.87, 2.16, 2.45, 2.74, 3.03, 3.32, 3.61, 3.89, 4.18, 4.47, 4.62, 3.23, 2.16, 1.94, 1.93, 1.97, 2.01, 2.05]
# avd =  [0.0, 0.59, 1.19, 1.78, 2.37, 2.96, 3.56, 4.15, 4.74, 5.34, 5.93, 6.52, 7.11, 7.71, 8.3, 8.89, 9.49, 10.08, 10.67, 11.26, 11.86, 12.45]
# avi =  [0.0, 0.62, 1.25, 1.87, 2.49, 3.12, 3.74, 4.36, 4.99, 5.61, 6.23, 6.86, 7.48, 8.1, 8.72, 9.35, 9.97, 10.59, 11.22, 11.84, 12.46, 13.09]
# avp =  [0.0, 0.68, 1.36, 2.04, 2.72, 3.39, 4.07, 4.75, 5.43, 6.11, 6.79, 7.47, 8.15, 8.82, 9.5, 10.18, 10.86, 11.54, 12.22, 12.9, 13.58, 14.26]

stddev_d =  [0.71, 1.0, 1.29, 1.58, 1.87, 2.16, 2.45, 2.74, 3.03, 3.32, 3.61, 3.89, 4.18, 4.47, 4.49, 3.01, 2.11, 1.94, 1.96, 2.0, 2.04, 2.08]
stddev_p =  [0.71, 1.0, 1.29, 1.58, 1.87, 2.16, 2.45, 2.74, 3.03, 3.32, 3.61, 3.89, 4.18, 4.47, 4.76, 3.53, 2.26, 1.89, 1.86, 1.89, 1.93, 1.97]
stddev_i =  [0.71, 1.0, 1.29, 1.58, 1.87, 2.16, 2.45, 2.74, 3.03, 3.32, 3.61, 3.89, 4.18, 4.47, 4.62, 3.23, 2.16, 1.94, 1.93, 1.97, 2.01, 2.05]
avd =  [0.0, 0.59, 1.19, 1.78, 2.37, 2.96, 3.56, 4.15, 4.74, 5.34, 5.93, 6.52, 7.11, 7.71, 8.3, 8.89, 9.49, 10.08, 10.67, 11.26, 11.86, 12.45]
avp =  [0.0, 0.68, 1.37, 2.05, 2.74, 3.42, 4.1, 4.79, 5.47, 6.15, 6.84, 7.52, 8.21, 8.89, 9.57, 10.26, 10.94, 11.62, 12.31, 12.99, 13.68, 14.36]
avi =  [0.0, 0.62, 1.25, 1.87, 2.49, 3.12, 3.74, 4.36, 4.99, 5.61, 6.23, 6.86, 7.48, 8.1, 8.72, 9.35, 9.97, 10.59, 11.22, 11.84, 12.46, 13.09]


#print_dict(lang_dict)
print(total(lang_dict))
'''
sub = lang_dict.fam("Indo-European")
for i in sub:
    print(i)
'''
cutoff = int(input("How small a language family should we count? ")) #Make an input at some point.
all = lang_dict.all()
all_values = [0,0,0]
all_no_datas = [0,0,0]
for lang in all:
    if lang.d() != None:
        all_values[0] += lang.d()
    else:
        all_no_datas[0] += 1
    if lang.p() != None:
        all_values[1] += lang.p()
    else:
        all_no_datas[1] += 1
    if lang.i() != None:
        all_values[2] += lang.i()
    else:
        all_no_datas[2] += 1

probs = []


def z_score(size, num, type):
    if type == 0:
        avg = avd[size]
        std = stddev_d[size]
    elif type == 1:
        avg = avp[size]
        std = stddev_p[size]
    elif type == 2:
        avg = avi[size]
        std = stddev_i[size]

    z = abs(((num - avg) / std))
    return z



for family in lang_dict.fam_list():
    sub = lang_dict.fam(family)
    sub_values = [0,0,0]
    no_datas = [0,0,0]        #The number of langs in the family without a particular piece of data.

    if len(sub) >= cutoff: #Arbitrary cutoff.
        print(family, len(sub))
        for lang in sub:
            #I'm sorry this got so much uglier.
            if lang.d() != None:
                sub_values[0] += lang.d()
            else:
                no_datas[0] += 1
            if lang.p() != None:
                sub_values[1] += lang.p()
            else:
                no_datas[1] += 1
            if lang.i() != None:
                sub_values[2] += lang.i()
            else:
                no_datas[2] += 1

        for i in range(0,3):
            #print((all_values[i] / len(all)))
            #print(sub_values[i], "out of", len(sub))
            if ((all_values[i] / (len(all) - all_no_datas[i])) < (sub_values[i] / (len(sub) - no_datas[i]) )):
                o_u = "o"
            else:
                o_u = "u"

            #probs.append(s_chance(len(all), all_values[i], len(sub),sub_values[i], o_u)) #old draft version
            probs.append(z_score((len(sub) - no_datas[i]), sub_values[i], i))

print("Number is: ", len(probs))
to_compare = average(probs)
print("Average z-score (absolute) is: ", to_compare)
stddev_empirical = statistics.stdev(probs)
print("Standard deviation is: ", stddev_empirical, "which is pretty high, but we have a very small sample set here. I care about the average.")



fql = lang_dict.fam_quant_list() #.sort is to make the random seed deterministic.
fql.sort()
#print(fql)

rand_langs_template = lang_dict.all()
rand_langs_template.sort()
rand_langs = rand_langs_template[:]
random.shuffle(fql)
random.shuffle(rand_langs)
new_probs = []

sum = 0
c = 10000   #Can increase or decrease number to try to get a more precise z-score. But we're reliably over 1.7, so who cares.
vals = []

total_Austronesian = [0,0,0]
count_Austronesian = 0

for x in range(0,c):
    rand_langs = rand_langs_template[:]
    random.shuffle(fql)
    random.shuffle(rand_langs)
    new_probs = []
    for family in fql:
        sub = rand_langs[0:family]
        del rand_langs[0:family]
        sub_values = [0,0,0]
        no_datas = [0,0,0]

        if len(sub) >= cutoff:
            #The idea is to only count families that are substantial.
            #print("Family", family)
            for lang in sub:
                if lang.d() != None:
                    sub_values[0] += lang.d()
                else:
                    no_datas[0] += 1
                if lang.p() != None:
                    sub_values[1] += lang.p()
                else:
                    no_datas[1] += 1
                if lang.i() != None:
                    sub_values[2] += lang.i()
                else:
                    no_datas[2] += 1

            for i in range(0,3):
                #print((all_values[i] / len(all)))
                #print(sub_values[i], "out of", len(sub))

                if(len(sub) == 21):
                    #print("Austronesian here:")
                    count_Austronesian+=1
                    total_Austronesian[i] += sub_values[i]


                if ((all_values[i] / (len(all) - all_no_datas[i])) < (sub_values[i] / (len(sub) - no_datas[i]) )):
                    o_u = "o"
                else:
                    o_u = "u"

                #new_probs.append(s_chance(len(all), all_values[i], len(sub),sub_values[i], o_u))
                new_probs.append(z_score((len(sub) - no_datas[i]), sub_values[i], i))
    #print(new_probs)
    #print("Number is: ", len(new_probs))
    #print ("Comparative Average is: ", average(new_probs))
    sum += average(new_probs)
    vals.append(average(new_probs))

for i in range(0,3):
   print('Average Aus = ', total_Austronesian[i] / (count_Austronesian/3), total_Austronesian, count_Austronesian)
full_avg = sum / c
print("The overall expected z-score is:", full_avg)
meta_zscore_stdev = statistics.stdev(vals)
print("The standard deviation is:", meta_zscore_stdev)

meta_z_score_value = (to_compare - full_avg) / meta_zscore_stdev
print("Our meta_z_score is: ", meta_z_score_value)

print("That means that there's a very small chance of us seeing the z-score we see in our actual data set.")
print("Let's count the number of tries it takes to get a result as z-score as ours, shall we?")


max_z_score = 0
n = 0
m = int(input("How many times should we try to hit our number? More than 200 will feel like an eternity. "))
expected_sum = 0
while n < m:
    n += 1
    stopper = False
    until_stop = 0
    while not stopper:
        until_stop += 1
        rand_langs = rand_langs_template[:]
        random.shuffle(fql)
        random.shuffle(rand_langs)
        new_probs = []
        for family in fql:
            sub = rand_langs[0:family]
            del rand_langs[0:family]
            sub_values = [0,0,0]
            no_datas = [0,0,0]

            if len(sub) >= cutoff:
                #The idea is to only count families that are substantial.
                #print("Family", family)
                for lang in sub:
                    if lang.d() != None:
                        sub_values[0] += lang.d()
                    else:
                        no_datas[0] += 1
                    if lang.p() != None:
                        sub_values[1] += lang.p()
                    else:
                        no_datas[1] += 1
                    if lang.i() != None:
                        sub_values[2] += lang.i()
                    else:
                        no_datas[2] += 1

                for i in range(0,3):
                    #print((all_values[i] / len(all)))
                    #print(sub_values[i], "out of", len(sub))
                    if ((all_values[i] / (len(all) - all_no_datas[i])) < (sub_values[i] / (len(sub) - no_datas[i]) )):
                        o_u = "o"
                    else:
                        o_u = "u"
                    #new_probs.append(s_chance(len(all), all_values[i], len(sub),sub_values[i], o_u))
                    new_probs.append(z_score((len(sub) - no_datas[i]), sub_values[i], i))

        #print(new_probs)
        #print("Number is: ", len(new_probs))
        #print ("Comparative Average is: ", average(new_probs))
        av = average(new_probs)
        if av >= to_compare:
            if(av > max_z_score):
                max_z_score = av
            stopper = True
        sum += av

    expected_sum += until_stop
    print("Oh my golly gee, it took us", until_stop, "tries to get our z-score", n, "times!")

expected = expected_sum / m
print("That means the mean time to happen is about once every", expected, "attempts!")
print("That's not very often!")
print("And the largest z score we ever saw was: ", max_z_score)
csvfile.close()