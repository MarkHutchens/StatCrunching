__author__ = 'mark'
import random
import math

per = int(input("Number Drawn Per Test: "))
pos = int(input("Positives: "))
total = int(input("Total: "))
neg = total - pos
target = int(input("What is the target number? "))
over_under = input("[o]ver or [u]nder? ").lower() #That's whether the language family result was over or under expected value

"""
#This section is pretty much just the last program. It's a Monte Carlo simulation. Uncomment if you want to compare results.
#https://en.wikipedia.org/wiki/Monte_Carlo_method

count = int(input("Number of Tests: "))
per = int(input("Number Drawn Per Test: "))
pos = int(input("Positives: "))
total = int(input("Total: "))
neg = total - pos

def sumlist(l):
    s = 0
    for i in l:
        s += i
    return s


list = [0]*neg + [1]*pos
totals = [0] * (per+1)

totalprob = []
indi = [0] * (per+1)
indiprob = []

for x in range(0,count):
    newlist = list.copy()
    random.shuffle(newlist)
    selected = []
    for i in range (0,per):
        selected.append(newlist.pop())
    sum = sumlist(selected)
    if sum == 0:
        print("Odd case happens")
    for i in range (0,sum + 1):
        totals[i] += 1
    indi[sum] += 1


for i in range(len(totals)):
    totalprob.append(totals[i]/count)
    indiprob.append(indi[i]/count)


for i in range(len(totalprob)):
    print(i, "has a probability of:", totalprob[i], "(" + str(indiprob[i]) + ")")
"""

#Math time
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
    sum += num_sets(feature_size, num) * num_sets(size - feature_size, sub - num)
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


print("Total possible subsets:", num_sets(total,per)) #Compare: http://stattrek.com/online-calculator/combinations-permutations.aspx
print("Chance of having exactly this many: " + str(num_sets_of_features_for_specific_num(total,pos,per,target) / num_sets(total,per)))

sum_chance = 0
#0 to target+1 if you're looking for odds of below, target to max+1 (21) if you're looking for odds of above.
if (over_under == "o"):
    for i in range(target, per + 1):
        sum_chance += num_sets_of_features_for_specific_num(total,pos,per,i) / num_sets(total,per)
    print("Chance of having exactly this many or more: ", sum_chance)
elif (over_under == "u"):
    for i in range(0, target + 1):
        sum_chance += num_sets_of_features_for_specific_num(total,pos,per,i) / num_sets(total,per)
    print("Chance of having exactly this many or less: ", sum_chance)

























