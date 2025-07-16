def converter_pedidos_para_dicionario(pedidos_tuplas):
    pedidos = []
    for p_tuple in pedidos_tuplas:
        pedido_dict = {
            'id': p_tuple[0],
            'id_morador': p_tuple[1],
            'casa': p_tuple[2],
            'local': p_tuple[3],
            'categoria': p_tuple[4],
            'quarto': p_tuple[5],
            'ala': p_tuple[6],
            'descricao': p_tuple[7],
            'comentario_gestor': p_tuple[8],
            'status': p_tuple[9],
            'data_criacao': p_tuple[10].strftime('%d/%m/%Y %H:%M:%S'),
            'nome_morador': p_tuple[11] if len(p_tuple) > 11 else 'Não encontrado'
        }
        pedidos.append(pedido_dict)
    return pedidos