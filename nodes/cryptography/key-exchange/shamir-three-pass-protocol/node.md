---
tag: 76HQ6M
kind: algorithm
slug: shamir-three-pass-protocol
name: Shamir's three-pass protocol
aliases:
- no-key protocol
area: cryptography/key-exchange
level: advanced
summary: Alice sends Bob a secret in three messages with no shared or public keys. Each locks it with a private exponent mod p, and the locks commute, so each can remove only their own lock.
solves: [key-transport-problem]
model: word-ram
complexity:
  vars: {m: the number of binary digits of the prime p}
  time: {worst: Θ(m^3), average: Θ(m^3), best: Θ(m^3)}
  space: {extra: Θ(m)}
properties: {deterministic: false, randomized: true}
history:
  year: 1980
  people: [Adi Shamir, Jim K. Omura, James L. Massey]
  note: Shamir's unpublished protocol of about 1980 was described by Konheim in 1981. Omura, and later Massey and Omura, proposed the exponentiation cipher for it.
prereqs: [key-transport-problem, modular-exponentiation, extended-euclidean-algorithm]
see_also: [key-transport-problem, diffie-hellman, elgamal-encryption, one-time-pad, man-in-the-middle-attack, legendre-symbol, pohlig-hellman, safe-prime]
sources:
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 12.3.1 (iii), Protocol 12.22 (Shamir's no-key protocol) and Remark 12.23 (the Vernam cipher fails), and the chapter notes in Section 12.10 on its attribution
  - paper: doi:10.1109/TIT.1978.1055817
    title: Stephen C. Pohlig and Martin E. Hellman, An improved algorithm for computing logarithms over GF(p) and its cryptographic significance, IEEE Transactions on Information Theory 24(1), pages 106 to 110, 1978
    locator: the exponentiation cipher C = M^e mod p with e a unit mod p - 1, and the need for p - 1 to have a large prime factor
  - url: "https://www.rfc-editor.org/rfc/rfc3526"
    title: Tero Kivinen and Mika Kojo, RFC 3526, More Modular Exponential (MODP) Diffie-Hellman groups for Internet Key Exchange (IKE), May 2003
    locator: Section 3 (the 2048-bit MODP group, the prime used by the code)
---

Shamir's three-pass protocol is a [key transport](/key-transport-problem/) protocol in which Alice sends a secret to Bob in three messages over a public channel, with no shared key and no public key. It uses a commutative cipher: Alice locks the secret, Bob adds his own lock, Alice removes hers, and Bob removes his. With the Massey-Omura cipher $x \mapsto x^a \bmod p$, each lock is a [modular exponentiation](/modular-exponentiation/) with a private exponent, and an eavesdropper must solve a [discrete logarithm](/discrete-logarithm-problem/)-type problem. Like plain [Diffie-Hellman](/diffie-hellman/) it resists only passive attackers, and it needs three messages and four exponentiations where Diffie-Hellman needs two messages.

**Notation.** $p$ is a large prime, public and shared. Alice's lock is an integer $a$ with $\gcd(a, p - 1) = 1$, and $a' = a^{-1} \bmod (p - 1)$ is her key to remove it; Bob has $b$ and $b'$ in the same way. $m$, with $2 \le m \le p - 2$, is the secret. All powers are taken modulo $p$, and $m$ in the complexity is the size of $p$ in binary digits.

## In plain words

Alice wants to send Bob a secret in a box, but they have no common key. She puts her own padlock on the box and sends it. Bob cannot open it, so he adds his padlock too and sends it back.

Alice now removes her padlock, which leaves only Bob's, and sends the box again. Bob removes his padlock and reads the secret.

The box always has at least one padlock on it while it travels. The trick needs locks that can be taken off in any order, and raising a number to a secret power works like that. But nothing tells Alice that the second padlock really belongs to Bob.

## The problem

Alice holds a secret $m$, such as a session key. She and Bob share nothing except public parameters, and Eve reads every message. Alice must give $m$ to Bob so that Eve cannot compute it. This is [key transport](/key-transport-problem/) with no prior keys, against a passive adversary.

## The algorithm

```pseudo id=main
THREE-PASS(m)                                ▷ p is public; 2 ≤ m ≤ p − 2
L1  check 2 ≤ m ≤ p − 2
L2  each party picks a lock e at random with gcd(e, p − 1) = 1 (Alice a, Bob b)
L3  each computes its unlock key e' ← e^(−1) mod (p − 1) (Alice a', Bob b')
L4  Alice → Bob:  c1 ← m^a mod p
L5  Bob → Alice:  c2 ← c1^b mod p
L6  Alice → Bob:  c3 ← c2^(a') mod p
L7  Bob:          m ← c3^(b') mod p
```

**About the code.** The locks commute because $(m^a)^b = m^{ab} = (m^b)^a$, and $x^{a a'} = x$ for $x \ne 0$ by [Fermat's little theorem](/fermat-little-theorem/), since $a a' \equiv 1 \pmod{p - 1}$. Lines L2 and L3 draw $a$ until the gcd test passes and invert it with the [extended Euclidean algorithm](/extended-euclidean-algorithm/). Line L1 excludes $0$, $1$ and $p - 1$, which no odd lock changes. The code uses the 2048-bit [safe prime](/safe-prime/) of RFC 3526, Section 3. It also has the XOR version of the same three passes, which round-trips but leaks $m$, and a test in which Mallory plays Bob. It is for study only, not constant time, and has no authentication.

## Example

Take $p = 23$, so $p - 1 = 22$. Alice picks $a = 5$, and $a' = 9$ since $5 \cdot 9 = 45 = 2 \cdot 22 + 1$. Bob picks $b = 7$, and $b' = 19$ since $7 \cdot 19 = 133 = 6 \cdot 22 + 1$. The secret is $m = 10$.

| pass | computation | value on the wire |
|---|---|---|
| L4 | $10^5 \bmod 23$ | $c_1 = 19$ |
| L5 | $19^7 \bmod 23$ | $c_2 = 15$ |
| L6 | $15^9 \bmod 23$ | $c_3 = 14 = 10^7 \bmod 23$ |
| L7 | $14^{19} \bmod 23$ | $10$, which Bob keeps |

Since 10 is not a square modulo 23, none of 19, 15 and 14 is a square either: this is the one-bit leak described in Pitfalls.

**The XOR version fails.** With one-time pads $k_A$ and $k_B$ as locks, the wire carries $m \oplus k_A$, $m \oplus k_A \oplus k_B$ and $m \oplus k_B$, and the XOR of the three is $m$ (HAC, Remark 12.23). The locks commute, but they do not hide the message once Eve combines all three passes.

## Correctness

Bob's output is $c_3^{b'} = m^{a b a' b'}$. Since $a a' \equiv 1$ and $b b' \equiv 1 \pmod{p - 1}$, the exponent is $\equiv 1 \pmod{p - 1}$, and $m^{p - 1} = 1$ for $m \ne 0$, so the output is $m$. Each step is a bijection of $\{1, \dots, p - 1\}$, so no information is lost on the way. The full proof is below.

