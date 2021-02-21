import random

a = [2, 3, 5, 1]
x1, x2, x3 = [random.randrange(1, 21, 1) for i in range(8)],\
             [random.randrange(1, 21, 1) for j in range(8)],\
             [random.randrange(1, 21, 1) for k in range(8)]
y = [a[0] + a[1] * x1[i] + a[2] * x2[i] + a[3] * x3[i] for i in range(8)]

x_zero = lambda x: (max(x) + min(x)) / 2
dx = lambda x: x_zero(x) - min(x)
xn = lambda x: (i - x_zero(x)) / dx(x)
y_etalon = a[0] + a[1] * x_zero(x1) + a[2] * x_zero(x2) + a[3] * x_zero(x3)
res_y = min([i for i in y if i > y_etalon])

xn1, xn2, xn3 = [], [], []
for i in x1: xn1.append(xn(x1))
for i in x2: xn2.append(xn(x2))
for i in x3: xn3.append(xn(x3))

row_format = "|{0:^5}|{1:^10}|{2:^10}|{3:^10}|{4:^10}|"
row_format_str = "|{0:^5}|{1:^10}|{2:^10}|{3:^10}|{4:^10}|{5:^20}|{6:^10}|{7:^10}|{8:^10}|"
row_format_num = "|{0:^5}|{1:^10}|{2:^10}|{3:^10}|{4:^10}|{5:^20}|{6:^10.4f}|{7:^10.4f}|{8:^10.4f}|"
separator_format = "+{0:-^5s}+{0:-^10s}+{0:-^10s}+{0:-^10s}+{0:-^10s}+{1:^20}+{0:-^10}+{0:-^10}+{0:-^10}+".format("-", "")
header_separator_format = "+{0:=^5s}+{0:=^10s}+{0:=^10s}+{0:=^10s}+{0:=^10s}+\n".format("=")

print(separator_format + "\n" + row_format_str.format("#", "x1", "x2", "x3", "y", "", "Xn1", "Xn2", "Xn3") + "\n"
      + separator_format)
for i in range(8): print(row_format_num.format(i + 1, x1[i], x2[i], x3[i], y[i], "", xn1[i], xn2[i], xn3[i]))
print(separator_format + "\n" + row_format.format(" x(0)", x_zero(x1), x_zero(x2), x_zero(x3), y_etalon) + " ⟵ Y(ет)")
print(header_separator_format + row_format.format("dx", dx(x1), dx(x2), dx(x3), "")+ "\n" + header_separator_format)
print(" Y(ет)🡐 =", res_y)
