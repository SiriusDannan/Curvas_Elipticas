# meu_bsgs.py
import math
from curves import edwards_add, Double_and_Add, scalar_multiplication
from montgomery import montgomery_add, montgomery_scalar_multiplication

def ponto_inverso(P, p):
    x, y = P
    return ((-x) % p, y)

def meu_baby_step_giant_step(P, Q, n, a, d, p, curve_type='edwards'):
    """
    Ataque BSGS para curvas de Edwards ou Montgomery.

    curve_type: 'edwards' ou 'montgomery'
    """
    m = math.ceil(math.sqrt(n))

    baby_steps = {}
    cur = None  # Ponto neutro depende da curva

    if curve_type == 'edwards':
        cur = (0, 1)  # Elemento neutro para Edwards
        for j in range(m):
            if cur not in baby_steps:
                baby_steps[cur] = j
            cur = edwards_add(cur, P, a, d, p)

        Pm = Double_and_Add(P, m, a, d, p)
        inv_Pm = ponto_inverso(Pm, p)

    else:  # Montgomery
        # Para Montgomery, o ponto neutro é None
        cur = None
        for j in range(m):
            if cur not in baby_steps:
                baby_steps[cur] = j
            cur = montgomery_add(cur, P, a, d, p) if cur else P

        # Cálculo de Pm = m*P
        Pm = montgomery_scalar_multiplication(P, m, a, d, p)
        # Inverso na curva de Montgomery é (x, -y)
        inv_Pm = (Pm[0], (-Pm[1]) % p) if Pm else None

    Qi = Q
    for i in range(m):
        if Qi in baby_steps:
            j = baby_steps[Qi]
            k_candidate = i * m + j

            # Verifica se o candidato está correto
            if curve_type == 'edwards':
                if scalar_multiplication(P, k_candidate, a, d, p) == Q:
                    return k_candidate % n
            else:
                if montgomery_scalar_multiplication(P, k_candidate, a, d, p) == Q:
                    return k_candidate % n

            return k_candidate % n

        # Qi = Qi + inv_Pm
        if curve_type == 'edwards':
            Qi = edwards_add(Qi, inv_Pm, a, d, p)
        else:
            Qi = montgomery_add(Qi, inv_Pm, a, d, p) if Qi and inv_Pm else (inv_Pm or Qi)

    return None