from os import path, walk
from pocketsphinx import *
from sphinxbase import *
import fnmatch
from my_functions import create_decoder_digits, find_files

if __name__ == "__main__":

    # Extract files from folder
    files = ['td_corpus_digits/SNR05dB/man', 
    'td_corpus_digits/SNR15dB/man', 'td_corpus_digits/SNR25dB/man',
    'td_corpus_digits/SNR35dB/man']
    for file_path in files:
        filehyp = open(f"outputs/exp4/exp4{file_path[17:24]}.hyp", "w")
        i = 0
        audio_file = find_files(file_path)
        for raw_file in audio_file:
            i += 1
            if i < 200:
                decoder = create_decoder_digits("one")
            elif i < 300:
                decoder = create_decoder_digits("three")
            else:
                decoder = create_decoder_digits("five")
            decoder.start_utt()
            stream = open(raw_file, 'rb')
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
            filehyp.write(best_hypothesis+'\n')
    for file_path in files:
        file_ref = open(f"outputs/exp4/exp4{file_path[17:24]}.ref", "w")
        ref_files = find_files(file_path, "*.ref")
        for ref_file in ref_files:
            tmp_ref = open(ref_file, 'r')
            for text in tmp_ref:
                file_ref.write(text)
        

