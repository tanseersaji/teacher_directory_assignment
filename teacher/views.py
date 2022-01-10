from django import forms
from django.shortcuts import redirect, render
from . import models
from . import forms
import pandas as pd
from django.conf import settings
from django.core.files import File
from pathlib import Path
from django.contrib.auth.decorators import login_required


"""
    View to register a new user using default Django registration form.
"""

def register(request):
    if request.method == 'POST':
        form = forms.NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = forms.NewUserForm()
    return render(request, 'registration/register.html', {'form': form})


"""
    View definitions for the teacher app based on URL patterns.
"""

def all_teachers(request):
    """
        View to display all teachers.
    """

    teachers = models.Teacher.objects.all().order_by('last_name')
    no_teachers = len(teachers) == 0

    last_name = request.GET.get('last_name_filter', None)
    subjects_taught = request.GET.getlist('subjects_filter', None)

    if last_name:
        teachers = teachers.filter(last_name__istartswith=last_name)
    if subjects_taught:
        subjects_taught = [subject_name for subject_name in subjects_taught if subject_name != '']
        print(len(subjects_taught))
        if len(subjects_taught) != 0:
            teachers = teachers.filter(subjects_taught__name__in=subjects_taught)

    context = {
        'teachers': teachers,
        'no_teachers': no_teachers,
        'alphabet': [chr(i) for i in range(ord('A'), ord('Z') + 1)],
        'subjects': models.Subject.objects.all(),
        'last_name_filter': last_name,
        'subjects_filter': subjects_taught,
    }

    return render(request, 'teacher/all_teachers.html', context=context)


def teacher_details(request, teacher_id):
    """
        View to display details of a teacher.
    """

    teacher = models.Teacher.objects.get(id=teacher_id)
    context = {
        'teacher': teacher,
    }

    return render(request, 'teacher/detailed_teacher.html', context=context)


@login_required
def bulk_add_teachers(request):
    """
        View to bulk add teachers.
    """

    if request.method == 'POST':
        form = forms.BulkTeacherForm(request.POST, request.FILES)
        csv_file = request.FILES['csv_file']
        
        # Read the CSV file and create a list of dictionaries
        # with the data from each row.
        df = pd.read_csv(csv_file)
        df = df.dropna(axis=0)
        
        data = df.to_dict(orient='records')

        for row in data:
            try:
                # Create a new teacher object.
                teacher = models.Teacher()
                teacher.first_name = row['First Name']
                teacher.last_name = row['Last Name']
                teacher.email = row['Email Address']
                teacher.phone = row['Phone Number']
                teacher.room_number = row['Room Number']

                # Get profile picture from the teachers folder.
                # If the picture does not exist, leave teacher.profile_picture as None.
                
                profile_picture_name = row['Profile picture']
                profile_picture_path = Path.joinpath(settings.BASE_DIR, 'teachers', profile_picture_name)
                if Path.exists(profile_picture_path):
                    teacher.profile_image.save(
                        profile_picture_name, 
                        File(open(profile_picture_path, 'rb')))

                teacher.save()

                # Add the subjects taught by the teacher.
                subjects_taught_str = row['Subjects taught'].lower().split(',')
                subjects_taught_str = [subject.strip() for subject in subjects_taught_str]
                for subject_name in subjects_taught_str:
                    subject = models.Subject.objects.get_or_create(name=subject_name)[0]
                    teacher.subjects_taught.add(subject)
            except Exception as e:
                # Log that the teacher could not be added.
                print(e)
                pass
            
        return redirect('view_all_teachers')
    else:
        form = forms.BulkTeacherForm()

    return render(request, 'teacher/add_teachers.html', {'form': form}) 
