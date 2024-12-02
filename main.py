from decimal import Decimal, getcontext

getcontext().prec = 35

text = "александровгеоргийолегович"

def calculate_frequencies(s):
    frequencies = {}
    for char in s:
        frequencies[char] = frequencies.get(char, 0) + 1
    return frequencies

def build_probability_table(frequencies, total_length):
    probability_table = {}
    cumulative_probability = Decimal(0)
    for char, freq in sorted(frequencies.items(), key=lambda x: -x[1]):  # Сортируем по частотам
        prob = Decimal(freq) / Decimal(total_length)
        probability_table[char] = (cumulative_probability, cumulative_probability + prob)
        cumulative_probability += prob
    return probability_table

def arithmetic_encoding(s, probability_table):
    left = Decimal(0)
    right = Decimal(1)
    for char in s:
        char_range = probability_table[char]
        range_width = right - left
        right = left + range_width * char_range[1]
        left = left + range_width * char_range[0]
        print(f"Символ: {char}, Левая граница: {left}, Правая граница: {right}")
    return left, right

def calculate_q_and_binary(left, right):
    interval_width = right - left
    q = (-interval_width.ln() / Decimal(2).ln()).quantize(Decimal('1'), rounding="ROUND_CEILING")
    scaled_left = (left * (Decimal(2) ** q)).quantize(Decimal('1'), rounding="ROUND_DOWN")
    scaled_right = (right * (Decimal(2) ** q)).quantize(Decimal('1'), rounding="ROUND_DOWN")
    return q, scaled_left, scaled_right

frequencies = calculate_frequencies(text)
probability_table = build_probability_table(frequencies, len(text))

print("\nТаблица вероятностей и интервалов:")
for char, (l, r) in probability_table.items():
    print(f"Символ: {char}, Вероятность: {Decimal(frequencies[char]) / len(text)}")

print("\nКодирование:")
left, right = arithmetic_encoding(text, probability_table)

q, scaled_left, scaled_right = calculate_q_and_binary(left, right)

print(f"q = {q}")
print("Границы для p:", left*Decimal(2)**q, right*Decimal(2)**q)


