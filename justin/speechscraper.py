from bs4 import BeautifulSoup
import requests
import json

JSON = "transcripts.json"

# generates list of URL tails leading to transcripts, returns list of links
def generateLinks():
    r = requests.get('http://millercenter.org/president/speeches')
    soup = BeautifulSoup(r.text, 'lxml')

    links = soup.find_all("a")

    stringy_links = []

    # finds all links with "/president", and isolates the URL tail
    for link in links:
        stringy_link = str(link)
        if "/president" in stringy_link:
            stringy_link = stringy_link[stringy_link.index("/president") : ]
            stringy_link = stringy_link[ : stringy_link.index("\"")]
            stringy_links.append(stringy_link)

    return stringy_links[56: ]

# from a transcript link, isolates the transcript, returns as string
def getTranscript(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'lxml')

    ps = soup.find_all("p")
    
    p_list = []

    for p in ps:
        p_list.append(str(p))

    # cleaning the string
    try:
        p_string = " ".join(p_list)
        p_string = p_string[p_string.index("it was used.</p>") : ]
        p_string = p_string[20 :].replace("<br/>", '')
        p_string = p_string.replace("</p>", '')
        p_string = p_string.replace("<p>", '')
    except:
        pass

    return(p_string)

# from a link, gets president name and speech number
def getPresidentName(link):
    link = link[11 : ]
    link = link[ : link.index("/")]
    return link

# creates a text file for the president, writes the transcripts to the txt file
def writeTranscriptsToFile(president):
    links = generateLinks()
    file_name = president + ".txt"
    with open(file_name, 'w') as file:
        for link in links:
            print(link)
            pres_name = getPresidentName(link)
            if (pres_name == president):
                try:
                    file.write(getTranscript("http://millercenter.org" + link))
                    print(getTranscript("http://millercenter.org" + link))
                except:
                    pass

for i in ["gwbush", "kennedy", "fdroosevelt", "clinton", "reagan", "jackson"]:
    writeTranscriptsToFile(i)

# for sl in stringy_links:
#     sl = sl[ :sl.index("\"")]
#     print(sl)