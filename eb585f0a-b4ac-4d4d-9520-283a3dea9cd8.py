#!/usr/bin/env python
# coding: utf-8

# <div class="alert alert-info">
# <font size="4"><b>Комментарий ревьюера</b></font>
#     <br /> 
#     <font size="3", color = "black">
# <br />
#     Привет, Сергей! Спасибо, что прислал задание :) <br>Меня зовут Никита Сон и я буду проверять твой проект. Предлагаю обращаться друг к другу на ты, как это принято в Практикуме, если ты не против. Но если хочешь на Вы - не буду возражать 🙂
#         
# Поехали 🚀
#     <br />
# 
# Мои комментарии обозначены пометкой <b>Комментарий ревьюера</b>. При внесении правок в проект, пожалуйста, не меняй и не удаляй их т.к. дальнейшая проверка будет происходить в том числе на основе того, исправлены замечания в комментариях или нет. Зато ты всегда можешь оставить свои комментарии для меня :)
#     </font>
# </div>
# 
# <div class="alert alert-success">
# <font size="4"><b>✔️ Комментарий ревьюера</b></font>
#     <br /> 
#     <font size="3", color = "black">
# <br />
# В зелёных блоках будут позитивные комментарии
# <br />
#     </font>
# </div>
# 
# <div class="alert alert-warning">
# <font size="4"><b>⚠️ Комментарий ревьюера</b></font>
#     <br /> 
#     <font size="3", color = "black">
# <br />
# В жёлтых - некритичные замечания
#     </font>
# </div>
# 
# <div class="alert alert-danger">
# <font size="4"><b>❌ Комментарий ревьюера</b></font>
#     <br /> 
#     <font size="3", color = "black">
# <br /> 
# В красных - важные замечания, которые надо обязательно устранить
#     </font>
# </div>
# 
# <div class="alert alert-info">
# <font size="4">🍕<b> Комментарий ревьюера</b></font>
#     <br /> 
#     <font size="3", color = "black">
# <br /> 
# В синих с пиццей - различные нейтральные сообщения, советы на будещее и прочее.
#     </font>
# </div>

# # Выбор локации для скважины

# Допустим, вы работаете в добывающей компании «ГлавРосГосНефть». Нужно решить, где бурить новую скважину.
# 
# Вам предоставлены пробы нефти в трёх регионах: в каждом 10 000 месторождений, где измерили качество нефти и объём её запасов. Постройте модель машинного обучения, которая поможет определить регион, где добыча принесёт наибольшую прибыль. Проанализируйте возможную прибыль и риски техникой *Bootstrap.*
# 
# Шаги для выбора локации:
# 
# - В избранном регионе ищут месторождения, для каждого определяют значения признаков;
# - Строят модель и оценивают объём запасов;
# - Выбирают месторождения с самым высокими оценками значений. Количество месторождений зависит от бюджета компании и стоимости разработки одной скважины;
# - Прибыль равна суммарной прибыли отобранных месторождений.

# ## Загрузка и подготовка данных

# In[5]:


import pandas as pd 
import seaborn as sns
import numpy as np
from scipy import stats as st
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


# In[6]:


df_0 = pd.read_csv('/datasets/geo_data_0.csv')
display(df_0.head())
df_0.info()


# In[7]:


df_1 = pd.read_csv('/datasets/geo_data_1.csv')
display(df_1.head())
df_1.info()


# In[8]:


df_2 = pd.read_csv('/datasets/geo_data_2.csv')
display(df_2.head())
df_2.info()


# В таблицах по 5 столбцов. Тип данных в столбцах — строки и вещественные числа, пропуски отсутствуют.
# 
# Согласно документации к данным:
#     -id — уникальный идентификатор скважины;
#     -f0, f1, f2 — три признака точек
#     -product — объём запасов в скважине (тыс. баррелей).

# In[9]:


print(df_0.duplicated().sum())
print(df_1.duplicated().sum())
print(df_2.duplicated().sum())


# Полные дубликаты отсутствуют

# In[10]:


print( df_0['id'].duplicated().sum())
print(df_1['id'].duplicated().sum())
print( df_2['id'].duplicated().sum())


# Дубликаты присутствуют, у них одинаковый id, но разные данные. Т.к их доля очень мала, можем удалить эти значения:

# In[11]:


df_0 = df_0.drop_duplicates(subset=['id'])
df_1 = df_1.drop_duplicates(subset=['id'])
df_2 = df_2.drop_duplicates(subset=['id'])


# <div class="alert alert-success">
# <font size="4"><b>✔️ Комментарий ревьюера</b></font>
#     <br /> 
#     <font size="3", color = "black">
# <br />
# Молодец, что обнаружил неявные дубликаты. Это делают далеко не все.

