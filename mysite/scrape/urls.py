from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.contrib import admin

urlpatterns = [
    path("", views.search, name="search"),
    path("search_result", views.search_result, name ="search_result"),
    # path("database", views.show_db, name="show_db"),
    path("form/", views.form_view, name="form"),
    path("products/", views.products_view, name="products"),
    path("sign-up", views.sign_up, name="sign_up"),
    path('add-to-favourite/<int:product_id>/', views.add_to_favourite, name='add-to-favourite'),
    path('remove-from-favourite/<int:product_id>/', views.remove_from_favourite, name='remove-from-favourite'),
    path('favourite/', views.view_favourite, name='favourite'),
    path('compare/', views.compare, name='compare'),
    path('compare/result/', views.compare_result, name='compare_result'),
    path('admin/', admin.site.urls),
    path('price_history/<int:product_id>/', views.price_history, name='price_history'),
    path('product/<int:product_id>/review/', views.add_review, name='add_review'),
    path('product/<int:product_id>/reviews/', views.view_reviews, name='view_reviews'),
    path("verify_code", views.verify_code, name="verify_code"),
    path('add_product/', views.add_product, name='add_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('change_product/<int:product_id>/', views.change_product, name='change_product'),
    path('signup_shop/', views.shop_user_signup, name='shop_user_signup'),
    path('shop/', views.shop, name='shop'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)