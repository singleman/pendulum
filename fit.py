import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import argrelextrema

# 读取数据
filename = 'data.txt'  # 这里改为你的数据文件路径
data = np.loadtxt(filename)

t = data[:, 0]  # 第一列为时间 t
x = data[:, 1]  # 第二列为横向位移 x

# 定义一个带有阻尼的正弦函数来拟合数据
def damped_sine_function(t, a, b, c, d, alpha):
    return a * np.exp(-alpha * t) * np.sin(b * t + c) + d

# 对整个曲线进行拟合
# 初始值 p0 需要根据你的数据特性进行调整
p0 = [300, 20, 0, 0, 0.05]  # [振幅, 频率, 相位, 偏移量, 阻尼系数]
popt, _ = curve_fit(damped_sine_function, t, x, p0=p0)

# 找到极大值和极小值点
max_indices = argrelextrema(x, np.greater)[0]
min_indices = argrelextrema(x, np.less)[0]

# 获取极大值和极小值的 t 和 x 值
max_t = t[max_indices]
max_x = x[max_indices]
min_t = t[min_indices]
min_x = x[min_indices]

# 对极大值点进行拟合
def max_fit_function(t, a, b, c):
    return a * np.exp(-b * t) + c

popt_max, _ = curve_fit(max_fit_function, max_t, max_x, p0=[300, 0.05, 0])

# 对极小值点进行拟合
def min_fit_function(t, a, b, c):
    return a * np.exp(-b * t) + c

popt_min, _ = curve_fit(min_fit_function, min_t, min_x, p0=[-300, 0.05, 0])

# 画出原始数据，拟合曲线和极值点
plt.figure(figsize=(12, 6))

# 原始数据
plt.plot(t, x, label='Original Data', color='black')

# 拟合的阻尼正弦曲线
plt.plot(t, damped_sine_function(t, *popt), label='Fitted Damped Sine Function', color='red', linestyle='--')

# 极大值点
plt.scatter(max_t, max_x, color='blue', label='Maxima Points')

# 极小值点
plt.scatter(min_t, min_x, color='orange', label='Minima Points')

# 极大值点拟合曲线
plt.plot(t, max_fit_function(t, *popt_max), label='Fitted Maxima Envelope', color='green', linestyle=':')

# 极小值点拟合曲线
plt.plot(t, min_fit_function(t, *popt_min), label='Fitted Minima Envelope', color='purple', linestyle='-.')

plt.xlabel('Time (t)')
plt.ylabel('Displacement (x)')
plt.legend()
plt.show()
