"""
Тесты для моделей приложения equipment.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.departments.models import Department
from apps.equipment.models import Category, Equipment, Assignment, EquipmentLog, Accessory


UserModel = get_user_model()


class CategoryModelTest(TestCase):
    """Тесты для модели Category."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.parent_category = Category.objects.create(
            name='Электроника',
            code='ELEC'
        )
        
        self.child_category = Category.objects.create(
            name='Компьютеры',
            code='COMP',
            parent=self.parent_category
        )
    
    def test_create_category(self):
        """Тест создания категории."""
        category = Category.objects.create(
            name='Мебель',
            code='FURN'
        )
        
        self.assertEqual(category.name, 'Мебель')
        self.assertEqual(category.code, 'FURN')
        self.assertIsNone(category.parent)
    
    def test_category_with_parent(self):
        """Тест категории с родителем."""
        self.assertEqual(self.child_category.parent, self.parent_category)
    
    def test_category_string_representation(self):
        """Тест строкового представления категории."""
        category = Category.objects.create(name='Тест', code='TEST')
        self.assertEqual(str(category), 'Тест')
    
    def test_category_code_unique(self):
        """Тест уникальности кода категории."""
        Category.objects.create(name='Категория 1', code='CAT1')
        
        with self.assertRaises(Exception):
            Category.objects.create(name='Категория 2', code='CAT1')
    
    def test_nested_categories(self):
        """Тест вложенных категорий."""
        level1 = Category.objects.create(name='Уровень 1', code='L1')
        level2 = Category.objects.create(name='Уровень 2', code='L2', parent=level1)
        level3 = Category.objects.create(name='Уровень 3', code='L3', parent=level2)
        
        self.assertEqual(level2.parent, level1)
        self.assertEqual(level3.parent, level2)


class EquipmentModelTest(TestCase):
    """Тесты для модели Equipment."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.department = Department.objects.create(name='IT-отдел', code='IT')
        self.category = Category.objects.create(name='Компьютеры', code='COMP')
        
        self.user = UserModel.objects.create_user(
            username='responsible',
            email='resp@example.com',
            password='pass123',
            department=self.department
        )
        
        self.equipment_data = {
            'inventory_number': '000001',
            'name': 'Ноутбук Dell',
            'category': self.category,
            'status': 'in_use',
            'serial_number': 'SN123456',
            'manufacturer': 'Dell',
            'model': 'Latitude 5420',
            'purchase_date': '2024-01-15',
            'purchase_price': 85000,
            'warranty_period': 24,
            'department': self.department,
            'responsible_person': self.user,
            'location': 'Кабинет 301'
        }
    
    def test_create_equipment(self):
        """Тест создания оборудования."""
        equipment = Equipment.objects.create(**self.equipment_data)
        
        self.assertEqual(equipment.inventory_number, '000001')
        self.assertEqual(equipment.name, 'Ноутбук Dell')
        self.assertEqual(equipment.category, self.category)
        self.assertEqual(equipment.status, 'in_use')
    
    def test_equipment_string_representation(self):
        """Тест строкового представления оборудования."""
        equipment = Equipment.objects.create(**self.equipment_data)
        self.assertEqual(str(equipment), '000001 - Ноутбук Dell')
    
    def test_equipment_status_choices(self):
        """Тест выбора статусов оборудования."""
        equipment = Equipment.objects.create(**self.equipment_data)
        
        statuses = [choice[0] for choice in Equipment.STATUS_CHOICES]
        self.assertIn(equipment.status, statuses)
    
    def test_equipment_inventory_number_unique(self):
        """Тест уникальности инвентарного номера."""
        Equipment.objects.create(**self.equipment_data)
        
        with self.assertRaises(Exception):
            Equipment.objects.create(
                inventory_number='000001',
                name='Другой ноутбук',
                category=self.category,
                status='in_use'
            )
    
    def test_equipment_without_category(self):
        """Тест оборудования без категории."""
        equipment = Equipment.objects.create(
            inventory_number='000002',
            name='Оборудование без категории',
            status='in_stock'
        )
        
        self.assertIsNone(equipment.category)
    
    def test_equipment_without_department(self):
        """Тест оборудования без подразделения."""
        equipment = Equipment.objects.create(
            inventory_number='000003',
            name='Оборудование без подразделения',
            status='in_stock'
        )
        
        self.assertIsNone(equipment.department)
    
    def test_equipment_timestamps(self):
        """Тест временных меток оборудования."""
        equipment = Equipment.objects.create(**self.equipment_data)
        
        self.assertIsNotNone(equipment.created_at)
        self.assertIsNotNone(equipment.updated_at)
    
    def test_equipment_warranty_expired(self):
        """Тест истечения гарантии."""
        from datetime import date, timedelta
        
        # Оборудование с истекшей гарантией
        old_purchase_date = date.today() - timedelta(days=730)  # 2 года назад
        equipment = Equipment.objects.create(
            inventory_number='000004',
            name='Старое оборудование',
            status='in_use',
            purchase_date=old_purchase_date,
            warranty_period=12  # 1 год гарантии
        )
        
        # Гарантия должна быть истекшей
        self.assertTrue(equipment.warranty_expired())
    
    def test_equipment_warranty_valid(self):
        """Тест действующей гарантии."""
        equipment = Equipment.objects.create(
            inventory_number='000005',
            name='Новое оборудование',
            status='in_use',
            purchase_date='2024-01-15',
            warranty_period=24  # 2 года гарантии
        )
        
        # Гарантия должна быть действующей
        self.assertFalse(equipment.warranty_expired())


class AssignmentModelTest(TestCase):
    """Тесты для модели Assignment."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.department1 = Department.objects.create(name='Отдел 1', code='DEPT1')
        self.department2 = Department.objects.create(name='Отдел 2', code='DEPT2')
        
        self.user = UserModel.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='pass123'
        )
        
        self.equipment = Equipment.objects.create(
            inventory_number='000001',
            name='Ноутбук',
            status='in_use',
            department=self.department1
        )
        
        self.assignment_data = {
            'equipment': self.equipment,
            'from_department': self.department1,
            'to_department': self.department2,
            'user': self.user,
            'received_by': self.user
        }
    
    def test_create_assignment(self):
        """Тест создания назначения."""
        assignment = Assignment.objects.create(**self.assignment_data)
        
        self.assertEqual(assignment.equipment, self.equipment)
        self.assertEqual(assignment.from_department, self.department1)
        self.assertEqual(assignment.to_department, self.department2)
    
    def test_assignment_string_representation(self):
        """Тест строкового представления назначения."""
        assignment = Assignment.objects.create(**self.assignment_data)
        expected = f"Перемещение: 000001 - Ноутбук (Отдел 1 -> Отдел 2)"
        self.assertEqual(str(assignment), expected)
    
    def test_assignment_timestamp(self):
        """Тест временной метки назначения."""
        assignment = Assignment.objects.create(**self.assignment_data)
        
        self.assertIsNotNone(assignment.timestamp)


