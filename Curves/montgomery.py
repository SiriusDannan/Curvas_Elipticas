# edwards_crypto/montgomery.py
# Implementação das operações na curva de Montgomery

def montgomery_add(P1, P2, A, B, p):
    """
    Adição de dois pontos P1 e P2 na curva de Montgomery.
    Curva: By² = x³ + Ax² + x (mod p)

    P1, P2: Pontos (x, y)
    A, B: Coeficientes da curva de Montgomery
    p: Módulo primo

    Retorna: P3 = P1 + P2
    """
    if P1 is None or P2 is None:
        return P1 if P2 is None else P2

    x1, y1 = P1
    x2, y2 = P2

    # Caso: P1 = -P2 (pontos opostos)
    if x1 == x2 and y1 == (-y2) % p:
        return None  # Ponto no infinito

    # Caso: P1 = P2 (duplicação)
    if x1 == x2 and y1 == y2:
        return montgomery_double(P1, A, B, p)

    # Caso: Adição normal (P1 ≠ P2)
    # Cálculo da inclinação λ (secante)
    lambda_num = (y2 - y1) % p
    lambda_den = (x2 - x1) % p

    # Inverso modular do denominador
    inv_lambda_den = pow(lambda_den, -1, p)
    λ = (lambda_num * inv_lambda_den) % p

    # Cálculo das coordenadas do ponto resultante
    x3 = (B * λ * λ - A - x1 - x2) % p
    y3 = (λ * (x1 - x3) - y1) % p

    return x3, y3

def montgomery_double(P, A, B, p):
    """
    Duplicação de um ponto na curva de Montgomery.
    Calcula 2P = P + P

    P: Ponto (x, y)
    A, B: Coeficientes da curva de Montgomery
    p: Módulo primo

    Retorna: 2P
    """
    if P is None:
        return None

    x1, y1 = P

    # Verificação de ponto no infinito ou y = 0
    if y1 == 0:
        return None  # 2P é o ponto no infinito

    # Cálculo da inclinação λ (tangente)
    # λ = (3x1² + 2Ax1 + 1) / (2By1)
    lambda_num = (3 * x1 * x1 + 2 * A * x1 + 1) % p
    lambda_den = (2 * B * y1) % p

    # Inverso modular do denominador
    inv_lambda_den = pow(lambda_den, -1, p)
    λ = (lambda_num * inv_lambda_den) % p

    # Cálculo das coordenadas do ponto resultante
    x3 = (B * λ * λ - A - 2 * x1) % p
    y3 = (λ * (x1 - x3) - y1) % p

    return x3, y3

def montgomery_scalar_multiplication(P, n, A, B, p):
    """
    Multiplicação escalar na curva de Montgomery.
    Calcula nP usando o algoritmo double-and-add.

    P: Ponto base (x, y)
    n: Escalar (inteiro)
    A, B: Coeficientes da curva de Montgomery
    p: Módulo primo

    Retorna: nP
    """
    if n == 0 or P is None:
        return None  # Ponto no infinito

    # Representação binária de n
    binary_n = bin(n)[2:]

    # Inicialização: Q = ponto no infinito, R = P
    Q = None  # Ponto no infinito
    R = P

    # Algoritmo double-and-add
    for bit in binary_n:
        # Dobro: Q = 2Q
        if Q is not None:
            Q = montgomery_double(Q, A, B, p)
        else:
            Q = None

        # Se o bit for 1, adiciona R
        if bit == '1':
            if Q is None:
                Q = R
            else:
                Q = montgomery_add(Q, R, A, B, p)

        # Dobro de R para o próximo bit
        R = montgomery_double(R, A, B, p)

    return Q

def montgomery_scalar_multiplication_optimized(P, n, A, B, p):
    """
    Multiplicação escalar otimizada usando coordenadas projetivas.
    Mais eficiente para curvas de Montgomery.

    Implementação do algoritmo de Montgomery ladder.
    """
    if n == 0 or P is None:
        return None

    # Representação binária de n (do MSB para LSB)
    bits = bin(n)[2:]

    # Inicialização
    x1, z1 = P[0], 1  # Ponto de partida
    x2, z2 = montgomery_double_projective(P, A, B, p)

    # Montgomery ladder
    for bit in bits[1:]:
        if bit == '0':
            # Troca condicional (implementação simplificada)
            x1, x2 = x2, x1
            z1, z2 = z2, z1

        # Adição e duplicação em coordenadas projetivas
        x1, z1 = montgomery_add_projective((x1, z1), (x2, z2), P, A, B, p)
        x2, z2 = montgomery_double_projective((x2, z2), A, B, p)

        if bit == '0':
            x1, x2 = x2, x1
            z1, z2 = z2, z1

    # Converte de coordenadas projetivas para afim
    x = (x1 * pow(z1, -1, p)) % p

    # Recupera y (opcional)
    # y = calcular_y(x, A, B, p)

    return x, None  # Retorna apenas x para operações Diffie-Hellman

def montgomery_double_projective(P, A, B, p):
    """Duplicação em coordenadas projetivas (X:Z)"""
    X, Z = P
    t0 = (X + Z) % p
    t1 = (X - Z) % p

    t0 = (t0 * t0) % p
    t1 = (t1 * t1) % p
    t2 = (t0 - t1) % p

    X3 = (t0 * t1) % p
    Z3 = (t2 * (t1 + ((A + 2) // 4) * t2)) % p

    return X3, Z3

def montgomery_add_projective(P1, P2, P, A, B, p):
    """Adição em coordenadas projetivas (X:Z) para o ladder de Montgomery"""
    X1, Z1 = P1
    X2, Z2 = P2
    x0, _ = P  # Coordenada x do ponto base

    t0 = (X1 - Z1) % p
    t1 = (X2 + Z2) % p
    t2 = (X1 + Z1) % p
    t3 = (X2 - Z2) % p

    t0 = (t0 * t1) % p
    t1 = (t2 * t3) % p

    t2 = (t0 + t1) % p
    t3 = (t0 - t1) % p

    t2 = (t2 * t2) % p
    t3 = (t3 * t3) % p

    X3 = (t2 * x0) % p
    Z3 = t3 % p

    return X3, Z3