import xlsxwriter

from app.excel.block import Parameters, Report


class XlsAnalyticPaymentWriter:

    ANALYTICS_BLOCKS_CLASSES = [Parameters, Report]

    def __init__(self, some_data):
        self.data = some_data
        self.position = 0

    def writer(self, write_file):
        workbook = xlsxwriter.Workbook(write_file)
        worksheet = workbook.add_worksheet()
        worksheet.set_column("A:A", 50)
        worksheet.set_column("B:B", 50)
        row = 0
        col = 0
        for items in self.ANALYTICS_BLOCKS_CLASSES:
            item_init = items(workbook, worksheet, row, col, self.data)
            item_init.writer_header()
            item_init.writer_some_data()
        workbook.close()
