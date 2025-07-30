from django.db import models

class Author(models.Model):
      name = models.CharField(max_length=20)
      
      def __str__(self):
            return self.name


class Books(models.Model):
      title = models.CharField(max_length=100)
      author = models.ForeignKey(Author,on_delete=models.CASCADE, related_name='books')
      published_at = models.DateTimeField(auto_now_add=True)
      
      def __str__(self):
            return self.title