
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls', namespace='accounts')),
    path('user/', include('adminapp.urls', namespace='adminapp')),
    path('venex_btc/', include('venexapp.urls', namespace='venexapp')),
]

admin.site.site_header = "Capital Finance Admin"
admin.site.site_title = "Capital Finance Admin Portal"
admin.site.index_title = "Welcome to Capital Finance Admin Portal"

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
