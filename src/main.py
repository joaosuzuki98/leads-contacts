import os
from dotenv import load_dotenv
from services.sendpulse_service import SendPulseService
from services.sheets_service import SheetsService
from services.contacts_updater import ContactUpdater
from utils.paths import get_paths

load_dotenv()

CLIENT_ID = os.getenv('SENDPULSE_ID')
CLIENT_SECRET = os.getenv('SENDPULSE_SECRET')
SHEETS_CREDENTIALS = os.getenv('SHEETS_CREDENTIALS')

contacts_path, updated_path, credentials_path = get_paths(SHEETS_CREDENTIALS)

sendpulse = SendPulseService(CLIENT_ID, CLIENT_SECRET)
sheets = SheetsService(credentials_path, 'Leads CFI AI', 'Página1')
updater = ContactUpdater(contacts_path, updated_path)

updater.load_data()
novos_contatos = updater.get_novos_contatos()

if novos_contatos.empty:
    print("Nenhuma nova linha para adicionar.")
else:
    source_urls = [
        sendpulse.get_source_url(cid) for cid in novos_contatos.iloc[:, 0]]
    novos_contatos = novos_contatos.copy()
    novos_contatos['campanha'] = source_urls
    updater.atualizar_contatos(novos_contatos)
    sheets.append_numbers_and_dates(
        novos_contatos.iloc[:, 1].astype(str).tolist(),
        novos_contatos.iloc[:, 5].astype(str).tolist()
    )
    print(f"{len(novos_contatos)} novas linhas adicionadas e sincronizadas.")
