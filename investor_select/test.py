from gensim.models import Word2Vec
import numpy 

startup = "my startup sells cement online. cement is essential. home-building solutions"

investors = [ 
              ['Ambuja Cements' , "Ambuja Cements Ltd is India's foremost cement company known for its hassle-free, home-building solutions. Unique products tailor-made for Indian climatic conditions, sustainable operations and initiatives that advance the company's philosophy of contributing to the larger good of the society, have made it the most trusted cement brand in India" ] ,
              ['NTPC Limited', "NTPC limited., is an Indian Public Sector Undertaking, engaged in the business of generation of electricity and allied activities. It is a company incorporated under the Companies Act 1956 and is promoted by the Government of India. The headquarters of the company is situated at New Delhi" ] ,
              ['chutiya company',"its a chutiya shit. blockchain technology startup. boring company "]
            ]


def avg_sentence_vector(words, model):
    num_features = 150
    #function to average all words vectors in a given paragraph
    featureVec = np.zeros((num_features,), dtype="float32")
    nwords = 0

    for word in words:
        if word in model.wv.vocab:
            nwords = nwords+1
            featureVec = np.add(featureVec, model[word])

    if nwords>0:
        featureVec = np.divide(featureVec, nwords)
    return featureVec
    
    
model = Word2Vec.load("1_word2vec.model")

f1 = avg_sentence_vector(startup.split(),model)
for investor in investors:
    f2 = avg_sentence_vector(investor[1].split(),model)
    cosine_similarity = numpy.dot(f1,f2)/(numpy.linalg.norm(f1)* numpy.linalg.norm(f2))
    print(investor[0]," : ",cosine_similarity)
