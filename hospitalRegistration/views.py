from django.shortcuts import render, redirect
from .forms import HospitalBookForm
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


def HospitalUser(request):
    global db
    if request.method == 'POST':
        form = HospitalBookForm(request.POST, request.FILES)
        if form.is_valid():
            firstname = form.cleaned_data.get('username')
            regno = form.cleaned_data.get('regNo')    
            email = form.cleaned_data.get('email')    
            address = form.cleaned_data.get('hospiAddress')                        
            accesst = {'name': firstname,'regno':regno,'email':email,'address':address}
            try:
                # the user will be identified by his phoneNo
                db.child('HospitalInfo').child(
                    regno).set(accesst)
            except:
                message2 = "Patient Already Exist with same Phone Number"
            form.save()
            return redirect('login')
            
    else:
        form = HospitalBookForm()
    return render(request, 'hospitalRegistration/userreg.html', {'form': form})