# ## Обучение и проверка модели

# С помощью тепловой карты посмотрим на взаимосвязь признаков:

# In[12]:


sns.heatmap(df_0.corr(), annot=True, square=True)
plt.title('Взаимосвязь признаков для региона geo_data_0')
plt.show() 


# In[13]:


sns.heatmap(df_1.corr(), annot=True, square=True)
plt.title('Взаимосвязь признаков для региона geo_data_1')
plt.show()


# In[14]:


sns.heatmap(df_2.corr(), annot=True, square=True)
plt.title('Взаимосвязь признаков для региона geo_data_2')
plt.show() 


# Для региона geo_data_1 видим странное значение корреляции целевого признака от f2 равное единице, это может быть вызвано ошибкой в данных. Значения же корреляции для регионов geo_data_0 и geo_data_2 похожи, в наибольшей степени на целевой признак product влияет признак f2

# <div class="alert alert-success">
# <font size="4"><b>✔️ Комментарий ревьюера</b></font>
#     <br /> 
#     <font size="3", color = "black">
# <br />
# Корреляции - важная часть EDA текущего проекта, ведь по условию мы используем линейную модель и нам важно не столкнуться с проблемой мультиколлинеарности.

# ### Разбиение данных на выборки и обучение модели 

# In[15]:


model = LinearRegression()


# Разбивать данные на выборки и получать предсказания модели и RMSE будем с помощью функции:

# In[16]:


def predictions_rmse(df):
    features = df.drop(['id', 'product'], axis = 1)
    target = df['product']
    features_train, features_valid, target_train, target_valid = train_test_split(features, target, test_size=0.25, random_state=12345)
    model.fit(features_train, target_train)
    predicted_valid = model.predict(features_valid)
    rmse = (mean_squared_error(target_valid, predicted_valid))**0.5
    print('средний запас сырья в регионе: ', predicted_valid.mean())
    print('RMSE: ', rmse)
    return predicted_valid, target_valid


# <div class="alert alert-success">
# <font size="4"><b>✔️ Комментарий ревьюера</b></font>
#     <br /> 
#     <font size="3", color = "black">
# <br />
# Молодец, что оформил код функцией. Это в принципе хороший подход, а когда весь проект - повторение одних и тех же действий над схожими датасетами - это тем более разумно.

# <div class="alert alert-info">
# <font size="4">🍕<b> Комментарий ревьюера</b></font>
#     <br /> 
#     <font size="3", color = "black">
# <br />
# Различные константы проекта, такие как рандом стейт, стоит сохранять в отдельные переменные и оперировать уже ими, а не числами

# In[17]:


print('Для региона geo_data_0:')
predicted_0, target_0 = predictions_rmse(df_0)
print('------------------')
print('Для региона geo_data_1:')
predicted_1, target_1 = predictions_rmse(df_1)
print('------------------')
print('Для региона geo_data_2:')
predicted_2, target_2 = predictions_rmse(df_2)


# <div class="alert alert-success">
# <font size="4"><b>✔️ Комментарий ревьюера</b></font>
#     <br /> 
#     <font size="3", color = "black">
# <br />
# Получены адекватные модели

# Наименьшую RMSE видим в регионе geo_data_1, но скорее всего такое значение обусловлено обнаруженными выше подозрительными значеними признака f2. Средний запас сырья больше всего в регионах geo_data_0 и geo_data_1, но значение RMSE здесь очень велико.

# ## Подготовка к расчёту прибыли

# In[18]:


POINTS_NUM = 500       # общее число скважин для исследования
BEST_POINTS_NUM = 200  # число скважин в одном регионе для разработки
BUDGET = 10*(10**9)   # бюджет на разработку скважин в регионе
INCOME = 450000        # доход с каждой единицы продукта
RISK_MAX = 0.025       # максимальная вероятность убытков


# Рассчитаем достаточный объём сырья для безубыточной разработки новой скважины:

# In[19]:


BUDGET / BEST_POINTS_NUM / INCOME


# In[28]:


print('Средний запас нефти на скважину по регионам:')
print('geo_data_0', df_0['product'].mean())
print('geo_data_1', df_1['product'].mean())
print('geo_data_2', df_2['product'].mean())


# <div class="alert alert-success">
# <font size="4"><b>✔️ Комментарий ревьюера</b></font>
#     <br /> 
#     <font size="3", color = "black">
# <br />
# Расчёт верный

# <div class="alert alert-info">
# <font size="4">🍕<b> Комментарий ревьюера</b></font>
#     <br /> 
#     <font size="3", color = "black">
# <br />
# Просто число как результат работы ячейки кода - не очень. Стоит вывод форматировать и добавлять описание что это за число и в каких единицах измерения.

