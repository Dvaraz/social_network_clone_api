from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from post.serializers import PostSerializer, PostDetailSerializer, CommentSerializer, TrendSerializer
from post.models import Post, Like, Comment, Trend
from post.forms import PostForm, AttachmentForm
from account.models import User
from account.serializers import UserMeSerializer


class PostListView(ListAPIView):

    def get_queryset(self):
        user_ids = [self.request.user.id]

        for user in self.request.user.friends.all():
            user_ids.append(user.id)
        posts = Post.objects.filter(created_by_id__in=list(user_ids))
        return posts

    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)


class PostDetail(APIView):
    def get(self, request, id):
        post = Post.objects.get(pk=id)

        return Response({
            'post': PostDetailSerializer(post).data
        })


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
    # serializer_class = PostSerializer
    def post(self, request):
        form = PostForm(request.POST)
        attachment = None
        attachment_form = AttachmentForm(request.POST, request.FILES)

        if attachment_form.is_valid():
            attachment = attachment_form.save(commit=False)
            attachment.created_by = request.user
            attachment.save()

        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.save()

            if attachment:
                post.attachments.add(attachment)

            user = request.user
            user.posts_count += 1
            user.save()

            serializer = PostSerializer(post)
            return Response(serializer.data)
        else:
            return Response({"hey": "done"})


class PostLike(APIView):
    def post(self, request, id):
        post = Post.objects.get(pk=id)

        if not post.likes.filter(created_by=request.user):
            like = Like.objects.create(created_by=request.user)

            post.likes_count += 1
            post.likes.add(like)
            post.save()
            return Response({'message': 'like created'})
        else:
            return Response({'message': 'post already liked'})


class PostCreateComment(APIView):
    def post(self, request, id):
        comment = Comment.objects.create(body=request.data.get('body'), created_by=request.user)

        post = Post.objects.get(pk=id)
        post.comments.add(comment)
        post.comments_count += 1
        post.save()

        serializer = CommentSerializer(comment)

        return Response(serializer.data)


class Trends(APIView):
    def get(self, request):
        trends = Trend.objects.all()
        serializer = TrendSerializer(trends, many=True)

        return Response(serializer.data)
