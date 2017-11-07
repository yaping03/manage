from django.shortcuts import render,redirect,HttpResponse
from myapp.models import Book,Author,Publish,AuthorDetail,Authlog
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def login_req(func):
    def inner(req,*args):
        auth = req.session.get("login", None)
        if auth:
            return func(req,*args)
        else:
            return redirect("/")
    return inner



# Create your views here.
@login_req
def book(req):
    obj = Book.objects.all()
    paginator = Paginator(obj,3)
    page_range = paginator.page_range
    num = req.GET.get("page", 1)
    obj = paginator.page(num)
    num = int(num)
    if paginator.num_pages>10:
        if num<6:
            page_range=range(1,10)
        elif num+5>paginator.num_pages:
            page_range=range(paginator.num_pages-8,paginator.num_pages+1)
        else:
            page_range=range(num-4,num+5)


    author_obj = Author.objects.all()
    pub_obj = Publish.objects.all()
    # authors = Author.objects.all().first()
    # lis = []
    # for i in range(100):
    #     book_obj = Book.objects.create(title="book"+str(i), publishDate='2016-10-15',
    #                                    price=66, publish_id=3)
    #     book_obj.authors.add(authors)
    if req.method=="POST":
        publish_obj = Publish.objects.filter(name=req.POST["publish"])[0]
        author_list = []
        for name in req.POST.getlist('author'):
            author_list.append(Author.objects.filter(name=name)[0])
        book_obj = Book.objects.create(title=req.POST["title"],publishDate = req.POST["publishDate"],price=req.POST["price"],publish=publish_obj)
        book_obj.authors.add(*author_list)
    return render(req,"book.html",locals())

@login_req
def author(req):
    obj = Author.objects.all()
    if req.method=="POST":
        detial_obj = AuthorDetail.objects.create(birthday=req.POST["birthday"], telephone=req.POST["telephone"], addr=req.POST["addr"])
        Author.objects.create(name=req.POST["name"],age = req.POST["age"],authorDetail=detial_obj)
    return render(req, "author.html",locals())
@login_req
def publishhouse(req):
    obj = Publish.objects.all()
    if req.method=="POST":
        Publish.objects.create(name=req.POST["name"],city = req.POST["city"],email=req.POST["email"])
    return render(req, "publishhouse.html", locals())

pro_dic = {"book":Book,"author":Author,"publish":Publish}
@login_req
def the_del(req,pro,id):
    pro_dic[pro].objects.filter(nid=id).delete()
    return redirect("/%s/"%pro)
@login_req
def the_edit_book(req,id):
    obj = Book.objects.get(nid=id)
    author_obj = Author.objects.all()
    pub_obj = Publish.objects.all()
    if req.method=="POST":
        publish_obj = Publish.objects.get(name=req.POST.get("publish"))
        Book.objects.filter(nid=id).update(title=req.POST["title"],publishDate=req.POST["publishDate"],price=req.POST["price"],publish=publish_obj)
        obj.authors.clear()
        author_list = []
        for name in req.POST.getlist("author"):
            author_list.append(Author.objects.get(name=name))
        obj.authors.add(*author_list)
        return redirect("/book/")
    return render(req, "editbook.html", locals())
@login_req
def the_edit_author(req,id):
    obj = Author.objects.get(nid=id)
    if req.method == "POST":
        # obj.authorDetail.objects.update(birthday=req.POST["birthday"],telephone=req.POST["telephone"],addr=req.POST["addr"])
        Author.objects.filter(nid=id).update(name=req.POST["name"],age=req.POST["age"])
        obj.authorDetail.birthday=req.POST["birthday"]
        obj.authorDetail.telephone=req.POST["telephone"]
        obj.authorDetail.addr=req.POST["addr"]
        obj.authorDetail.save()
        return redirect("/author/")
    return render(req, "editauthor.html", locals())
@login_req
def the_edit_publish(req,id):
    obj = Publish.objects.get(nid=id)
    if req.method == "POST":
        Publish.objects.filter(nid=id).update(name=req.POST["name"],city=req.POST["city"],email=req.POST["email"])
        return redirect("/publish/")
    return render(req, "editpublish.html", locals())

def login(request):
    state = ""
    if request.method=="POST":
        username = request.POST['user']
        password = request.POST['pwd']
        auth = Authlog.objects.filter(user=username,pwd=password)
        if auth:
            request.session["login"]=True
            request.session["user"]=username
            return redirect("/home")
        else:
            state = "用户名或密码错误"
    return render(request,"login.html",locals())

def regist(request):
    state = ''
    if request.method == 'POST':
        password = request.POST.get('pwd', '')
        username = request.POST.get('user', '')
        if Authlog.objects.filter(user=username):
            state = '用户已存在'
        else:
            new_user =Authlog.objects.create(user=username, pwd=password)
            return redirect('/')
    content = {
        'state': state,
        'user': None,
    }
    return render(request, 'regist.html',content)

@login_req
def home(request):
    user = request.session.get("user")
    return render(request,"home.html",locals())

@login_req
def blog(req):
    user = req.session.get("user")
    return render(req, "blog.html", locals())
