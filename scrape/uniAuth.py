# coding: utf-8
import math
import re
import urllib.request
import urllib
from bs4 import BeautifulSoup
from scrape import authorExtractM
# import authorExtractM
# import pymongo

academia_titles = {'Dr', 'Mr', 'Mrs', 'Miss', 'Ms', 'PhD'}
academia_degrees = {'PhD', 'MS', 'MAcc', 'MA', 'MAE', 'MFA', 'AuD', 'MAS', 'MBA', 'MEd', 'ME', 'MCS', 'EdS', 'MDATA', 'MDA', 'EdD', 'MFP', 'MFSQ', 'MPH', 'MPSH', 'MHDFS', 'MHR', 'MHR', 'MLA', 'MMIS', 'MMFT', 'MTC', 'MMath', 'MM', 'MNR', 'MRC', 'MSLT', 'MSW', 'DVM', 'Licenure', 'Cert', 'Endorsement', 'BS', 'BA', 'AAS', 'BFA', 'CC', 'AB', 'CNA', 'CP', 'Apprenticeship', 'CP', 'BID', 'BLA', 'BM', 'BSN'}
academia_ranks = {'Lecturer', 'Assistant' , 'Associate', 'Professor', 'Teaching Assistant', 'Senior Teaching Assistant', 'Professeur', 'Maître de Conférences', 'Classe A', 'Classe B', 'Maître Assistant', 'Level A', 'Level B', 'Level C', 'Level D', 'Level E', 'Profesor Titular Plenario', 'Profesor Titular', 'Profesor Asociado', 'Profesor Adjunto', 'Profesor', 'Instructor', 'Associate Lecturer', 'Lecturer', 'Senior Lecturer', 'Professor emeritus', 'Demonstrator', 'Universitätsprofessor', 'Hochschuldozent', 'Juniorprofessor', 'Prafiesar', 'Прафесар', 'Dacent', 'Дацэнт', 'Starejshy vykladchyk', 'Старэйшы выкладчык', 'Asistent', 'Vykladchyk', 'Асістэнт', 'Выкладчык', 'rector', 'Rektar', 'Рэктар', 'Prarektar', 'Прарэктар', 'vice-rector', 'Dekan Fakultetа', 'Дэкан факультэта', 'dean', 'Namiesnik dekana', 'Намеснік дэкана', 'vice-dean', 'head', 'Zahadchyk kafiedry', 'Загадчык кафедры', 'Gewoon hoogleraar', 'Deeltijds gewoon hoogleraar', 'Hoogleraar', 'Hoofddocent', 'Docent', 'Docent-assistent', 'Assistent', 'Aspirant', 'Vice-Rector', 'Decaan', 'Professeur', 'Chargé de cours invité', 'Chargé de cours définitif', 'Chargé de cours temporaire', 'Maître de conférences', 'Directeur de recherche', 'Chef de travaux agrégé', 'Maître de recherche','Chef de travaux', 'Chercheur qualifié', 'Premier assistant', "Maître d'enseignement", 'Chargé de recherche', 'Assistant de recherche', 'Recteur', 'Doyen', "Président d'institut", 'Vice-Doyen', 'Président de département', 'Asistent', 'Viši Asistent',  'Docent', 'Vanredni profesor', 'Pofesor', 'Rektor', 'Prorektor', 'Dekan', 'Prodekan', 'Šef katedre', 'Асистент', 'Главен Асистент', 'Доцент', 'Професор', 'Scientist', 'habilitation', 'Secretary general', 'Academic', 'chairman', 'Research', 'Chairman', 'Senior', 'sénior', 'Fellow', 'Principal', 'Investigator', 'supervisor', 'research', '正教授', '副教授', '讲师', '助教' 'Rektor', 'Pročelnik', 'Predstojnik', 'OSTADH', 'OSTADH MOTAFAREGH', 'OSTADH  MOSAED', 'MODARRES', "MOA'ED", 'Emeriitprofessor', 'Õpetaja', 'tohtorikoulutettava', 'tutkija', 'Post-doctorant', 'Post-doc', 'doc', 'Post-doctorate', 'Universitätsprofessor', 'Deputy', 'Pro', 'Tutor', 'Laboratory', 'Peneliti', 'Asisten Ahli', 'Lektor', 'Guru', 'Wakil', 'Professore', 'Prof', 'Dekāns', 'Dekāne', 'Chancellor', 'Lab', 'Engineer', 'Profesör' 'Doçent', 'Öğretim Görevlisi', 'Okutman', 'Araştırma Görevlisi', 'Rektör', 'Bölüm Başkanı', 'Yüksekokul Müdürü', 'Ana Bilim Dalı Başkanı', 'Ana Bilim Dalı Başkanı', 'Dekan Yardımcısı', 'Enstitü müdürü', 'Fakülte Dekanı', 'Rektör Yardımcısı', 'Chair'}
academic_departments = ['department', 'campus', 'biorenewable', 'administration', 'honors', 'chemical', 'nutrition', 'departments,', 'philosophy', 'history', 'reality', 'microelectronics', 'youtube', 'units\t\t', 'facebook', 'coaching', 'programs', 'social', 'natural', 'academic', 'industrial', 'soil', 'graphic', 'political', 'reserved', 'culinary', 'copyright', 'software', 'resources', 'events', 'development', 'mathematics', 'second', 'accounting', 'programs\n', 'graduate', 'army', 'precollegiate', 'program', 'leadership', 'women', 'training', 'civil', 'communication,', 'finance', 'illustration', 'plant', 'genetics,', 'library', 'statistics', 'chemistry', 'contact@iastate.edu', 'sociology', 'pre-health', 'institutes', 'languages', 'manufacturing', 'interior', 'clinical', 'centers', 'services', 'regional', 'performing', 'family', 'language/applied', 'educational', 'materials', 'physics', 'media', 'developmental', 'gifted', 'human', 'biochem,', 'apparel,', 'planning', 'master', 'transportation,', 'agriculture', 'instagram', 'textiles', 'institute', 'business', 'architecture', 'resource', 'design', 'directory', 'evolution', 'laboratory', 'office', 'entrepreneurial', 'music\xa0', 'molecular', 'education,', 'theatre', 'organismal', 'marketing', 'force', 'sustainable', 'computational', 'clothing', 'linguistics', 'russian', 'economics', 'electrical', 'technology', 'biology', 'school', 'dance', 'systems,', 'quality', 'liberal', 'teacher', 'hospitality', 'access', 'chain', 'management', 'dietetics', 'agronomy', 'data', 'science', 'earth', 'health', 'ecology', 'aerospace', 'interdepartmental', 'evaluation', 'neuroscience', 'naval', 'production', 'microbiology', 'food', 'veterinary', 'faculty', 'anthropology', 'biomedical', 'footer', 'life', 'arts', 'computer', 'information', 'university', 'preparation', 'meteorology', 'landscape', 'horticulture', 'construction', 'digital', 'professions', 'entomology', 'supply', 'navy', 'american', 'civil,', 'education', "women's", 'agricultural', 'bioinformatics', 'research', 'curriculum', 'technical', 'astronomy', 'contacts', 'exercise', 'rotc:\xa0', 'studio', 'extension', 'phone', 'rights', 'senate', '\n', 'physiology', 'engineering', 'english', 'studies', 'distance', 'virtual', 'provost', 'immunobiology', 'higher', 'biological/pre-medical', 'physical', 'gerontology', 'degree', 'greenlee', 'evolutionary', 'world', 'consumer', 'facility', 'journalism', '\nschools\n', 'nursing', 'african', 'sciences', 'mechanical', '\niowa', 'privacy', 'advertising', 'non-discrimination', 'biotechnology,', 'language', 'biosystems', 'diagnostic', 'cultures', 'preventive', 'undergraduate', 'pathology', 'policy', 'kinesiology', 'foreign', 'military', 'systems', 'integrated', 'geology', 'toxicology', 'units', 'teaching', 'communication', 'agriculture,', 'communications', 'cell', 'iowa', 'accessibility', 'medicine', 'botany', 'biophysics', 'center', 'international', 'instrumentation', 'talented', 'psychology', 'cellular', 'sponsored', 'applied', 'u.s.', 'applications', 'music\xa0&', 'speech', 'opptag', 'biological', 'ecology,', 'state', 'animal', 'major', 'twitter', 'public', 'bioethics', 'operations', 'instruction', 'latino/a', 'community', 'environmental', 'athletic', 'religious', '\nacademic', 'forestry', 'administrative', 'interdisciplinary', 'molecular,']
academia_titles = [x.lower() for x in academia_titles]
academia_degrees = [x.lower() for x in academia_degrees]
academia_ranks = [x.lower() for x in academia_ranks]
academic_departments.remove('degree')
academic_departments = [x.lower() for x in academic_departments]

