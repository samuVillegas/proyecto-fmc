from email.policy import default
from django import forms
from apps.company.utilities.choose_type.Question import Question 
from apps.company.utilities.data_flow.Question import Flow
from apps.company.utilities.data_flow.Question import Question as FlowQuestion
import logging

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
                self.fields['numOptions' + str(count)] = forms.CharField(initial=str(len(q.options)))
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
    
    def addOption(self, form):
        size = 40
        key_list = list(form.keys())
        val_list = list(form.values())
        key_list.pop(0)
        val_list.pop(0)
        self.fields.clear()
        for key,val in zip(key_list,val_list):
            if 'add' not in key:
                lastKey = key
                lastVal = val
                if 'lock' in key:
                    self.fields[key] = forms.CharField(initial=val, 
                        widget=forms.Textarea(attrs={"rows":1, "cols":size/2, "style": "resize: none"}))
                else: 
                    self.fields[key] = forms.CharField(initial=val,
                        required=False, widget=forms.Textarea(attrs={"rows":(len(val)/size)+1, "cols":size}))
            else:
                lastVal = str(int(lastVal) + 1)
                self.fields['option' + lastKey.replace('numOptions','') + '_' + lastVal] = forms.CharField( 
                    required=False, widget=forms.Textarea(attrs={"rows":1, "cols":size}))
                self.fields['output' + lastKey.replace('numOptions','') + '_' + lastVal] = forms.CharField(
                    required=False, widget=forms.Textarea(attrs={"rows":1, "cols":size}))
                self.fields.pop(lastKey, None)
                self.fields[lastKey] = forms.CharField(initial=lastVal,
                    required=False, widget=forms.Textarea(attrs={"rows":(len(val)/size)+1, "cols":size}))
            
        self.fields['size'] = forms.CharField(initial=str(int(form['size'])+1))

    def removeOption(self, form):
        size = 40
        key_list = list(form.keys())
        val_list = list(form.values())
        key_list.pop(0)
        val_list.pop(0)
        self.fields.clear()
        numOptKey = ''
        optkey = ''
        for key,val in zip(key_list,val_list):
            if 'remove' not in key:
                outkey = optkey
                optkey = numOptKey
                numOptKey = key
                numOptVal = val
                logging.warning(outkey + ' ' + optkey)
                if 'lock' in key:
                    self.fields[key] = forms.CharField(initial=val, 
                        widget=forms.Textarea(attrs={"rows":1, "cols":size/2, "style": "resize: none"}))
                else: 
                    self.fields[key] = forms.CharField(initial=val,
                        required=False, widget=forms.Textarea(attrs={"rows":(len(val)/size)+1, "cols":size}))
            else:
                logging.warning(outkey + ' ' + optkey)
                self.fields.pop(optkey, None)
                self.fields.pop(outkey, None)
                self.fields[numOptKey] = forms.CharField(initial=str(int(numOptVal) - 1),
                    required=False, widget=forms.Textarea(attrs={"rows":(len(val)/size)+1, "cols":size}))
            
        self.fields['size'] = forms.CharField(initial=str(int(form['size'])+1))
            
        
    