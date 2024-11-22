import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import argrelextrema

# 读取数据
filename = 'data.txt'  # 修改为你的数据文件路径
data = np.loadtxt(filename)

t = data[:, 0]  # 第一列为时间 t
x = data[:, 1]  # 第二列为横向位移 x

# 定义一个带有阻尼的正弦函数来拟合数据
def damped_sine_function(t, a, b, c, d, alpha):
    return a * np.exp(-alpha * t) * np.sin(b * t + c) + d

# 对整个曲线进行拟合
p0 = [300, 20, 0, 0, 0.05]  # [振幅, 频率, 相位, 偏移量, 阻尼系数]
popt, _ = curve_fit(damped_sine_function, t, x, p0=p0)

# 输出拟合的阻尼正弦函数形式
print(f"Fitted Damped Sine Function: y(t) = {popt[0]:.3f} * exp(-{popt[4]:.3f} * t) * sin({popt[1]:.3f} * t + {popt[2]:.3f}) + {popt[3]:.3f}")

# 找到极大值点
max_indices = argrelextrema(x, np.greater)[0]

# 获取极大值的 t 和 x 值
max_t = t[max_indices]
max_x = x[max_indices]

# 对极大值点进行拟合
def max_fit_function(t, a, b, c):
    return a * np.exp(-b * t) + c

popt_max, _ = curve_fit(max_fit_function, max_t, max_x, p0=[300, 0.05, 0])
print(f"Fitted Maxima Envelope: y(t) = {popt_max[0]:.3f} * exp(-{popt_max[1]:.3f} * t) + {popt_max[2]:.3f}")

# 画出原始数据，拟合曲线和极大值点
plt.figure(figsize=(12, 6))

# 原始数据
plt.plot(t, x, label='Original Data', color='black')

# 拟合的阻尼正弦曲线
plt.plot(t, damped_sine_function(t, *popt), label='Fitted Damped Sine Function', color='red', linestyle='--')

# 极大值点
plt.scatter(max_t, max_x, color='blue', label='Maxima Points')

# 极大值点拟合曲线
plt.plot(t, max_fit_function(t, *popt_max), label='Fitted Maxima Envelope', color='green', linestyle=':')

plt.xlabel('Time (t)')
plt.ylabel('Displacement (x)')
plt.legend()
plt.show()
