from my_functions import create_decoder_digits, find_files
import os



# print('************!!!!!!!!!!!!!', test_folder(""))

# create_folder("test")
for folder in ["td_corpus_digits/SNR35dB/man", "td_corpus_digits/SNR35dB/woman"]:
   audio_data = find_files(folder)
   references = find_files(folder, "*.ref")
   hyp_file1, hyp_file3, hyp_file5 = [open(f"outputs/exp3/{folder[25:]}_{number}.hyp","w",encoding="utf-8") \
      for number in ["one", "three", "five"]]
   ref_files1, ref_files3, ref_files5 = [open(f"outputs/exp3/{folder[25:]}_{number}.ref","w", encoding="utf-8")\
       for number in ["one", "three", "five"]]
   for i, (raw_audio, ref) in enumerate(zip(audio_data, references)):
      f = open(ref, "r", encoding="utf-8")
      if i < 200:
         decoder = create_decoder_digits("one")
         for text in f:
            ref_files1.write(text)
         decoder.start_utt()
      # Open the file to decode
         stream = open(raw_audio, 'rb')
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
         hyp_file1.write(best_hypothesis+'\n')  # use the custom grammar
      elif  i < 300:
         decoder = create_decoder_digits("three")
         for text in f:
            ref_files3.write(text)
         decoder.start_utt()
      # Open the file to decode
         stream = open(raw_audio, 'rb')
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
         hyp_file3.write(best_hypothesis+'\n') 
      else:
         decoder = create_decoder_digits("five")
         for text in f:
            ref_files5.write(text)
      # Start the decoder
         decoder.start_utt()
         # Open the file to decode
         stream = open(raw_audio, 'rb')
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
         hyp_file5.write(best_hypothesis+'\n') 
                           
# Process files