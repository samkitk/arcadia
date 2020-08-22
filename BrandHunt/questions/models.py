from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def lowercase_answer(value):
    if (value.islower()):
        return value
    else:
        raise ValidationError(
            _('%(value)s should not contain any capital letters'),
            params={'value': value},
        )
# Create your models here.
class Question(models.Model):
        Question_Number = models.IntegerField()
        Question_Text = models.TextField(null=True,blank=True)
        Question_Image = models.ImageField(upload_to='gallery',null=True,blank=True)
        Question_Answer = models.CharField(max_length=50,validators=[lowercase_answer])
        #Answer_Field = models.CharField(max_length=50,validators=[lowercase_answer],null=True)

        #if(Answer_Field==Question_Answer)
        def __str__(self):
            return str(self.Question_Number)