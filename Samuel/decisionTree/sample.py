from sklearn import tree

# Training data
# [height, weight, hair, feathers, eggs, milk, airborne, aquatic, predator, toothed, backbone, breathes, venomous, fins, legs, tail, domestic, catsize]
X = [[180, 15, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 4, 0, 0, 0],
     [120, 10, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 4, 1, 0, 0],
     [100, 5, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0],
     [90, 5, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0],
     [50, 2, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
     [10, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 2, 1, 1]]

# Animal labels
# ['mammal', 'mammal', 'bird', 'bird', 'fish', 'fish']
Y = ['lion', 'deer', 'parrot', 'penguin', 'shark', 'dolphin']

# Initialize and train the classifier
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, Y)

# Test data
# [height, weight, hair, feathers, eggs, milk, airborne, aquatic, predator, toothed, backbone, breathes, venomous, fins, legs, tail, domestic, catsize]
X_test = [[120, 10, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 4, 1, 0, 0]]

# Predict the class of the test data
prediction = clf.predict(X_test)
print("Predicted class: ", prediction)