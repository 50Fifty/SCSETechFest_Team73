from sklearn import tree

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
clf = clf.fit(X, Y)

# Test data
# [Backend or Frontend, Coding Logic, Coding Design, Coding Mobile, Manage Team, Analyse Data]
X_test = [[0,1,1,0,0,1]]

# Predict the class of the test data
prediction = clf.predict(X_test)
print("Predicted class: ", prediction)