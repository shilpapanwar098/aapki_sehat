from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

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


# Create your views here.
@login_required
def allPatients(request):
    global db
    hospitalName = request.user.username
    if db.child('Patients').child(hospitalName).shallow().get().val():
        users_query = db.child('Patients').child(hospitalName).order_by_child('mews').start_at(0).end_at(14).get()
        users = users_query.val() # Pyrebase object gave the data
        content = []

        for user in reversed(users):
            content.append(users[user])
        # take only the second part of each entry i.e value corresponding to the key
        return render(request, 'mainApp/allPatients.html', {'content': content, 'hospitalName': hospitalName})
         # query created and Pyrebase object returned
    else:
        return render(request, 'mainApp/nopatients.html', {'hospitalName': hospitalName}) 

@login_required
def patientDetail(request, phoneNo):
    global db
    hospitalName = request.user.username
    # query created and Pyrebase object returned
    users_query = db.child('Patients').child(hospitalName).get()
    users = users_query.val()  # Pyrebase object gave the data
    content = []
    # phoneNo converted to string since it is an integer
    specific_user = users[str(phoneNo)]
    return render(request, 'mainApp/patientDetails.html', {'user': specific_user, 'hospitalName': hospitalName})

@login_required
def requests_patients(request):
    global db
    hospitalName = request.user.username
    #contact

    try:
        content1 = []
        users_query=db.child("contact").order_by_child("request").equal_to(hospitalName).get()
        users= users_query.val()     
        if users:
            for user in users:
                content1.append(users[user])
    except:
        content1="None"
    print(content1)
    #positive
    try:
        content2 = []
        users_query2=db.child("positive").order_by_child("request").equal_to(hospitalName).get()
        users2= users_query2.val()     
        if users2:
            for user2 in users2:
                content2.append(users2[user2]) 
    except:
        content2="None"   
    #postcovid
    try:
        content3 = []
        users_query3=db.child("postcovid").order_by_child("request").equal_to(hospitalName).get()
        users3= users_query3.val()     
        if users_query3.val():
            for user3 in users3:
                content3.append(users3[user3])                  
    except:
        content3="None"                           
    return render(request, 'mainApp/requests.html', {'content1': content1,'content2': content2,'content3': content3, 'hospitalName': hospitalName})



@login_required
def contactpatientDetail(request, uid):
  global db
  hospitalName = request.user.username
  try:
      users_query=db.child("contact").order_by_child("request").equal_to(hospitalName).get()
      users = users_query.val() 
      specific_user = users[uid]
  except:
      specific_user="No Requests!"
  return render(request, 'mainApp/requestPatientDetails.html', {'user': specific_user, 'hospitalName': hospitalName})  


@login_required
def postcovidpatientDetail(request, uid):
  global db
  hospitalName = request.user.username
  try:
      users_query=db.child("postcovid").order_by_child("request").equal_to(hospitalName).get()
      users = users_query.val() 
      specific_user = users[uid]
  except:
      specific_user="No Requests!"
  return render(request, 'mainApp/requestPatientDetails.html', {'user': specific_user, 'hospitalName': hospitalName})  
def redirectU(request):
  return redirect('login')


@login_required
def covidpatientDetail(request, uid):
    global db
    hospitalName = request.user.username
    try:
        users_query=db.child("positive").order_by_child("request").equal_to(hospitalName).get()
        users = users_query.val() 
        specific_user = users[uid]
    except:
        specific_user="No Requests!"
    return render(request, 'mainApp/requestpatientDetail.html', {'user': specific_user, 'hospitalName': hospitalName})  