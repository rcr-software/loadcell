import loadcell_to_csv
import transducer_to_csv
ch1 = loadcell_to_csv.main()
ch2 = transducer_to_csv.main()

# wait for user to end it
input("press enter when finished")
print("have a nice day :)")


ch1.close()
ch1.setOnVoltageRatioChangeHandler(None)
ch2.close()
ch2.setOnVoltageRatioChangeHandler(None)
# save final csv
# must be after tear down, otherwise might different lengths
loadcell_to_csvsave_to_csv('ducer_final')
transducer_to_csv('final')
