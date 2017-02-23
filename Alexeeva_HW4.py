# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 13:19:26 2017

@author: USER
"""

from nltk.corpus import wordnet
from nltk.wsd import lesk


#1) Найти все значения (синсеты) для лексемы plant
#2) Найти определение для лексемы plant в значении (а) "завод" и в значении (b) "растение"
#3) Найдите два произвольных контекста для слова plant в значениях (a) "завод" и (b) "растение"; продемонстрируйте на них действие алгоритма Леска для разрешения неоднозначности
#4) Найдите гиперонимы для значения (a) и гиперонимы для значения (b)
#5) Вычислите наименьшее расстояние между значением plant "завод" и значениями лексемы industry, а также plant "растение" и значениями лексемы leaf
#Найти min (d(plant: "завод", industry), d(plant: "завод", leaf)), а также min (d(plant: "растение", industry), d(plant: "растение", leaf))
#6)Вычислить двумя разными способами расстояние:
#d(plant: "растение", rattlesnake's master) и d(organism, whole)
#Есть ли разница в расстояниях? Какое из расстояний, по Вашему мнению, в лучшей степени отражает интуитивное представление о семантчиеской близости слов?



#1) Найти все значения (синсеты) для лексемы plant
print (wordnet.synsets('plant'))

#2) Найти определение для лексемы plant в значении (а) "завод" и в значении (b) "растение"
#завод
set1 = wordnet.synset('plant.n.01')
print (set1.definition())
#растение
set2 = wordnet.synset('plant.n.02')
print (set2.definition())

#3) Найдите два произвольных контекста для слова plant в значениях
#(a) "завод" и (b) "растение"; продемонстрируйте на них действие
#алгоритма Леска для разрешения неоднозначности
sent1 = ['I', 'went', 'to', 'the', 'clothing', 'plant', 'in', 'the', 'undustrial', 'part', 'of', 'the', 'city', '.']
sent2 = ['The', 'company', 'has', '30', 'plants', 'in', 'Mexico', '.']
sent3 = ['It', 'melts', 'to', 'supply', 'water', 'and', 'nutrients', 'to', 'plants', '.']
sent4 = ['I', 'really', 'worry', 'about', 'my', 'plant', 'which', 'I', 'leaved', 'at', 'home', 'with', 'my', 'cat', '.']
print (lesk(sent1, 'plant', 'n').definition())
print (lesk(sent2, 'plant', 'n').definition())
print (lesk(sent3, 'plant', 'n').definition())
print (lesk(sent4, 'plant', 'n').definition())
#алгоритм работает очень плохо, не вывел ниодного правильного результата


#4) Найдите гиперонимы для значения (a) и гиперонимы для значения (b)
print (set1.hypernyms())
print (set2.hypernyms())

#5) Вычислите наименьшее расстояние между значением plant "завод" и значениями
#лексемы industry, а также plant "растение" и значениями лексемы leaf
set1 = wordnet.synset('plant.n.01')
industry_1 = wordnet.synset('industry.n.01')
industry_2 = wordnet.synset('industry.n.01')
for ss in wordnet.synsets('leaf'):
    print(ss, ss.definition())

#print(set1.shortest_path_distance(industry_1))
#print(sent1.path_similarity(industry_1))
#print (wordnet.path_similarity(sent1, industry_1))
print (min(wordnet.path_similarity(set1, industry_1), wordnet.path_similarity(set1,industry_2)))

set2 = wordnet.synset('plant.n.02')
leaf_1 = wordnet.synset('leaf.n.01')
leaf_2 = wordnet.synset('leaf.n.02')
leaf_3 = wordnet.synset('leaf.n.03')
leaf_4 = wordnet.synset('leaf.v.02')
leaf_5 = wordnet.synset('leaf.v.03')

#print(set2.path_similarity(leaf_1))
#print(set2.path_similarity(leaf_2))
#print(set2.path_similarity(leaf_3))
#print(set2.path_similarity(leaf_4))
#print(set2.path_similarity(leaf_5))

#print(set2.shortest_path_distance(leaf_1))
#print(set2.shortest_path_distance(leaf_2))
#print(set2.shortest_path_distance(leaf_3))
#print(set2.shortest_path_distance(leaf_4))
#print(set2.shortest_path_distance(leaf_5))

print (min(set2.shortest_path_distance(leaf_1), set2.shortest_path_distance(leaf_2), set2.shortest_path_distance(leaf_3)))
print (min(set2.path_similarity(leaf_1), set2.path_similarity(leaf_2), set2.path_similarity(leaf_3)))
#еще есть такая функция как shortest_path_distance,
#она выдает немного другие результаты для примера с plant-leaf

#6)Вычислить двумя разными способами расстояние:
#d(plant: "растение", rattlesnake's master) и d(organism, whole)
set1 = wordnet.synset ('organism.n.01')
set2 = wordnet.synset ('organism.n.02')
set1_1 = wordnet.synset ('whole.n.01')
set2_2 = wordnet.synset ('whole.n.02')
print (set1.shortest_path_distance(set1_1))
print (set1.shortest_path_distance(set2_2))
print (set1.path_similarity(set1_1))
print (set1.path_similarity(set2_2))
print (set2.shortest_path_distance(set1_1))
print (set2.shortest_path_distance(set2_2))
print (set2.path_similarity(set1_1))
print (set2.path_similarity(set2_2))
   
#функции противоположны друг другу: shortest_path_distance - чем меньше, тем лучше
#path_similarity - чем больше, тем лучше
#на наших данных они одинаково точно передают большую связь второго значения organism с whole
# хотя данные по  organism1~whole2 существенно выше остальных условий.

#а если сравнить path_similarity и lch_similarity:
    
print (set1.lch_similarity(set1_1))
print (set2.lch_similarity(set1_1))
print (set1.lch_similarity(set2_2))
print (set2.lch_similarity(set2_2))
#цифры немного различаются, но это потому что в lch_similarity еще измеряется глубина
#также как и в предыдущем, лучше всего связаны organism1~whole2 тк имеют самые высокие показатели
set1 = wordnet.synset('plant.n.02')
print (wordnet.synsets("rattlesnake's master"))
print (set1.path_similarity(set1_1))
# измерения не работают, тк синсета rattlesnake's master нет в корпусе