from os import system, chdir

if __name__ =="__main__":
    
    chdir("outputs/exp3")
    print("***** Experiment 3 *****")
    
    system("wer -i exp3_one.hyp exp3_one.ref > exp3_one.res")
    system("wer -i exp3_three.hyp exp3_three.ref > exp3_three.res")
    system("wer -i exp3_five.hyp exp3_five.ref > exp3_five.res")
    system("wer -i man_one.hyp man_one.ref > man_one.res")
    system("wer -i man_three.hyp man_three.ref > man_three.res")
    system("wer -i man_five.hyp man_five.ref > man_five.res")
    system("wer -i woman_one.hyp woman_one.ref > woman_one.res")
    system("wer -i woman_three.hyp woman_three.ref > woman_three.res")
    system("wer -i woman_five.hyp woman_five.ref > woman_five.res")

    chdir("../exp4")
    print("***** Experiment 4 *****")

    system("wer -i exp4SNR05DB.hyp exp4SNR05DB.ref > exp4SNR05DB.res")
    system("wer -i exp4SNR15DB.hyp exp4SNR15DB.ref > exp4SNR15DB.res")
    system("wer -i exp4SNR25DB.hyp exp4SNR25DB.ref > exp4SNR25DB.res")
    system("wer -i exp4SNR35DB.hyp exp4SNR35DB.ref > exp4SNR35DB.res")


    print("Done")