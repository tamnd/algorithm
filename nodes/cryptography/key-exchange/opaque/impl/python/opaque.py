# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/opaque/. The authors are listed in prov/4VXR26.jsonl.
"""A simplified OPAQUE, after RFC 9807 (July 2025): the OPRF, the envelope,
the masked credential response and the 3DH key exchange, with the same
structure and order of steps as the RFC.

What is simplified, so the code is NOT the RFC 9807 wire protocol and does
not reproduce its test vectors:

* Group: the quadratic residues modulo the 1024-bit safe prime of RFC 5054,
  Appendix A (g = 4, prime order q), not ristretto255 or P-256.
* Hash to group: SHA-512 output expanded to 1088 bits, reduced mod p and
  squared. RFC 9497 uses hash-to-curve.
* OPRF: the 2HashDH function F(k, pw) = H(pw, H'(pw)^k) with blinding,
  in the spirit of RFC 9497 (mode 0x00), without its exact encodings.
* KSF: the identity. Production must use a memory-hard function such as
  Argon2 or scrypt here.
* Key schedule: HKDF-SHA256 with plain labels, not the Expand-Label format.

For study only. The code is not constant time, and it must not protect real
data.

Lines marked L1 to L11 match the pseudocode on the page.
"""

import hashlib
import hmac
import secrets

P = int(
    "EEAF0AB9ADB38DD69C33F80AFA8FC5E86072618775FF3C0B9EA2314C"
    "9C256576D674DF7496EA81D3383B4813D692C6E0E0D5D8E250B98BE4"
    "8E495C1D6089DAD15DC7D7B46154D6B6CE8EF4AD69B15D4982559B29"
    "7BCF1885C529F566660E57EC68EDBC3C05726CC02FD4CBF4976EAA9A"
    "FD5138FE8376435B9FC61D2FC0EB06E3",
    16,
)
Q = (P - 1) // 2
G = 4
NE = 128   # bytes in an encoded group element
NH = 32    # bytes in a hash, MAC or key


class OpaqueError(ValueError):
    pass


def i2b(x: int) -> bytes:
    return x.to_bytes(NE, "big")


def in_group(X: int) -> bool:
    return 1 < X < P and pow(X, Q, P) == 1


# ---------------------------------------------------------------- HKDF (RFC 5869), local copy


def extract(salt: bytes, ikm: bytes) -> bytes:
    return hmac.new(salt or bytes(NH), ikm, hashlib.sha256).digest()


def expand(prk: bytes, info: bytes, length: int = NH) -> bytes:
    out, t, i = b"", b"", 1
    while len(out) < length:
        t = hmac.new(prk, t + info + bytes([i]), hashlib.sha256).digest()
        out += t
        i += 1
    return out[:length]


def mac(key: bytes, msg: bytes) -> bytes:
    return hmac.new(key, msg, hashlib.sha256).digest()


# ---------------------------------------------------------------- the OPRF (2HashDH)


def hash_to_group(pw: bytes) -> int:
    wide = b"".join(hashlib.sha512(b"H2G" + bytes([i]) + pw).digest() for i in range(3))[:136]
    y = int.from_bytes(wide, "big") % P
    return y * y % P


def blind(pw: bytes, rng=secrets.randbelow):
    r = 1 + rng(Q - 1)
    return r, pow(hash_to_group(pw), r, P)


def evaluate(k: int, M: int) -> int:
    if not in_group(M):
        raise OpaqueError("blinded element is not in the group")
    return pow(M, k, P)


def finalize(pw: bytes, r: int, Z: int) -> bytes:
    N = pow(Z, pow(r, -1, Q), P)
    return hashlib.sha256(len(pw).to_bytes(2, "big") + pw + i2b(N) + b"Finalize").digest()


def ksf(y: bytes) -> bytes:
    return y                     # identity. Use Argon2id or scrypt in production.


