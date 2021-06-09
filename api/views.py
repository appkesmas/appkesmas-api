from django.http import HttpResponse
from django.views import View
from django.http.multipartparser import MultiPartParser

from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import accuracy_score

from . import models

import json
import datetime
import pickle
import uuid
import pandas as pd
import requests
from geopy.distance import geodesic

# Create your views here.
class PuskesmasView(View):
    def get(self, request):
        puskesmas = models.Puskesmas.objects.all().values("id", "name", "address")
        puskesmas = list(puskesmas)
        for index in range(len(puskesmas)):
            puskesmas[index]["id"] = str(puskesmas[index]["id"].hex)
        
        # NOT IMPLEMENTED YET : Get puskesmas data from ML prediction

        data = puskesmas
        return HttpResponse(json.dumps(data), content_type="application/json")

    def post(self, request):
        puskesmas = models.Puskesmas()
        puskesmas.name = request.POST.get('name')
        puskesmas.address = request.POST.get('address')
        puskesmas.save()

        data = {
            "status": "success",
            "message": "Berhasil menambahkan data puskesmas"
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    
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
    
        return HttpResponse(json.dumps(data), content_type="application/json")

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
        return HttpResponse(json.dumps(data), content_type="application/json")

    def delete(self, request, id_puskesmas):
        puskesmas = models.Puskesmas(id=id_puskesmas)
        puskesmas.delete()

        data = {
            "status": "success",
            "message": "Berhasil menghapus data puskesmas"
        }

        return HttpResponse(json.dumps(data), content_type="application/json")

class UserView(View):
    def get(self, request):
        user = models.User.objects.all().values("id", "name", "medical_id", "identity_number")
        user = list(user)

        for index in range(len(user)):
            user[index]["id"] = str(user[index]["id"].hex)

        data = list(user)
        return HttpResponse(json.dumps(data), content_type="application/json")
    
    def post(self, request):
        user = models.User()

        # UNUSED
        # get puskesmas object
        # id_puskesmas = request.POST.get("id_puskesmas")
        # puskesmas = models.Puskesmas.objects.get(pk=id_puskesmas)
        # user.puskesmas = puskesmas

        user_id = uuid.uuid4()
        user.id = user_id
        user.medical_id = "MID-" + str(int(str(user_id).split("-")[0], 16))

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
            "message": "Berhasil menambahkan data user",
            "user": {
                "id": user.id.hex,
                "medical_id": user.medical_id,
                "name": user.name,
                "address": user.address,
                "sex": user.sex,
                "age": user.age,
                "phone_number": user.phone_number,
                "identity_number": user.identity_number,
                }
        }

        return HttpResponse(json.dumps(data), content_type="application/json")

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
                "medical_id": user.medical_id,
                "sex": user.sex,
                "age": user.age
            }
        }

        return HttpResponse(json.dumps(data), content_type="application/json")

    def put(self, request, id_user):
        req = MultiPartParser(request.META, request, request.upload_handlers).parse()[0]
        
        user = models.User.objects.get(pk=id_user)
        # UNUSED Puskesmas
        # id_puskesmas = req.get("id_puskesmas")
        # puskesmas = models.Puskesmas.objects.get(id=id_puskesmas)
        # user.puskesmas = puskesmas
        
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
        return HttpResponse(json.dumps(data), content_type="application/json")
    
    def delete(self, request, id_user):
        user = models.User(pk=id_user)
        user.delete()

        data = {
            "status": "success",
            "message": "Berhasil menghapus data pengguna"
        }

        return HttpResponse(json.dumps(data), content_type="application/json")

