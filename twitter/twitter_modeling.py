import boto3

def getData(table_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    features = []
    labels = []
    response = table.scan()
    data = response['Items']
    for d in data:
        features.append(d["features"])
        labels.append(d["sarcastic"])

    while response.get('LastEvaluatedKey'):
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data = response['Items']
        for d in data:
            features.append(d["features"])
            labels.append(d["sarcastic"])
            
    return (features, labels)

trainX, trainY = getData("twitter_train")
testX, testY = getData("twitter_test")

print("Training features count: ", len(trainX))
print("Training sarcasm labels count: ", len(trainY))
print("Testing features count: ", len(testX))
print("Testing features count: ", len(testY))
print("Total count: ", len(trainX) + len(testX))

# features split into all, sarcastic, non-sarcastic
feat, sarcFeat, nonsarcFeat = [], [], []
for i in range(0, len(trainX)):
    feat.append(trainX[i])
    if trainY[i]:
        sarcFeat.append(trainX[i])
    else:
        nonsarcFeat.append(trainX[i])
        
for i in range(0, len(testX)):
    feat.append(testX[i])
    if testY[i]:
        sarcFeat.append(testX[i])
    else:
        nonsarcFeat.append(testX[i])
print("Sarcastic count: ", len(sarcFeat))
print("Non-sarcatic count: ", len(nonsarcFeat))
print("Total count: ", len(feat))

from sklearn import metrics
def evaluation(true, prediction):
    print("Accuracy: ", metrics.accuracy_score(true, prediction))
    print("Precision: ", metrics.precision_score(true, prediction))
    print("Recall: ", metrics.recall_score(true, prediction))
    print("Confusion Matrix\n", metrics.confusion_matrix(true, prediction))
    print("F1 score: ", metrics.f1_score(true, prediction))

trainXNoEmoji = [a[0:5] for a in trainX]
testXNoEmoji = [a[0:5] for a in testX]

# SVM
print("SVM no emoji")
from sklearn import svm
from sklearn.model_selection import GridSearchCV
parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10, 50, 100, 120, 135, 150, 160, 170, 180]}
svc = svm.SVC(gamma='scale')
clf = GridSearchCV(svc, parameters, cv= 5)
clf.fit(trainXNoEmoji, trainY)
prediction = clf.predict(testXNoEmoji)
evaluation(testY, prediction)
print(clf.best_estimator_)
print()

# Gaussian Process Classification
print("Gaussian Process Classification no emoji")
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
kernel = 1.0 * RBF(1.0)
clf = GaussianProcessClassifier(kernel=kernel,random_state=0)
clf.fit(trainXNoEmoji, trainY)
prediction = clf.predict(testXNoEmoji)
evaluation(testY, prediction)
print()

# Random Forest Classification
print("Random Forest Classification no emoji")
from sklearn.model_selection import RandomizedSearchCV
rfc = RandomForestClassifier()
n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
max_features = ['auto', 'sqrt']
max_depth = [int(x) for x in np.linspace(100, 500, num = 11)]
max_depth.append(None)
random_grid = {
 'n_estimators': n_estimators,
 'max_features': max_features,
 'max_depth': max_depth
 }
clf = RandomizedSearchCV(estimator = rfc, param_distributions = random_grid, n_iter = 100, cv = 5, verbose=2, random_state=42, n_jobs = -1)
# Fit the model
clf.fit(trainXNoEmoji, trainY)
prediction = clf.predict(testXNoEmoji)
evaluation(testY, prediction)
print(clf.best_params_)
print()

# Neural Network Classification
print("Neural Network Classification no emoji")
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
mlp = MLPClassifier(max_iter=1000)
parameter_space = {
    'hidden_layer_sizes': [(5), (4), (3), (5, 2), (4, 2), (3, 2)],
    'activation': ['tanh', 'relu'],
    'solver': ['sgd', 'adam', 'lbfgs'],
    'alpha': [0.0001, 0.01, 0.001],
    'learning_rate': ['constant', 'adaptive'],
}
clf = GridSearchCV(mlp, parameter_space, n_jobs=-1, cv=5, verbose=True)
clf.fit(trainXNoEmoji, trainY)
prediction = clf.predict(testXNoEmoji)
evaluation(testY, prediction)
print(clf.best_params_)
print()


# SVM
print("SVM emoji")
from sklearn import svm
from sklearn.model_selection import GridSearchCV
parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10, 50, 100, 120, 135, 150, 160, 170, 180]}
svc = svm.SVC(gamma='scale')
clf = GridSearchCV(svc, parameters, cv= 5)
clf.fit(trainX, trainY)
prediction = clf.predict(testX)
evaluation(testY, prediction)
print(clf.best_estimator_)
print()

# Gaussian Process Classification
print("Gaussian Process Classification emoji")
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
kernel = 1.0 * RBF(1.0)
clf = GaussianProcessClassifier(kernel=kernel,random_state=0)
clf.fit(trainX, trainY)
prediction = clf.predict(testX)
evaluation(testY, prediction)
print()

# Random Forest Classification
print("Random Forest Classification emoji")
from sklearn.model_selection import RandomizedSearchCV
rfc = RandomForestClassifier()
n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
max_features = ['auto', 'sqrt']
max_depth = [int(x) for x in np.linspace(100, 500, num = 11)]
max_depth.append(None)
random_grid = {
 'n_estimators': n_estimators,
 'max_features': max_features,
 'max_depth': max_depth
 }
clf = RandomizedSearchCV(estimator = rfc, param_distributions = random_grid, n_iter = 100, cv = 5, verbose=2, random_state=42, n_jobs = -1)
# Fit the model
clf.fit(trainX, trainY)
prediction = clf.predict(testX)
evaluation(testY, prediction)
print(clf.best_params_)
print()

# Neural Network Classification
print("Neural Network Classification emoji")
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
mlp = MLPClassifier(max_iter=1000)
parameter_space = {
    'hidden_layer_sizes': [(5), (4), (3), (5, 2), (4, 2), (3, 2)],
    'activation': ['tanh', 'relu'],
    'solver': ['sgd', 'adam', 'lbfgs'],
    'alpha': [0.0001, 0.01, 0.001],
    'learning_rate': ['constant', 'adaptive'],
}
clf = GridSearchCV(mlp, parameter_space, n_jobs=-1, cv=5, verbose=True)
clf.fit(trainX, trainY)
prediction = clf.predict(testX)
evaluation(testY, prediction)
print(clf.best_params_)
print()
