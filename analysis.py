from my_functions import find_files, plot_results
import re
import matplotlib.pyplot as plt
import numpy as np
from os import system, chdir

# Variables - choice of the experiment
''' 
    if experiment is not in [0, 1, 2, 3, 4]
    the script will stop now
    if experiment is equal to 0:
    the script will generate the results for every experiment
    if experiment is equal to 1, 2, 3 or 4:
    the script will run the associated experiment
'''




if __name__ == '__main__':
    # Generate res files
    chdir('outputs/exp1')
    system('wer -i SNR35dB_man.ref \
        SNR35dB_man_Ngram.hyp > SNR35dB_man_Ngram.res')
    system('wer -i SNR35dB_man.ref \
        SNR35dB_man_FixedDigits.hyp > SNR35dB_man_FixedDigits.res')
    system('wer -i SNR35dB_man.ref \
        SNR35dB_man_UnkDigits.hyp > SNR35dB_man_UnkDigits.res')
    
    chdir('../exp2')
    system('wer -i SNR35dB_man.ref \
        SNR35dB_man.hyp > SNR35dB_man.res')
    system('wer -i SNR35dB_woman.ref \
        SNR35dB_woman.hyp > SNR35dB_woman.res')
    system('wer -i SNR35dB_girl.ref \
        SNR35dB_girl.hyp > SNR35dB_girl.res')
    system('wer -i SNR35dB_boy.ref \
        SNR35dB_boy.hyp > SNR35dB_boy.res')
   
    chdir('../exp3')
    system('wer -i SNR35dB_1digit.ref \
        SNR35dB_1digit.hyp > SNR35dB_1digit.res')
    system('wer -i SNR35dB_3digits.ref \
        SNR35dB_3digits.hyp > SNR35dB_3digits.res')
    system('wer -i SNR35dB_5digits.ref \
        SNR35dB_5digits.hyp > SNR35dB_5digits.res')
    
    chdir('../exp4')
    system('wer -i SNR35dB_man.ref \
        SNR35dB_man.hyp > SNR35dB_man.res')
    system('wer -i SNR25dB_man.ref \
        SNR25dB_man.hyp > SNR25dB_man.res')
    system('wer -i SNR15dB_man.ref \
        SNR15dB_man.hyp > SNR15dB_man.res')
    system('wer -i SNR05dB_man.ref \
        SNR05dB_man.hyp > SNR05dB_man.res')
    chdir('../..')

    # Find the path of result files.
    x = find_files('outputs/', '*.res')
    
    # Exp 1: 3 results, Exp 2: 4 results, 
    # Exp 3: 2 results, Exp 4: 4 results
    # Total: 14 results

    assert len(x) == 14

    exp1 = []
    exp2 = []
    exp3 = []
    exp4 = []

    for result in x:
        with open(result, 'r') as f:
            if 'exp1' in result:
                content = f.readlines() 
                values = np.array([float(re.split('\s+',line)[2][:-1])
                    for line in content if 'Errors' in line])

                exp1.append(tuple([re.split('[_.]', result)[-2],
                    re.split('\s+',content[-3])[1][:-1], np.mean(values),
                    np.quantile(values, 0.025), np.quantile(values, 0.975)]))

            if 'exp2' in result:
                content = f.readlines()
                values = np.array([float(re.split('\s+',line)[2][:-1]) 
                    for line in content if 'Errors' in line])
                exp2.append(tuple([re.split('[_.]', result)[-2],
                    re.split('\s+',content[-3])[1][:-1], np.mean(values),
                    np.quantile(values, 0.025), np.quantile(values, 0.975)]))

            if 'exp3' in result:
                content = f.readlines()
                values = np.array([float(re.split('\s+',line)[2][:-1])
                    for line in content if 'Errors' in line])
                exp3.append(tuple([re.split('[_.]', result)[-2],
                    re.split('\s+',content[-3])[1][:-1], np.mean(values),
                    np.quantile(values, 0.025), np.quantile(values, 0.975)]))

            if 'exp4' in result:
                content = f.readlines()
                values = np.array([float(re.split('\s+',line)[2][:-1])
                    for line in content if 'Errors' in line])
                exp4.append(tuple([re.split('[/_.]', result)[2],
                    re.split('\s+',content[-3])[1][:-1], np.mean(values),
                    np.quantile(values, 0.025), np.quantile(values, 0.975)]))

    assert len(exp1) == 3
    assert len(exp2) == 4
    assert len(exp3) == 3
    assert len(exp4) == 4



    for i, exp in enumerate([exp1, exp2, exp3, exp4]):
        var = [x[0] for x in exp]
        wer = [float(re.search('\d+\.\d', x[1]).group()) for x in exp]
        mean = np.array([x[2] for x in exp])
        p25 = np.array([x[3] for x in exp])
        p975 = np.array([x[4] for x in exp])


        plot_results(var, wer, mean, p25, p975, 'Value', 'WER (%)',
        'WER for exp #{}'.format(i+1),
        'Exp_{}_WER.png'.format(i+1) )

        
        
        
        