class HospitalView(View):
    def get_availabilility_columns(self, df):
        return [col for col in df.columns if 'Ketersediaan' in col]


    def get(self, request):
        user = {
            "latitude": str(request.GET.get("latitude")),
            "longitude": str(request.GET.get("longitude"))
        }

        RS_type = {
            "0": "RSU",
            "1": "RSIA",
            "2": "RSK GM",
            "3": "RSK BEDAH",
            "4": "RSK Mata",
            "5": "RSK Jiwa",
            "6": "RSK JANTUNG",
            "7": "RSK KANKER",
            "8": "RSK THT-KL",
            "9": "RSK OTAK",
            "10": "RSK INFEKSI",
            "11": "RSKO"
        }

        response = requests.get('http://eis.dinkes.jakarta.go.id/eis/home/ajax_list_data_bed', headers={'accept': 'application/json'})
        
        j = json.loads(response.text[response.text.index("{"):response.text.index("}")+1])
        bor_header = ['No', 'Wilayah', 'Nama RS', 'Ketersediaan ICU Tekanan Negatif Dengan Ventilator',
                    'Ketersediaan ICU Tekanan Negatif Tanpa Ventilator', 'Ketersediaan ICU Tanpa Tekanan Negatif dengan Ventilator',
                    'Ketersediaan ICU Tanpa Tekanan Negatif tanpa Ventilator', 'Ketersediaan Isolasi Tekanan Negatif',
                    'Ketersediaan Isolasi Tanpa Tekanan Negatif', 'Ketersediaan NICU khusus COVID-19', 'Ketersediaan Perina khusus COVID-19',
                    'Ketersediaan PICU khusus COVID-19', 'Ketersediaan OK khusus COVID-19', 'Ketersediaan HD khusus COVID-19',
                    'Update Terakhir', 'Hotline SPGDT']

        curl_df = pd.DataFrame.from_dict(j['data'])
        curl_df.columns = bor_header

        curl_df[self.get_availabilility_columns(curl_df)] = curl_df[self.get_availabilility_columns(curl_df)].apply(pd.to_numeric)

        rs_clean_df = pd.read_csv('../appkesmasML/hospital_ranking/rs_dki_cleaned.csv', dtype={"Latitude": str, "Longitude": str})
        curl_df['Nama RS'] = curl_df['Nama RS'].apply(lambda x: 'RS Darurat Covid Wisma Atlet' if 'RSDC' in x else x)
        curl_df['Nama RS'] = curl_df['Nama RS'].apply(lambda x: 'RS Ibu dan Anak Avisena' if 'Avisena' in x else x)

        combined_df = pd.merge(curl_df,rs_clean_df,on='Nama RS')

        hospital_id_as_index = False
        if hospital_id_as_index:
                combined_df = combined_df.set_index('Hospital ID')

        def calc_distance(row, site_coords):
            station_coords = (row['Latitude'], row['Longitude'])
            dist = geodesic(site_coords, station_coords).km
            return(dist)

        rs_type = RS_type[str(request.GET.get("rs_type"))]
        combined_df = combined_df[combined_df["Jenis RS"] == rs_type]

        combined_df['Jarak'] = combined_df.apply(calc_distance, site_coords=(user["latitude"], user["longitude"]), axis=1)
        combined_df['Jarak_Weighted'] = combined_df['Jarak'].copy()

        availability_cols = self.get_availabilility_columns(combined_df)
        combined_df['Total Ketersediaan'] = combined_df[availability_cols].sum(axis=1)
        combined_df['Ketersediaan_Weighted'] = combined_df['Total Ketersediaan'].copy()

        combined_df.loc[combined_df.query("Kelas == 'A'").index, 'Kelas_Weighted'] = 5
        combined_df.loc[combined_df.query("Kelas == 'B'").index, 'Kelas_Weighted'] = 4
        combined_df.loc[combined_df.query("Kelas == 'C'").index, 'Kelas_Weighted'] = 3
        combined_df.loc[combined_df.query("Kelas == 'D'").index, 'Kelas_Weighted'] = 2
        combined_df.loc[combined_df.query("Kelas == 'Belum Ditetapkan'").index, 'Kelas_Weighted'] = 1

        cols = ['Ketersediaan_Weighted','Kelas_Weighted','Jarak_Weighted']
        for col in cols:
              combined_df[col] = (combined_df[col]-combined_df[col].min())/(combined_df[col].max()-combined_df[col].min())

        combined_df['Jarak_Weighted'] = 1 - combined_df['Jarak_Weighted']
        combined_df.loc[combined_df.query("Ketersediaan_Weighted == 0").index, 'Ketersediaan_Weighted'] = -1

        combined_df['Rank'] = (combined_df['Jarak_Weighted']*0.45 + combined_df['Kelas_Weighted']*0.1 + combined_df['Ketersediaan_Weighted']*0.45).rank(ascending=False).astype('int')

        combined_df = combined_df.sort_values("Rank")


        final_features = ['Kode RS', 'Nama RS', 'Wilayah',
                       'Total Ketersediaan', 'Ketersediaan ICU Tekanan Negatif Dengan Ventilator',
                       'Ketersediaan ICU Tekanan Negatif Tanpa Ventilator',
                       'Ketersediaan ICU Tanpa Tekanan Negatif dengan Ventilator',
                       'Ketersediaan ICU Tanpa Tekanan Negatif tanpa Ventilator',
                       'Ketersediaan Isolasi Tekanan Negatif',
                       'Ketersediaan Isolasi Tanpa Tekanan Negatif',
                       'Ketersediaan NICU khusus COVID-19',
                       'Ketersediaan Perina khusus COVID-19',
                       'Ketersediaan PICU khusus COVID-19', 'Ketersediaan OK khusus COVID-19',
                       'Ketersediaan HD khusus COVID-19', 'Hotline SPGDT',
                       'Jenis RS', 'Kelas', 'Jarak', 'Image URL', 'Rank']

        count = int(request.GET.get("count"))
        if hospital_id_as_index:
            final_data = combined_df[final_features][:count]
        else:
            final_data = combined_df[['Hospital ID']+final_features][:count]

        if hospital_id_as_index:
            result = final_data.to_json(orient='index')
        else:
            result = final_data.to_json(orient='records')

        final_data_json = json.loads(result)
    
        return HttpResponse(json.dumps(final_data_json), content_type="application/json")


    #def get(self, request):
    #    hospital = models.Hospital.objects.all().values("id", "name", "address", "latitude", "longitude", "area", "category", "class_type", "bed_availability", "image_name")
    #    hospital = list(hospital)

    #    for index in range(len(hospital)):
    #        hospital[index]["id"] = str(hospital[index]["id"].hex)
    #        hospital[index]

    #    data = list(hospital)
    #    return HttpResponse(json.dumps(data), content_type="application/json")
    
    def post(self, request):
        hospital = models.Hospital()

        # get puskesmas object
        hospital.name = request.POST.get("name")
        hospital.address = request.POST.get("address")
        hospital.latitude = request.POST.get("latitude")
        hospital.longitude = request.POST.get("longitude")
        hospital.area = request.POST.get("area")
        hospital.category = request.POST.get("category")
        hospital.class_type = request.POST.get("class_type")
        hospital.bed_availability = request.POST.get("bed_availability")
        hospital.image_name = request.POST.get("image_name")
        hospital.save()

        data = {
            "status": "success",
            "message": "Berhasil menambahkan data rumah sakit"
        }

        return HttpResponse(json.dumps(data), content_type="application/json")

