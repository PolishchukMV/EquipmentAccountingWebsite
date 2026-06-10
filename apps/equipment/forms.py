"""
Формы для приложения оборудования с валидацией.
"""

import os
import re
from django import forms
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from .models import Equipment, Category, Accessory


class EquipmentForm(forms.ModelForm):
    """Форма для создания и редактирования оборудования."""
    
    class Meta:
        model = Equipment
        fields = [
            'inventory_number', 'name', 'category', 'manufacturer', 'model',
            'serial_number', 'status', 'department', 'responsible_person',
            'location', 'purchase_date', 'purchase_price', 'warranty_period',
            'notes', 'photo', 'document'
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Введите примечания...'}),
            'location': forms.TextInput(attrs={'placeholder': 'Укажите местоположение'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем классы Bootstrap к полям
        for field_name, field in self.fields.items():
            if field_name not in ['notes']:
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': 'form-control', 'rows': '3'})
    
    def clean_inventory_number(self):
        """Валидация инвентарного номера."""
        inventory_number = self.cleaned_data.get('inventory_number')
        
        if not inventory_number:
            raise ValidationError('Инвентарный номер обязателен.')
        
        # Проверка на дубликаты
        if self.instance.pk:
            # При редактировании исключаем текущий объект
            if Equipment.objects.filter(
                inventory_number__iexact=inventory_number
            ).exclude(pk=self.instance.pk).exists():
                raise ValidationError('Оборудование с таким инвентарным номером уже существует.')
        else:
            # При создании проверяем все записи
            if Equipment.objects.filter(inventory_number__iexact=inventory_number).exists():
                raise ValidationError('Оборудование с таким инвентарным номером уже существует.')
        
        # Проверка на длину
        if len(inventory_number) < 3:
            raise ValidationError('Инвентарный номер должен содержать минимум 3 символа.')
        
        return inventory_number.upper()
    
    def clean_name(self):
        """Валидация названия."""
        name = self.cleaned_data.get('name')
        
        if not name:
            raise ValidationError('Название обязательно.')
        
        if len(name) < 2:
            raise ValidationError('Название должно содержать минимум 2 символа.')
        
        if len(name) > 200:
            raise ValidationError('Название не должно превышать 200 символов.')
        
        return name.strip()
    
    def clean_purchase_price(self):
        """Валидация цены."""
        price = self.cleaned_data.get('purchase_price')
        
        if price is not None and price < 0:
            raise ValidationError('Цена не может быть отрицательной.')
        
        if price is not None and price > 999999999:
            raise ValidationError('Цена слишком большая.')
        
        return price
    
    def clean_warranty_period(self):
        """Валидация гарантийного срока."""
        warranty = self.cleaned_data.get('warranty_period')
        
        if warranty is not None and warranty < 0:
            raise ValidationError('Гарантийный срок не может быть отрицательным.')
        
        if warranty is not None and warranty > 1200:  # 100 лет
            raise ValidationError('Гарантийный срок слишком большой.')
        
        return warranty
    
    def clean_photo(self):
        """Валидация фотографии."""
        photo = self.cleaned_data.get('photo')
        
        if photo:
            # Проверка размера файла (10MB)
            if photo.size > 10 * 1024 * 1024:
                raise ValidationError('Размер фото не должен превышать 10 МБ.')
            
            # Проверка расширения
            ext = os.path.splitext(photo.name)[1][1:].lower()
            allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
            if ext not in allowed_extensions:
                raise ValidationError(f'Разрешены только изображения: {", ".join(allowed_extensions)}')
        
        return photo
    
    def clean_document(self):
        """Валидация документа."""
        document = self.cleaned_data.get('document')
        
        if document:
            # Проверка размера файла (10MB)
            if document.size > 10 * 1024 * 1024:
                raise ValidationError('Размер документа не должен превышать 10 МБ.')
            
            # Проверка расширения
            ext = os.path.splitext(document.name)[1][1:].lower()
            allowed_extensions = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'txt']
            if ext not in allowed_extensions:
                raise ValidationError(f'Разрешены только документы: {", ".join(allowed_extensions)}')
        
        return document
    
    def clean(self):
        """Общая валидация формы."""
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        department = cleaned_data.get('department')
        responsible_person = cleaned_data.get('responsible_person')
        
        # Если оборудование в использовании, должно быть назначено подразделение или лицо
        if status == 'in_use' and not department and not responsible_person:
            raise ValidationError(
                'Если оборудование в использовании, укажите подразделение или ответственное лицо.'
            )
        
        return cleaned_data


class AccessoryForm(forms.ModelForm):
    """Форма для аксессуаров."""
    
    class Meta:
        model = Accessory
        fields = ['name', 'quantity', 'serial_number', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
    
    def clean_quantity(self):
        """Валидация количества."""
        quantity = self.cleaned_data.get('quantity')
        
        if quantity is not None and quantity <= 0:
            raise ValidationError('Количество должно быть больше нуля.')
        
        if quantity is not None and quantity > 10000:
            raise ValidationError('Слишком большое количество.')
        
        return quantity
    
    def clean_name(self):
        """Валидация названия аксессуара."""
        name = self.cleaned_data.get('name')
        
        if not name:
            raise ValidationError('Название обязательно.')
        
        if len(name) < 2:
            raise ValidationError('Название должно содержать минимум 2 символа.')
        
        return name.strip()