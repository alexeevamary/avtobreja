# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 12:30:39 2017

@author: USER
"""

import numpy as np
import re
from matplotlib import pyplot as plt

from sklearn import grid_search, svm




#признаки:
#длина предложения в буквах,
#число различных букв в предложении,
#число гласных в предложении,
#медиана числа букв в слове,
#медиана числа гласных в слове.







#длина предложения в буквах
def lenletters(sentence):
    sentence = re.sub('[\.!,:;\?\-\'\"]', "", sentence)
    k = 0
    for word in sentence.split():
        k += len(word)
    return k
# число различных букв в предложении
def diffletters(sentence):
    sentence = re.sub("[\.!,:;\?\-\'\"]", "", sentence)
    sentence = sentence.lower()
    k = 0
    letters = list(sentence)
    for i in set(letters):
        if i!=' ':
            k += 1
    return k

#число гласных в предложении
def vowels(sentence):
    sentence = re.sub("[\.!,:;\?\-\'\"]", "", sentence)
    k = 0
    vowel = ('аеёиоуыэюя')
    sentence = sentence.lower()
    letters = list(sentence)
    for i in letters:
        if i!=' ':
            i = i.lower()
            if i in vowel:
                k += 1
    return k

#медиана числа букв в слове
def medletters(sentence):
    sentence = re.sub("[\.!,:;\?\-\'\"]", "", sentence)
    sentence = sentence.lower()
    lenword =[]
    for word in sentence.split():
        lenword.append(len(word))
    return np.median(lenword)

#медиана числа гласных в слове
def medvowels(sentence): 
    sentence = re.sub("[\.!,:;\?\-\'\"]", "", sentence)
    sentence = sentence.lower()
    lenvowels = []
    for word in sentence.split():
        k = 0 
        vowel = ('аеёиоуыэюя')
        letters = list(word)
        for letter in letters:
            if letter in vowel:
                k+=1
        lenvowels.append(k)
    return np.median(lenvowels)




def lenwords(sentence):
    return [len(word) for word in sentence.split()]


with open('anna2.txt', encoding='utf-8') as f:
    anna = f.read()
with open('sonets2.txt', encoding='utf-8') as f:
    sonets = f.read()

anna_sentences = re.split(r'(?:[.]\s*){3}|[.?!]', anna)
sonets_sentences = re.split(r'(?:[.]\s*){3}|[.?!]', sonets)

anna_data = [(lenletters(sentence), diffletters(sentence), vowels(sentence), medletters(sentence), medvowels(sentence)) for sentence in anna_sentences if len(lenwords(sentence)) > 0]
sonets_data = [(lenletters(sentence), diffletters(sentence), vowels(sentence), medletters(sentence), medvowels(sentence)) for sentence in sonets_sentences if len(lenwords(sentence)) > 0]


anna_data = np.array(anna_data)
sonets_data = np.array(sonets_data)

#plt.figure()
#c1, c2 = 0, 1
#plt.axis([0,1000, 0, 300])
#plt.plot(anna_data[:,2],'sb', sonets_data[:,2], 'og' )
#plt.show() 
#по всем признакам на графиках особой разницы нет

data = np.vstack((anna_data, sonets_data))
#parameters = {'C': (.7, .75, .8)}
#gs = grid_search.GridSearchCV(svm.LinearSVC(), parameters)
#gs.fit(data[:, 1:], data[:, 0])
#print('Best result is ',gs.best_score_)
#print('Best C is', gs.best_estimator_.C)
#поиграла с параметрами и получила Best C - 0.75


clf = svm.LinearSVC(C=0.75)
clf.fit(data[::2, 1:], data[::2, 0])
wrong = 0
for obj in data[1::2, :]:
    label = clf.predict(obj[1:])
    if label != obj[0] and wrong < 3:
        print('Пример ошибки машины: class = ', obj[0], ', label = ', label, ', экземпляр ', obj[1:])
        wrong += 1
    if wrong > 3:
        break
#мой компьютер не очень мощный и не мог справиться с задачей на полном объеме данных
# поэтому я взяла небольшие части от обоих файлов. 
# чтобы не мучаться с поиском вывода ошибок среди ворнингов системы:
#Пример ошибки машины: class =  26.0 , label =  [ 195.] , экземпляр  [ 16.   9.   4.   2.]
#Пример ошибки машины: class =  107.0 , label =  [ 195.] , экземпляр  [ 21.   47.    5.5   2. ]
#Пример ошибки машины: class =  51.0 , label =  [ 195.] , экземпляр  [ 21.  22.   4.   2.]