class HospitalDetailView(View):
    def get(self, request, id_hospital):
        try:
            hospital = models.Hospital.objects.get(pk=id_hospital)
        except:
            data = {}
            return HttpResponse(json.dumps(data), content_type="application/json")

        image_url = hospital.image_name

        data = {
            "status": "success",
            "data": {
                "id": hospital.id.hex,
                "name": hospital.name,
                "address": hospital.address,
                "latitude": hospital.latitude,
                "longitude": hospital.longitude,
                "area": hospital.area,
                "category": hospital.category,
                "class_type": hospital.class_type,
                "bed_availability": hospital.bed_availability,
                "image_url": image_url
            }
        }

        return HttpResponse(json.dumps(data), content_type="application/json")
    
    def put(self, request, id_hospital):
        req = MultiPartParser(request.META, request, request.upload_handlers).parse()[0]
        
        hospital = models.Hospital.objects.get(pk=id_hospital)
        hospital.name = req.get("name")
        hospital.address = req.get("address")
        hospital.latitude = req.get("latitude")
        hospital.longitude = req.get("longitude")
        hospital.area = req.get("area")
        hospital.category = req.get("category")
        hospital.class_type = req.get("class_type")
        hospital.bed_availability = req.get("bed_availability")
        hospital.image_name = req.get("image_name")
        hospital.save()

        data = {
            "status": "success",
            "message": "Berhasil menambahkan data puskesmas"
        }

        return HttpResponse(json.dumps(data), content_type="application/json")

    def delete(self, request, id_hospital):
        try:
            hospital = models.Hospital.objects.get(pk=id_hospital)
            hospital.delete()
        except:
            data = {}
            return HttpResponse(json.dumps(data), content_type="application/json")

        data = {
            "status": "success",
            "message": "Berhasil menghapus data rumah sakit"
        }

        return HttpResponse(json.dumps(data), content_type="application/json")

