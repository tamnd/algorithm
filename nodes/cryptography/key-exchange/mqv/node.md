---
tag: 9AG3KC
kind: algorithm
slug: mqv
name: MQV key agreement
aliases:
- MQV
area: cryptography/key-exchange
level: advanced
summary: An implicitly authenticated Diffie-Hellman protocol. Each party combines its static and ephemeral keys as s = x + d*a, with d half the length of q, and raises the peer's combined key (Y * B^e) to s.
solves: [key-agreement-problem]
model: word-ram
complexity:
  vars: {m: the number of binary digits of the prime p}
  time: {worst: Θ(m^3), average: Θ(m^3), best: Θ(m^3)}
  space: {extra: Θ(m)}
properties: {deterministic: false, randomized: true}
history:
  year: 1995
  people: [Alfred Menezes, Minghua Qu, Scott Vanstone]
  note: Menezes, Qu and Vanstone proposed the protocol in 1995; Law, Menezes, Qu, Solinas and Vanstone gave the standard form with the half-length exponent in 2003.
prereqs: [diffie-hellman, authenticated-key-exchange]
see_also: [hmqv, key-compromise-impersonation, unknown-key-share-attack, ecdh, perfect-forward-secrecy, small-subgroup-attack, sigma-key-exchange, key-confirmation]
sources:
  - paper: "Laurie Law, Alfred Menezes, Minghua Qu, Jerry Solinas and Scott Vanstone, An efficient protocol for authenticated key agreement, Designs, Codes and Cryptography 28(2), 2003, pages 119 to 134"
    locator: the protocol with the half-length values, the cofactor, the claimed security attributes and the one-pass variant
  - paper: "Alfred Menezes, Minghua Qu and Scott Vanstone, Some new key agreement protocols providing mutual implicit authentication, Workshop on Selected Areas in Cryptography (SAC) 1995"
    locator: the first form of the protocol (venue and pages to check)
  - paper: "Burton S. Kaliski Jr., An unknown key-share attack on the MQV key agreement protocol, ACM Transactions on Information and System Security 4(3), 2001, pages 275 to 288"
    locator: the attack with an on-line registered static key derived from the victim's ephemeral value
  - url: "https://doi.org/10.6028/NIST.SP.800-56Ar3"
    title: "E. Barker, L. Chen, A. Roginsky, A. Vassilev and R. Davis, NIST SP 800-56A Rev. 3, Recommendation for Pair-Wise Key-Establishment Schemes Using Discrete Logarithm Cryptography, April 2018"
    locator: Section 5.7.2 (the MQV primitives, MQV2 and ECC MQV, with the associate value function) and Section 6 (the schemes that use them)
  - paper: "Hugo Krawczyk, HMQV: a high-performance secure Diffie-Hellman protocol, CRYPTO 2005, LNCS 3621, Springer, 2005, pages 546 to 566"
    locator: the analysis of MQV and the weaknesses that motivated HMQV; full version IACR ePrint 2005/176
---

MQV (Menezes, Qu and Vanstone) is an authenticated [Diffie-Hellman](/diffie-hellman/) key agreement in which each party has a static key pair and makes a fresh ephemeral pair for each session, and the two are combined into one exponent. Party $\hat A$ computes $s_A = x + d \cdot a \bmod q$, where $d$ is a half-length number taken from its own ephemeral value $X$, and raises the peer's combined value $Y \cdot B^e$ to $s_A$. Both parties get $g^{s_A s_B}$. The protocol needs only two messages, no signatures and about half an exponentiation more than plain Diffie-Hellman, and authentication is implicit: only the owner of $b$ can compute the key. MQV is in IEEE 1363, ANSI X9.42 and X9.63, and NIST SP 800-56A. It has no security proof, and [HMQV](/hmqv/) is its proven successor.

**Notation.** $G = \langle g \rangle$ is a subgroup of prime order $q$ of $\mathbb{Z}_p^*$ (or of an elliptic curve group), with cofactor $h$. $\hat A$ has the static pair $(a, A = g^a)$ and the ephemeral pair $(x, X = g^x)$; $\hat B$ has $(b, B)$ and $(y, Y)$. $w = \lceil \lceil \log_2 q \rceil / 2 \rceil$, and the associate value function is $\overline{R} = (R \bmod 2^w) + 2^w$ for a group element $R$ written as an integer (for a curve point, its $x$-coordinate).

## In plain words

Each person has a long-term key that everybody knows belongs to them, and for each conversation each makes a fresh random key as well. MQV mixes the two keys of each person into one number, in a way that only that person can compute. Then the two people do a Diffie-Hellman exchange with these mixed numbers.

