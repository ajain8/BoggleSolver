from Boggle import Boggle
import timeit

# from pytrie import StringTrie as Trie
#
# trie_dict = Trie()
# count = 1
# words = open("words.txt", "r")
#
# for word in words:
#     word = word[:-1]
#     trie_dict[word] = count
#     count += 1
#     if count > 5000:
#         break
#
# print "Done! All words loaded in dictionary!"
#
# print trie_dict.keys(prefix='aam')



custom_board = 'rndcadlsrinttoew'
test_bog = Boggle(custom_board, width=4, height=4, random=False, prob_arr=None)
test_bog.print_board()


start = timeit.default_timer()
final_words = test_bog.solve_boggle_serial()
for word in final_words:
    print word
specialized_words =set()
for word in final_words:
    for i in test_bog.filter:
        if i in word:
            specialized_words.add(word)
# print specialized_words
print "\nSPECIALIZED WORDS,"
high_val_words = list(specialized_words)
high_val_words.sort(key = len, reverse=True)
for word in high_val_words:
    print word

print "WORDS FOUND: "+str(len(final_words))
stop = timeit.default_timer()
print "TIME TAKEN: "+str(stop - start)+"s"


# start = timeit.default_timer()
# final_words = test_bog.solve_boggle_parallel()
# print final_words
# print "LENGTH: "+str(len(final_words))
# stop = timeit.default_timer()
# print stop - start
