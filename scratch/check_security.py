from app.core.security import hash_password, verify_password, create_access_token, decode_token

h = hash_password("Prueba123!")
assert verify_password("Prueba123!", h)

tok = create_access_token(sub="ana@test.local", uid=1, rol="cliente", minutes=1)
data = decode_token(tok)
assert data["sub"] == "ana@test.local" and data["uid"] == 1

print("OK security")
