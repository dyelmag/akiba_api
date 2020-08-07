from django.db import models
from django.contrib.auth.models import User

# Create your models here.


def pasta_foto(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/capa/{1}'.format(instance.user.id, filename)


class Perfil(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='perfil')
    profile_picture = models.ImageField(upload_to=pasta_foto, blank=True)
    gender = models.IntegerField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    biography = models.CharField(max_length=400, null=True, blank=True)
