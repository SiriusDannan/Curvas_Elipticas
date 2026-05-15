# edwards_crypto/curves.py

def edwards_add(P1, P2, a, d, p):
    """
    Realiza a adição de dois pontos P1 e P2 em uma Curva de Edwards definida por
    ax^2 + y^2 = 1 + dx^2y^2 sobre um corpo finito Fp.

    P1: Primeiro ponto (x1, y1)
    P2: Segundo ponto (x2, y2)
    a: Coeficiente 'a' da curva de Edwards
    d: Coeficiente 'd' da curva de Edwards
    p: Módulo do corpo finito (número primo)

    Retorna: O ponto resultante da adição (x3, y3)
    Levanta ZeroDivisionError se ocorrer divisão por zero.
    """
    x1, y1 = P1
    x2, y2 = P2

    # Denominadores conforme a fórmula da adição de Edwards
    denom_x = (1 + d * x1 * x2 * y1 * y2) % p
    denom_y = (1 - d * x1 * x2 * y1 * y2) % p

    # Verifica se os denominadores são zero para evitar erro de divisão
    if denom_x == 0 or denom_y == 0:
        # Em criptografia de curva elíptica, isso pode indicar um ponto no infinito
        # ou uma adição inválida para um ponto específico.
        # Para fins de exemplo, lançamos um erro. Em uma implementação real,
        # o tratamento do ponto no infinito (elemento neutro) seria feito aqui.
        raise ZeroDivisionError("Divisão por zero na adição de pontos. Possivelmente, o resultado é o ponto no infinito ou uma operação inválida.")

    # Calcula os inversos modulares dos denominadores
    # pow(base, exp, mod) é uma função embutida do Python para exponenciação modular
    # que lida com inversos modulares para exp=-1.
    inv_denom_x = pow(denom_x, -1, p)
    inv_denom_y = pow(denom_y, -1, p)

    # Coordenadas do ponto resultante (x3, y3)
    x3 = ((x1 * y2 + y1 * x2) * inv_denom_x) % p
    y3 = ((y1 * y2 - a * x1 * x2) * inv_denom_y) % p

    return (x3, y3)

def scalar_multiplication(P, n, a, d, p):
    """
    Realiza a multiplicação escalar de um ponto P por um inteiro n
    usando o algoritmo de "repetido quadrado" (double-and-add).

    P: Ponto base (x, y)
    n: Escalar (inteiro)
    a: Coeficiente 'a' da curva de Edwards
    d: Coeficiente 'd' da curva de Edwards
    p: Módulo do corpo finito

    Retorna: O ponto resultante nP
    """
    # Ponto no infinito (elemento neutro para curvas de Edwards é (0, 1) se y^2 = x^2 + 1)
    # Para a forma ax^2 + y^2 = 1 + dx^2y^2, (0,1) é o elemento neutro
    R = (0, 1)  # Inicializa o acumulador com o ponto neutro

    # Itera sobre os bits da representação binária de n, do mais significativo ao menos significativo
    # bin(n)[2:] remove o prefixo '0b' da string binária
    for bit in bin(n)[2:]:
        # Sempre dobra o ponto acumulador (R = 2R)
        R = edwards_add(R, R, a, d, p)
        
        # Se o bit atual for '1', adiciona o ponto P
        if bit == '1':
            R = edwards_add(R, P, a, d, p)

    return R
    
    
def Double_and_Add(P, k, a, d, p):
    """
    Implementa o "Algoritmo 1 Método Binário" para calcular Q = kP.

    Entrada:
        k: O escalar (um número inteiro).
        P: O ponto inicial (simulado como um inteiro).
    Saída:
        Q: O ponto resultante Q = kP (simulado como um inteiro).
    """
    
    # "Representação Binária de k"
    # Em Python, obtemos isso com bin(k) e removemos o prefixo '0b'
    k_binario = bin(k)[2:]
    n = len(k_binario)
    
    Q = P

    for i in range(1, n):
        bit_ki = k_binario[i]

        # 3: Q = 2Q {Doubling}
        # Sempre faz o doubling
        Q = edwards_add(Q, Q, a, d, p)  
        
        # 4: if ki = 1 then
        if bit_ki == '1':
            # 5: Q = Q + P {Addition}
            Q = edwards_add(Q, P, a, d, p)


    # 8: return Q
    return Q


