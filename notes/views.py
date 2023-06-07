from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from notes.forms import * 
from django.views.generic.list import ListView
from django.core.exceptions import ValidationError
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse



# Create your views here.
def index(request):
    return render(request,'notes/login.html')

def register(request):
    if request.method == 'POST':
        a=request.POST.get('name')
        b=request.POST.get('username')
        c=request.POST.get('email')
        d=request.POST.get('password')
        e=request.POST.get('confirmpassword')
        if d==e:
            if Customer.objects.filter(username=b).exists():
                messages.info(request,"username already exists")
                return redirect("notes/register.html")
            elif Customer.objects.filter(email=c).exists():
                messages.info(request,"email already exists")
                return redirect("notes/register.html")
            else:
                user = Customer.objects.create(name=a,username=b,email=c,password=d)
                user.save()
                return redirect("http://127.0.0.1:8000/login")
        else:
            messages.info(request,"passwords do not match")
            return render(request,"notes/register.html")
    else:
        return render(request,"notes/register.html")


def login(request):
    if request.method == 'POST':
        u=request.POST.get('username')
        p=request.POST.get('password')
        log1 = Customer.objects.filter(username=u,password=p)
        if log1.filter(username=u, password=p).exists():
            for i in log1:
                x = i.username
                y = i.status
                request.session['username'] = u
                request.session['password'] = p
                if y == 'A':
                    return render(request, "notes/admin1.html")
                else:   
                    return render(request, "notes/user.html")
        else:
            return render(request, "notes/login.html")
    else:
        return render(request, "notes/login.html")
        
def user(request):
    return render(request,"notes/user.html") 
        
    
#crud of file
@login_required
def upload(request):
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            c=request.session["username"]
            cus=Customer.objects.get(username=c) 
            post.username = cus
            post.save()
            return redirect("uploaddash")
    else:
        form = PostForm()
    return render(request, 'notes/upload.html', {'form': form})

@login_required
def pdfedit(request, pk):
    c=request.session.get("username")
    cus = get_object_or_404(Customer, username=c)
    pdf = get_object_or_404(Post, pk=pk)
    if cus != pdf.username:  # check if the user owns the document
        
        return redirect('uploaddash')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=pdf)
        if form.is_valid():
            form.save()
            
            return redirect('uploaddash')
    else:
        form = PostForm(instance=pdf)
    return render(request, 'notes/pdfedit.html', {'form': form, 'pdf': pdf})

@login_required
def delete(request, pk):
    c=request.session.get("username")
    cus = get_object_or_404(Customer, username=c)
    pdf = get_object_or_404(Post, pk=pk)
    if cus == pdf.username:  # check if the user owns the document
        pdf.delete()
        
    return redirect('uploaddash')

def uploaddash(request):
    c=request.session["username"]
    cus=Customer.objects.get(username=c)
    details = Post.objects.filter(username=cus)
    return render(request,'notes/uploaddash.html', {'details': details})
def logouts(request):
    logout(request)
    return redirect('login')

def editprofile(request):
    # Get the current user object
    username = request.session.get('username')
    user = Customer.objects.get(username=username)

    if request.method == 'POST':
        # Update the user object with new data from the form
        user.name = request.POST.get('name', user.name)
        user.email = request.POST.get('email', user.email)
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            user.password = password
            user.confirmpassword = confirm_password
        else:
            return redirect('profilee')
        user.save()
        return render(request,"notes/user.html")
    else:
        # Render the edit profile form with the current user data
        context = {'user': user}
        return render(request, 'notes/profileedit.html', context)        
def profilee(request):
    return render(request,'notes/profileedit.html')


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'notes/post_detail.html', {'post': post})   

#search
def search(request):
    query = request.GET.get('query')
    results = []
    if query:
        results = Post.objects.filter(title__icontains=query)
    return render(request, 'notes/search.html', {'results': results})
#favorites
@login_required
def add_to_favorites(request, post_id):
    c=request.session.get("username")
    cus = get_object_or_404(Customer, username=c)
    post = get_object_or_404(Post, id=post_id)
    favorite, created = Favorite.objects.get_or_create(username=cus, post=post)
    if created:
        return render(request,'notes/popup.html')
    else:
        return render(request,'notes/popup1.html')
    print("errorr3")    
    return redirect(request.META.get('HTTP_REFERER'))
    
@login_required
def favorites(request):
    c=request.session["username"]
    cus=Customer.objects.get(username=c)
    favorites = Favorite.objects.filter(username=cus)
    return render(request, 'notes/favorites.html', {'favorites': favorites})

#courses crud
def upload_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save()
            messages.success(request, 'Course "{}" has been available'.format(course.name))
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'courses/courseupload.html', {'form': form})

def editcourse(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            course = form.save()
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/editcourse.html', {'form': form})

def deletecourse(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if request.method == 'POST':
        course.delete()
        return redirect('course_list')  # Assuming 'courses_list' is the name of the view to display the list of courses
    return render(request, 'courses/delete.html', {'course': course})

def course_list(request):
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'courses/courselist.html', context)

def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    context = {'course': course}
    return render(request, 'courses/coursedetail.html', context)

def coursedash(request):
    return render(request,'courses/coursedashboard.html')

#videos crud
def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('videos_list')
    else:
        form = VideoForm()
    return render(request, 'videos/uploadvideo.html', {'form': form})

def edit_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            return redirect('videos_list')
    else:
        form = VideoForm(instance=video)
    return render(request, 'videos/editvideo.html', {'form': form, 'video': video})
def delete_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.method == 'POST':
        video.delete()
        return redirect('videos_list')
    return render(request, 'videos/deletevideo.html', {'video': video})

def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    return render(request, 'videos/view_video.html', {'video': video})

def videos_list(request):
    videos = Video.objects.all()
    return render(request, 'videos/videodisplay.html', {'videos': videos})
#tags
def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'tags/display.html', {'tags': tags})

def tag_detail(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    return render(request, 'tags/detail.html', {'tag': tag})

def tag_create(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tag_list')
    else:
        form = TagForm()
    return render(request, 'tags/create.html', {'form': form})

def tag_update(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect('tag_list')
    else:
        form = TagForm(instance=tag)
    return render(request, 'tags/update.html', {'form': form, 'tag': tag})

def tag_delete(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    if request.method == 'POST':
        tag.delete()
        return redirect('tag_list')
    return render(request, 'tags/delete.html', {'tag': tag})


#prerequites
def prerequisite_list(request):
    prerequisite_objects = Prerequisite.objects.all()
    return render(request, 'prerequisites/display.html', {'prerequisite_objects': prerequisite_objects})

def prerequisite_detail(request, prerequisite_id):
    prerequisite_object = get_object_or_404(Prerequisite, id=prerequisite_id)
    return render(request, 'prerequisites/detail.html', {'prerequisite_object': prerequisite_object})

def prerequisite_create(request):
    if request.method == 'POST':
        form = PrerequisiteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('prerequisite_list')
    else:
        form = PrerequisiteForm()
    return render(request, 'prerequisites/create.html', {'form': form})

def prerequisite_update(request, prerequisite_id):
    prerequisite_object = get_object_or_404(Prerequisite, id=prerequisite_id)
    if request.method == 'POST':
        form = PrerequisiteForm(request.POST, instance=prerequisite_object)
        if form.is_valid():
            form.save()
            return redirect('prerequisite_list')
    else:
        form = PrerequisiteForm(instance=prerequisite_object)
    return render(request, 'prerequisites/update.html', {'form': form, 'prerequisite_object': prerequisite_object})

def prerequisite_delete(request, prerequisite_id):
    prerequisite_object = get_object_or_404(Prerequisite, id=prerequisite_id)
    if request.method == 'POST':
        prerequisite_object.delete()
        return redirect('prerequisite_list')
    return render(request, 'prerequisites/delete.html', {'prerequisite_object': prerequisite_object})

#learning
def learning_list(request):
    learning_objects = Learning.objects.all()
    return render(request, 'learning/display.html', {'learning_objects': learning_objects})

def learning_detail(request, learning_id):
    learning_object = get_object_or_404(Learning, id=learning_id)
    return render(request, 'learning/detail.html', {'learning_object': learning_object})

def learning_create(request):
    if request.method == 'POST':
        form = LearningForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_list')
    else:
        form = LearningForm()
    return render(request, 'learning/create.html', {'form': form})

def learning_update(request, learning_id):
    learning_object = get_object_or_404(Learning, id=learning_id)
    if request.method == 'POST':
        form = LearningForm(request.POST, instance=learning_object)
        if form.is_valid():
            form.save()
            return redirect('learning_list')
    else:
        form = LearningForm(instance=learning_object)
    return render(request, 'learning/update.html', {'form': form, 'learning_object': learning_object})

def learning_delete(request, learning_id):
    learning_object = get_object_or_404(Learning, id=learning_id)
    if request.method == 'POST':
        learning_object.delete()
        return redirect('learning_list')
    return render(request, 'learning/delete.html', {'learning_object': learning_object})
#admin dashboard
def admin1(request):
    return render(request,"notes/admin1.html")


#question



#usercourse
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.shortcuts import HttpResponse


class MyCoursesList(ListView):
    template_name = 'user/my_courses.html'
    context_object_name = 'user_courses'
    def get_queryset(self):
        c = self.request.session.get("username")
        cus=Customer.objects.get(username=c)
        user = cus
        return UserCourse.objects.filter(user = cus)


def coursePage(request , slug):
    course = Course.objects.get(slug  = slug)
    serial_number  = request.GET.get('lecture')
    videos = course.video_set.all().order_by("serial_number")

    if serial_number is None:
        serial_number = 1 

    video = Video.objects.get(serial_number = serial_number , course = course)

    if (video.is_preview is False):

        if request.user.is_authenticated is False:
            return redirect("login")
        else:
            c=request.session["username"]
            cus=Customer.objects.get(username=c)
            user=cus
            try:
                user_course = UserCourse.objects.get(user = cus , course = course)
            except:
                return  render(request , "user/check_out.html" , slug=course.slug )
    # Handle rating submission
    # Prepare the context with the rating form    
    context = {
        "course" : course , 
        "video" : video , 
        'videos':videos,
        
    }
    return  render(request , "user/course_page.html" , context=context )
#checkout.py
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from time import time
from study.settings import *
from notes.models import Course , Video , Payment , UserCourse,Customer
from django.shortcuts import HttpResponse
from time import time


import razorpay
client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))


@login_required(login_url='/login')
def checkout(request, slug):
    c = request.session["username"]
    cus = Customer.objects.get(username=c)
    course = Course.objects.get(slug=slug)
    user = cus
    action = request.GET.get('action')
    order = None
    payment = None
    error = None
    try:
        user_course = UserCourse.objects.get(user=user, course=course)
        error = "You are already enrolled in this course"
    except UserCourse.DoesNotExist:
        pass
    amount = None
    if error is None:
        amount = int((course.price - (course.price * course.discount * 0.01)) * 100)
    
    # If amount is zero, don't create payment, only save enrollment object
    if amount == 0:
        userCourse = UserCourse(user=user, course=course)
        userCourse.save()
        return render(request, 'user/my_courses.html')
    
    if action == 'create_payment':
        currency = "INR"
        notes = {
            "email": user.email,
            "name": f'{user.name}'
        }
        receipt = f"notes-{int(time())}"
        order = client.order.create(
            {
                'receipt': receipt,
                'notes': notes,
                'amount': amount,
                'currency': currency
            }
        )
        payment = Payment()
        payment.user = user
        payment.course = course
        payment.order_id = order.get('id')
        payment.save()

    context = {
        "course": course,
        "order": order,
        "payment": payment,
        "user": user,
        "error": error
    }
    return render(request, "user/check_out.html", context=context)
#verify payment
@csrf_exempt
def verifyPayment(request):
    if request.method == "POST":
        data = request.POST
        context = {}
        print(data)
        try:
            client.utility.verify_payment_signature(data)
            razorpay_order_id = data['razorpay_order_id']
            razorpay_payment_id = data['razorpay_payment_id']

            payment = Payment.objects.get(order_id = razorpay_order_id)
            payment.payment_id  = razorpay_payment_id
            payment.status =  True
            
            userCourse = UserCourse(user = payment.user , course = payment.course)
            userCourse.save()

            print("UserCourse" ,  userCourse.id)

            payment.user_course = userCourse
            payment.save()

            return redirect('my-courses')   

        except:
            return HttpResponse("Invalid Payment Details")            

#home.py
from notes.models import Course , Video , Payment , UserCourse,Customer
def home_page_view(request):
    courses = Course.objects.filter(active=True)
    context = {'courses': courses}
    return render(request, 'user/home.html', context)

#rating
from django.db.models import Avg
def course_detaill(request, course_id):
    course = Course.objects.get(id=course_id)
    ratings = Rating.objects.filter(Course=course)
    avg_rating = ratings.aggregate(Avg('rating')).get('rating__avg')

    context = {
        'course': course,
        'ratings': ratings,
        'avg_rating': avg_rating,
    }
    return render(request, 'rating/course_detail.html', context)

#notifications views
def notifications(request):
    messages.success(request, 'Notification message.')
    return render(request, 'notes/notification.html', {'notifications': notifications})
