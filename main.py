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

from datetime import datetime

def log_action(message):
    with open('log.txt', 'a', encoding='utf-8') as f:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'{now} — {message}\n')

def plot_storage_fill():
    log_action('Построение графика: заполненность складов')
    storage_sum = df.groupby('Складское помещение')['Количество'].sum()
    storage_sum.plot(kind='bar', color='pink')
    plt.title('Заполненность складов (сумма товаров)')
    plt.xlabel('Склад')
    plt.ylabel('Количество товаров')
    plt.xticks(rotation=0)
    plt.show()
    plt.savefig('storage_fill.png')
    print('\033[38;5;118mГрафик сохранён как storage_fill.png')

def plot_total_items():
    log_action('Построение графика: число товаров (сумма на всех складах)')
    total_items = df.groupby('Название')['Количество'].sum()
    total_items.plot(kind='bar', color='pink')
    plt.title('Количество каждого товара на всех складах')
    plt.xlabel('Товар')
    plt.ylabel('Суммарное количество')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
    plt.savefig('total_items.png')
    print('\033[38;5;118mГрафик сохранён как total_items.png')

def plot_storage_cost():
    st = input('\033[38;5;229mВведите склад для расчета стоимости: \033[0m')
    log_action(f'Построение графика: стоимость товаров на складе {st}')
    subset = df[df['Складское помещение'] == st].copy()
    if subset.empty:
        print('Такого склада нет!')
        return
    subset['Стоимость'] = subset['Цена за единицу'] #* subset['Количество']
    subset.plot(x='Название', y='Стоимость', kind='bar', color='hotpink', legend=False)
    plt.title(f'Стоимость товаров на складе {st}')
    plt.xlabel('Товар')
    plt.ylabel('Стоимость')
    plt.tight_layout()
    plt.show()
    plt.savefig(f'storage_{st}_cost.png')
    print(f'\033[38;5;118mГрафик сохранён как storage_{st}_cost.png')


def plot_category_share():
    df_copy = df.copy()
    log_action('Построение круговой диаграммы: доля категорий в общей стоимости всех товаров')
    df_copy['Стоимость'] = df_copy['Количество'] * df_copy['Цена за единицу']
    category_sum = df_copy.groupby('Категория')['Стоимость'].sum()

    plt.figure(figsize=(7,7), facecolor='lightgoldenrodyellow')
    plt.pie(category_sum, labels=category_sum.index, autopct='%1.1f%%', colors=plt.cm.Pastel2.colors)
    plt.title('Доля категорий в общей стоимости товаров')
    plt.savefig('category_share.png')
    plt.show()
    print('\033[38;5;118mГрафик сохранён как category_share.png\033[0m')


def show_all():
    log_action('Просмотр всей таблицы')
    print('\033[38;5;217;48;5;236m\n',df,'\033[0m')


def add_product():
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
        log_action(f'Добавлен товар: {name}, склад {storage}, количество {quantity}, цена {price}')
        return

    for idx, row in matches.iterrows():
        if row['Категория'] != category:
            print('\033[31mТовар с таким названием уже существует, но его категория отличается! Добавление отменено')
            return
        
        if  row['Цена за единицу'] == price and row['Складское помещение'] == storage:
            df.loc[idx, 'Количество'] += quantity
            print('\033[38;5;118mТакой товар уже существует на данном складе. Количество товара увеличено!')
            log_action(f'Количество товара {name} на складе {storage} увеличено на {quantity}')
            return
        
        if  row['Цена за единицу'] != price and row['Складское помещение'] == storage:
            df.loc[idx, 'Количество'] += quantity
            print('\033[31mТакой товар уже существует на данном складе, но его цена отличается! Добавление отменено')
            return

        df.loc[len(df)] = [name, category, quantity, price, storage]
        print('\033[38;5;118mТовар добавлен на новый склад!')
        return


