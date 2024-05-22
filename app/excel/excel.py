import os
from datetime import datetime

from app.excel.writer import XlsAnalyticPaymentWriter


def set_exel_report(email, short_user):
    write_file = f"{email}_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
    reports_dir = os.path.join(os.getcwd(), "reports")

    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    full_path = os.path.join(reports_dir, write_file)
    some_data = {"user": email, "report": short_user}
    analytic_writer = XlsAnalyticPaymentWriter(some_data)
    analytic_writer.writer(full_path)

    return write_file
