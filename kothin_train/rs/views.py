from django.shortcuts import *
from django.db import connection
from django.contrib.auth import *
from django.urls import *
from datetime import date
from django.contrib import messages
from django.http import JsonResponse
from sslcommerz_lib import SSLCOMMERZ 
from django.views.decorators.csrf import csrf_exempt
import math

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

    if(request.method=='POST'):
        email=request.POST.get('email')
        password=request.POST.get('password')
        cursor=connection.cursor()
        query=(
            "SELECT * "
            "FROM R_USER "
            "WHERE E_MAIL=%s "
            "AND PASSWORD=%s "
            )
        cursor.execute(query,(email,password))
        res=cursor.fetchall()
        cursor.close()
        if(len(res)==0):
            context['not_reg']=True
            return render(request, "login.html",context)
        else:
            user_data={}
            user_data['email']=res[0][5]
            user_data['name']=res[0][2]+" "+res[0][3]
            user_data['id']=res[0][0]
            user_data['phone']=res[0][11]
            request.session['user_data'] = user_data
            return redirect('homepage')
        
    return render(request, "login.html",context)

def homepage(request):
    context={}

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

    if request.method == 'POST':
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
        if(res):
            context['nid_duplicate']=True
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
    context={}

    from_station = request.GET.get('from').strip()
    to_station = request.GET.get('to').strip()
    date_user = request.GET.get('date').strip()
    try:
        date_user = date.fromisoformat(date_user)  # Convert the string to a date object
        date_user = date_user.strftime('%Y-%m-%d')
    except ValueError:
        # Handle invalid date_user format here
        pass

    cursor=connection.cursor()
    from_station_id = cursor.callfunc("getID", int,[from_station])
    query = (
        """SELECT * 
        FROM "Train-Timetable" tt 
        JOIN "Train" t ON t."Train ID" = tt."Train ID"
        WHERE tt."From Station Name" =%s
        AND tt."To Station Name" = %s
        AND TRUNC(tt."Departure Time") = TO_DATE(%s, 'YYYY-MM-DD')
        AND tt."Departure Time" > SYSTIMESTAMP """
    )
    cursor.execute(query,(from_station,to_station,date_user));
    res=cursor.fetchall()
    query2=(
        """SELECT SHOVAN,S_CHAIR,SNIGDHA
        FROM "Cost"
        WHERE "Train ID"=%s and
        "FromStation Name"=%s AND
        "ToStation Name"=%s """
    )
    cursor.close();
    formatted_res=[]
    for row in res:
        print(row)
        fr=[] #id+train name,start station, start time, end station, end time,shovan,s_chair,snigdha,id,date,cost1,cost2,cost3
        fr.append(str(row[6])+" ("+str(row[0])+")")
        fr.append(from_station)
        formatted_departure_time = row[3].strftime('%d %b, %I:%M %p')
        fr.append(formatted_departure_time)
        fr.append(to_station)
        formatted_arrival_time = row[4].strftime('%d %b, %I:%M %p')
        fr.append(formatted_arrival_time)
        fr.append(50)
        fr.append(50)
        fr.append(50)
        fr.append(row[0])
        fr.append(row[3].date().strftime('%Y-%m-%d'))
        cursor=connection.cursor()
        cursor.execute(query2,(int(row[0]),from_station,to_station))
        res2=cursor.fetchall()
        cursor.close()
        fr.append(res2[0][0])
        fr.append(res2[0][1])
        fr.append(res2[0][2])
        formatted_res.append(fr)

    context['train_res']=formatted_res
    context['from_station']=from_station
    context['to_station']=to_station
    context['doj']=date_user
    return render(request,'train_show.html',context)

def booked_seats(request):
    selected_seats = request.GET.get('selectedSeats', '').split(',')
    seatClass=request.GET.get('seatClass','')
    train_id=request.GET.get('trainID','')
    from_station=request.GET.get('from')
    to_station=request.GET.get('to')
    doj=request.GET.get('doj')
    fromid=get_station_id(from_station)
    toid=get_station_id(to_station)
    cost=0
    query=(
        """SELECT SHOVAN,S_CHAIR,SNIGDHA
        FROM "Cost"
        WHERE "Train ID"=%s AND
        "FromStation Name"=%s AND
        "ToStation Name"=%s """
    )
    cursor=connection.cursor()
    cursor.execute(query,(train_id,from_station,to_station))
    res=cursor.fetchall()
    if seatClass=='Snigdha':
        cost=res[0][2]
    elif seatClass=='Shovan':
        cost=res[0][0]
    else:
        cost=res[0][1]
        cost=cost+cost*15/100
        cost=math.ceil(cost)
    total=cost*len(selected_seats)
    if request.method=='POST':
        base_url = request.build_absolute_uri('/')[:-1]
        settings = { 'store_id': 'shoho64ef8f4171208', 'store_pass': 'shoho64ef8f4171208@ssl', 'issandbox': True }
        sslcommez = SSLCOMMERZ(settings)
        post_body = {}
        post_body['total_amount'] = total
        post_body['currency'] = "BDT"
        post_body['tran_id'] = "1111"
        post_body['success_url'] = f"{base_url}/success"
        post_body['fail_url'] = f"{base_url}/failed"
        post_body['cancel_url'] = f"{base_url}/failed"
        post_body['ipn_url'] = f"{base_url}/verify"
        post_body['emi_option'] = 0
        post_body['cus_name'] = request.session.get('user_data')['name']
        post_body['cus_email'] = request.session.get('user_data')['email']
        post_body['cus_phone'] = request.session.get('user_data')['phone']
        post_body['cus_add1'] = ""
        post_body['cus_city'] = "Dhaka"
        post_body['cus_country'] = "Bangladesh"
        post_body['shipping_method'] = "NO"
        post_body['multi_card_name'] = ""
        post_body['num_of_item'] = 1
        post_body['product_name'] = "ticket"
        post_body['product_category'] = "ticket"
        post_body['product_profile'] = "general"
        post_body['value_a'] = request.session.get('user_data')['id'] # USER ID
        post_body['value_b'] = str(train_id)+"*"+str(fromid)+"*"+str(toid)+"*"+str(doj)+"*"+seatClass+"*"+",".join(selected_seats);
        response = sslcommez.createSession(post_body)
        #print(response)
        #print(str(train_id)+"-"+str(fromid)+"-"+str(toid)+"-"+str(doj)+"-"+seatClass+"-"+",".join(selected_seats))
        return redirect(response['GatewayPageURL'])
    
    context = {'train_id':train_id,'seat_class':seatClass,'selected_seats': selected_seats}
    return render(request,'booked_seats.html',context)

