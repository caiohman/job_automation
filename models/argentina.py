import os
import pdfplumber
import pandas as pd
import re
from decimal import ROUND_UP, Decimal

class Argentina():

    def __init__(self, pdf_directory, result_directory) -> None:
        self.taxes_order = [
            "(010)",
            "(011+061+041+051)",
            "(415)",
            "(422)",
            "(424)",
            "(500)",
            "(900)",
            "(417)"
        ]

        self.custom_broker = [
            "BASALDUA MARTIN JORGE",
            "MICUCCI OSVALDO ALFREDO",
            "MENDIETA ROSARIO RAMON",
            "RUSSO DANIEL OSCAR"
        ]

        pdf_files = [os.path.join(pdf_directory, f) for f in os.listdir(pdf_directory) if f.lower().endswith('.pdf')]
        result_excel_file = os.path.join(result_directory, "dados_extraidos_argentina.xlsx")

        data = []
        self.pdf_files_read_correctly = []
        self.pdf_files_not_read  = []

        for pdf_file in pdf_files:
            result = self.extract_data_from_pdf(pdf_file)
            if result :
                filename = os.path.basename(pdf_file)
                self.pdf_files_read_correctly.append(filename)
                data.extend(result)
                self.move_file_read_correctly(pdf_file, filename)
            else:
                self.pdf_files_not_read.append(os.path.basename(pdf_file))

        if self.pdf_files_read_correctly :
            self.save_to_excel(data, result_excel_file)

    def move_file_read_correctly(self, pdf_file, filename):
        new_directory = os.path.join(os.path.dirname(pdf_file), "files_read_correctly" )
        os.makedirs(new_directory , exist_ok = True)

        try:
            os.rename(pdf_file, os.path.join(new_directory, filename))
        except OSError as e:
            print(e)

    def extract_data_from_pdf(self, pdf_path) -> list :
        filename = os.path.basename(pdf_path).split(".")[0]
        extracted_data = []

        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[0]
            text = page.extract_text()

            if not text:
                return []

            order = self.order(text)
            date = self.date(text)
            cotiz = self.cotiz(text)
            taxes = self.taxes(text)
            aduana_value = self.aduana(text, taxes)

            if not aduana_value:
                return []

            custom_broker = self.find_custom_broker(text)
            char_block = filename.split("_")[0]

            data_row = {
                "Pedido": order,
                "Data": date,
                "Bloco Caracteres": char_block,
                "Cotiz": cotiz,
                "Valor Aduana": aduana_value,
                "Despachante": custom_broker
            }

            data_row.update(taxes)
            extracted_data.append(data_row)
            print("Impostos extraídos:", taxes)

        return extracted_data

    def taxes_sum(self, taxes) -> Decimal:
        try:
            aduana = Decimal(0).quantize(Decimal('0.01'), rounding=ROUND_UP)

            for key, value in taxes.items():
                aduana += value

            return aduana
        except ValueError as e:
            print(e)
        return Decimal(0).quantize(Decimal('0.01'), rounding=ROUND_UP)

    def order(self, text):
        order_match = re.search(r'\|\s*([\w\d/-]+)', text)
        return order_match.group(1).strip() if order_match else ""

    def date(self, text):
        date_match = re.search(r'\d{2}/\d{2}/\d{4}', text)
        date = date_match.group() if date_match else ""
        return date.replace("/", ".") if date else ""

    def cotiz(self, text):
        cotiz_match = re.search(r'Cotiz\s*=\s*([\d.,]+)', text)
        return cotiz_match.group(1) if cotiz_match else ""

    def aduana(self, text, taxes) -> Decimal | None:
        aduana = self.taxes_sum(taxes)
        formatted_number = f"{aduana:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return aduana if re.search(r'' + formatted_number + '', text) else None

    def taxes(self, text) -> dict:
        # MELHORIA: Nova expressão regular para capturar impostos
        taxes = {}
        # Padrão 1: (XXX) NOME DO IMPOSTO P VALOR
        tax_matches = re.findall(r'\(\s*(\d{3})\s*\)\s*([A-Za-z\s\.]*)\s*P\s*([\d.,]+)', text)
        # Padrão 2: (XXX) VALOR (quando o nome está em outra linha)
        tax_matches += re.findall(r'\(\s*(\d{3})\s*\)\s*([\d.,]+)', text)

        for match in tax_matches:
            # O padrão pode ter 2 ou 3 grupos (com ou sem nome do imposto)
            tax_code = match[0]

            if len(match) == 3:
                value = match[2]
                # tax_name, value = match[1], match[2]
            else:
                value = match[1]

            tax_title = f"({tax_code.strip()})"

            try:
                value = value.strip().replace('.', '').replace(',', '.')

                if value:
                    taxes[tax_title] = Decimal(value).quantize(Decimal('0.01'), rounding=ROUND_UP)
                else:
                    taxes[tax_title] = Decimal(0).quantize(Decimal('0.01'), rounding=ROUND_UP)

            except: # TODO: find suitable Excetion
                taxes[tax_title] = Decimal(0).quantize(Decimal('0.01'), rounding=ROUND_UP)

        # Verificação adicional para garantir que todos os impostos necessários existam
        required_taxes = ['(011)', '(061)', '(041)', '(051)']
        for tax in required_taxes:
            if tax not in taxes:
                taxes[tax] = Decimal(0).quantize(Decimal('0.01'), rounding=ROUND_UP)

        return taxes

    def find_custom_broker(self, text):
        custom_broker = ""

        for nome in self.custom_broker:

            if nome in text:
                custom_broker = nome
                break

        return custom_broker

    def save_to_excel(self, data, output_file):
        if not data:
            print("Nenhum dado para salvar.")
            return

        df = pd.DataFrame(data)

        # Somar os impostos (011) e (061) e criar uma nova coluna
        if any(col in df.columns for col in ["(011)", "(061)", "(041)", "(051)"]):
            # Converter as colunas para numérico, preenchendo valores inválidos com 0
            df["(011)"] = pd.to_numeric(df["(011)"], errors="coerce").fillna(0) if "(011)" in df.columns else 0
            df["(061)"] = pd.to_numeric(df["(061)"], errors="coerce").fillna(0) if "(061)" in df.columns else 0
            df["(041)"] = pd.to_numeric(df["(041)"], errors="coerce").fillna(0) if "(041)" in df.columns else 0
            df["(051)"] = pd.to_numeric(df["(051)"], errors="coerce").fillna(0) if "(051)" in df.columns else 0

            # Somar os valores das colunas (011), (061) e (041)
            df["(011+061+041+051)"] = df["(011)"] + df["(061)"] + df["(041)"] + df["(051)"]

            # Remover as colunas (011), (061) e (041) se existirem
            df.drop(columns=["(011)", "(061)", "(041)", "(051)"], inplace=True, errors="ignore")
        else:
            # Se nenhuma das colunas existir, criar a coluna (011+061+041) preenchida com 0
            df["(011+061+041+051)"] = 0

        # Reordenando as colunas dos impostos conforme a ordem fornecida

        # Padroniza os nomes das colunas para corresponder a impostos_ordem
        df.columns = [col.split()[0] if col.startswith("(") else col for col in df.columns]

        # Reindexação das colunas
        colunas_finais = ["Data", "Bloco Caracteres", "Cotiz"] + self.taxes_order + ["Valor Aduana", "Despachante"]
        df = df.reindex(columns=colunas_finais, fill_value="")

        # Adicionando a fórmula para calcular a análise
        df["Análise"] = df.index.map(lambda i: f"=L{i+2}-SOMA(D{i+2}:K{i+2})")

        df.to_excel(output_file, index=False)
        print(f"Dados salvos em {output_file}")

        print(df.head())  # Verificar primeiras linhas
        print("Colunas no DataFrame:", df.columns)
