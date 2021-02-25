from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from tinymce.widgets import TinyMCE

from item_management.models import Weapon, Item


class BaseItemForm(ModelForm):
    flavor = forms.CharField(widget=TinyMCE(attrs={'cols': 10, 'rows': 4}, mce_attrs={'height': 150}))
    text_description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 10}))

    def clean(self):
        cleaned_data = super().clean()
        is_attuned = cleaned_data.get('is_attuned')
        player = cleaned_data.get('player')
        if is_attuned and not (player or player.name == 'Party'):
            self.add_error('is_attuned', ValidationError('Must have an owner to be attuned'))


class WeaponForm(BaseItemForm):
    class Meta:
        model = Weapon
        # fields = '__all__'
        fields = ('name', 'player', 'text_description', 'flavor', 'requires_attunement', 'is_attuned', 'is_equipped',
                  'item_slot')
        exclude = 'obtained_from',
        # fields = 'name', 'flavor', 'rarity', 'requires_attunement', 'is_attuned', 'player', 'obtained_from',
        # 'quantity'


class ProjectAdminForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        widgets = {
            'text_description': TinyMCE(mce_attrs={'width': '75%', 'height': 300}),
            'flavor': TinyMCE(mce_attrs={'width': '50%', 'height': 200})
        }
