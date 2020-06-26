import json
import xmltodict
import os
rootdir = 'D:\datasets\HindawiArticles\\2008'
from pymongo import MongoClient
from pymongo.errors import *

def formArticleBody(body):
    sections=[]
    for section in body['sec']:
        i=0
        single_section={}
        single_section['title']=section['title']
        single_section['content'] = ''
        if 'p' in section:
            for para in section['p']:
                if(isinstance(para,str)):
                    single_section['content'] += para
                    single_section['content'] += '\n'
                else:
                    if('sec' in para):
                        print("subsectioni")
                        for subsection in para['sec']:
                            for subpara in subsection['p']:
                                single_section['content'] += subpara['#text']
                                single_section['content'] +='\n' 
                    if '#text' in para:
                        single_section['content'] += para['#text']
                        single_section['content'] +='\n'
        if 'sec' in section:
            for subsec in section['sec']:
                if 'p' in subsec:
                    for subpara2 in subsec['p']:
                        if(isinstance(subpara2,str)):
                            single_section['content'] += subpara2
                            single_section['content'] +='\n'
                        else:
                            if '#text' in subpara2:
                                single_section['content'] += subpara2['#text']
                        
        filename = "section"+str(i)+".json"
        with open(filename,'w')as output_section_file:
            output_section_file.write(json.dumps(section))
        sections.append(single_section)
        i+=1
    return sections
  

with open('D:\\datasets\\HindawiArticles\\2008\\HINDAWI.AAA\\531361-2008-02-24.xml') as xml_file:
            # print(article['body']['sec'][2])
            # exit()
    
    data_dict = xmltodict.parse(xml_file.read())
    json_data = json.dumps(data_dict)
    article = data_dict["article"]
    with open('article.json','w')as article_out_file:
        article_out_file.write(json.dumps(article))
    front = article["front"]
    journalMeta = {"id": front["journal-meta"]["journal-id"]["#text"],
    "title": front["journal-meta"]["journal-title-group"]["journal-title"],
    "issn": {"epub": front["journal-meta"]["issn"][0]["#text"], "ppub": front["journal-meta"]["issn"][0]["#text"]},
    "publisher": front["journal-meta"]["publisher"]["publisher-name"]}
    articleMeta = {
    "id": front["article-meta"]["article-id"][2]["#text"],
    "categories":front["article-meta"]["article-categories"]["subj-group"]["subject"],
    "title":front["article-meta"]["title-group"]["article-title"],
    "contributors":[{"name": author["name"]["surname"]+author["name"]["given-names"],"type":author["@contrib-type"],"id":author["@id"]} for author in front["article-meta"]["contrib-group"]["contrib"] ],
    "published":front["article-meta"]["pub-date"],
    "history":[{"type":recType["@date-type"],"date":recType["day"]+"/"+recType["month"]+"/"+recType["year"]} for recType in front["article-meta"]["history"]["date"]],
    "permission":{"year":front["article-meta"]["permissions"]["copyright-year"],"holder":front["article-meta"]["permissions"]["copyright-holder"],"license":front["article-meta"]["permissions"]["license"]["license-p"]},
    "abstract":front["article-meta"]["abstract"]["p"],
    "reference-counts":front["article-meta"]["counts"]["ref-count"]["@count"],
    "page-count":front["article-meta"]["counts"]["page-count"]['@count'],
    "body":formArticleBody(article['body']),
    "affiliations":front["article-meta"]["aff"]
    }
    # with open('D:\python_project\games2\src\db_scripts\hindwai\json_file\\full_article.json','w') as output_json_file:
    #     output_json_file.write(json.dumps(articleMeta))
    journal = {"journalMeta":journalMeta,"article":articleMeta}
    # Write data to mongodbb:
    try:
        client = MongoClient('localhost', 27017)
    except ConnectionFailure:
        print("Server not available")


    db = client['hindwai']
    collection = db['journals']
    # insert the document
    try:
        result = collection.insert_one(journal)
        print("Insertion done ...",result.inserted_id)
    except OperationFailure as OperationFailureError:
        print("OperationFailureError error",OperationFailureError)
    except ExecutionTimeout as ExecutionTimeoutError:
        print("ExecutionTimeoutError error",ExecutionTimeoutError)
    except WriteError as WriteErrorError:
        print("WriteErrorError error",WriteErrorError)


    