def remove_product():
    '''Удалить'''
    print('\033[38;5;217;48;5;236m\n',df,'\033[0m')
    name = input('\033[38;5;229mВведите название товара для удаления:\033[0m ')
    if name in df['Название'].values:
        df.drop(df[df['Название'] == name].index, inplace=True)
        print('\033[38;5;118mТовар успешно удален!')
        log_action(f'Удалён товар: {name}')
    else:
        print('\033[31mТовар не найден! Удаление отменено')


def change_quantity():
    '''Изменить количество'''
    print('\033[38;5;217;48;5;236m\n',df,'\033[0m')
    name = input('\033[38;5;229mНазвание товара для изменения количества: \033[0m')
    matches = df[df['Название'] == name]
    if matches.empty:
        print('\033[31mТовара с таким названием не существует!')
        return

    storage = input('\033[38;5;229mСклад: \033[0m')
    match_storage = matches[matches['Складское помещение'] == storage]
    if match_storage.empty:
        print('\033[31mНа этом складе нет такого товара!')
        return

    while True:
        q = input('\033[38;5;229mНовое количество (целое число >= 0): \033[0m')
        try:
            new_q = int(q)
            if new_q >= 0:
                break
        except:
            print('\033[31mВведите целое число!')

    df.loc[(df['Название'] == name) & (df['Складское помещение'] == storage),'Количество'] = new_q
    print('\033[38;5;118mКоличество обновлено!')
    log_action(f'Изменено количество: {name} на складе {storage} → {new_q}')


def change_price():
    '''Изменить цену товара (на всех складах или на одном)'''
    print('\033[38;5;217;48;5;236m\n',df,'\033[0m')
    name = input('\033[38;5;229mНазвание товара:\033[0m ')
    matches = df[df['Название'] == name]

    if matches.empty:
        print('\033[31mТовар с таким названием не найден!\033[37m')
        return

    while True:
        p = input('\033[38;5;229mНовая цена (число >= 0):\033[0m ')
        try:
            new_price = float(p)
            if new_price >= 0:
                break
        except:
            pass

    while True:
        mode = input('\033[38;5;229mИзменить на всех складах? (да/нет):\033[0m ').strip().lower()
        if mode in ('да', 'нет'):
            break
        print('\033[31mВведите "да", если хотите изменить цену на всех складах, или "нет", чтобы изменить на одном')

    if mode == 'да':
        df.loc[df['Название'] == name, 'Цена за единицу'] = new_price
        print('\033[38;5;118mЦена успешно изменена на всех складах!')
        log_action(f'Изменена цена товара {name}: новая цена {new_price}')
        return

    storage = input('\033[38;5;229mСклад:\033[0m ')
    match_storage = matches[matches['Складское помещение'] == storage]
    if match_storage.empty:
        print('\033[31mНа этом складе данного товара нет! Изменение отменено')
        return

    df.loc[
        (df['Название'] == name) &(df['Складское помещение'] == storage),'Цена за единицу'] = new_price
    print('\033[38;5;118mЦена успешно изменена на выбранном складе!')
    log_action(f'Изменена цена товара {name}: новая цена {new_price}')


def stats():
    '''статистика'''
    print('\033[30;43m\nДоступная статистика:\033[0m')
    log_action('\033[36mПросмотр статистики')
    print('\033[33m1 — Общая стоимость всех товаров')
    print('2 — Средняя цена по категориям')
    print('3 — ТОП-5 самых дорогих')
    print('4 — Количество товаров категории')
    print('5 — Количество товаров на складе\n')
    while True:
        choice = input('\033[38;5;229mВыберите пункт (число 1-5): ').strip()
        if choice in ('1','2', '3', '4', '5'):
            break
    
    if choice == '1':
        total = (df['Количество'] * df['Цена за единицу']).sum()
        print('\033[38;5;217mОбщая стоимость всех товаров:', total)

    elif choice == '2':
        print('\033[38;5;217mСредняя цена по категориям:\033[38;5;217;48;5;236m')
        print(df.groupby('Категория')['Цена за единицу'].mean().to_frame().rename(columns={'Цена за единицу': ''}),'\033[0m')


    elif choice == '3':
        print('\033[38;5;217mТОП-5 самых дорогих:\033[38;5;217;48;5;236m')
        print(df.nlargest(5, 'Цена за единицу'),'\033[0m')

    elif choice == '4':
        cat = input('\033[38;5;229mКатегория: ')
        if cat not in df['Категория'].unique():
            print('\033[31mТакой категории нет в базе данных!')
            return
        print('\033[38;5;217mКоличество товаров в категории:', df[df['Категория'] == cat]['Количество'].sum()) 

    elif choice == '5':
        st = input('\033[38;5;229mСклад: ')
        if st not in df['Складское помещение'].unique():
            print('\033[31mТакого склада нет в базе данных!')
            return
        print('\033[38;5;217mКоличество товаров на складе:', df[df['Складское помещение'] == st]['Количество'].sum())


