from django.shortcuts import *
from django.db import connection
# Create your views here.

def get_next_cardinal():
    with connection.cursor() as cursor:
        query =(
            "SELECT COUNT(*) FROM R_USER"
        )
        cursor.execute(query)
        user_count = int(cursor.fetchone()[0])
        return user_count + 1


def login(request):
    dict={}
    return render(request, "login.html", context=dict)

def homepage(request):
    dict={}
    return render(request, "search.html", context=dict)

def registration(request):
    if request.method == 'POST':
        # Extract form data
        first_name = request.POST.get('frst')
        last_name = request.POST.get('last')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        nid = request.POST.get('nid')
        house_number = request.POST.get('houseno')
        road_number = request.POST.get('roadno')
        zip_code = request.POST.get('zip')
        city = request.POST.get('city')
        contact = request.POST.get('contact')
        password = request.POST.get('password')

        # Execute raw SQL query to insert data
        with connection.cursor() as cursor:
            query = (
                "INSERT INTO R_USER (user_id,first_name, last_name, gender, e_mail, nid, house_no,road_no,zip_code,city, contact, password)"
                "VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)"
            )
            cardinal=get_next_cardinal()
            cursor.execute(query, (cardinal,first_name, last_name, gender, email, nid, house_number,road_number,zip_code,city, contact, password))
            query2=(
                "SELECT * FROM R_USER"
            )
            cursor.execute(query2)
            res=cursor.fetchall()
            print(res)
        # Redirect to a success page or login page
        return redirect('login')  # Replace 'login' with the appropriate URL name
    return render(request,'registration.html')