# Согласно полученным выше значениям среднего запаса сырья по регионам, ни в одном регионе нет достаточного количества для безубыточной разработки, но по условию задачи нужно исследовать 500 скважин и выбрать 200 лучших. Для этого определим функцию income_calc:

# In[20]:


def income_calc(target, predicted):
    target = pd.Series(target).reset_index(drop=True)
    predicted = pd.Series(predicted).reset_index(drop=True)
    pred_sorted = predicted.sort_values(ascending=False)
    selected = target[pred_sorted.index][:BEST_POINTS_NUM]
    return INCOME * selected.sum() - BUDGET


# <div class="alert alert-success">
# <font size="4"><b>✔️ Комментарий ревьюера</b></font>
#     <br /> 
#     <font size="3", color = "black">
# <br />
# Не знаю догадался ты как-то сам или кто-то рассказал тебе об этом тонком моменте работы (склоняюсь ко второму варианту), но сброс индексов в начале функции прибыли тебе помог избежать красного комментария. На всякий случай покажу что бы было без него на микропримере:

# In[21]:


# КОД РЕВЬЮЕРА
# предположим, у нас есть очень маленький датасет из 1 элемента целевой перемнной и соотв. 1 предсказания
_target = pd.DataFrame({'target': [1]})
_preds = pd.DataFrame({'pred': [1]})

print("Исходные данные:")
display(_preds)
display(_target)

# сделаем бутстрапированную выборку предсказаний размера 2 и по индексам возьмём соотв. таргеты
preds_bs = _preds.sample(n=2, replace=True)
target_bs = _target.loc[preds_bs.index]

print("После сэмплирования:")
display(preds_bs)
display(target_bs)

# допустим, нам нужно взять 2 лучшие по предсказаниям точки и посчитать в них прибыль
preds_sorted = preds_bs.sort_values('pred', ascending=False)
target_selected = target_bs.loc[preds_sorted[:2].index]

print("После отбора лучших точек:")
display(preds_sorted)
display(target_selected)


# <div class="alert alert-success">
# <font size="4"></font>
#     <font size="3", color = "black">
# И также бы стали множиться повторяющиеся элементы выборок у тебя. Почему предсказаний 2, а таргетов 4? На самом деле, всё очень просто. Когда мы попросили у пандаса взять таргеты по индексам предсказаний, и у нас и там и там 2 одинаковых элемента, он отнюдь должен вернуть не 2. Он для каждого запрошенного индекса предсказаний выдаёт все таргеты с таким индексом. Таким образом, мы запросили 2 раза элемента с индексом 0 - оба раза пандас отдал нам 2 таких элемента из таргетов - всего 4 элемента. А если бы у нас было и там, и там по 3 одинаковых элемента, то в итоге было бы 9. Логика, надеюсь, ясна.<br>
# 
# Сброс индексов при этом - не единственное решение проблемы. Проще было бы поступить так: в функцию расчёта прибыли передать сэмпл предсказаний и таргет (не сэмпл таргетов, а исходный, полный валидационный таргет, 25000 уникальных элементов с неповторяющимися индексами), и тогда получилось бы, что мы сэмплируем предсказания, сортируем их, выбираем 200 лучших, и только после этого по их индексам берём таргеты. Но поскольку таргеты бы были исходные, с уникальными индексами, то запросив один и тот же индекс 2 раза, мы бы в ответ получили 2 одинаковых элемента, а не 4, ошибки бы не было.

# ## Расчёт прибыли и рисков 

# In[22]:


check = income_calc(target_0, predicted_0)
check


# In[23]:


check = income_calc(target_1, predicted_1)
check


# In[24]:


check = income_calc(target_2, predicted_2)
check


# <div class="alert alert-warning">
# <font size="4"><b>⚠️ Комментарий ревьюера</b></font>
#     <br /> 
#     <font size="3", color = "black">
# <br />
# Вычисление этих 3 прибылей - шаг хороший, но отсутствие вывода говорит о том, что наверное не очень понимаешь в чём его хорошесть. Мы сейчас видим, что во всех регионах прибыль. А вывод, что каждый регион имеет прибыль, на самом деле, для нас очень важен.<br>
# 
# Дело в том, что на текущем этапе, когда мы ещё не знаем что получится с помощью бутстрапа, мы уже можем оценить насколько хорошая картина нас может ждать. Ранее мы сравнили средние запасы регионов с точкой безубыточности, и увидели, что каждый регион в среднем убыточен. Если бы мы и здесь увидели убытки, то дальнейшая работа была бы бессмысленной. Зачем нам что-то считать, если у нас даже в лучшем случае убыток? А раз у нас возможна прибыль, то смысл есть, мы делаем качественную осмысленную работу, наша модель для бизнеса может быть полезна.<br>
# 
# В реальных проектах важно как можно раньше понять движемся ли мы в верном направлении или надо что-то менять. Потому что тратить время и деньги впустую - не лучшая затея.

