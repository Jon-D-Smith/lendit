from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from taggit.managers import TaggableManager
from taggit.models import Tag, TaggedItem
# Create your models here.

class Item(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'av', 'Available'
        BORROWED = 'br', 'Borrowed'
        LOST = 'ls', 'Lost'
        REPAIR = 'nr', 'Needs Repair'
        REPLACE = 're', 'Needs Replacing'
        PENDING = 'pc', 'Pending Checkin'

    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='media/item_images/', default='media/default.jpg')
    description = models.TextField(blank=True, null=True)
    replacement_link = models.URLField(max_length=2000, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tags = TaggableManager()
    status = models.CharField(max_length=3, choices=Status, default=Status.AVAILABLE)
    is_hidden = models.BooleanField(default=False)
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    last_borrowed_at = models.DateTimeField(blank=True, null=True)
    checked_in_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        # This will attempt to go into the item-detail url and inject the items primary key into the <int:pk> portion of the url
        return reverse("item-detail", kwargs={"pk": self.pk})
    


class BorrowEvent(models.Model):
    item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name="borrow_events")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    borrowed_at = models.DateTimeField(default=timezone.now)
    returned_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f"{self.user} borrowed {self.item.name} on {self.borrowed_at.strftime('%Y-%m-%d %H:%M')}"
    

class InventoryTag(Tag):
    class Meta:
        proxy = True
        app_label = 'inventory'
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

class InventoryTaggedItem(TaggedItem):
    class Meta:
        proxy = True
        app_label = 'inventory'
        verbose_name = 'Tagged Item'
        verbose_name_plural = 'Tagged Items'