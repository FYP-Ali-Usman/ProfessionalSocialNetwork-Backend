from django.contrib import admin
from .models import Profile
from .forms import ProfileForm

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','phone','image','typeOf','organization','about']
    form = ProfileForm
    # class Meta:
    #     # model = Status



admin.site.register(Profile, ProfileAdmin)