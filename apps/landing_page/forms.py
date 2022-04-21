from email.policy import default
from django import forms
from apps.company.utilities.choose_type.Question import Question 
from apps.company.utilities.data_flow.Question import Flow
from apps.company.utilities.data_flow.Question import Question as FlowQuestion

class ContactForm(forms.Form):
    def initials(self, questions):
        count = 1
        size = 40
        for q in questions:
            if isinstance(q, Question) or isinstance(q, FlowQuestion):
                self.fields['type' + str(count)] = forms.CharField(initial='Pregunta')
                self.fields['lock' + str(count)] = forms.CharField(initial=q.lock, 
                    widget=forms.Textarea(attrs={"rows":1, "cols":size/2, "style": "resize: none"}))
                self.fields['question' + str(count)] = forms.CharField(initial=q.question, 
                    required=False, widget=forms.Textarea(attrs={"rows":(len(q.question)/size) + 1, "cols":size}))
                if hasattr(q, 'reference'):
                    self.fields['reference' + str(count)] = forms.CharField(initial=q.reference, 
                        required=False, widget=forms.Textarea(attrs={"rows":(len(q.reference)/size) + 1, "cols":size}))
                self.fields['image' + str(count)] = forms.CharField(initial='\n'.join(q.image.split(';')), 
                    required=False, widget=forms.Textarea(attrs={"rows":len(q.image.split(';')) + 1, "cols":size}))
                count2 = 1
                for opt, out in zip(q.options, q.outputs):
                    self.fields['option' + str(count) + '_' + str(count2)] = forms.CharField(initial=opt, 
                        required=False, widget=forms.Textarea(attrs={"rows":(len(opt)/size)+1, "cols":size}))
                    self.fields['output' + str(count) + '_' + str(count2)] = forms.CharField(initial=out,  
                        required=False, widget=forms.Textarea(attrs={"rows":(len(out)/size)+1, "cols":size}))
                    count2 += 1
            elif isinstance(q, Flow):
                self.fields['type' + str(count)] = forms.CharField(initial='Flujo')
                self.fields['lock' + str(count)] = forms.CharField(initial=q.lock, 
                    widget=forms.Textarea(attrs={"rows":1, "cols":size/2, "style": "resize: none"}))
                self.fields['reference' + str(count)] = forms.CharField(initial=q.reference, required=False,
                    widget=forms.Textarea(attrs={"rows":(len(q.reference)/size) + 1, "cols":size}))
                self.fields['law' + str(count)] = forms.CharField(initial=q.law, required=False,
                    widget=forms.Textarea(attrs={"rows":(len(q.law)/size) + 1, "cols":size}))
            count += 1
        self.fields['size'] = forms.CharField(initial=str(count-1))