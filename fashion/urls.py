from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('page/<int:page_id>', views.index, name='home'),
    path('', views.page, name='index'),
    path('detail/<int:clothes_id>/', views.detail, name='detail'),
    path('success/url', views.index, name='index'),
    path('clothes', views.clothes, name='clothes'),
    path('login', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('<int:user_id>', views.profile, name='profile'),
    path('signup', views.signup, name='signup')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
