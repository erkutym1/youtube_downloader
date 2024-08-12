from django import forms

class YouTubeLinkForm(forms.Form):
    url = forms.URLField(label='YouTube Video Linki', widget=forms.TextInput(attrs={'size': '80'}))

class YouTubeResolutionForm(forms.Form):
    resolution = forms.ChoiceField(label='Çözünürlük Seçin')
