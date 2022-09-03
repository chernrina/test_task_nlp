
## Задание

https://docs.google.com/document/d/19MNbA9birxSfkVOEb3W8wa4POsZn5gQRHnWgERd_W1E/edit?usp=sharing

## Инструкция по запуску

В вашей системе должен быть установлео: Python3.7+

### Подготовка

> git clone https://github.com/chernrina/test_task_nlp.git

> cd test_task_nlp

### Важно
В папку test_task_nlp следует поместить файл test_data.csv

А также необходимо скачать предобученную модель по ссылке - https://drive.google.com/file/d/1dZFWt9yMTtgAey5BnmTB7ALWlcr0Jd48/view?usp=sharing 
(модель скачана с rusvectores, весит больше 100мб)

Необходима установка следующих packages:
> pip install pandas nltk pymorphy2 gensim spacy

> python3 -m spacy download ru_core_news_sm

### Запуск:
>python3 main.py

### Использование

После запуска в командной строке словесно отображается процесс выполнения скрипта (Загрузка, подготовка, обработка, результаты). 

Далее указаны найденные реплики в соответствии с заданием в формате:

ID : dlg_id

GREETINGS : реплика с приветствием

INTRODUCE : реплика с представлением

NAME : имя менеджера

COMPANY : название компании

GOODBYE : реплики с прощанием

CONDITION GREETINGS AND GOODBYE : TRUE/FALSE

Также создается файл results.csv, где можно увидеть 4 столбца names, greetings, goodbyes, companies с результатами парсинга


### Проблемы

Слово "здравствуйте" при лемматизации pymorphy2 остается таким же, однако в нормальной форме с использованием, например, pymystem3 будет "здравствовать", что было бы уместнее при работе с предобученной моделью. От использования pymystem3 пришлось отказаться из-за долгой работы



