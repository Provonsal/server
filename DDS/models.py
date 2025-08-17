from datetime import datetime
from uuid import uuid4
from django.db import models
from django.forms import ValidationError

# Create your models here.

class WriteStatus(models.Model):
    
    """
    Модель статусов движений денежных средств
    
    Поля модели:
    
    status: varchar(15)
    """
    
    status = models.CharField(name="status", verbose_name="Статус", max_length=15, null=False, primary_key=True)
    
    class Meta:
        ordering = ['status']
        verbose_name = 'Статус сделки'
        verbose_name_plural = 'Статусы сделки'
    
    def __str__(self):
        return f"{self.status}"

class WriteType(models.Model):
    
    """
    Модель типов движений денежных средств
    
    Поля модели:
    
    write_type: varchar(20)
    """
    
    write_type = models.CharField(name="write_type", verbose_name="Тип", max_length=20, null=False, primary_key=True)
    
    class Meta:
        ordering = ['write_type']
        verbose_name = 'Тип сделки'
        verbose_name_plural = 'Типы сделок'
    
    def __str__(self):
        return f"{self.write_type}"

class WriteCategory(models.Model):
    
    """
    Модель категории движений денежных средств.
    
    Поля модели:
    
    name: varchar(30)
    parent_type: varchar(20)
    """
    
    name = models.CharField(name='name', verbose_name="Название категории", max_length=30, null=False, primary_key=True)
    parent_type = models.ForeignKey(WriteType, verbose_name="Тип", on_delete=models.CASCADE, null=False)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        
    def __str__(self):
        return f"{self.name}"

class WriteSubcategory(models.Model):
    
    """
    Модель подкатегорий движений денежных средств.
    
    Поля модели:
    
    name: varchar(30), pk
    parent_category: varchar(30), fk
    """
    
    name = models.CharField(name='name', verbose_name="Название подкатегории", max_length=30, null=False, primary_key=True)
    parent_category = models.ForeignKey(WriteCategory, verbose_name="Категория", on_delete=models.CASCADE, null=False)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        
    def __str__(self):
        return f"{self.name}"


                
            

class DDS(models.Model):
    
    """
    Модель записи о движении денежных средств (ДДС).
    
    Поля модели:
    
    write_id: uuid, pk
    write_date: datetime
    status: varchar(15), fk
    write_type: varchar(15), fk
    category: varchar(30), fk
    subcategory: varchar(30), fk
    summ: decimal(max_digits=6, decimal_places=3)
    commentary: text
    """    
    
    write_id = models.UUIDField(verbose_name="Уникальный номер записи", primary_key=True, default=uuid4)
    write_date = models.DateField(verbose_name="Дата создания записи", null=False, editable=True, default=datetime.now)
    status = models.ForeignKey(WriteStatus, verbose_name="Статус", on_delete=models.CASCADE, null=False)
    write_type = models.ForeignKey(WriteType, verbose_name="Тип", on_delete=models.CASCADE, null=False)
    category = models.ForeignKey(WriteCategory, verbose_name="Категория", on_delete=models.CASCADE, null=False)
    subcategory = models.ForeignKey(WriteSubcategory, verbose_name="Подкатегория", on_delete=models.CASCADE, null=False)
    summ = models.DecimalField(verbose_name="Сумма", max_digits=6, decimal_places=3, null=False, default=0)
    commentary = models.TextField(verbose_name="Комментарий", null=True)
   
    def clean(self):
        super().clean()
        if self.category and self.write_type and self.category.parent_type != self.write_type:
            raise ValidationError({
                'category': "Категория должна принадлежать выбранному типу."
            })
        if self.subcategory and self.category and self.subcategory.parent_category != self.category:
            raise ValidationError({
                'subcategory': "Подкатегория должна принадлежать выбранной категории."
            })
