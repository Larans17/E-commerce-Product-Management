
from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    def create_user(self, user_name, password=None, **kwargs):
        if not user_name:
            raise ValueError("The Username field must be set")
        username = self.normalize_email(user_name)
        user = self.model(user_name=username, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, password=None, **kwargs):
        user = self.create_user(
            user_name=user_name,
            password=password,
            is_superadmin=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    user_name = models.CharField(max_length=100, unique=True, error_messages={"unique": "This username already exists."})
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.user_name

    def has_perm(self, perm, obj=None):
        return self.is_superadmin

    def has_module_perms(self, app_label):
        return self.is_superadmin
    
    
    
class Logs(models.Model):
    transaction_name = models.CharField(max_length=500)
    mode = models.CharField(max_length=100)
    log_message = models.TextField()
    user = models.ForeignKey(
        "User",
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="log_user_id",
    )
    ip_address = models.CharField(max_length=100, null=True, blank=True)
    system_name = models.CharField(max_length=100, null=True, blank=True)
    log_date = models.DateTimeField(auto_now=True)
    
    
class Category(models.Model):
    category_name = models.CharField(max_length=250)
    createdby = models.ForeignKey("User", on_delete=models.RESTRICT,null=True,blank=True,related_name="cate_user")
    created_date = models.DateTimeField(auto_now_add=True)
    editedby = models.ForeignKey("User", on_delete=models.RESTRICT,null=True,blank=True,related_name="cate_edit_user")
    edited_date = models.DateTimeField(null=True,blank=True)
    
class Product(models.Model):
    product_name = models.CharField(max_length=1000,unique=True, error_messages={"unique": "This product name already exists."})
    category = models.ForeignKey('Category',on_delete=models.RESTRICT,related_name='product_cate')
    encrypted_price = models.BinaryField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    createdby = models.ForeignKey("User", on_delete=models.RESTRICT,null=True,blank=True,related_name="product_user")
    created_date = models.DateTimeField(auto_now_add=True)
    editedby = models.ForeignKey("User", on_delete=models.RESTRICT,null=True,blank=True,related_name="product_edit_user")
    edited_date = models.DateTimeField(null=True,blank=True)
 
    # Encryption key from settings
    key = settings.ENCRYPTION_KEY
    cipher = Fernet(key)   
    
    
    # Getter for price (decrypting the encrypted value)
    @property
    def price(self):
        if self.encrypted_price:
            decrypted_value = self.cipher.decrypt(self.encrypted_price).decode()
            return float(decrypted_value)
        return None

    # Setter for price (encrypting the value before storing)
    @price.setter
    def price(self, value):
        value_str = str(value).encode()  # Convert the price to string and encode to bytes
        self.encrypted_price = self.cipher.encrypt(value_str)
        
        
    def price_(self):
        if not self.encrypted_price:
            return None  # or handle as needed

        try:
            decrypted_value = self.cipher.decrypt(self.encrypted_price).decode()
            return decrypted_value
        except InvalidToken:
            # Handle the error, possibly log it or return a default value
            return None