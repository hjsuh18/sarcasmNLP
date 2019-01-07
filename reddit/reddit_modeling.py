#!/usr/bin/env python
# coding: utf-8

# # Reddit Analysis

# ## Import Data from DynamoDB

# In[1]:


import boto3


# In[2]:


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


# In[3]:


trainX, trainY = getData("reddit_train_balanced_features")
testX, testY = getData("reddit_test_balanced_features")


# ## Import Data using Pickle

# In[4]:


import pickle
with open('trainX.pkl', 'wb') as f:
    pickle.dump(trainX, f)
with open('trainY.pkl', 'wb') as f:
    pickle.dump(trainY, f)
with open('testX.pkl', 'wb') as f:
    pickle.dump(testX, f)
with open('testY.pkl', 'wb') as f:
    pickle.dump(testY, f)


# In[5]:


# import trainX, trainY, testX and testY from pickle files
with open('trainX.pkl', 'rb') as f:
    trainX = pickle.load(f)
with open('trainY.pkl', 'rb') as f:
    trainY = pickle.load(f)
with open('testX.pkl', 'rb') as f:
    testX = pickle.load(f)
with open('testY.pkl', 'rb') as f:
    testY = pickle.load(f)


# In[6]:


print("Training features count: ", len(trainX))
print("Training sarcasm labels count: ", len(trainY))
print("Testing features count: ", len(testX))
print("Testing features count: ", len(testY))
print("Total count: ", len(trainX) + len(testX))


# ## Split into sarcastic and non-sarcastic lists

# In[7]:


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


# In[ ]:


import numpy as np
trainX = np.array(trainX)
trainY = np.array(trainY)
testX = np.array(testX)
testY = np.array(testY)


# ## Statistical Analysis

# ### features:
# - a[0]: sentence positivity
# - a[1]: adjacent contrast
# - a[2]: maxPhrase
# - a[3]: minPhrase
# - a[4]: phrase contrast : maxPhrase - minPhrase
# - a[5]: positivity score of parent
# - a[6]: parent-child sentiment contrast

# ### Isolate each feature data into lists

# In[8]:


sarcSentScore = [float(a[0]) for a in sarcFeat]
nonsarcSentScore = [float(a[0]) for a in nonsarcFeat]

sarcAdjContrast = [float(a[1]) for a in sarcFeat]
nonsarcAdjContrast = [float(a[1]) for a in nonsarcFeat]

sarcMaxScore = [float(a[2]) for a in sarcFeat]
nonsarcMaxScore = [float(a[2]) for a in nonsarcFeat]

sarcMinScore = [float(a[3]) for a in sarcFeat]
nonsarcMinScore = [float(a[3]) for a in nonsarcFeat]

sarcSentRange = [float(a[4]) for a in sarcFeat]
nonsarcSentRange = [float(a[4]) for a in nonsarcFeat]

sarcParentScore = [float(a[5]) for a in sarcFeat]
nonsarcParentScore = [float(a[5]) for a in nonsarcFeat]

sarcParentContrast = [float(a[6]) for a in sarcFeat]
nonsarcParentContrast = [float(a[6]) for a in nonsarcFeat]


# In[9]:


from scipy import stats
def printStatsHelper(heading, stats):
    print(heading)
    print("min, max: ", stats[1])
    print("mean: ", stats[2])
    print("variance: ", stats[3])
    print("skewness: ", stats[4], "\n")

def printStats(sarc, nonsarc):
    print("Statistics: \n")
    print("Sentence sentiment score:")
    
    printStatsHelper("Sarcastic: ", stats.describe(sarcSentScore))
    printStatsHelper("Non-sarcastic: ", stats.describe(nonsarcSentScore))
    
    print("Adjacent Sentiment Contrast Score:")
    printStatsHelper("Sarcastic: ", stats.describe(sarcAdjContrast))
    printStatsHelper("Non-sarcastic: ", stats.describe(nonsarcAdjContrast))
    
    print("Maximum sentiment score:")
    printStatsHelper("Sarcastic: ", stats.describe(sarcMaxScore))
    printStatsHelper("Non-sarcastic: ", stats.describe(nonsarcMaxScore))
    
    print("Minimum sentiment score:")
    printStatsHelper("Sarcastic: ", stats.describe(sarcMinScore))
    printStatsHelper("Non-sarcastic: ", stats.describe(nonsarcMinScore))
    
    print("Sentiment score range:")
    printStatsHelper("Sarcastic: ", stats.describe(sarcSentRange))
    printStatsHelper("Non-sarcastic: ", stats.describe(nonsarcSentRange))
    
    print("Parent sentiment score:")
    printStatsHelper("Sarcastic: ", stats.describe(sarcParentScore))
    printStatsHelper("Non-sarcastic: ", stats.describe(nonsarcParentScore))
    
    print("Parent-text contrast score")
    printStatsHelper("Sarcastic: ", stats.describe(sarcParentContrast))
    printStatsHelper("Non-sarcastic: ", stats.describe(nonsarcParentContrast))


