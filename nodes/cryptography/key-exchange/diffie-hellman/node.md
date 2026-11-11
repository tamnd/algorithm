---
tag: 65FYHX
kind: algorithm
slug: diffie-hellman
name: Diffie-Hellman key exchange
aliases:
- DH key exchange
- Diffie-Hellman-Merkle key agreement
area: cryptography/key-exchange
level: intro
summary: Two parties send g^x and g^y mod p over an open channel and both compute g^(xy). An eavesdropper must solve the Diffie-Hellman problem. It needs authentication against active attacks.
solves: [key-agreement-problem]
model: word-ram
complexity:
  vars: {m: the number of binary digits of the prime p}
  time: {worst: Θ(m^3), average: Θ(m^3), best: Θ(m^3)}
  space: {extra: Θ(m)}
properties: {deterministic: false, randomized: true}
history:
  year: 1976
  people: [Whitfield Diffie, Martin Hellman, Ralph Merkle]
  note: Diffie and Hellman published the method in New Directions in Cryptography (1976), building on Merkle's idea of public key distribution. Hellman proposed the name Diffie-Hellman-Merkle in 2002.
prereqs: [key-agreement-problem, modular-exponentiation, cyclic-group]
see_also: [ecdh, x25519, man-in-the-middle-attack, small-subgroup-attack, computational-diffie-hellman, decisional-diffie-hellman, station-to-station-protocol, elgamal-encryption]
sources:
  - paper: doi:10.1109/TIT.1976.1055638
    title: Whitfield Diffie and Martin E. Hellman, New directions in cryptography, IEEE Transactions on Information Theory 22(6), pages 644 to 654, 1976
    locator: Section III (public key distribution systems, the exchange of alpha^x mod q)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 12, Section 12.6.1, Protocol 12.47 (basic Diffie-Hellman key agreement) and Section 12.9.1 (intruder-in-the-middle)
  - url: "https://www.rfc-editor.org/rfc/rfc3526"
    title: Tero Kivinen and Mika Kojo, RFC 3526, More Modular Exponential (MODP) Diffie-Hellman groups for Internet Key Exchange (IKE), May 2003
    locator: Section 3 (the 2048-bit MODP group, group 14)
  - url: "https://www.rfc-editor.org/rfc/rfc7919"
    title: Daniel Kahn Gillmor, RFC 7919, Negotiated Finite Field Diffie-Hellman Ephemeral Parameters for Transport Layer Security (TLS), August 2016
    locator: Section 3 (client behavior and the named groups), Section 5 (peer validation) and Appendix A (the ffdhe groups)
  - paper: doi:10.6028/NIST.SP.800-56Ar3
    title: Elaine Barker, Lily Chen, Allen Roginsky, Apostol Vassilev and Richard Davis, NIST SP 800-56A Rev. 3, Recommendation for Pair-Wise Key-Establishment Schemes Using Discrete Logarithm Cryptography, April 2018
    locator: Section 5.6.2.3.1 (FFC full public-key validation) and Section 5.7.1.1 (the FFC DH primitive)
  - paper: doi:10.1145/2810103.2813707
    title: David Adrian, Karthikeyan Bhargavan, Zakir Durumeric, Pierrick Gaudry, Matthew Green, J. Alex Halderman, Nadia Heninger, Drew Springall, Emmanuel Thomé, Luke Valenta, Benjamin VanderSloot, Eric Wustrow, Santiago Zanella-Béguelin and Paul Zimmermann, Imperfect forward secrecy, how Diffie-Hellman fails in practice, ACM CCS 2015
    locator: the abstract and Section 1 (Logjam downgrade, a week of precomputation for a 512-bit group, then about a minute per discrete logarithm; the estimates for 1024-bit groups)
  - paper: doi:10.1109/MCOM.2002.1006971
    title: Martin E. Hellman, An overview of public key cryptography, IEEE Communications Magazine 40(5), pages 42 to 49, 2002
    locator: the history of the discovery and the proposal to call the method Diffie-Hellman-Merkle key exchange
---

