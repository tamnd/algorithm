# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kerberos/. The authors are listed in prov/D7Z6QK.jsonl.
"""A toy Kerberos V5 after RFC 4120: the AS, TGS and client/server (AP)
exchanges, with tickets, authenticators, clock skew checks, a replay cache
and PA-ENC-TIMESTAMP pre-authentication.

What is simplified:
* Messages are Python dicts and the sealed parts are JSON, not ASN.1 DER.
* The encryption is a study AEAD (encrypt-then-MAC with an HMAC-SHA256 key
  stream in counter mode and a 16-byte HMAC-SHA256 tag). The RFC 4120 key
  usage number is the associated data, as RFC 3961 derives a key per usage.
  It is not the aes256-cts-hmac-sha1-96 or aes256-cts-hmac-sha384-192
  enctype of real Kerberos.
* The string-to-key function is PBKDF2-HMAC-SHA256 with the salt
  realm || name and a low toy iteration count, after the idea of RFC 3962.
* There are no flags, no renewal, no addresses, no cross-realm keys and no
  KDC options.

For study only. The code is not constant time and must not protect real
data. Use MIT Kerberos, Heimdal or Active Directory.
"""

import hashlib
import hmac
import json
import secrets
from typing import Dict, Iterable, Optional, Tuple

SKEW = 300  # seconds; RFC 4120 Section 3.2.3 gives 5 minutes as an example
MAX_LIFE = 10 * 3600  # the longest ticket life that the KDC issues
TOY_ITERATIONS = 1000  # RFC 3962 uses 4096 by default; a toy value keeps the tests fast

# Key usage numbers, RFC 4120 Section 7.5.1
USAGE_PA_ENC_TIMESTAMP = 1
USAGE_TICKET = 2
USAGE_AS_REP_ENC = 3
USAGE_TGS_REQ_AUTH = 7
USAGE_TGS_REP_ENC = 8
USAGE_AP_REQ_AUTH = 11
USAGE_AP_REP_ENC = 12


