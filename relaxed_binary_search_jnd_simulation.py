import random
import numpy as np
import matplotlib.pyplot as plt
import math

# playlist initialization
JND_candidate_playlist = np.arange(0, 52, 1) # for VideoSet QP from 0 to 51
print('JND_candidate_playlist: (Note: this playlist must be ordered by quality!')
print(JND_candidate_playlist)

# observer model for simulation
mean_of_jnd = 25
std_of_jnd = 3


def JND_quartile_search(STOP_index, x_n, x_l, x_r, x_c, score):
    """
    implementation of Algo 1 of paper:VideoSet: A large-scale compressed video quality dataset based on JND measurement
    Wang et al. 2017
    :param STOP_index: True or False. True: stop the search; False: continue the search
    :param x_n: JND index
    :param x_l: left boundary of the interval
    :param x_r: right boundary of the interval
    :param x_c: current compared stimulus
    :param score: 1 or 0. 1: perceive difference between x_l and x_c; 0: no difference between x_l and x_c
    :return: x_c, x_r, x_l, x_n, STOP_index
    """
    # INPUT:  current answer from observer , interval [x_l, x_r], current compared stimulus x_c, JND index in x_n
    # score = 1: x_l and x_c have difference

    if score == 1:
        x_n = x_c
        if x_c - x_l <= 1:
            STOP_index = True
        else:
            x_r = math.floor((float(x_l) + 3 * float(x_r)) / 4.0)
            # print('x_r is updated to ' + str(x_r))
            x_c = math.floor((float(x_l) + float(x_r)) / 2.0)
            # print('x_c is updated to ' + str(x_c))
    else:
        if x_r - x_c <= 1:
            STOP_index = True
        else:
            x_l = math.ceil((3 * float(x_l) + float(x_r)) / 4.0)
            # print('x_l is updated to ' + str(x_l))
            x_c = math.ceil((float(x_l) + float(x_r)) / 2)
            # print('x_c is updated to ' + str(x_c))
    return x_c, x_r, x_l, x_n, STOP_index


def subjective_test_simulate(reference:int, distord: int, mu: int, sigma: float) -> int:
    threshold = np.random.normal(loc=mu, scale=sigma)
    if abs(reference - distord) >= threshold:  # todo
        score = 1 # perceive difference
    else:
        score = 0
    return score


def subjective_test_imitate(reference:int, distord:int) -> int:
    print('Do you see the difference between video {} and video {}(QP{})? yes: 1; no: 0. Please Enter:'.format(reference, distord, JND_candidate_playlist[distord]))
    score = input()
    return int(score)



if __name__ == '__main__':

    nb_pvs = len(JND_candidate_playlist) - 1 # qp 0 is the reference

    [x_l, x_r] = [0, nb_pvs]
    ref = x_l  # reference/anchor is best quality video index
    x_c = math.floor((float(x_l) + float(x_r)) / 2.0)
    x_n = x_l  # JND index init with 0, when no JND, x_n = 0
    stop_index = False

    n_1 = 0
    nb_trials = []
    current_stimulus = []
    current_score = []
    while not stop_index:
        n_1 += 1
        # two ways to simulate subjective test: 1. simulate the observer 2. you need to answer the question
        score = subjective_test_simulate(ref, x_c, mu=mean_of_jnd, sigma=std_of_jnd)
        # score = subjective_test_imitate(ref, x_c, )
        print('{} time comparison, video {} and video {}(QP{}) are compared: score = {}'.format(n_1, ref, x_c, JND_candidate_playlist[x_c], score))
        # x_c, x_r, x_l, x_n, stop_index = JND_quartile_search(stop_index, x_n, x_l, x_r, x_c, score)
        nb_trials.append(n_1)
        current_stimulus.append(x_c)
        current_score.append(score)
        plt.plot(nb_trials, current_stimulus, '--', color='grey')
        if score == 1:
            plt.plot(n_1, x_c, 'v', color='C1')

        else:
            plt.plot(n_1, x_c, '^', color='C2')

        x_c, x_r, x_l, x_n, stop_index = JND_quartile_search(stop_index, x_n, x_l, x_r, x_c, score)
        print('next interval[{}, {}]; next compare stimulus: {}(QP{}); current JND = {}(QP{})\n'.format(x_l, x_r, x_c, JND_candidate_playlist[x_c], x_n, JND_candidate_playlist[x_n]))



    # define legend
    plt.plot([], [], 'v', color='C1', label='Yes')
    plt.plot([], [], '^', color='C2', label='No')

    plt.xlabel('Trial Number')
    plt.ylabel('Stimulus Intensity (QP)')
    plt.title('Binary Search Simulation, final JND index is {}'.format(x_n))
    plt.grid(True)
    plt.legend()
    plt.savefig('binary_search_simulation.png')
    plt.show()

    print('Final JND index is {}'.format(x_n))

