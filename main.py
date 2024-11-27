import copy

class Node:
    def __init__(self, name, children=None, value=None):
        self.name = name  # Имя узла для отображения
        self.children = children or []  # Список дочерних узлов
        self.value = value  # Значение узла (для листьев)
        self.minimax_value = None  # Вычисленное минимаксное значение

    def is_leaf(self):
        return len(self.children) == 0

def build_sample_tree():
    """
    Создает дерево с указанными узлами и значениями.
    """
    # Листовые узлы для A311
    A3111 = Node("A3111", value=4)
    A3112 = Node("A3112", value=6)
    A311 = Node("A311", children=[A3111, A3112])

    # Узел A312 (предположим, это лист без значения)
    A312 = Node("A312", value=5)  # Присвоим значение 5, если это лист

    # Узел A31
    A31 = Node("A31", children=[A311, A312])

    # Листовые узлы для A321
    A3211 = Node("A3211", value=2)
    A3212 = Node("A3212", value=9)
    A321 = Node("A321", children=[A3211, A3212])

    # Листовые узлы для A322
    A3221 = Node("A3221", value=-2)
    A3222 = Node("A3222", value=7)
    A322 = Node("A322", children=[A3221, A3222])

    # Узел A32
    A32 = Node("A32", children=[A321, A322])

    # Узел A3
    A3 = Node("A3", children=[A31, A32])

    # Остальные части дерева (как в оригинальном коде)
    # Уровень 5 (листья)
    A11111 = Node("A11111", value=3)
    A11112 = Node("A11112", value=5)
    A11121 = Node("A11121", value=2)
    A11122 = Node("A11122", value=9)
    A11211 = Node("A11211", value=0)
    A11212 = Node("A11212", value=-1)
    A11221 = Node("A11221", value=4)
    A11222 = Node("A11222", value=7)

    # Уровень 4
    A1111 = Node("A1111", children=[A11111, A11112])
    A1112 = Node("A1112", children=[A11121, A11122])
    A1121 = Node("A1121", children=[A11211, A11212])
    A1122 = Node("A1122", children=[A11221, A11222])

    # Уровень 3
    A111 = Node("A111", children=[A1111, A1112])
    A112 = Node("A112", children=[A1121, A1122])

    # Уровень 2
    A11 = Node("A11", children=[A111, A112])
    A12 = Node("A12", children=[
        Node("A121", value=6),
        Node("A122", value=1)
    ])

    # Узел A1
    A1 = Node("A1", children=[A11, A12])

    # Узел A2
    A21 = Node("A21", value=8)
    A221 = Node("A221", value=5)
    A222 = Node("A222", value=3)
    A22 = Node("A22", children=[A221, A222])
    A2 = Node("A2", children=[A21, A22])

    # Корневой узел
    root = Node("Root", children=[A1, A2, A3])

    return root

def print_tree(node, depth=0):
    indent = "  " * depth
    value_str = f", Value: {node.value}" if node.value is not None else ""
    minimax_str = f", Minimax: {node.minimax_value}" if node.minimax_value is not None else ""
    print(f"{indent}{node.name}{value_str}{minimax_str}")
    for child in node.children:
        print_tree(child, depth + 1)

def minimax(node, is_maximizing, debug_info, order='left-to-right'):
    if node.is_leaf():
        node.minimax_value = node.value
        debug_info['evaluated_nodes'].append((node.name, node.value))
        return node.value

    # Изменение порядка обхода детей
    children = node.children if order == 'left-to-right' else list(reversed(node.children))

    if is_maximizing:
        max_eval = float('-inf')
        debug_info['current_player'].append('MAX')
        for child in children:
            eval = minimax(child, False, debug_info, order)  # Инвертируем is_maximizing
            max_eval = max(max_eval, eval)
        node.minimax_value = max_eval
        debug_info['intermediate_values'].append((node.name, max_eval))
        debug_info['current_player'].pop()
        return max_eval
    else:
        min_eval = float('inf')
        debug_info['current_player'].append('MIN')
        for child in children:
            eval = minimax(child, True, debug_info, order)  # Инвертируем is_maximizing
            min_eval = min(min_eval, eval)
        node.minimax_value = min_eval
        debug_info['intermediate_values'].append((node.name, min_eval))
        debug_info['current_player'].pop()
        return min_eval