class KerberosError(Exception):
    """Carries the name of the RFC 4120 error code, for example KRB_AP_ERR_SKEW."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


class AuthError(Exception):
    pass


# ---------------------------------------------------------------- study AEAD and keys


def _prf(key: bytes, data: bytes) -> bytes:
    return hmac.new(key, data, hashlib.sha256).digest()


def seal(key: bytes, usage: int, obj: dict) -> bytes:
    """Encrypt-then-MAC of the JSON form of obj, bound to the key usage."""
    pt = json.dumps(obj, sort_keys=True).encode()
    nonce = secrets.token_bytes(12)
    ke, km = _prf(key, b"enc%d" % usage), _prf(key, b"mac%d" % usage)
    stream = b"".join(_prf(ke, nonce + i.to_bytes(4, "big")) for i in range(len(pt) // 32 + 1))
    ct = bytes(x ^ y for x, y in zip(pt, stream))
    return nonce + ct + _prf(km, nonce + ct)[:16]


def unseal(key: bytes, usage: int, box: bytes) -> dict:
    if len(box) < 28:
        raise AuthError("short")
    nonce, ct, tag = box[:12], box[12:-16], box[-16:]
    ke, km = _prf(key, b"enc%d" % usage), _prf(key, b"mac%d" % usage)
    if not hmac.compare_digest(tag, _prf(km, nonce + ct)[:16]):
        raise AuthError("bad tag")
    stream = b"".join(_prf(ke, nonce + i.to_bytes(4, "big")) for i in range(len(ct) // 32 + 1))
    return json.loads(bytes(x ^ y for x, y in zip(ct, stream)))


def string_to_key(password: str, realm: str, name: str, iterations: int = TOY_ITERATIONS) -> bytes:
    """The long-term key of a principal from its password; the salt is realm || name."""
    return hashlib.pbkdf2_hmac("sha256", password.encode(), (realm + name).encode(), iterations, 32)


class Clock:
    """The local clock of one party; tests move it and set it wrong."""

    def __init__(self, t: int) -> None:
        self.t = t

    def now(self) -> int:
        return self.t


class ReplayCache:
    """Remembers authenticators seen within the skew window (RFC 4120 Section 3.2.3)."""

    def __init__(self, skew: int = SKEW) -> None:
        self.skew = skew
        self.seen: Dict[Tuple[str, int, int, str], int] = {}

    def check_and_add(self, entry: Tuple[str, int, int, str], now: int) -> None:
        self.seen = {e: t for e, t in self.seen.items() if t >= now - self.skew}
        if entry in self.seen:
            raise KerberosError("KRB_AP_ERR_REPEAT")
        self.seen[entry] = entry[1]


def verify_ap_req(ap_req: dict, sname: str, skey: bytes, clock: Clock, cache: ReplayCache, usage: int) -> Tuple[dict, dict]:
    """The checks of RFC 4120 Section 3.2.3, shared by the TGS and by each service."""
    try:
        ticket = unseal(skey, USAGE_TICKET, ap_req["ticket"])
    except AuthError:
        raise KerberosError("KRB_AP_ERR_MODIFIED")
    if ticket["sname"] != sname:
        raise KerberosError("KRB_AP_ERR_NOT_US")
    now = clock.now()
    if now > ticket["endtime"] + cache.skew:
        raise KerberosError("KRB_AP_ERR_TKT_EXPIRED")
    if now < ticket["starttime"] - cache.skew:
        raise KerberosError("KRB_AP_ERR_TKT_NYV")
    try:
        auth = unseal(bytes.fromhex(ticket["key"]), usage, ap_req["authenticator"])
    except AuthError:
        raise KerberosError("KRB_AP_ERR_MODIFIED")
    if auth["cname"] != ticket["cname"]:
        raise KerberosError("KRB_AP_ERR_BADMATCH")
    if abs(now - auth["ctime"]) > cache.skew:
        raise KerberosError("KRB_AP_ERR_SKEW")
    cache.check_and_add((auth["cname"], auth["ctime"], auth["cusec"], sname), now)
    return ticket, auth


# ---------------------------------------------------------------- the KDC


class KDC:
    def __init__(self, realm: str, clock: Clock) -> None:
        self.realm = realm
        self.clock = clock
        self.tgs_name = "krbtgt/" + realm
        self.db: Dict[str, bytes] = {self.tgs_name: secrets.token_bytes(32)}
        self.preauth: Dict[str, bool] = {}
        self.cache = ReplayCache()

    def add_principal(self, name: str, key: bytes, require_preauth: bool = True) -> None:
        self.db[name] = key
        self.preauth[name] = require_preauth

    def _ticket(self, sname: str, cname: str, key: bytes, authtime: int, endtime: int) -> bytes:
        now = self.clock.now()
        part = {"key": key.hex(), "cname": cname, "sname": sname, "authtime": authtime, "starttime": now, "endtime": endtime}
        return seal(self.db[sname], USAGE_TICKET, part)

    def as_req(self, req: dict) -> dict:
        cname, now = req["cname"], self.clock.now()
        if cname not in self.db or cname == self.tgs_name:
            raise KerberosError("KDC_ERR_C_PRINCIPAL_UNKNOWN")
        kc = self.db[cname]
        if self.preauth.get(cname, True):  # @line L2
            if "padata" not in req:
                raise KerberosError("KDC_ERR_PREAUTH_REQUIRED")
            try:
                ts = unseal(kc, USAGE_PA_ENC_TIMESTAMP, req["padata"])["patimestamp"]
            except AuthError:
                raise KerberosError("KDC_ERR_PREAUTH_FAILED")
            if abs(now - ts) > SKEW:
                raise KerberosError("KRB_AP_ERR_SKEW")
        k_tgs = secrets.token_bytes(32)  # @line L3
        endtime = min(req["till"], now + MAX_LIFE)
        tgt = self._ticket(self.tgs_name, cname, k_tgs, now, endtime)
        enc = {"key": k_tgs.hex(), "nonce": req["nonce"], "sname": self.tgs_name, "authtime": now, "endtime": endtime}
        return {"cname": cname, "ticket": tgt, "enc_part": seal(kc, USAGE_AS_REP_ENC, enc)}  # @line L4

    def tgs_req(self, req: dict) -> dict:
        tgt, auth = verify_ap_req(req["ap_req"], self.tgs_name, self.db[self.tgs_name], self.clock, self.cache, USAGE_TGS_REQ_AUTH)  # @line L7
        sname = req["sname"]
        if sname not in self.db or sname == self.tgs_name:
            raise KerberosError("KDC_ERR_S_PRINCIPAL_UNKNOWN")
        now = self.clock.now()
        k_cs = secrets.token_bytes(32)  # @line L8
        endtime = min(req["till"], tgt["endtime"], now + MAX_LIFE)
        ticket = self._ticket(sname, tgt["cname"], k_cs, tgt["authtime"], endtime)
        enc = {"key": k_cs.hex(), "nonce": req["nonce"], "sname": sname, "authtime": tgt["authtime"], "endtime": endtime}
        return {"cname": tgt["cname"], "ticket": ticket, "enc_part": seal(bytes.fromhex(tgt["key"]), USAGE_TGS_REP_ENC, enc)}  # @line L9


# ---------------------------------------------------------------- services and clients


class Service:
    def __init__(self, name: str, key: bytes, clock: Clock) -> None:
        self.name, self.key, self.clock = name, key, clock
        self.cache = ReplayCache()
        self.sessions: Dict[str, bytes] = {}

    def ap_req(self, msg: dict, mutual: bool = True) -> Optional[bytes]:
        ticket, auth = verify_ap_req(msg, self.name, self.key, self.clock, self.cache, USAGE_AP_REQ_AUTH)  # @line L12
        k_cs = bytes.fromhex(ticket["key"])
        self.sessions[ticket["cname"]] = k_cs
        if not mutual:
            return None
        return seal(k_cs, USAGE_AP_REP_ENC, {"ctime": auth["ctime"], "cusec": auth["cusec"]})  # @line L13


class Client:
    def __init__(self, name: str, password: str, realm: str, clock: Clock) -> None:
        self.name, self.realm, self.clock = name, realm, clock
        self.key = string_to_key(password, realm, name)
        self.tgt: Optional[bytes] = None
        self.tgs_key: Optional[bytes] = None
        self.tickets: Dict[str, Tuple[bytes, bytes]] = {}
        self._usec = 0

    def _authenticator(self, key: bytes, usage: int) -> Tuple[bytes, Tuple[int, int]]:
        self._usec += 1
        ctime = self.clock.now()
        return seal(key, usage, {"cname": self.name, "ctime": ctime, "cusec": self._usec}), (ctime, self._usec)

    def as_exchange(self, kdc: KDC, preauth: bool = True, life: int = 8 * 3600) -> None:
        nonce = secrets.randbelow(2**31)
        req = {"cname": self.name, "sname": kdc.tgs_name, "nonce": nonce, "till": self.clock.now() + life}  # @line L1
        if preauth:
            req["padata"] = seal(self.key, USAGE_PA_ENC_TIMESTAMP, {"patimestamp": self.clock.now()})
        rep = kdc.as_req(req)
        try:
            enc = unseal(self.key, USAGE_AS_REP_ENC, rep["enc_part"])  # @line L5
        except AuthError:
            raise KerberosError("KRB_AP_ERR_MODIFIED")
        if enc["nonce"] != nonce or enc["sname"] != kdc.tgs_name:
            raise KerberosError("KRB_AP_ERR_BADMATCH")
        self.tgt, self.tgs_key = rep["ticket"], bytes.fromhex(enc["key"])

    def tgs_exchange(self, kdc: KDC, sname: str, life: int = 8 * 3600) -> None:
        assert self.tgt is not None and self.tgs_key is not None
        nonce = secrets.randbelow(2**31)
        auth, _ = self._authenticator(self.tgs_key, USAGE_TGS_REQ_AUTH)
        req = {"ap_req": {"ticket": self.tgt, "authenticator": auth}, "sname": sname, "nonce": nonce, "till": self.clock.now() + life}  # @line L6
        rep = kdc.tgs_req(req)
        enc = unseal(self.tgs_key, USAGE_TGS_REP_ENC, rep["enc_part"])  # @line L10
        if enc["nonce"] != nonce or enc["sname"] != sname:
            raise KerberosError("KRB_AP_ERR_BADMATCH")
        self.tickets[sname] = (rep["ticket"], bytes.fromhex(enc["key"]))

    def make_ap_req(self, sname: str) -> Tuple[dict, Tuple[int, int]]:
        ticket, k_cs = self.tickets[sname]
        auth, stamp = self._authenticator(k_cs, USAGE_AP_REQ_AUTH)
        return {"ticket": ticket, "authenticator": auth}, stamp  # @line L11

    def check_ap_rep(self, sname: str, ap_rep: bytes, stamp: Tuple[int, int]) -> bool:
        _, k_cs = self.tickets[sname]
        try:
            rep = unseal(k_cs, USAGE_AP_REP_ENC, ap_rep)  # @line L14
        except AuthError:
            return False
        return (rep["ctime"], rep["cusec"]) == stamp


def full_login(kdc: KDC, client: Client, service: Service) -> bool:
    """AS, TGS and AP exchanges with mutual authentication."""
    client.as_exchange(kdc)
    client.tgs_exchange(kdc, service.name)
    ap_req, stamp = client.make_ap_req(service.name)
    ap_rep = service.ap_req(ap_req)
    assert ap_rep is not None
    return client.check_ap_rep(service.name, ap_rep, stamp) and service.sessions[client.name] == client.tickets[service.name][1]


# ---------------------------------------------------------------- offline guessing (toy only)


def offline_guess(box: bytes, usage: int, realm: str, name: str, words: Iterable[str]) -> Optional[str]:
    """Try each word as the password behind a sealed part. The tag tells a right guess from a wrong one.

    Applied to the enc-part of an AS-REP that the KDC sent without pre-authentication,
    this is the guess that AS-REP roasting makes. Applied to a service ticket whose
    service key comes from a password, it is Kerberoasting.
    """
    for w in words:
        try:
            unseal(string_to_key(w, realm, name), usage, box)
            return w
        except AuthError:
            continue
    return None
