# Constants for ship sizes
SHIP_SIZES = {
    '1': 4,
    '2': 5,
    '3': 1,
    '4': 2
}

def read_and_validate_player_file(filename, player_id):
    try:
        with open(filename, 'r') as file:
            lines = file.read().splitlines()
    except FileNotFoundError:
        return f"Erro: Arquivo do Jogador {player_id} não encontrado"

    pieces = {'1': [], '2': [], '3': [], '4': []}
    torpedos = []
    is_torpedo_section = False

    for line in lines:
        if line.startswith("# Jogada"):
            is_torpedo_section = True
            continue

        if not is_torpedo_section and line[0].isdigit():
            code, piece_positions_data = line.split(';')
            piece_positions = piece_positions_data.split('|')
            pieces[code].extend(piece_positions)
        elif is_torpedo_section and line.startswith("T;"):
            torpedo_positions = line.split(';')[1].split('|')
            torpedos.extend(torpedo_positions)

    return pieces, torpedos

def calculate_all_squares(square, ship_size):
    letter = square[0]
    number = int(square[1:-1]) #A1
    orientation = square[-1]

    squares = []

    if orientation == "V":
        for i in range(ship_size):
            new_square = letter + str(number + i) + orientation
            squares.append(new_square)
    elif orientation == "H":
        for i in range(ship_size):
            new_square = f"{chr(ord(letter) + i)}{number}{orientation}"
            squares.append(new_square)

    return squares

def validate_piece_positions(pieces):
    for code, piece_positions in pieces.items():
        for position in piece_positions:
            if code == '3':
                if len(position) != 2 and len(position) != 3:
                    return f"Erro: Posição do submarino inválida encontrada: {position}"
            else:
                if len(position) < 3 or len(position) > 4 or position[0] not in "ABCDEFGHIJKLMNO" or int(position[1:-1]) < 1 or int(position[1:-1]) > 15:
                    return f"Erro: Posição da peça inválida encontrada: {position}"
                if position[-1] not in "VH":
                    return f"Erro: Orientação da peça inválida encontrada: {position}"
    return True

def validate_piece_overlap(pieces):
    occupied_positions = set()

    # 1;A2V|C7H|E1V|G3H|I7V
    for code, piece_positions in pieces.items():
        if code != "3":
            ship_size = SHIP_SIZES[code]
            for square in piece_positions:
                # letter = square[0]
                # number = square[1:-1]
                # direction = square[-1]
                squares = calculate_all_squares(square, ship_size)
                for square in squares:
                    if square in occupied_positions:
                        return f"Erro: Peças se sobrepõem na posição {square}"
                    occupied_positions.add(square)
    return True

def validate_torpedo_positions(torpedos):
    for torpedo in torpedos:
        if len(torpedo) != 2 or torpedo[0] not in "ABCDEFGHIJKLM" or not torpedo[1].isdigit():
            return f"Erro: Posição de torpedo inválida encontrada: {torpedo}"
    return True


def calculate_score(board, torpedo_targets):
    score = 0
    for target in torpedo_targets:
        col, row = target[:-1], int(target[-1])
        if board[col][row - 1] != ' ':
            score += 3
            board[col][row - 1] = ' '  # Update the list element to ' ' to clear the hit position
    return score


