import json
from datetime import datetime

from app.excel.base import BaseXlsBlock


class Parameters(BaseXlsBlock):
    TITLE = "Выгрузка по клиенту "
    DATE = "Дата выгрузки"

    def writer_some_data(self):
        all_column = self.workbook.add_format(self.column_format)
        all_column.set_text_wrap()
        all_column.set_align("center")
        self.row += 1
        self.worksheet.write(self.row, self.col, self.DATE)
        self.col += 1
        formatted_date = datetime.now().strftime("%Y-%m-%d")
        self.worksheet.write(self.row, self.col, formatted_date, all_column)
        self.col -= 1
        self.row += 1

    def writer_header(self):
        self.TITLE += self.some_data["user"]
        hd = self.workbook.add_format(self.header_format)
        hd.set_text_wrap()
        hd.set_align("center")
        self.worksheet.write(self.row, self.col, self.TITLE, hd)


class Report(BaseXlsBlock):
    TITLE = "Клиент не создавал коротких ссылок"
    TITLE_REPORT = "Элемент "
    URL = "Оригинальная ссылка"
    SHORT_URL = "Короткая ссылка"
    COUNTER = "Количество переходов"
    DATA = "Дата создания"

    def writer_header(self):
        hd = self.workbook.add_format(self.header_format)
        hd.set_text_wrap()
        hd.set_align("center")
        self.row = 5
        self.worksheet.write(self.row, self.col, self.TITLE, hd)

    def writer_some_data(self):
        all_column = self.workbook.add_format(self.column_format)
        all_column.set_text_wrap()
        all_column.set_align("left")
        title_format = self.workbook.add_format(self.title_format)
        title2_format = self.workbook.add_format(self.title2_format)
        h2 = self.workbook.add_format(self.title2_format)
        h2.set_text_wrap()
        h2.set_align("center")
        report_data = json.loads(self.some_data["report"])
        for count, item in enumerate(report_data):
            self.TITLE_REPORT = f"Элемент {count+1}"
            self.worksheet.write(self.row, self.col, self.TITLE_REPORT, title_format)
            self.col += 1
            self.row += 1
            self.col -= 1
            self.worksheet.write(self.row, self.col, self.URL, title2_format)
            self.col += 1
            self.worksheet.write(self.row, self.col, str(item["url"]), all_column)
            self.col -= 1
            self.row += 1
            self.worksheet.write(self.row, self.col, self.SHORT_URL, title2_format)
            self.col += 1
            self.worksheet.write(self.row, self.col, str(item["short_url"]), all_column)
            self.col -= 1
            self.row += 1
            self.worksheet.write(self.row, self.col, self.COUNTER, title2_format)
            self.col += 1
            self.worksheet.write(self.row, self.col, str(item["counter"]), all_column)
            self.col -= 1
            self.row += 1
            self.worksheet.write(self.row, self.col, self.DATA, title2_format)
            self.col += 1
            self.worksheet.write(self.row, self.col, str(item["created_at"]), all_column)
            self.col -= 1
            self.row += 1
            self.row += 1
