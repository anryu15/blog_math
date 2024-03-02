from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from .models import Post,Category,SubCategory, Comment, AccountUser
from .forms import PostForm, AccountUserForm, AddAccountUserForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
import re
from django.http import JsonResponse

from . import functions

class IndexView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.order_by('-id')
        login_user = request.user
        login_user_id = str(login_user)+"_"+str(login_user.id)
        categoryLst = functions.category_list_dic()
        subcategorylst = functions.subcategory_list_dic()

        return render(request, 'index.html', {
            'post_data' : post_data,
            'login_user' : login_user,
            'login_user_id' : login_user_id,
            'subcategoryList':subcategorylst,
            'categoryLst' : categoryLst,
        })

class IndexByUserView(View):
    def get(self, request, userid):
        userid = int(userid.split("_")[-1]) -1
        account_user = AccountUser.objects.get(id=userid)
        post_data = Post.objects.filter(author=account_user.user)
        
        login_user = request.user
        login_user_id = str(login_user)+"_"+str(login_user.id)
        categoryLst = functions.category_list_dic()
        subcategorylst = functions.subcategory_list_dic()
       
        return render(request, 'mypage.html', {
            'post_data' : post_data,
            'account_user': account_user,
            'login_user' : login_user,
            'login_user_id' : login_user_id,
            'subcategoryList':subcategorylst,
            'subcategoryList':subcategorylst,
            'categoryLst' : categoryLst,
        })
    
class IndexByCategoryView(View):
    def get(self, request, category_slug):
        category = Category.objects.get(name=category_slug)
        filtered_post_data = Post.objects.filter(category=category).order_by('id')
        login_user = request.user
        login_user_id = str(login_user)+"_"+str(login_user.id)
        subcategorylst = functions.subcategory_list_dic(category=category)

        return render(request, 'index.html', {
            'post_data' : filtered_post_data,
            'login_user' : login_user,
            'login_user_id' : login_user_id,
            'subcategoryList':subcategorylst,
            'category' : category,
            'filtered_flag' : True,
        })
    
class IndexBySubcategoryView(View):
    def get(self, request, subcategory_slug):
        subcategory = SubCategory.objects.get(name=subcategory_slug)
        filtered_post_data = Post.objects.filter(subcategory=subcategory).order_by('id')
        category = subcategory.category
        login_user = request.user
        login_user_id = str(login_user)+"_"+str(login_user.id)
        subcategorylst = functions.subcategory_list_dic(category=category)

        return render(request, 'index.html', {
            'post_data' : filtered_post_data,
            'login_user' : login_user,
            'login_user_id' : login_user_id,
            'subcategoryList':subcategorylst,
            'category' : category,
            'filtered_flag' : True,
        })

class PostDetailView(View):
    def get(self, request, *args, **kwargs):
        login_user = request.user
        login_user_id = str(login_user)+"_"+str(login_user.id)
        post_data = Post.objects.get(id=self.kwargs['pk'])

        likes_count = post_data.likes.count()
        if post_data.img:
            img_url = '/media/' + str(post_data.img)
        else:
            img_url =''

        comment_data_objects = post_data.comments.all()
        comment_data_lists = []
        for comment_data in comment_data_objects:
            comment_data_list = []
            comment_data_dic = {}
            comment_data_dic['id'] = comment_data.id
            comment_data_dic['posted_date'] = comment_data.posted_date
            comment_data_dic['author'] = comment_data.author
            comment_data_dic['content'] = comment_data.content
            comment_data_dic['goods'] = comment_data.goodcomment
            comment_data_dic['bads'] = comment_data.badcomment
            comment_data_dic['good_count'] = comment_data.goodcomment.count()
            comment_data_dic['bad_count'] = comment_data.badcomment.count()
            if comment_data.img:
                comment_data_dic['img'] = comment_data.img
            comment_data_list.append(comment_data_dic)
            comment_data_lists.append(comment_data_list)

        return render(request, 'post_detail.html', {
            'post_data': post_data,
            'img_url' : img_url,
            'comment_data_list': comment_data_lists,
            'likes_count': likes_count,
            'login_user' : login_user,
            'login_user_id' : login_user_id
        })

class CreatePostView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)
        categorylst=Category.objects.all()
        subcategorylst=SubCategory.objects.all()
        login_user = request.user
        login_user_id = str(login_user)+"_"+str(login_user.id)
        return render(request, 'post_form.html', {
            'form': form,
            'categoryList': categorylst,
            'subcategoryList':subcategorylst,
            'login_user' : login_user,
            'login_user_id' : login_user_id
        })

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():

            post_data = Post(
                author=request.user,
                title=form.cleaned_data['title'],
                img = form.cleaned_data['img']
            )
            category_name = form.cleaned_data['category_element']
            subcategory_name = form.cleaned_data['subcategory_element']
            category = get_object_or_404(Category, name=category_name)
            subcategory = get_object_or_404(SubCategory, name=subcategory_name)
            post_data.content = form.cleaned_data['content']
            post_data.category = category
            post_data.subcategory = subcategory
            post_data.save()
            return redirect('post_detail', post_data.id)

        return render(request, 'post_form.html', {'form': form})

    
