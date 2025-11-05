from django import forms

from auctions.models import List_Auctions


class create_auction_form(forms.ModelForm):
    title = forms.CharField(label="Title ", widget=forms.TextInput(attrs={'class': 'input_place'}))

    description = forms.CharField(label="Description ",
                                  widget=forms.Textarea(attrs={'class': 'description_for_auction input_place'}))
    start_bid = forms.IntegerField(label="Start Bid ", widget=forms.NumberInput(attrs={'class': 'input_place'}))
    category = forms.CharField(label="Category ", required=False,
                               widget=forms.TextInput(attrs={'class': 'input_place'}))
    photo = forms.URLField(label="Image URL ", required=False, widget=forms.URLInput(attrs={'class': 'input_place'}))

    class Meta:
        model = List_Auctions
        fields = ['title', 'description', 'category', 'start_bid', 'photo']
        labels = {
            'title': 'Title',
            'description': 'Description',
            'category': 'Category',
            'photo': 'Image URL',
            'start_bid': 'Start Bid',
        }
