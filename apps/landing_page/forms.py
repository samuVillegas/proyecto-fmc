from email.policy import default
from django import forms
from apps.company.utilities.choose_type.Question import Question
from apps.company.utilities.choose_type.Group import getQuestions

class ContactForm(forms.Form):
    source = forms.CharField(       # A hidden input for internal use
            max_length=50,              # tell from which page the user sent the message
            widget=forms.HiddenInput()
        )

    def initials(self, questions):
        count = 1
        for q in questions:
            self.fields['lock' + str(count)] = forms.CharField()
            self.fields['lock' + str(count)].initial = q.lock
            self.fields['question' + str(count)] = forms.CharField()
            self.fields['question' + str(count)].initial = q.question
            self.fields['image' + str(count)] = forms.CharField()
            self.fields['image' + str(count)].initial = q.image
            count2 = 1
            for opt, out in zip(q.options, q.outputs):
                self.fields['options' + str(count) + '_' + str(count2)] = forms.CharField()
                self.fields['options' + str(count) + '_' + str(count2)].initial = opt
                self.fields['outputs' + str(count) + '_' + str(count2)] = forms.CharField()
                self.fields['outputs' + str(count) + '_' + str(count2)].initial = out
                count2 += 1
            count += 1

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