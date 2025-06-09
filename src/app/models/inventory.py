from tortoise import Model, fields
import unidecode


class Inventory(Model):
    name = fields.CharField(max_length=200)
    name_unaccent = fields.TextField(null=True, blank=True)
    quantity = fields.BigIntField(default=0)
    price = fields.FloatField(default=0)
    information = fields.TextField(null=True, blank=True)

    class Meta:
        table = 'inventory'

    def save(self, using_db=None, update_fields=None, force_create=False, force_update=False):
        if not self.id:
            self.name_unaccent = unidecode.unidecode(self.name)
        return super().save(using_db, update_fields, force_create, force_update)

    def __str__(self):
        return self.name
