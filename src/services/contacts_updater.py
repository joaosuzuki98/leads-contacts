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
        Encontra o ID da segunda linha da planilha contacts.csv e pega todos os
        contatos acima desse ID na updated.csv.
        """
        if len(self.df_contacts) < 2:
            return pd.DataFrame()

        line2_id = self.df_contacts.iloc[1, 0]

        try:
            idx = self.df_updated[
                self.df_updated.iloc[:, 0] == line2_id].index[0]
        except IndexError:
            return pd.DataFrame()

        return self.df_updated.iloc[:idx]

    def atualizar_contatos(self, novos_contatos):
        """Atualiza contacts com os contatos novos"""
        line2_id = self.df_contacts.iloc[1, 0]

        try:
            idx_in_contacts = self.df_contacts[
                self.df_contacts.iloc[:, 0] == line2_id].index[0]
        except IndexError:
            idx_in_contacts = 1

        before = self.df_contacts.iloc[:idx_in_contacts]
        after = self.df_contacts.iloc[idx_in_contacts:]

        df_final = pd.concat(
            [before, novos_contatos, after], ignore_index=True)
        df_final.to_csv(self.contacts_path, index=False)
