BATALHA NAVAL - TODO

Feito:
[✓] verificar sobreposição dos submarinos
[✓] verificar colisões de todas as peças
[✓] COLISÃO DO L14
[✓] calcular erros
[✓] desenhar navios que têm código "V"
[✓] arrumar formato do resultado: 

A Fazer: 
[x] calcular caso dos 5 pontos 
[x] formatar as mensagens de erro
[x] validar número de torpedos (?)


A linha que representa os torpedos a serem disparados deverá ser lida e para 
cada posição que representa o ponto onde o torpedo será direcionado, o 
sistema deverá analisar se o adversário possui algum navio na posição. Se o 
alvo na posição for abatido parcialmente, deverá ser somado ao jogar 3 pontos
por parte acertada. Caso o alvo seja destruído integralmente, deverá ser 
somado ao jogador 5 pontos adicionais às partes já acertadas. Caso nenhum 
alvo seja acertado, nada deve ser computado.


Torpedos J1:
T;A1|A2|B1|B2|C1|C2|D1|D2|E1|E2|F1|F2|G1|G2|H1|H2|I1|I2|J1|J2|K1|K2|L1|L2|M1

Torpedos J2:
T;N1|N2|O1|O2|A1|A2|B1|B2|C1|C2|O1|O2|D1|D2|E1|E2|F1|F2|G1|G2|H1|H2|I1|I2|J1


```

{'1': ['A2V', 'C7H', 'E1V', 'G3H', 'I7V'],
'2': ['H5H', 'L10V'],
'3': ['O5', 'M7', 'M9', 'J4', 'G10', 'O13', 'O2', 'D12', 'K14', 'I15'],
'4': ['J10H', 'J14V', 'D13H', 'B2H', 'B10V']}


```

========================================================================
Código:


def ship_sunk(board, ship_code, target):
    """ Checks if all the squares occupied by the ship were hit. """
    row = target[0]             # Letra da coordenada
    col = int(target[1:]) - 1   # Número da coordenada

    if ship_code == "3":  # Submarine == 1 position
        print("You sunk a submarine!")
        return True

    if ship_code == "1":  # Battleship == 4 positions
        count = 1
        for i in range(4):
            # Conferindo casas à direita
            if "*" in board[row][col + i]:
                print(f"conferindo coordenada: {row}{col + 1}")
                count += 1
        if count >= 4:
            print("You sunk a battleship!")
            return True

    if ship_code == "2":  # Carrier == 5 positions
        count = 0
        for i in range(3):
            if board[row][col + i] == 'X':
                count += 1
        if count == 3:
            print("You sunk a carrier!")
            return True

    if ship_code == "4":  # Cruiser == 2 positions
        count = 0
        for i in range(2):
            if board[row][col + i] == 'X':
                count += 1
        if count == 4:
            print("You sunk a cruiser!")
            return True

    return False