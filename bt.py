# Constants for ship sizes
SHIP_SIZES = {
    '1': 4, # Encouraçado
    '2': 5, # Porta-avião
    '3': 1, # Submarino
    '4': 2  # Cruzador
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
    number = int(square[1:-1]) 
    orientation = square[-1]
    squares = []
    # print(f"Placing ship at {letter}{number} with direction {orientation}. Size: {ship_size}")

    if orientation == "V":
        for i in range(ship_size):
            new_square = letter + str(number + i) + orientation
            squares.append(new_square)
    elif orientation == "H":
        for i in range(ship_size):
            new_square = f"{chr(ord(letter) + i)}{number}{orientation}"
            squares.append(new_square)

    # print(f"This ship occupies these squares: {squares}")
    # print("--------------------------------------------------")
    return squares

def validate_piece_positions(pieces):
    for code, piece_positions in pieces.items():
        for position in piece_positions:
            if code == '3':
                if len(position) != 2 and len(position) != 3:
                    return f"ERROR_POSITION_NONEXISTENT_VALIDATION"
            else:
                if len(position) < 3 or len(position) > 4 or position[0] not in "ABCDEFGHIJKLMNO" or int(position[1:-1]) < 1 or int(position[1:-1]) > 15:
                    return f"ERROR_POSITION_NONEXISTENT_VALIDATION"
                if position[-1] not in "VH":
                    return f"ERROR_POSITION_NONEXISTENT_VALIDATION"
    return True

def validate_piece_overlap(pieces):
    occupied_positions = set()

    for code, piece_positions in pieces.items():
        if code == "3":
            for square in piece_positions:
                if square in occupied_positions:
                        return f"ERROR_OVERWRITE_PIECES_VALIDATION"
                occupied_positions.add(square)
        else:
            ship_size = SHIP_SIZES[code]
            for square in piece_positions:
                squares = calculate_all_squares(square, ship_size)
                for square in squares:
                    if square[0:-1] in occupied_positions: # L12H
                        return f"ERROR_OVERWRITE_PIECES_VALIDATION"
                    occupied_positions.add(square[0:-1])
    return True

def validate_torpedo_positions(torpedos):
    print(torpedos)
    for torpedo in torpedos: 
        print(f"torpedo: #{torpedo}#")
        if ((len(torpedo) < 2 or len(torpedo) > 3)
            or torpedo[0] not in "ABCDEFGHIJKLMNO"
            or not torpedo[1:].isdigit()):
            return False
    return True


def ship_sunk(board, ship_code, target):
    print(f"Target: #{target}#")
    # print(f"Ship code: #{ship_code}#")
    # M13
    col = target[0] # Letra da coordenada
    row = int(target[1:]) - 1 # Número da coordenada

    ship_size = SHIP_SIZES[ship_code]
    # print(f"Ship size: {ship_size}")
    
    counter = 1
    for i in range(ship_size):
        try:
            if ('*' in board[chr(ord(col) + i)][row]
                and
                ship_code in board[chr(ord(col) + i)][row]):
                # print(f"Verificando casa {chr(ord(col) + i)},{row}")
                counter += 1

            elif ('*' in board[chr(ord(col) - i)][row]
                  and
                ship_code in board[chr(ord(col) - i)][row]):
                counter += 1

            elif ('*' in board[col][row + i]
                  and
                ship_code in board[col][row + i]):
                # print(f"Verificando casa {col},{row + 1}")
                counter += 1

            elif ('*' in board[col][row - i]
                  and
                  board[col][row - i]):
                # print(f"Verificando casa {col},{row - 1}")
                counter += 1
        
            if counter >= ship_size:        
                print("afundou!!!!!!!")
                return True  # Ship is sunk horizontally
        except: "Out of bounds."
    return False  # Ship is not sunk in any direction


def calculate_score(board, torpedo_targets):
    hits = 0
    misses = 0
    points = 0
    for target in torpedo_targets:
        col = target[0]
        row = int(target[1:])
        try:
            if '*' in board[col][row - 1]:
                print("Esta casa já foi bombardeada.")
                break
            if board[col][row - 1] != '  ':
                hits += 1
                points += 3

                ship_code = board[col][row - 1][0] # "1", "2", "3", "4"
                if ship_sunk(board, ship_code, target):
                    points += 5

                board[col][row - 1] = board[col][row - 1].replace(" ", "*") # "1 " =>  "1*"
                # print(f"acertou no {col},{row}")
            else:
                misses += 1
        except: "Square out of bounds."
    return (hits, misses, points)


def batalha_naval(jogador1_file, jogador2_file):
    jogador1_pieces, jogador1_torpedos = read_and_validate_player_file(jogador1_file, 1)
    jogador2_pieces, jogador2_torpedos = read_and_validate_player_file(jogador2_file, 2)

    validation_error = validate_piece_positions(jogador1_pieces)
    if validation_error != True:
        return f"ERROR_POSITION_NONEXISTENT_VALIDATION"

    validation_error = validate_piece_positions(jogador2_pieces)
    if validation_error != True:
        return f"ERROR_POSITION_NONEXISTENT_VALIDATION"

    validation_error = validate_piece_overlap(jogador1_pieces)
    if validation_error != True:
        return f"ERROR_OVERWRITE_PIECES_VALIDATION"

    validation_error = validate_piece_overlap(jogador2_pieces)
    if validation_error != True:
        return f"ERROR_OVERWRITE_PIECES_VALIDATION"
    
    validation_error = validate_torpedo_positions(jogador1_torpedos)
    if validation_error != True:
        return f"ERROR_POSITION_NONEXISTENT_VALIDATION"
    
    validation_error = validate_torpedo_positions(jogador2_torpedos)
    if validation_error != True:
        return f"ERROR_POSITION_NONEXISTENT_VALIDATION"

    board_jogador1 = {chr(ord('A') + i): ['  '] * 15 for i in range(15)}
    board_jogador2 = {chr(ord('A') + i): ['  '] * 15 for i in range(15)}
    torpedo_targets_jogador1 = []
    torpedo_targets_jogador2 = []

    for piece in jogador1_pieces.items():
        code = piece[0]
        piece_positions_data = piece[1]
        ship_size = SHIP_SIZES[code]
        for position in piece_positions_data:
            if len(position) > 2 and not position[-1].isdigit():
                col = position[0]
                row = int(position[1:-1])
                direction = position[-1]

                if direction == 'H': # Horizontal: atualiza letra (col), mantém número (row)
                    if chr(ord(col) + ship_size - 1) > 'O':
                        return f"J2 - BAD POSITION: {chr(ord(col) + ship_size - 1) }"
                    for i in range(ship_size):
                        board_jogador1[chr(ord(col) + i)][row - 1] = f"{code} " 

                elif direction == "V": # Vertical: mantém letra (col), atualiza número (row)
                    if row + ship_size - 1 > 15:
                        return f"J2 - BAD POSITION: {row + ship_size - 1}"
                    for i in range(ship_size):
                        board_jogador1[col][row - 1 + i] = f"{code} "
                    
            else: 
                if len(position) == 2:
                    col = position[0]
                    row = int(position[1])
                    board_jogador1[col][row-1] = "3 "
                elif len(position) == 3:
                    col = position[0]
                    row = int(position[1:])
                    board_jogador1[col][row-1] = "3 "


    for piece in jogador2_pieces.items():
        code = piece[0]
        piece_positions_data = piece[1]
        ship_size = SHIP_SIZES[code]
        for position in piece_positions_data:
            if len(position) > 2 and not position[-1].isdigit():
                col = position[0]
                row = int(position[1:-1])
                direction = position[-1]

                if direction == 'H':
                    if chr(ord(col) + ship_size - 1) > 'O':
                        return f"J2 {validation_error} {chr(ord(col) + ship_size - 1) } BAD POSITION J2"
                    for i in range(ship_size):
                        board_jogador2[chr(ord(col) + i)][row - 1] = f"{code} " 
                elif direction == "V": 
                    if row + ship_size - 1 > 15:
                        return f"J2 {validation_error} {row + ship_size - 1} BAD POSITION J2"
                    for i in range(ship_size):
                        board_jogador2[col][row - 1 + i] = f"{code} " 
                    

            else: 
                if len(position) == 2:
                    col = position[0]
                    row = int(position[1])
                    board_jogador2[col][row-1] = "3 "
                elif len(position) == 3:
                    col = position[0]
                    row = int(position[1:])
                    board_jogador2[col][row-1] = "3 "


    for torpedo in jogador1_torpedos:
        if torpedo not in torpedo_targets_jogador1:
            torpedo_targets_jogador1.append(torpedo)

    for torpedo in jogador2_torpedos:
        if torpedo not in torpedo_targets_jogador2:
            torpedo_targets_jogador2.append(torpedo)

    score_jogador1 = calculate_score(board_jogador2, torpedo_targets_jogador1)
    # (30, 50)
    score_jogador2 = calculate_score(board_jogador1, torpedo_targets_jogador2)
    # (28, 52)

    print('Tabuleiro 1:')   
    for line in board_jogador1.items(): 
        print(line)

    print('Tabuleiro 2:')   
    for line in board_jogador2.items(): 
        print(line)

    if score_jogador1[0] == score_jogador2[0]:
        return f"J1 {score_jogador1[0]}AA {score_jogador2[1]}AE J2 {score_jogador2[0]}AA {score_jogador2[1]}AE - EMPATE"
    elif score_jogador1[0] > score_jogador2[0]:
        return f"J1 {score_jogador1[0]}AA {score_jogador1[1]}AE {score_jogador1[2]}PT"
    else:
        return f"J2 {score_jogador2[0]}AA {score_jogador2[1]}AE {score_jogador2[2]}PT"

# Example of usage
resultado = batalha_naval('jogador1.txt', 'jogador2.txt')
with open('resultado.txt', 'w') as output_file:
    output_file.write(resultado)
