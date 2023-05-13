from os import environ, path, walk
from pocketsphinx import *
from sphinxbase import *
import fnmatch

from my_functions import create_decoder_ngram, create_decoder_goforward, create_decoder_digits, find_files

folder_path = "td_corpus_digits/SNR35dB/man/seq3digits_100_files/"

decoder_type = ""
decoder = ""
def create_decoder(decoder_type):
	decoder = ""
	if decoder_type == "n-gram":
		decoder = create_decoder_ngram()

	if decoder_type == "unk":
		decoder = create_decoder_digits()

	decoder = create_decoder_digits(decoder_type)

	return decoder

fs = find_files(folder_path)
ref_files = find_files(folder_path, pattern = "*.ref")
decoder = create_decoder("three")

# Start the decoder
decoder.start_utt()

data_hyp_file = open("./outputs/data.hyp", "w")

# run the next lines just one time, to create the data file 
# with the refs
"""
data_ref_file = open("./outputs/data.ref", "w")

for f in ref_files:
	file = open(f, 'r')
	for l in file:
		print("fffffffffffffffffff:", l)
		data_ref_file.write(l)
"""

for f in fs:
	decoder = create_decoder("n-gram")

	# Start the decoder
	decoder.start_utt()
	print(f)
	stream = open(f, 'rb')
	uttbuf = stream.read(-1)

	# Process the file with the decoder
	if uttbuf:
	    decoder.process_raw(uttbuf, False, True)
	else:
	    print("Error reading speech data")
	    exit()
	decoder.end_utt()

	# test for empty hypothesis and replace the output with an empty string if needed
	if decoder.hyp() is None:
	    best_hypothesis = ''
	else:
	    best_hypothesis = decoder.hyp().hypstr

	# Print the results
	print('Best hypothesis: ', best_hypothesis,
	      "\n model score: ", decoder.hyp().best_score,
	      "\n confidence: ", decoder.get_logmath().exp(decoder.hyp().prob))

	# write best hypothesis to a file
	data_hyp_file.write(best_hypothesis+'\n')


	print('Best hypothesis segments: ', [seg.word for seg in decoder.seg()])

	# Access N best decodings
	N = 8
	print('Best ' + str(N) + ' hypothesis: ')
	for best, i in zip(decoder.nbest(), range(N)):
	    print(best.hypstr, best.score)