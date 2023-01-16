from sklearn import tree
import pickle

# Training data
# [Backend or Frontend, Coding Logic, Coding Design, Coding Mobile, Manage Team, Analyse Data]
X = [[1, 1, 1, 0, 0, 0],
     [1, 1, 0, 0, 0, 0],
     [0,0,1,0,0,0],
     [0,1,1,1,0,0],
     [1,0,0,0,1,1],
     [1,1,0,0,0,1]]

# Animal labels
# ['mammal', 'mammal', 'bird', 'bird', 'fish', 'fish']
Y = ['fullStackDev', 'backEndDev', 'frontEndDev', 'MobileDev', 'DevOps', 'DataScientist']


# Initialize and train the classifier
clf = tree.DecisionTreeClassifier()
clf = clf.partial_fit(X, Y)

# # Test data
# # [Backend or Frontend, Coding Logic, Coding Design, Coding Mobile, Manage Team, Analyse Data]
X_test = [[0,1,1,0,0,1]]

# # Predict the class of the test data
# prediction = clf.predict(X_test)
# print("Predicted class: ", prediction)





# # save the model to disk
# filename = 'finalized_model.sav'
# pickle.dump(clf, open(filename, 'wb'))
 
# some time later...
 
# load the model from disk
# loaded_model = pickle.load(open(filename, 'rb'))
# result = loaded_model.predict(X_test)
# print(result)