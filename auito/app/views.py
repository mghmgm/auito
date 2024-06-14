from .models import Post, Ad, Car, Comment, Favorite
from .forms import LoginForm
from django.views import generic
from django.views.generic import FormView, UpdateView, DeleteView, CreateView
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render


class PostsView(generic.ListView):
    template_name = 'app/posts.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self):
        return Post.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")


class PostView(generic.DetailView):
    model = Post
    template_name = 'app/post.html'

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       post = self.get_object()
       user = self.request.user
       if user.is_authenticated:
           context['is_favorited'] = Favorite.objects.filter(user=user, post=post).exists()
       return context
     


class AdsView(generic.ListView):
    template_name = 'app/ads.html'
    context_object_name = 'latest_ad_list'

    def get_queryset(self):
        return Ad.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")
        

class AdView(generic.DetailView):
    model = Ad
    template_name = 'app/ad.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ad = self.object
        comments_list = Comment.objects.filter(ad=ad)
        context['comments_list'] = comments_list
        
        return context
    


class LoginView(FormView):
    template_name = 'app/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('app:posts')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, "Неверное имя пользователя или пароль")
            return self.form_invalid(form)


class ProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'app/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        cars_list = Car.objects.filter(owner=user)
        favorites_list = Favorite.objects.filter(user=user)

        context['user'] = user
        context['cars_list'] = cars_list
        context['favorites_list'] = favorites_list
        
        return context
    


class CreateAdView(CreateView):
    model = Ad
    fields = ['image', 'title', 'description']
    template_name = 'app/create.html'
    success_url = reverse_lazy('app:profile')

    def form_valid(self, form):
        form.instance.pub_date = timezone.now()  
        form.instance.author = self.request.user    
        car_id = self.kwargs['pk']
        car = Car.objects.get(pk=car_id)
        form.instance.car = car

        return super().form_valid(form)
    

class UpdateAdView(UpdateView):
    model = Ad
    fields = ['title', 'description', 'image']
    template_name = 'app/update.html'
    success_url = reverse_lazy('app:profile')
    

class DeleteAdView(DeleteView):
    model = Ad
    template_name = 'app/delete.html'
    success_url = reverse_lazy('app:profile')



def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('app:posts'))

def error_404_view(request, exception):
    return render(request, 'app/404.html')