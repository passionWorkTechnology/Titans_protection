import re
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    pass


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    video = models.FileField(upload_to='posts/videos/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True, help_text="URL d'une vidéo YouTube ou Vimeo")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def has_media(self):
        return self.image or self.video or self.video_url
    
    def is_video_url(self):
        return self.video_url and any(domain in self.video_url for domain in ['youtube', 'youtu.be', 'vimeo'])

    def get_youtube_id(self):
        """
        Extrait l'ID d'une vidéo YouTube depuis son URL
        """
        if not self.video_url:
            return None
            
        # Patterns pour les URLs YouTube
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'(?:embed\/)([0-9A-Za-z_-]{11})',
            r'(?:youtu.be\/)([0-9A-Za-z_-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.video_url)
            if match:
                return match.group(1)
                
        return None
    
    def get_vimeo_id(self):
        """
        Extrait l'ID d'une vidéo Vimeo depuis son URL
        """
        if not self.video_url:
            return None
            
        pattern = r'(?:vimeo.com\/)([0-9]+)'
        match = re.search(pattern, self.video_url)
        
        if match:
            return match.group(1)
            
        return None


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"