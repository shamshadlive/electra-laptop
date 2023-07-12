from .models import Wallet

def wallet_balance(request):
    wallet_balance = 0
    try:
        wallet,created = Wallet.objects.get_or_create(user=request.user)
        wallet_balance = wallet.balance 
        
    except Exception:
        wallet_balance = 0
    return dict(wallet_balance=wallet_balance)