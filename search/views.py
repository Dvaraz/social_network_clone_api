from collections import OrderedDict

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters import FilterSet, CharFilter
from post.serializers import PostSerializer
from post.models import Post


class SearchView(ListAPIView):
    class PostPaginator(LimitOffsetPagination):
        def get_paginated_response(self, data):
            return Response(OrderedDict([
                ('count', self.count),
                ('posts', data)
            ]))

    class PostFilter(FilterSet):

        createdBy = CharFilter(field_name="created_by__name", lookup_expr="icontains")
        body = CharFilter(field_name="body", lookup_expr="icontains")
        class Meta:
            model = Post
            fields = ["body", "createdBy"]

    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    pagination_class = PostPaginator
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter

# class Search(APIView):
#     def post(self, request):
#         data = request.data
#
#         query = data['query']
#         print(query)
#         user_ids = [request.user.id]
#
#         # for user in request.user.friends.all():
#         #     user_ids.append(user.id)
#
#         users = User.objects.filter(name__icontains=query)
#         users_serializer = UserMeSerializer(users, many=True)
#
#         posts = Post.objects.filter(
#             Q(body__icontains=query) |
#             Q(created_by__name__icontains=query, body__icontains=query)
#             )
#         posts_serializer = PostSerializer(posts, many=True)
#
#         return Response({
#                     'users': users_serializer.data,
#                     'posts': posts_serializer.data
#                 }
#             )