def batalha_naval(jogador1_file, jogador2_file):
    jogador1_pieces, jogador1_torpedos = read_and_validate_player_file(jogador1_file, 1)
    jogador2_pieces, jogador2_torpedos = read_and_validate_player_file(jogador2_file, 2)

    validation_error = validate_piece_positions(jogador1_pieces)
    if validation_error != True:
        return f"J1 {validation_error} ID_GANHADOR ERRO_DE_VALIDACAO1"

    validation_error = validate_piece_positions(jogador2_pieces)
    if validation_error != True:
        return f"J2 {validation_error} ID_GANHADOR ERRO_DE_VALIDACAO2"

    validation_error = validate_piece_overlap(jogador1_pieces)
    if validation_error != True:
        return f"J1 {validation_error} ID_GANHADOR ERRO_DE_VALIDACAO3"

    validation_error = validate_piece_overlap(jogador2_pieces)
    if validation_error != True:
        return f"J2 {validation_error} ID_GANHADOR ERRO_DE_VALIDACAO4"

    board_jogador1 = {chr(ord('A') + i): [' '] * 15 for i in range(15)}
    board_jogador2 = {chr(ord('A') + i): [' '] * 15 for i in range(15)}
    torpedo_targets_jogador1 = []
    torpedo_targets_jogador2 = []

    for piece in jogador1_pieces.items():
        code = piece[0]
        piece_positions_data = piece[1]
        ship_size = SHIP_SIZES[code]
        for position in piece_positions_data:
            if len(position) > 2:
                col = position[0]
                row = int(position[1:-1])
                direction = position[-1]

                if direction == 'H':
                    if chr(ord(col) + ship_size - 1) > 'O':
                        return f"J1 {validation_error} {chr(ord(col) + ship_size - 1) } DEU RUIM"
                    board_jogador1[col][row - 1: row - 1 + ship_size] = ['X'] * ship_size
                elif position == "V":
                    for i in range(ship_size):
                        print(f"Limite vertical: {chr(ord(col) + i)}")
                        board_jogador1[chr(ord(col) + i)][row - 1] = 'X'

    for piece in jogador2_pieces.items():
        code = piece[0]
        piece_positions_data = piece[1]
        ship_size = SHIP_SIZES[code]
        for position in piece_positions_data:
            if len(position) > 2:
                col = position[0]
                row = int(position[1:-1])
                direction = position[-1]

                if direction == 'H':
                    if chr(ord(col) + ship_size - 1) > 'O':
                        return f"J2 {validation_error} {chr(ord(col) + ship_size - 1) } DEU RUIM"
                    board_jogador2[col][row - 1: row - 1 + ship_size] = ['X'] * ship_size
                elif position == "V":
                    for i in range(ship_size):
                        board_jogador2[chr(ord(col) + i)][row - 1] = 'X'

    for torpedo in jogador1_torpedos:
        if torpedo not in torpedo_targets_jogador1:
            torpedo_targets_jogador1.append(torpedo)

    for torpedo in jogador2_torpedos:
        if torpedo not in torpedo_targets_jogador2:
            torpedo_targets_jogador2.append(torpedo)

    score_jogador1 = calculate_score(board_jogador1, torpedo_targets_jogador1)
    score_jogador2 = calculate_score(board_jogador2, torpedo_targets_jogador2)

    if score_jogador1 == score_jogador2:
        return f"J1 {score_jogador1} J2 {score_jogador2} EMPATE"
    elif score_jogador1 > score_jogador2:
        return f"J1 {score_jogador1} J2 {score_jogador2} J1"
    else:
        return f"J1 {score_jogador1} J2 {score_jogador2} J2"

#=============================================================
#                           TESTES
#=============================================================
    # Calculate the total number of hits and misses for each player
    hits_jogador1 = len(torpedo_targets_jogador1)
    misses_jogador1 = len(jogador1_torpedos) - hits_jogador1

    hits_jogador2 = len(torpedo_targets_jogador2)
    misses_jogador2 = len(jogador2_torpedos) - hits_jogador2

    # Calculate the total score for each player
    total_score_jogador1 = score_jogador1 - (3 * misses_jogador1)
    total_score_jogador2 = score_jogador2 - (3 * misses_jogador2)

    # Determine the winner
    if total_score_jogador1 == total_score_jogador2:
        winner = "EMPATE"
    elif total_score_jogador1 > total_score_jogador2:
        winner = "J1"
    else:
        winner = "J2"

    # Format the result string
    result_string = f"{winner} {hits_jogador1}AA {misses_jogador1}AE {total_score_jogador1}PT"

    # Example of usage
    with open('resultado.txt', 'w') as output_file:
        output_file.write(result_string)

    return result_string




# resultado = batalha_naval('jogador1.txt', 'jogador2.txt')
# with open('resultado.txt', 'w') as output_file:
#     output_file.write(resultado)