class TreatmentFilterUserView(View):
    def get(self, request, id_user):
        treatment = models.Treatment.objects.filter(user=id_user).order_by('start_time').values("id", "start_time", "end_time", "painscale", "immediacy", "temperature", "puskesmas_id", "user_id", "prediction_time")
        treatment = list(treatment)

        for index in range(len(treatment)):
            treatment[index]["id"] = str(treatment[index]["id"].hex)
            treatment[index]["user_id"] = str(treatment[index]["user_id"].hex)
            treatment[index]["puskesmas_id"] = str(treatment[index]["puskesmas_id"].hex)
            puskesmas = models.Puskesmas.objects.get(pk=treatment[index]["puskesmas_id"])
            treatment[index]["puskesmas"] = {
                    "id": str(puskesmas.id.hex),
                    "name": puskesmas.name,
                    "address": puskesmas.address
                    }
            del treatment[index]["puskesmas_id"]
            treatment[index]["start_time"] = str(treatment[index]["start_time"])
            treatment[index]["end_time"] = str(treatment[index]["end_time"])

        data = list(treatment)
        return HttpResponse(json.dumps(data), content_type="application/json")

class TreatmentView(View):
    def getCategoryAge(self, age):
        if age < 15:
            return 1 
        elif age >= 15 and age < 25:
            return 2
        elif age >=25 and age < 45:
            return 3
        elif age >= 45 and age < 65:
            return 4
        elif age >= 65 and age < 75:
            return 5
        elif age >= 75:
            return 6

    def getCategorySex(self, sex):
        if sex == "Perempuan" or sex == "Female":
            return 1
        elif sex == "Laki-laki" or sex == "Male":
            return 2

    def getPredictionTime(self, sex, age, immediacy, painscale, temperature):
        filename = 'lib/appkesmasML/weight_model_waittime'
        load_model = pickle.load(open(filename,'rb'))

        category_age = self.getCategoryAge(age)
        category_sex = self.getCategorySex(sex)

        prediction_result = load_model.predict([[ category_sex, category_age, immediacy, painscale, temperature ]]) 

        return prediction_result

    def get(self, request):
        treatment = models.Treatment.objects.all().values("id", "start_time", "end_time", "painscale", "immediacy", "temperature", "puskesmas_id", "user_id", "prediction_time")
        treatment = list(treatment)

        for index in range(len(treatment)):
            treatment[index]["id"] = str(treatment[index]["id"].hex)
            treatment[index]["user_id"] = str(treatment[index]["user_id"].hex)
            treatment[index]["puskesmas_id"] = str(treatment[index]["puskesmas_id"].hex)
            treatment[index]["start_time"] = str(treatment[index]["start_time"])
            treatment[index]["end_time"] = str(treatment[index]["end_time"])

        data = list(treatment)
        return HttpResponse(json.dumps(data), content_type="application/json")

    def post(self, request):
        treatment = models.Treatment()

        # get puskesmas object
        user_id = request.POST.get("user_id")
        user = models.User.objects.get(pk=user_id)

        treatment.user = user
        # treatment.doctor_name = request.POST.get("doctor_name")
        # treatment.jenis_pengobatan = request.POST.get("jenis_pengobatan")
        treatment.puskesmas_id = request.POST.get("puskesmas_id")
        painscale = request.POST.get("painscale")
        immediacy = request.POST.get("immediacy")
        temperature = request.POST.get("temperature")
        treatment.prediction_time = self.getPredictionTime(user.sex, user.age, painscale, immediacy, temperature)
        
        treatment.save()

        data = {
            "status": "success",
            "message": "Berhasil menambahkan data treatment",
            "data": {
                "id": treatment.id.hex
            }
        }

        return HttpResponse(json.dumps(data), content_type="application/json")


