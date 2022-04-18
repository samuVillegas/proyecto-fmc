from email.policy import default
from django import forms
from apps.company.utilities.choose_type.Question import Question
from apps.company.utilities.choose_type.Group import getQuestions

class ContactForm(forms.Form):
    def initials(self, questions):
        count = 1
        for q in questions:
            self.fields['lock' + str(count)] = forms.CharField(initial=q.lock)
            self.fields['question' + str(count)] = forms.CharField(initial=q.question)
            self.fields['image' + str(count)] = forms.CharField(initial=q.image)
            count2 = 1
            for opt, out in zip(q.options, q.outputs):
                self.fields['options' + str(count) + '_' + str(count2)] = forms.CharField(initial=opt)
                self.fields['outputs' + str(count) + '_' + str(count2)] = forms.CharField(initial=out)
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