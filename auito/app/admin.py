from django.contrib import admin
from .models import User, Car, Ad, Post, Comment, Favorite


class AdInline(admin.TabularInline):
    model = Ad
    extra = 0

class CarInline(admin.TabularInline):
    model = Car
    extra = 0

class PostInline(admin.TabularInline):
    model = Post
    extra = 0

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class FavoriteInline(admin.TabularInline):
    model = Favorite
    extra = 0


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'last_login', 'is_staff', 'date_joined', 'is_superuser', 'password']
    list_display_links = ['username']
    inlines = [CarInline, AdInline, PostInline, CommentInline, FavoriteInline]  
    search_fields = ['username'] 
    readonly_fields = ['is_active'] 
    filter_horizontal = ['favorites']
     

class CarAdmin(admin.ModelAdmin):
    list_display = ['id', 'brand', 'model', 'mileage', 'body_type', 'power', 'price', 'owner']
    list_display_links = ['brand'] 
    list_filter = ['owner_id', 'brand']

    def owner(self, obj):
       return obj.owner.username


class AdAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'short_description', 'image', 'author', 'car_id', 'pub_date']
    list_filter = ['author_id']
    inlines = [CommentInline]  
    list_display_links = ['title'] 
    date_hierarchy = 'pub_date'  
    search_fields = ['title']
    raw_id_fields = ['car']  

    def author(self, obj):
       return obj.author.username

    @admin.display(description='Short Description')
    def short_description(self, obj):
        return obj.description[:80] + '...' if len(obj.description) > 80 else obj.description


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'short_description', 'image', 'author', 'pub_date']
    list_filter = ['author_id']
    list_display_links = ['title']
    search_fields = ['title']
    date_hierarchy = 'pub_date' 

    def author(self, obj):
       return obj.author.username
    
    @admin.display(description='Short Description')
    def short_description(self, obj):
        return obj.description[:80] + '...' if len(obj.description) > 80 else obj.description


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'author', 'ad_id', 'pub_date']
    list_filter = ['author_id'] 
    raw_id_fields = ['ad'] 
    list_display_links = ['text'] 
    date_hierarchy = 'pub_date'
    search_fields = ['text']
    readonly_fields = ['pub_date']

    def author(self, obj):
       return obj.author.username


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'post_id']
    raw_id_fields = ['post'] 
    list_filter = ['user_id', 'post_id']

    def username(self, obj):
       return obj.user.username


admin.site.register(User, UserAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Ad, AdAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Favorite, FavoriteAdmin)