Because the long-term key is inside the mix, only the real Bob can get the same result as Alice. Nobody has to sign anything. Alice does not get a proof that Bob was there; she only knows that if anyone can read her messages, it is Bob. That is called implicit authentication.

The trick that makes MQV fast is that the long-term key enters with a short multiplier, half the usual length, so the extra work is small.

## The problem

Two parties with certified static Diffie-Hellman public keys want a fresh shared key over a network controlled by an adversary, with [key compromise impersonation](/key-compromise-impersonation/) resistance and [forward secrecy](/perfect-forward-secrecy/) where possible, at a cost close to that of plain Diffie-Hellman, with only two messages and no signatures. This is the [authenticated key exchange](/authenticated-key-exchange/) problem with implicit authentication.

## The algorithm

Each party sends its ephemeral value ($\hat A$ sends $X$, $\hat B$ sends $Y$; the order does not matter) and then runs MQV-KEY. The pseudocode is $\hat A$'s side; $\hat B$'s side swaps the roles, computing $s_B = y + \overline{Y} b$ and $\sigma = (X A^{\overline{X}})^{h s_B}$.

```pseudo id=main
MQV-KEY(a, x, B, Y)                              ▷ own static a, own ephemeral x; peer's B and Y
L1  X ← g^x                                       ▷ sent to the peer before this call
L2  if B ∉ G or Y ∉ G then fail                   ▷ public key validation
L3  d ← avf(X); e ← avf(Y)                        ▷ avf(R) = (R mod 2^w) + 2^w
L4  s_A ← (x + d · a) mod q                       ▷ the implicit signature of A
L5  σ ← (Y · B^e)^(h · s_A)
L6  if σ = 1 then fail                            ▷ the point at infinity on a curve
L7  return K = KDF(σ, A, B, X, Y)                 ▷ then erase x and s_A
```

The value $s_A$ at line L4 is called an implicit signature: it is a combination of the ephemeral and the static secret, like the response in a Schnorr signature, but nobody verifies it. Instead, $Y \cdot B^e = g^{y + eb} = g^{s_B}$ is $\hat B$'s implicit signature in the exponent, which $\hat A$ can compute from public values at line L5. The value $d$ at line L3 has only $w$ bits, about half of $q$, so $B^e$ costs half an exponentiation. Bit $w$ is set so that $d$ and $e$ are never zero.

The cofactor $h$ at line L5 matters on curves (or subgroups of $\mathbb{Z}_p^*$) with $h > 1$: if only partial validation is done, raising to $h$ removes a small-order component that an attacker put into $Y$. In the code, line L2 checks full membership in the subgroup of order $q$, so $h = 1$.

**About the code.** The Python code of this page uses a 256-bit safe prime with $q$ of 255 bits, so $w = 128$. It is for study only. It is not constant time, and it must not protect real data. Use an SP 800-56A validated module, and prefer HMQV or a signed protocol in new designs. No official MQV test vector was used; the tests check agreement against an independent formula.

## Example

Take the toy group of order $q = 1019$ in $\mathbb{Z}_{2039}^*$ with $g = 4$, so $\lceil \log_2 1019 \rceil = 10$ and $w = 5$.

| value | Alice | Bob |
|---|---|---|
| static | $a = 57$, $A = 1556$ | $b = 311$, $B = 1502$ |
| ephemeral | $x = 100$, $X = 1153$ | $y = 200$, $Y = 2020$ |
| L3 | $d = (1153 \bmod 32) + 32 = 33$, $e = (2020 \bmod 32) + 32 = 36$ | same $d$ and $e$ |
| L4 | $s_A = 100 + 33 \cdot 57 \bmod 1019 = 962$ | $s_B = 200 + 36 \cdot 311 \bmod 1019 = 187$ |
| L5 | $Y B^{36} \bmod 2039 = 612$, $\sigma = 612^{962} \bmod 2039 = 1795$ | $X A^{33} \bmod 2039 = 667$, $\sigma = 667^{187} \bmod 2039 = 1795$ |

Both get $\sigma = 1795 = 4^{962 \cdot 187 \bmod 1019}$.

## Correctness

$Y \cdot B^e = g^y g^{eb} = g^{y + eb} = g^{s_B}$ in $G$, so $\hat A$'s value is $\sigma = g^{s_B \cdot h s_A}$, and $\hat B$'s value is $(X A^d)^{h s_B} = g^{s_A \cdot h s_B}$. Both parties compute the same $d$ and $e$ from the same $X$ and $Y$, so they agree. Exponents can be reduced mod $q$ because $g$ has order $q$. The proof is below.