**Security, in brief.** If Eve can compute discrete logarithms modulo $p$, she finds $b$ from $c_2 = c_1^b$ and then $m = c_3^{b^{-1}}$. So $p - 1$ must have a large prime factor, as for Diffie-Hellman ([Pohlig-Hellman](/pohlig-hellman/)). The reverse reduction is not known: breaking the protocol means finding $m$ from $(m^a, m^{ab}, m^b)$, a problem close to computational Diffie-Hellman with base $m$.

## Complexity

Each party does two exponentiations modulo $p$ with exponents of about $m$ binary digits, which is $\Theta(m^3)$ time with schoolbook multiplication, plus one inversion modulo $p - 1$ in $O(m^2)$ and an expected constant number of gcd tests, since the fraction $\varphi(p - 1)/(p - 1)$ of units is at least about $1/(e^{\gamma} \ln\ln p)$, and close to $1/2$ for a safe prime. Space is $\Theta(m)$. The protocol has three messages of $m$ binary digits each, against two for Diffie-Hellman.

## Properties

- **No prior keys.** Neither shared secrets nor public keys are needed; the prime is a public parameter.
- **Key transport.** Alice chooses $m$; Bob has no influence on it.
- **Passive security only.** Anyone who answers the first message gets $m$.
- **Randomized**: the locks must be fresh and secret.

## Variants and improvements

- **Elliptic curve form.** The Massey-Omura idea works in any group of known order $n$: the locks are units modulo $n$ and the message is a point.
- **Messages in a subgroup.** Encoding $m$ as a square modulo a safe prime, and drawing locks modulo $q = (p - 1)/2$, removes the Legendre-symbol leak.
- **[ElGamal](/elgamal-encryption/) with a fresh key.** Bob sends a fresh public key, and Alice sends $m$ encrypted to it; HAC notes that this does the same job in two passes, with the roles reversed.
- **Diffie-Hellman.** For a key that both parties may shape, Diffie-Hellman is shorter and more studied.

## When to use it

In practice, almost never: [Diffie-Hellman](/diffie-hellman/) or [ElGamal](/elgamal-encryption/) does the same job with fewer messages, and real protocols need authentication anyway. The protocol is a good teaching example of commutative encryption, and the same idea appears in protocols for mental poker and private set intersection, where commutative locks let parties compare or shuffle values without showing them.

## Pitfalls

- **No authentication.** A [man in the middle](/man-in-the-middle-attack/) plays Bob to Alice, gets $m$, and plays Alice to Bob.
- **The wrong cipher.** XOR, or any cipher where the three messages can be combined, gives $m$ to Eve. The cipher must be secure even when the same message is seen under the locks $a$, $ab$ and $b$.
- **The Legendre symbol leaks one bit.** Every lock is odd, since $p - 1$ is even, so each $c_i$ is a square modulo $p$ exactly when $m$ is (see the [Legendre symbol](/legendre-symbol/)). If $m$ is a key, hash it before use.
- **Fixed points.** $1$ and $p - 1$ pass through unchanged, so they must not be messages.
- **A weak prime.** If $p - 1$ has only small prime factors, [Pohlig-Hellman](/pohlig-hellman/) finds $b$ from $c_1$ and $c_2$, and then $m$. Use a [safe prime](/safe-prime/).

## Implementations

## History

Adi Shamir devised the protocol around 1980 and did not publish it; HAC (Section 12.10) reports that Konheim's book of 1981 attributes it to him. Massey notes that Jim Omura, who knew Shamir's generic protocol, independently proposed to implement it with the exponentiation cipher of Pohlig and Hellman, and Massey and Omura later patented a version over finite fields of characteristic 2, now called the Massey-Omura cryptosystem. HAC presents it as Shamir's no-key protocol.

## References
