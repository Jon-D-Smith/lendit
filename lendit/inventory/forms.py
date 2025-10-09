from taggit.models import Tag
from django import forms 
from .models import Item

class ItemAdminForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    tags.help_text = "Click Taggit -> Tags to add new tag options"

    class Meta:
        model = Item
        fields = '__all__'
        help_texts = {
            'description' : 'File uploads < 20mb',
            'replacement_link' : 'For shortened Amazon links click Share->Copy Link',
            'image' : '< 20mb',
        }