class TreatmentDetailView(View):
    def get(self, request, id_treatment):
        try:
            treatment = models.Treatment.objects.get(pk=id_treatment)
        except:
            data = {}
            return HttpResponse(json.dumps(data), content_type="application/json")

        data = {
            "status": "success",
            "data": {
                "id": treatment.id.hex,
                "doctor_name": treatment.doctor_name,
                "jenis_pengobatan": treatment.jenis_pengobatan,
                "start_time": str(treatment.start_time),
                "end_time": str(treatment.end_time),
                "immediacy": treatment.immediacy,
                "temperature": treatment.temperature,
                "painscale": treatment.painscale,
                "prediction_time": treatment.prediction_time,
                "puskesmas_id": treatment.puskesmas_id.hex,
                "user_id": treatment.user_id.hex
            }
        }

        return HttpResponse(json.dumps(data), content_type="application/json")

    def put(self, request):
        req = MultiPartParser(request.META, request, request.upload_handlers).parse()[0]
        
        treatment = models.Treatment.objects.get(pk=id_treatment)

        user_id = req.get("user_id")
        user = models.User.objects.get(pk=user_id)

        treatment.user = user
        treatment.doctor_name = req.get("doctor_name")
        treatment.jenis_pengobatan = req.get("jenis_pengobatan")
        treatment.start_time = req.get("start_time")
        treatment.end_time = req.get("end_time")
        treatment.prediction_time = req.get("prediction_time")
        treatment.save()

        data = {
            "status": "success",
            "message": "Berhasil mengubah data treatment"
        }

        return HttpResponse(json.dumps(data), content_type="application/json")
    
    def delete(self, request, id_treatment):
        try:
            treatment = models.Treatment.objects.get(pk=id_treatment)
            treatment.delete()
        except:
            data = {}
            return HttpResponse(json.dumps(data), content_type="application/json")

        data = {
            "status": "success",
            "message": "Berhasil menghapus data treatment"
        }

        return HttpResponse(json.dumps(data), content_type="application/json")

class CovidDataView(View):
    def get(self, request):
        covid_data = models.CovidData.objects.all().values("id", "date", "cases", "recovered", "death")
        covid_data = list(covid_data)

        for index in range(len(covid_data)):
            covid_data[index]["id"] = str(covid_data[index]["id"].hex)
            covid_data[index]["date"] = str(covid_data[index]["date"])

        data = list(covid_data)
        return HttpResponse(json.dumps(data), content_type="application/json")

    def post(self, request):
        covid_data = models.CovidData()

        covid_data.cases = request.POST.get("cases")
        covid_data.recovered = request.POST.get("recovered")
        covid_data.death = request.POST.get("death")
        covid_data.save()

        data = {
            "status": "success",
            "message": "Berhasil menambahkan data covid"
        }

        return HttpResponse(json.dumps(data), content_type="application/json")

# class CovidDetailView(View):
#     def get(self, request):
#     def put(self, request):
#     def delete(self, request):

