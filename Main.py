import json
import re

acc_file = 'accounts.json'
base_pizza_price = 500


def load_accounts():
    try:
        with open(acc_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return []
            f.seek(0)
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Внимание: Файл аккаунтов поврежден или содержит невалидный JSON. Начинаем с чистого листа.")
        return []


def save_accounts(accounts_data):
    with open(acc_file, 'w', encoding='utf-8') as f:
        json.dump(accounts_data, f, indent=4, ensure_ascii=False)


def register():
    accounts = load_accounts()
    print("\n--- Регистрация ---")

    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    while True:
        email = input("Введите почту: ").strip()
        if re.match(email_regex, email):
            break
        print("Некорректный формат почты.")

    while True:
        name = input("Введите имя пользователя: ").strip()
        if not name: print("Имя не может быть пустым."); continue
        if any(acc['name'] == name for acc in accounts):
            print(f"Пользователь '{name}' уже существует.")
        else:
            break

    password_regex = r"^.{6,}$"
    while True:
        password = input("Введите пароль (мин. 6 символов): ").strip()
        if re.match(password_regex, password):
            break
        print("Пароль должен быть не менее 6 символов.")

    accounts.append({'email': email, 'name': name, 'password': password})
    save_accounts(accounts)
    print(f"\nАккаунт '{name}' успешно зарегистрирован!")


def login():
    accounts = load_accounts()
    print("\n--- Вход в аккаунт ---")
    name = input("Имя пользователя: ").strip()
    password = input("Пароль: ").strip()

    for account in accounts:
        if account['name'] == name and account['password'] == password:
            print(f"\nДобро пожаловать, {name}!")
            return name

    print("Неверное имя пользователя или пароль.")
    return None


def auth_handler():
    while True:
        choice = input(
            "\n--- Главное меню ---\n"
            "1. Регистрация\n"
            "2. Вход\n"
            "3. Выход\n"
            "Выберите действие: "
        ).strip()

        if choice == '1':
            register()
        elif choice == '2':
            user = login()
            if user:
                return user
        elif choice == '3':
            print("Выход из программы.")
            return None
        else:
            print("Неверный выбор. Пожалуйста, попробуйте еще раз.")


current_user = None

while True:
    if not current_user:
        current_user = auth_handler()
        if not current_user:
            break

    print(f"\n*** Добро пожаловать в основное приложение, {current_user}! ***\n"
          f"1. Заказать пиццу\n"
          f"2. Выйти из аккаунта\n"
          f"3. Завершить приложение\n")
    app_choice = input("Ваш выбор: ").strip()

    if app_choice == '1':
        pizza_orders = []
        drink_orders = []


        def say_hello(name):
            print(f"Привет {name}")


        def get_pizza_menu(current_age):
            if current_age <= 17:
                return {
                    1: 'пицца гаваи - 600р',
                    2: 'пицца пеперони - 450р',
                    3: 'пицца 4 сыра - 500р',
                    4: 'пицца с ананасами - 650р',
                    5: 'пицца с креветками - 700р',
                    6: 'кастомная пицца - 500'
                }
            else:
                return {
                    1: 'пицца гаваи - 700р',
                    2: 'пицца пеперони - 550р',
                    3: 'пицца 4 сыра - 600р',
                    4: 'пицца с ананасами - 750р',
                    5: 'пицца с креветками - 800р',
                    6: 'кастомная пицца - 400'

                }


        def get_drink_menu(current_age):
            if current_age <= 17:
                return {
                    1: 'вода - 25р',
                    2: 'лимонад - 75р',
                    3: 'кола - 125р',
                    4: 'пепси - 125р',
                    5: 'спрайт - 100р'
                }
            else:
                return {
                    1: 'вода - 30р',
                    2: 'лимонад - 90р',
                    3: 'кола - 150р',
                    4: 'пепси - 150р',
                    5: 'спрайт - 125р'
                }


        def total_cost_check(pizza_orders, drink_orders, pizza_menu, drink_menu):
            total_cost = 0

            for pizza_desc in pizza_orders:
                parts = pizza_desc.split(' - ')
                if len(parts) == 2:
                    price_str = parts[1].replace('р', '').strip()
                    price = int(price_str)
                    total_cost += price

            for drink_desc in drink_orders:
                parts = drink_desc.split(' - ')
                if len(parts) == 2:
                    price_str = parts[1].replace('р', '').strip()
                    price = int(price_str)
                    total_cost += price

            return total_cost


        def check(input_func):
            def output_func(*args, **kwargs):
                print('\n--- Ваш заказ ---')
                input_func(*args, **kwargs)
                print('--- Приятного дня! ---\n')

            return output_func


        @check
        def current_order():
            if not pizza_orders and not drink_orders:
                print('Пока что вы ничего не заказали')
            else:
                print('Пиццы:')
                if not pizza_orders:
                    print('Нет')
                for item in pizza_orders:
                    print(f'{item}')
                print('\nНапитки:')
                if not drink_orders:
                    print('нет')
                for item in drink_orders:
                    print(f'{item}')


        age = int(input('Введите свой возраст: '))

        current_menuP = get_pizza_menu(age)
        current_menuD = get_drink_menu(age)

        running = True
        while running:
            order_choice = int(input('1.Заказать пиццу\n'
                                     '2.Заказать напиток\n'
                                     '3.Изменить возраст\n'
                                     '4.Посмотреть чек\n'
                                     '5.Оплатить и выйти\n'
                                     'Что хотите сделать: '))
            if order_choice == 1:
                print('\nМеню пицц:')
                for item_num, item_desc in current_menuP.items():
                    print(item_num, item_desc)
                orderP_num = int(input('Какую пиццу хотите заказать: '))
                if orderP_num == 6:
                    pizza_ing = {
                        1: 'помидоры - 150р',
                        2: 'курица - 150р',
                        3: 'сыр - 200р',
                        4: 'пеперони - 200р',
                        5: 'грибы - 250р'
                    }
                    custom_run = True
                    while custom_run:
                        print(pizza_ing)
                        custom_add = int(input('Что хотите добавить: '))
                        if custom_add in pizza_ing:
                            print(f'ингредиент {pizza_ing[custom_add]} добавлен в пиццу')
                            if custom_add == 1:
                                base_pizza_price += 150
                                print(base_pizza_price)
                            elif custom_add == 2:
                                base_pizza_price += 150
                                print(base_pizza_price)
                            elif custom_add == 3:
                                base_pizza_price += 200
                                print(base_pizza_price)
                            elif custom_add == 4:
                                base_pizza_price += 200
                                print(base_pizza_price)
                            elif custom_add == 5:
                                base_pizza_price += 250
                                print(base_pizza_price)
                            print('1. добавить такию пиццу\n'
                                  '2. добавить ингредиентов')
                            end_customP_while = int(input('Что хотите сделать: '))
                            if end_customP_while == 1:
                                custom_run = False
                                current_custom_pizza = (f'кастомная пицца - {base_pizza_price}')
                                pizza_orders.append(current_custom_pizza)
                            else:
                                custom_run = True


                elif orderP_num in current_menuD:
                    pizza_orders.append(current_menuP[orderP_num])
                    print(f"'{current_menuP[orderP_num]}' добавлена в заказ")
                else:
                    print("Неверный номер пиццы")
            elif order_choice == 2:
                print('\nМеню напитков:')
                for item_num, item_desc in current_menuD.items():
                    print(item_num, item_desc)
                orderD_num = int(input('Какой напиток хотите заказать: '))
                if orderD_num in current_menuD:
                    drink_orders.append(current_menuD[orderD_num])
                    print(f"'{current_menuD[orderD_num]}' добавлен в заказ")
                else:
                    print("Неверный номер напитка")
            elif order_choice == 3:
                new_age = int(input('Напишите новый возраст: '))
                if new_age != age:
                    age = new_age
                    current_menuP = get_pizza_menu(age)
                    current_menuD = get_drink_menu(age)
                    print(f"Ваш возраст изменен на {age}, меню обновлено")
                else:
                    print("Возраст не изменился")
            elif order_choice == 4:
                total = total_cost_check(pizza_orders, drink_orders, current_menuP, current_menuD)
                print(f"\nОбщая стоимость заказа: {total}р")
                current_order()
            else:
                pay = int(input('Чем хотите оплатить?\n'
                                '1.наличка\n'
                                '2.карта'))
                if pay == 1:
                    pay_nal = int(input(f'С вас {total}р, сколько вы даёте: '))
                    if total > pay_nal:
                        print('недостаточно')
                    else:
                        pay_back = pay_nal - total
                        print(f'Ваша сдача {pay_back}')
                        print('Хорошего дня!')
                        running = False
                else:
                    print('Хорошего дня!')
                    running = False
    elif app_choice == '2':
        print(f"{current_user} вышел из аккаунта.")
        current_user = None
    elif app_choice == '3':
        print("Завершение работы приложения. До свидания!")
        break
    else:
        print("Неверный выбор.")