import csv
import nltk
from sentence_transformers import SentenceTransformer

movie_script_path = ['data_imp/TheAvengers1_Script.txt',
                     'data_imp/TheAvengers2_Script.txt',
                     'data_imp/TheAvengers3_Script.txt',
                     'data_imp/TheAvengers4_Script.txt']

print("looking at movie data")

script = []
characs = ['tony', 'fury', 'nick fury', 'tony stark', 'clint barton', 'natasha romanoff', 'steve rogers', 'thor', 'loki', 'maria hill', 'jarvis', 'bruce banner', 'pepper potts', 'hulk', 'wanda maximoff', 'vision', 'sam wilson', 'james rhodes', 'ultron', 'thanos', 'peter parker', 'doctor strange']

data = [['name', 'dialogue']]

for movie in movie_script_path:
    
  with open(movie, 'r') as f:

    for l in f:
      if l.strip()!='':
        script.append(l.strip())
      else:
        pass

  for i in script:
    line = i.lower().split(' ')

    if line[0][-1]==':':
      name = line[0]
      dialogue = i.lower().replace(name, '')
      if name[:-1] in characs:
        l = [name[:-1], dialogue.strip()]
        data.append(l)

    elif line[1][-1]==':':
      name = line[0]+' '+line[1]
      dialogue = i.lower().replace(name, '')
      if name[:-1] in characs:
        l = [name[:-1], dialogue.strip()]
        data.append(l)
    else:
      pass



with open('script_avengers.csv', mode='w', newline='', encoding='utf-8') as g:
    csv_writer = csv.writer(g)
    csv_writer.writerows(data)


nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

print("embed dialogues")
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
data[0].append('embedding')
for i in data[1:]:
  embedding = model.encode(i[1])
  data[data.index(i)].append(embedding)


print("movie data saved, now looking at chats")
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC


dialogues = []
labels = []
vectors = []

for i in data[1:]:
  dialogues.append(i[1])
  labels.append(i[0])
  vectors.append(i[2])

print("making model")
############## MODEL
svm = LinearSVC()
svm.fit(vectors, labels)

#### Personal Chat

chat_path = "whatsapp_chat.txt"
data1 = [['person', 'chat']]
names = []
name_said = []

print("my chat is being read")
with open(chat_path, 'r') as k:
  for l in k:
    l = l[23:].strip()
    index = l.index(':')
    name = l[:index].strip()
    said = l[index+1:].strip()
    data1.append([name, said])

    if name not in names:
      names.append(name)


for j in names:
    j_said = ""
    for i in data1[1:]:
        if i[0]==j:
           j_said = j_said + "\n" + i[1]
    name_said.append(j_said)


### sending chats of each person to the model
dict_f = {}

for dialogue1 in name_said:
  testing_val = model.encode(dialogue1)
  pred_charac = svm.predict(testing_val.reshape(1, -1))
  dict_f[names[name_said.index(dialogue1)]] = pred_charac[0].item()

print(dict_f)