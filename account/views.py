from rest_framework.response import Response
from rest_framework.views import APIView


from account.forms import SignupForm

class SingUp(APIView):
    permission_classes = []
    authentication_classes = []
    def post(self, request):
        data = request.data
        message = 'success'
        print(data)

        form = SignupForm({
            'email': data.get('email'),
            'name': data.get('name'),
            'password1': data.get('password1'),
            'password2': data.get('password2'),
        })

        print(form)
        if form.is_valid():
            user = form.save()
            user.is_active = True
            user.save()
        else:
            form.errors.as_json()

        print(message)

        return Response({'message': message})
