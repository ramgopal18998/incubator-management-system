
import gensim 
from . import preprocess
from nltk.tokenize import word_tokenize,sent_tokenize



def train_model():
	print("Inside train model")
	#input_file = "recommendations/training_data.txt"
	input_file = "/home/mayank/Desktop/hackstreet/Startup_incubator/recommendations/training_data.txt"
	documents = []

	with open(input_file, 'rb') as f:
	    for i,line in enumerate (f):
	        sentence = line.decode('utf-8')
	        print(sentence)
	        documents.append(sentence)
	    
	       
	documents = [[w for w in word_tokenize(text) ] for text in documents ]
	#print(documents)

	for i in range(len(documents)):
	    documents[i] = preprocess.normalize(documents[i])
	print(documents)
	model = gensim.models.Word2Vec(documents,
	        size=150,
	        window=10,
	        min_count=1,
	        workers=20)
	model.train(documents, total_examples=len(documents), epochs=10)
	model.save("word2vec.model")
	#model.wv.save_word2vec_format("mayank"+".bin",binary=True)
	print("model trained successfully")