def derive_key_pair(seed: bytes):
    sk = 1 + int.from_bytes(expand(seed, b"OPAQUE-DeriveDiffieHellmanKeyPair", 64), "big") % (Q - 1)
    return sk, pow(G, sk, P)


def random_key_pair(rng=secrets.randbelow):
    sk = 1 + rng(Q - 1)
    return sk, pow(G, sk, P)


# ---------------------------------------------------------------- the envelope (RFC 9807, Section 4)


def cleartext(pk_s: int, server_id: bytes, client_id: bytes) -> bytes:
    return i2b(pk_s) + len(server_id).to_bytes(2, "big") + server_id + len(client_id).to_bytes(2, "big") + client_id


def store(rwd: bytes, pk_s: int, server_id: bytes, client_id: bytes, nonce: bytes):
    masking_key = expand(rwd, b"MaskingKey")
    auth_key = expand(rwd, nonce + b"AuthKey")
    export_key = expand(rwd, nonce + b"ExportKey")
    seed = expand(rwd, nonce + b"PrivateKey")
    _, pk_u = derive_key_pair(seed)                                                  # @line L4
    tag = mac(auth_key, nonce + cleartext(pk_s, server_id, client_id))              # @line L5
    return nonce + tag, pk_u, masking_key, export_key


def recover(rwd: bytes, pk_s: int, server_id: bytes, client_id: bytes, envelope: bytes):
    nonce, tag = envelope[:NH], envelope[NH:]
    auth_key = expand(rwd, nonce + b"AuthKey")
    export_key = expand(rwd, nonce + b"ExportKey")
    sk_u, pk_u = derive_key_pair(expand(rwd, nonce + b"PrivateKey"))
    if not hmac.compare_digest(tag, mac(auth_key, nonce + cleartext(pk_s, server_id, client_id))):
        raise OpaqueError("envelope recovery failed")
    return sk_u, pk_u, export_key


# ---------------------------------------------------------------- the server


class Server:
    def __init__(self, server_id: bytes = b"server", rng=secrets.randbelow):
        self.id, self.rng = server_id, rng
        self.sk, self.pk = random_key_pair(rng)
        self.oprf_seed = rng(2**256).to_bytes(32, "big")
        self.records = {}

    def oprf_key(self, credential_id: bytes) -> int:
        """One OPRF key per user, derived from a server seed and the credential identifier."""
        return 1 + int.from_bytes(expand(self.oprf_seed, credential_id + b"OprfKey", 64), "big") % (Q - 1)

    def registration_response(self, credential_id: bytes, M: int):
        return evaluate(self.oprf_key(credential_id), M), self.pk                    # @line L2

    def finish_registration(self, credential_id: bytes, record: dict):
        self.records[credential_id] = record

    def ke2(self, credential_id: bytes, client_id: bytes, ke1: dict):
        rec = self.records[credential_id]
        Z = evaluate(self.oprf_key(credential_id), ke1["M"])                         # @line L7
        masking_nonce = self.rng(2**256).to_bytes(32, "big")
        pad = expand(rec["masking_key"], masking_nonce + b"CredentialResponsePad", NE + 2 * NH)
        masked = bytes(a ^ b for a, b in zip(pad, i2b(self.pk) + rec["envelope"]))
        esk, epk = random_key_pair(self.rng)
        nonce_s = self.rng(2**256).to_bytes(32, "big")
        if not in_group(ke1["epk"]):
            raise OpaqueError("bad client key share")
        dh1, dh2, dh3 = pow(ke1["epk"], esk, P), pow(ke1["epk"], self.sk, P), pow(rec["pk_u"], esk, P)
        resp = dict(Z=Z, masking_nonce=masking_nonce, masked=masked, nonce=nonce_s, epk=epk)
        preamble = transcript(client_id, ke1, self.id, resp)
        km2, km3, session_key = key_schedule(dh1, dh2, dh3, preamble)
        resp["mac"] = mac(km2, hashlib.sha256(preamble).digest())
        self._pending = (km3, session_key, preamble + resp["mac"])
        return resp

    def finish(self, ke3: bytes) -> bytes:
        km3, session_key, th = self._pending
        if not hmac.compare_digest(ke3, mac(km3, hashlib.sha256(th).digest())):      # @line L11
            raise OpaqueError("client MAC failed")
        return session_key


