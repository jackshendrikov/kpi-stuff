from math import sqrt
from time import process_time
from scipy.stats import f, t
from functools import partial
from random import randrange
from numpy.linalg import solve

x1, x2, x3 = [-25, -5], [15, 50], [-25, -15]
m, N, l = 2, 15, 1.73  # кількість повторень кожної комбінації &  кількість повторення дослідів

x_avg = [(max(x1) + max(x2) + max(x3)) / 3, (min(x1) + min(x2) + min(x3)) / 3]  # Xcр(max) & Xср(min)
xo = [(min(x1) + max(x1)) / 2, (min(x2) + max(x2)) / 2, (min(x3) + max(x3)) / 2]  # Xoi
delta_x = [max(x1) - xo[0], max(x1) - xo[1], max(x1) - xo[2]]  # delta Xi

y_range = [200 + int(max(x_avg)), 200 + int(min(x_avg))]  # Yi(max) & Yi(min)

xn = [[-1, -1, -1, -1, +1, +1, +1, +1, -1.73, 1.73, 0, 0, 0, 0, 0], # нормовані значення факторів
      [-1, -1, +1, +1, -1, -1, +1, +1, 0, 0, -1.73, 1.73, 0, 0, 0],
      [-1, +1, -1, +1, -1, +1, -1, +1, 0, 0, 0, 0, -1.73, 1.73, 0]]

xx = [[int(x * y) for x, y in zip(xn[0], xn[1])],  # нормовані значення факторів для ефекту взаємодії
      [int(x * y) for x, y in zip(xn[0], xn[2])],
      [int(x * y) for x, y in zip(xn[1], xn[2])]]

xxx = [int(x * y * z) for x, y, z in zip(xn[0], xn[1], xn[2])]

x_xn = [[round(xn[j][i] ** 2, 3) for i in range(N)] for j in range(3)]  # нормовані знач. факторів для квад. членів

x = [[min(x1), min(x1), min(x1), min(x1), max(x1), max(x1), max(x1), max(x1), round(-l * delta_x[0] + xo[0], 3),
      round(l * delta_x[0] + xo[0], 3), xo[0], xo[0], xo[0], xo[0], xo[0]],  # натуральні значення факторів
     [min(x2), min(x2), max(x2), max(x2), min(x2), min(x2), max(x2), max(x2), xo[1], xo[1],
      round(-l * delta_x[1] + xo[1], 3), round(l * delta_x[1] + xo[1], 3), xo[1], xo[1], xo[1]],
     [min(x3), max(x3), min(x3), max(x3), max(x3), min(x3), max(x3), min(x3), xo[2], xo[2], xo[2], xo[2],
      round(-l * delta_x[2] + xo[2], 3), round(l * delta_x[2] + xo[2], 3), xo[2]]]

xx2 = [[round(x * y, 3) for x, y in zip(x[0], x[1])],  # натуральні значення факторів для ефекту взаємодії
       [round(x * y, 3) for x, y in zip(x[0], x[2])],
       [round(x * y, 3) for x, y in zip(x[1], x[2])]]

xxx2 = [round(x * y * z, 3) for x, y, z in zip(x[0], x[1], x[2])]

x_x = [[round(x[j][i] ** 2, 3) for i in range(N)] for j in range(3)]  # натуральні значення факторів для квадрат. членів

