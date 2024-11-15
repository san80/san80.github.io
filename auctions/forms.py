from django import forms
from .models import *

class AuctionForm(forms.ModelForm):
    class Meta:
        model = auction_list
        fields=['title','description','image_url', 'starting_bid', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'starting_bid': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
            'category': forms.Select()
        }
        category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select a category"  
        )

class CommentForm(forms.ModelForm):
    class Meta:
        model=comments
        fields=["comment"]
        widgets= {
            'comment': forms.Textarea()
        }


class BidsForm(forms.ModelForm):
    class Meta:
        model=bids
        fields=["price"]
        widgets={
            'price': forms.NumberInput()
        }

        