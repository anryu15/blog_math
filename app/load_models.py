from app.models import Category, SubCategory

"""
python manage.py shell    
実行後以下を実行
"""
category = Category(name='数学I')
category.save()
subcategory = SubCategory.objects.create(name="数と式", category=category)
subcategory = SubCategory.objects.create(name="2次関数", category=category)
subcategory = SubCategory.objects.create(name="図形と計量", category=category)
subcategory = SubCategory.objects.create(name="データの分析", category=category)
category = Category(name='数学II')
category.save()
subcategory = SubCategory.objects.create(name="式と証明", category=category)
subcategory = SubCategory.objects.create(name="複素数と方程式", category=category)
subcategory = SubCategory.objects.create(name="図形と方程式", category=category)
subcategory = SubCategory.objects.create(name="三角関数", category=category)
subcategory = SubCategory.objects.create(name="指数定数関数", category=category)
subcategory = SubCategory.objects.create(name="数II微積", category=category)
category = Category(name='数学III')
category.save()
subcategory = SubCategory.objects.create(name="複素数平面", category=category)
subcategory = SubCategory.objects.create(name="平面状の曲線", category=category)
subcategory = SubCategory.objects.create(name="数III極限", category=category)
subcategory = SubCategory.objects.create(name="数III微分", category=category)
subcategory = SubCategory.objects.create(name="数III積分", category=category)
category = Category(name='数学A')
category.save()
subcategory = SubCategory.objects.create(name="場合の数と確立", category=category)
subcategory = SubCategory.objects.create(name="図形の性質", category=category)
subcategory = SubCategory.objects.create(name="整数の性質", category=category)
category = Category(name='数学B')
category.save()
subcategory = SubCategory.objects.create(name="ベクトル", category=category)
subcategory = SubCategory.objects.create(name="数列", category=category)