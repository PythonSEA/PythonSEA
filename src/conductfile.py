'''
In There, I will conduct the data about numbers of companies skill
'''
import os

def ConductFile() :
    filepath = "../doc/Children{0}vInfo.txt"
    count = CountFile("../doc/")
    compslist = []
    datalist = []
    listfile = []
    for i in range(0, count) :
        file = open(filepath.format(i), mode = 'r')
        listfile.append(file)
        
    for i in range(0, count) :
        text = listfile[i].readlines()
        for line in text :
            compslist.append(line)
            
#     for line in text:
#         compslist.append(line)
    for i in range(0, len(compslist)) :
        datalist.append(compslist[i].strip("\n").split("\t"))
        datalist[i].pop()
        #print(datalist[i])
    for i in range(0, count) : 
        listfile[i].close()
        
    return datalist

#count how many file in the directory
def CountFile(dirname):
    count = 0
    for item in os.listdir(dirname) :
        abs_item = os.path.join(dirname, item)
        if os.path.isfile(abs_item) :
            count += 1
            
    return count - 5

def CreateDirectory(minicount = 10) :
    datalist = ConductFile()
    keyseq = []
    keydirectory = {}
    companycount = len(datalist)
    for i in range(0, len(datalist)) :
        for j in range(0, len(datalist[i])) :
            if datalist[i][j] not in  keydirectory :
                keydirectory[datalist[i][j]] = 1
            else :
                keydirectory[datalist[i][j]] = keydirectory[datalist[i][j]] + 1
    keydirectory_list = sorted(keydirectory.items(), key = lambda keydirectory:keydirectory[1], reverse = True)
    keydirectory.clear()
    for i in range(0, len(keydirectory_list)) :
        if keydirectory_list[i][1] < minicount :
            break   
        keyseq.append(keydirectory_list[i][0])
        keydirectory[keydirectory_list[i][0]] = keydirectory_list[i][1]
    
    return (keyseq, keydirectory,companycount)

def CreateDictionary(keyword) :
    datalist = ConductFile()
    sub_dict = {}
    sub_list = []
    count = 0
    minicount = 10
    for line in datalist :
        if keyword in line :
            count += 1
            line.remove(keyword)
            for elem in line :
                if not elem in sub_dict :
                    sub_dict[elem] = 1
                else :
                    sub_dict[elem] += 1
    
    tmp_dict_list = sorted(sub_dict.items(), key = lambda sub_dict:sub_dict[1], reverse = True)
    sub_dict.clear()
    for i in range(0, len(tmp_dict_list)) :
        if tmp_dict_list[i][1] < minicount :
            break   
        sub_list.append(tmp_dict_list[i][0])
        sub_dict[tmp_dict_list[i][0]] = tmp_dict_list[i][1]
        
    return (sub_list , sub_dict , count)