def filter_data():
    '''Фильтрация по категории или складу'''

    while True:
        f = input('\033[38;5;229mФильтр по (категория/склад): \033[0m').strip().lower()
        if f in ('категория', 'склад'):
            break
        print('\033[31mВведите "категория" или "склад"\033[37m')

    log_action(f'Фильтрация по {f}')
    if f == 'категория':
        cat = input('\033[38;5;229mВведите категорию: \033[0m').strip()
        if cat not in df['Категория'].unique():
            print('\033[31mТакой категории нет в базе данных!')
            return
        print('\033[38;5;217;48;5;236m', df[df['Категория'] == cat], '\033[0m')
        return

    if f == 'склад':
        st = input('\033[38;5;229mВведите склад: \033[0m').strip()
        if st not in df['Складское помещение'].unique():
            print('\033[31mТакого склада нет в базе данных!')
            return
        print('\033[38;5;217;48;5;236m',df[df['Складское помещение'] == st],'\033[0m')
        return


def order_products():
    '''Заказ'''

    print('\033[38;5;217;48;5;236m\n',df,'\033[0m')
    while True:
        try:
            while True:
                name = input('\033[38;5;229mНазвание товара: \033[0m')
                available = df[df['Название'] == name]
                if available.empty:
                    print('\033[31mТакого товара нет в базе данных! Повторите ввод')
                else:
                    break
            
            log_action(f'Оформление заказа: {name}')
            if available['Количество'].sum() == 0:
                print('\033[31mТовар закончился! Информация сохранена в out.txt')
                with open('out.txt', 'a', encoding='utf-8') as f:
                    f.write(f'{name} — закончился\n')
                log_action(f'{name} — закончился, запись в out.txt')

            else:
                if len(available) > 1:
                    print('\033[38;5;217mТовар есть на нескольких складах:')
                    print('\033[38;5;217;48;5;236m', available[['Складское помещение', 'Количество']], '\033[0m')
                    while True:
                        st = input('\033[38;5;229mВыберите склад: \033[0m')
                        if st in available['Складское помещение'].values:
                            break
                        print('\033[31mДанного склада нет в списке доступных!')
                else:
                    st = available['Складское помещение'].iloc[0]

                row = df[(df['Название'] == name) & (df['Складское помещение'] == st)]
                current_q = row['Количество'].iloc[0]

                if current_q == 0:
                    print('\033[31mНа выбранном складе товара нет! Информация сохранена в out.txt')
                    with open('C:\\Users\\Liza\\Downloads\\ицп\\out.txt', 'a', encoding='utf-8') as f:
                        f.write(f'{name} — закончился на складе {st}\n')
                    log_action(f'{name} — закончился на складе, запись в out.txt')
                else:
                    while True:
                        print(f'\n\033[38;5;217mВ наличии: {current_q}')
                        amount_s = input('\033[38;5;229mСколько нужно (число > 0): \033[0m')
                        if not amount_s.isdigit():
                            continue
                        amount = int(amount_s)
                        if amount < 1:
                            continue
                        if amount > current_q:
                            print('\033[31mНельзя заказать больше, чем есть в наличии!')
                            continue
                        break

                    df.loc[row.index, 'Количество'] = current_q - amount
                    print('\033[38;5;118mЗаказ успешно оформлен!')
                    log_action(f'Заказ оформлен: {name}, {amount} шт., склад {st}')
        except:
            print('\033[31mОшибка ввода!')

        while True:
            again = input('\n\033[38;5;229mВыбрать ещё товар? (да/нет): \033[0m').strip().lower()
            if again in ('да', 'нет'):
                break
            print('\033[31mВведите "да", если хотите выбрать ещё товар, или "нет", чтобы выйти из заказа!')
        if again == 'нет':
            break


