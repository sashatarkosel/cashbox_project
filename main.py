import tkinter as tk
import ast
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

root = tk.Tk()
root.title("Калькулятор сдачи")
root.geometry("1000x1080")

def show_new_cashbox_window():
    global new_cashbox_window, all_column_labels_new_window
    new_cashbox_window = tk.Toplevel(root)
    new_cashbox_window.title('Ввод новой кассы')
    new_cashbox_window.geometry('710x300')

    all_column_labels_new_window = {d: [] for d in DENOMS}

    tk.Button(new_cashbox_window, text='Подтвердить', font=('Arial', 18), command=submit_changes).grid(row=3, column=0, columnspan=11)

    for idx, denom in enumerate(DENOMS):
        label = tk.Label(new_cashbox_window, text=str(denom), font=("Arial", 18), relief="solid", borderwidth=1, width=2*k, height=1*k)
        label.grid(row=1, column=idx)
        all_column_labels_new_window[denom].append(label)

        entry = tk.Entry(new_cashbox_window, font=("Arial", 20), relief='solid', borderwidth=1, width=2*k)
        entry.insert(0, cashbox[denom])
        entry.grid(row=2, column=idx)
        all_column_labels_new_window[denom].append(entry)
    

def submit_changes():
    global new_cashbox
    new_cashbox = {d: 0 for d in DENOMS}
    for denom in DENOMS:
        new_cashbox[denom] = int(all_column_labels_new_window[denom][1].get())
    if new_cashbox == cashbox:
        new_cashbox_window.destroy()
    else:
        cashbox_history.append(new_cashbox)
        listbox.insert(tk.END, new_cashbox)
        go_back('', 'calculate')
        new_cashbox_window.destroy()




def delete_listbox_element():
    global all_cnt, cnt, index, cashbox
    index = listbox.curselection()
    if index:
        listbox.delete(index)
        index = index[0]
        del cashbox_history[index]
        if cnt == all_cnt:
            all_cnt -= 1
            cnt -= 1
            cashbox = cashbox_history[index - 1]
            cashbox_label_update()
        else:
            all_cnt -= 1
        count_label.config(text=f'{cnt}/{all_cnt}')

def create_listbox():
    global listbox
    # Создаём Listbox
    listbox = tk.Listbox(root, font=("Arial", 14))
    listbox.grid(row=0, column=6, rowspan=4)
    listbox.bind('<Double-1>', lambda event: go_back(event, direction='click'))

    items = cashbox_history
    for item in items:
        listbox.insert(tk.END, item)

