from APIApp.models import *
from rest_framework import serializers
from APIApp.common.api_response_message import *
from APIApp.utils import *



class LoginSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(max_length=250, required=True)
    password = serializers.CharField(
        label=("password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        max_length=125,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['id','user_name', 'password']

    def validate(self, data):
        """
        The function validates user input data including username, and password for a user
        account.
        
        :param data: The `validate` method you provided seems to be a part of a Django REST framework
        serializer. The `data` parameter in this context likely represents the input data that needs to
        be validated before further processing
        :return: The `validate` method is returning the `data` dictionary with an additional key-value
        pair `{'user': user}` added to it.
        """
        user_name = data.get('user_name')
        password = data.get('password')

        if not user_name:
            raise serializers.ValidationError(
                            {'message': USERNAME,'status':400},
                            CODE
                        )

        user = None

        if not user and user_name:
            user = User.objects.filter(user_name=user_name).first()

        if not user:
            raise serializers.ValidationError({
                'message':INVALID_USERNAME,'status':400
            })

        if password and not user.check_password(password):
            raise serializers.ValidationError(
                    {'message': INVALID_PASSWORD,'status':400},CODE
                )

        data['user'] = user
        return data
    

# category ------------------------------
class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','category_name','createdby','created_date']
        
    def validate_category_name(self, value):
        if Category.objects.filter(category_name=value).exists():
            raise serializers.ValidationError('Category name already exists.')
        return value
    
class GetCategorySerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format="%d-%m-%Y %I:%M %p")
    edited_date = serializers.DateTimeField(format="%d-%m-%Y %I:%M %p")
    class Meta:
        model = Category
        fields = ['id','category_name','createdby','created_date','editedby',\
            'edited_date']
    
    
    
class PutCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','category_name','editedby',\
            'edited_date']
        
        
    def validate_category_name(self, value):
        cate_id = self.context.get('id')
        existing_cate_with_same_name = Category.objects.exclude(id=cate_id).filter(category_name=value).exists()
        if existing_cate_with_same_name:
            raise serializers.ValidationError('Category name already exists.')
        return value
    
    

# product ------------------------------
class PostProductSerializer(serializers.ModelSerializer):
    price = serializers.FloatField()
    class Meta:
        model = Product
        fields = ['id','product_name','category','price','description','createdby','created_date']
        
    def validate_product_name(self, value):
        if Product.objects.filter(product_name=value).exists():
            raise serializers.ValidationError('Product name already exists.')
        return value
    
class GetProductSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format="%d-%m-%Y %I:%M %p")
    edited_date = serializers.DateTimeField(format="%d-%m-%Y %I:%M %p")
    category_name = serializers.StringRelatedField(source='category.category_name')
    price = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id','product_name','category','price','category_name','description','createdby','created_date','editedby',\
            'edited_date']
        
    def get_price(self, obj):
        return obj.price_()
    
    
    
class PutProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','product_name','category','price','description','editedby',\
            'edited_date']
        
        
    def validate_product_name(self, value):
        cate_id = self.context.get('id')
        existing_cate_with_same_name = Product.objects.exclude(id=cate_id).filter(product_name=value).exists()
        if existing_cate_with_same_name:
            raise serializers.ValidationError('Product name already exists.')
        return value
    