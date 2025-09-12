from django.shortcuts import render

def map_view(request):
    return render(request, 'game/map.html', {})

def house_view(request):
    # house.html はクライアント側でランダムにアイテムを生成して処理する軽量画面
    # クラスはクエリパラメータで渡される（例: /house/?cls=wizard）
    return render(request, 'game/house.html', {})