def min_max_price_storage():
    '''Товары с минимальной и максимальной ценой на складе'''

    st = input('\033[38;5;229mВведите склад: \033[0m')
    subset = df[df['Складское помещение'] == st]
    if subset.empty:
        print('\033[31mТакого склада нет в базе данных!')
        return
    
    log_action(f'Запрос min/max цен на складе {st}')
    print('\033[38;5;217mМаксимальная цена:')
    print('\033[38;5;217;48;5;236m', subset.nlargest(1, 'Цена за единицу'), '\033[0m')
    print('\n\033[38;5;217mМинимальная цена:')
    print('\033[38;5;217;48;5;236m', subset.nsmallest(1, 'Цена за единицу'), '\033[0m')


def filter_by_price():
    '''Фильтрация по диапазону цен'''

    try:
        while True:
            try:
                low = float(input('\033[38;5;229m\nМинимальная цена:\033[0m '))
                high = float(input('\033[38;5;229mМаксимальная цена:\033[0m '))
            except ValueError:
                print('\033[31mВведите числовые значения!')
                continue
            if low > high:
                print('\033[31mМинимальная цена не может быть больше максимальной! Попробуйте снова')
                continue
            break
        
        log_action(f'Фильтрация по цене: {low} - {high}')
        result = df[(df['Цена за единицу'] >= low) & (df['Цена за единицу'] <= high)]

        if result.empty:
            print('\033[31mТовары в этом диапазоне не найдены!')
            return
        print('\033[38;5;217;48;5;236m', result, '\033[0m')

    except:
        pass

def export_to_csv():
    filename = input('\033[38;5;229m\nВведите имя файла для сохранения (например, data): \033[0m').strip()
    filename += '.csv'
    try:
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f'\033[38;5;118mДанные успешно сохранены в файл {filename}')
        log_action(f'Экспорт данных в CSV: {filename}')
    except:
        print('\033[31mОшибка при сохранении файла! Попробуйсте другое имя')



while True:
    print('\033[30;43m\nДоступные команды:\033[0m')
    print('\033[33m1 — показать весь склад')
    print('2 — добавить товар')
    print('3 — удалить товар')
    print('4 — изменить количество товара')
    print('5 — изменить цену товара')
    print('6 — статистика')
    print('7 — фильтрация по категории или складу')
    print('8 — заказать товар')
    print('9 — товары с мин/макс ценой на складе')
    print('10 — фильтрация по диапазону цены')
    print('11 — визуализация складов')
    print('12 — Экспорт данных в CSV')
    print('0 — выйти\n')

    command = input('\033[38;5;229mВведите номер команды (0-12):\033[0m ').strip()

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

    elif command == '11':
        print('\033[30;43m\nГрафики:\033[0m')
        print('\033[33m1 — Диаграмма заполненности складов')
        print('2 — График числа товаров')
        print('3 — График стоимости товаров на складе')
        print('4 — Круговая диаграмма доли категорий\n')
        while True:
            choice = input('\033[38;5;229mВыберите график (1-4):\033[0m ').strip()
            if choice in ('1', '2', '3', '4'):
                if choice == '1':
                    plot_storage_fill()
                elif choice == '2':
                    plot_total_items()
                elif choice == '3':
                    plot_storage_cost()
                elif choice == '4':
                    plot_category_share()
                break
            else:
                print('\033[91mКоманда не распознана! Введите число от 1 до 4\033[0m')

    elif command == '12':
        export_to_csv()

    elif command == '0':
        print('\033[38;5;118mРабота завершена!')
        break

    else:
        print('\033[31mКоманда не распознана! Введите число от 0 до 12\033[0m')
