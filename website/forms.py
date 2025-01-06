from .models import Thesis, TempURL
from django import forms
from django.utils.safestring import mark_safe

class ThesisForm(forms.ModelForm):
    class Meta:
        model = Thesis
        fields = ['published_date', 'title', 'authors', 'poster', 'pdf_file', 'tags']
        widgets = {
            'published_date': forms.DateInput(attrs={'type': 'date'}),
            'poster': forms.HiddenInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super(ThesisForm, self).__init__(*args, **kwargs)
        self.fields['published_date'].widget.attrs['class'] = 'form-control'
        self.fields['published_date'].widget.attrs['placeholder'] = 'Published Date'
        self.fields['published_date'].label = 'Published Date:'

        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['title'].widget.attrs['placeholder'] = 'Title'
        self.fields['title'].widget.attrs['rows'] = '3'
        self.fields['title'].widget.attrs['style'] = 'resize:none'
        self.fields['title'].label = 'Title:'

        self.fields['authors'].widget.attrs['class'] = 'form-control'
        self.fields['authors'].widget.attrs['placeholder'] = 'Last Name, First Name - author #1\nLast Name, First Name - author #2\nLast Name, First Name - author #3\n...'
        self.fields['authors'].widget.attrs['rows'] = '7'
        self.fields['authors'].widget.attrs['style'] = 'resize:none'
        self.fields['authors'].label = 'Author(s):'
        self.fields['authors'].help_text = mark_safe('''<span class="form-text text-muted"><small>Separate each author with a new line (Enter key).</small></span><br>
                                            <span class="form-text text-muted"><small>Enter the Last Name followed by a comma \',\' then the First Name and Middle Initial</small></span>''')

        self.fields['poster'].widget.attrs['class'] = 'form-control'
        self.fields['poster'].widget.attrs['placeholder'] = 'poster'
        self.fields['poster'].widget.attrs['id'] = 'poster'
        #self.fields['poster'].widget.attrs['readonly'] = 'readonly'
        self.fields['poster'].label = 'poster:'
        
        self.fields['pdf_file'].widget.attrs['class'] = 'form-control'
        self.fields['pdf_file'].widget.attrs['placeholder'] = 'PDF'
        self.fields['pdf_file'].label = 'Thesis PDF File:'
        
        self.fields['tags'].widget.attrs['class'] = 'form-control'
        self.fields['tags'].widget.attrs['placeholder'] = 'tag 1, tag 2, tag 3, ...'
        self.fields['tags'].label = 'Tag(s):'
        self.fields['tags'].help_text = mark_safe('<span class="form-text text-muted"><small>Separate each tag with a comma \",\"</small></span>')

class ThesisRejectReasonForm(forms.ModelForm):
    class Meta:
        model = Thesis
        fields = ['rejection_reason']

    reject_choices = Thesis.reject_choices

    rejection_reason = forms.ChoiceField(choices=reject_choices, widget=forms.Select,)

    def __init__(self, *args, **kwargs):
        super(ThesisRejectReasonForm, self).__init__(*args, **kwargs)
        self.fields['rejection_reason'].widget.attrs['class'] = 'form-control'
        self.fields['rejection_reason'].widget.attrs['placeholder'] = 'Rejection Reason'
        self.fields['rejection_reason'].label = 'Rejection Reason:'
        

class RequestForm(forms.ModelForm):
    class Meta:
        model = TempURL
        fields = ['email', 'first_name', 'last_name', 'id_pic']
    
    id_pic = forms.ImageField(required=True)
        
    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['email'].label = 'Email:'

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['first_name'].label = 'First Name:'
        
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['last_name'].label = 'Last Name:'

        self.fields['id_pic'].widget.attrs['class'] = 'form-control'
        self.fields['id_pic'].widget.attrs['placeholder'] = 'ID'
        self.fields['id_pic'].label = 'ID Picture:'
        self.fields['id_pic'].help_text = '<span class="form-text text-muted"><small>Upload a picture of your ID.</small></span>'

class RequestRejectReasonForm(forms.ModelForm):
    class Meta:
        model = Thesis
        fields = ['rejection_reason']

    reject_choices = TempURL.url_reject_choices

    rejection_reason = forms.ChoiceField(choices=reject_choices, widget=forms.Select,)

    def __init__(self, *args, **kwargs):
        super(RequestRejectReasonForm, self).__init__(*args, **kwargs)
        self.fields['rejection_reason'].widget.attrs['class'] = 'form-control'
        self.fields['rejection_reason'].widget.attrs['placeholder'] = 'Rejection Reason'
        self.fields['rejection_reason'].label = 'Rejection Reason:'