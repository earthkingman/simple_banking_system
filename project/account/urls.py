from django.urls import path
from account.views import AccountView
urlpatterns = [
    path('account', AccountView.as_view()),
    # path('/<int:id>', views.detail, name = 'detail'),
    # path('/list', views.list, name = 'list')
]