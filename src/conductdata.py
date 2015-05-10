def GetMostPopularSkillGroup(data = ()) :
    keyseq = data[0]
    keydictory = data[1]
    maxvalue = keydictory[keyseq[0]]
    populargroup = []
    populargroup.append(keyseq[0])
    for i in range(1, len(keyseq)):
        if maxvalue == keydictory[keyseq[i]]:
            populargroup.append(keyseq[i])
    
    return populargroup

def GetMostPopularLanguage(data = ()) :
    languagelist = ['FORTRAN', 'FLOW-MATIC', 'IPL-V', 'COMIT',
               'COBOL', 'JOVIAL', 'GPSS', 'FORMAC',
               'SIMULA', 'PASCAL', 'PROLOG','PYTHON',
               'PERL', 'RUBY','C', 'C++', 'JAVA',
               'SEHLL', 'JAVASCRIPT', 'NUVA', 'RUBY', 
               'VBSCRIPT', 'CSS']
    keyseq = data[0]
    keydirectory = data[1]
    result = []
    maxvalue = 0 
    for i in range(len(keyseq)) :
        if keyseq[i] in languagelist :
            if maxvalue < keydirectory[keyseq[i]] :
                maxvalue = keydirectory[keyseq[i]]
                result.clear()
                result.append(keyseq[i])
            elif maxvalue == keydirectory[keyseq[i]] :
                result.append(keyseq[i])
    
    return result