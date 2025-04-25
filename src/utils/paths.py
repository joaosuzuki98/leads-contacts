from pathlib import Path


def get_paths(sheets_credential_file):
    base = Path(__file__).resolve().parent.parent.parent / 'storage'
    contacts_path = base / 'contacts' / 'contacts.csv'
    updated_path = base / 'contacts' / 'updated.csv'
    credentials_path = base / 'credentials' / sheets_credential_file
    backup_path = base / 'backup'
    return contacts_path, updated_path, credentials_path, backup_path
