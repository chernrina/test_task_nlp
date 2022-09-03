import pandas as pd
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pymorphy2
import gensim
import ru_core_news_sm

print("Загрузка")
#Загрузка данных
data = pd.read_csv('test_data.csv')
#Копия данных с ролью=менеджер
data_manager = data[data.role=='manager'].copy(deep=True)

nltk.download('punkt')
#Разделение реплик на токены - слова
ans = pd.DataFrame()
ans['words'] = [word_tokenize(word.lower()) for word in data_manager.text]

print("Подготовка данных")
#Лемматизация
morph = pymorphy2.MorphAnalyzer()
n_words = []
for i in range(len(ans.words)) :
    n_words.append([])
    for j in range(len(ans.words[i])) :
        n_words[i].append(morph.parse(ans.words[i][j])[0].normal_form)
ans['normal_words'] = n_words

nltk.download('stopwords')
#кдаление стоп-слов
ans['no_stopwords'] = [[elem for elem in words if elem not in stopwords.words('russian')] 
                         for words in ans['normal_words']]

#Загрузка предобученной модели
model = gensim.models.KeyedVectors.load_word2vec_format('web_0_300_20.bin', encoding='utf-8', unicode_errors='ignore', binary=True)
model.init_sims(replace=True)
#Загрузка pipeline на русском языке
nlp = ru_core_news_sm.load()

print("Обработка")
#Массивы для заполнения результатов парсинга
names = []
greetings = []
goodbyes = []
companies = []
for elem in ans.no_stopwords:
	#Обработка реплики
    doc = nlp(' '.join(elem))
    #Получение заглавной буквы для имени собственного
    elem_name = ' '.join([string.capwords(token.text) if token.pos_=='PROPN' else token.text for token in doc])

    greetings.append([])
    goodbyes.append([])
    companies.append([])
    for token in doc:
        try:
        	#Сходство слов с приветствием при помощи загруженной предобученной модели
            if token.text == 'здравствуйте' or model.similarity(token.text + '_' + token.pos_, 'здравствовать_VERB') > 0.5 or \
                model.similarity(token.text + '_' + token.pos_, 'день_NOUN') > 0.8:
                greetings[-1].append(token.text)
                break
            #Сходство слов с прощанием при помощи загруженной предобученной модели
            if model.similarity(token.text + '_' + token.pos_, 'свидание_NOUN') > 0.8 or \
                model.similarity(token.text + '_' + token.pos_, 'вечер_NOUN') > 0.8:
                goodbyes[-1].append(token.text)
                break
            #Сходство слов с компанией при помощи загруженной предобученной модели
            if model.similarity(token.text + '_' + token.pos_, 'компания_NOUN') > 0.5 :
                companies[-1].append(token.text)
                break
        except Exception:
        	#Не все слова присутствуют в предобученной модели
            continue

    #Обработка реплики с заглавными буквами для имени собственного
    doc = nlp(elem_name)
    #Добавление найденной сущности PERSON
    names.append([ent.text if ent.label_ == 'PER' else '' for ent in doc.ents])


data_manager['names'] = names
data_manager['greetings'] = greetings
data_manager['goodbyes'] = goodbyes
data_manager['companies'] = companies
data_manager.to_csv('results.csv', encoding='utf-8-sig')


print("Результаты:")
#Результаты парсинга
ids = 0 
name_flag = False
greeting_flag = False
goodbye_flag = False
company_flag = False
print('ID : {}'.format(ids))
for dlg_id, text, name, greetings, goodbye, company in \
    zip(data_manager.dlg_id, data_manager.text, data_manager.names,data_manager.greetings,data_manager.goodbyes,data_manager.companies):
    if ids != dlg_id:
        ids += 1
        if greeting_flag and goodbye_flag:
            print('CONDITION GREETINGS AND GOODBYE : TRUE')
        else:
            print('CONDITION GREETINGS AND GOODBYE : FALSE')
        name_flag = False
        greeting_flag = False
        goodbye_flag = False
        company_flag = False
        print('ID : {}'.format(dlg_id))
    if not greeting_flag and len(greetings) != 0 :
        print('GREETINGS : ' + text)
        greeting_flag = True
    if not name_flag and len(name) != 0 :
        print('INTRODUCE : ' + text)
        print('NAME : ' + ''.join(name))
        name_flag = True
    if not company_flag and len(company) != 0 :
        print('COMPANY : ' + ' '.join(company))
        company_flag = True
    if not goodbye_flag and len(goodbye) != 0 :
        print('GOODBYE : ' + ''.join(text))
        goodbye_flag = True
if greeting_flag and goodbye_flag:
    print('CONDITION GREETINGS AND GOODBYE : TRUE')
else:
    print('CONDITION GREETINGS AND GOODBYE : FALSE')