def fetch_booked_seats(request):
    train_id = request.GET.get('train_id')
    date_user=request.GET.get('departure_date')
    seat_class=request.GET.get('seat_class')
    with connection.cursor() as cursor:
        query = (
            """SELECT "Seat No"
                from "Reserved-seat"
                WHERE "Train ID"=%s
                and "Departure Date"=to_date(%s,'YYYY-MM-DD') 
                and "Class"=%s """
        )
        cursor.execute(query, (train_id,date_user,seat_class))
        booked_seats = [row[0] for row in cursor.fetchall()]
    return JsonResponse({'booked_seats': booked_seats})

@csrf_exempt
def success(request):
    if(request.method=='POST'):
        tran_date = request.POST['tran_date']
        tran_date=tran_date.split(" ")[0].strip()
        val_id = request.POST['val_id']
        amount = request.POST['amount']
        currency = request.POST['currency']
        status = request.POST['status']
        tran_id = request.POST['tran_id']
        userid=request.POST['value_a']
        info=request.POST['value_b']

        train_id, fromid, toid, doj, seat_class, selected_seats = info.split('*')
        selected_seats_list = selected_seats.split(',')
        print(status)
        print("-------------------")
        print(info)
        if status=='VALID':
            query = (
                """INSERT INTO "C##KOTHIN_TRAIN"."Reservation"
                ("Reservation ID", "Date of Reservation", "Date of Journey", "No. of Tickets", "Class", "From Station", "To Station", "User-ID", "Payment ID")
                VALUES (%s, TO_DATE(%s, 'YYYY-MM-DD'), TO_DATE(%s, 'YYYY-MM-DD'), %s, %s, %s, %s, %s, %s) """
            )
            cursor=connection.cursor()
            cursor.execute(query, (info, tran_date,doj, len(selected_seats_list), seat_class, fromid, toid, userid,tran_id))
            query2 = (
                    """INSERT INTO "C##KOTHIN_TRAIN"."Reserved-seat" ("Train ID", "From Station ID", "To Station ID", "Departure Date", "Seat No", "User ID", "Class") 
                    VALUES (%s, %s, %s, TO_DATE(%s, 'YYYY-MM-DD'), %s, %s, %s) """
                )
            for seat in selected_seats_list:
                cursor.execute(query2,(train_id,fromid,toid,doj,seat,userid,seat_class))
            cursor.close()
    return render(request,'confirm.html')

@csrf_exempt
def failed(request):
    return render(request,'failed.html')

@csrf_exempt
def ipn_handler(request):
    if(request.method=='POST'):
        tran_date = request.POST['tran_date']
        val_id = request.POST['val_id']
        amount = request.POST['amount']
        currency = request.POST['currency']
        status = request.POST['status']
        tran_id = request.POST['tran_id']
        userid=request.POST['value_a']
        info=request.POST['value_b']

        train_id, fromid, toid, doj, seat_class, selected_seats = info.split('*')
        selected_seats_list = selected_seats.split(',')
        print(status)
        print("-------------------")
        print(info)
        if status=='VALID':
            query = (
                """INSERT INTO "C##KOTHIN_TRAIN"."Reservation"
                ("Reservation ID", "Date of Reservation", "Date of Journey", "No. of Tickets", "Class", "From Station", "To Station", "User-ID", "Payment ID")
                VALUES (%s, TO_DATE(%s, 'YYYY-MM-DD'), TO_DATE(%s, 'YYYY-MM-DD'), %s, %s, %s, %s, %s, %s) """
            )
            cursor=connection.cursor()
            cursor.execute(query, (info, tran_date,doj, len(selected_seats_list), seat_class, fromid, toid, userid,tran_id))
            query2 = (
                    """INSERT INTO "C##KOTHIN_TRAIN"."Reserved-seat" ("Train ID", "From Station ID", "To Station ID", "Departure Date", "Seat No", "User ID", "Class") 
                    VALUES (%s, %s, %s, TO_DATE(%s, 'YYYY-MM-DD'), %s, %s, %s) """
                )
            for seat in selected_seats_list:
                cursor.execute(query2,(train_id,fromid,toid,doj,seat,userid,seat_class))
            cursor.close()
            return HttpResponse(status=200)
        
        return HttpResponse(status=400)
    return HttpResponse(status=400)

#returns station id
def get_station_id(name):
    cursor=connection.cursor()
    id = cursor.callfunc("getID", int,[name])
    cursor.close()
    return id

def purchase_history():
    pass;
