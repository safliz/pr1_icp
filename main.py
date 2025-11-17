import pandas as pd
import numpy as np

df = pd.DataFrame({
    'Название': [f'Товар_{i}' for i in range(1, 21)],
    'Категория': np.random.choice(['Обувь', 'Одежда', 'Продукты', 'Техника', 'Игрушки'], 20),
    'Количество': np.random.randint(1, 100, 20),
    'Цена за единицу': np.random.randint(100, 5000, 20),
    'Складское помещение': np.random.choice( ['1','2','3'], 20)
})

def show_all():
    print(df)


def add_product():
    '''добавить'''

    name = input('Название: ')
    category = input('Категория: ')
    storage = input('Склад: ')

    while True:
        q = input('Количество (число >= 0): ')
        try:
            quantity = int(q)
            if quantity >= 0:
                break
        except:
            pass

    while True:
        p = input('Цена (число >= 0): ')
        try:
            price = float(p)
            if price >= 0:
                break
        except:
            pass


    matches = df[df['Название'] == name]

    if matches.empty:
        df.loc[len(df)] = [name, category, quantity, price, storage]
        print('Товар успешно добавлен!')
        return

    for idx, row in matches.iterrows():
        if row['Категория'] != category:
            print(' Товар с таким названием уже существует, но его категория отличается! Добавление отменено')
            return
        
        if  row['Цена за единицу'] == price and row['Складское помещение'] == storage:
            df.loc[idx, 'Количество'] += quantity
            print('Такой товар уже существует на данном складе. Количество товара увеличено!')
            return
        
        if  row['Цена за единицу'] != price and row['Складское помещение'] == storage:
            df.loc[idx, 'Количество'] += quantity
            print('Такой товар уже существует на данном складе, но его цена отличается! Добавление отменено')
            return

        df.loc[len(df)] = [name, category, quantity, price, storage]
        print('Товар добавлен на новый склад!')
        return


def remove_product():
    '''Удалить'''

    name = input('Введите название товара для удаления: ')
    if name in df['Название'].values:
        df.drop(df[df['Название'] == name].index, inplace=True)
        print('Товар успешно удален')
    else:
        print('Товар не найден. Список доступных для удаления товаров доступен по команде show')


def change_quantity():
    '''Изменить количество'''

    name = input('Название товара: ')
    matches = df[df['Название'] == name]
    if matches.empty:
        print('Товара с таким названием не существует!')
        return

    storage = input('Склад: ')
    match_storage = matches[matches['Складское помещение'] == storage]
    if match_storage.empty:
        print('На этом складе нет такого товара!')
        return

    while True:
        q = input('Новое количество (число >= 0): ')
        try:
            new_q = int(q)
            if new_q >= 0:
                break
        except:
            print('Введите целое число!')

    df.loc[(df['Название'] == name) & (df['Складское помещение'] == storage),'Количество'] = new_q
    print('Количество обновлено!')


def change_price():
    '''Изменить цену товара (на всех складах или на одном)'''

    name = input('Название товара: ')
    matches = df[df['Название'] == name]

    if matches.empty:
        print('Товар с таким названием не найден!')
        return

    while True:
        p = input('Новая цена (число >= 0): ')
        try:
            new_price = float(p)
            if new_price >= 0:
                break
        except:
            pass

    while True:
        mode = input('Изменить на всех складах? (да/нет): ').strip().lower()
        if mode in ('да', 'нет'):
            break

    if mode == 'да':
        df.loc[df['Название'] == name, 'Цена за единицу'] = new_price
        print('Цена успешно изменена на всех складах!')
        return

    storage = input('Склад: ')
    match_storage = matches[matches['Складское помещение'] == storage]
    if match_storage.empty:
        print('На этом складе данного товара нет! Изменение отменено')
        return

    df.loc[
        (df['Название'] == name) &(df['Складское помещение'] == storage),'Цена за единицу'] = new_price
    print('Цена успешно изменена на выбранном складе!')


def stats():
    '''статистика'''

    print('1 — Общая стоимость всех товаров')
    print('2 — Средняя цена по категориям')
    print('3 — ТОП-5 самых дорогих')
    print('4 — Количество товаров категории')
    print('5 — Количество товаров на складе\n')
    while True:
        choice = input('Выберите пункт (1-5): ').strip()
        if choice in ('1','2', '3', '4', '5'):
            break

    if choice == '1':
        total = (df['Количество'] * df['Цена за единицу']).sum()
        print('Общая стоимость всех товаров:', total)

    elif choice == '2':
        print('Средняя цена по категориям:')
        print(df.groupby('Категория')['Цена за единицу'].mean())

    elif choice == '3':
        print('ТОП-5 самых дорогих:')
        print(df.nlargest(5, 'Цена за единицу'))

    elif choice == '4':
        cat = input('Категория: ')
        if cat not in df['Категория'].unique():
            print('Такой категории нет в базе данных!')
            return
        print('Количество товаров в категории:', df[df['Категория'] == cat]['Количество'].sum()) 

    elif choice == '5':
        st = input('Склад: ')
        if st not in df['Складское помещение'].unique():
            print('Такого склада нет в базе данных!')
            return
        print('Количество товаров на складе:', df[df['Складское помещение'] == st]['Количество'].sum())


