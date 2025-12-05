from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('train/', views.train, name='train'),
    path('models/', views.model_list, name='model_list'),
    path('models/<int:model_id>/train-data/', views.model_train_data, name='model_train_data'),
    path('testmodel/', views.testmodel, name='testmodel'),
]