Diffie-Hellman key exchange lets two parties who share no secret agree on a secret over an open channel. In a [cyclic group](/cyclic-group/) of prime order $q$ with generator $g$, Alice sends $g^x$ and Bob sends $g^y$, and each raises the value it receives to its own secret exponent, so both get $g^{xy}$. An eavesdropper sees only $g$, $g^x$ and $g^y$; computing $g^{xy}$ from them is the [computational Diffie-Hellman problem](/computational-diffie-hellman/), believed hard in well-chosen groups. Whitfield Diffie and Martin Hellman published it in 1976, after Ralph Merkle's work on [public key distribution](/merkle-puzzles/), and it is the first practical solution of the [key agreement problem](/key-agreement-problem/). By itself it gives no authentication, so an active [man in the middle](/man-in-the-middle-attack/) can break it.

**Notation.** $p$ is a [safe prime](/safe-prime/), $p = 2q + 1$ with $q$ prime. $G$ is the subgroup of order $q$ of $\mathbb{Z}_p^*$, which is the set of [quadratic residues](/quadratic-residue/) modulo $p$, and $g \in G$ is a generator ($g = 2$ when $p \equiv 7 \pmod 8$). $x$ and $y$ are the secret exponents of Alice and Bob, $X = g^x \bmod p$ and $Y = g^y \bmod p$ their public values, and $Z$ the shared secret. $m = \lceil \log_2 p \rceil$ is the size of $p$ in binary digits.

## In plain words

Alice and Bob agree in public on a large prime number and a base number. Alice picks a secret number and sends the base raised to that power, reduced by the prime. Bob does the same with his own secret number.

Each one then takes the number they got and raises it to their own secret power. Alice computes (Bob's number) to the power of (Alice's secret); Bob computes (Alice's number) to the power of (Bob's secret). Both results are the base raised to the product of the two secrets, so they are equal.

A spy sees the prime, the base and the two sent numbers. To get the shared number, the spy would have to undo a power in modular arithmetic, and no fast method is known for that when the prime is large and well chosen.

## The problem

Two parties with no shared secret exchange messages over a channel that an adversary reads. Each must output the same secret value, which the adversary cannot compute. This is the [key agreement problem](/key-agreement-problem/) against a passive adversary. The group parameters $(p, q, g)$ are public and fixed in advance, for example group 14 of RFC 3526 or a group of RFC 7919.

## The algorithm

Each party runs DH-KEYGEN, sends its public value, and runs DH-SHARED on the value it receives. The two runs are symmetric, and their messages can be sent at the same time.

```pseudo id=main
DH-KEYGEN(p, q, g)                          ▷ p = 2q + 1, g of order q
L1  x ← a uniform integer in [1, q − 1]
L2  X ← g^x mod p
L3  return (x, X)                            ▷ keep x secret, send X

DH-SHARED(x, Y)                             ▷ Y is the peer's public value
L4  if Y < 2 or Y > p − 2 then fail          ▷ reject 0, 1, p − 1 and values out of range
L5  if Y^q mod p ≠ 1 then fail               ▷ Y must lie in the subgroup G
L6  Z ← Y^x mod p
L7  if Z = 1 then fail
L8  return Z as a big-endian string of ⌈m/8⌉ bytes
```

**About the code.** Lines L4 and L5 are the full public-value validation of SP 800-56A Rev. 3 (Section 5.6.2.3.1), and lines L6 to L8 are its FFC DH primitive (Section 5.7.1.1). Line L5 costs one more exponentiation, but it shuts out the [small subgroup attack](/small-subgroup-attack/). In a safe-prime group the elements outside $G$ are exactly the non-residues, $p - 1$ among them, so line L5 is the same as a [Legendre symbol](/legendre-symbol/) test. Line L8 keeps the leading zero bytes, so the length of $Z$ does not depend on its value. $Z$ is not a uniform string, so the parties pass it to a key derivation function such as [HKDF](/hkdf/), with the transcript, before they use it as a [session key](/session-key/). The Python code of this page uses the 2048-bit group 14 of RFC 3526; it is for study only and is not constant time.

## Example

