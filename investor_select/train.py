
import gensim 
from preprocess import normalize
from nltk.tokenize import word_tokenize,sent_tokenize

input_file = "/home/mayank/Desktop/hackstreet/investor_select/investor_description.txt"
documents = []


with open (input_file, 'rb') as f:
    for i,line in enumerate (f):
        sentence = line.decode('utf-8')
        documents.append(sentence)
    
       
documents = [[w for w in word_tokenize(text) ] for text in documents ]
#print(documents)

for i in range(len(documents)):
    documents[i] = normalize(documents[i])
     
model = gensim.models.Word2Vec(documents,
        size=150,
        window=10,
        min_count=1,
        workers=10)

model.train(documents, total_examples=len(documents), epochs=100)

model.save("word2vec.model")