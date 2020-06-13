from django import forms
from home.models import Comment
from multiphoto.models import MultiPhoto, Image, MultiComment


class MultiForm(forms.ModelForm):
    class Meta:
        model = MultiPhoto
        fields = ['title', 'content']


class MultiCommentForm(forms.ModelForm):
    class Meta:
        model = MultiComment
        fields = ('text',)


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['file',]


ImageFormSet = forms.inlineformset_factory(MultiPhoto, Image, form=ImageForm, extra=5)
