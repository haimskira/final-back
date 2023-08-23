from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView





urlpatterns = [
    #Login
    path('register/', views.register, name="register"),
    path('login/', TokenObtainPairView.as_view()),
    #Products
    path('product/', views.ProductViews.as_view()),
    path('product/<int:pk>/', views.ProductViews.as_view()),
    #profile url
    path('getprofile/', views.ProfileViews.as_view(), name='get-profile'),
    path('getprofile/<int:pk>', views.ProfileViews.as_view(),name='getprofile'),
    path('getprofile/<int:pk>/update_profile_image/', views.ProfileViews.as_view(), name='update-profile-image'),

    path('profile/purchases/', views.PurchaseViewSet.as_view({'get': 'get_purchase_history'}), name='purchase-list'),

    path('img/<int:pk>/', views.ProfileViews.as_view()),
    path('img/', views.ProfileViews.as_view()),
    path('profile/<int:pk>/', views.ProfileViews.as_view()),
    path('profile/', views.ProfileViews.as_view()),
    path('getprofile/', views.ProfileViews.as_view(), name='get-profile'),
    path('purchase/', views.PurchaseViewSet.as_view({'post': 'create_purchase'}), name='create_purchase'),

    path('user-id/', views.get_user_id),

    #Cart
    path('cart/', views.get_user_cart),
    path('add_cart_item/', views.add_cart_item, name='add_cart_item'),
    path('cart/delete-item/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),

    # path('postcart/', views.post_user_cart),
    # path('postcart/update-item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    # path('cart/history/', views.get_user_cart_history),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
