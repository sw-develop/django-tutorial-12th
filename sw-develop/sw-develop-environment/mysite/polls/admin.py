from django.contrib import admin

#관리 사이트에서 polls app을 변경 가능하도록 만들기
from .models import Question

admin.site.register(Question)

# Register your models here.