class EquipmentLogModelTest(TestCase):
    """Тесты для модели EquipmentLog."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.user = UserModel.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='pass123'
        )
        
        self.equipment = Equipment.objects.create(
            inventory_number='000001',
            name='Ноутбук',
            status='in_use'
        )
    
    def test_create_log(self):
        """Тест создания журнала."""
        log = EquipmentLog.objects.create(
            equipment=self.equipment,
            action='created',
            user=self.user,
            old_value='',
            new_value='Новое оборудование'
        )
        
        self.assertEqual(log.equipment, self.equipment)
        self.assertEqual(log.action, 'created')
        self.assertEqual(log.user, self.user)
    
    def test_log_string_representation(self):
        """Тест строкового представления журнала."""
        log = EquipmentLog.objects.create(
            equipment=self.equipment,
            action='updated',
            user=self.user
        )
        
        expected = f"000001 - Ноутбук: updated (testuser)"
        self.assertEqual(str(log), expected)
    
    def test_log_actions(self):
        """Тест действий в журнале."""
        log = EquipmentLog.objects.create(
            equipment=self.equipment,
            action='status_changed',
            user=self.user
        )
        
        actions = [choice[0] for choice in EquipmentLog.ACTION_CHOICES]
        self.assertIn(log.action, actions)


class AccessoryModelTest(TestCase):
    """Тесты для модели Accessory."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.equipment = Equipment.objects.create(
            inventory_number='000001',
            name='Ноутбук',
            status='in_use'
        )
        
        self.accessory_data = {
            'equipment': self.equipment,
            'name': 'Документация',
            'quantity': 1,
            'serial_number': 'DOC001'
        }
    
    def test_create_accessory(self):
        """Тест создания аксессуара."""
        accessory = Accessory.objects.create(**self.accessory_data)
        
        self.assertEqual(accessory.equipment, self.equipment)
        self.assertEqual(accessory.name, 'Документация')
        self.assertEqual(accessory.quantity, 1)
    
    def test_accessory_string_representation(self):
        """Тест строкового представления аксессуара."""
        accessory = Accessory.objects.create(**self.accessory_data)
        self.assertEqual(str(accessory), 'Документация (Ноутбук)')
    
    def test_accessory_without_serial_number(self):
        """Тест аксессуара без серийного номера."""
        accessory = Accessory.objects.create(
            equipment=self.equipment,
            name='Кабель',
            quantity=2
        )
        
        self.assertIsNone(accessory.serial_number)