Security is a different matter. MQV has no reduction to a standard assumption. Law et al. (2003) argue for its security attributes informally. Krawczyk (2005) showed that MQV does not meet the security definitions he used, in particular without a check that the received values lie in $G$, and that the half-length $d$ and $e$ computed from the group elements alone, without identities, are the root of the problems; HMQV changes exactly this.

## Complexity

Line L1 is one exponentiation, which can be done ahead of time. Line L5 costs one half-length exponentiation ($B^e$) and one full one, or about 1.2 full exponentiations with simultaneous multi-exponentiation; line L2 adds one exponentiation per value checked (the static key once per peer). With schoolbook multiplication this is $\Theta(m^3)$ bit operations and $\Theta(m)$ space. Plain DH costs two exponentiations, so MQV gives authentication for about half an exponentiation more, and much less than a signature and its verification.

## Properties

- **Implicit mutual authentication.** Only a party that knows $b$ (and $y$) can compute $\sigma$.
- **Two messages, any order.** The messages do not depend on each other.
- **Key compromise impersonation resistance** is claimed: with $a$ alone, $\mathcal{E}$ still misses the factor $g^{bxe}$ (see [KCI](/key-compromise-impersonation/)).
- **Forward secrecy only in the weak sense.** Like every two-message implicitly authenticated protocol, MQV cannot have full PFS; see [perfect forward secrecy](/perfect-forward-secrecy/).
- **No proof.** Its security rests on heuristic arguments; HMQV has a proof in the random oracle model.

## Variants and improvements

- **One-pass MQV.** The receiver uses its static key in place of an ephemeral one ($y = b$), for store-and-forward settings such as e-mail; it has no forward secrecy for the receiver.
- **ECMQV.** The same protocol on an elliptic curve, with $\overline{R}$ taken from the $x$-coordinate and the cofactor in the exponent.
- **SP 800-56A schemes.** C(2e, 2s) with MQV2 and its one-pass form C(1e, 2s), with the identities in the KDF and optional [key confirmation](/key-confirmation/).
- **HMQV.** [HMQV](/hmqv/) replaces $d$ and $e$ by hashes $H(X, \hat B)$ and $H(Y, \hat A)$, which binds the identities and gives a proof.
- **FHMQV and other successors** add properties such as security under leakage of ephemeral keys.

## When to use it

Use MQV only where a standard or an existing system requires it, with full validation of public keys, identities in the key derivation, and key confirmation. For new designs with static Diffie-Hellman keys, use HMQV-like protocols with proofs, or a [Noise](/noise-protocol-framework/) pattern; with signature keys, use [SIGMA](/sigma-key-exchange/) through IKEv2 or TLS 1.3.

## Pitfalls

- **Unknown key share without identities in the KDF.** Kaliski (2001) showed that if $K = \mathrm{KDF}(\sigma)$ at line L7, an attacker $\hat E$ who sees $X$ can pick $u$, set $X_E = X A^{d} g^{-u}$, and register the static key $E = g^{u / \overline{X_E}}$. Then $X_E E^{\overline{X_E}} = X A^d$, so $\hat B$, talking to $\hat E$ with $X_E$, computes the same $\sigma$ as $\hat A$ talking to $\hat B$. $\hat E$ knows its private key, so proof of possession at the CA does not stop it. Put the identities and the ephemeral values into the KDF at line L7. The tests run this attack.
- **Missing validation.** Without line L2, small-order components in $Y$ or $B$ change $\sigma$ in ways the attacker controls. Either check full membership in $G$, or use partial validation with the cofactor $h$ at line L5.
- **$x$ and $s_A$ not erased after line L7.** If $s_A$ leaks, the attacker can compute $\sigma$ for that session. If $x$ leaks as well, $a = (s_A - x) / d \bmod q$ follows, and with it every later session can be attacked.
- **Patents and deployment.** Certicom held patents on MQV, which slowed its use outside the US government profiles; NSA's Suite B first listed ECMQV and later dropped it.

## Implementations

## History

Menezes, Qu and Vanstone proposed the protocol in 1995. Law, Menezes, Qu, Solinas and Vanstone gave the efficient version with half-length values and the cofactor in Designs, Codes and Cryptography in 2003, after it had entered IEEE 1363-2000 and the ANSI X9.42 and X9.63 standards. Kaliski published the unknown key-share attack in 2001. NIST included MQV in SP 800-56A (2006, revised in 2007 and 2018), and the NSA listed ECMQV in Suite B in 2005 before removing it. Krawczyk's 2005 analysis and HMQV, and Menezes' 2007 reply on HMQV, are the main later work on its security.

## References
