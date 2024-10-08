import json
import csv

class Dados:

    def __init__(self, path=None, tipo=None, dados=None):
        if dados is not None:
            self.dados = dados
        else:
            self.path = path
            self.tipo = tipo
            self.dados = self.leitura_dados()  # Carrega os dados ao inicializar
        
        self.nome_colunas = self.get_columns()
        self.qtd_linhas = self.size_data()

    def leitura_json(self):
        dados_json = []
        with open(self.path, 'r') as file:
            dados_json = json.load(file)
        return dados_json

    def leitura_csv(self):
        dados_csv = []
        with open(self.path, 'r') as file:
            spamreader = csv.DictReader(file, delimiter=',')
            for row in spamreader:
                dados_csv.append(row)
        return dados_csv

    def leitura_dados(self):
        if self.tipo == 'csv':
            return self.leitura_csv()
        elif self.tipo == 'json':
            return self.leitura_json()
        return []

    def get_columns(self):
        return list(self.dados[-1].keys())

    def rename_columns(self, key_mapping):
        new_dados = []
        for old_dict in self.dados:
            dict_temp = {}
            for old_key, value in old_dict.items():
                dict_temp[key_mapping.get(old_key, old_key)] = value  # Substitui a chave antiga pela nova
            new_dados.append(dict_temp)
        self.dados = new_dados
        self.nome_colunas = self.get_columns()

    def size_data(self):
        return len(self.dados)

    @staticmethod
    def join(dadosA, dadosB):
        combined_list = dadosA.dados + dadosB.dados  # Junta os dados
        return Dados(dados=combined_list)

    def transformando_dados_tabela(self):
        dados_combinados_tabela = [self.nome_colunas]
        for row in self.dados:
            linha = []
            for coluna in self.nome_colunas:
                linha.append(row.get(coluna, 'Indisponivel'))
            dados_combinados_tabela.append(linha)
        return dados_combinados_tabela

    def salvando_dados(self, path):
        dados_combinados_tabela = self.transformando_dados_tabela()
        with open(path, 'w') as file:
            writer = csv.writer(file)
            writer.writerows(dados_combinados_tabela)
