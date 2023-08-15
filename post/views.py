from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from post.serializers import PostSerializer
from post.models import Post
from post.forms import PostForm


class PostListView(ListAPIView):
    queryset = Post.objects.all()

    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)


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