# ---------------------------------------------------------------- the 3DH key schedule


def transcript(client_id: bytes, ke1: dict, server_id: bytes, ke2: dict) -> bytes:
    return b"|".join([b"OPAQUE study", client_id, ke1["nonce"], i2b(ke1["M"]), i2b(ke1["epk"]), server_id,
                      i2b(ke2["Z"]), ke2["masking_nonce"], ke2["masked"], ke2["nonce"], i2b(ke2["epk"])])


def key_schedule(dh1: int, dh2: int, dh3: int, preamble: bytes):
    prk = extract(b"", i2b(dh1) + i2b(dh2) + i2b(dh3))
    th = hashlib.sha256(preamble).digest()
    hs = expand(prk, b"HandshakeSecret" + th)
    session_key = expand(prk, b"SessionKey" + th)
    return expand(hs, b"ServerMAC"), expand(hs, b"ClientMAC"), session_key


# ---------------------------------------------------------------- the client


def register(server: Server, credential_id: bytes, client_id: bytes, pw: bytes, rng=secrets.randbelow) -> bytes:
    r, M = blind(pw, rng)                                                            # @line L1
    Z, pk_s = server.registration_response(credential_id, M)
    y = finalize(pw, r, Z)                                                           # @line L3
    rwd = extract(b"", y + ksf(y))
    nonce = rng(2**256).to_bytes(32, "big")
    envelope, pk_u, masking_key, export_key = store(rwd, pk_s, server.id, client_id, nonce)
    server.finish_registration(credential_id, dict(pk_u=pk_u, masking_key=masking_key, envelope=envelope))
    return export_key


def login(server: Server, credential_id: bytes, client_id: bytes, pw: bytes, rng=secrets.randbelow):
    """Returns (client session key, server session key, export key). Raises OpaqueError on failure."""
    r, M = blind(pw, rng)                                                            # @line L6
    esk, epk = random_key_pair(rng)
    ke1 = dict(M=M, nonce=rng(2**256).to_bytes(32, "big"), epk=epk)
    ke2 = server.ke2(credential_id, client_id, ke1)
    y = finalize(pw, r, ke2["Z"])                                                    # @line L8
    rwd = extract(b"", y + ksf(y))
    masking_key = expand(rwd, b"MaskingKey")
    pad = expand(masking_key, ke2["masking_nonce"] + b"CredentialResponsePad", NE + 2 * NH)
    plain = bytes(a ^ b for a, b in zip(pad, ke2["masked"]))
    pk_s, envelope = int.from_bytes(plain[:NE], "big"), plain[NE:]
    if not in_group(pk_s):
        raise OpaqueError("envelope recovery failed")
    sk_u, _, export_key = recover(rwd, pk_s, server.id, client_id, envelope)
    if not in_group(ke2["epk"]):
        raise OpaqueError("bad server key share")
    dh1, dh2, dh3 = pow(ke2["epk"], esk, P), pow(pk_s, esk, P), pow(ke2["epk"], sk_u, P)   # @line L9
    preamble = transcript(client_id, ke1, server.id, ke2)
    km2, km3, session_key = key_schedule(dh1, dh2, dh3, preamble)
    if not hmac.compare_digest(ke2["mac"], mac(km2, hashlib.sha256(preamble).digest())):
        raise OpaqueError("server MAC failed")
    ke3 = mac(km3, hashlib.sha256(preamble + ke2["mac"]).digest())                  # @line L10
    return session_key, server.finish(ke3), export_key
