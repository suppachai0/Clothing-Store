from django.contrib import admin
from django.urls import path, include  # ✅ ต้อง import path และ include

from django.conf import settings
from django.conf.urls.static import static  # ✅ ใช้สำหรับแสดงไฟล์ media

urlpatterns = [
    path('admin/', admin.site.urls),  # ✅ ตรวจสอบว่าเส้นทาง admin ถูกต้อง
    path('', include('clothing_store.urls')),  # ✅ ให้แน่ใจว่า clothing_store มี `urls.py`
]

# ✅ รองรับการแสดงผลไฟล์รูปภาพ (Media Files)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)