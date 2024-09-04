# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import pickle
import openpyxl

# +----------------------------------------------------------------------------

# Обработчик моделей
# ------------------
# Для корректной работы модуля нужны установленные модули python3:

# - numpy
# - pandas
# - pickle 
# - scikit-learn

# На вход поступает таблица в формате .xlsx с определенным образом 
# проименованными колонками, как они находились в таблице, которую я получил
# 
# Имена колонок:
# --------------
# ['Возраст', 'Пол', 'СД', 'Курение',
# 'RR', 'TpTe', 'VAT', 'QTc', 'QT/TQ',
# 'HFQRS', 'JA', 'J80A', 'TA', 'QRSenergy', 'Tenergy', 'Tpenergy',
# 'Sbeta', 'Beta', 'QRS11energy', 'QRS12energy', 'QRS2energy', 'QRSE1',
# 'QRSE2', 'QRSE3', 'QRSE4', 'TE1', 'TE2', 'TE3', 'TE4', 'QRSw', 'Pan',
# 'Pan.1', 'RA', 'SA', 'Pst', 'Pfi', 'QRSst', 'QRSfi', 'Tfi', 'PpeakP',
# 'PpeakN', 'Rpeak', 'Speak', 'Tpeak', 'Tons', 'Toffs', 'RonsF', 'RoffsF',
# 'SDNN', 'RR.1']

# +----------------------------------------------------------------------------

if __name__ == '__main__':

    X_test_path = str(input ("Введите полный путь к данным: "))
    model_diast_path = str(input ("Введите полный путь \
        к модели диастолической дисфункции: "))
    model_fv_path = str(input ("Введите полный путь к модели оценки ФВЛЖ: "))

    try:
        X_test = pd.read_excel(X_test_path, engine = 'openpyxl')
    except:
        print("Ошибка при вводе пути!")
        print("Введите верный путь или свяжитесь с разработчиком")
        X_test_path = str(input ("Введите полный путь к данным: "))
        X_test = pd.read_excel(X_test_path, engine = 'openpyxl')

    try:
        X_test = X_test[['Возраст', 'Пол', 'СД', 'Курение',
        'RR', 'TpTe', 'VAT', 'QTc', 'QT/TQ',
        'HFQRS', 'JA', 'J80A', 'TA', 'QRSenergy', 'Tenergy', 'Tpenergy',
        'Sbeta', 'Beta', 'QRS11energy', 'QRS12energy', 'QRS2energy', 'QRSE1',
        'QRSE2', 'QRSE3', 'QRSE4', 'TE1', 'TE2', 'TE3', 'TE4', 'QRSw', 'Pan',
        'Pan.1', 'RA', 'SA', 'Pst', 'Pfi', 'QRSst', 'QRSfi', 'Tfi', 'PpeakP',
        'PpeakN', 'Rpeak', 'Speak', 'Tpeak', 'Tons', 'Toffs', 'RonsF', 'RoffsF',
        'SDNN', 'RR.1']]
    except:
        raise ValueError("Колонки должны быть проименованы \
            следующим образом: \n \
            [Возраст, Пол, СД, Курение, \n \
        RR, TpTe, VAT, QTc, QT/TQ, \n\
        HFQRS, JA, J80A, TA, QRSenergy, Tenergy, Tpenergy, \n\
        Sbeta, Beta, QRS11energy, QRS12energy, QRS2energy, QRSE1, \n\
        QRSE2, QRSE3, QRSE4, TE1, TE2, TE3, TE4, QRSw, Pan, \n\
        Pan.1, RA, SA, Pst, Pfi, QRSst, QRSfi, Tfi, PpeakP, \n\
        PpeakN, Rpeak, Speak, Tpeak, Tons, Toffs, RonsF, RoffsF, \n\
        SDNN, RR.1]")

    for col in ['Pfi', 'QRSst', 'QRSfi', 'Tfi', 'PpeakP', 'PpeakN', 'Rpeak', 
        'Speak', 'Tpeak', 'Tons', 'Toffs']:
        X_test[col] = X_test[col] - X_test['Pst']

    try:
        model_diast = pickle.load(open(model_diast_path, 'rb'))
    except:
        print("Ошибка при вводе пути модели по диастоле!")
        print("Введите верный путь или свяжитесь с разработчиком")
        model_diast_path = str(input ("Введите полный путь \
            к модели диастолической дисфункции: "))
        model_diast = pickle.load(open(model_diast_path, 'rb'))

    try:
        model_fv = pickle.load(open(model_fv_path, 'rb'))
    except:
        print("Ошибка при вводе пути модели по ФВ!")
        print("Введите верный путь или свяжитесь с разработчиком")
        model_fv_path = str(input ("Введите полный путь \
            к модели оценки ФВЛЖ: "))
        # model_fv = joblib.load(model_fv_path)
        model_fv = pickle.load(open(model_fv_path, 'rb'))    

    pred_diast = model_diast.predict_proba(X_test)[:,1] 
    pred_fv = model_fv.predict_proba(X_test)[:,1]

    np.savetxt('diastolic_test_results.txt', pred_diast, delimiter=',')
    np.savetxt('fv_test_results.txt', pred_fv, delimiter=',')
    
print('Вывод успешно сохранен в файле diastolic_test_results.txt')
print('Вывод успешно сохранен в файле fv_test_results.txt')
