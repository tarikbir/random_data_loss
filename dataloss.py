import random
import timeit

#Init Settings
random.seed()
loss = int(input("Enter the percentage of corruption: ")) #No error handling, hardcoded.
sep = ',' #Seperator
file_name = "insert_file_name_here" #File name
doRandomCheck = True #If true, checks to not roll the same randoms again. Makes process slower.
doRowCheck = True #If true, corrupts any row just once. Makes process faster.

#Functions
def checkCorruptRow(cor,rR):
    for x, line in enumerate(cor):
        if cor[x][0] == rR:
            return False
    return True
def checkCorrupt(cor,rR,rC):
    for x, line in enumerate(cor):
        if cor[x] == [rR, rC]:
            return False
    return True
#File Operations
tic = timeit.default_timer()
with open(file_name,'r',errors='replace') as inputFile:
    imported = []
    row = 0
    print("Importing file, please wait...")
    for e,l in enumerate(inputFile):
        l=l.replace('\n', '') #Hardcoded to remove any unnecessary lines in a file.
        imported.append(l.split(sep))
        row += 1
    col = len(imported[0])
    print("Columns:", col, "\nRows:", row)
    toc = timeit.default_timer()
    print("File imported in", "{0:.1f}".format(toc-tic), "seconds. Starting corruption operations...")
    corrupt = int(row*loss/100)
    if doRandomCheck: est = (corrupt*(corrupt+1)/2)*(0.0025)/20000 #Estimated time calculation (hardcoded for my computer)
    else: est = corrupt*(0.0032)/1000
    print("Will remove", corrupt, "elements with", loss, "% loss.\nCorruption started, estimated time: ", "{0:.2f}".format(est) ,"seconds (", "{0:.1f}".format(est/60), "minutes ).")
    if doRandomCheck == True: # Makes process much slower but precise
        if doRowCheck == True:
            corrupted = []
            for i in range(1, corrupt):
                isReady = False
                while not isReady:
                    randomColumn = random.randrange(0, col)
                    randomRow = random.randrange(0, row)
                    isReady = checkCorruptRow(corrupted,randomRow)
                corrupted.append([randomRow,randomColumn])
                imported[randomRow][randomColumn] = ''
        else:
            corrupted = []
            for i in range(1, corrupt):
                isReady = False
                while not isReady:
                    randomColumn = random.randrange(0, col)
                    randomRow = random.randrange(0, row)
                    isReady = checkCorrupt(corrupted, randomRow,randomColumn)
                corrupted.append([randomRow, randomColumn])
                imported[randomRow][randomColumn] = ''
    else:
        for i in range(1, corrupt):
            randomColumn = random.randrange(0, col - 1)
            randomRow = random.randrange(0, row)
            imported[randomRow][randomColumn] = ''
    tic = timeit.default_timer()
    print("Corruption completed in", "{0:.1f}".format(tic-toc), "seconds.")
    with open(file_name+"."+str(loss)+"loss", 'w',errors='replace') as outputFile:
        print("Generated output file. Writing...")
        toc = timeit.default_timer()
        for i in imported:
            line = sep.join(i) + '\n'
            outputFile.write(line)
        outputFile.truncate()
        print("Writing completed in ", "{0:.1f}".format(toc-tic), "seconds.")