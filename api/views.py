from django.http import HttpResponse
from django.views import View
from django.http.multipartparser import MultiPartParser

from . import models

import json
import datetime

# Create your views here.
class PuskesmasView(View):
    def get(self, request):
        puskesmas = models.Puskesmas.objects.all().values("id", "name", "address")
        puskesmas = list(puskesmas)
        for index in range(len(puskesmas)):
            puskesmas[index]["id"] = str(puskesmas[index]["id"].hex)
        
        # NOT IMPLEMENTED YET : Get puskesmas data from ML prediction

        data = puskesmas
        return HttpResponse(json.dumps(data))

    def post(self, request):
        puskesmas = models.Puskesmas()
        puskesmas.name = request.POST.get('name')
        puskesmas.address = request.POST.get('address')
        puskesmas.save()

        data = {
            "status": "success",
            "message": "Berhasil menambahkan data puskesmas"
        }
        return HttpResponse(json.dumps(data))
    
class PuskesmasDetailView(View):
    def get(self, request, id_puskesmas):
        puskesmas = models.Puskesmas.objects.get(id=id_puskesmas)
        data = {
            "id": puskesmas.id.hex,
            "name": puskesmas.name,
            "address": puskesmas.address
        }
        
        # NOT IMPLEMENTED YET : Use exception
        # except ValidationError
        # except DoesNotExist
    
        return HttpResponse(json.dumps(data))

    def put(self, request, id_puskesmas):
        req = MultiPartParser(request.META, request, request.upload_handlers).parse()[0]
        puskesmas = models.Puskesmas.objects.get(id=id_puskesmas)
        puskesmas.name = req.get("name")
        puskesmas.address = req.get("address")
        puskesmas.save()

        data = {
            "status": "success",
            "message": "Berhasil memperbarui data puskesmas"
        }
        return HttpResponse(json.dumps(data))

    def delete(self, request, id_puskesmas):
        puskesmas = models.Puskesmas(id=id_puskesmas)
        puskesmas.delete()

        data = {
            "status": "success",
            "message": "Berhasil menghapus data puskesmas"
        }

        return HttpResponse(json.dumps(data))

class UserView(View):
    def get(self, request):
        user = models.User.objects.all().values("id", "name", "identity_number")
        user = list(user)

        for index in range(len(user)):
            user[index]["id"] = str(user[index]["id"].hex)

        data = list(user)
        return HttpResponse(json.dumps(data))
    
    def post(self, request):
        user = models.User()

        # get puskesmas object
        id_puskesmas = request.POST.get("id_puskesmas")
        puskesmas = models.Puskesmas.objects.get(pk=id_puskesmas)
        user.puskesmas = puskesmas

        user.name = request.POST.get("name")
        user.address = request.POST.get("address")
        user.phone_number = request.POST.get("phone_number")
        user.bpjs_number = request.POST.get("bpjs_number")
        user.identity_number = request.POST.get("identity_number")
        user.sex = request.POST.get("sex")
        user.age = request.POST.get("age")
        user.save()

        data = {
            "status": "success",
            "message": "Berhasil menambahkan data puskesmas"
        }

        return HttpResponse(json.dumps(data))

class UserDetailView(View):
    def get(self, request, id_user):
        user = models.User.objects.get(pk=id_user)
        
        data = {
            "status": "success",
            "data": {
                "id": user.id.hex,
                "name": user.name,
                "address": user.address,
                "phone_number": user.phone_number,
                "bpjs_number": user.bpjs_number,
                "identity_number": user.identity_number,
                "sex": user.sex,
                "age": user.age,
                "puskesmas": {
                    "name": user.puskesmas.name,
                    "id": user.puskesmas.id.hex
                }
            }
        }

        return HttpResponse(json.dumps(data))

    def put(self, request, id_user):
        req = MultiPartParser(request.META, request, request.upload_handlers).parse()[0]
        
        user = models.User.objects.get(pk=id_user)
        id_puskesmas = req.get("id_puskesmas")
        puskesmas = models.Puskesmas.objects.get(id=id_puskesmas)
        user.puskesmas = puskesmas
        
        user.name = req.get("name")
        user.address = req.get("address")
        user.phone_number = req.get("phone_number")
        user.bpjs_number = req.get("bpjs_number")
        user.identity_number = req.get("identity_number")
        user.sex = req.get("sex")
        user.age = req.get("age")
        user.save()

        data = {
            "status": "success",
            "message": "Berhasil memperbarui data pengguna"
        }
        return HttpResponse(json.dumps(data))
    
    def delete(self, request, id_user):
        user = models.User(pk=id_user)
        user.delete()

        data = {
            "status": "success",
            "message": "Berhasil menghapus data pengguna"
        }

        return HttpResponse(json.dumps(data))

