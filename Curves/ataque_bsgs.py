# ataque_bsgs.py

from curves import scalar_multiplication

from meu_bsgs import meu_baby_step_giant_step

if __name__ == "__main__":

    p = 17
    a = 1
    d = 2

    P = (3, 0)
    n = 16
    alicia_pkey = 3
    benjamin_pkey = 5

    print("Parâmetros usados:")
    print(" p =", p, " a =", a, " d =", d, " n =", n)
    print(" P =", P, " alicia_pkey =", alicia_pkey, " benjamin_pkey =", benjamin_pkey)
    print()

    A = scalar_multiplication(P, alicia_pkey, a, d, p)
    B = scalar_multiplication(P, benjamin_pkey, a, d, p)

    print("Chave pública de Alicia (A):", A)
    print("Chave pública de Benjamin   (B):", B)

    k_alicia = meu_baby_step_giant_step(P, A, n, a, d, p)
    k_benjamin = meu_baby_step_giant_step(P, B, n, a, d, p)

    print("\nChave de Alicia encontrada:", k_alicia)
    print("Chave de Benjamin encontrada:  ", k_benjamin)

    if k_alicia == alicia_pkey and k_benjamin == benjamin_pkey:
        print("\nAtaque bem-sucedido! Chaves recuperadas com sucesso.")
    else:
        print("\nAtaque falhou. Verifique a implementação e os parâmetros.")
