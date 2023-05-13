from my_functions import create_ref, decode_file, create_folder, find_files, create_decoder_ngram, create_decoder_digit, write_list_to_file
import re
from os import remove


# Variables - choice of the experiment
''' 
    if experiment is not in [0, 1, 2, 3, 4]
    the script will stop now
    if experiment is equal to 0:
    the script will generate the results for every experiment
    if experiment is equal to 1, 2, 3 or 4:
    the script will run the associated experiment
'''

experiment = 0

if __name__ == '__main__':

    # Check that experiment has a correct value
    assert experiment in range(5), 'Please check the value of the variable experiment\
    \nit has to be in [0, 1, 2, 3, 4]. \nIf you want to run all the experiments\
    choose 0, \nelse choose the number of the wanted experiment.'

    # Experiment 1
    if experiment in [0, 1]:

        # Create folder for the experiment if it does not exist.
        create_folder('outputs/exp1')

        ## Generate ref for experiment 1
        create_ref(1,'SNR35dB', 'man')

        files = find_files('td_corpus_digits/{}/{}'.format('SNR35dB','man'),'*.raw' )
        
        ## Initialize empty files
        ## Name structure is: [Sound level(dB)]_[group]_[decoder].hyp
        for decoder in ['Ngram', 'UnkDigits', 'FixedDigits']:
            with open('outputs/exp1/SNR35dB_man_{}.hyp'.format(decoder), 'w') as f:
                output = ''
                for i, file in enumerate(files):
                    ## Pick the model
                    if decoder == 'Ngram':
                        model = create_decoder_ngram()
                    
                    elif decoder == 'UnkDigits':
                        model = create_decoder_digit('unk_digits')
                    
                    elif decoder == 'FixedDigits':
                        if i < 200:
                            model = create_decoder_digit('digit1')
                        elif i < 300:
                            model = create_decoder_digit('digits3')
                        else:
                            model = create_decoder_digit('digits5')

                    ## Write model ouput            
                    output += '{}\n'.format(decode_file(file, model))

                ## As two different pronounciations can be predicted for
                ## 0 and 1, we remove the suffix _2 from the second variant 
                output = re.sub('_2', '', output)

                ## Replace the remaining '2' by 'two', as '2' is in the dictionary (cf. report):
                output = re.sub('2', 'two', output)

                ## Write output in a file
                f.write(output)
                f.close()

        print('Outputs of experiment 1: Generated.')



    # Experiment 2
    if experiment in [0, 2]:

        # Create folder for the experiment if it does not exist.
        create_folder('outputs/exp2')

        for group in ['boy', 'girl', 'man', 'woman']:

            ##Generate ref for experiment 2
            create_ref(2,'SNR35dB', group)

            ## List of files to analyze
            files = find_files('td_corpus_digits/{}/{}'.format('SNR35dB',group),'*.raw' )

            output = ''
            ## Initialize empty files
            ## Name structure is: [Sound level(dB)]_[group].hyp
            with open('outputs/exp2/SNR35dB_{}.hyp'.format(group), 'w') as f:
                for i, file in enumerate(files):   

                    if i < 200:
                        model = create_decoder_digit('digit1')
                    elif i < 300:
                        model = create_decoder_digit('digits3')
                    else:
                        model = create_decoder_digit('digits5')

                    ## Write model ouput            
                    output += '{}\n'.format(decode_file(file, model))

                ## As two different pronounciations can be predicted for
                ## 0 and 1, we remove the suffix _2 from the second variant 
                output = re.sub('_2', '', output)

                ## Replace the remaining '2' by 'two', as '2' is in the dictionary (cf. report):
                output = re.sub('2', 'two', output)

                ## Write output in a file
                f.write(output)
                f.close()

        print('Outputs of experiment 2: Generated.')

    # Experiment 3
    if experiment in [0,3]:

        # Create folder for the experiment if it does not exist.
        create_folder('outputs/exp3')

        for group in ['man', 'woman']:

            #Generate ref for experiment 3 by group
            create_ref(3,'SNR35dB', group)

            ## List of files to analyze
            files = find_files('td_corpus_digits/{}/{}'.format('SNR35dB',group),'*.raw' )
            output = ''

            ## Initialize empty files
            ## Name structure is: [Sound level(dB)]_[group].hyp
            with open('outputs/exp3/SNR35dB_{}.hyp'.format(group), 'w') as f:
                for i, file in enumerate(files):   

                    if i < 200:
                        model = create_decoder_digit('digit1')
                    elif i < 300:
                        model = create_decoder_digit('digits3')
                    else:
                        model = create_decoder_digit('digits5')

                    ## Write model ouput            
                    output += '{}\n'.format(decode_file(file, model))

                ## As two different pronounciations can be predicted for
                ## 0 and 1, we remove the suffix _2 from the second variant 
                output = re.sub('_2', '', output)

                ## Replace the remaining '2' by 'two', as '2' is in the dictionary (cf. report):
                output = re.sub('2', 'two', output)

                ## Write output in a file
                f.write(output)
                f.close()

        # Generate ref by output length
        ref_content1 = []
        ref_content3 = []
        ref_content5 = []
        for ref in find_files('outputs/exp3', '*.ref'):
            with open(ref, 'r') as f:
                content = f.readlines()
                ref_content1.extend(content[:200])
                ref_content3.extend(content[200:300])
                ref_content5.extend(content[300:])
                f.close()

        # If you rerun the script, it raises an AssertionError, you have to delete 
        #the .ref and .hyp to bypass it.
        assert len(ref_content1) == 400
        assert len(ref_content3) == 200
        assert len(ref_content5) == 200

        # reference file for seqs of 1 digit
        write_list_to_file(ref_content1, 'outputs/exp3/SNR35dB_1digit.ref')

        # reference file for seqs of 3 digits
        write_list_to_file(ref_content3, 'outputs/exp3/SNR35dB_3digits.ref')

        # reference file for seqs of 5 digits
        write_list_to_file(ref_content5, 'outputs/exp3/SNR35dB_5digits.ref')
        

        # Generate hyp by output length
        hyp_content1 = []
        hyp_content3 = []
        hyp_content5 = []
        for hyp in find_files('outputs/exp3', '*.hyp'):
            with open(hyp, 'r') as f:
                content = f.readlines()
                hyp_content1.extend(content[:200])
                hyp_content3.extend(content[200:300])
                hyp_content5.extend(content[300:])
                f.close()

        assert len(hyp_content1) == 400
        assert len(hyp_content3) == 200
        assert len(hyp_content5) == 200

        # reference file for seqs of 1 digit
        write_list_to_file(hyp_content1, 'outputs/exp3/SNR35dB_1digit.hyp')

        # reference file for seqs of 3 digits
        write_list_to_file(hyp_content3, 'outputs/exp3/SNR35dB_3digits.hyp')

        # reference file for seqs of 5 digits
        write_list_to_file(hyp_content5, 'outputs/exp3/SNR35dB_5digits.hyp')

        # delete temporary ref and hyp files: they contains 'man' 
        for file in find_files('outputs/exp3', '*man*'):
            remove(file)
        print('Outputs of experiment 3: Generated.')



    # Experiment 4
    if experiment in [0,4]:

        # Create folder for the experiment if it does not exist.
        create_folder('outputs/exp4')
        
        for dB in ['SNR05dB', 'SNR15dB', 'SNR25dB', 'SNR35dB']:

            #Generate ref for experiment 4
            create_ref(4, dB, 'man')

            ## List of files to analyze
            files = find_files('td_corpus_digits/{}/{}'.format(dB,'man'),'*.raw' )
            output = ''

            ## Initialize empty files
            ## Name structure is: [Sound level(dB)]_[group].hyp
            with open('outputs/exp4/{}_man.hyp'.format(dB), 'w') as f:
                for i, file in enumerate(files):   

                    if i < 200:
                        model = create_decoder_digit('digit1')
                    elif i < 300:
                        model = create_decoder_digit('digits3')
                    else:
                        model = create_decoder_digit('digits5')

                    ## Write model ouput            
                    output += '{}\n'.format(decode_file(file, model))

                ## As two different pronounciations can be predicted for
                ## 0 and 1, we remove the suffix _2 from the second variant 
                output = re.sub('_2', '', output)

                ## Replace the remaining '2' by 'two', as '2' is in the dictionary (cf. report):
                output = re.sub('2', 'two', output)

                ## Write output in a file
                f.write(output)
                f.close()

        print('Outputs of experiment 4: Generated.')




