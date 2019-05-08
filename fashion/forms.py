from django import forms
from django.forms import ModelForm
from fashion.models import Clothes, Bidding, Person
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ClothesForm(forms.Form):
    clothes_original_price = forms.FloatField(label='Original Price')
    clothes_sellprice = forms.FloatField(label='Sell Price')
    clothes_size = forms.ChoiceField(label='Size', required=False,
                                     choices=(('', '----'),
                                              ('Small', 'Small'),
                                              ('Medium', 'Medium'),
                                              ('Large', 'Large'),
                                              ('X-Large', 'X-Large'),
                                              ('XX-Large', 'XX-Large')))
    clothes_color = forms.CharField(label='Clothes color', max_length=100)
    clothes_brand = forms.CharField(label='Clothes brand', max_length=100)
    clothes_type = forms.CharField(label='Clothes type', max_length=100)
    clothes_condition = forms.ChoiceField(label='Condition', required=False,
                                          choices=(('', '----'),
                                                   ('New', 'New'),
                                                   ('Good', 'Good'),
                                                   ('Wearable', 'Wearable'),
                                                   ('Broken', 'Broken'),
                                                   ('Bad', 'Bad'))
                                          )
    clothes_details = forms.CharField(label='Clothes details', max_length=100)
    clothes_img = forms.ImageField()


class BiddingForm(forms.Form):
    bidding_price = forms.FloatField(label='Bidding price')


class FilterForm(ModelForm):
    brand = forms.CharField(label='Brand', required=False)
    color = forms.CharField(label='Color', required=False)
    ctype = forms.CharField(label='Clothes Type', required=False)
    size = forms.ChoiceField(label='Size', required=False,
                             choices=(('', '----'),
                                      ('Small', 'Small'),
                                      ('Medium', 'Medium'),
                                      ('Large', 'Large'),
                                      ('X-Large', 'X-Large'),
                                      ('XX-Large', 'XX-Large')))
    condition = forms.ChoiceField(label='Condition', required=False,
                                  choices=(('', '----'),
                                           ('New', 'New'),
                                           ('Good', 'Good'),
                                           ('Wearable', 'Wearable'),
                                           ('Broken', 'Broken'),
                                           ('Bad', 'Bad'))
                                  )
    input_sellprice_low = forms.FloatField(label='Minimum Bidding Price higher than', required=False)
    input_sellprice_high = forms.FloatField(label='Minimum Bidding Price lower than', required=False)
    input_originalprice_low = forms.FloatField(label='Original Price higher than', required=False)
    input_originalprice_high = forms.FloatField(label='Original Price lower than', required=False)

    class Meta:
        model = Clothes
        fields = ['brand', 'color', 'ctype', 'size', 'condition']


class AddFilterForm(forms.Form):
    biddingprice_low = forms.FloatField(label='Latest Bidding Price higher than', required=False)
    biddingprice_high = forms.FloatField(label='Latest Bidding Price lower than', required=False)


class RegistrationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    email = forms.EmailField(label='Email', required=False)
    collegeid = forms.IntegerField(label='College Id', required=False)
    phone = forms.DecimalField(label='Phone Number', required=False)

    class Meta:
        model = Person
        fields = ('email', 'collegeid', 'phone', 'username')
