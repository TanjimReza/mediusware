from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self,email,full_name,password=None, **extra_fields):
        if not any([email,full_name,password]):
            raise ValueError("Email, First Name and Last Name are required")
        user = self.model(
            email = self.normalize_email(email),
            full_name = full_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    #! Leaving create_superuser for now
        


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email',max_length=60,unique=True,primary_key=True)
    
    full_name = models.CharField(max_length=50, blank=False, null=False)
    
    # first_name = models.CharField(max_length=20, blank=False, null=False)
    # last_name = models.CharField(max_length=20, blank=False, null=False)
    
    #! Just in case creating an extra field to use in future if needed
    #! Can only be assigned from Admin
    is_admin = models.BooleanField(default=False)
    
    objects = UserManager()
    USERNAME_FIELD = 'email'
    
    def __str__(self):
        return self.email
    
    
    
class Task(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    due_date = models.DateTimeField(blank=False, null=False)
        
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    user = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE)
    
    STATUS_CHOICES = (
        ('pending','Pending'),
        ('completed','Completed'),
    )
    PRIORITY_CHOICES = (
        ('low','Low'),
        ('medium','Medium'),
        ('high','High'),
    )
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    priority = models.CharField(max_length=20,choices=PRIORITY_CHOICES,default='low')
    
    def __str__(self):
        return self.title
    
    # Sort by default by highest priority
    class Meta:
        ordering = ['-priority'] 
        
class TaskPhoto(models.Model):   
    photo = models.ImageField(upload_to='task_photos/')
    task = models.ForeignKey(Task, related_name='photos', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Image of -> {self.task.title} "