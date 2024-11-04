from tortoise import models, fields

class Chat(models.Model):
    id = fields.IntField(pk=True)
    message = fields.TextField()
    response = fields.TextField()
    model = fields.CharField(max_length=100)
    chated_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.id

    class Meta:
        table = "chat"
        app = "app_main"