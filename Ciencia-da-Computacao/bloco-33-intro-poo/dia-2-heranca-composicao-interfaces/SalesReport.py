import json
import gzip
from zipfile import ZipFile
from csv import DictWriter
from abc import ABC, abstractmethod


class Compressor(ABC):
    def __init__(self, filepath="./"):
        self.filepath = filepath

    @abstractmethod
    def compress(self, file_name):
        raise NotImplementedError


class ZipCompressor(Compressor):
    FILE_PATH = "./"

    @classmethod
    def compress(cls, file_name):
        with ZipFile(cls.file_name + file_name + ".zip", "w") as zip_file:
            zip_file.write(file_name)


class GzCompressor(Compressor):
    @staticmethod
    def compress(file_name):
        with open(file_name, "rb") as content:
            with gzip.open(file_name + ".gz", "wb") as gzip_file:
                gzip_file.writelines(content)


class SalesReport(ABC):
    # Nossa classe agora espera *instâncias* de compressor como um parâmetro.
    # Temos um valor padrão para suportar o código que usava as SalesReport
    # sem parâmetros -- não precisa correr pra re-escrever nada ;)
    def __init__(self, export_file, compressor=GzCompressor()):
        self.export_file = export_file
        self.compressor = compressor

    def build(self):
        """Aqui colocamos a lógica para a entidade 'se criar',
        ou seja, criar um relatório imprimível. Por simplicidade,
        vamos omitir essa lógica nos exemplos!"""
        return [
            {"Coluna 1": "Dado 1", "Coluna 2": "Dado 2", "Coluna 3": "Dado 3"},
            {"Coluna 1": "Dado A", "Coluna 2": "Dado B", "Coluna 3": "Dado C"},
        ]

    # Aqui temos um atributo de classe!
    FILE_EXTENSION = ""

    def get_export_file_name(self):
        # Aqui usamos o atributo de classe
        # Vai fazer mais sentido nas classes herdeiras!
        return self.export_file + self.FILE_EXTENSION

    def compress(self):
        self.serialize()
        self.compressor.compress(self.get_export_file_name())

    @abstractmethod
    def serialize(self):
        raise NotImplementedError


class SalesReportJSON(SalesReport):
    # Nós não reimplementamos o get_export_file_name
    # mas como ele usa um atributo de classe pra pegar a extensão
    # só de redefinir o atributo já vamos conseguir mudar o resultado!
    FILE_EXTENSION = ".json"

    def serialize(self):
        with open(self.get_export_file_name(), "w") as file:
            json.dump(self.build(), file)


class SalesReportCSV(SalesReport):
    FILE_EXTENSION = ".csv"

    def serialize(self):
        with open(self.get_export_file_name() + ".csv", "w") as file:
            headers = ["Coluna 1", "Coluna 2", "Coluna 3"]
            csv_writer = DictWriter(file, headers)
            csv_writer.writeheader()
            for item in self.build():
                csv_writer.writerow(item)


# Para testar
# relatorio_de_vendas = SalesReportJSON("meu_relatorio")
# relatorio_de_vendas.serialize()

# relatorio_de_compras = SalesReportCSV("meu_relatorio")
# relatorio_de_compras.serialize()
# relatorio_de_compras.compress()

relatorio_de_compras = SalesReportJSON("meu_relatorio_1")
relatorio_de_vendas = SalesReportJSON("meu_relatorio_2", ZipCompressor())

relatorio_de_compras.compress()
relatorio_de_vendas.compress()
