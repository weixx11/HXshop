#!/usr/bin/env python
#coding=utf-8


from django.views.generic.base import View
from django.views.generic import ListView
from goods.models import Goods
from django.forms.models import model_to_dict
import json
from django.http import HttpResponse,JsonResponse
from django.core import serializers

class GoodsListView(View):

    def get(self,request):
        """
        通过django的view实现商品列表页

        :param request:
        :return:
        """

        json_list=[]
        goods=Goods.objects.all()[:10]

        # for good in goods:
        #     json_dict={}
        #     json_dict["name"]=good.name
        #     json_dict["category"]=good.category.name
        #     json_dict["market_price"]=good.market_price
        #     json_dict["add_time"]=good.add_time
        #     json_list.append(json_dict)

        for good in goods:
            json_dict=model_to_dict(good)
            json_list.append(json_dict)


        json_data=serializers.serialize("json",goods)
        json_data=json.loads(json_data)
        print(type(json_data))
        return HttpResponse(json.dumps(json_data),content_type="application/json")
        # return HttpResponse("heelp")