def create_labels():
    global count_label, entry, alarm_label, cashbox_label, change_label, user_input_label

    alarm_label = tk.Label(root, text='Нельзя выдать сдачу', font=("Arial", 18))

    cashbox_label = tk.Label(root, text=f'Всего в кассе: {cashbox_sum}')
    cashbox_label.grid(row=12, column=4)

    change_label = tk.Label(root, text=f'Сумма Сдачи: 0')
    change_label.grid(row=12, column=5)

    user_input_label = tk.Label(root, text=f'Покупатель дал: 0')
    user_input_label.grid(row=13, column=5)

    tk.Button(root, text='←', font=("Arial", 20), command=lambda event=None: go_back(event, 'left')).grid(row=11, column=3)
    root.bind('<Left>', lambda event: go_back(event, 'left'))
    tk.Button(root, text='→', font=("Arial", 20), command=lambda event=None: go_back(event, 'right')).grid(row=11, column=5)
    root.bind('<Right>', lambda event: go_back(event, 'right'))

    tk.Button(root, text='Рассчитать сдачу', font=("Arial", 13), command=lambda event=None: update_change(event)).grid(row=12, column=0, columnspan=3)
    root.bind('<Return>', update_change)

    tk.Button(root, text='Очистить Всё', font=("Arial", 13), command=lambda event=None: reset_all(event)).grid(row=13, column=0, columnspan=3)
    root.bind('<Delete>', reset_all)

    count_label = tk.Label(root, text=f'{cnt}/{all_cnt}', font=("Arial", 20), relief='solid')
    count_label.grid(row=11, column=4)

    entry = tk.Entry(root, font=("Arial", 18), width=12)
    entry.grid(row=11, column=0, columnspan=3, rowspan=1)
    
    for idx, denom in enumerate(DENOMS):
        label1 = tk.Label(root, text=str(denom), font=("Arial", 18), relief="solid", borderwidth=1, width=2*k, height=1*k)
        label1.grid(row=idx, column=1)
        all_column_labels[denom].append(label1)

        label2 = tk.Label(root, text=user_input[denom], font=("Arial", 18), relief="solid", borderwidth=1, width=2*k, height=1*k)
        label2.grid(row=idx, column=3)
        all_column_labels[denom].append(label2)

        label3 = tk.Label(root, text=cashbox[denom], font=("Arial", 18), relief="solid", borderwidth=1, width=2*k, height=1*k)
        label3.grid(row=idx, column=4, padx=15)
        all_column_labels[denom].append(label3)

        label4 = tk.Label(root, text=change[denom], font=("Arial", 18), relief="solid", borderwidth=1, width=2*k, height=1*k)
        label4.grid(row=idx, column=5, padx=15)
        all_column_labels[denom].append(label4)

        tk.Button(root, text='-', font=("Arial", 14), relief="solid", borderwidth=1, width=4, height=1*k, command=lambda d=denom: plus_one('-', d)).grid(row=idx, column=0)
        tk.Button(root, text='+', font=("Arial", 14), relief="solid", borderwidth=1, width=4, height=1*k, command=lambda d=denom: plus_one("+", d)).grid(row=idx, column=2)

        tk.Button(root, text='Удалить', font=("Arial", 18), relief="solid", borderwidth=2, bg='red', activebackground='darkred', 
                  command=delete_listbox_element).grid(row=4, column=6)
        
        tk.Button(root, text='Изменить кассу', font=('Arial', 18), relief='solid', borderwidth=2, command=show_new_cashbox_window).grid(row=5, column=6)