Take $p = 23 = 2 \cdot 11 + 1$, $q = 11$ and $g = 2$. Since $23 \equiv 7 \pmod 8$, 2 is a quadratic residue, and its powers are

$$2^0, \dots, 2^{10} \equiv 1, 2, 4, 8, 16, 9, 18, 13, 3, 6, 12 \pmod{23},$$

the 11 elements of $G$.

| step | Alice | Bob |
|---|---|---|
| L1 | $x = 6$ | $y = 9$ |
| L2 | $X = 2^6 \bmod 23 = 18$ | $Y = 2^9 \bmod 23 = 6$ |
| send | 18 to Bob | 6 to Alice |
| L4 | $2 \le 6 \le 21$ | $2 \le 18 \le 21$ |
| L5 | $6^{11} \bmod 23 = 1$ | $18^{11} \bmod 23 = 1$ |
| L6 | $Z = 6^6 \bmod 23 = 12$ | $Z = 18^9 \bmod 23 = 12$ |

Both get $Z = 12 = 2^{54 \bmod 11} = 2^{10}$. If an attacker sends $Y = 22 = p - 1$, line L4 rejects it; without line L4, Alice's result would be $22^6 \bmod 23 = 1$, a value the attacker knows. If the attacker sends $Y = 5$, a non-residue, line L5 rejects it, since $5^{11} \bmod 23 = 22$.

## Correctness

If both parties are honest, they compute the same value. $G$ is commutative, so $Y^x = (g^y)^x = g^{xy} = (g^x)^y = X^y$. The checks never reject an honest value: $X = g^x$ with $1 \le x \le q - 1$ has order exactly $q$, so $X \ne 1$, $X \ne p - 1$ (which has order 2), $X^q = 1$, and $Z = g^{xy}$ with $q \nmid xy$ is not 1. Conversely, a value $Y$ that passes lines L4 and L5 is a generator of $G$, so the secret $Z = Y^x$ ranges over all of $G \setminus \{1\}$ as $x$ does, and line L7 can never fire after a successful check. The full proof is below.

Security against an eavesdropper is a separate claim. Recovering $Z$ from $(g, X, Y)$ is the [CDH problem](/computational-diffie-hellman/), and telling $Z$ from a random element of $G$ is the [DDH problem](/decisional-diffie-hellman/). DDH is believed hard in the subgroup of quadratic residues of a safe prime, so $Z$ is pseudorandom in $G$, and a good key derivation function turns it into a pseudorandom key.

## Complexity

Each party performs two exponentiations modulo $p$ with exponents below $q$ (lines L2 and L6), plus one for the check of line L5. By [binary exponentiation](/binary-exponentiation/), each costs at most $2m$ multiplications of $m$-digit numbers modulo $p$. With schoolbook multiplication on a [word RAM](/word-ram/) with $w$-digit words, one multiplication costs $\Theta(m^2/w^2)$ word operations, so a party does $\Theta(m^3/w^2)$ work, which is $\Theta(m^3)$ for fixed $w$. [Karatsuba](/karatsuba-multiplication/) and [Montgomery multiplication](/montgomery-multiplication/) lower the constant and the exponent of $m$ in practice. Each party sends one group element, $m$ binary digits, and the protocol has one round. The extra space is $\Theta(m)$.

Many deployments use short exponents of about twice the security level instead of exponents up to $q$; the cost of lines L2 and L6 then falls in proportion to the exponent length. The check of line L5 still needs a full exponent $q$.

