from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name="index"),
    # Classes
    path('classes', views.class_list_view, name="class_list"),
    path('classes/add', views.class_add, name="class_add"),
    path('classes/delete', views.class_delete, name="class_delete"),
    path('classes/change', views.class_change, name="class_change"),
    # Class Profiles
    path('class_profile', views.class_profile_list_view, name="class_profile_list"),
    path('class_profile/add', views.class_profile_add, name="class_profile_add"),
    path('class_profile/delete', views.class_profile_delete, name="class_profile_delete"),
    path('class_profile/change', views.class_profile_change, name="class_profile_change"),
    # Class Subjects
    path('class_subject/class/<int:id>', views.class_subject_list_view, name="class_subject_list"),
    path('class_subject/add', views.class_subject_add, name="class_subject_add"),
    path('class_subject/delete', views.class_subject_delete, name="class_subject_delete"),
    path('class_subject/change', views.class_subject_change, name="class_subject_change"),
    # Subjects
    path('subjects', views.subject_list_view, name="subject_list"),
    path('subjects/add', views.subject_add, name="subject_add"),
    path('subjects/delete', views.subject_delete, name="subject_delete"),
    path('subjects/change', views.subject_change, name="subject_change"),
    # Students
    path('students', views.student_list_view, name="student_list"),
    path('students/details/<int:id>', views.student_view, name="student"),
    path('students/add', views.student_add, name="student_add"),
    path('students/delete', views.student_delete, name="student_delete"),
    path('students/change', views.student_change, name="student_change"),
    # Teachers
    path('teachers', views.teacher_list_view, name="teacher_list"),
    path('teachers/details/<int:id>', views.teacher_view, name="teacher"),
    path('teachers/add', views.teacher_add, name="teacher_add"),
    path('teachers/delete', views.teacher_delete, name="teacher_delete"),
    path('teachers/change', views.teacher_change, name="teacher_change"),
    # Parents
    path('parents', views.parent_list_view, name="parent_list"),
    path('parents/details/<int:id>', views.parent_view, name="parent"),
    path('parents/add', views.parent_add, name="parent_add"),
    path('parents/delete', views.parent_delete, name="parent_delete"),
    path('parents/assign', views.parent_assign, name="parent_assign"),
    path('parents/assign/delete', views.parent_assign_delete, name="parent_assign_delete"),
    path('parents/change', views.parent_change, name="parent_change"),
    # Time Tables
    path('timetables', views.time_table_list_view, name="time_table_list"),
    path('timetables/details/<int:id>', views.time_table_view, name="time_table"),
    path('timetables/add', views.time_table_add, name="time_table_add"),
    path('timetables/delete', views.time_table_delete, name="time_table_delete"),
    path('timetables/change', views.time_table_change, name="time_table_change"),
    # Grades
    path('grades', views.grade_list_view, name="grade_list"),
    path('grades/student/<int:id>', views.grade_view, name="grade"),
    path('grades/class/<int:id>', views.grade_class_view, name="grade_class"),
    path('grades/add', views.grade_add, name='grade_add'),
    path('grades/delete', views.grade_delete, name='grade_delete'),
    path('grades/change', views.grade_change, name='grade_change'),
    # Attendance
    path('attendance', views.attendance_list_view, name="attendance_list"),
    path('attendance/student/<int:id>', views.attendance_view, name="attendance"),
    path('attendance/class/<int:id>', views.attendance_class_view, name="attendance_class"),
    path('attendance/add', views.attendance_add, name='attendance_add'),
    path('attendance/delete', views.attendance_delete, name='attendance_delete'),
    path('attendance/change', views.attendance_change, name='attendance_change'),
    # Messages
    path('message/list', views.message_list_view, name='message_list'),
    path('message/send', views.message_send, name='message_send'),
    path('messages', views.messages_view, name='messages'),
    # Authorization
    path('accounts/login/', views.login_view, name="login"),
    path('accounts/logout/', views.logout_view, name="logout")
]