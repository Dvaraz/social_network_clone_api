from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
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
            user.is_active = False
            user.save()

            url = f'http://127.0.0.1:8000/api/activateemail/?email={user.email}&id={user.id}'
            # # url = f'{settings.WEBSITE_URL}/activateemail/?email={user.email}&id={user.id}'
            #
            send_mail(
                "Please verify your email",
                f"The url for activating your account is: {url}",
                "noreply@wey.com",
                [user.email],
                fail_silently=False,
            )
        else:
            message = form.errors.as_json()

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

            serializer = UserMeSerializer(user)

            return Response({'message': 'information updated', 'user': serializer.data})


class EditPassword(APIView):
    def post(self, request):
        user = request.user

        form = PasswordChangeForm(data=request.POST, user=user)

        if form.is_valid():
            form.save()
            return Response({'message': 'success'})
        else:
            return Response({'message': form.errors.as_json()})


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
        user.friends_count += 1
        user.save()

        request_user = request.user
        request_user.friends_count += 1
        request_user.save()

        return Response({'message': 'friendship request updated'})


class ActivateEmail(APIView):
    permission_classes = []
    authentication_classes = []
    def get(self, request):
        email = request.GET.get('email', '')
        id = request.GET.get('id', '')

        if email and id:
            user = User.objects.get(id=id, email=email)
            user.is_active = True
            user.save()

            return Response('The user is now activated. You can go ahead and log in!')
        else:
            return Response('The parameters is not valid!')