# In[10]:


printStats(sarcFeat, nonsarcFeat)


# ## Plots

# In[11]:


import matplotlib.pyplot as plt

data = [sarcSentScore, nonsarcSentScore, sarcMaxScore, nonsarcMaxScore, 
        sarcMinScore, nonsarcMinScore, sarcSentRange, nonsarcSentRange, 
        sarcAdjContrast, nonsarcAdjContrast, sarcParentScore, nonsarcParentScore,
        sarcParentContrast, nonsarcParentContrast]
data.reverse()

fig, ax = plt.subplots()
fig.set_figheight(15)
fig.set_figwidth(15)

ax.boxplot(data, showmeans=True, vert=False)

ax.set_title('Reddit Sentiment Feature Box Plots', fontsize=30)
ax.set_xlabel('Score', fontsize=18)
ax.set_ylabel('Feature Type (S: Sarcastic, NS: Not Sarcastic)', fontsize=18)
ax.tick_params(axis='both', labelsize=15)

labels = ["Sentence score (S)", "Sentence score (NS)",
          "Maximum score (S)", "Maximum score (NS)",
          "Minimum score (S)", "Minimum score (NS)",
          "Score range (S)", "Score range (NS)",
          "Adjacent contrast (S)", "Adjacent contrast (NS)",
          "Parent score (S)", "Parent score (NS)",
          "Parent-text contrast(S)", "Parent-text contrast(NS)"]
labels.reverse()
ax.set_yticklabels(labels, fontsize=8)

plt.show()


# In[12]:


import matplotlib.pyplot as plt

height = [0.98, 1.03, 0.74, 0.79]
label = ["Score range (NS)", "Score range (S)", 
         "Adjacent contrast (NS)", "Adjacent contrast (S)"]
stddev = [0.66, 0.62, 0.52, 0.50]

fig, ax = plt.subplots()
fig.set_figheight(7)
fig.set_figwidth(12)

ax.barh(label, height, xerr=stddev)

ax.set_title('Mean Scores of Adjacent Contrast and Score Range', fontsize=25)
ax.set_ylabel('Feature (S: Sarcastic, NS: Not Sarcastic)', fontsize=18)
ax.set_xlabel('Score', fontsize=18)
ax.tick_params(axis='both', labelsize=15)

plt.show()


# In[13]:


import matplotlib.pyplot as plt

data = [sarcParentScore, nonsarcParentScore,
        sarcParentContrast, nonsarcParentContrast]
data.reverse()

fig, ax = plt.subplots()

ax.boxplot(data, showmeans=True, vert=False)

ax.set_title('Reddit Sentiment Feature Box Plots')
ax.set_xlabel('Score')
ax.set_ylabel('Feature Type (S: Sarcastic, NS: Not Sarcastic)')

labels = ["Parent score (S)", "Parent score (NS)",
          "Parent-text contrast(S)", "Parent-text contrast(NS)"]
labels.reverse()
ax.set_yticklabels(labels, fontsize=8)

plt.show()


# ## Evaluation

# In[14]:


from sklearn import metrics
def evaluation(true, prediction):
    print("Accuracy: ", metrics.accuracy_score(true, prediction))
    print("Precision: ", metrics.precision_score(true, prediction))
    print("Recall: ", metrics.recall_score(true, prediction))
    print("Confusion Matrix\n", metrics.confusion_matrix(true, prediction))
    print("F1 score: ", metrics.f1_score(true, prediction))


