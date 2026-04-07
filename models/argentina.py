import os
import pdfplumber
import pandas as pd
import re
from decimal import ROUND_UP, Decimal

class Argentina():

    def __init__(self, pdf_directory, result_directory) -> None:
        self.custom_broker = [
            "BASALDUA MARTIN JORGE",
            "MICUCCI OSVALDO ALFREDO",
            "MENDIETA ROSARIO RAMON",
            "RUSSO DANIEL OSCAR"
        ]

        pdf_files = [os.path.join(pdf_directory, f) for f in os.listdir(pdf_directory) if f.lower().endswith('.pdf')]
        result_excel_file = os.path.join(result_directory, "dados_extraidos_argentina.xlsx")
        sap_excel_file = os.path.join(result_directory, "sap_argentina.xlsx")

        data = []
        self.pdf_files_read_correctly = []
        self.pdf_files_not_read  = []
        pdfs_read_correctly_quantity = 0

        for pdf_file in pdf_files:
            result = self.extract_data_from_pdf(pdf_file)
            if result :
                filename = os.path.basename(pdf_file)
                self.pdf_files_read_correctly.append(filename)
                data.extend(result)
                self.move_file_read_correctly(pdf_file, filename)
                pdfs_read_correctly_quantity += 1
            else:
                self.pdf_files_not_read.append(os.path.basename(pdf_file))

        if self.pdf_files_read_correctly :
            self.save_to_excel(data, result_excel_file, pdfs_read_correctly_quantity, sap_excel_file)

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
        return Decimal(
            cotiz_match.group(1).strip().replace('.', '').replace(',', '.')).quantize(Decimal('0.01'), rounding=ROUND_UP
        ) if cotiz_match else ""

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

    def save_to_excel(self, data, output_file, pdfs_read_correcty_quantity, sap_excel_file):
        df = self.create_dataframe_extract(data)
        sap_df = self.create_dataframe_sap(df, pdfs_read_correcty_quantity)

        df.to_excel(output_file, index=False)
        sap_df.to_excel(sap_excel_file, index=False)

    def create_dataframe_extract(self, data):
        taxes_order = [
            "(010)",
            "(011+061+041+051)",
            "(415)",
            "(422)",
            "(424)",
            "(500)",
            "(900)",
            "(417)"
        ]
        df = pd.DataFrame(data)

        if any(col in df.columns for col in ["(011)", "(061)", "(041)", "(051)"]):
            df["(011+061+041+051)"] = df["(011)"] + df["(061)"] + df["(041)"] + df["(051)"]
            df.drop(columns=["(011)", "(061)", "(041)", "(051)"], inplace=True, errors="ignore")
        else:
            df["(011+061+041+051)"] = 0

        df.columns = [col.split()[0] if col.startswith("(") else col for col in df.columns]
        colunas_finais = ["Data", "Bloco Caracteres", "Cotiz"] + taxes_order + ["Valor Aduana", "Despachante"]
        df = df.reindex(columns=colunas_finais, fill_value="")
        df["Análise"] = df.index.map(lambda i: f"=L{i+2}-SOMA(D{i+2}:K{i+2})")

        return df

    def create_dataframe_sap(self, df, pdfs_read_correcty_quantity):
        excel_rows = []

        for pdf in range(pdfs_read_correcty_quantity):
            cotiz = df["Cotiz"].iloc[pdf]
            tax_010 = df["(010)"].iloc[pdf] if not df["(010)"].iloc[pdf] == "" and not pd.isna(df["(010)"].iloc[pdf]) else 0
            tax_sum = df["(011+061+041+051)"].iloc[pdf] if not df["(011+061+041+051)"].iloc[pdf] == "" else 0
            tax_500 = df["(500)"].iloc[pdf] if not df["(500)"].iloc[pdf] == "" and not pd.isna(df["(500)"].iloc[pdf]) else 0
            derechos_importacion_010 = tax_010 * cotiz
            tasa_estadisticas = tax_sum * cotiz
            iva_415 = df["(415)"].iloc[pdf] * cotiz if not df["(415)"].iloc[pdf] == "" and not pd.isna(df["(415)"].iloc[pdf]) else 0
            iva_adicional_inscr_422 = df["(422)"].iloc[pdf] * cotiz if not df["(422)"].iloc[pdf] == "" and not pd.isna(df["(422)"].iloc[pdf]) else 0
            imp_a_las_ganancias_424 = df["(424)"].iloc[pdf] * cotiz if not df["(424)"].iloc[pdf] == "" and not pd.isna(df["(424)"].iloc[pdf]) else 0
            arancel_sim_impo_500 = tax_500 * cotiz
            ingresos_brutos_900 = df["(900)"].iloc[pdf] * cotiz if not df["(900)"].iloc[pdf] == "" and not pd.isna(df["(900)"].iloc[pdf]) else 0
            impuestos_internos_417 = df["(417)"].iloc[pdf] * cotiz if not df["(417)"].iloc[pdf] == "" and not pd.isna(df["(417)"].iloc[pdf]) else 0
            total_part = derechos_importacion_010 + tasa_estadisticas + iva_415 + iva_adicional_inscr_422
            total_part += imp_a_las_ganancias_424 + arancel_sim_impo_500 + ingresos_brutos_900 + impuestos_internos_417
            impuestos_column = []
            cta_mayor_column = []
            importe_moneda_column = []
            ind_impuestos_column = []
            tax_object_column = []
            total = [Decimal(total_part).quantize(Decimal('0.01'), rounding=ROUND_UP)]
            costos_indirectos = [Decimal(( tax_010 + tax_sum + tax_500 ) * cotiz).quantize(Decimal('0.01'), rounding=ROUND_UP)]
            custom_broker = [df["Despachante"].iloc[pdf]]
            name = [df["Bloco Caracteres"].iloc[pdf]]
            date = [df["Data"].iloc[pdf]]

            if iva_415 != 0:
                impuestos_column.append("( 415 ) I.V.A")
                cta_mayor_column.append("2500001")
                importe_moneda_column.append(Decimal(iva_415).quantize(Decimal('0.01'), rounding=ROUND_UP))
                ind_impuestos_column.append("C0")
                tax_object_column.append("IV04")

            if iva_adicional_inscr_422 != 0:
                impuestos_column.append("( 422 ) IVA ADICIONAL INSCR")
                cta_mayor_column.append("2500000")
                importe_moneda_column.append(Decimal(iva_adicional_inscr_422).quantize(Decimal('0.01'), rounding=ROUND_UP))
                ind_impuestos_column.append("C0")
                tax_object_column.append("")

            if ingresos_brutos_900 != 0:
                impuestos_column.append("( 900 ) INGRESOS BRUTOS")
                cta_mayor_column.append("2500007")
                importe_moneda_column.append(Decimal(ingresos_brutos_900).quantize(Decimal('0.01'), rounding=ROUND_UP))
                ind_impuestos_column.append("C0")
                tax_object_column.append("IB03")

            if imp_a_las_ganancias_424 != 0:
                impuestos_column.append("( 424 ) IMP. A LAS GANANCIAS")
                cta_mayor_column.append("2500011")
                importe_moneda_column.append(Decimal(imp_a_las_ganancias_424).quantize(Decimal('0.01'), rounding=ROUND_UP))
                ind_impuestos_column.append("C0")
                tax_object_column.append("RT03")

            if impuestos_internos_417 != 0:
                impuestos_column.append("( 417 ) IMPUESTOS INTERNOS")
                cta_mayor_column.append("2500001")
                importe_moneda_column.append(Decimal(impuestos_internos_417).quantize(Decimal('0.01'), rounding=ROUND_UP))
                ind_impuestos_column.append("C0")
                tax_object_column.append("IIC2")

            for i in range(1, len(impuestos_column)):
                total.append(Decimal('NaN'))
                costos_indirectos.append(Decimal('NaN'))
                custom_broker.append("")
                name.append("")
                date.append("")

            impuestos_column.append("")
            cta_mayor_column.append("")
            importe_moneda_column.append("")
            ind_impuestos_column.append("")
            tax_object_column.append("")
            total.append(Decimal('NaN'))
            costos_indirectos.append(Decimal('NaN'))
            custom_broker.append("")
            name.append("")
            date.append("")

            data_row = {
                "Impuestos": impuestos_column,
                "Cta Mayor (SAP)": cta_mayor_column,
                "Importe moneda doc.": importe_moneda_column ,
                "Ind. Impuestos": ind_impuestos_column,
                "Tax Object": tax_object_column,
                "Total": total,
                "Costos Indirectos":costos_indirectos,
                "Despachante": custom_broker,
                "Nome": name,
                "Data": date
            }

            excel_rows.append(data_row)

        sap_dataframe = pd.DataFrame(excel_rows)
        return sap_dataframe.explode(
            ["Impuestos", "Cta Mayor (SAP)", "Importe moneda doc.", "Ind. Impuestos", "Tax Object", "Total", "Costos Indirectos", "Despachante", "Nome", "Data"]
        )
