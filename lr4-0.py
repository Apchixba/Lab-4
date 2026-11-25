
class Item:
    def __init__(self, name, weight, value):
        self.name = name
        self.weight = weight
        self.value = value


def knapsack(items, capacity):
    def node_bound_count(i, weight, value):
        if weight > capacity:
            return 0

        bound_value = value
        j = i
        total_weight = weight

        while j < len(items) and total_weight + items[j].weight <= capacity:
            bound_value += items[j].value
            total_weight += items[j].weight
            j += 1

        if j < len(items):
            bound_value += (capacity - total_weight) * (
                items[j].value / items[j].weight
            )

        return bound_value

    def branch_bound(i, weight, value, selected):
        nonlocal max_value, best_combination

        if weight <= capacity and value > max_value:
            max_value = value
            best_combination = selected[:]

        if i == len(items):
            return

        if node_bound_count(i, weight, value) <= max_value:
            return

        if weight + items[i].weight <= capacity:
            selected.append(items[i])
            branch_bound(
                i + 1,
                weight + items[i].weight,
                value + items[i].value,
                selected
            )
            selected.pop()

        branch_bound(i + 1, weight, value, selected)

    items = sorted(
        items,
        key=lambda item: item.value / item.weight,
        reverse=True
    )

    max_value = 0
    best_combination = []

    branch_bound(0, 0, 0, [])

    return max_value, best_combination


def find_all_combinations(items, capacity, start_score, total_value):
    combinations = []

    for mask in range(1 << len(items)):
        selected = [
            items[i]
            for i in range(len(items))
            if mask & (1 << i)
        ]

        total_weight = sum(item.weight for item in selected)
        total_selected_value = sum(item.value for item in selected)

        if total_weight > capacity:
            continue

        score = start_score + total_selected_value - (
            total_value - total_selected_value
        )

        if score > 0:
            combinations.append((selected, total_weight, score))

    return combinations


if __name__ == '__main__':
    items = [
        Item('r', 3, 25),
        Item('p', 2, 15),
        Item('a', 2, 15),
        Item('m', 2, 20),
        Item('i', 1, 5),
        Item('k', 1, 15),
        Item('x', 3, 20),
        Item('t', 1, 25),
        Item('f', 1, 15),
        Item('d', 1, 10),
        Item('s', 2, 20),
        Item('c', 2, 20)
    ]

    capacity = 9
    start_score = 10
    total_value = sum(item.value for item in items)

    max_value, best_combination = knapsack(items, capacity)

    score = start_score + max_value - (total_value - max_value)

    print('Оптимальное решение:')
    print('Выбранные предметы:', [item.name for item in best_combination])
    print('Суммарная ценность:', max_value)
    print('Суммарный вес:', sum(item.weight for item in best_combination))
    print('Итоговые очки выживания:', score)

    inventory = []

    for item in best_combination:
        inventory.extend([item.name] * item.weight)

    print('\nИнвентарь 3x3:')

    for i in range(0, 9, 3):
        print(','.join(f'[{name}]' for name in inventory[i:i + 3]))

    all_combinations = find_all_combinations(
        items, capacity, start_score, total_value
    )

    print('\nВсе комбинации с положительным счётом:')
    print('Количество комбинаций:', len(all_combinations))

    for number, (selected, weight, result_score) in enumerate(
        all_combinations, 1
    ):
        names = [item.name for item in selected]
        print(
            number,
            names,
            'Вес:', weight,
            'Очки:', result_score
        )

    seven_capacity = 7

    seven_value, seven_combination = knapsack(items, seven_capacity)

    seven_score = start_score + seven_value - (
        total_value - seven_value
    )

    if seven_score <= 0:
        print(f'\nПоложительного решения для 7 ячеек нет.(Итоговый счет {seven_score} < 0)')
    else:
        print('\nПоложительное решение существует.')
