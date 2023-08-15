from django.shortcuts import *
from django.db import connection
from django.contrib.auth import *
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
    context={}
    #context['User_Name']=""
    if(request.method=='POST'):
        print('here')
        email=request.POST.get('email')
        password=request.POST.get('password')
        cursor=connection.cursor()
        query=(
            "SELECT FIRST_NAME||' '||LAST_NAME AS NAME "
            "FROM R_USER "
            "WHERE E_MAIL=%s "
            "AND PASSWORD=%s "
            )
        cursor.execute(query,(email,password))
        res=cursor.fetchall()
        cursor.close()
        if(len(res)==0):
            context['login_failed']=True
            return render(request, "login.html",context)
        else:
            context['User_Name']=res[0][0]
            request.session['User_Name'] = context['User_Name']
            return redirect('homepage')
    return render(request, "login.html",context)

def homepage(request):
    context={}
    user_name = request.session.get('User_Name')
    print(request.session.items())
    if user_name:
        context['User_Name'] = user_name
        request.session['User_Name'] = context['User_Name']
    query=(
        "SELECT * "
    )
    #print(context['User_Name'])
    return render(request, "search.html",context)

def registration(request):
    context={}
    user_name = request.session.get('User_Name')
    if user_name:
        context['User_Name'] = user_name
        request.session['User_Name'] = context['User_Name']
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
        cursor=connection.cursor()
        query=(
            "SELECT NID "
            "FROM R_USER "
            "WHERE NID =%s "
        )
        cursor.execute(query,(nid,))
        res=cursor.fetchall()
        print(res)
        if(res):
            context['NID_Duplicate']=True
            cursor.close()
            return render(request,"registration.html",context)
        else:
            query = (
                "INSERT INTO R_USER (user_id,first_name, last_name, gender, e_mail, nid, house_no,road_no,zip_code,city, contact, password)"
                "VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)"
            )
            cardinal=get_next_cardinal()
            cursor.execute(query, (cardinal,first_name, last_name, gender, email, nid, house_number,road_number,zip_code,city, contact, password))
            cursor.close()
            return redirect('login')  # Replace 'login' with the appropriate URL name
    return render(request,'registration.html',context)

def about(request):
    return render(request,'about.html')

def test(request):
    return render(request,'test.html')

def log_out(request):
    logout(request)
    return redirect('login')