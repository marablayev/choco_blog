from django.db.models import Avg
from django.utils import timezone

from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import permission_classes as perm_decorator
from rest_framework.pagination import PageNumberPagination

from account.models import Author
from .models import Post, Comment, Category, Rate
from .serializers import PostSerializer, CategorySerializer, CommentSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 7
    page_size_query_param = 'page_size'
    max_page_size = 1000


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny, )
    pagination_class = StandardResultsSetPagination
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        category = request.query_params.get('category')
        qfilter = request.query_params.get('filter')

        self.queryset = self.queryset.filter(status=1).order_by('-publish_date')

        if category:
            self.queryset = self.queryset.filter(category__slug=category)

        if qfilter == 'featured':
            self.queryset = self.queryset.annotate(rate=Avg('rates__rate'))\
                                            .filter(rate__gt=4)

        return super(PostViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, slug=None, *args, **kwargs):
        author = Author.objects.get(username=request.user.username)
        obj = self.get_object()
        already_rate = obj.rates.filter(author=author).exists()
        rate = None
        if already_rate:
            rate = obj.rates.filter(author=author).first().rate

        serializer = self.serializer_class(obj)
        return Response({'post': serializer.data, 'rate': rate,\
                         'already_rate': already_rate})

    def create(self, request):
        data = request.data

        author = Author.objects.get(username=request.user.username)
        category = Category.objects.get(slug=data['category'])
        data['author'] = author
        data['category'] = category
        data['publish_date'] = timezone.now()
        data['status'] = 1

        post = Post.objects.create(**data)
        serializer = self.serializer_class(post)

        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny, )
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        return super(CategoryViewSet, self).list(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny, )
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, *args, **kwargs):
        slug = request.query_params.get('slug')
        self.queryset = self.queryset.filter(post__slug=slug).order_by('-publish_date')
        return super(CommentViewSet, self).list(request, *args, **kwargs)

    @perm_decorator((permissions.IsAuthenticated,))
    def create(self, request):
        slug = request.data.get('slug')
        text = request.data.get('text', '')
        author = Author.objects.get(username=request.user.username)

        try:
            post = Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=400)

        Comment.objects.create(post=post, author=author, text=text, \
                               publish_date=timezone.now())
        self.queryset = self.queryset.filter(post=post).order_by('-publish_date')
        serializer = self.serializer_class(self.queryset, many=True)

        return Response(serializer.data)


class RateViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Rate.objects.all()

    @perm_decorator((permissions.IsAuthenticated,))
    def create(self, request):
        slug = request.data.get('slug')
        rate = request.data.get('rate', 5)
        author = Author.objects.get(username=request.user.username)

        try:
            post = Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=400)

        Rate.objects.create(post=post, author=author, rate=rate)

        return Response({'rating': post.rating})
