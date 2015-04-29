import RegulomeDBWebInterface, datetime
from optparse import OptionParser
from math import pow
import os

def importFile(filename, headerLinesToSkip):
    f = open(filename, "r")
    coords=[]
    for i in range(0, headerLinesToSkip):
        next=f.readline()
    #go to first line of data
    next=f.readline()
    while next !="":
        lineData=next.split("\t")
        if len(lineData)>1:
            val=lineData[1]
            if 'e+' in val:
                base, power=val.split('e+')
                val=int(float(base)*pow(10,int(power)))
            else:
                val=int(val)
            coords.append(lineData[0]+'\t'+str(val-1)+'\t'+str(val))
        next=f.readline()
    f.close()
    return coords

def readInAlreadyFinished(outputFile):
    coords=[]
    f=open(outputFile, 'r')
    line=f.readline()
    line=f.readline()
    line=f.readline()
    while line !="":
        vals=line.strip().split("\t")
        if len(vals)>1:
            coords.append(vals[0].replace("chr", "")+"\t"+vals[1])
        line=f.readline()
    f.close()
    return coords

def annotate(inputFile, outputFile, type, numPerRequest):
    if type == 'mutect':
        coords = importFile(inputFile, 2)
    elif type == 'merged':
        coords = importFile(inputFile, 3)
    else: return
    if os.path.exists(outputFile):
        finished = readInAlreadyFinished(outputFile)
        print coords[1:10]
        coords = list(set(coords)-set(finished))
        print coords[1:10]
    else:
        f=open(outputFile, 'w')
        f.writelines(["# RegulomeDB Annotations", str("\n# "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M")+"\n")])
        f.close()
    RegulomeDBWebInterface.getRegulomeDBDataWithList(coords, outputFile, numPerRequest)
        
    
def getOptions():
    parser = OptionParser()
    parser.add_option("--I", dest = "inputFile", help = "",
                      metavar = "FILE", type = "string", default = "/Users/cmelton/Documents/Lab/SnyderLab/Publications/AAA/testRegDBInput.tsv")
    parser.add_option("--T", dest = "type",
                      help = "indicates whether the file is a mutect file or merged", metavar = "FILE", 
                      type = "string", default = "merged")
    parser.add_option("--O", dest = "outputFile",
                      help = "the path to the output file", metavar = "FILE", 
                      type = "string", default = "/Users/cmelton/Documents/Lab/SnyderLab/Publications/AAA/testRegDBInput.RegDB")
    parser.add_option("--N", dest = "numPerRequest",
                      help = "the number of locations to submit to regulome db per POST request", metavar = "FILE", 
                      type = "string", default = "20")
    (options, args) = parser.parse_args()
    return options


def run():
    # get options and defaults
    options = getOptions()
    print options.inputFile
    print options.outputFile
    print options.type
    numPerRequest = int(options.numPerRequest)
    print numPerRequest
    annotate(options.inputFile, options.outputFile, options.type, numPerRequest)
    
# annotate("/home/archana/Documents/SnyderLab/LUSC_Analysis/mutectOnly (2)/0ab8d063-62b4-4d47-82aa-e3351a60029d.call_stats.corrected.out.nonrejected.out", 
#                "out.reg", 'mutect', 2000)
run()

# for i in range(3,229):
#     path="/srv/gsfs0/projects/snyder/collinmelton/"
#     inputPath=path+"AllDBPositions/AllPos_"+str(i)+".merged" 
#     outputPath=path+"AllDBPositionsRegDB/AllPos_"+str(i)+".RegDB"
#     annotate(inputPath, outputPath, "merged", 2000)

# inputPath="/srv/gsfs0/projects/snyder/collinmelton/TCGAWGSResubmission/NewRegDB/allMatchedData.tsv" 
# outputPath="/srv/gsfs0/projects/snyder/collinmelton/TCGAWGSResubmission/NewRegDB/allMatchedData.RegDB"
# inputPath="/Users/cmelton/Documents/Lab/SnyderLab/Publications/TCGAWGSAnalysis/Resubmission/PropensityScoreMatching/allMatchedData.tsv" 
# outputPath="/Users/cmelton/Documents/Lab/SnyderLab/Publications/TCGAWGSAnalysis/Resubmission/PropensityScoreMatching/allMatchedData.RegDB"
# annotate(inputPath, outputPath, "merged", 20)
