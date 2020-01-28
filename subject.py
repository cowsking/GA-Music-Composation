import random
import numpy as np
np.set_printoptions(threshold=np.nan)

DNA_SIZE = 9    # DNA length
DNA_NUM = 64    # Numbers of pitches in a theme
POP_SIZE = 1  # population size
# def encode(N, unit):
#     unit = int(unit)
#     unit_str = str(bin(unit))[2:].zfill(N)
#     unit_list = []
#     for s in unit_str:
#         unit_list.append(s)
#     return unit_list


# def decode(unit_list):
#     l = ll = len(unit_list) - 1
#     c = 0
#     while l >= 0:
#         if unit_list[l] == '1':
#             c +=  pow(2, ll - l)
#         l -= 1
#     return c

# def init_Population(iterations):
#     for numbers in range(iterations):
#         theme = []
#         random.seed()
#         for i in range(64):
#             r_module = random.randint(0,511)
#             theme.append(r_module)
#         population.append(theme)

population = np.random.randint(2, size=(POP_SIZE, DNA_NUM, DNA_SIZE))
#init_Population(1)
# for theme in population:
#     for module in theme:
#         print(encode(9,module))
# for theme in population:
#     for module in theme:
#         print(module)
def translateTheme(theme):
    themeList = []
    cur_length = 0
    cur_pitch = 0
    last_state = ''
    for i, module in enumerate(theme):
        if i == 0:
            if ((module[-2:] == np.array([1,1])).all()):
                cur_pitch = translatePitch(module)
                cur_length = 1
                themeList.append((cur_pitch, cur_length))
                last_state = 'end'
            elif ((module[-2:] == np.array([1,0])).all()):
                cur_pitch = 128
                cur_length = 1
                last_state = 'rest'
            else:
                cur_pitch = translatePitch(module)
                cur_length = 1
                last_state = 'link'
        else:
            if ((module[-2:] == np.array([0,0])).all() or ((module[-2:] == np.array([0,1])).all())):
                if(last_state == 'link'):
                    cur_length += 1
                elif(last_state == 'rest'):
                    themeList.append((cur_pitch, cur_length))
                    cur_pitch = translatePitch(module)
                    cur_length = 1
                    last_state = 'link'
            elif((module[-2:] == np.array([1,0])).all()):
                if(last_state == 'rest'):
                    cur_length += 1
                elif(last_state == 'link'):
                    themeList.append((cur_pitch, cur_length))
                    cur_pitch = 128
                    cur_length = 1
                    last_state = 'rest'
            else:
                cur_pitch = translatePitch(module)
                cur_length = 1
                themeList.append((cur_pitch, cur_length))
                last_state = 'end'
    return themeList


def translatePitch(module):
    return module[:-2].dot(2 ** np.arange(DNA_SIZE-2)[::-1])
def fitness_function(theme):
    def PitchPenalty():
        value = 0
        for i, module in enumerate(theme):
            if (i > 0):
                pitchDifference = abs(translatePitch(module) - translatePitch(theme[i-1]))
                if (pitchDifference > 16):
                    value += pitchDifference ** 2 / 100
        return value
    def NoteLength():
        value = 0





    score = -PitchPenalty()
    return score

for theme in population:
    print(translateTheme(theme))
