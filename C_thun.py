import random

def randHit(enemies, num):
    enemies[num] -= 1
    if enemies[num] == 0:
        enemies.pop(num)


def runCthun(enemies, hits):
    #enemies is a list of health values.

    for h in range(0,hits):
        x = len(enemies) - 1
        to_hit = random.randint(0,x)
        #randHit(enemies, to_hit)
        enemies[to_hit] -= 1
        if enemies[to_hit] == 0:
            enemies.pop(to_hit)
    return

tally = 0
num = 10000
for cthun in range(0,27):
    for n in range(0,num):
        en = [20, 6]
        runCthun(en, cthun)
        if len(en) == 1 or len(en) == 0:
            tally += 1

    avg = tally / num
    tally = 0

    print ("At C'thun of", cthun, ", average is", avg)