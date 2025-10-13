from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile


# users(user_id,email,username,password)
#
# list_auctions(auction_id,user_id,title,description,start_bid,photo,category,start_date,end_date,active)
#
# watchlist(watchlist_id,user_id UNIQUE)
#
# watchlist_items(id,watchlist_id,auction_id)
#
# comments(comment_id,user_id,auction_id,text,written_at)
#
# bids(bid_id,user_id ,auction_id ,amount,written_at)


class User(AbstractUser):
    pass


class List_Auctions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='List_Auctions')
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_bid = models.FloatField()
    photo = models.URLField(max_length=500, blank=True, null=True)
    photo_file = models.ImageField(upload_to='auction_photos/', blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def convert_URL_to_file(self):
        if self.photo and not self.photo_file:
            try:
                temp_space = NamedTemporaryFile(delete=True)
                temp_space.write(urlopen(self.photo).read())
                temp_space.flush()
                self.photo_file.save(f"image_{self.pk}.jpg", File(temp_space), save=False)
            except:
                pass

    def __str__(self):
        return (f" {self.id} + {self.user} + {self.title} + {self.description} + {self.start_date} - {self.end_date}"
                f"+ {self.category} + {self.start_bid} + {self.photo} + {self.active}")


class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='Watchlist', blank=True, null=True)

    def __str__(self):
        return f"{self.user} + {self.id}"


class Watchlist_Items(models.Model):
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE, related_name='Watchlist_Items')
    auction = models.ForeignKey(List_Auctions, on_delete=models.CASCADE, related_name='Watchlist_Items'
                                , blank=True, null=True)

    def __str__(self):
        return f"{self.id} + {self.watchlist} + {self.auction}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='Comments', null=True, blank=True)
    # Using on_delete=models.SET_NULL so if the user is deleted, the comment is kept for reference.
    author_name = models.CharField(max_length=100)
    auction = models.ForeignKey(List_Auctions, on_delete=models.CASCADE, related_name='Comments', blank=True, null=True)
    text = models.TextField()
    written_at = models.DateTimeField()

    def __str__(self):
        return f"{self.id} + {self.user} + {self.auction} + {self.text} + {self.written_at}"


class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Bids')
    auction = models.ForeignKey(List_Auctions, on_delete=models.CASCADE, related_name='Bids')
    amount = models.FloatField()
    written_at = models.DateTimeField()

    def __str__(self):
        return f"{self.id} + {self.user} + {self.auction} + {self.amount} + {self.written_at}"
