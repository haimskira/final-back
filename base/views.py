from .models import Cart, CartItem, Product, Profile, Purchase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from datetime import datetime
from django.utils import timezone

from rest_framework import status
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import viewsets

User = get_user_model()

################################ Create new user and cart for the user #################################


@api_view(['POST'])
def register(request):
    data = request.data
    # Validate the data
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return Response({'error': 'Username, email, and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
    # Check if the username or email already exists
    if User.objects.filter(username=data['username']).exists() or User.objects.filter(email=data['email']).exists():
        return Response({'error': 'Username or email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
    # Create a new user
    user = User.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
  # Create a cart for the user
    cart = Cart.objects.create(user=user)
    # Associate the cart with the user
    user.user_cart = cart
    user.save()

    return Response({'message': 'Registration successful.'}, status=status.HTTP_201_CREATED)

######################## Get User ID ############################
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_id(request):
    user_id = request.user.id
    return Response({'user_id': user_id})

################################ PRODUCT CRUD #################################


class ProductSerializer(serializers.ModelSerializer):
    # image_url = serializers.ImageField(source='image.url')

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image','size','category']


class ProductViews(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk=None):
        if pk:
            product = self.get_object(pk)
            if product:
                serializer = ProductSerializer(product)
                return Response(serializer.data)
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        prodname = request.query_params.get('prodname')
        if prodname:
            products = Product.objects.filter(name__icontains=prodname)
        else:
            products = Product.objects.all()

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        product = self.get_object(pk)
        if not product:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        product = self.get_object(pk)
        if not product:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


############################## Cart CRUD Shit ##########################################
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'updated_at']


class GetCartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity']

class PostCartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    price = serializers.CharField(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'price']

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_cart(request):
    user = request.user
    cart = user.user_cart

    if request.method == 'GET':
        cart_items = CartItem.objects.filter(cart=cart)
        serialized_cart_items = GetCartItemSerializer(cart_items, many=True)
        return Response({'cartItems': serialized_cart_items.data})
    
@api_view(['POST'])
def add_cart_item(request):
    user = request.user
    cart = user.user_cart
    item_data = request.data
    print("Add cart item")

    product_id = item_data.get('product')
    existing_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()

    if existing_item:
        existing_item.quantity += item_data.get('quantity', 1)
        existing_item.save()
        cart_item_id = existing_item.id
    else:
        item_data['cart'] = cart.id
        serializer = PostCartItemSerializer(data=item_data)
        if serializer.is_valid():
            cart_item = serializer.save()
            cart_item_id = cart_item.id
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    response_data = {
        'message': 'Cart item added/updated successfully',
        'cartItemId': cart_item_id
    }
    return Response(response_data, status=status.HTTP_201_CREATED)


# @api_view(['POST'])
# def post_user_cart(request):
#     user = request.user
#     cart = user.user_cart
#     print("posting user cart")


#     if request.method == 'POST':
#         cart_items_data = request.data.get('cartItems', [])
#         existing_items = CartItem.objects.filter(cart=cart)

#         # Check if each item already exists in the cart
#         for item_data in cart_items_data:
#             product_id = item_data.get('product')
#             if existing_items.filter(product_id=product_id).exists():
#                 # Skip saving the item if it already exists in the cart
#                 continue
#             item_data['cart'] = cart.id
#             serializer = PostCartItemSerializer(data=item_data)
#             if serializer.is_valid():
#                 serializer.save()
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         return Response({'message': 'Cart items created successfully'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def update_cart_item(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id)
        serializer = PostCartItemSerializer(instance=cart_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
    except CartItem.DoesNotExist:
        return Response({"message": "Cart item not found."}, status=404)

@api_view(['DELETE'])
def delete_cart_item(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id)
        cart_item.delete()
        return Response({"message": "Cart item deleted successfully."}, status=200)
    except CartItem.DoesNotExist:
        return Response({"message": "Cart item not found."}, status=404)

class PurchaseHistorySerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CartItem
        fields = ['product']

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_cart_history(request):
    user = request.user
    cart = user.user_cart

    # Retrieve the purchase history of the cart
    purchase_history = cart.cartitem_set.all()

    # Serialize the purchase history data
    history_serializer = PurchaseHistorySerializer(purchase_history, many=True)

    return Response(history_serializer.data)

################################ PROFILE CRUD #################################


class ProfileSerializer(serializers.ModelSerializer):
    profileimage = serializers.SerializerMethodField()

    def get_profileimage(self, profile):
        if profile.profileimage:
            return profile.profileimage.url
        return None
 
    class Meta:
        model = Profile
        fields = ['pk', 'username', 'firstname', 'lastname','phone_number', 'city', 'street', 'apartmentnumber', 'housenumber',
                  'zipcode', 'profileimage', 'is_active', 'is_staff','email']



class ProfileViews(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return None

    def get(self, request, pk=None):
        if pk:
            profile = self.get_object(pk)
            if profile:
                serializer = ProfileSerializer(profile)
                return Response(serializer.data)
            return Response({'error': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve profiles only for the authenticated user
        profiles = Profile.objects.filter(username=request.user)

        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def post(self, request, pk=None):
        profile = self.get_object(pk)
        if not profile:
            return Response({'error': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the authenticated user is the owner of the profile
        if profile != request.user:
            return Response({'error': 'You are not authorized to modify this profile.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            # Update the profile image if included in the request
            if 'profileimage' in request.FILES:
                profileimage = request.FILES['profileimage']
                profile.profileimage.delete()  # Delete the previous image
                profile.profileimage.save(profileimage.name, profileimage)

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        profile = self.get_object(pk)
        if not profile:
            return Response({'error': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        if profile.username != request.user.username:
            return Response({'error': 'You are not authorized to delete this profile.'}, status=status.HTTP_403_FORBIDDEN)

        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, pk=None):
        profile = self.get_object(pk)
        if not profile:
            return Response({'error': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the authenticated user is the owner of the profile
        if profile != request.user:
            return Response({'error': 'You are not authorized to modify this profile.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            # Update the profile image if included in the request
            if 'profileimage' in request.FILES:
                profileimage = request.FILES['profileimage']
                profile.profileimage.delete()  # Delete the previous image
                profile.profileimage.save(profileimage.name, profileimage)

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

    @action(detail=True, methods=['post'], name='Update Profile Image')
    def update_profile_image(self, request, pk=None):
        profile = self.get_object(pk)
        if not profile:
            return Response({'error': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the authenticated user is the owner of the profile
        if profile.username != request.user.username:
            return Response({'error': 'You are not authorized to modify this profile.'}, status=status.HTTP_403_FORBIDDEN)

        # Update the profile image if included in the request
        if 'profileimage' in request.FILES:
            profileimage = request.FILES['profileimage']
            profile.profileimage.delete()  # Delete the previous image
            profile.profileimage = profileimage
            profile.save()

            serializer = ProfileSerializer(profile)
            return Response(serializer.data)

        return Response({'error': 'Profile image not provided.'}, status=status.HTTP_400_BAD_REQUEST)



##########################################PurchaseViewSet######################################################



class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['id', 'user', 'product', 'quantity']

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated] 

    User = get_user_model()


    @action(detail=False, methods=['post'])
    def create_purchase(self, request):
        product_id = request.data.get('productId')
        quantity = request.data.get('quantity')
        user = request.user 

        # Retrieve the product and create the purchase entry
        product = Product.objects.get(pk=product_id)
        purchase = Purchase.objects.create(user=user, product=product, quantity=quantity)

        serializer = self.get_serializer(purchase)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)





    @action(detail=False, methods=['get'])
    def get_purchase_history(self, request):
        user = request.user
        purchases = Purchase.objects.select_related('product').filter(user=user)

        purchase_history = []
    
        for purchase in purchases:
            product = purchase.product
            purchase_date = purchase.purchase_date.strftime('%Y-%m-%d %H:%M:%S') if purchase.purchase_date else None

            purchase_data = {
                'id': purchase.id,
                'product_name': product.name,
                'product_category': product.category,
                'product_description': product.description,
                'product_price': product.price,
                'product_image': product.image.url if product.image else None,
                'quantity': purchase.quantity,
                'purchase_date': purchase_date,
            }
            purchase_history.append(purchase_data)
    
        return Response(purchase_history)


    