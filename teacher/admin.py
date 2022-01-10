from django.contrib import admin
from . import models


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'room_number' )
    list_filter = ('last_name',)
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'room_number')
    ordering = ('first_name', 'last_name',)
    filter_horizontal = ('subjects_taught',)
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'room_number', 'profile_image', 'subjects_taught')
        }),
    )


admin.site.register(models.Teacher, TeacherAdmin)


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
    )


admin.site.register(models.Subject, SubjectAdmin)