class PrescriptionFilterUserView(View):
    def get(self, request, id_user):
        prescription = models.Prescription.objects.filter(user=id_user).order_by('date').values("id", "user", "puskesmas", "doctor_name", "date", "drug_list")
        prescription = list(prescription)


        for index in range(len(prescription)):
            prescription[index]["id"] = str(prescription[index]["id"].hex)
            prescription[index]["user"] = str(prescription[index]["user"].hex)

            puskesmas = models.Puskesmas.objects.get(pk=prescription[index]["puskesmas"])
            puskesmas_data = {
                "id": puskesmas.id.hex,
                "name": puskesmas.name
            }
            prescription[index]["puskesmas"] = puskesmas_data

            prescription[index]["date"] = str(prescription[index]["date"].date())

        data = list(prescription)

        return HttpResponse(json.dumps(data), content_type="application/json")

class PrescriptionView(View):
    def get(self, request):
        prescription = models.Prescription.objects.all().values("id", "user", "puskesmas", "doctor_name", "date", "drug_list")
        prescription = list(prescription)

        for index in range(len(prescription)):
            prescription[index]["id"] = str(prescription[index]["id"].hex)
            prescription[index]["user"] = str(prescription[index]["user"].hex)
            prescription[index]["puskesmas"] = str(prescription[index]["puskesmas"].hex)

        data = list(prescription)

        return HttpResponse(json.dumps(data), content_type="application/json")

    def post(self, request):
        prescription = models.Prescription()

        user_id = request.POST.get("user_id")
        user = models.User.objects.get(pk=user_id)

        prescription.user = user
        prescription.drug_list = request.POST.get("drug_list")
        puskesmas_id = request.POST.get("puskesmas_id")
        puskesmas = models.Puskesmas.objects.get(pk=puskesmas_id)
        prescription.puskesmas = puskesmas

        prescription.doctor_name = request.POST.get("doctor_name")
        prescription.save()

        data = {
            "status": "success",
            "message": "Berhasil menambahkan data resep obat"
        }

        return HttpResponse(json.dumps(data), content_type="application/json")

class PrescriptionDetailView(View):
    def get(self, request, id_prescription):
        try:
            prescription = models.Prescription.objects.get(pk=id_prescription)
        except:
            data = {}
            return HttpResponse(json.dumps(data), content_type="application/json")

        data = {
            "status": "success",
            "data": {
                "id": prescription.id.hex,
                "user_id": prescription.user.id.hex,
                "drug_list": prescription.drug_list
            }
        }

        return HttpResponse(json.dumps(data), content_type="application/json")

    def put(self, request):
        req = MultiPartParser(request.META, request, request.upload_handlers).parse()[0]
        
        prescription = models.Prescription.objects.get(pk=id_prescription)

        user_id = req.get("user_id")
        user = models.User.objects.get(pk=user_id)
        prescription.user = user
        prescription.drug_list = req.get("drug_list")
        prescription.save()

        data = {
            "status": "success",
            "message": "Berhasil mengubah data resep obat"
        }

        return HttpResponse(json.dumps(data), content_type="application/json")
    
    def delete(self, request, id_treatment):
        try:
            prescription = models.Prescription.objects.get(pk=id_prescription)
            prescription.delete()
        except:
            data = {}
            return HttpResponse(json.dumps(data), content_type="application/json")

        data = {
            "status": "success",
            "message": "Berhasil menghapus data resep obat"
        }

        return HttpResponse(json.dumps(data), content_type="application/json")

class BannerHeaderView(View):
    def get(self, request):
        banner_header = models.BannerHeader.objects.all().values("id", "image_url", "status")
        banner_header = list(banner_header)

        for index in range(len(banner_header)):
            banner_header[index]["id"] = str(banner_header[index]["id"].hex)

        data = list(banner_header)

        return HttpResponse(json.dumps(data), content_type="application/json")

    def post(self, request):
        banner_header = models.BannerHeader()

        banner_header.image_url = request.POST.get("image_url")
        banner_header.status = request.POST.get("status")
        banner_header.save()

        data = {
            "status": "success",
            "message": "Berhasil menambahkan data banner header"
        }

        return HttpResponse(json.dumps(data), content_type="application/json")

