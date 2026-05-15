# edwards_crypto/__init__.py

# Para que as funções edwards_add e scalar_multiplication
# possam ser importadas diretamente de 'edwards_crypto'
# (ex: from edwards_crypto import edwards_add)
# Ao invés de 'from edwards_crypto.curves import edwards_add'
from curves import edwards_add, scalar_multiplication, Double_and_Add

from montgomery import montgomery_add, montgomery_double, montgomery_scalar_multiplication, montgomery_scalar_multiplication_optimized