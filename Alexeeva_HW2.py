import codecs, nltk
from nltk.collocations import *
from nltk.metrics.spearman import *
                 
corpus = []

f = codecs.open('court-V-N.csv', "r", "utf8")
for line in f:
    line = line.rstrip()
    words = line.split(",")
    text = [x.replace(" ","") for x in words]
    corpus.append(text)


finder = BigramCollocationFinder.from_documents(corpus)
finder.apply_freq_filter(3)
bigram_measures = nltk.collocations.BigramAssocMeasures()
# золотой стандарт делала на основе частотности биграмм в корпусе
GOLD = [('УДОВЛЕТВОРИТЬ', 'ИСК'),
                 ('ПРИНЯТЬ', 'РЕШЕНИЕ'),
                 ('ЛИШИТЬ', 'СВОБОДА'),
                 ('УДОВЛЕТВОРИТЬ', 'ХОДАТАЙСТВО'),
                 ('ВЫНЕСТИ', 'РЕШЕНИЕ'),
                 ('ВЫДАТЬ', 'САНКЦИЯ'),
                 ('НАЛОЖИТЬ', 'АРЕСТ'),
                 ('САНКЦИОНИРОВАТЬ', 'АРЕСТ'),
                 ('ОТКАЗАТЬ', 'УДОВЛЕТВОРЕНИЕ'),
                 ('ВЫНЕСТИ', 'ПРИГОВОР')]

# метрика Log-Likelihood
print ("___Log-Likelihood___")
scored_1 = finder.score_ngrams(bigram_measures.likelihood_ratio)
scored_bigrams = finder.score_ngrams(bigram_measures.raw_freq)
scored_gold_1 = []
for i in scored_1:
    for b in GOLD:
        if i[0][0] == b[0] and i[0][1] == b[1]:
            scored_gold_1.append(i)
gold_output_1 = []
for i in sorted(scored_gold_1, key=lambda bigram: bigram[-1], reverse=True):
        gold_output_1.append(i[0])
print('%0.1f' % spearman_correlation(ranks_from_sequence(GOLD),
                                         ranks_from_sequence(gold_output_1)))
    
#метрика Chi-square   
print("___Chi-square____")
scored_2 = finder.score_ngrams(bigram_measures.chi_sq)
scored_bigrams = finder.score_ngrams(bigram_measures.raw_freq)
scored_gold_2 = []
for i in scored_2:
    for b in GOLD:
        if i[0][0] == b[0] and i[0][1] == b[1]:
            scored_gold_2.append(i)
gold_output_2 = []
for i in sorted(scored_gold_2, key=lambda bigram: bigram[-1], reverse=True):
        gold_output_2.append(i[0])

print('%0.1f' % spearman_correlation(ranks_from_sequence(GOLD),
                                         ranks_from_sequence(gold_output_2)))


# я применила 2 метрики - Хи квадрат, Log-Likelihood
# при сравнении с золотым стандартом оказалось,
# что данные метрики Log-Likelihood имеют сильную связь с ним (0.6), 
# тогда как метрика Хи-квадрат не справилась с задачей
# и получила отрицательный корреляцию, гораздо слабее чем Log (-0.2).
# поэтому для анализа из этих двух метрик лучше выбрать Log-Likelihood
