# Replaces divire "," in CSV file with "."
import glob

def convertFiles():
    files = glob.glob("import_data/Skoda_Export_*.csv")
    files.reverse()
    ctr = 1
    for file in files:
        f = open(file,'r')
        filedata = f.read()
        f.close()

        newdata = filedata.replace(",",".")

        f = open('import_data/_Skoda_Export_'+str(ctr)+'.csv','w')
        f.write(newdata)
        f.close()
        ctr += 1

if __name__ == "__main__":
    convertFiles()
