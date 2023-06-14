import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager

##################`UserManager`################################
class ProfileManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

##################`Profile manager`################################
class Profile(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, null=True, blank=True)
    city = models.CharField(max_length=50, blank=True )
    email = models.EmailField(max_length=50, unique=True)
    street = models.CharField(max_length=50, blank=True)
    apartmentnumber = models.DecimalField(max_digits=9, decimal_places=0, null=True, blank=True)
    housenumber = models.DecimalField(max_digits=9, decimal_places=0, null=True, blank=True)
    zipcode = models.DecimalField(max_digits=9, decimal_places=0, null=True, blank=True)
    phone_number = models.CharField(max_length=12,default=False)
    profileimage = models.ImageField(null=True, blank=True, upload_to='profile/')
    firstname = models.CharField(max_length=50,default="changeme") 
    lastname = models.CharField(max_length=50,default="changeme")  
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = ProfileManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


##################`Product`################################

class Product(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50,default=False)
    description = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=9, decimal_places=0)
    size = models.DecimalField(max_digits=9, decimal_places=0, default=0)
    image = models.ImageField(null=True, blank=True, upload_to='products/')

    def __str__(self):
        return self.name


##################`Cart`################################
class Cart(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='user_cart')
    products = models.ManyToManyField(Product, through='CartItem', related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1) 

    def __str__(self):
        return f"CartItem: {self.product})"

##################`Purchase`################################

class Purchase(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='purchases')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Purchase: {self.product} by {self.user}"
