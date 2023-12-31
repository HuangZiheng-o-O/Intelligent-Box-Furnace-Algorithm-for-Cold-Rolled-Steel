from django.shortcuts import render
from django.http.response import JsonResponse

from anneal.models import Materials

import json

# Create your views here.

# 获取数据库信息
def get_material(request):
    try:
        obj_material = Materials.objects.all().values() #获取所有材料信息
        print(obj_material[0])
        materials = list(obj_material) #把结果转为list格式
        return JsonResponse({'code': 1, 'data': materials})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "获取材料信息异常"+str(e)})

# 接收前端传递的数据
def receive(request):
    data = json.loads(request.body.decode("utf-8"))
    try:
        print(data["id"])
        print(data["material"])
        return JsonResponse({'code': 1, 'data': data})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "接收材料信息异常" + str(e)})
