from django.urls import path
from .views import (
    BookListView, BookDetailView,    BookPdfDownloadView,
)

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('<int:pk>/download/', BookPdfDownloadView.as_view(), name='book_download'),
    # path('<int:pk>/rent/', RentalCreateView.as_view(), name='rental_create'),
    # path('<int:book_id>/queue/', queue_book, name='queue_book'),
    # path('queue/<int:queue_id>/status/', QueueStatusView.as_view(), name='queue_status'),
    # path('rental_confirmation/<int:rental_id>/', rental_confirmation, name='rental_confirmation'),
]
