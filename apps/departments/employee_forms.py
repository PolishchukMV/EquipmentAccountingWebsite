"""
Формы для управления сотрудниками.
"""

from django import forms
from .models import Employee
from apps.accounts.models import CustomUser


class EmployeeForm(forms.ModelForm):
    """Форма для создания и редактирования сотрудника."""
    
    username = forms.CharField(
        max_length=150,
        required=True,
        label='Имя пользователя',
        help_text='Пользователь должен существовать в системе'
    )
    
    class Meta:
        model = Employee
        fields = [
            'username', 'department', 'position',
            'employee_id', 'hire_date', 'is_active'
        ]
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'username':
                field.widget.attrs.update({'class': 'form-control'})
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            user = CustomUser.objects.get(username=username)
            # Проверяем, нет ли уже сотрудника с таким пользователем
            if self.instance.pk:
                if Employee.objects.filter(user=user).exclude(pk=self.instance.pk).exists():
                    raise forms.ValidationError('У этого пользователя уже есть запись сотрудника.')
            else:
                if Employee.objects.filter(user=user).exists():
                    raise forms.ValidationError('У этого пользователя уже есть запись сотрудника.')
            return username
        except CustomUser.DoesNotExist:
            raise forms.ValidationError('Пользователь с таким именем не найден.')
    
    def clean_employee_id(self):
        employee_id = self.cleaned_data.get('employee_id')
        
        if self.instance.pk:
            if Employee.objects.filter(employee_id__iexact=employee_id).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Сотрудник с таким номером уже существует.')
        else:
            if Employee.objects.filter(employee_id__iexact=employee_id).exists():
                raise forms.ValidationError('Сотрудник с таким номером уже существует.')
        
        return employee_id.upper()
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Получаем пользователя по имени
        username = self.cleaned_data.get('username')
        instance.user = CustomUser.objects.get(username=username)
        
        if commit:
            instance.save()
        return instance
