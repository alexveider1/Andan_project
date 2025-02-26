import os
import sys
import numpy as np
import pandas as pd
"""
Модуль для первичной обработки, удаления пропусков и ошибок из данных, полученных с сайта `https://sofifa.com/`. 
"""


def normalize_money(row: str) -> float:
    """
    Функция для обработки столбцов с денежными единицами. 
    """
    if 'B' in row:
        row = 1_000_000_000 * float(row.strip('€').strip('B').strip())
    elif 'M' in row:
        row = 1_000_000 * float(row.strip('€').strip('M').strip())
    elif 'K' in row:
        row = 1_000 * float(row.strip('€').strip('K').strip())
    else:
        row = float(row.strip('€').strip())
    return row


def normalize_name(row: str) -> str:
    """
    Функция для обработки столбцов с именами игроков
    """
    positions = np.array(['ST', 'GK', 'CAM', 'CB', 'CF', 'CM', 'LF', 'CDM',
                         'RWB', 'LB', 'LW', 'LM', 'RF', 'RB', 'LWB', 'RM', 'RW', 'SW'])
    for pos in positions:
        if f' {pos}' in row:
            row = row.replace(f' {pos}', '')
    return row


def normalize_positions(row: str) -> str:
    """
    Функция для обработки столбцов с позициями игроков
    """
    positions = np.array(['ST', 'GK', 'CAM', 'CB', 'CF', 'CM', 'LF', 'CDM',
                         'RWB', 'LB', 'LW', 'LM', 'RF', 'RB', 'LWB', 'RM', 'RW', 'SW'])
    best_positions = []
    for pos in positions:
        if f' {pos}' in row:
            best_positions.append(pos)
    for i in best_positions:
        if i in best_positions:
            if i == 'RWB':
                best_positions.remove('RW')
            elif i == 'LWB':
                best_positions.remove('LW')
    best_positions = ', '.join(best_positions)
    return best_positions


def normalize_weight(row) -> float:
    """
    Функция для обработки столбцов с весом игроков
    """
    row = float(row.split(' / ')[0].strip('kg'))
    return row


def normalize_height(row) -> float:
    """
    Функция для обработки столбцов с высотой игроков
    """
    row = float(row.split(' / ')[0].strip('cm'))
    return row


def normalize_contract(row):
    """
    Функция для обработки столбца с контрактом игрока
    """
    if 'loan' in row:
        on_loan = 'Yes'
        start = np.nan
        end = np.nan
        loan_end = row.rstrip(' On loan').split(', ')[-1]
        row = ' '.join(row.rstrip(' On loan').split(', ')[0].split(' ')[:-2])
        return row, start, end, on_loan, loan_end
    if 'Free' in row:
        row = 'Free'
        start = np.nan
        end = np.nan
        on_loan = 'No'
        loan_end = np.nan
        return row, start, end, on_loan, loan_end
    if 'Netherlands' in row:
        row = 'Free'
        start = np.nan
        end = np.nan
        on_loan = 'No'
        loan_end = np.nan
        return row, start, end, on_loan, loan_end
    elif '~' in row:
        start = row.split('~')[-2].strip().split(' ')[-1]
        end = row.split('~')[-1].strip()
        row = ' '.join(row.split(' ')[:-3])
        on_loan = 'No'
        loan_end = np.nan
        return row, start, end, on_loan, loan_end
    elif '~' not in row:
        start = np.nan
        end = row.split(' ')[-1]
        row = ' '.join(row.split(' ')[:-1])
        on_loan = 'No'
        loan_end = np.nan
        return row, start, end, on_loan, loan_end


def normalize_nums(row):
    """
    Функция для обработки столбцов с числовыми значениями-рейтингами
    """
    if '-' in str(row):
        row = row.split('-')[0]
        return int(row)
    elif '+' in str(row):
        row = row.split('+')[0]
        return int(row)

    else:
        if row != row:
            return row
        else:
            return int(row)