class BannerHeaderDetailView(View):
    def get(self, request, id_banner_header):
        try:
            banner_header = models.BannerHeader.objects.get(pk=id_banner_header)
        except:
            data = {}
            return HttpResponse(json.dumps(data), content_type="application/json")

        data = {
            "status": "success",
            "data": {
                "id": banner_header.id.hex,
                "image_url": banner_header.image_url,
                "status": banner_header.status
            }
        }

        return HttpResponse(json.dumps(data), content_type="application/json")

    def put(self, request, id_banner_header):
        req = MultiPartParser(request.META, request, request.upload_handlers).parse()[0]
        
        banner_header = models.BannerHeader.objects.get(pk=id_banner_header)

        banner_header_id = req.get("banner_header_id")
        banner_header = models.BannerHeader.objects.get(pk=banner_header_id)

        banner_header.image_url = req.get("image_url")
        banner_header.status = req.get("status")
        banner_header.save()

        data = {
            "status": "success",
            "message": "Berhasil mengubah data Banner Header"
        }

        return HttpResponse(json.dumps(data), content_type="application/json")
    
    def delete(self, request, id_banner_header):
        try:
            banner_header = models.BannerHeader.objects.get(pk=id_banner_header)
            banner_header.delete()
        except:
            data = {}
            return HttpResponse(json.dumps(data), content_type="application/json")

        data = {
            "status": "success",
            "message": "Berhasil menghapus data Banner Header"
        }

        return HttpResponse(json.dumps(data), content_type="application/json")

class ArticleView(View):
    def get(self, request):
        article = models.Article.objects.all().values("id", "image_url", "title", "category", "status")
        article = list(article)

        for index in range(len(article)):
            article[index]["id"] = str(article[index]["id"].hex)

        data = list(article)

        return HttpResponse(json.dumps(data), content_type="application/json")

    def post(self, request):
        article = models.Article()

        article.image_url = request.POST.get("image_url")
        article.status = request.POST.get("status")
        article.title = request.POST.get("title")
        article.content = request.POST.get("content")
        article.category = request.POST.get("category")
        article.save()

        data = {
            "status": "success",
            "message": "Berhasil menambahkan data article"
        }

        return HttpResponse(json.dumps(data), content_type="application/json")


class ArticleDetailView(View):
    def get(self, request, id_article):
        try:
            article = models.Article.objects.get(pk=id_article)
        except:
            data = {}
            return HttpResponse(json.dumps(data), content_type="application/json")

        data = {
            "status": "success",
            "data": {
                "id": article.id.hex,
                "image_url": article.image_url,
                "status": article.status,
                "title": article.title,
                "category": article.category,
                "content": article.content
            }
        }

        return HttpResponse(json.dumps(data), content_type="application/json")

    def put(self, request, id_article):
        req = MultiPartParser(request.META, request, request.upload_handlers).parse()[0]
        
        article = models.BannerHeader.objects.get(pk=id_article)

        article.image_url = req.get("image_url")
        article.status = req.get("status")
        article.content = req.get("content")
        article.title = req.get("title")
        article.category = req.get("category")
        article.save()

        data = {
            "status": "success",
            "message": "Berhasil mengubah data artikel"
        }

        return HttpResponse(json.dumps(data), content_type="application/json")

    def delete(self, request, id_article):
        try:
            article = models.Article.objects.get(pk=id_article)
            article.delete()
        except:
            data = {}
            return HttpResponse(json.dumps(data), content_type="application/json")

        data = {
            "status": "success",
            "message": "Berhasil menghapus data artikel"
        }

        return HttpResponse(json.dumps(data), content_type="application/json")