# myclient = pymongo.MongoClient("localhost", 27017)
# mydb = myclient["Fyp"]
# uniUrl = mydb["universities"]
#loading and matching dict
def load_words():
    with open("./English_words.txt") as word_file:
        valid_words = set(word_file.read().split())

    return valid_words

def PK_cities():
    with open("./PK.txt") as word_file:
#         print(word_file.read().split())
#         valid_words = set(word_file.read().split())
        valid_words = word_file.read().split()

    return valid_words
# if __name__ == '__main__':
#
# # print('contact' in english_words)


def onlystringcheck(s):
    ans = False
    for i in s:
        if re.match('[A-Za-z]', i):
            ans = True
            break
    return ans

def getAuthInfoLink(url, name, advanced = False):
    print(url)
    print(name)

    unidata = {'url': '', 'faculty': []}
    unidata['url']=str(url)

    # find = uniUrl.find_one({'url':str(url)},{'url':1,'faculty':0})
    # if(find):
    #     title = uniUrl.find_one({})
    #     for i in finalreqlist:
    #         if finalseqlist[finalreqlist.index(i)] == 'title':
    #             # print(finalseqlist[finalreqlist.index(i)]+ '   '+i)
    #             authorExtractM.getAuthInfoLink(str(i), name)

    returnData = {
        'url': url,
        'name': name,
        'message': 'done crawling'
    }
    english_words = load_words()
    sequence = []
    real_seq = []
    temp_seq = []
    seqcount = 0
    titlecount = 0
    degreecount = 0
    rankcount = 0
    departmentcount = 0
    requirement = []  # same length with sequence[]
    templist = []
    savecount = 0
    finalseqlist = []
    finalreqlist = []

    #getting uni page source
    print('Crawling url, time taken is proportional to the length of the page.')
    try:
        html=urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        content = e.read()
        # print(content)
        returnData = {
            'url': url,
            'name': name,
            'message': 'broken url'
        }
        print(returnData)
    soup = BeautifulSoup(html,'lxml')
    d=soup.body.findAll(text=True)

    #filtering text
    slashprob = r'\\'
    forwardslah = '/'
    backwardslash = slashprob[0]
    j=[]
    for ll in d:
    #     if forwardslah in ll or backwardslash in ll:
    #         d.remove(ll)
        if ll == '\n':
            d.remove('\n')

    # print(d)

    for i in d[::-1]:
        #     print('\n')
        if len(i) > 300 or not onlystringcheck(
                i) or i == '' or i == '\n' or '/' in i or r'\\' in i or '"' in i or '|' in i or ":" in i or 'jQuery' in i or 'script' in i or 'function()' in i or '>' in i or '<' in i:
            continue

        if re.search(('dr'), i.lower()) or re.search(('mr'), i.lower()) or re.search(('mrs'), i.lower()) or re.search(
                ('miss'), i.lower()):
            sequence.append('title')
            requirement.append(i)
            finalseqlist.append(sequence[len(sequence) - 1])
            finalreqlist.append(requirement[len(sequence) - 1])

        else:
            for j in academia_degrees:
                if j in i.split():
                    #             if re.search(str(j), i.lower()) and j not in templist:
                    degreecount += 1
                    templist.append(j)
            templist = []
            for j in academia_ranks:
                if re.search(str(j), i.lower()) and j not in templist:
                    rankcount += 1
                    templist.append(j)
            templist = []
            for j in academic_departments:
                if re.search(str(j), i.lower()) and j not in templist:
                    departmentcount += 1
            templist = []
            for j in academia_titles:
                tempi = i
                newtitle = ''
                newabout = ''
                bracketcounterstart = 0
                bracketcounterend = 0

                if '(' in tempi and ')' in tempi:
                    for bracketstart in tempi:
                        bracketcounterstart += 1
                        if bracketstart == '(':
                            break
                    for bracketend in tempi[::-1]:
                        bracketcounterend += 1
                        if bracketend == ')':
                            break
                    newtitle = tempi[:bracketcounterstart - 1:1] + tempi[len(tempi) - bracketcounterend + 1::1]
                    newabout = tempi[bracketcounterstart:len(tempi) - bracketcounterend:1]
                elif '(' in tempi and ')' not in tempi:
                    for bracketstart in tempi:
                        bracketcounterstart += 1
                        if bracketstart == '(':
                            break
                    newtitle = tempi[:bracketcounterstart - 1:1]
                    newabout = tempi[bracketcounterstart::1]
                elif ')' in tempi and '(' not in tempi:
                    for bracketend in tempi:
                        bracketcounterend += 1
                        if bracketend == ')':
                            break
                    newtitle = tempi[:bracketcounterend - 1:1]
                    newabout = tempi[bracketcounterend::1]

                if bracketcounterstart > 0 or bracketcounterend > 0:
                    for j in academia_degrees:
                        if j in newabout.split():
                            if degreecount > 0:
                                degreecount -= 1
                    for j in academia_ranks:
                        if re.search(str(j), i.lower()) and j not in templist:
                            if rankcount > 0:
                                rankcount -= 1
                    for j in academic_departments:
                        if re.search(str(j), i.lower()) and j not in templist:
                            if departmentcount > 0:
                                departmentcount -= 1

                if re.search(str(j), newtitle.lower()) and j not in templist:
                    titlecount += 1
                    templist.append(j)

                bracketcounterend = 0
                bracketcounterstart = 0
            templist = []

            #         print('word is '+i)
            #         print(titlecount)
            #         print(rankcount)
            #         print(departmentcount)
            #         print(degreecount)
            cont = False
            if degreecount == titlecount == rankcount == departmentcount == 0:
                for j in i.split('-'):
                    if j.lower() in english_words:
                        #                 print(j.lower() in english_words)
                        cont = True
                        break
            #         for j in i.split(' '):
            #             if j.lower() in english_words:
            #                 print(j.lower() in english_words)
            #                 cont = True
            #                 break
            if cont:
                continue

            max = departmentcount
            if titlecount > max:
                max = titlecount
            elif degreecount > max:
                max = degreecount
            elif rankcount > max:
                max = rankcount
            else:
                pass

            if max == degreecount and max == titlecount and max == rankcount and max == departmentcount:
                sequence.append('title')
                requirement.append(i)
            elif max == titlecount and max == degreecount and max == rankcount:
                sequence.append('title')
                requirement.append(i)
            elif max == titlecount and max == degreecount and max == departmentcount:
                sequence.append('title')
                requirement.append(i)
            elif max == titlecount and max == rankcount and max == departmentcount:
                sequence.append('title')
                requirement.append(i)
            elif max == departmentcount and max == degreecount and max == rankcount:
                sequence.append('about')
                requirement.append(i)
            elif max == titlecount and max == degreecount:
                sequence.append('title')
                requirement.append(i)
            elif max == titlecount and max == rankcount:
                sequence.append('title')
                requirement.append(i)
            elif max == titlecount and max == departmentcount:
                sequence.append('title')
                requirement.append(i)
            elif max == degreecount:
                sequence.append('about')
                requirement.append(i)
            elif max == rankcount:
                sequence.append('about')
                requirement.append(i)
            elif max == departmentcount:
                sequence.append('about')
                requirement.append(i)
            else:
                sequence.append('title')
                requirement.append(i)

            finalseqlist.append(sequence[len(sequence) - 1])
            finalreqlist.append(requirement[len(sequence) - 1])
            seqcount += 1
            if seqcount > 4:
                if sequence[len(sequence) - 1] == sequence[len(sequence) - 2] == sequence[len(sequence) - 3] == sequence[
                    len(sequence) - 4] == 'about':
                    #                 print(sequence[len(sequence)-4])
                    #                 print(requirement[len(sequence)-4])
                    sequence.remove(sequence[len(sequence) - 4])
                    #             finalseqlist.remove(sequence[len(sequence)-4])
                    #             finalreqlist.remove(requirement[len(sequence)-4])
                    requirement.remove(requirement[len(sequence) - 4])
                    seqcount -= 1
                if sequence[len(sequence) - 1] == sequence[len(sequence) - 2] == sequence[len(sequence) - 3] == sequence[
                    len(sequence) - 4] == 'title':
                    #                 print(sequence[len(sequence)-4])
                    #                 print(requirement[len(sequence)-4])
                    sequence.remove(sequence[len(sequence) - 4])
                    #             finalseqlist.remove(sequence[len(sequence)-4])
                    #             finalreqlist.remove(requirement[len(sequence)-4])
                    requirement.remove(requirement[len(sequence) - 4])
                    seqcount -= 1

        #     print(sequence)
        # #     print(len(sequence))
        #     print(requirement)
        # #     print(requirement.index(i))

        departmentcount = rankcount = degreecount = titlecount = 0
    finallength = len(finalseqlist)
    finalseqlist = finalseqlist[:finallength - 90:1]
    finalreqlist = finalreqlist[:finallength - 90:1]
    
    for indx, ii in enumerate(finalreqlist):
        if "\\" in r"%r" % ii:
            newName = ""
            skipChar = False
            for i in r"%r" % ii:
                if i == "\\":
                    skipChar = True
                if skipChar == False:
                    if i != "'":
                        newName += i
                if i != "\\":
                    skipChar = False
            finalreqlist[indx] = newName

    for indx, ii in enumerate(finalreqlist):
        if " " in ii:
            newName = ''
            skipChar = False
            lastChar = ''
            for i in ii:
                if i == " " and i == ii[0]:
                    continue
                if skipChar == False:
                    if i != "'":
                        newName += i
                else:
                    if lastChar == " " and i != " ":
                        if i != "'":
                            newName += i
                if i == " ":
                    skipChar = True
                else:
                    skipChar = False
                lastChar = i
            finalreqlist[indx] = newName

    print(finalreqlist)



    # cities = PK_cities()
    # # wrongWords = missLeadingNames()
    # for idx, i in enumerate(finalreqlist):
    #     if idx < 8540:
    #         continue
    #     # if finalseqlist[finalreqlist.index(i)] == 'title':
    #     if finalseqlist[idx] == 'title':
    #         #print(finalseqlist[finalreqlist.index(i)]+ '   '+i)
    #         if '"'+str(i)+'",' not in cities:
    #             if 'Dr' in str(i):
    #                 # print("trying for: {}".format(str(i)[str(i).index('Dr')+len('Dr')+1::]))
    #                 authorExtractM.getAuthInfoLink(str(i)[str(i).index('Dr')+len('Dr')+1::], name)
    #             else:
    #                 print("trying for: {}".format(str(i)))
    #                 authorExtractM.getAuthInfoLink(str(i), name)
    

    # if advanced:
    #     for i in finalreqlist:
    #         if finalseqlist[finalreqlist.index(i)] == 'title':
    #             pass
    # authorExtractM.closeBrowserInstances()

    return returnData
    
    # tempnewlist = ['muhammad imran']
    # for i in tempnewlist:
    #     authorExtractM.getAuthInfoLink(str(i), 'name')

# authorExtractM.getAuthInfoLink('muhammad imran', 'comsats')