class PostEditView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        categorylst=Category.objects.all()
        subcategorylst=SubCategory.objects.all()
        login_user = request.user
        login_user_id = str(login_user)+"_"+str(login_user.id)
        form = PostForm(
            request.POST or None,
            initial = {
                'title': post_data.title,
                'content': post_data.content,
                'category_element': post_data.category,
                'subcategory_element': post_data.subcategory,
            }
        )
        
        if post_data.img:
            img_url = '/media/' + str(post_data.img)
        else:
            img_url =''

        return render(request, 'post_form_edit.html', {
            'post_data': post_data,
            'form': form,
            'img_url' : img_url,
            'categoryList': categorylst,
            'subcategoryList':subcategorylst,
            'selected_category': post_data.category.name if post_data.category else '',
            'selected_subcategory': post_data.subcategory.name if post_data.subcategory else '',
            'login_user' : login_user,
            'login_user_id' : login_user_id
        })
    
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post_data = Post.objects.get(id=self.kwargs['pk'])
            post_data.author = request.user
            post_data.title = form.cleaned_data['title']
            post_data.content = form.cleaned_data['content']
            if form.cleaned_data['img']:
                post_data.img = form.cleaned_data['img']
            category_name = form.cleaned_data['category_element']
            subcategory_name = form.cleaned_data['subcategory_element']
            category = get_object_or_404(Category, name=category_name)
            subcategory = get_object_or_404(SubCategory, name=subcategory_name)
            post_data.category = category
            post_data.subcategory = subcategory
            post_data.save()
            
            return redirect('post_detail', self.kwargs['pk'])
        
        return render(request, 'post_form_edit.html', {
            'form': form
        })
    
