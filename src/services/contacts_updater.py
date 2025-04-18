import pandas as pd


class ContactUpdater:
    def __init__(self, contacts_path, updated_path):
        self.contacts_path = contacts_path
        self.updated_path = updated_path

    def load_data(self):
        """Carrega o arquivo csv"""
        self.df_contacts = pd.read_csv(self.contacts_path)
        self.df_updated = pd.read_csv(self.updated_path)

    def get_novos_contatos(self):
        """
        Obtém os contatos novos da planilha updated a começar pelo último
        contato igual que há em ambas as planilhas
        """
        return self.df_updated[
            ~self.df_updated.iloc[:, 0].isin(self.df_contacts.iloc[:, 0])]

    def atualizar_contatos(self, novos_contatos):
        """Atualiza contacts com os contatos novos"""
        df_final = pd.concat(
            [self.df_contacts, novos_contatos], ignore_index=True)
        df_final.to_csv(self.contacts_path, index=False)
