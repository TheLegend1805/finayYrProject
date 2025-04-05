from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient('mongodb://localhost:27017/')
db = client['MedicalProjectDB']
patient_collection = db['patients']
patient_medical_info = db['patient_meds']
doctors_collection = db['doctors']
doctors_info_collection = db['doctors_info']
admin_collection = db['admin']
otp_collection = db['otp_verifications']

try:
    client.admin.command('ping')
    print("mongodb connected")
except Exception as e:
    print(e)