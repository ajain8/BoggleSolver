# import random
# import copy
# from joblib import Parallel, delayed
# import multiprocessing
# import pathos.multiprocessing as mp

import string
import enchant
import numpy as np
from pytrie import StringTrie as Trie
import re

class Boggle:

    # TODO Add ability to initialize with custom or random boggle board

    def __init__(self, board, width=4, height=4, random=True, prob_arr=None):

        self.width = width
        self.height = height

        if random:
            letters = list(string.ascii_lowercase)
            if prob_arr is None:
                req_letter_prob = {'e':5,'r':10,'s':7, 'o':50,'a':53, 'b':5}
            else:
                req_letter_prob = prob_arr

            # Compute the probability array for alphabets to appear inside the boggle board
            total_req_prob = 0
            count = 0

            for k, v in req_letter_prob.iteritems():
                total_req_prob += v
                count +=1
            total_req_prob += (len(letters) - count)
            prob_arr = [1.0/total_req_prob]*len(letters)

            for k, v in req_letter_prob.iteritems():
                if k in letters:
                    letter_pos = letters.index(k)
                    prob_arr[letter_pos] *= v
            self.__board_state__ = np.random.choice(letters,(height,width),p=prob_arr)
        else:
            t_board_state = np.zeros((width, height)).tolist()
            if len(board) is not (width*height):
                print "Input boggle board does not match provided height and width"
                exit()
            else:
                for i in range(height):
                    for j in range(width):
                        idx = i * width + j
                        t_board_state[i][j] = board[idx]
            self.__board_state__ = t_board_state

        t_alphabet = set()
        for i in range(len(self.__board_state__)):
            for j in range(len(self.__board_state__[0])):
                t_alphabet.add(self.__board_state__[i][j])
        print t_alphabet
        alphabet = ''.join(t_alphabet)
        reg_exp_alphabet = '[^'+alphabet+']'

        self.enchant_dict = enchant.Dict("en_US")

        words = open("words.txt", "r")
        self.trie_dict = Trie()
        count = 1

        try:
            for word in words:
                matchObj = re.match(pattern=reg_exp_alphabet, string=word)
                if matchObj is None:
                    self.trie_dict[word] = count
                    count += 1
            print "Done! " + str(count) + " words loaded in dictionary!\n"
        finally:
            words.close()

    # TODO Add ability to filter words

    def solve_boggle_serial(self):
        self.filter = {'n','h','t'}
        b = self.__board_state__
        potential_words = set()
        for i in range(0, len(b)):
            for j in range(0, len(b[i])):
                visited_list = []
                # print i,j
                # result = self.pool.apply_async(self.find_words(), (i,j), visited_list, potential_words)
                potential_words = potential_words.union(self.find_words(curr_pos=(i,j),visited_list=visited_list, potential_words=potential_words))
                # self.results_arr.append(result.get(timeout=10000))
                # print len(potential_words)
        potential_words_list = list(potential_words)
        potential_words_list.sort(key = len, reverse=True)
        return potential_words_list

    # def solve_boggle_parallel(self):
    #     w = self.width
    #     h = self.height
    #     move_list = []
    #     for i in range(0, h):
    #         for j in range(0, w):
    #             move_list.append((i,j))
    #
    #     num_cores = multiprocessing.cpu_count()
    #     # results = Parallel(n_jobs=num_cores)(delayed(self.find_words_parallel)(i) for i in move_list)
    #     pool = mp.ProcessingPool(4)
    #     potential_words_arr = pool.map(self.find_words_parallel, move_list)
    #     results_union = set().union(*potential_words_arr)
    #     return results_union

    # def find_words_parallel(self, curr_pos):
    #     visited_list = []
    #     potential_words = set()
    #     words = self.find_words(curr_pos, visited_list, potential_words)
    #     print "DONE!"
    #     return words

    def find_words(self, curr_pos, visited_list, potential_words):
        # b = copy.copy(self.__board_state__)
        b = self.__board_state__
        t_word = ''
        if len(visited_list) > 0:
            for pos in visited_list:
                r, c = pos
                t_word += b[r][c]
        r, c = curr_pos
        t_word += b[r][c]
        visited_list.append(curr_pos)
        if self.is_valid_word(t_word):
            potential_words.add(t_word)
        valid_moves = self.get_moves(curr_pos)
        for move in valid_moves:
            t_r, t_c = move
            next_word = t_word + b[t_r][t_c]
            if move not in visited_list and len(self.trie_dict.keys(prefix=next_word)) > 0:
                copied_list = visited_list[:]
                potential_words = potential_words.union(self.find_words(curr_pos=move, visited_list=copied_list, potential_words=potential_words))
                # potential_words.append(self.find_words(curr_pos=move, visited_list=copied_list, potential_words=potential_words))
        return potential_words

    def is_valid_word(self, word):
        if len(word) > 1:
            # if len(self.trie_dict.keys(prefix=word)) > 0:
            if self.enchant_dict.check(word):
                return True
        return False

    def get_moves(self, pos):
        r, c = pos

        directions = [(0, -1), (1, 0),
                      (0, 1), (-1, 0),
                      (-1, -1), (-1, 1),
                      (1, -1), (1, 1)]

        valid_moves = [(r + dr, c + dc) for dr, dc in directions
                       if self.move_is_legal(r + dr, c + dc)]

        return valid_moves

    def move_is_legal(self, row, col):
        return 0 <= row < self.height and \
               0 <= col < self.width

    def print_board(self):
        b = self.__board_state__
        out = ''

        print "Randomly Generated Boggle Board,"
        for i in range(0, len(b)):
            for j in range(0, len(b[i])):
                out +=  b[i][j]
                out += ' | '
            out += '\n\r'

        print out