while True:
    start_time = process_time()
    # формування Y
    y = [[round(3.5 + 6.6 * x[0][j] + 5.3 * x[1][j] + 5 * x[2][j] + 5.1 * x[0][j] * x[0][j] + 0.1 * x[1][j] * x[1][j] +
                7.2 * x[2][j] * x[2][j] + 1.4 * x[0][j] * x[1][j] + 0.7 * x[0][j] * x[2][j] + 4.2 * x[1][j] * x[2][j] +
                7.7 * x[0][j] * x[1][j] * x[2][j] + randrange(0, 10) - 5, 2) for i in range(m)] for j in range(N)]
    arr_avg = lambda arr: round(sum(arr) / len(arr), 4)
    y_avg = list(map(arr_avg, y))  # середнє значення Y

    dispersions = [sum([((y[i][j] - y_avg[i]) ** 2) / m for j in range(m)]) for i in range(N)]  # дисперсії по рядках
    x_matrix = x + xx2 + [xxx2] + x_x  # повна матриця з натуральними значеннями факторів
    norm_matrix = xn + xx + [xxx] + x_xn  # повна матриця з нормованими значеннями факторів

    mx = list(map(arr_avg, x_matrix))  # середні значення х по колонкам
    my = sum(y_avg) / N  # середнє значення Y_avg

    # ======================================== Форматування таблиці ====================================================

    table_factors_1 = ["X1", "X2", "X3"]
    table_factors_2 = ["X1X2", "X1X3", "X2X3", "X1X2X3", "X1^2", "X2^2", "X3^2"]
    table_y = ["Y{}".format(i + 1) for i in range(m)]
    other = ["#", "Y"]

    header_format_norm = "+{0:=^3}" + "+{0:=^8}" * (len(table_factors_1)) + "+{0:=^8s}" * (len(table_factors_2))
    header_format = "+{0:=^3}" + "+{0:=^8}" * (len(table_factors_1)) + "+{0:=^10s}" * (len(table_factors_2)) + "+{0:=^10s}" * (len(table_y)) + "+{0:=^10s}"
    row_format_norm = "|{:^3}" + "|{:^8}" * (len(table_factors_1)) + "|{:^8}" * (len(table_factors_2))
    row_format = "|{:^3}" + "|{:^8}" * (len(table_factors_1)) + "|{:^10}" * (len(table_factors_2)) + "|{:^10}" * (len(table_y)) + "|{:^10}"
    separator_format_norm = "+{0:-^3s}" + "+{0:-^8s}" * (len(table_factors_1)) + "+{0:-^8s}" * (len(table_factors_2))
    separator_format = "+{0:-^3s}" + "+{0:-^8s}" * (len(table_factors_1)) + "+{0:-^10s}" * (len(table_factors_2)) + "+{0:-^10s}" * (len(table_y)) + "+{0:-^10s}"
    my_sep_norm = "|{:^93s}|\n"
    my_sep = "|{:^140s}|\n" if m == 2 else "|{:^151s}|\n"
    # ======================================== Нормальні значення ======================================================
    print(header_format_norm.format("=") + "+\n" + my_sep_norm.format("Матриця ПФЕ (нормальні значення факторів)") +
          header_format_norm.format("=") + "+\n" + row_format_norm.format(other[0], *table_factors_1, *table_factors_2)
          + "|\n" + header_format_norm.format("=") + "+")

    for i in range(N):
        print("|{:^3}|".format(i + 1), end="")
        for j in range(3): print("{:^+8}|".format(xn[j][i]), end="")
        for j in range(3): print("{:^+8}|".format(xx[j][i]), end="")
        print("{:^+8}|".format(xxx[i]), end="")
        for j in range(3): print("{:^+8}|".format(x_xn[j][i]), end="")
        print()

    print(separator_format_norm.format("-") + "+\n\n")

    # ======================================== Натуральні значення =====================================================
    print(header_format.format("=") + "+\n" + my_sep.format("Матриця ПФЕ (натуральні значення факторів)") +
          header_format.format("=") + "+\n" + row_format.format(other[0], *table_factors_1, *table_factors_2, *table_y,
                                                                other[1]) + "|\n" + header_format.format("=") + "+")

    for i in range(N):
        print("|{:^3}|".format(i + 1), end="")
        for j in range(3): print("{:^ 8}|".format(x[j][i]), end="")
        for j in range(3): print("{:^ 10}|".format(xx2[j][i]), end="")
        print("{:^ 10}|".format(xxx2[i]), end="")
        for j in range(3): print("{:^ 10}|".format(x_x[j][i]), end="")
        for j in range(m): print("{:^ 10}|".format(y[i][j]), end="")
        print("{:^10.2f}|".format(y_avg[i]))


    def a(first, second): return sum([x_matrix[first - 1][j] * x_matrix[second - 1][j] / N for j in range(N)])
    def find_a(num): return sum([y_avg[j] * x_matrix[num - 1][j] / N for j in range(N)])
    def check(b_lst, k):
        return b_lst[0] + b_lst[1] * x_matrix[0][k] + b_lst[2] * x_matrix[1][k] + b_lst[3] * x_matrix[2][k] + \
               b_lst[4] * x_matrix[3][k] + b_lst[5] * x_matrix[4][k] + b_lst[6] * x_matrix[5][k] + \
               b_lst[7] * x_matrix[6][k] + b_lst[8] * x_matrix[7][k] + b_lst[9] * x_matrix[8][k] + \
               b_lst[10] * x_matrix[9][k]

    unknown = [[1, mx[0], mx[1], mx[2], mx[3], mx[4], mx[5], mx[6], mx[7], mx[8], mx[9]],  # ліва частина рівнянь з невідомими для пошуку коефіцієнтів b (приклад в методі)
               [mx[0], a(1, 1), a(1, 2), a(1, 3), a(1, 4), a(1, 5), a(1, 6), a(1, 7), a(1, 8), a(1, 9), a(1, 10)],
               [mx[1], a(2, 1), a(2, 2), a(2, 3), a(2, 4), a(2, 5), a(2, 6), a(2, 7), a(2, 8), a(2, 9), a(2, 10)],
               [mx[2], a(3, 1), a(3, 2), a(3, 3), a(3, 4), a(3, 5), a(3, 6), a(3, 7), a(3, 8), a(3, 9), a(3, 10)],
               [mx[3], a(4, 1), a(4, 2), a(4, 3), a(4, 4), a(4, 5), a(4, 6), a(4, 7), a(4, 8), a(4, 9), a(4, 10)],
               [mx[4], a(5, 1), a(5, 2), a(5, 3), a(5, 4), a(5, 5), a(5, 6), a(5, 7), a(5, 8), a(5, 9), a(5, 10)],
               [mx[5], a(6, 1), a(6, 2), a(6, 3), a(6, 4), a(6, 5), a(6, 6), a(6, 7), a(6, 8), a(6, 9), a(6, 10)],
               [mx[6], a(7, 1), a(7, 2), a(7, 3), a(7, 4), a(7, 5), a(7, 6), a(7, 7), a(7, 8), a(7, 9), a(7, 10)],
               [mx[7], a(8, 1), a(8, 2), a(8, 3), a(8, 4), a(8, 5), a(8, 6), a(8, 7), a(8, 8), a(8, 9), a(8, 10)],
               [mx[8], a(9, 1), a(9, 2), a(9, 3), a(9, 4), a(9, 5), a(9, 6), a(9, 7), a(9, 8), a(9, 9), a(9, 10)],
               [mx[9], a(10, 1), a(10, 2), a(10, 3), a(10, 4), a(10, 5), a(10, 6), a(10, 7), a(10, 8), a(10, 9), a(10, 10)]]
    known = [my, find_a(1), find_a(2), find_a(3), find_a(4), find_a(5), find_a(6), find_a(7), find_a(8), find_a(9), find_a(10)]  # знаходення відомих значень a1, a2, ...

    b = solve(unknown, known)
    print(separator_format.format("-") + f"+\n\n\tОтримане рівняння регресії при m={m}:\n"
                                         f"ŷ = {b[0]:.3f} + {b[1]:.3f}*X1 + {b[2]:.3f}*X2 + "
                                         f"{b[3]:.3f}*X3 + {b[4]:.3f}*X1X2 + {b[5]:.3f}*X1X3 + "
                                         f"{b[6]:.3f}*X2X3 + {b[7]:.3f}*X1X2X3 + {b[8]:.3f}*X11^2 + "
                                         f"{b[9]:.3f}*X22^2 + {b[10]:.3f}*X33^2\n\n\tПеревірка:")
    for i in range(N): print("ŷ{} = {:.3f} ≈ {:.3f}".format((i + 1), check(b, i), y_avg[i]))

    # ======================================== Критерій Кохрена ========================================================
    def table_fisher(prob, n, m, d):
        x_vec = [i * 0.001 for i in range(int(10 / 0.001))]
        f3 = (m - 1) * n
        for i in x_vec:
            if abs(f.cdf(i, n - d, f3) - prob) < 0.0001:
                return i

    f1, f2 = m - 1, N
    f3 = f1 * f2
    fisher = table_fisher(0.95, N, m, 1)
    Gp = max(dispersions) / sum(dispersions)
    Gt = fisher / (fisher + (m - 1) - 2)

    print("\nОднорідність дисперсії (критерій Кохрена): ")
    print(f"Gp = {Gp}\nGt = {Gt}")
    if Gp < Gt:
        print("\nДисперсія однорідна (Gp < Gt)")

        D_beta = sum(dispersions) / (N * N * m)
        Sb = sqrt(abs(D_beta))
        beta = [sum([(y_avg[j] * norm_matrix[i][j]) / N for j in range(N)]) for i in range(len(norm_matrix))]

        t_list = [abs(i) / Sb for i in beta]
        student = partial(t.ppf, q=1-0.025)
        d, T = 0, student(df=f3)
        print("\nt табличне = ", T)

        for i in range(len(t_list)):
            if t_list[i] < T:
                b[i] = 0
                print("\tt{} = {} => коефіцієнт незначимий, його слід виключити з рів-ня регресії".format(i, t_list[i]))
            else:
                print("\tt{} = {} => коефіцієнт значимий".format(i, t_list[i]))
                d += 1

        print("\nОтже, кіл-ть значимих коеф. d =", d, "\n\n\tРів-ня регресії з урахуванням критерія Стьюдента:\nŷ = ", end="")
        print("{:.3f}".format(b[0]), end="") if b[0] != 0 else None
        for i in range(1, 10):
            print(" + {:.3f}*{}".format(b[i], (table_factors_1 + table_factors_2)[i]), end="") if b[i] != 0 else None
        print("\n\n\tПеревірка при підстановці в спрощене рів-ня регресії:")
        for i in range(N): print("y`{} = {:.3f} ≈ {:.3f}".format((i + 1), check(b, i), y_avg[i]))

        f4 = N - d
        fisher_sum = sum([(check(b, i) - y_avg[i]) ** 2 for i in range(N)])
        D_ad = (m / f4) * fisher_sum

        fisher = partial(f.ppf, q=1-0.05)
        Fp = D_ad / sum(dispersions) / N
        Ft = fisher(dfn=f4, dfd=f3)
        print("\nКритерій Фішера:")
        if Fp > Ft:
            print("\tРівняння регресії неадекватне (Ft < Fp).")
            break
        else:
            print("\tРівняння регресії адекватне (Ft > Fp)!")
            print("\n\n--- Час виконання програми: %s секунд ---" % (process_time() - start_time))
            break

    else:
        print("Дисперсія неоднорідна (Gp > Gt), збільшуємо m, повторюємо операції")
        m += 1
