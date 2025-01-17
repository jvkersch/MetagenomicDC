import cPickle as pickle
from sklearn.model_selection import StratifiedKFold
import sys
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Convolution1D
from keras.datasets import mnist
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution1D, MaxPooling1D
from keras.utils import np_utils
from keras import backend as K
import numpy as np

#parameters: sys.argv[1] = input dataset as matrix of k-mers
nome_train=sys.argv[1].split(".")[0]				

def load_data(file):
	lista=[]
	records= list(open(file, "r"))
	records=records[1:]
	for seq in records:
		elements=seq.split(",")
		level=elements[-1].split("\n")
		classe=level[0]
		lista.append(classe)

	lista=set(lista)
	classes=sorted(lista)
	X=[]
	Y=[]
	for seq in records:
		elements=seq.split(",")
		X.append(elements[1:-1])
		level=elements[-1].split("\n")
		classe=level[0]
		Y.append(classes.index(classe))
	X=np.array(X,dtype=float)
	Y=np.array(Y,dtype=int)
	data_max= np.amax(X)
	X = X/data_max
	return X,Y,len(classes),len(X[0])

def create_model(nb_classes,input_length):
    model = Sequential()
    model.add(Convolution1D(5,5, border_mode='valid', input_dim=1,input_length=input_length)) #input_dim
    model.add(Activation('relu'))
    model.add(MaxPooling1D(pool_length=2,border_mode='valid'))
    model.add(Convolution1D(10, 5,border_mode='valid'))
    model.add(Activation('relu'))
    model.add(MaxPooling1D(pool_length=2,border_mode='valid'))
    model.add(Flatten())
    ##
    ##MLP
    model.add(Dense(500))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))
    model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
    return model


def train_and_evaluate_model (model, datatr, labelstr, nb_classes):


    datatr = datatr.reshape(datatr.shape + (1,))
    labelstr = np_utils.to_categorical(labelstr, nb_classes)

    history = model.fit(datatr, labelstr, epochs=100, batch_size=20, validation_split=0.1)
    model.save("{}.dat".format(nome_train))
    with open("{}.hist".format(nome_train), "wb") as fp:
            pickle.dump(history.history, fp)
    

# def train_and_evaluate_model (i, model, datatr, labelstr, datate, labelste,nb_classes):


#     datatr = datatr.reshape(datatr.shape + (1,))
#     labelstr = np_utils.to_categorical(labelstr, nb_classes)
#     labelste_bin = np_utils.to_categorical(labelste, nb_classes)

#     history = model.fit(datatr, labelstr, nb_epoch=100, batch_size=20, verbose = 0)
#     datate = datate.reshape(datate.shape + (1,))
#     model.save("{}-{}.dat".format(nome_train, i))
#     with open("{}-{}.hist".format(nome_train, i), "wb") as fp:
#             pickle.dump(history.history, fp)
    
#     tr_scores = model.evaluate(datatr,labelstr,verbose=0)
#     preds = model.predict_classes(datate,verbose = 0)
    
#     scores = model.evaluate(datate, labelste_bin,verbose=0)
#     return preds, labelste



if __name__ == "__main__":
	n_folds = 10
	X,Y,nb_classes,input_length = load_data(sys.argv[1])
	
	model = create_model(nb_classes,input_length)
	train_and_evaluate_model(model, X, Y, nb_classes)
        
