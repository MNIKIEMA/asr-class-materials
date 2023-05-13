from os import path, walk
from pocketsphinx import *
from sphinxbase import *
import fnmatch
from my_functions import create_decoder_digits, find_files

if __name__ == "__main__":

	folder_path = "td_corpus_digits/SNR35dB/"
	filehyp_one = open("outputs/exp3/exp3_one.hyp", "w", encoding="utf-8") # Store one digit hypothesis
	filehyp_three = open("outputs/exp3/exp3_three.hyp", "w", encoding="utf-8")
	filehyp_five = open("outputs/exp3/exp3_five.hyp", "w", encoding="utf-8")
	for name in ["man", "woman"]:
		current_folder = f"{folder_path}{name}"
		files = find_files(current_folder,"*.raw")

		for lines, raw_audio in enumerate(files):
			if lines < 200:
				decoder = create_decoder_digits("one")
				decoder.start_utt()
				stream = open(raw_audio, 'rb')
				uttbuf = stream.read(-1)
				if uttbuf:
					decoder.process_raw(uttbuf, False, True)
				else:
					print("Error reading speech data")
					exit()
				decoder.end_utt()
				if decoder.hyp() is None:
					best_hypothesis = ''
				else:
					best_hypothesis = decoder.hyp().hypstr
				filehyp_one.write(best_hypothesis+'\n')
				

			elif lines < 300:
				decoder = create_decoder_digits("three")
				decoder.start_utt()
				stream = open(raw_audio, 'rb')
				uttbuf = stream.read(-1)
				if uttbuf:
					decoder.process_raw(uttbuf, False, True)
				else:
					print("Error reading speech data")
					exit()
				decoder.end_utt()
				if decoder.hyp() is None:
					best_hypothesis = ''
				else:
					best_hypothesis = decoder.hyp().hypstr
				filehyp_three.write(best_hypothesis+'\n')
			else:
				decoder = create_decoder_digits("five")
				decoder.start_utt()
				stream = open(raw_audio, 'rb')
				uttbuf = stream.read(-1)
				if uttbuf:
					decoder.process_raw(uttbuf, False, True)
				else:
					print("Error reading speech data")
					exit()
				decoder.end_utt()
				if decoder.hyp() is None:
					best_hypothesis = ''
				else:
					best_hypothesis = decoder.hyp().hypstr
				filehyp_five.write(best_hypothesis+'\n')


	# Store references files per digit
	man_ref = find_files("td_corpus_digits/SNR35dB/man", "*.ref")
	woman_ref = find_files("td_corpus_digits/SNR35dB/woman", "*.ref")
	file_one_d = open("outputs/exp3/exp3_one.ref", "w")
	file_three_d = open("outputs/exp3/exp3_three.ref", "w")
	file_five_d = open("outputs/exp3/exp3_five.ref", "w")

	for file in [man_ref, woman_ref]:
		current_file = file
		for i, text_file in enumerate(current_file):
			current_text = open(text_file,"r")
			if i < 200:
				for text in current_text:
					file_one_d.write(text)
			elif i < 300:
				#current_text = open(text_file,"r")
				for text in current_text:
					file_three_d.write(text)
			else:
				#current_text = open(text_file,"r")
				for text in current_text:
					file_five_d.write(text)


	file_one_d.close()
	file_three_d.close()
	file_five_d.close()