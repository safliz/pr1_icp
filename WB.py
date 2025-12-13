def order(df):
    """
    заказ и корзина
    """
    logo = "WILDBERRIS"
    left = (120 - len(logo)) // 2
    right = 120 - len(logo) - left
    print(f"\033[1;37;48;5;129m{'-'*120}"+"\033[0m")
    print("\033[1;37;48;5;129m" + " "*left + logo + " "*right + "\033[0m")
    print(f"\033[1;37;48;5;129m{'-'*120}\033[0m")

    print(f"\033[38;5;54;48;5;236m\n{df}\033[0m")


    # Корзина: (Название, Склад) → {'Количество': x, 'Цена': y}
    cart = {}
    df_new = df.copy()

    while True:
        name = input('\033[38;5;229m\nВведите название товара для добавления в корзину: \033[0m').strip()
        names = df_new[df_new['Название'] == name]
        if names.empty:
            print('\033[31mТакого товара нет на складе!\033[0m')
            continue

        if len(names) > 1:
            print('\033[38;5;218m\nТовар есть на нескольких складах:\033[38;5;54;48;5;236m')
            print(names, '\033[0m')
            while True:
                st = input('\033[38;5;229m\nВыберите склад: \033[0m').strip()
                if st in names['Складское помещение'].values:
                    break
                print('\033[31mДанного склада нет в списке доступных!\033[0m')
        else:
            st = names['Складское помещение'].iloc[0]

        max_q = names[names['Складское помещение'] == st]['Количество'].iloc[0] - cart.get((name, st), {}).get('Количество', 0)
        if max_q == 0:
            print(f'\033[31mНа складе "{st}" больше нет товара "{name}"!\033[0m')
            continue

        while True:
            cmd = input(f'\033[38;5;229mВведите количество \033[38;5;218m(доступно {max_q})\033[38;5;229m: \033[0m').strip()
            if not cmd.isdigit():
                continue
            q = int(cmd)
            if 1 <= q <= max_q:
                break
            print(f'\033[31mВведите число от 1 до {max_q}!\n\033[0m')

        key = (name, st)
        price = names[names['Складское помещение'] == st]['Цена за единицу'].iloc[0]
        if key in cart:
            cart[key]['Количество'] += q
        else:
            cart[key] = {'Количество': q, 'Цена': price}

        print('\033[38;5;218mТовар добавлен в корзину! \033[0m')