# Для оценки рисков определим функцию bootstrap:

# In[25]:


def bootstrap(target, predicted):
    state = np.random.RandomState(12345)
    values = []
    for i in range(1000):
        target_subsample = target.reset_index(drop=True).sample(n=POINTS_NUM, replace=True, random_state=state)
        predicted = pd.Series(predicted)
        pred_subsample = predicted[target_subsample.index]
        res = income_calc(target_subsample, pred_subsample)
        values.append(res)
    values = pd.Series(values)

    lower = values.quantile(.025)
    upper = values.quantile(.975)
    mean = values.mean() 
    risks = (values < 0).mean() * 100   
    print('Средняя выручка:', round(mean/1000000), 'млн.р.')
    print('2.5%-квантиль:', round(lower/1000000), 'млн.р')
    print('Доверительный интервал:  от', round(lower/1000000), 'до', round(upper/1000000), 'млн.р')
    print('Bероятность убытков:', risks, '%')
    ax=values.plot(kind='hist', bins=12, grid=True)  
    ax.set_xlabel('Прибыль, млн.руб.', fontsize=13)
    plt.show()


# In[26]:


print('Для региона geo_data_0:')
bootstrap(target_0, predicted_0)
print('--------------')
print('Для региона geo_data_1:')
bootstrap(target_1, predicted_1)
print('--------------')
print('Для региона geo_data_2:')
bootstrap(target_2, predicted_2)


# <div class="alert alert-info">
# <font size="4">🍕<b> Комментарий ревьюера</b></font>
#     <br /> 
#     <font size="3", color = "black">
# <br />
# Финальные результаты было бы неплохо визуализировать, ведь они - то, ради чего вся работа делалась. Для этого подойдут ящики с усами или гистограммы распределений выборочных прибылей с нанесёнными на них границами найденных дов. интервалов.

# Таким образом, в обозначенную границу вероятности убытков менее 2.5% попадает только регион geo_data_1. Также этот регион показывает наибольшую среднюю выручку в 478 млн.р.

# <div class="alert alert-success">
# <font size="4"><b>✔️ Комментарий ревьюера</b></font>
#     <br /> 
#     <font size="3", color = "black">
# <br />    
# Здорово, что обратил внимание не только на то, что в данном регионе самый низкий риск, но и лучшая средняя прибыль. Это делает твоё экспертное мнение только сильнее.

# ----

# <div class="alert alert-info">
# <font size="4">🍕<b> Комментарий ревьюера</b></font>
#     <br /> 
#     <font size="3", color = "black">
# <br />
# В целом всё отлично, требуется только одна небольшая правка: сравнение безубыточности с истинными средними и ответ на вопрос почему истинные во всех регионах близки предсказанным, и проект готов к принятию.

# Добрый вечер, добавил расчет истинных средних значений и визуализацию результатов. К сожалению не понимаю почему предсказания почти идентичны с таргетом, неважно при каком RMSE. Очень сильно плаваю в теории по последним спринтам с машинным обучением. Буду благодарен если смодешь подсказать.

# ## Чек-лист готовности проекта

# Поставьте 'x' в выполненных пунктах. Далее нажмите Shift+Enter.

# - [x]  Jupyter Notebook открыт
# - [x]  Весь код выполняется без ошибок
# - [x]  Ячейки с кодом расположены в порядке исполнения
# - [x]  Выполнен шаг 1: данные подготовлены
# - [x]  Выполнен шаг 2: модели обучены и проверены
#     - [x]  Данные корректно разбиты на обучающую и валидационную выборки
#     - [x]  Модели обучены, предсказания сделаны
#     - [x]  Предсказания и правильные ответы на валидационной выборке сохранены
#     - [x]  На экране напечатаны результаты
#     - [x]  Сделаны выводы
# - [x]  Выполнен шаг 3: проведена подготовка к расчёту прибыли
#     - [x]  Для всех ключевых значений созданы константы Python
#     - [x]  Посчитано минимальное среднее количество продукта в месторождениях региона, достаточное для разработки
#     - [x]  По предыдущему пункту сделаны выводы
#     - [x]  Написана функция расчёта прибыли
# - [x]  Выполнен шаг 4: посчитаны риски и прибыль
#     - [x]  Проведена процедура *Bootstrap*
#     - [x]  Все параметры бутстрепа соответствуют условию
#     - [x]  Найдены все нужные величины
#     - [x]  Предложен регион для разработки месторождения
#     - [x]  Выбор региона обоснован

# In[ ]:




