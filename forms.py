from django import forms


class MainForm(forms.Form):

    destination_address = forms.CharField(
        label='Destination Address', 
        widget=forms.TextInput(attrs={'size': '40'}),
        max_length=100
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['destination_address'].widget.attrs.update({
            'placeholder': 'Enter Wallet Address'
        })
