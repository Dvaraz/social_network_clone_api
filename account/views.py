from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView


from account.forms import SignupForm, ProfileForm
from account.serializers import UserMeSerializer, FriendshipRequestSerializer
from account.models import User, FriendshipRequest


class UserMe(APIView):

    def get(self, request):
        data = User.objects.filter(id=request.user.id)
        data = UserMeSerializer(data, many=True).data
        return Response(data)


class SingUp(APIView):
    permission_classes = []
    authentication_classes = []
    def post(self, request):
        data = request.data
        message = 'success'

        form = SignupForm({
            'email': data.get('email'),
            'name': data.get('name'),
            'password1': data.get('password1'),
            'password2': data.get('password2'),
        })

        if form.is_valid():
            user = form.save()
            user.is_active = True
            user.save()
        else:
            form.errors.as_json()

        return Response({'message': message})


class Friends(APIView):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        requests = []

        if user == self.request.user:
            requests = FriendshipRequest.objects.filter(created_for=self.request.user, status=FriendshipRequest.SENT)
            requests = FriendshipRequestSerializer(requests, many=True)
            requests = requests.data

        friends = user.friends.all()

        return Response({
            'user': UserMeSerializer(user).data,
            'friends': FriendshipRequestSerializer(friends, many=True).data,
            'requests': requests
        })


class EditProfile(APIView):
    def post(self, request):
        user = request.user
        email = request.data.get('email')

        if User.objects.exclude(id=user.id).filter(email=email).exists():
            return Response({'message': 'email already exists'})
        else:
            form = ProfileForm(request.POST, request.FILES, instance=user)

            if form.is_valid():
                form.save()

            # serializer = UserMeSerializer(user)

            # return Response({'message': 'information updated', 'user': serializer.data})
            return Response({'message': 'information updated'})


class SendFriendshipRequest(APIView):
    def post(self, request, pk):
        user = User.objects.get(pk=pk)

        friendship_request_check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
        friendship_request_check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)

        if not friendship_request_check1 or not friendship_request_check2:
            friendship_request = FriendshipRequest.objects.create(created_for=user, created_by=request.user)

            return Response({'message': 'friendship request created'})
        else:
            return Response({'message': 'request already sent'})


class HandleRequest(APIView):
    def post(self, request, pk, status):
        user = User.objects.get(pk=pk)
        friendship_request = FriendshipRequest.objects.filter(created_for=request.user).get(created_by=user)
        friendship_request.status = status
        friendship_request.save()

        user.friends.add(request.user)
        user.save()

        request_user = request.user
        request_user.friends_count += 1
        request_user.save()

        return Response({'message': 'friendship request updated'})
