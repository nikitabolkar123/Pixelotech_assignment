from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# from user.jwt_util import JWT
from logconfig.logger import get_logger
from user.models import User
from user.serializers import RegistrationSerializer, LoginSerializer

logger = get_logger()


# Create your views here.
class UserRegistration(APIView):
    serializer_class = RegistrationSerializer
    """
        class used to register for the user
    """

    def post(self, request):
        """
            this method is used to create the user for the registration
        """
        try:
            serializer = RegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)  # if valid then deserialization
            serializer.save()
            return Response({"message": "User Registration Successfully", "status": 201, "data": serializer.data},
                            status=201)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400, "data": {}}, status=400)

    def get(self, request,user_id):
        """
            this method is used to retrieve the all registered users data
        """
        try:
            user = User.objects.get(id=user_id)
            serializer = RegistrationSerializer(user)
            return Response({"message": "Retrieve Data  Successfully", "status": 200, "data": serializer.data},
                            status=200)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400, "data": {}}, status=400)


    def put(self, request, user_id):
        """
                   this method is used to update user data
               """
        try:
            user = User.objects.get(id=user_id)
            serializer = RegistrationSerializer(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Updated Successfully", "status": 200, "data": serializer.data},
                            status=200)
        except Exception as e:
            return Response({"message": str(e), "status": 400, "data": {}}, status=400)


    def delete(self, request, user_id):
        """
                   this method is used to delete user
               """
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response({"message": " deleted Successfully", "status": 200, "data": {}},
                            status=200)
        except Exception as e:
            return Response({"message": str(e), "status": 400, "data": {}}, status=400)



class UserLogin(APIView):
    serializer_class = LoginSerializer
    """
       class is used for the user login
    """

    def post(self, request):
        """
            using the post method user can login by giving the credentials
        """
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            login(request, serializer.context.get('user'))
            return Response({"message": "Login Successful", "status": 201, "data": {}}, status=201)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400, "data": {}}, status=400)


class Logout(APIView):
    def get(self, request):
        try:
            if request.user.is_authenticated:
                logout(request)
                return Response({"Message": "Logout Successfully"})
            else:
                return Response({"Message": "you are not log in"})
        except Exception as e:
            logger.exception(e)
        return Response({"Message": "An error occurred during logout:{}".format(str(e))})
