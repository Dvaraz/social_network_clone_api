from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from post.serializers import PostSerializer
from post.models import Post
from post.forms import PostForm
from account.models import User
from account.serializers import UserMeSerializer


class PostListView(ListAPIView):
    queryset = Post.objects.all()

    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)


class PostListProfile(APIView):
    def get(self, request, id):
        user = User.objects.get(pk=id)
        posts = Post.objects.filter(created_by_id=id)

        posts_serializer = PostSerializer(posts, many=True)
        user_serializer = UserMeSerializer(user)

        return Response({
            'posts': posts_serializer.data,
            'user': user_serializer.data
        })


class PostCreate(APIView):
    serializer_class = PostSerializer
    def post(self, request):

        form = PostForm(request.data)

        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.save()
            serializer = PostSerializer(post)
            return Response(serializer.data)
        else:
            return Response({"hey": "done"})
