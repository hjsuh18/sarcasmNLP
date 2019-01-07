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

trainX, trainY = getData("reddit_train_balanced_features")
testX, testY = getData("reddit_test_balanced_features")

print("Training features count: ", len(trainX))
print("Training sarcasm labels count: ", len(trainY))
print("Testing features count: ", len(testX))
print("Testing features count: ", len(testY))
print("Total count: ", len(trainX) + len(testX))


from sklearn import metrics
def evaluation(true, prediction):
    print("Accuracy: ", metrics.accuracy_score(true, prediction))
    print("Precision: ", metrics.precision_score(true, prediction))
    print("Recall: ", metrics.recall_score(true, prediction))
    print("Confusion Matrix\n", metrics.confusion_matrix(true, prediction))
    print("F1 score: ", metrics.f1_score(true, prediction))

trainXNoParent = [a[0:5] for a in trainX]
testXNoParent = [a[0:5] for a in testX]


# SVM
print("SVM no parent")
from sklearn import svm
# from sklearn.model_selection import GridSearchCV
# parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10, 50, 100, 120, 135, 150, 160, 170, 180]}
# svc = svm.SVC(gamma='scale')
# clf = GridSearchCV(svc, parameters, cv= 5)
print("(kernel='rbf', C=135, gamma='scale'")
clf = svm.SVC(kernel='rbf', C=135, gamma='scale')
clf.fit(trainXNoParent, trainY)
prediction = clf.predict(testXNoParent)
evaluation(testY, prediction)
# print(clf.best_estimator_)
print()

# Gaussian Process Classification
#print("Gaussian Process Classification no parent")
#from sklearn.gaussian_process import GaussianProcessClassifier
#from sklearn.gaussian_process.kernels import RBF
#kernel = 1.0 * RBF(1.0)
#clf = GaussianProcessClassifier(kernel=kernel,random_state=0)
#clf.fit(trainXNoParent, trainY)
#prediction = clf.predict(testXNoParent)
#evaluation(testY, prediction)
#print()
#
## Random Forest Classification
#print("Random Forest Classification no parent")
## from sklearn.model_selection import RandomizedSearchCV
#from sklearn.ensemble import RandomForestClassifier
#print("n_estimator=500, max_features='sqrt', max_depth=300")
## import numpy as np
#rfc = RandomForestClassifier(n_estimator=500, max_features='sqrt', max_depth=300)
## n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
## max_features = ['auto', 'sqrt']
## max_depth = [int(x) for x in np.linspace(100, 500, num = 11)]
## max_depth.append(None)
## random_grid = {
##  'n_estimators': n_estimators,
##  'max_features': max_features,
##  'max_depth': max_depth
##  }
## clf = RandomizedSearchCV(estimator = rfc, param_distributions = random_grid, n_iter = 100, cv = 5, verbose=2, random_state=42, n_jobs = -1)
## Fit the model
#rfc.fit(trainXNoParent, trainY)
#prediction = rfc.predict(testXNoParent)
#evaluation(testY, prediction)
## print(clf.best_params_)
#print()
#
## Neural Network Classification
#print("Neural Network Classification no parent")
#from sklearn.neural_network import MLPClassifier
## from sklearn.model_selection import GridSearchCV
#print("max_iter=1000, hidden_layer_sizes=(4, 2), activation='tanh', solver='lbfgs', alpha=0.001, learning_rate='adaptive'")
#mlp = MLPClassifier(max_iter=1000, hidden_layer_sizes=(4, 2), activation='tanh', solver='lbfgs', alpha=0.001, learning_rate='adaptive')
## parameter_space = {
##     'hidden_layer_sizes': [(5), (4), (3), (5, 2), (4, 2), (3, 2)],
##     'activation': ['tanh', 'relu'],
##     'solver': ['sgd', 'adam', 'lbfgs'],
##     'alpha': [0.0001, 0.01, 0.001],
##     'learning_rate': ['constant', 'adaptive'],
## }
## clf = GridSearchCV(mlp, parameter_space, n_jobs=-1, cv=5, verbose=True)
#mlp.fit(trainXNoParent, trainY)
#prediction = mlp.predict(testXNoParent)
#evaluation(testY, prediction)
## print(clf.best_params_)
#print()
#
#
## SVM
#print("SVM parent")
#from sklearn import svm
## from sklearn.model_selection import GridSearchCV
## parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10, 50, 100, 120, 135, 150, 160, 170, 180]}
#print("gamma='scale', kernel='rbf', C=60")
#clf = svm.SVC(gamma='scale', kernel='rbf', C=60)
## clf = GridSearchCV(svc, parameters, cv= 5)
#clf.fit(trainX, trainY)
#prediction = clf.predict(testX)
#evaluation(testY, prediction)
## print(clf.best_estimator_)
#print()
#
## Gaussian Process Classification
#print("Gaussian Process Classification parent")
#from sklearn.gaussian_process import GaussianProcessClassifier
#from sklearn.gaussian_process.kernels import RBF
#kernel = 1.0 * RBF(1.0)
#clf = GaussianProcessClassifier(kernel=kernel,random_state=0)
#clf.fit(trainX, trainY)
#prediction = clf.predict(testX)
#evaluation(testY, prediction)
#print()
#
## Random Forest Classification
#print("Random Forest Classification parent")
## import numpy as np
## from sklearn.model_selection import RandomizedSearchCV
#print("n_estimator=200, max_features='sqrt', max_depth=100")
#rfc = RandomForestClassifier(n_estimator=200, max_features='sqrt', max_depth=100)
## n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
## max_features = ['auto', 'sqrt']
## max_depth = [int(x) for x in np.linspace(100, 500, num = 11)]
## max_depth.append(None)
## random_grid = {
##  'n_estimators': n_estimators,
##  'max_features': max_features,
##  'max_depth': max_depth
##  }
## clf = RandomizedSearchCV(estimator = rfc, param_distributions = random_grid, n_iter = 100, cv = 5, verbose=2, random_state=42, n_jobs = -1)
## Fit the model
#rfc.fit(trainX, trainY)
#prediction = rfc.predict(testX)
#evaluation(testY, prediction)
## print(rfc.best_params_)
#print()
#
## Neural Network Classification
#print("Neural Network Classification parent")
#from sklearn.neural_network import MLPClassifier
#from sklearn.model_selection import GridSearchCV
#print("max_iter=1000, hidden_layer_sizes=(5, 2), activation='tanh', solver='lbfgs', alpha=0.001, learning_rate='adaptive'")
#clf = MLPClassifier(max_iter=1000, hidden_layer_sizes=(5, 2), activation='tanh', solver='lbfgs', alpha=0.001, learning_rate='adaptive')
## parameter_space = {
##     'hidden_layer_sizes': [(7), (6), (5), (4), (3), (7, 3), (7, 4), (7, 2), (6, 4), (6, 3), (6, 2), (5, 3), (5, 2), (4, 2), (3, 2)],
##     'activation': ['tanh', 'relu'],
##     'solver': ['sgd', 'adam', 'lbfgs'],
##     'alpha': [0.0001, 0.01, 0.001],
##     'learning_rate': ['constant', 'adaptive'],
## }
## clf = GridSearchCV(mlp, parameter_space, n_jobs=-1, cv=5, verbose=True)
#clf.fit(trainX, trainY)
#prediction = clf.predict(testX)
#evaluation(testY, prediction)
## print(clf.best_params_)
#print()
