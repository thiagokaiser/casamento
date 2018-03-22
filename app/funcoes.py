from datetime import date, timedelta
from io import StringIO, BytesIO
from .models import Pagamento
import xlsxwriter
from decimal import *


def funcao_data(i):
    array = []
    dt = date.today()
    array.append(dt)
    while i > 0:
        prev = dt.replace(day=1) - timedelta(days=1)
        dt = prev        
        array.append(prev)
        i = i - 1
    return array


def gera_excel(orcamentos):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)   

    # excel styles
    title = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'align': 'center',
        'valign': 'vcenter'
    })
    header = workbook.add_format({
        'bold': True,
        'bg_color': '#337ca5',
        'color': 'white',
        'align': 'center',
        'valign': 'top',
        'border': 1
    })
    cell = workbook.add_format({
        'align': 'left',
        'valign': 'top',
        'text_wrap': True,
        'border': 1
    })
    cell_center = workbook.add_format({
        'align': 'center',
        'valign': 'top',
        'border': 1
    })
    cell_valor = workbook.add_format({
        'num_format': 'R$ #,##0.00;[Red]R$ #,##0.00',
        'valign': 'top',
        'border': 1
    })

    for idx, orcamento in enumerate(orcamentos):
        worksheet_s = workbook.add_worksheet(orcamento.empresa)

        title_text = orcamento.empresa
        
        # merge cells
        worksheet_s.merge_range('A2:L2', title_text, title)

        # write header
        worksheet_s.write(3, 0, "Categoria", header)
        worksheet_s.write(3, 1, "Empresa", header)
        worksheet_s.write(3, 2, "Cidade", header)
        worksheet_s.write(3, 3, "Endereço", header)   
        worksheet_s.write(3, 4, "Contato", header)
        worksheet_s.write(3, 5, "Num Contato", header)
        worksheet_s.write(3, 6, "Valor Total", header)
        worksheet_s.write(3, 7, "Valor Saldo", header)   
        worksheet_s.write(3, 8, "Valor Multa", header)
        worksheet_s.write(3, 9, "Forma Pagto", header)
        worksheet_s.write(3, 10, "Dt Ult Pagto", header)
        worksheet_s.write(3, 11, "Dt Prox Reuniao", header)     


        row = 4
        
        worksheet_s.write_string(row, 0, orcamento.categoria.nome, cell)
        worksheet_s.write_string(row, 1, orcamento.empresa, cell)
        worksheet_s.write_string(row, 2, orcamento.cidade, cell)
        worksheet_s.write_string(row, 3, orcamento.endereço, cell)
        worksheet_s.write_string(row, 4, orcamento.nome_contato, cell)
        worksheet_s.write_string(row, 5, orcamento.num_contato, cell)
        
        worksheet_s.write_number(row, 6, Decimal(orcamento.valor_total or 0), cell_valor)     
        worksheet_s.write_number(row, 7, Decimal(orcamento.valor_saldo or 0), cell_valor)     
        worksheet_s.write_number(row, 8, Decimal(orcamento.valor_multa or 0), cell_valor)     

        worksheet_s.write_string(row, 9, orcamento.forma_pagto, cell)
        
        worksheet_s.write(row, 10, orcamento.dt_ult_pagto and orcamento.dt_ult_pagto.strftime('%d/%m/%Y'), cell_center)
        worksheet_s.write(row, 11, orcamento.dt_prox_reuniao and orcamento.dt_prox_reuniao.strftime('%d/%m/%Y'), cell_center)
     

        worksheet_s.merge_range('A7:D7', 'Pagamentos', title)
        # write header
        worksheet_s.write(7, 0, "Empresa", header)
        worksheet_s.write(7, 1, "Descricao", header)
        worksheet_s.write(7, 2, "Data", header)
        worksheet_s.write(7, 3, "Valor", header)        

        pagamentos = Pagamento.objects.filter(orcamento=orcamento.pk)

        # add data to the table
        for idx, data in enumerate(pagamentos):
            row = 8 + idx

            worksheet_s.write_string(row, 0, data.orcamento.empresa, cell)
            worksheet_s.write_string(row, 1, data.descricao, cell)
            worksheet_s.write(row, 2, data.dt_pagto.strftime('%d/%m/%Y'), cell_center)
            worksheet_s.write_number(row, 3, data.valor_pagto, cell_valor)        

            row = row + 1

        # change column widths
        worksheet_s.set_column('A:A', 15)  
        worksheet_s.set_column('B:B', 15)  
        worksheet_s.set_column('C:C', 15)          
        worksheet_s.set_column('D:D', 15)  
        worksheet_s.set_column('E:E', 15)  
        worksheet_s.set_column('F:F', 15)  
        worksheet_s.set_column('G:G', 15)  
        worksheet_s.set_column('H:H', 15)  
        worksheet_s.set_column('I:I', 15)          
        worksheet_s.set_column('J:J', 15)  
        worksheet_s.set_column('K:K', 15)  
        worksheet_s.set_column('L:L', 15)  
        
    

    # close workbook
    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data