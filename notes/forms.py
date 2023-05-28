from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from notes.models import*

  
class PostForm(forms.ModelForm):
    pdf = forms.FileField(
        label=_('PDF'),
        help_text=_('PDF file type only.'),
        widget=forms.FileInput(attrs={'accept': 'application/pdf'})
    )
    
    class Meta:
        model = Post
        fields = ('title', 'thumbnail', 'pdf', 'desc')

    def clean_pdf(self):
        pdf = self.cleaned_data['pdf']
        if pdf.content_type != 'application/pdf':
            raise ValidationError(_('Please upload a PDF file.'))
        return pdf

    
    
class SearchForm(forms.Form):
    query = forms.CharField(label='Search')    
    
class SearchForm(forms.Form):
    q = forms.CharField(label='Search', max_length=100)
    
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'slug', 'description', 'price', 'discount', 'active', 'thumbnail', 'resource', 'length']
        widgets = {
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'serial_number', 'video', 'is_preview']
        widgets = {
            'is_preview': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }            
        
        
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['description', 'course']   
        
class PrerequisiteForm(forms.ModelForm):
    class Meta:
        model = Prerequisite
        fields = ['description', 'course'] 
        
class LearningForm(forms.ModelForm):
    class Meta:
        model = Learning
        fields = ['description', 'course']                    

class VideoForm(forms.ModelForm):
    class Meta:
        model = Learning
        fields = '__all__'                    
        
        