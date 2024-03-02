from django.urls import path
from app import views



urlpatterns = [
    path('', views.IndexView.as_view(), name='index'), # home
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'), # 投稿詳細
    path('post/new/', views.CreatePostView.as_view(), name='post_new'), # 投稿画面
    path('post/<int:pk>/edit/', views.PostEditView.as_view(), name='post_edit'), # 投稿編集
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'), # 投稿削除
    path('post/<int:pk>/new_comment', views.AddCommentView.as_view(), name="add_comment"), # コメント投稿
    path('like_post/<int:post_id>/', views.like_post, name='like_post'), # 投稿good
    path('good_comment/<int:comment_id>/', views.good_comment, name='good_comment'), # コメントgood
    path('bad_comment/<int:comment_id>/', views.bad_comment, name='bad_comment'), # コメントbad
    path('comment/<int:pk>/edit/', views.CommentEditView.as_view(), name='comment_edit'), # コメント編集
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'), # コメント削除
    path('category/<str:category_slug>/', views.IndexByCategoryView.as_view(), name='selected_category'), # カテゴリのhome
    path('subcategory/<str:subcategory_slug>/', views.IndexBySubcategoryView.as_view(), name='selected_subcategory'), # サブカテゴリのhome
    path('description/', views.DescriptionView.as_view(), name='description'),
    path('mypage/<str:userid>', views.IndexByUserView.as_view(), name='mypage'),
    # アカウント関連
    path('login/',views.Login,name='Login'),
    path("logout/",views.Logout,name="Logout"),
    path('register',views.AccountRegistration.as_view(), name='register'),
]


from django.conf import settings
from django.conf.urls.static import static
# メディアファイルのURLパスを追加
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)