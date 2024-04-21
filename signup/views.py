from rest_framework.response import Response
from rest_framework.decorators import APIView
from login.models import CustomUser
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import datetime
import re


class Signup(APIView):
    def post(self, request):
        """
        Creates a new user with the data provided:

        1- Takes a list of arguments:

        - first_name: Your First Name
        - last_name: Your Last Name
        - username: For Account Login
        - email: Valid Email
        - password: Hashed password for Account Login

        """
        # Get request data

        data = request.data

        # Check if the username doesn't exist in the database
        try:
            check_username = CustomUser.objects.get(username=data["username"])
            if check_username:
                return Response({"message": "Username not available pick another one"}, status=HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            # Check if the email doesn't exist in the database
            try:
                check_email = CustomUser.objects.get(email=data["email"])
                if check_email:
                    return Response({"message": "This email belongs to another account"}, status=HTTP_400_BAD_REQUEST)
            except CustomUser.DoesNotExist:
                # Check if the date is a valid format
                try:
                    datetime.date.fromisoformat(data["birthday"])
                except:
                    return Response({"message": "Birthday is required for legal issues"}, status=HTTP_400_BAD_REQUEST)
                # Check if the email is valid
                if len(data["email"]) < 3 or "@" not in data["email"]:
                    return Response({"message": "A valid email is required to activate your account after registration"}, status=HTTP_400_BAD_REQUEST)
                # Check strong password
                password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
                is_valid = re.match(password_pattern, data["password"])
                if is_valid == None:
                    return Response({"message": """A strong password should have:,
                                                  ,At least 8 characters in length.
                                                  ,At least one uppercase English letter.
                                                  ,At least one lowercase English letter.
                                                  ,At least one digit.
                                                  ,At least one special character."""}, status=HTTP_400_BAD_REQUEST)
                # Create user ( Abstract User Creation )
                user = CustomUser.objects.create(
                    first_name=data["firstname"],
                    last_name=data["lastname"],
                    username=data["username"],
                    email=data["email"],
                    password=data["password"],
                    birthday=data["birthday"],
                    is_active=1
                )

                user.set_password(data["password"])
                user.save()

                response_body = {

                    "user_id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "username": user.username,
                    "email": user.email,
                    "message": "Register Successfully"
                }

                return Response(response_body, status=HTTP_200_OK)
