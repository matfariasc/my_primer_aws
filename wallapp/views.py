from django.shortcuts import redirect, render , HttpResponse
from .models import users , validaremail , comments ,messages as dbmessages
from django.contrib import messages
import bcrypt
# Create your views here.

def index_login(request):
    if "id" in request.session:
        return redirect("index_wall")
    return render(request,"login/index.html")

def wall_index(request):
    if 'id' in request.session:
        contex = {
            'user' : users.objects.get(id=request.session['id']),
            'messages' : dbmessages.objects.all()
        }
        return render (request,'wall/index.html',contex)
    return redirect("/login")

def new_user(request):
    if request.method == "POST":
        print("Entrando a la creacion de un nuevo usuario, validando datos")
        erros = users.objects.basic_validator(request.POST)
        if len(erros) >0:
            for key, value in erros.items():
                messages.error(request, value, key)
            return render(request,"login/index.html")
        encrippw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        users.objects.create(
        first_name = request.POST["fname"],
        last_name = request.POST["lname"],
        email = request.POST["email"],
        password = encrippw.decode()
        )
        id_user = users.objects.get(email=request.POST["email"])
        request.session["id"] = id_user.id
        print(id_user.id)
        return redirect("index_wall")
    if request.method == "GET":
        return redirect("/")
    
def login(request):
    if request.method == "GET":
        return redirect("index_login")
    if request.method == "POST":
        email = request.POST["email"]
        usuario = validaremail(email=email)
        if usuario:
            validacionpw = bcrypt.checkpw(request.POST["password"].encode(), usuario.password.encode())
            if validacionpw:
                request.session["id"] = usuario.id
                return redirect("index_wall")
        messages.error(request, "La contraseña y/o email no son validos", "loginerror")
        return redirect("index_login")
                
def log_out(request):
    if "id" in request.session:
        del request.session["id"]
    return redirect("/")

def post_new(request):
    if request.method == "GET":
        return redirect("index_login")

    if request.method == "POST":
        dbmessages.objects.create(message=request.POST['message'],user_id=request.session['id'])
        return redirect("index_wall")

def comment_new(request):
    if request.method == "GET":
        return redirect("index_login")
    if request.method == "POST":
        comments.objects.create(comment=request.POST['comment'],user_id=request.session['id'],message_id=request.POST['message_id'])
        return redirect("index_wall")