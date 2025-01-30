# Программа для работы с банковскими операциями

## Описание:
    Данное приложение анализирует транзакции, которые находятся в Excel-файле.
    Приложение генерирует JSON-данные для веб-страниц, формирует Excel-отчеты, 
    а также предоставлять другие сервисы.

---

## Содержание:
* ## <a id="title1">Описание</a>
* ## <a id="title1">Установка</a>
* ## <a id="title1">Использование</a>
* ## <a id="title1">Тестирование</a>
* ## <a id="title1">Команда проекта</a>
* ## <a id="title1">Источники</a>

---

## Установка:
1. #### Клонируйте репозиторий:
```commandline
python
git clone git@github.com:MikhailGubin/banking_applications.git
```

2. #### Установите зависимости:
```commandline
python
pip install -r requirements.txt
```

---

## Использование:

#### Работа основной программы
##### Описание:
    

##### Пример работы функции:
```commandline
python
Пример вызова программы:



Работа программы:



```

1. #### Функция  
##### Описание:
     
##### Пример работы функции:
```commandline
python


```

2. #### Функция 
##### Описание:
    
##### Пример работы функции:
```commandline
python


```

3. #### Функция  
##### Описание:
    
##### Пример работы функции:

```commandline
python

```

4. #### Функция 
##### Описание:
   
##### Пример работы функции:

```commandline
python
Пример входных данных для проверки функции

Выход функции


```

5. #### Функция sort_by_date 
##### Описание:
    
##### Пример работы функции:

```commandline
python
Пример входных данных для проверки функции



Выход функции 


```

13. ### Функция read_excel_file
##### Описание:
    Считывает финансовые операции из Excel-файла.
    Принимает путь к файлу Excel в качестве аргумента,
    выдает список словарей с транзакциями.    
    Функция расположена в модуле csv_and_excel_readers.py
##### Пример использования функции:
```commandline
#Пример вызова функции:

pprint.pprint(read_excel_file(PATH_TO_EXCEL_FILE), width=85, indent=4)

#Пример входных данных:
```
| id      | state    | date                       | ... | to                        | description              | 
|---------|----------|----------------------------|---  |---------------------------|--------------------------|
| 650703  | EXECUTED | 2023-09-05T11:30:32Z;16210 | ... | Cчет 39745660563456619397 | Перевод организации      |
| 3598919 | EXECUTED | 2020-12-06T23:00:58Z;29740 | ... | Discover 0720428384694643 | Перевод с карты на карту |
| ...     | ...      | ...                        | ... | ...                       | ...                      |

```commandline
#Пример выходных данных:
[
{'amount': 16210.0,
        'currency_code': 'PEN',
        'currency_name': 'Sol',
        'date': '2023-09-05T11:30:32Z',
        'description': 'Перевод организации',
        'from': 'Счет 58803664561298323391',
        'id': 650703.0,
        'state': 'EXECUTED',
        'to': 'Счет 39745660563456619397'},
    {   'amount': 29740.0,
        'currency_code': 'COP',
        'currency_name': 'Peso',
        'date': '2020-12-06T23:00:58Z',
        'description': 'Перевод с карты на карту',
        'from': 'Discover 3172601889670065',
        'id': 3598919.0,
        'state': 'EXECUTED',
        'to': 'Discover 0720428384694643'},
        ...
]
```
14. ### Функция 
##### Описание:
    
##### Пример использования
```commandline
python
# Пример вызова функции:


# Пример выходных данных:


```
---

## Тестирование:
Код данного проекта покрыт тестами фреймворка pytest более чем на 80 %. 

Для запуска тестов выполните команду:

'''
python
pytest
'''

Чтобы установить pytest через Poetry, используйте команду:

'''
python
poetry add --group dev pytest
'''

Модули с тестами хранятся в директории tests\. 

---

## Команда проекта:
* Губин Михаил — Back-End Engineer

---

## Источники:
* курс лекций и учебных материалов учебного центра "SkyPro"
