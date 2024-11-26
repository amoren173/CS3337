from django import forms
from django.forms import ModelForm
from .models import Book

from django import forms
from .models import Comment


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            'name',
            'web',
            'price',
            'picture',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book name'}),
            'web': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter website URL'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
            'picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

# Comments
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',  # Apply Bootstrap's form-control class
                'rows': 5,  # Optional: Set height
                'placeholder': 'Write your comment here...',  # Optional: Placeholder text
            }),

        }

#Checkout
class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100, label="Full Name", widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
    address = forms.CharField(max_length=255, label="Address", widget=forms.Textarea(attrs={'placeholder': 'Street, City, State, ZIP', 'rows': 3}))
    contact_number = forms.CharField(max_length=15, label="Contact Number", widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))
    payment_method = forms.ChoiceField(
        choices=[
            ('credit_card', 'Credit Card'),
            ('paypal', 'PayPal'),
            ('cash', 'Cash on Delivery'),
        ],
        widget=forms.RadioSelect,
        label="Payment Method",
    )


