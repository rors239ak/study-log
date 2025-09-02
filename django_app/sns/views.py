from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Message,Good
from .forms import PostForm
# Create your views here.
@login_required(login_url="/admin/login/")
def index(request, page=1):
  max = 10
  form = PostForm(request.user)
  msgs = Message.objects.all()
  paginate = Paginator(msgs, max)
  page_items = paginate.get_page(page)
  params = {
    "login_user":request.user,
    "form": form,
    "contents":page_items,
  }
  return render(request, "sns/index.html",params)

@login_required(login_url="/admin/login/")
def goods(request):
  goods = Good.objects.filter(owner=request.user).all()
  params = {
    "login_user":request.user,
    "contents":goods,
  }
  return render(request, "sns/good.html",params)

@login_required(login_url="/admin/login/")
def post(request):
  if request.method == "POST":
    content = request.POST["content"]
    msg = Message()
    msg.owner = request.user
    msg.content = content
    msg.save()
    return redirect(to="/sns/")
  else:
    messages = Message.objects.filter(owner=request.user).all()
    params = {
    "login_user":request.user,
    "contents":messages,
    }
    return render(request, "sns/post.html",params)
  
@login_required(login_url="/admin/login/")
def good(request, good_id):
  good_msg = Message.objects.get(id=good_id)
  is_good = Good.objects.filter(owner=request.user).filter(message=good_msg).count()
  if is_good > 0:
    messages.success(request, "すでにメッセージにGoodしています。")
    return redirect(to="/sns")
  
  good_msg.good_count += 1
  good_msg.save()

  good = Good()
  good.owner = request.user
  good.message = good_msg
  good.save()
  messages.success(request, "メッセージにGoodしました！")
  return redirect(to="/sns")