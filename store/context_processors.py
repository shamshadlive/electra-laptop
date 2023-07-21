from cart.models import Wishlist,WishlistItem

def wishlist(request):
    if request.user.is_authenticated:  
        wishlist,created= Wishlist.objects.get_or_create(user=request.user)
        wishlist_items = WishlistItem.objects.filter(wishlist=wishlist, is_active=True).values_list('product_id', flat=True)
    else:
        wishlist_items =[]
    return dict(wishlist_items=wishlist_items)