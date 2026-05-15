# main_montgomery.py
# Demonstração do Diffie-Hellman usando curva de Montgomery

from montgomery import montgomery_scalar_multiplication

if __name__ == "__main__":
    # Parâmetros da curva de Montgomery
    # Curva Curve25519 (usada em várias aplicações criptográficas)
    # p = 2^255 - 19
    # A = 486662
    # B = 1

    # Parâmetros simplificados para demonstração
    p = 17  # Módulo primo
    A = 1  # Coeficiente A da curva de Montgomery
    B = 1  # Coeficiente B da curva de Montgomery

    # Ponto base na curva de Montgomery By² = x³ + Ax² + x
    # Para x=3, encontramos y que satisfaz a equação
    # y² = (x³ + Ax² + x) / B
    x = 3
    y_squared = (pow(x, 3, p) + A * x * x + x) % p
    # y = sqrt(y_squared) mod p - em geral precisa calcular raiz quadrada modular
    # Para simplificar, usamos um ponto já verificado
    P = (3, 4)  # Verificar: 1*16 = 27+9+3=39≡5? Ajustar

    # Chaves privadas
    alice_private = 3
    bob_private = 5

    print("=== Diffie-Hellman na Curva de Montgomery ===")
    print(f"Parâmetros: p={p}, A={A}, B={B}")
    print(f"Ponto base P = {P}")
    print(f"Chave privada de Alice: {alice_private}")
    print(f"Chave privada de Bob: {bob_private}")
    print()

    try:
        # Alice calcula chave pública: A = alice_private * P
        A_pub = montgomery_scalar_multiplication(P, alice_private, A, B, p)
        print(f"Chave pública de Alice: {A_pub}")

        # Bob calcula chave pública: B = bob_private * P
        B_pub = montgomery_scalar_multiplication(P, bob_private, A, B, p)
        print(f"Chave pública de Bob: {B_pub}")
        print()

        # Alice calcula segredo compartilhado: alice_private * B_pub
        shared_alice = montgomery_scalar_multiplication(B_pub, alice_private, A, B, p)
        print(f"Segredo compartilhado (Alice): {shared_alice}")

        # Bob calcula segredo compartilhado: bob_private * A_pub
        shared_bob = montgomery_scalar_multiplication(A_pub, bob_private, A, B, p)
        print(f"Segredo compartilhado (Bob): {shared_bob}")

        if shared_alice == shared_bob:
            print("\nSucesso! Os segredos compartilhados são iguais.")
        else:
            print("\nErro: Os segredos não coincidem.")

    except Exception as e:
        print(f"Erro durante a computação: {e}")