# ## Without Parent Contrast

# In[15]:


trainXNoParent = [a[0:5] for a in trainX]
testXNoParent = [a[0:5] for a in testX]


# In[16]:


# Support Vector Machine (RBF Kernel)
from sklearn import svm
print("Support Vector Machine - RBF Kernel")
clf = svm.SVC(kernel='rbf', gamma='scale', probability=True)
clf.fit(trainXNoParent, trainY)
prediction = clf.predict(testXNoParent)
evaluation(testY, prediction)
print()


# In[ ]:


# Support Vector Machine (Linear)
from sklearn import svm
print("Support Vector Machine - Linear")
clf = svm.SVC(kernel='linear')
clf.fit(trainXNoParent, trainY)
prediction = clf.predict(testXNoParent)
evaluation(testY, prediction)
print()


# In[ ]:


# Gaussian Process Classification
print("Gaussian Process Classification")
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
kernel = 1.0 * RBF(1.0)
clf = GaussianProcessClassifier(kernel=kernel,random_state=0)
clf.fit(trainXNoParent, trainY)
prediction = clf.predict(testXNoParent)
evaluation(testY, prediction)
print()

# Random Forest Classification
print("Random Forest Classification")
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(n_estimators=10)
clf.fit(trainXNoParent, trainY)
prediction = clf.predict(testXNoParent)
evaluation(testY, prediction)
print()

# Neural Network Classification
print("Neural Network Classification")
from sklearn.neural_network import MLPClassifier
clf = MLPClassifier(solver='lbfgs', alpha=1e-3, hidden_layer_sizes=(5, 2), random_state=1)
clf.fit(trainXNoParent, trainY)
prediction = clf.predict(testXNoParent)
evaluation(testY, prediction)


# ## With Parent Contrast

# In[ ]:


print("Support Vector Machine - RBF Kernel")
from sklearn import svm
clf = svm.SVC(kernel='rbf', gamma='scale', probability=True)
clf.fit(trainX, trainY)
prediction = clf.predict(testX)
evaluation(testY, prediction)
# print(clf.predict_proba(testX)[0:5])
# print(testY[0:5])
print()


# In[ ]:


print("Support Vector Machine - Linear")
from sklearn import svm
clf = svm.SVC(kernel='linear')
clf.fit(trainX, trainY)
prediction = clf.predict(testX)
evaluation(testY, prediction)
print()
# features_names = ["positivity", "adjacentContrast", "maxPhrase", "minPhrase", "phraseContrast", "emojiSentiment", "emojisentimentContrast"]
# clf.coef_


# In[ ]:


print("Gaussian Process Classifier")
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
kernel = 1.0 * RBF(1.0)
clf = GaussianProcessClassifier(kernel=kernel,random_state=0)
clf.fit(trainX, trainY)
prediction = clf.predict(testX)
evaluation(testY, prediction)
print()

print("Random Forest Classification")
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(n_estimators=10)
clf.fit(trainX, trainY)
prediction = clf.predict(testX)
evaluation(testY, prediction)
print()

print("Neural Network Classification")
from sklearn.neural_network import MLPClassifier
clf = MLPClassifier(solver='lbfgs', alpha=1e-3, hidden_layer_sizes=(5, 2), random_state=1)
clf.fit(trainX, trainY)
prediction = clf.predict(testX)
evaluation(testY, prediction)


# In[ ]:


from sklearn import svm
clf = svm.SVC(kernel='rbf', gamma='scale', probability=True)
clf.fit(trainX, trainY)
prediction = clf.predict(testX)
evaluation(testY, prediction)
print(clf.predict_proba(testX)[0:5])
print(testY[0:5])


# In[7]:


from sklearn import svm
clf = svm.SVC(kernel='linear')
clf.fit(trainX, trainY)
prediction = clf.predict(testX)
evaluation(testY, prediction)


# In[10]:


from sklearn import tree
clf = tree.DecisionTreeClassifier()
clf = clf.fit(trainX, trainY)
prediction = clf.predict(testX)
evaluation(testY, prediction)


# In[11]:


from sklearn.neural_network import MLPClassifier
clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
clf.fit(trainX, trainY)
prediction = clf.predict(testX)
evaluation(testY, prediction)


# In[ ]:




