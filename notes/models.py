from django.db import models
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import User
from .validators import file_size
from django.utils.html import format_html






# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=80)
    username = models.CharField(max_length=80,primary_key=True)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    confirmpassword = models.CharField(max_length=40)
    status = models.CharField(max_length=10, default='U')

    def __str__(self):
        return self.username

#category class
class CategoryManager(models.Manager):
    def search(self, query):
        return self.get_queryset().filter(
            Q(title__icontains=query)
        )

class Category(models.Model):
    name = models.CharField(max_length=100,primary_key=True)
    
    objects = CategoryManager()
    
    def __str__(self):
        return self.name
    

#file upload class
class PostManager(models.Manager):
    def search(self, query):
        return self.get_queryset().filter(
            Q(title__icontains=query)
        )

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200,null=False)
    thumbnail=models.ImageField(upload_to='uploads/',null=True)
    pdf = models.FileField(upload_to="uploads/")
    desc = models.TextField()
    username = models.ForeignKey(Customer, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    
    objects = PostManager()
    
    
    def __str__(self):
        return f"{self.title}"
    
    
#favorites class
class Favorite(models.Model):
    username = models.ForeignKey(Customer, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
        
    
    def __str__(self):
        return f"{self.username} - {self.post.title}"


    

class Notification(models.Model):
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
 #courses   
class Course(models.Model):
    name = models.CharField(max_length = 50 , null = False)
    slug = models.CharField(max_length = 50 , null = False , unique = True)
    description = models.CharField(max_length = 200 , null = True)
    price = models.IntegerField(null=False)
    discount = models.IntegerField(null=False , default = 0) 
    active = models.BooleanField(default = False)
    thumbnail = models.ImageField(upload_to = 'uploads/') 
    date = models.DateTimeField(auto_now_add= True) 
    resource = models.FileField(upload_to = "resource/")
    length = models.IntegerField(null=False)

    def __str__(self):
        return self.name

    list_display = ["name" , 'get_price' , 'get_discount' , 'active']
    list_filter = ("discount" , 'active')

    def get_discount(self , course):
        return f'{course.discount} %'
    
    def get_price(self , course):
        return f'₹ {course.price}'
    
    get_discount.short_description= "Discount"
    get_price.short_description = "Price"

    

class Tag(models.Model):
    description  = models.CharField(max_length = 100 , null = False)
    course = models.ForeignKey(Course , null = False , on_delete=models.CASCADE)
   
class Prerequisite(models.Model):
    description  = models.CharField(max_length = 100 , null = False)
    course = models.ForeignKey(Course , null = False , on_delete=models.CASCADE)
    
class Learning(models.Model):
    description  = models.CharField(max_length = 100 , null = False)
    course = models.ForeignKey(Course , null = False , on_delete=models.CASCADE)
    
class Video(models.Model):
    title  = models.CharField(max_length = 100 , null = False)
    course = models.ForeignKey(Course , null = False , on_delete=models.CASCADE)
    serial_number = models.IntegerField(null=False)
    video = models.FileField(upload_to = "video/%y",validators=[file_size])
    is_preview = models.BooleanField(default = False)

    def __str__(self):
        return self.title

class UserCourse(models.Model):
    username = models.ForeignKey(User , null = False , on_delete=models.CASCADE)
    course = models.ForeignKey(Course , null = False , on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.username} - {self.course.name}'
    
    list_display = ['click' , 'get_user' , 'get_course'] 
    list_filter = ['course']

    def get_user(self , usercourse):
        return format_html(f"<a target='_blank' href='/admin/auth/user/{usercourse.user.id}'>{usercourse.user}</a>")
    
    def click(self , usercourse):
        return "Click to Open"
    

    def get_course(self , usercourse):
        return format_html(f"<a target='_blank' href='/admin/courses/course/{usercourse.course.id}'>{usercourse.course}</a>")

    get_course.short_description = "Course"
    get_user.short_description = "User"


class Payment(models.Model):
    order_id = models.CharField(max_length = 50 , null = False)
    payment_id = models.CharField(max_length = 50)
    user_course = models.ForeignKey(UserCourse , null = True , blank = True ,  on_delete=models.CASCADE)
    user = models.ForeignKey(User ,  on_delete=models.CASCADE)
    course = models.ForeignKey(Course , on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    
    list_display = [ "order_id" , 'get_user' , 'get_course' , 'status'] 
    list_filter = ["status" , 'course']

    def get_user(self , payment):
        return format_html(f"<a target='_blank' href='/admin/auth/user/{payment.user.id}'>{payment.user}</a>")
    

    def get_course(self , payment):
        return format_html(f"<a target='_blank' href='/admin/courses/course/{payment.course.id}'>{payment.course}</a>")

    get_course.short_description = "Course"
    get_user.short_description = "User"



#rating
class Rating(models.Model):
    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    Course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, '1 star'), (2, '2 stars'), (3, '3 stars'), (4, '4 stars'), (5, '5 stars')])

    class Meta:
        unique_together = ('Customer', 'Course')
