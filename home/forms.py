from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'video', 'video_url']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input input-bordered w-full bg-gray-100',
                'placeholder': 'Titre de la publication'
            }),
            'content': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered h-48 w-full bg-gray-100',
                'placeholder': 'Contenu de la publication'
            }),
            'image': forms.FileInput(attrs={
                'class': 'file-input file-input-bordered w-full bg-gray-100'
            }),
            'video': forms.FileInput(attrs={
                'class': 'file-input file-input-bordered w-full bg-gray-100'
            }),
            'video_url': forms.URLInput(attrs={
                'class': 'input input-bordered w-full bg-gray-100',
                'placeholder': 'https://youtube.com/... ou https://vimeo.com/...'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        # Labels personnalisés
        self.fields['video_url'].label = "URL vidéo (YouTube/Vimeo)"
        self.fields['video'].label = "Fichier vidéo"
        
        # Champs média facultatifs
        self.fields['image'].required = False
        self.fields['video'].required = False
        self.fields['video_url'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        video = cleaned_data.get('video')
        video_url = cleaned_data.get('video_url')
        
        # Vérifie qu’on n’a pas à la fois fichier vidéo + URL
        if video and video_url:
            raise forms.ValidationError("Vous ne pouvez pas ajouter à la fois un fichier vidéo et une URL vidéo.")
        
        # Vérifie que l’URL est bien YouTube ou Vimeo
        if video_url:
            if 'youtube.com' not in video_url and 'youtu.be' not in video_url and 'vimeo.com' not in video_url:
                raise forms.ValidationError("Veuillez entrer une URL YouTube ou Vimeo valide.")
        
        return cleaned_data
    

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'content']
        widgets = {
            'author': forms.TextInput(attrs={
                'class': 'input input-bordered w-full bg-gray-100',
                'placeholder': 'Votre nom'
            }),
            'content': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered h-24 w-full bg-gray-100',
                'placeholder': 'Votre commentaire'
            })
        }
