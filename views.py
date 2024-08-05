
from django.http import JsonResponse

import datetime
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
import json



# def index(request):
#     return JsonResponse("Hello, world. You're at the polls index.")

deals = {}
purchases = {}
deal_id_counter = 1
purchase_id_counter = 1

@csrf_exempt
def create_deal(request):
    global deal_id_counter
    if request.method == 'POST':
        data = json.loads(request.body)
        deal = {
            'id': deal_id_counter,
            'name': data['name'],
            'price': data['price'],
            'quantity': data['quantity'],
            'end_time': timezone.now()+ timedelta(hours= int(data['end_time'])),
            }
        deals[deal_id_counter] = deal
    # deal.dumps(deal)
        return JsonResponse(deal, status=201)
    return JsonResponse({"error": "invalid method"}, status = 405)

@csrf_exempt
def claim_deal(request):
    global purchase_id_counter
    if request.method == 'POST':
        print(deals)
        data = json.loads(request.body)
        user = data['user']
        deal_id = int(data['deal_id'])
        quantity = int(data.get('quantity'))
        deal=  deals.get(deal_id)
        if not deal:
            return JsonResponse({"error": "deal not found"}, status=404)
        if deal['end_time'] < timezone.now():
            return JsonResponse({"error": "deal has  expired"}, status=400)
        if deal['quantity'] < quantity:
            return JsonResponse({"error": "not enough in stock"}, status=400)
        for purchase in purchases.values():
            if purchase['user'] == user and purchase['deal_id'] == deal_id:
                return JsonResponse({"error": "deal is already claimed by user"}, status=400)
        deal['quantity']  -= quantity
        purchase = {
            "id": purchase_id_counter,
            "user": user,
            "deal_id": deal_id,
            "quantity": quantity,
            "time": timezone.now()
        }
        purchases[purchase_id_counter] = purchase

        purchase_id_counter +=1
        
        return JsonResponse(purchase, status=201)
    return JsonResponse({"error": "invalid method"}, status = 405)







