from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.cats, name="categories"),
    path("categories/<int:category_id>",views.cat_product,name="cat_product"),
    path("add_comment",views.add_comment,name="add_comment"),
    
   
    path("watchlist", views.watchlist, name="watchlist"),
    path("product/<int:auction_id>", views.productdetails, name="auction_detail"),
    path("register_product", views.register_product, name="register_product"),
    path("watchlist/<int:remove_id>",views.remove_watchlist,name="remove_watchlist"),
    path("add_comment", views.add_comment, name="add_comment"),
    path("update_bid", views.update_bid, name="update_bid"),
    path("stop_bid", views.stop_bid, name="stop_bid"),
    

]
