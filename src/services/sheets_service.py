import gspread
from oauth2client.service_account import ServiceAccountCredentials


class SheetsService:
    def __init__(self, credentials_path, spreadsheet_name, worksheet_name):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            str(credentials_path), scope
        )
        client = gspread.authorize(creds)
        self.worksheet = client.open(spreadsheet_name).worksheet(
            worksheet_name
        )

    def append_numbers_and_dates(self, number, dates, campaign):
        """
        Adiciona o número de telefone, a data e a campanha à planilha do
        Google Sheets
        """
        start_row = len(self.worksheet.col_values(1)) + 1
        valores = list(zip(number, dates, campaign))
        end_row = start_row + len(valores) - 1
        cell_range = f'A{start_row}:C{end_row}'
        self.worksheet.update(cell_range, valores)
