with open(UFile, "r") as targetFile:
        lines = targetFile.readlines()

    #rawData = [];
    #for line in lines :
    #    rawData.append(line.strip().split());
    #print(rawData)


    badChars = [ '(', ')' ];

    rawList=[];
    for line in lines:
        rawList.append(line.strip().replace('(','').replace(')','').split());

    #print('-----')
    #print(rawList)
    #print("Size of rawList[-1]=",len(rawList[-1]))

    nProbes = int(round((len(rawList[-1])-1)/3))
    #print("nPro