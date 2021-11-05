from django.contrib import admin
from django.urls import path, include  # new

urlpatterns = [
    path("admin/", admin.site.urls),
    #path("", include("dobo_party.urls")),
    path("api", include("meme_generator.urls"))
]
