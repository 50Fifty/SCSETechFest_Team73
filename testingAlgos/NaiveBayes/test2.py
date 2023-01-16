from sklearn.naive_bayes import GaussianNB
from sklearn import datasets
import numpy as np
import json


np.set_printoptions(suppress=True)
# Load the iris dataset as an example
iris = datasets.load_iris()
X = [[1, 1, 1, 0, 0, 0],
     [1, 1, 0, 0, 0, 0],
     [0,0,1,0,0,0],
     [0,1,1,1,0,0],
     [1,0,0,0,1,1],
     [1,1,0,0,0,1]]
y = ['fullStackDev', 'backEndDev', 'frontEndDev', 'MobileDev', 'DevOps', 'DataScientist']


# Create a GaussianNB object
gnb = GaussianNB()

# Train the model using the training sets
gnb.partial_fit(X, y, classes=np.unique(y))


answers = [[5, 4, 3, 2,3, 4]]
# Predict the class of new samples
predicted_class = gnb.predict(answers)



predicted_proba = gnb.predict_proba(answers)
print("Predicted class:", predicted_class)
print("Predicted class probability:", predicted_proba)


gnb.partial_fit(answers, ["frontEndDev"])

predicted_class = gnb.predict(answers)



predicted_proba = gnb.predict_proba(answers)
print("Predicted class:", predicted_class)
print("Predicted class probability:", predicted_proba)

