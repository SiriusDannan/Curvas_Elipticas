# main_diffie_hellman.py

# Importa as funções diretamente do pacote edwards_crypto
# Se __init__.py importou de curves, elas estarão disponíveis assim.
# Caso contrário, seria: from edwards_crypto curves import edwards_add, scalar_multiplication
from curves import scalar_multiplication

if __name__ == "__main__":
    # Parâmetros da Curva de Edwards e do corpo finito Fp
    # Estes são os mesmos do seu exemplo original
    p = 17  # Módulo primo
    a = 1   # Coeficiente 'a' da curva de Edwards
    d = 2   # Coeficiente 'd' da curva de Edwards

    # Ponto base da curva (gerador)
    P = (3, 0)

    # Chaves privadas (escalares) para Alice e Bob
    alice_pkey = 3
    bob_pkey = 5

    try:
        # Alice calcula sua chave pública: A = alice_pkey * P
        A = scalar_multiplication(P, alice_pkey, a, d, p)
        print(f"Chave Pública de Alice (A): {A}")

        # Bob calcula sua chave pública: B = bob_pkey * P
        B = scalar_multiplication(P, bob_pkey, a, d, p)
        print(f"Chave Pública de Bob (B): {B}")

        # Alice calcula a chave secreta compartilhada: S_alice = alice_pkey * B
        S_alice = scalar_multiplication(B, alice_pkey, a, d, p)
        print(f"Chave Secreta Compartilhada de Alice (S_alice): {S_alice}")

        # Bob calcula a chave secreta compartilhada: S_bob = bob_pkey * A
        S_bob = scalar_multiplication(A, bob_pkey, a, d, p)
        print(f"Chave Secreta Compartilhada de Bob (S_bob): {S_bob}")

        # Verifica se as chaves secretas são iguais
        if S_alice == S_bob:
            print("\nAs chaves secretas compartilhadas são idênticas. Protocolo bem-sucedido!")
        else:
            print("\nAs chaves secretas compartilhadas NÃO são idênticas. Houve um erro.")

    except ZeroDivisionError as e:
        print(f"Erro na computação da curva elíptica: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
