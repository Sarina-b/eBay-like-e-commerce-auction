from django.contrib import admin

from auctions.models import User, List_Auctions, Watchlist, Watchlist_Items, Comment, Bids

# Register your models here.

admin.site.register(User)
admin.site.register(List_Auctions)
admin.site.register(Watchlist)
admin.site.register(Watchlist_Items)
admin.site.register(Comment)
admin.site.register(Bids)
