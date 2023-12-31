# 函数拟合
import json
from decimal import Decimal

import numpy as np
from matplotlib import pyplot as plt
from django.http.response import JsonResponse

# 模拟退火功能
def bpDeep(request):
    data = json.loads(request.body.decode("utf-8"))
    try:
        if data["id"] == '1':
            # print(data)
            # print(type(data["thickness"]))
            # 硅钢厚度mm/重量kg
            x = [30, 32, 35, 38, 40, 43, 45, 48, 50, 55]
            # 第一个平峰
            y_01 = [10, 12, 13, 14, 15, 16.5, 18, 20, 24, 30]
            # 第二个平峰
            y_02 = [9, 9.2, 9.5, 9.8, 10, 10.5, 10.8, 11, 12, 15]
            # 第三个平峰
            y_03 = [20, 22, 24, 25, 26, 30, 32, 35, 40, 50]

            # 这是直线的例子，如果是二次、三次....曲线，在Python里也很简单，只是把上述代码里np.polyfit() 函数中的第三个参数改成相应的次数就可以了。
            parameters_01 = np.polyfit(x, y_01, 2)
            func_01 = np.poly1d(parameters_01)
            print(parameters_01)

            parameters_02 = np.polyfit(x, y_02, 2)
            func_02 = np.poly1d(parameters_02)
            print(parameters_02)

            parameters_03 = np.polyfit(x, y_03, 2)
            func_03 = np.poly1d(parameters_03)
            print(parameters_03)

            plt.scatter(x, y_01)  # print the original numbers in dots
            x = [0] + x + [60]
            plt.grid(True, color='black')
            plt.plot(x, func_01(x), color='orange', linestyle='-')
            plt.xlim(0, 60)
            plt.ylim(0, 50)
            plt.xlabel('mm')
            plt.ylabel('h')
            print(round(func_01(data["thickness"]), 2))
            print(round(func_02(data["thickness"]), 2))
            print(round(func_03(data["thickness"]), 2))
            plt.show()
            res_data = {# 字典格式，四舍五入保留2位小数
                'first': round(func_01(data["thickness"]), 2),
                'second': round(func_02(data["thickness"]), 2),
                'third': round(func_03(data["thickness"]), 2),
            }
        return JsonResponse({'code': 1, 'data': res_data})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "接收材料信息异常" + str(e)})