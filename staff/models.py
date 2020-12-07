from django.db import models
from django.utils.translation import ugettext_lazy
from .managers import TemporalQuerySet
# Create your models here.


class Employee(models.Model):
    emp_num = models.IntegerField(primary_key=True)
    birth_date = models.DateField()
    first_name = models.CharField(max_length=14)
    last_name = models.CharField(max_length=16)
    gender = models.CharField(max_length=1)
    hire_date = models.DateField()

    class Meta:
        db_table = 'staff'

    def __str__(self):
        return "{0} {1}".format(self.first_name, self.last_name)


class Department(models.Model):
    """Danadams Department Model"""
    dept_name = models.CharField(max_length=50, unique=True)
    dept_num = models.CharField(max_length=10, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'departments'
        ordering = ('dept_num',)

    def __str__(self):
        return self.dept_name


class DepartmentStaff(models.Model):
    """Model of staff in each department"""
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, db_column='emp_num')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, db_column='dept_num')
    from_date = models.DateField()
    to_date = models.DateField()

    class Meta:
        db_table = 'employees'
        verbose_name_plural = 'Department Staff'

    def __str__(self):
        return '{0}'.format(self.employee.first_name)


class DepartmentManager(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='emp_num')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, db_column='dept_num')
    from_date = models.DateField()
    to_date = models.DateField()

    objects = TemporalQuerySet.as_manager()

    class Meta:
        db_table = 'dept_manager'
        ordering = ['-from_date']
        verbose_name_plural = 'Department Managers'


class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='emp_num')
    salary = models.IntegerField()
    from_date = models.DateField()
    to_date = models.DateField()

    objects = TemporalQuerySet.as_manager()

    class Meta:
        db_table = 'salaries'
        ordering = ['-from_date']
        verbose_name = 'Salary'
        verbose_name_plural = 'Salaries'


class Title(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='emp_num')
    title = models.CharField(max_length=50)
    from_date = models.DateField()
    to_date = models.DateField(blank=True, null=True)

    objects = TemporalQuerySet.as_manager()

    class Meta:
        db_table = 'titles'
