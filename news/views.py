from rest_framework import generics, permissions, filters, viewsets
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination

from .permissions import IsAuthorOrIsAuthenticated, IsStaff
from .serializers import NewsSerializer, CommentSerializer, \
    StatusSerializer, CommentStatusSerializer, NewsStatusSerializer
from .models import News, Comment, Status, NewsStatus, CommentStatus


class NewsListCreateAPIView(generics.ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    pagination_class = LimitOffsetPagination
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]
    search_fields = ['title', 'author__user__username__exact']
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['created_at', ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author)


class NewsRetrieveDestroyUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthorOrIsAuthenticated, ]


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthorOrIsAuthenticated, ]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return super().get_queryset().filter(news_id=self.kwargs['news_id'])


class CommentRetrieveDestroyUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthorOrIsAuthenticated, ]

    def get_queryset(self):
        return super().get_queryset().filter(news_id=self.kwargs['news_id'])


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsStaff, ]


class NewsStatusCreateAPIView(generics.CreateAPIView):
    queryset = NewsStatus.objects.all()
    serializer_class = NewsStatusSerializer
    permission_classes = [IsAuthorOrIsAuthenticated, ]

    def perform_create(self, serializer):
        news_id = self.kwargs['news_id']
        news = News.objects.get(id=news_id)
        serializer.save(
            author_id=self.request.user.author.id,
            news=news
        )


class CommentStatusCreateAPIView(generics.CreateAPIView):
    queryset = CommentStatus.objects.all()
    serializer_class = CommentStatusSerializer
    permission_classes = [IsAuthorOrIsAuthenticated, ]

    def perform_create(self, serializer):
        comm_id = self.kwargs['pk']
        comment = Comment.objects.get(id=comm_id)
        serializer.save(
            author_id=self.request.user.author.id,
            comment=comment
        )