**The cost of attacks.** The best known attack computes a discrete logarithm in $\mathbb{Z}_p^*$ with the [number field sieve](/general-number-field-sieve/), in time $L_p[1/3, (64/9)^{1/3}]$, where $L_p[\alpha, c] = \exp\bigl((c + o(1)) (\ln p)^\alpha (\ln \ln p)^{1 - \alpha}\bigr)$. A large part of the work depends only on $p$, so after one precomputation for a prime, each new logarithm is cheap. Generic methods such as [baby-step giant-step](/baby-step-giant-step/) and [Pollard's rho](/pollard-rho-discrete-logarithm/) cost $\Theta(\sqrt{q})$ group operations, and this is optimal in the [generic group model](/generic-group-model/). A 2048-bit $p$ gives about 112 bits of security; a 3072-bit $p$ about 128.

## Properties

- **Contributory.** The key depends on the secrets of both parties.
- **One round, two messages.** The two messages do not depend on each other and can cross on the wire.
- **Forward secrecy when ephemeral.** If both exponents are fresh and erased after use, a later leak of long-term keys does not expose $Z$ ([perfect forward secrecy](/perfect-forward-secrecy/)).
- **Unauthenticated.** Nothing ties $X$ or $Y$ to a person; see [man in the middle attack](/man-in-the-middle-attack/).
- **Randomized.** Each run picks new exponents, unless a party uses a static key.

## Variants and improvements

- **Elliptic curves.** The same protocol in the group of points of an elliptic curve gives [ECDH](/ecdh/), with much shorter keys for the same security; [X25519](/x25519/) and [X448](/x448/) are the common forms.
- **Static and ephemeral keys.** A party may keep a long-term key pair (static DH) to get implicit authentication, as in the unified model, [MQV](/mqv/) and [HMQV](/hmqv/).
- **Authenticated DH.** Signatures or MACs over the transcript give the [station-to-station protocol](/station-to-station-protocol/), [SIGMA](/sigma-key-exchange/) (used in IKE and TLS 1.3), and the [Noise](/noise-protocol-framework/) patterns.
- **Many parties.** [Group Diffie-Hellman](/group-diffie-hellman/) and tree-based variants extend the idea to groups.
- **Public-key encryption.** Fixing one message as a public key gives [ElGamal encryption](/elgamal-encryption/).

## When to use it

Use finite-field Diffie-Hellman only where a protocol requires it, such as older IKE or SSH set-ups, and then only with a standard group of at least 2048 binary digits, like the RFC 7919 or RFC 3526 groups. For new designs, [X25519](/x25519/) gives the same function with keys of 32 bytes and much faster code. In both cases add authentication, and derive keys with a KDF.

## Pitfalls

- **No authentication.** Plain DH falls to a [man in the middle](/man-in-the-middle-attack/). Sign the transcript or use a static authenticated key.
- **No validation.** Without lines L4 and L5, a peer can send $p - 1$ or an element of small order and fix the key or learn the secret exponent bit by bit ([small subgroup attack](/small-subgroup-attack/)). This matters most when $p - 1$ has many small factors, as in DSA-style groups.
- **Small or shared primes.** Logjam (Adrian et al., CCS 2015) downgraded TLS connections to 512-bit export groups. After a precomputation of about a week for one 512-bit group, the authors computed each discrete logarithm in about a minute. They estimated that a nation-state could do the precomputation for a 1024-bit prime, and that one such prime would expose 18% of popular HTTPS sites. Use groups of 2048 digits or more.
- **Raw Z as a key.** $Z$ is an element of $G$, not a uniform string. Hash it with the transcript.
- **Leading zero bytes.** TLS 1.2 strips the leading zero bytes of $Z$ (RFC 5246, Section 8.1.2), so the time of the following hash depends on the secret; the Raccoon attack of 2020 used this. Keep the fixed length of line L8, as TLS 1.3 does.
- **Timing.** Python's `pow` and most big-integer libraries are not constant time. Real code needs a constant-time exponentiation.

## Implementations

## History

Diffie and Hellman published the protocol in November 1976 in *New Directions in Cryptography*, which also proposed public-key encryption and digital signatures. Ralph Merkle had found an earlier form of public key distribution, [Merkle's puzzles](/merkle-puzzles/), as a student in 1974, published in 1978. In 2002 Hellman proposed the name Diffie-Hellman-Merkle key exchange to credit Merkle. At GCHQ in the United Kingdom, Malcolm Williamson found the same method in the mid-1970s, but the work stayed secret until 1997. The Internet standards followed: the Oakley groups and IKE in the 1990s, RFC 3526 in 2003, and the negotiated groups of RFC 7919 in 2016. Logjam (2015) led browsers to reject groups under 1024 digits and then to drop finite-field DH in TLS in favour of elliptic curves.

## References
