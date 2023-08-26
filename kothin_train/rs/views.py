from django.shortcuts import *
from django.db import connection
from django.contrib.auth import *
from django.urls import *
from datetime import date
from django.contrib import messages
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
        print(res)
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
    #print(context['User_Name'])
    if request.method == 'POST':
        from_station = request.POST.get('from')
        to_station = request.POST.get('to')
        date = request.POST.get('date')
        adult = request.POST.get('adult')
        child = request.POST.get('child')
        s_class = request.POST.get('class')
        train_show_url = reverse('train_show') + f'?from={from_station}&to={to_station}&date={date}&adult={adult}&child={child}&class={s_class}'
        return redirect(train_show_url)
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

def train_show(request):
    from_station = request.GET.get('from').strip()
    to_station = request.GET.get('to').strip()
    date_user = request.GET.get('date').strip()
    adult = request.GET.get('adult')
    child = request.GET.get('child')
    s_class = request.GET.get('class')
    date_n=date.today()
    try:
        date_user = date.fromisoformat(date_user)  # Convert the string to a date object
        date_user = date_user.strftime('%Y-%m-%d')
    except ValueError:
        # Handle invalid date_user format here
        pass
    print('this is ',date_user,' and ',type(date_user))

    query = (
        """SELECT * 
        FROM "Train-Timetable" tt 
        JOIN "Train" t ON t."Train ID" = tt."Train Id"
        WHERE tt."Station Id" = (SELECT "Station ID" FROM "Station" WHERE "Name" = %s)
        AND tt."Direction" = %s
        AND TRUNC(tt."Departure Time") = TO_DATE(%s, 'YYYY-MM-DD')  -- Corrected format
        AND tt."Departure Time" > SYSTIMESTAMP """
    )
    cursor=connection.cursor()
    cursor.execute(query,(from_station,to_station,date_user));
    res=cursor.fetchall()
    #print(res);
    cursor.close();
    formatted_res=[]
    for row in res:
        fr=[] #id+train name,start station, start time, end station, end time,shovan,s_chair,snigdha
        fr.append(str(row[5])+" ("+str(row[0])+")")
        fr.append(from_station)
        formatted_departure_time = row[2].strftime('%d %b, %I:%M %p')
        fr.append(formatted_departure_time)
        fr.append(row[3])
        fr.append('')
        fr.append(row[6])
        fr.append(row[7])
        fr.append(row[8])
        formatted_res.append(fr)

    context={
        'train_res':formatted_res,
    }
    return render(request,'train_show.html',context)

def booked_seats(request):
    selected_seats = request.GET.get('selectedSeats', '').split(',')
    # Process the selected seats as needed

    context = {'selected_seats': selected_seats}
    return render(request,'booked_seats.html',context)