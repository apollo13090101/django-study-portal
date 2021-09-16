from django.urls import path

from dashboard import views

urlpatterns = [
    path('', views.index, name="index"),
    path('home/', views.home, name="home"),

    path('profile/', views.profile, name="profile"),
    path('change_password/', views.change_password, name="change_password"),
    path('login/', views.signin, name="login"),
    path('logout/', views.signout, name="logout"),
    path('register/', views.register, name="register"),

    # Notes
    path('notes/', views.notes, name="notes"),
#     path('notes/<str:pk>/', views.NoteDetail.as_view(), name="note_detail"),
    path('notes/<str:pk>/', views.note_detail, name="note_detail"),
    path('delete_note/<str:pk>/', views.delete_note, name="delete_note"),

    # Homeworks
    path('homeworks/', views.homeworks, name="homeworks"),
    path('update_homework/<str:pk>/',
         views.update_homework, name="update_homework"),
    path('delete_homework/<str:pk>/',
         views.delete_homework, name="delete_homework"),

    # Youtube
    path('youtube/', views.youtube, name="youtube"),

    # Todo
    path('todo/', views.todo, name="todo"),
    path('update_todo/<str:pk>/', views.update_todo, name="update_todo"),
    path('delete_todo/<str:pk>/', views.delete_todo, name="delete_todo"),
    
    # Books
    path('books/', views.books, name="books"),
    
    # Dictionary
    path('dictionary/', views.dictionary, name="dictionary"),
    
    # Wikipedia
    path('wiki/', views.wiki, name="wiki"),
    
    # Converter
    path('converter/', views.converter, name="converter"),
    path('converter/unit-converter/', views.unit_converter, name="unit_converter"),
    path('converter/number-converter/', views.number_converter, name="number_converter"),
    path('converter/morse-converter/', views.morse_converter, name="morse_converter"),
    path('converter/currency-converter/', views.currency_converter, name="currency_converter"),
]