def alpha_beta(node, is_maximizing, alpha, beta, debug_info, order='left-to-right'):
    if node.is_leaf():
        node.minimax_value = node.value
        debug_info['evaluated_nodes'].append((node.name, node.value))
        return node.value

    # Изменение порядка обхода детей
    children = node.children if order == 'left-to-right' else list(reversed(node.children))

    if is_maximizing:
        max_eval = float('-inf')
        debug_info['current_player'].append('MAX')
        for child in children:
            eval = alpha_beta(child, False, alpha, beta, debug_info, order)  # Инвертируем is_maximizing
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                debug_info['pruned_branches'].append((node.name, child.name))
                break
        node.minimax_value = max_eval
        debug_info['intermediate_values'].append((node.name, max_eval))
        debug_info['current_player'].pop()
        return max_eval
    else:
        min_eval = float('inf')
        debug_info['current_player'].append('MIN')
        for child in children:
            eval = alpha_beta(child, True, alpha, beta, debug_info, order)  # Инвертируем is_maximizing
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                debug_info['pruned_branches'].append((node.name, child.name))
                break
        node.minimax_value = min_eval
        debug_info['intermediate_values'].append((node.name, min_eval))
        debug_info['current_player'].pop()
        return min_eval

def change_leaf_values(node):
    if node.is_leaf():
        while True:
            try:
                new_value = int(input(f"Введите новое значение для листа {node.name} (текущее: {node.value}): "))
                node.value = new_value
                break
            except ValueError:
                print("Неверный ввод. Пожалуйста, введите целое число.")
    else:
        for child in node.children:
            change_leaf_values(child)

def get_player_order():
    while True:
        choice = input("Установить роль корня как MAX или MIN? (Введите MAX/MIN): ").strip().upper()
        if choice in ['MAX', 'MIN']:
            return choice
        else:
            print("Неверный выбор. Пожалуйста, введите MAX или MIN.")

def get_analysis_order():
    while True:
        choice = input("Выберите порядок анализа детей: 1. Слева-направо  2. Справа-налево (Введите 1 или 2): ").strip()
        if choice == '1':
            return 'left-to-right'
        elif choice == '2':
            return 'right-to-left'
        else:
            print("Неверный выбор. Пожалуйста, введите 1 или 2.")
def main():
    root = build_sample_tree()
    player_role = 'MAX'  # По умолчанию корень - MAX
    analysis_order = 'left-to-right'  # По умолчанию слева-направо

    while True:
        print("\nМеню:")
        print("1. Изменить оценки листьев дерева")
        print("2. Изменить порядок ходов игроков (MIN/MAX)")
        print("3. Изменить порядок анализа листьев дерева (слева-направо / справа-налево)")
        print("4. Выполнить минимаксный алгоритм")
        print("5. Выполнить алгоритм с альфа-бета отсечениями")
        print("6. Показать дерево")
        print("0. Выход")

        choice = input("Выберите опцию: ")

        if choice == '1':
            change_leaf_values(root)
            print("Оценки листьев обновлены.")
        elif choice == '2':
            player_role = get_player_order()
            print(f"Роль корня установлена как {player_role}.")
        elif choice == '3':
            analysis_order = get_analysis_order()
            print(
                f"Порядок анализа детей установлен как {'Слева-направо' if analysis_order == 'left-to-right' else 'Справа-налево'}.")
        elif choice == '4':
            debug_info = {'evaluated_nodes': [], 'intermediate_values': [], 'current_player': []}

            # Определяем, является ли корень MAX или MIN
            is_maximizing = True if player_role == 'MAX' else False

            minimax(root, is_maximizing, debug_info, analysis_order)
            print("\nРезультаты минимаксного анализа:")
            print("Промежуточные оценки:")
            for name, value in debug_info['intermediate_values']:
                print(f"Узел {name}: {value}")
            print("Оцененные листья:")
            for name, value in debug_info['evaluated_nodes']:
                print(f"Лист {name}: {value}")
            print(f"Выбранное значение корня: {root.minimax_value}")
        elif choice == '5':
            debug_info = {'evaluated_nodes': [], 'intermediate_values': [], 'pruned_branches': [], 'current_player': []}

            # Определяем, является ли корень MAX или MIN
            is_maximizing = True if player_role == 'MAX' else False

            alpha_beta(root, is_maximizing, float('-inf'), float('inf'), debug_info, analysis_order)
            print("\nРезультаты анализа с альфа-бета отсечениями:")
            print("Промежуточные оценки:")
            for name, value in debug_info['intermediate_values']:
                print(f"Узел {name}: {value}")
            print("Оцененные листья:")
            for name, value in debug_info['evaluated_nodes']:
                print(f"Лист {name}: {value}")
            print("Отсеченные ветви:")
            for parent, child in debug_info['pruned_branches']:
                print(f"Ветвь {child} отсечена от узла {parent}")
            print(f"Выбранное значение корня: {root.minimax_value}")
        elif choice == '6':
            print("\nТекущее дерево:")
            print_tree(root)
        elif choice == '0':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()