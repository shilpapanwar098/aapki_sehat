from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import PatientRegistrationForm
import pyrebase #import firebase

config = {
   'apiKey': "AIzaSyASzMZ8TCwipB0ijj0UnwYahYgx5mRvY_c",
  'authDomain': "solid-arcadia-269918.firebaseapp.com",
  'databaseURL': "https://solid-arcadia-269918.firebaseio.com",
  'projectId': "solid-arcadia-269918",
  'storageBucket': "solid-arcadia-269918.appspot.com",
  'messagingSenderId': "60290511239",
  'appId': "1:60290511239:web:b7645a217836e12003a322",
  'measurementId': "G-T8F0WNL4RW"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()


@login_required
def register_patient(request):
    if request.method == 'POST':
        hospitalName = request.user.username
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data.get('firstname')
            lastname = form.cleaned_data.get('lastname')
            phoneNo = form.cleaned_data.get('phoneNo')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            age = form.cleaned_data.get('age')
            aadharno = form.cleaned_data.get('aadharno')
            bloodgrp = form.cleaned_data.get('bloodgrp')
            temperature = 0
            bp = 0
            spo2 = 0
            heartrate = 0
            rr = 0
            avpu = 0
            mews = 0
            password = str(phoneNo)

            data = {'firstname': firstname, 'lastname': lastname, 'phoneNo': phoneNo,  'email': email, 'gender': gender, 'age': age, 'aadharno': aadharno,
                    'bloodgrp': bloodgrp, 'temperature': temperature, 'bp': bp, 'spo2': spo2, 'rr': rr, 'avpu': avpu, 'heartrate': heartrate, 'mews': mews}
            accesst = {'hospital': hospitalName,
                       'phno': phoneNo}
            try:
                if db.child('Patients').child(hospitalName).child(phoneNo).get().val():
                    message1 = "Patient Already exists with the same Phone Number"
                    form = PatientRegistrationForm()
                    return render(request, 'patients/patientRegister.html', {'form': form, 'message': message1})
                else:
                    auth.create_user_with_email_and_password(email, password)
                       # the user will be identified by his phoneNo
                    db.child('Patients').child(
                    hospitalName).child(phoneNo).set(data)
                    user = auth.sign_in_with_email_and_password(email, password)
                    uid = (user['localId'])
                    db.child('Access').child(
                    uid).set(accesst)
                    return redirect('user/')
            except:
                message2 = "Enter valid credentials"
                form = PatientRegistrationForm()
                return render(request, 'patients/patientRegister.html', {'form': form, 'message': message2})
        else:
            message2 = form.errors
            form = PatientRegistrationForm()
            return render(request, 'patients/patientRegister.html', {'form': form, 'message': message2})
    else:
        form = PatientRegistrationForm()
        message2 = None
        return render(request, 'patients/patientRegister.html', {'form': form, 'message': message2})