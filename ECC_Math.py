"""This code calculate the multiplication Elliptic curves over Zp"""

G = [2, 2]  # '''G Point'''
a = 0
p = 257
nb = 41  # '''User B private key'''
na = 101  # User A private key


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('Mod inverse does not exist')
    else:
        return x % m


def ng(veces, P, Q):
    xp = P[0]
    yp = P[1]
    xq, yq = Q[0], Q[1]
    # print(f"The next results are the multiplication of {veces}*({xp},{yp}), the q values are ({xq},{yq}),
    # the G values")
    if veces == 1:
        z = 0
    else:
        z = 1
    while z <= (veces - 1):
        if xp == xq and yp == yq:
            numerador = (3 * pow(xp, 2) + a) % p
            denominador = ((2 * yp) % p)
            inver = modinv(denominador, p)
            landa = (inver * numerador) % p

        else:
            numerador = (yq - yp) % p
            denominador = (xq - xp) % p
            inver = modinv(denominador, p)
            landa = (inver * numerador) % p

        xr = (pow(landa, 2) - xp - xq) % p
        yr = (landa * (xp - xr) - yp) % p
        z += 1
        xp, yp = xr, yr

    # You can uncomment this line to check the xp and yp values.
    # print(f"The result is ({xp},{yp})")

    return xp, yp


'''User A Key Generation'''

pa = ng(veces=na, P=G, Q=G)
print(f"User A public key is {pa}")

'''User B key generation'''

pb = ng(veces=nb, P=G, Q=G)
print(f"User B public key is {pb}")

'''Calculation of secret key by User'''
K1 = ng(veces=na, P=pb, Q=pb)
print(f"The calculated secret key by user A is {K1}")

K2 = ng(veces=nb, P=pa, Q=pa)
print(f"The calculated secret key by user B is {K2}")

'''From here is for private message encryption, it will ask for the PM value and k value'''

# Encryption

pm = [112, 26]
k = 41
kpb = ng(veces=k, P=pb, Q=pb)
cm = [ng(veces=k, P=G, Q=G), ng(veces=1, P=pm, Q=kpb)]
print(f"the ciphertext message is {cm}. User B public key is {pb} ")

# Decryption

print(f"The private message calculcation would be {cm[1]} - {nb}*{cm[0]}")
cm1 = ng(veces=nb, P=cm[0], Q=cm[0])
cm2 = [cm1[0], -cm1[1] % p]
pm = ng(veces=1, P=cm[1], Q=cm2)
print(f"The private message received by A is {pm}")
