from email.policy import default
from django import forms
from apps.company.utilities.choose_type.Question import Question
from apps.company.utilities.choose_type.Group import getQuestions

class ContactForm(forms.Form):

    #def __init__(self, quest, *args, **kwargs):

    lock = forms.CharField(max_length=1000)
    question = forms.CharField(max_length=1000)
    image = forms.CharField(max_length=1000)
    options = forms.CharField(max_length=1000)
    outputs = forms.CharField(max_length=1000)

    source = forms.CharField(       # A hidden input for internal use
            max_length=50,              # tell from which page the user sent the message
            widget=forms.HiddenInput()
        )
        
    def initials(self, quest):
        self.fields['lock'].initial = quest.lock
        self.fields['question'].initial = quest.question
        self.fields['image'].initial = quest.image
        self.fields['options'].initial = quest.options
        self.fields['outputs'].initial = quest.outputs

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        lock = cleaned_data.get('lock')
        question = cleaned_data.get('question')
        image = cleaned_data.get('image')
        options = cleaned_data.get('options')
        outputs = cleaned_data.get('outputs')
        if not lock and not question:
            raise forms.ValidationError('You have to write something!')

class ColorfulContactForm(forms.Form):
    name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'style': 'border-color: blue;',
                'placeholder': 'Write your name here'
            }
        )
    )
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'style': 'border-color: green;'})
    )
    message = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(attrs={'style': 'border-color: orange;'}),
        help_text='Write here your message!'
    )