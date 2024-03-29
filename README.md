# Тренажер для слепой печати

## Описание
Пользователю предлагается напечатать английский текст на скорость.\
![Картинка с примером теста](/readme_images/test.png)\
После прохождения теста тренажер предоставляет результаты.\
![Картинка с результатами теста](/readme_images/results.png)\
При желании в тренажер можно загрузить собственный текст.\
![Картинка с заранее заданным тестом](/readme_images/custom.png)

## Управление
Английские буквы и пробел - для прохождения теста.\
Tab - для повторного прохождения теста.\
Escape - для выхода из тренажера.

## Обозначения
CPM - количество правильно напечатанных символов в минуту\
ACC - точность напечатанного текста\
REAL ACC - точность напечатанного текста с учетом исправлений

## Управление тестами
Чтобы сделать свой тест нужно:
1. Создать файл в папке content/tests/ с расширением .txt
2. Написать текст в этом файле (без заглавных букв, знаков пунктуации и специальных символов)
3. Написать название созданного файла в content/data/test_info.txt

Для рандомного теста надо написать random в файле content/data/test_info.txt

## Установка и запуск
```
git clone git@github.com:rgrinom/touch_typing.git
cd touch_typing
pip install -r requirements.txt
python3 main.py
```