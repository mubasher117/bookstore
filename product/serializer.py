from rest_framework import serializers
from .models import Book, Category, Author
from user.serializer import UserSerializer
from rest_framework.reverse import reverse
from user.models import User

class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    brief = serializers.CharField(style={'base_template': 'textarea.html'})
    number_of_books = serializers.IntegerField(default=0)
    image = serializers.FileField(required=False)

    def create(self, validated_data):
        """
        Create a new author instance.
        """
        author = Author.objects.create(**validated_data)
        # Update number of books for the newly created author
        author.number_of_books = author.author_book.count()
        author.save()
        return author

    def update(self, instance, validated_data):
        """
        Update an existing author instance.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.brief = validated_data.get('brief', instance.brief)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        # Update number of books for the updated author
        instance.number_of_books = instance.author_book.count()
        instance.save()
        return instance

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    detail = serializers.SerializerMethodField('get_links')
    background = serializers.FileField(required=False)

    def get_links(self, obj):
        request = self.context['request']
        return {
            'category detail': reverse('category-detail',
                                       kwargs={'pk': obj.pk}, request=request),
        }

    def create(self, validated_data):
        """
        Create a new category instance.
        """
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update an existing category instance.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.background = validated_data.get('background', instance.background)
        instance.save()
        return instance

class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(style={'base_template': 'textarea.html'})
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='name')
    added_by = serializers.SlugRelatedField(slug_field='email', read_only=True)
    author = serializers.SlugRelatedField(queryset=Author.objects.all(), slug_field='name')
    stock_amount = serializers.IntegerField()
    available = serializers.BooleanField()
    image = serializers.FileField(required=False)
    price = serializers.FloatField()

    def create(self, validated_data):
        """
        Create a new book instance.
        """
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update an existing book instance.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.author = validated_data.get('author', instance.author)
        instance.stock_amount = validated_data.get('stock_amount', instance.stock_amount)
        instance.available = validated_data.get('available', instance.available)
        instance.image = validated_data.get('image', instance.image)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance