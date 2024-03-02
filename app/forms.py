from django import forms
from django.contrib.auth.models import User
from .models import AccountUser

class PostForm(forms.Form):
    title = forms.CharField(max_length=30, label='タイトル')
    content = forms.CharField(label='内容', widget=forms.Textarea())
    category_element = forms.CharField(max_length=10, label='カテゴリー')
    subcategory_element = forms.CharField(max_length=10, label='サブカテゴリー')
    img = forms.ImageField(label='img',required=False)

    def clean(self):
        cleaned_data = super().clean()
        # 必要に応じてデータの検証や変更を行う
        return cleaned_data
    
class CommentForm(forms.Form):
    content = forms.CharField(label='内容', widget=forms.Textarea())
    img = forms.ImageField(label='img',required=False)

# フォームクラス作成
class AccountUserForm(forms.ModelForm):
    # パスワード入力：非表示対応
    password = forms.CharField(widget=forms.PasswordInput(),label="パスワード")

    class Meta():
        # ユーザー認証
        model = User
        # フィールド指定
        fields = ('username','email','password')
        # フィールド名指定
        labels = {'username':"ユーザーID",'email':"メール"}

class AddAccountUserForm(forms.ModelForm):
    class Meta():
        # モデルクラスを指定
        model = AccountUser
        fields = ('contents',)
        labels = {'contents':"紹介文",}
