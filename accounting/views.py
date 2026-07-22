from collections import defaultdict
from decimal import Decimal
from io import BytesIO

from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle

from .forms import TransactionForm
from .models import Category, Gst, Ledger, Transaction


def add_transaction(request):
    gst_amount = None
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save()
            rate = transaction.category.gst_percentage
            gst_amount = (transaction.amount * rate) / Decimal("100")
            Gst.objects.update_or_create(
                transaction=transaction,
                defaults={"gst_percentage": rate, "gst_amount": gst_amount},
            )
            last = Ledger.objects.order_by("-id").first()
            balance = last.current_balance if last else Decimal("0.00")
            balance = (
                balance + transaction.amount
                if transaction.type == "Income"
                else balance - transaction.amount
            )
            Ledger.objects.update_or_create(
                transaction=transaction,
                defaults={
                    "date": transaction.date,
                    "current_balance": balance,
                },
            )
            return redirect("add_transaction")
    else:
        form = TransactionForm()
    return render(
        request,
        "accounting/add_transaction.html",
        {"form": form, "gst_amount": gst_amount},
    )


def categorize_transactions(request):
    categories = Category.objects.all()
    if request.method == "POST":
        t = get_object_or_404(
            Transaction, id=request.POST.get("transaction_id")
        )
        c = get_object_or_404(Category, id=request.POST.get("category"))
        t.category = c
        t.save()
        return redirect("categorize_transactions")
    transactions = Transaction.objects.select_related("category").order_by(
        "-date"
    )
    return render(
        request,
        "accounting/categorize_transactions.html",
        {"transactions": transactions, "categories": categories},
    )


def generate_gst_bill(request, transaction_id):
    t = get_object_or_404(Transaction, id=transaction_id)
    g = get_object_or_404(Gst, transaction=t)
    buf = BytesIO()
    doc = SimpleDocTemplate(buf)
    styles = getSampleStyleSheet()
    total = t.amount + g.gst_amount
    data = [
        ["Description", t.description],
        ["Category", t.category.name],
        ["Amount", f"₹{t.amount:.2f}"],
        ["GST %", f"{g.gst_percentage}%"],
        ["GST Amount", f"₹{g.gst_amount:.2f}"],
        ["Total", f"₹{total:.2f}"],
    ]
    tbl = Table(data)
    tbl.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ]
        )
    )
    doc.build([Paragraph("GST Bill", styles["Title"]), tbl])
    buf.seek(0)
    return FileResponse(
        buf, as_attachment=True, filename=f"GST_Bill_{t.id}.pdf"
    )


def generate_total_gst_bill(request):
    tx = Transaction.objects.all()
    taxable = Decimal("0")
    gst = Decimal("0")
    for t in tx:
        gst_record = Gst.objects.filter(transaction=t).first()

        if gst_record:
            taxable += t.amount
            gst += gst_record.gst_amount
    total = taxable + gst
    buf = BytesIO()
    doc = SimpleDocTemplate(buf)
    styles = getSampleStyleSheet()
    tbl = Table(
        [
            ["Taxable", f"₹{taxable:.2f}"],
            ["GST", f"₹{gst:.2f}"],
            ["Grand Total", f"₹{total:.2f}"],
        ]
    )
    tbl.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 1, colors.black)]))
    doc.build([Paragraph("Total GST Bill", styles["Title"]), tbl])
    buf.seek(0)
    return FileResponse(
        buf, as_attachment=True, filename="Total_GST_Bill.pdf"
    )


def generate_gst_report(request):

    transactions = Transaction.objects.select_related("category")

    report = defaultdict(
        lambda: {
            "taxable": Decimal("0.00"),
            "gst": Decimal("0.00"),
        }
    )

    for transaction in transactions:

        gst = Gst.objects.filter(transaction=transaction).first()

        if not gst:
            continue

        category_name = (
            transaction.category.name
            if transaction.category
            else "Uncategorized"
        )

        report[category_name]["taxable"] += transaction.amount
        report[category_name]["gst"] += gst.gst_amount

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    data = [["Category", "Taxable Amount", "GST Amount"]]

    total_taxable = Decimal("0.00")
    total_gst = Decimal("0.00")

    for category_name, values in report.items():

        data.append(
            [
                category_name,
                f"₹ {values['taxable']:.2f}",
                f"₹ {values['gst']:.2f}",
            ]
        )

        total_taxable += values["taxable"]
        total_gst += values["gst"]

    data.append(
        [
            "TOTAL",
            f"₹ {total_taxable:.2f}",
            f"₹ {total_gst:.2f}",
        ]
    )

    table = Table(data)

    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("BACKGROUND", (0, -1), (-1, -1), colors.lightgrey),
            ]
        )
    )

    doc.build([Paragraph("GST Report", styles["Title"]), table])

    buffer.seek(0)

    return FileResponse(
        buffer, as_attachment=True, filename="GST_Report.pdf"
    )