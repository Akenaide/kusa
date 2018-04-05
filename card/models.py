from django.db import models

# Create your models here.

class Card(models.Model):
    card_id = models.TextField(db_index=True)
    image = models.SlugField(max_length=220)
    yyt = models.SlugField(max_length=220)
    rarity = models.TextField()

    def __str__(self):
        return self.card_id

class Price(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, unique_for_date="timestamp")
    value = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)