class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        login_user = request.user
        login_user_id = str(login_user)+"_"+str(login_user.id)
        return render(request, 'post_delete.html', {
            'post_data': post_data,
            'login_user' : login_user,
            'login_user_id' : login_user_id
        })

    def post(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        post_data.delete()
        return redirect('index')
    
class AddCommentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        form = CommentForm(request.POST or None)
        login_user = request.user
        login_user_id = str(login_user)+"_"+str(login_user.id)
        
        return render(request, 'comment_form.html', {
            'form': form,
            'post_data': post_data,
            'login_user' : login_user,
            'login_user_id' : login_user_id})

    def post(self, request, *args, **kwargs): #ボタンクリック時
        post_data = Post.objects.get(id=self.kwargs['pk'])
        form = CommentForm(request.POST, request.FILES)
        # 有効か
        if form.is_valid():
            comment_data = Comment()
            comment_data.post = Post.objects.get(id=self.kwargs['pk'])
            comment_data.author = request.user
            comment_data.content = form.cleaned_data['content']
            if form.cleaned_data['img']:
                comment_data.img = form.cleaned_data['img']
            comment_data.save()
            return redirect("post_detail", post_data.id)
        
        return render(request, "post_detail.html", {"form":form})
    
class CommentEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        comment_data = Comment.objects.get(id=self.kwargs['pk'])
        login_user = request.user
        login_user_id = str(login_user)+"_"+str(login_user.id)
        form = CommentForm(
            request.POST or None,
            initial = {
                'content':comment_data.content
            }
        )
        
        if comment_data.img:
            img_url = '/media/' + str(comment_data.img)
        else:
            img_url =''

        return render(request, 'comment_form_edit.html', {
            'comment_data': comment_data,
            'form': form,
            'img_url' : img_url,
            'login_user' : login_user,
            'login_user_id' : login_user_id
        })
    
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment_data = Comment.objects.get(id=self.kwargs['pk'])
            comment_data.author = request.user
            comment_data.content = form.cleaned_data['content']
            if form.cleaned_data['img']:
                comment_data.img = form.cleaned_data['img']
            comment_data.save()
            post_data = comment_data.post
            return redirect('post_detail', post_data.id)
        
        return render(request, 'comment_form_edit.html', {
            'form': form
        })
    
class CommentDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        comment_data = Comment.objects.get(id=self.kwargs['pk'])
        login_user = request.user
        login_user_id = str(login_user)+"_"+str(login_user.id)
        return render(request, 'comment_delete.html', {
            'comment_data': comment_data,
            'login_user' : login_user,
            'login_user_id' : login_user_id
        })

    def post(self, request, *args, **kwargs):
        comment_data = Comment.objects.get(id=self.kwargs['pk'])
        comment_data.delete()

        post_data = comment_data.post
        return redirect('post_detail', post_data.id)
    
    
def like_post(request, post_id):
    post_data = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post_data.likes.add(request.user)
        likes_count = post_data.likes.count()
        author = post_data.author
        author_profile = author.accountuser
        author_profile.numgood += 1
        author_profile.save()
        
        return JsonResponse({'likes_count': likes_count})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    
def good_comment(request, comment_id):
    comment_data = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        comment_data.goodcomment.add(request.user)
        goods_count = comment_data.goodcomment.count()
        author = comment_data.author
        author_profile = author.accountuser
        author_profile.numgood += 1
        author_profile.save()
        return JsonResponse({'good_count': goods_count})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    
def bad_comment(request, comment_id):
    comment_data = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        comment_data.badcomment.add(request.user)
        bads_count = comment_data.badcomment.count()
        
        return JsonResponse({'bad_count': bads_count})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    
class DescriptionView(View):
    def get(self, request, *args, **kwargs):
        login_user = request.user
        login_user_id = str(login_user)+"_"+str(login_user.id)
        
        return render(request, 'description_page.html', {
            'login_user' : login_user,
            'login_user_id' : login_user_id
        })
    
"""
アカウント関連
・ログイン
・ログアウト
・サインアップ
"""

# ログイン
def Login(request):
    # POST
    error_message = ""
    if request.method == 'POST':
        # フォーム入力のユーザーID・パスワード取得
        username =  request.POST.get('username')
        password = request.POST.get('password')
        # Djangoの認証機能
        user = authenticate(username=username, password=password)
        # ユーザー認証
        if user:
            #ユーザーアクティベート判定
            if user.is_active:
                # ログイン
                login(request,user)
                # ホームページ遷移
                login_user = user
                login_user_id = str(user)+"_"+str(user.id)
                
                post_data = Post.objects.order_by('-id')
                return render(request, 'index.html', {
                    'post_data':post_data,
                    'login_user' : login_user,
                    'login_user_id' : login_user_id
                })
            else:
                # アカウント利用不可
                error_message = "アカウントが有効ではありません"
                params = {
                    "AccountCreate":False,
                    "account_form": AccountUserForm(),
                    "add_account_form":AddAccountUserForm(),
                    "error_message" : error_message
                }
                params["account_form"] = AccountUserForm()
                return render(request, 'login.html',context=params)
                
        # ユーザー認証失敗
        else:
            error_message = "ユーザー名またはパスワードが間違っています"
            params = {
                "AccountCreate":False,
                "account_form": AccountUserForm(),
                "add_account_form":AddAccountUserForm(),
                "error_message" : error_message
            }
            params["account_form"] = AccountUserForm()
            return render(request, 'login.html',context=params)
    # GET
    else:
        params = {
            "AccountCreate":False,
            "account_form": AccountUserForm(),
            "add_account_form":AddAccountUserForm(),
            "error_message" : error_message
        }
        params["account_form"] = AccountUserForm()
        return render(request, 'login.html',context=params)


#ログアウト
@login_required
def Logout(request):
    logout(request)
    post_data = Post.objects.order_by('-id')
    return render(request, 'index.html', {
        'post_data':post_data
    })

class  AccountRegistration(TemplateView):
    def __init__(self):
        self.error_message = ""
        self.params = {
            "AccountCreate":False,
            "account_form": AccountUserForm(),
            "add_account_form":AddAccountUserForm(),
            "error_message" : self.error_message,
        }
    # Get処理
    def get(self,request):
        self.params["AccountCreate"] = False
        self.params["account_form"] = AccountUserForm()
        self.params["add_account_form"] = AddAccountUserForm()
        return render(request,"register.html",context=self.params)

    # Post処理
    def post(self,request):
        self.params["account_form"] = AccountUserForm(data=request.POST)
        self.params["add_account_form"] = AddAccountUserForm(data=request.POST)

        # フォーム入力の有効検証
        if self.params["account_form"].is_valid() and self.params["add_account_form"].is_valid():
            account_password = self.params["account_form"].cleaned_data.get('password', None)
            if len(account_password) < 6:
                self.error_message = "パスワードが短いです。6文字以上にしてください。"
                self.params["AccountCreate"] = False
                self.params["account_form"] = AccountUserForm()
                self.params["add_account_form"] = AddAccountUserForm()
                self.params["error_message"] = self.error_message
                return render(request,"register.html",context=self.params)
            # アカウント情報をDB保存
            account = self.params["account_form"].save()
            # パスワードをハッシュ化
            account.set_password(account.password)
            # ハッシュ化パスワード更新
            account.save()

            # 下記操作のため、コミットなし
            add_account = self.params["add_account_form"].save(commit=False)
            # AccountForm & AddAccountForm 1vs1 紐付け
            add_account.user = account
            # モデル保存
            add_account.save()

            # アカウント作成情報更新
            self.params["AccountCreate"] = True

        else:
            self.error_message = self.get_error_message(str(self.params["account_form"].errors))
            self.params["AccountCreate"] = False
            self.params["account_form"] = AccountUserForm()
            self.params["add_account_form"] = AddAccountUserForm()
            self.params["error_message"] = self.error_message
            return render(request,"register.html",context=self.params)
        
        login(request, account)
        return redirect('index')
    
    def get_error_message(self, error_string):
        error_string_no_li = re.sub(r'<li>', '', error_string)
        # '</li>' または '<ul class="errorlist">' で分割して配列に格納
        error_list = re.split(r'</li>|<ul class="errorlist">', error_string_no_li)
        error_list = [item for item in error_list if item]
        return error_list[1]