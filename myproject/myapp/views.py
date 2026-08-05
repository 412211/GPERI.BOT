from django.shortcuts import redirect, render
from django.contrib.auth.hashers import check_password, make_password
from myapp.models import *
import random
from django.db.models import Min

# Create your views here.

def login(request):
    if request.method=="POST":
       
        email = request.POST.get("email")
        
        password = request.POST.get("password")
        user=User.objects.filter(Email=email).first()
        if user:
            if check_password(password,user.Password):
                request.session["userID"]=user.id
                request.session["emailADD"]=user.Email
                request.session["uNAME"]=user.Name
                return redirect('/home/')
            else:
                return render(request,'login.html',{"errorMsg":"Invalid Credential."})
        else:
            return render(request,'login.html',{"errorMsg":"Invalid Credential."})
    return render(request, 'login.html')

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method=="POST":
        fullname = request.POST.get("fname")
        email = request.POST.get("email")
        contact = request.POST.get("contact")
        createpassword = request.POST.get("createpass")
        confirmpassword = request.POST.get("confirmpass")
        hashpassword = make_password(createpassword)
        if createpassword != confirmpassword:
            return render(request, 'registration.html',{"pwdError":"Password does not matched."})
        else:
            user = User(Name=fullname,Email=email,Contact=contact,Password=hashpassword)
            user.save()
        return redirect('/login/')
    else:
        print("Get Method")
    
    return render(request, 'registration.html')

def forgot(request):
    return render(request, 'forgotpass.html')

def newchat(request):
    
    uName = request.session.get("uNAME")
    email = request.session.get("emailADD")
    uId = request.session.get("userID")
    request.session.flush()
    request.session["userID"]=uId
    request.session["emailADD"]=email
    request.session["uNAME"]=uName
   
    return redirect("/home/")

def home(request):
    uid = request.session.get("userID")
    first_chat = (
        TempChatMaster.objects.filter(UserId=uid)
        .values('Temptoken').annotate(min_id=Min('id'))
    )
    
    chats_list = TempChatMaster.objects.filter(id__in=[chat['min_id'] for chat in first_chat])
    
    if request.method == "POST":
        if request.session.get("chatSession"):
            rno = request.session.get("chatSession")
            que = request.POST.get("message")
            que1 = que.upper() if que else ""

            # Find the question in QuestionSetMaster
            queInfo = QuestionSetMaster.objects.filter(Title=que1).first()

            # Save user's question to TempChatMaster
            uId=0
            if request.session.get("userID"):
                uId = request.session.get("userID")
            TempChatMaster.objects.create(Temptoken=rno, Message=que, Type="Sender", UserId=uId)

            if queInfo:
                # Fetch answer_id from QASetMaster
                qa_entry = QADataSet.objects.filter(Question_id=queInfo.id).first() # type: ignore
                
                if qa_entry:
                    # Fetch the actual answer from AnswerSetMaster
                    answer = AnswerSetMaster.objects.filter(id=qa_entry.Answer_id).first()
                    
                    if answer:
                        uId=0
                        if request.session.get("userID"):
                            uId = request.session.get("userID")
                        TempChatMaster.objects.create(Temptoken=rno, Message=answer.Title, Type="Reciever", UserId=uId)
                    else:
                        uId=0
                        if request.session.get("userID"):
                            uId = request.session.get("userID")
                        cMessage = "Sorry, we are working on your question. Please ask another question if you have."
                        TempChatMaster.objects.create(Temptoken=rno, Message=cMessage, Type="Reciever", UserId=uId)
                else:
                    cMessage = "Sorry! I have no answer about this."
                    uId=0
                    if request.session.get("userID"):
                        uId = request.session.get("userID")
                    TempChatMaster.objects.create(Temptoken=rno, Message=cMessage, Type="Reciever", UserId=uId)
            else:
                cMessage = "Sorry! I have no answer about this."
                uId=0
                if request.session.get("userID"):
                    uId = request.session.get("userID")
                TempChatMaster.objects.create(Temptoken=rno, Message=cMessage, Type="Reciever", UserId=uId)

            return redirect('/home1/' + str(rno))
        else:
            rno = random.randint(111111, 999999)
            request.session["chatSession"] = rno
            que = request.POST.get("message")
            que1 = que.upper() if que else ""

            if que:
                uId=0
                if request.session.get("userID"):
                    uId = request.session.get("userID")
                TempChatMaster.objects.create(Temptoken=rno, Message=que, Type="Sender", UserId=uId)
                queInfo = QuestionSetMaster.objects.filter(Title=que1).first()

                if queInfo:
                    qa_entry = QADataSet.objects.filter(Question_id=queInfo.id).first()
                    
                    if qa_entry:
                        answer = AnswerSetMaster.objects.filter(id=qa_entry.Answer_id).first()
                        
                        if answer:
                            uId=0
                            if request.session.get("userID"):
                                uId = request.session.get("userID")
                            TempChatMaster.objects.create(Temptoken=rno, Message=answer.Title, Type="Reciever", UserId=uId)
                        else:
                            uId=0
                            if request.session.get("userID"):
                                uId = request.session.get("userID")
                            cMessage = "Sorry, we are working on your question. Please ask another question if you have."
                            TempChatMaster.objects.create(Temptoken=rno, Message=cMessage, Type="Reciever", UserId=uId)
                    else:
                        uId=0
                        if request.session.get("userID"):
                            uId = request.session.get("userID")
                        cMessage = "Sorry! I have no answer about this."
                        TempChatMaster.objects.create(Temptoken=rno, Message=cMessage, Type="Reciever", UserId=uId)
                else:
                    uId=0
                    if request.session.get("userID"):
                        uId = request.session.get("userID")
                    cMessage = "Sorry! I have no answer about this."
                    TempChatMaster.objects.create(Temptoken=rno, Message=cMessage, Type="Reciever", UserId=uId)
            print("chat list")
            print(chats_list)
            return redirect('/home1/' + str(rno))
    else:
        #return render(request,'home.html',{"chats_list",chats_list})
        return render(request, 'home.html', {"chats_list": chats_list})
    

def home1(request,token):
    uid = request.session.get("userID")
    first_chat = (
        TempChatMaster.objects.filter(UserId=uid)
        .values('Temptoken').annotate(min_id=Min('id'))
    )
    chats_list = TempChatMaster.objects.filter(id__in=[chat['min_id'] for chat in first_chat])
    
    data = TempChatMaster.objects.filter(Temptoken=token).all()
    return render(request, 'home1.html',{"chatHistory":data, "chats_list":chats_list})

def logout(request):
    request.session.flush()
    return redirect("/home/")

def deletechat(request):
    if request.method == "POST":
        tknNo = request.POST.get('tknNo')
        TempChatMaster.objects.filter(Temptoken=tknNo).all().delete()
    return redirect("/home/")