class HospitalView(View):
    def get(self, request):
        hospital = models.Hospital.objects.all().values("id", "name", "address", "latitude", "longitude")
        hospital = list(hospital)

        for index in range(len(hospital)):
            hospital[index]["id"] = str(hospital[index]["id"].hex)

        data = list(hospital)
        return HttpResponse(json.dumps(data))
    
    def post(self, request):
        hospital = models.Hospital()

        # get puskesmas object
        hospital.name = request.POST.get("name")
        hospital.address = request.POST.get("address")
        hospital.latitude = request.POST.get("latitude")
        hospital.longitude = request.POST.get("longitude")
        hospital.save()

        data = {
            "status": "success",
            "message": "Berhasil menambahkan data rumah sakit"
        }

        return HttpResponse(json.dumps(data))

class HospitalDetailView(View):
    def get(self, request, id_hospital):

        try:
            hospital = models.Hospital.objects.get(pk=id_hospital)
        except:
            data = {}
            return HttpResponse(json.dumps(data))

        data = {
            "status": "success",
            "data": {
                "id": hospital.id.hex,
                "name": hospital.name,
                "address": hospital.address,
                "latitude": hospital.latitude,
                "longitude": hospital.longitude
            }
        }

        return HttpResponse(json.dumps(data))
    
    def put(self, request, id_hospital):
        req = MultiPartParser(request.META, request, request.upload_handlers).parse()[0]
        
        hospital = models.Hospital.objects.get(pk=id_hospital)
        hospital.name = req.get("name")
        hospital.address = req.get("address")
        hospital.latitude = req.get("latitude")
        hospital.longitude = req.get("longitude")
        hospital.save()

        data = {
            "status": "success",
            "message": "Berhasil menambahkan data puskesmas"
        }

        return HttpResponse(json.dumps(data))

    def delete(self, request, id_hospital):
        try:
            hospital = models.Hospital.objects.get(pk=id_hospital)
            hospital.delete()
        except:
            data = {}
            return HttpResponse(json.dumps(data))

        data = {
            "status": "success",
            "message": "Berhasil menghapus data rumah sakit"
        }

        return HttpResponse(json.dumps(data))

class TreatmentView(View):
    def get(self, request):
        treatment = models.Treatment.objects.all().values("id", "doctor_name", "jenis_pengobatan", "start_time", "end_time", "hospital_id", "user_id")
        treatment = list(treatment)

        for index in range(len(treatment)):
            treatment[index]["id"] = str(treatment[index]["id"].hex)

        data = list(treatment)
        return HttpResponse(json.dumps(data))

    def post(self, request):
        treatment = models.Treatment()

        # get puskesmas object
        treatment.name = request.POST.get("name")
        treatment.doctor_name = request.POST.get("doctor_name")
        treatment.jenis_pengobatan = request.POST.get("jenis_pengobatan")
        treatment.start_time = datetime.datetime.now()
        treatment.end_time = ""
        treatment.hospital_id = request.POST.get("hospital_id")
        treatment.user_id = request.POST.get("user_id")
        treatment.save()

        data = {
            "status": "success",
            "message": "Berhasil menambahkan data puskesmas"
        }

        return HttpResponse(json.dumps(data))


# class TreatmentDetailView(View):
#     def get(self, request):
#     def put(self, request):
#     def delete(self, request):

# class covidView(View):
#     def get(self, request):
#     def post(self, request):

# class CovidDetailView(View):
#     def get(self, request):
#     def put(self, request):
#     def delete(self, request):