from .models import Post,Category,SubCategory

def category_list_dic():
    category_data_objects = Category.objects.all()
    category_data_lists = []

    for category_data in category_data_objects:
        category_data_list = []
        category_data_dic = {}
        category_data_dic['id'] = category_data.id
        category_data_dic['name'] = category_data.name
        filtered_post_count = Post.objects.filter(category=category_data).count()
        category_data_dic['post_count'] = filtered_post_count
        category_data_list.append(category_data_dic)
        category_data_lists.append(category_data_list)
    return category_data_lists

def subcategory_list_dic(category=None):
    if category:
        subcategory_data_objects = category.subcategories.all()
    else:   
        subcategory_data_objects = SubCategory.objects.all()
    subcategory_data_lists = []
    for subcategory_data in subcategory_data_objects:
        subcategory_data_list = []
        subcategory_data_dic = {}
        subcategory_data_dic['id'] = subcategory_data.id
        subcategory_data_dic['name'] = subcategory_data.name
        filtered_post_count = Post.objects.filter(subcategory=subcategory_data).count()
        subcategory_data_dic['post_count'] = filtered_post_count
        subcategory_data_list.append(subcategory_data_dic)
        subcategory_data_lists.append(subcategory_data_list)
    return subcategory_data_lists