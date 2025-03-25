from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

items = [
    {"id": 1, "name": "Item1", "description": "Description of Item1"},
    {"id": 2, "name": "Item2", "description": "Description of Item2"}
]

def get_items(request):
    search_query = request.GET.get('search', '')
    filtered_items = [item for item in items if search_query.lower() in item['name'].lower()]
    return JsonResponse(filtered_items if search_query else items, safe=False)

def get_item(request, item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    return JsonResponse(item if item else {"error": "Item not found"}, safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def add_item(request):
    try:
        data = json.loads(request.body)
        new_item = {
            "id": max(item["id"] for item in items) + 1 if items else 1,
            "name": data["name"],
            "description": data.get("description", "")
        }
        items.append(new_item)
        return JsonResponse(new_item, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["PUT"])
def update_item(request, item_id):
    try:
        data = json.loads(request.body)
        for item in items:
            if item['id'] == item_id:
                item.update(data)
                return JsonResponse(item)
        return JsonResponse({"error": "Item not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_item(request, item_id):
    global items
    items = [item for item in items if item['id'] != item_id]
    return JsonResponse({"message": "Item deleted successfully"})