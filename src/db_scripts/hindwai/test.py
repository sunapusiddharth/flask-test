import json
with open("test.json",'r') as json_file:
    data_dict = json.load(json_file)
    # print(data_dict['p'][0]['#text'])
    content = ''
    content +=data_dict['title']
    for para in data_dict['p']:
        print("Types",type(para))
        if(isinstance(para,str)):
            pass
            content += para
        else:
            content += para['#text']
            # pass
            
    print("Content=",content)
    with open("article.json",'w')as output_file:
        output_file.write(content)
        print("Writing done...")
# print(type(data_dict),data_dict['title'])