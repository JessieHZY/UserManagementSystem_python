from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.

# class PermissionList(models.Model):
#     name = models.CharField(max_length=64)
#     url = models.CharField(max_length=255)

#     def __unicode__(self):
#         return '%s(%s)' %(self.name,self.url)
                                              
# class RoleList(models.Model):
#     name = models.CharField(max_length=64)
#     permission = models.ManyToManyField(PermissionList,null=True,blank=True)

#     def __unicode__(self):
#         return self.name


class UserManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # def create_superuser(self,email,username,password):
    #     user = self.create_user(email,
    #         username = username,
    #         password = password,
    #     )

    #     user.is_active = True
    #     user.is_superuser = True
    #     user.save(using=self._db)
    #     return user

# class FormalUser(AbstractBaseUser):
class User(AbstractBaseUser):
    # username = models.CharField(max_length=40, unique=True, db_index=True)
    username = models.CharField(max_length=40, unique=True, db_index=True,primary_key=True)
    email = models.EmailField(max_length=255)
    is_active = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)
    # user_id = models.IntegerField(max_length=10, null=True)
    # nickname = models.CharField(max_length=64, null=True)
    # sex = models.CharField(max_length=2, null=True)
    # role = models.ForeignKey(RoleList,null=True,blank=True)

    user_id = models.IntegerField(null=True)
    
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    # def has_perm(self,perm,obj=None):
    #     if self.is_active and self.is_superuser:
    #         return True


    # upload_to 指定上传文件位置
    # 这里指定存放在img/ 目录下
    # headimg = models.FileField(upload_to="images/",null=True)
    headimg = models.FileField(upload_to="images/",null=True)
   
 
    

  
  