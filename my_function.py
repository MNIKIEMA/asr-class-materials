from os import environ, path, walk, mkdir
from pocketsphinx import *
from sphinxbase import *
import fnmatch
import matplotlib.pyplot as plt
import numpy as np


def create_folder(path):
    """Create a folder if it doesn't already exist"""
    if not os.path.isdir(path):
        os.makedirs(path)
    return


def find_files(directory, pattern='*.raw'):
    """Recursively finds all files matching the pattern."""
    files = []
    for root, dirnames, filenames in walk(directory):
        for filename in fnmatch.filter(filenames, pattern):
            files.append(path.join(root, filename))

    # sort the list, to avoid mismatch in the output files
    files = sorted(files)

    return files


def create_decoder_ngram():
    """Create a decoder based on the Ngram language model"""
    config = Decoder.default_config()
    config.set_string('-hmm', 'ps_data/model/en-us')  # acoustic model
    config.set_string('-dict', 'ps_data/lex/turtle.dict')  # lexicon / dictionary
    config.set_string('-lm', 'ps_data/lm/turtle.lm.bin')  # language model
    decoder_ngram = Decoder(config)
    return decoder_ngram


def create_decoder_goforward():
    """Create a decoder based on the goforward custom grammar"""
    config = Decoder.default_config()
    config.set_string('-hmm', 'ps_data/model/en-us')  # acoustic model
    config.set_string('-dict', 'ps_data/lex/turtle.dict')  # lexicon / dictionary
    decoder_gofwd = Decoder(config)

    # Now we use a custom language model
    # Prepare the grammar to be used
    jsgf = Jsgf('ps_data/jsgf/goforward.jsgf')  # load the grammar file
    rule = jsgf.get_rule('goforward.move2')  # choose the rule
    fsg = jsgf.build_fsg(rule, decoder_gofwd.get_logmath(), 7.5)  # build the grammar rule
    fsg.writefile('outputs/goforward.fsg')  # write the compiled grammar rule as an external file

    # Now set the fsg grammar rule in the decoder
    decoder_gofwd.set_fsg("outputs/goforward", fsg)  # load the pre-recorded compiled grammar rule in the decoder
    decoder_gofwd.set_search("outputs/goforward")  # and set it as the grammar to use

    return decoder_gofwd

def create_decoder_digit(rule):
    """Create a decoder based on the goforward custom grammar"""
    config = Decoder.default_config()
    config.set_string('-hmm', 'ps_data/model/en-us')  # acoustic model
    config.set_string('-dict', 'ps_data/lex/digits.dict')  # lexicon / dictionary
    decoder_digits = Decoder(config)

    # Now we use a custom language model
    # Prepare the grammar to be used

    jsgf = Jsgf('ps_data/jsgf/digits.jsgf')  # load the grammar file
    rule = jsgf.get_rule('digits.{}'.format(rule))  # choose the rule
    fsg = jsgf.build_fsg(rule, decoder_digits.get_logmath(), 7.5)  # build the grammar rule
    fsg.writefile('outputs/digits.fsg')  # write the compiled grammar rule as an external file

    # Now set the fsg grammar rule in the decoder
    decoder_digits.set_fsg("outputs/digits", fsg)  # load the pre-recorded compiled grammar rule in the decoder
    decoder_digits.set_search("outputs/digits")  # and set it as the grammar to use

    return decoder_digits

def decode_file(file_path, decoder):
    '''Decode the content of an audio file'''

    # Start the decoder
    decoder.start_utt()

    # Open the file to decode
    stream = open(file_path, 'rb')
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
    print('Best hypothesis: ', best_hypothesis)
          #"\n model score: ", decoder.hyp().best_score,
          #"\n confidence: ", decoder.get_logmath().exp(decoder.hyp().prob))
    #bh=  ' '.join([seg.word for seg in decoder.seg()])
    #print('Best hypothesis segments: ', bh)
    return best_hypothesis

def create_ref(exp, db, group, partial = False):
    '''Parse content of ref files and 
    write it on a new file which will be our reference file '''
    
    # Store the name of the reference files
    x = find_files('td_corpus_digits/{}/{}'.format(db,group),'*.ref' )

    # Create a new file which contains the content of all the files 
    with open('outputs/exp{}/{}_{}.ref'.format(exp,db,group), 'w') as f:
        for name in x:
            with open(name, 'r') as o:
                f.write(o.read())


def write_list_to_file(l:list, filename:str):
    '''write the content of a list in a file,
    each element of the list is written in a new line'''
    with open(filename, 'w') as f:
        for x in l:
            f.write(x)
        f.close()
    return

def plot_results(abs, ord, mean, p25, p975,
    xlabel, ylabel, title, picture_name, display = False):

    '''plot WER '''

    plt.clf()
    plt.scatter(abs, ord)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.ylim(0,)
    plt.title(title)
    plt.errorbar(abs,ord, yerr = [mean - p25, p975 - mean],
        linestyle='')
    for j in range(len(abs)):
        plt.annotate(str(ord[j]), xy=(abs[j], ord[j]))
    if display:
        plt.show()
    plt.savefig(picture_name)

    return 

# EOF
