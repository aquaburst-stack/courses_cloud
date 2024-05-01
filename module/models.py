from django.db import models

# Create your models here.


class ContactUs(models.Model):
    email = models.EmailField(db_column='email')
    subject = models.CharField(max_length=255, null=True, blank=True, db_column='subject')
    message = models.TextField(db_column='message', null=True, blank=True)

    class Meta:
        db_table = 'ContactUs'
        ordering = ['-id']