###########################################################

        while True:
            print('\n\033[37;48;5;129mДоступные действия: \033[0m')
            print('\033[38;5;129m1 - добавить еще')
            print('2 - перейти в корзину\n')
            cmd = input('\033[38;5;229mВыберите действие (1-2): \033[0m').strip()
            if cmd in ('1', '2'):
                break
            print('\033[31mВведите 1 или 2!\n')

        if cmd == '1':
            continue

        # ---- Работа с корзиной ----
        while True:
            if not cart:
                print('\033[38;5;218mКорзина пуста!')
                break

            print('\033[37;48;5;129m\nКорзина:\033[38;5;54;48;5;236m')
            total_sum = 0
            for (item_name, storage), info in cart.items():
                item_sum = info['Количество'] * info['Цена']
                total_sum += item_sum
                print(f'{item_name} | Склад {storage} | Кол-во: {info["Количество"]} | Сумма: {item_sum}')
            print(f'\033[38;5;15mОбщая сумма: {total_sum} \033[0m')

            print('\n\033[37;48;5;129mДоступные действия: \033[0m')
            print('\033[38;5;129m1 — добавить еще товары')
            print('2 — изменить количество')
            print('3 — удалить товар')
            print('4 — завершить заказ')

            cmd = input('\n\033[38;5;229mВыберите действие (1-4): \033[0m').strip()
            while cmd not in ('1', '2', '3', '4'):
                print('\033[31mВведите число от 1 до 4!\n')
                cmd = input('\033[38;5;229mВыберите действие (1-4): \033[0m').strip()

            if cmd == '1':
                break
            
            elif cmd == '2':
                item_to_change = input('\033[38;5;229mВведите товар, для которого изменить количество: \033[0m').strip()

                keys = [i for i in cart if i[0] == item_to_change]
                if not keys:
                    print('\033[31mТакого товара нет в корзине!')
                    continue
                if len(keys) > 1:
                    while True:
                        st = input('\033[38;5;229mВыберите склад: \033[0m').strip()
                        if (item_to_change, st) in keys:
                            key = (item_to_change, st)
                            break
                        print('\033[31mНет данного товара на выбранном складе!')
                else:
                    key = keys[0]

                max_q = df_new[df_new['Название'] == key[0]]
                max_q = max_q[max_q['Складское помещение'] == key[1]]['Количество'].iloc[0]

                while True:
                    q_input = input(f'\033[38;5;229mНовое количество \033[38;5;218m(доступно {max_q})\033[38;5;229m: \033[0m').strip()
                    if not q_input.isdigit():
                        continue
                    q_new = int(q_input)
                    if 1 <= q_new <= max_q:
                        break
                    print(f'\033[31mВведите число от 1 до {max_q}!')

                cart[key]['Количество'] = q_new
                print('\033[38;5;218mКоличество обновлено!')

            elif cmd == '3':
                item_remove = input('\033[38;5;229mКакой товар удалить: \033[0m').strip()
                keys = [i for i in cart if i[0] == item_remove]
                if not keys:
                    print('\033[31mТакого товара нет в корзине!')
                    continue
                if len(keys) > 1:
                    while True:
                        st_remove = input('\033[38;5;229mВыберите склад: \033[0m').strip()
                        if (item_remove, st_remove) in keys:
                            key_remove = (item_remove, st_remove)
                            break
                        print('\033[31mНет данного товара из этого склада склад!')
                else:
                    key_remove = keys[0]

                del cart[key_remove]
                print('\033[38;5;218mТовар удален!')

            elif cmd == '4':
                print('\033[1;37;48;5;129m З а к а з   п о д т в е р ж д е н ! \033[0m')

                # ЧЕК

                for (name, st), info in cart.items():
                    df.loc[(df['Название'] == name) & (df['Складское помещение'] == st), 'Количество'] -= info['Количество']
                return 
            
def add_product(df):
    '''добавить'''
    name = input('\033[38;5;229mНазвание:\033[0m ')
    category = input('\033[38;5;229mКатегория:\033[0m ')
    storage = input('\033[38;5;229mСклад:\033[0m ')

    while True:
        q = input('\033[38;5;229mКоличество (целое число >= 0):\033[0m ')
        try:
            quantity = int(q)
            if quantity >= 0:
                break
        except:
            pass

    while True:
        p = input('\033[38;5;229mЦена (число >= 0): \033[0m')
        try:
            price = float(p)
            if price >= 0:
                break
        except:
            pass


    matches = df[df['Название'] == name]

    if matches.empty:
        df.loc[len(df)] = [name, category, quantity, price, storage]
        print('\033[38;5;118mТовар успешно добавлен!')
        return

    for idx, row in matches.iterrows():
        if row['Категория'] != category:
            print('\033[31mТовар с таким названием уже существует, но его категория отличается! Добавление отменено')
            return
        
        if  row['Цена за единицу'] == price and row['Складское помещение'] == storage:
            df.loc[idx, 'Количество'] += quantity
            print('\033[38;5;118mТакой товар уже существует на данном складе. Количество товара увеличено!')
            return
        
        if  row['Цена за единицу'] != price and row['Складское помещение'] == storage:
            df.loc[idx, 'Количество'] += quantity
            print('\033[31mТакой товар уже существует на данном складе, но его цена отличается! Добавление отменено')
            return

        df.loc[len(df)] = [name, category, quantity, price, storage]
        print('\033[38;5;118mТовар добавлен на новый склад!')
        return
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from termcolor import colored
df = pd.DataFrame({
    'Название': [f'Товар_{i}' for i in range(1, 21)],
    'Категория': np.random.choice(['обувь', 'одежда', 'продукты', 'техника', 'игрушки'], 20),
    'Количество': np.random.randint(1, 100, 20),
    'Цена за единицу': np.random.randint(100, 5000, 20),
    'Складское помещение': np.random.choice( ['1','2','3'], 20)
})
print(df)
add_product(df)
order(df)