def calculate_change(amount): 
    result = {d: 0 for d in DENOMS}  # Инициализируем словарь с нулями

    for denom in DENOMS[::-1]:  # Проходим по номиналам в обратном порядке
        # Проверяем, есть ли такая купюра в кассе
        if cashbox:
            # Считаем сколько раз можно использовать текущую купюру
            result[denom] = min(amount // denom, cashbox[denom])
            # Уменьшаем оставшуюся сумму
            amount -= result[denom] * denom

    # Проверяем, если оставшаяся сумма больше 0, то сдачу нельзя выдать
    if amount > 0:
        return None  # Если не удалось разложить всю сумму, возвращаем None
    
    return result

def get_entry_value():
    entry_value = entry.get()
    if entry_value.strip() == "":
        total_sum = 0
    else:
        try:
            total_sum = int(entry_value)
        except ValueError:
            total_sum = 0
    return total_sum

def dict_sum(dict: dict):
    cnt = 0
    for denom in DENOMS:
        cnt += dict[denom] * denom
    return cnt

def update_change(event):
    global change, new_cashbox
    entry_value = get_entry_value()
    user_give = dict_sum(user_input) # int
    change = calculate_change(user_give - entry_value)
    if change != None:
        alarm_label.grid_forget()
        change_sum = dict_sum(change)
        new_cashbox = {d:0 for d in DENOMS}
        for denom in DENOMS:
            current_digit = cashbox[denom] - change[denom] + user_input[denom]
            new_cashbox[denom] = current_digit
        cashbox_history.append(new_cashbox)
        listbox.insert(tk.END, new_cashbox)
        go_back(event, 'calculate')
        for denom in DENOMS:
            all_column_labels[denom][3].config(text=change[denom])
    else:
        change_sum = 0
        alarm_label.grid(row=0, column=7)
        for denom in DENOMS:
            all_column_labels[denom][3].config(text='0')
    change_label.config(text=f'Сумма сдачи {change_sum}')
    change_label.grid(row=12, column=5)

def plus_one(flag, denom):
    global user_input
    if flag == '-':
        user_input[denom] -= 1
        all_column_labels[denom][1].config(text=user_input[denom])
        
    elif flag == '+':
        user_input[denom] += 1
        all_column_labels[denom][1].config(text=user_input[denom])
    user_input_sum = dict_sum(user_input)
    user_input_label.config(text=f'Покупатель дал: {user_input_sum}')

# Файл должен менять словарь cashbox при каждом изменении
def go_back(event, direction: str):
    global cnt, all_cnt, cashbox, cashbox_history
    if direction == 'left' and cnt > 1:
        # Логика для перехода назад в истории
        cnt -= 1
        count_label.config(text=f'{cnt}/{all_cnt}')
        cashbox = cashbox_history[cnt-1]
        cashbox_sum = dict_sum(cashbox)
        cashbox_label.config(text=f'Всего в кассе: {cashbox_sum}')
        for denom in DENOMS:
            all_column_labels[denom][2].config(text=cashbox[denom])
    elif direction == 'right' and cnt < all_cnt:
        # Логика для перехода вперед в истории
        cnt += 1
        count_label.config(text=f'{cnt}/{all_cnt}')
        cashbox = cashbox_history[cnt-1]
        cashbox_sum = dict_sum(cashbox)
        cashbox_label.config(text=f'Всего в кассе: {cashbox_sum}')
        for denom in DENOMS:
            all_column_labels[denom][2].config(text=cashbox[denom])
    elif direction == 'calculate':
        all_cnt += 1
        cnt = all_cnt
        cashbox = new_cashbox
        cashbox_label_update()
    elif direction == 'click':
        index = listbox.curselection()[0]
        cashbox = cashbox_history[index]
        cnt = index + 1
        cashbox_label_update()

def cashbox_label_update():
    count_label.config(text=f'{cnt}/{all_cnt}')
    cashbox_sum = dict_sum(cashbox)
    cashbox_label.config(text=f'Всего в кассе: {cashbox_sum}')
    for denom in DENOMS:
        all_column_labels[denom][2].config(text=cashbox[denom])

def reset_all(event):
    for denom in DENOMS:
        user_input[denom] = 0
        all_column_labels[denom][1].config(text=user_input[denom])

with open('history.txt', 'r+') as file:
# Открываем файл с историей кассы и добавляем его содержимое в cashbox_history
    lines = file.readlines()
    cashbox_history_str = [line.strip() for line in lines]
    cashbox_history = []
    for elem in cashbox_history_str:
        cashbox_history.append(ast.literal_eval(elem))

    DENOMS = [1, 2, 5, 10, 50, 100, 200, 500, 1000, 2000, 5000] # Список номиналов
    all_column_labels = {d: [] for d in DENOMS}
    user_input = {d: 0 for d in DENOMS}
    change = {d: 0 for d in DENOMS}
    change_sum = dict_sum(change)

    cnt = len(cashbox_history) # Индекс последнего элемента в истории
    all_cnt = cnt
    cashbox = cashbox_history[cnt - 1]  # Берем последний элемент истории как текущую кассу
    cashbox_sum = dict_sum(cashbox)
    k = 2  # Коэффициент для масштабирования элементов интерфейса
    
    create_labels()
    create_listbox()

    if __name__ == "__main__":
        root.mainloop()

    # Перемещаем курсор в начало файла
    file.seek(0)
    
    # Очищаем содержимое файла
    file.truncate(0)

    # Обновляем историю
    for history in cashbox_history:
        file.write(str(history) + '\n')

    # Закрываем файл
    file.close()