def filter_data():
    '''Фильтрация по категории или складу'''

    while True:
        f = input('Фильтр по (категория/склад): ').strip().lower()
        if f in ('категория', 'склад'):
            break

    if f == 'категория':
        cat = input('Введите категорию: ').strip()
        if cat not in df['Категория'].unique():
            print('Такой категории нет в базе данных!')
            return
        print(df[df['Категория'] == cat])
        return

    if f == 'склад':
        st = input('Введите склад: ').strip()
        if st not in df['Складское помещение'].unique():
            print('Такого склада нет в базе данных!')
            return
        print(df[df['Складское помещение'] == st])
        return


def order_products():
    '''Заказ'''

    while True:
        try:
            while True:
                name = input('Название товара: ')
                available = df[df['Название'] == name]
                if available.empty:
                    print('Такого товара нет в базе данных! Повторите ввод')
                else:
                    break

            if available['Количество'].sum() == 0:
                print('Товар закончился! Информация сохранена в out.txt')
                with open('C:\\Users\\Liza\\Downloads\\ицп\\out.txt', 'a', encoding='utf-8') as f:
                    f.write(f'{name} — закончился\n')
            
            else:
                if len(available) > 1:
                    print('Товар есть на нескольких складах:')
                    print(available[['Складское помещение', 'Количество']])
                    while True:
                        st = input('Выберите склад: ')
                        if st in available['Складское помещение'].values:
                            break
                        print('Данного склада нет в списке доступных!')
                else:
                    st = available['Складское помещение'].iloc[0]

                row = df[(df['Название'] == name) & (df['Складское помещение'] == st)]
                current_q = row['Количество'].iloc[0]

                if current_q == 0:
                    print('На выбранном складе товара нет! Информация сохранена в out.txt')
                    with open('C:\\Users\\Liza\\Downloads\\ицп\\out.txt', 'a', encoding='utf-8') as f:
                        f.write(f'{name} — закончился на складе {st}\n')

                else:
                    while True:
                        print(f'\nВ наличии: {current_q}')
                        amount_s = input('Сколько нужно: ')
                        if not amount_s.isdigit():
                            print('Введите число > 0')
                            continue
                        amount = int(amount_s)
                        if amount < 1:
                            print('Введите число > 0')
                            continue
                        if amount > current_q:
                            print('Нельзя заказать больше, чем есть в наличии')
                            continue
                        break

                    df.loc[row.index, 'Количество'] = current_q - amount
                    print('Заказ успешно оформлен!')
        except:
            print('Ошибка ввода.')

        while True:
            again = input('\nВыбрать ещё товар? (да/нет): ')
            if again in ('да', 'нет'):
                break
        if again == 'нет':
            break


def min_max_price_storage():
    '''Товары с минимальной и максимальной ценой на складе'''

    st = input('Введите склад: ')
    subset = df[df['Складское помещение'] == st]
    if subset.empty:
        print('Такого склада нет в базе данных!')
        return
    
    print('Максимальная цена:')
    print(subset.nlargest(1, 'Цена за единицу'))
    print('\nМинимальная цена:')
    print(subset.nsmallest(1, 'Цена за единицу'))


def filter_by_price():
    '''Фильтрация по диапазону цен'''

    try:
        while True:
            try:
                low = float(input('Минимальная цена: '))
                high = float(input('Максимальная цена: '))
            except ValueError:
                print('Введите числовые значения')
                continue
            if low > high:
                print('Минимальная цена не может быть больше максимальной! Попробуйте снова')
                continue
            break
        
        result = df[(df['Цена за единицу'] >= low) & (df['Цена за единицу'] <= high)]

        if result.empty:
            print('Товары в этом диапазоне не найдены!')
            return
        print(result)

    except:
        pass


while True:
    print('\nДоступные команды (0-10):')
    print('1 — показать весь склад')
    print('2 — добавить товар')
    print('3 — удалить товар')
    print('4 — изменить количество товара')
    print('5 — изменить цену товара')
    print('6 — статистика')
    print('7 — фильтрация по категории или складу')
    print('8 — заказать товар')
    print('9 — товары с мин/макс ценой на складе')
    print('10 — фильтрация по диапазону цены')
    print('0 — выйти\n')

    command = input('Введите номер команды: ').strip()

    if command == '1':
        show_all()

    elif command == '2':
        add_product()

    elif command == '3':
        remove_product()

    elif command == '4':
        change_quantity()

    elif command == '5':
        change_price()

    elif command == '6':
        stats()

    elif command == '7':
        filter_data()

    elif command == '8':
        order_products()

    elif command == '9':
        min_max_price_storage()

    elif command == '10':
        filter_by_price()

    elif command == '0':
        break

    else:
        print('Команда не распознана! Попробуйте снова')
