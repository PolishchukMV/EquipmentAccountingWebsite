"""
Формы для назначений оборудования.
"""

from django import forms
from .models import Assignment


class AssignmentForm(forms.ModelForm):
    """Форма для создания и редактирования назначений оборудования."""
    
    class Meta:
        model = Assignment
        fields = [
            'equipment', 'from_department', 'to_department',
            'from_person', 'to_person', 'reason', 'document'
        ]
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Укажите причину назначения...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем классы Bootstrap к полям
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
    
    def clean(self):
        """Общая валидация формы."""
        cleaned_data = super().clean()
        from_dept = cleaned_data.get('from_department')
        to_dept = cleaned_data.get('to_department')
        from_person = cleaned_data.get('from_person')
        to_person = cleaned_data.get('to_person')
        
        # Должен быть указан хотя бы один получатель
        if not to_dept and not to_person:
            raise forms.ValidationError(
                'Укажите хотя бы одно: подразделение или сотрудника получателя.'
            )
        
        # Нельзя назначить оборудование самому себе
        if from_person and to_person and from_person == to_person:
            raise forms.ValidationError(
                'Невозможно назначить оборудование самому себе.'
            )
        
        return cleaned_data


class AssignmentReturnForm(forms.ModelForm):
    """Форма для возврата оборудования."""
    
    class Meta:
        model = Assignment
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Укажите причину возврата (необязательно)...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reason'].widget.attrs.update({'class': 'form-control'})
        self.fields['reason'].required = False
