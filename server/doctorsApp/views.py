from datetime import datetime
import random
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from db_connections import doctors_collection, otp_collection, doctors_info_collection
import bcrypt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from mailjetMailSender import send_email

def get_tokens_for_doctor(doctor_data):
    refresh = RefreshToken.for_user(doctor_data)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }

@api_view(["POST"])
def register_doctor(request):
    data = request.data
    personal_info = data.get("personal_info", {})
    professional_info = data.get("professional_info", {})
    verification_info = data.get("verification_info", {})
    password = data.get("password")

    email = personal_info.get("email")

    if doctors_collection.find_one({"personal_info.email": email}):
        return Response({"error": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    data["password"] = hashed_password.decode('utf-8')
    data["created_at"] = datetime.utcnow()
    data["verification_info"]["approval_status"] = "pending"

    otp = str(random.randint(100000, 999999))
    otp_collection.update_one(
        {"email": email}, 
        {"$set": {"otp": otp, "doctor_data": data}}, 
        upsert=True
    )

    subject = "Your OTP for Doctor Registration"
    message = f"Your OTP is: {otp}"

    status_code, response = send_email(email, subject, message)
    if status_code == 200:
        return Response({"message": f"OTP sent successfully: {otp} (for testing)"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Failed to send OTP email"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def verify_doctor_otp(request):
    data = request.data
    email = data.get("email")
    user_otp = data.get("otp")

    stored_otp = otp_collection.find_one({"email": email})

    if not stored_otp or stored_otp["otp"] != user_otp:
        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

    doctor_data = stored_otp["doctor_data"]
    doctor_data["created_at"] = datetime.utcnow()

    doctors_collection.insert_one(doctor_data)

    otp_collection.delete_one({"email": email})

    return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_doctor_info(request):
    data = request.data
    doctor = request.user
    email = request.email

    doctor_data = doctors_collection.find_one({"email": email})

    if not doctor_data:
        return Response({"error": "Doctor details not found"}, status=status.HTTP_404_NOT_FOUND)
    
    data["doctor_id"] = str(doctor_data["_id"])
    data["created_at"] = datetime.utcnow()

    doctors_info_collection.insert_one(data)
    return Response({"message": "Medical information added successfully"}, status=status.HTTP_201_CREATED)

@api_view(["POST"])
def doctor_login(request):
    data = request.data
    email = data.get("email")
    password = data.get("password")

    doctor = doctors_collection.find_one({"personal_info.email": email})
    if not doctor:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    if not bcrypt.checkpw(password.encode('utf-8'), doctor["password"].encode('utf-8')):
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    otp = str(random.randint(100000, 999999))
    otp_collection.update_one(
        {"email": email},
        {"$set": {"otp": otp, "doctor_id": str(doctor["_id"])}},
        upsert=True,
    )

    subject = "Your OTP for Doctor Login"
    message = f"Your OTP is: {otp}"

    status_code, response = send_email(email, subject, message)
    
    if status_code == 200:
        return Response({"message": f"OTP sent: {otp} (for testing)"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Failed to send OTP email"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CustomUser:
    def __init__(self, doctor_data):
        self.id = str(doctor_data["_id"])
        self.email = doctor_data["email"]

@api_view(["POST"])
def verify_doctor_login_otp(request):
    data = request.data
    email = data.get("email")
    user_otp = data.get("otp")

    stored_otp = otp_collection.find_one({"email": email})

    if not stored_otp or stored_otp["otp"] != user_otp:
        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
    
    doctor_data = doctors_collection.find_one({"email": email})

    if not doctor_data:
        return Response({"error": "Doctor Not Found"}, status=status.HTTP_404_NOT_FOUND)

    otp_collection.delete_one({"email": email})
    custom_doctor = CustomUser(doctor_data)
    tokens = get_tokens_for_doctor(custom_doctor)

    return Response({"message": "Login successful", "tokens": tokens}, status=status.HTTP_200_OK)
