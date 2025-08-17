from django import forms
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from .models import DDS, WriteCategory, WriteStatus, WriteSubcategory, WriteType



# Дополняем и переопределяем модель админской формы.
class DDSAdmin(admin.ModelAdmin):
    list_display = [
        "write_id",
        "write_date",
        "status",
        "write_type",
        "category",
        "subcategory",
        "summ",
        "commentary"
    ]
    
    fields = [
        "write_id",
        "write_date",
        "status",
        "write_type",
        "category",
        "subcategory",
        "summ",
        "commentary"
    ]
    
    # Задаем путь к пользовательскому шаблону для изменения формы
    change_form_template = 'admin/product_change_form.html'

    # Переопределяем метод получений путей
    def get_urls(self):
        urls = super().get_urls() # Получаем все пути от родительского класса
        
        # Задаем пользовательские пути
        my_urls = [
            path('get-subcategories/', self.get_subcategories, name='get_subcategories'),
            path('get-categories/', self.get_categories, name='get_categories')
        ]
        
        # Возвращаем наследованные и новые пользовательские пути
        return my_urls + urls

    def get_subcategories(self, request):
        
        """
        Метод пути для получения подкатегорий, которые принадлежат категории.
        """
        
        # Извлекаем категорию из запроса
        category = request.GET.get('category_id')
        
        # Если получилось извлечь категорию
        if category: 
        
            # Извлекаем подкатегории относящиеся к полученная категории
            subcategories = WriteSubcategory.objects.filter(parent_category=category).values('name')
        
            # Возвращаем полученный результат
            return JsonResponse(list(subcategories), safe=False)
        
        # Если категории не передано, то возвращаем пустой список
        return JsonResponse([], safe=False)
    
    def get_categories(self, request):
        
        """
        Метод пути для получения категорий, которые принадлежат к типу
        """
        
        # Извлекаем тип записи из запроса
        write_type = request.GET.get('write_type_id')
        
        # Если получилось извлечь тип записи
        if write_type:
            
            # Извлекаем категории относящиеся к полученному типу записи
            categories = WriteCategory.objects.filter(parent_type=write_type).values('name')
            
            # Возвращаем полученный результат
            return JsonResponse(list(categories), safe=False)
        
        # Если типу не передано, то возвращаем пустой список
        return JsonResponse([], safe=False)

# Регистрируем модели в админке
admin.site.register(WriteStatus)
admin.site.register(WriteType)
admin.site.register(WriteCategory)
admin.site.register(WriteSubcategory)
admin.site.register(DDS, DDSAdmin) # Помимо регистрации модели, регистрируем модель админки

