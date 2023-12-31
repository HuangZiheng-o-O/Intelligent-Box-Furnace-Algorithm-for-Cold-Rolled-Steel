from django.db import models

# Create your models here.

#材料编号、材料名称
class Materials(models.Model):
    id = models.IntegerField(db_column="id", null=False, primary_key=True)
    material = models.TextField(db_column="material", null=False)
    class Meta:
        managed: True
        db_table = 'material'
    def __str__(self):
        return '编号：%\t材料：%s' %(self.id, self.material)