from rest_framework.response import Response
from rest_framework.views import APIView


from account.forms import SignupForm
from account.serializers import UserMeSerializer
from account.models import User


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
