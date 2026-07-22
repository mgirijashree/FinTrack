from django.urls import path
from . import views

urlpatterns = [

    # Add Transaction
    path(
        "add/",
        views.add_transaction,
        name="add_transaction",
    ),

    # Categorize Transactions
    path(
        "categorize/",
        views.categorize_transactions,
        name="categorize_transactions",
    ),

    # GST Report PDF
    path(
        "report/gst/",
        views.generate_gst_report,
        name="generate_gst_report",
    ),

    # Individual GST Bill
    path(
        "bill/<int:transaction_id>/",
        views.generate_gst_bill,
        name="generate_gst_bill",
    ),

    # Total GST Bill
    path(
        "bill/total/",
        views.generate_total_gst_bill,
        name="generate_total_gst_bill",
    ),

]