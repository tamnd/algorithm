---
tag: J4FG25
kind: algorithm
slug: x448
name: X448
aliases:
- Curve448 ECDH
area: cryptography/key-exchange
level: advanced
summary: The Diffie-Hellman function on Curve448 (RFC 7748). Like X25519 it clamps the scalar and runs the Montgomery ladder, over p = 2^448 - 2^224 - 1, for about 224 bits of security.
solves: [key-agreement-problem]
model: word-ram
complexity:
  vars: {m: "the number of binary digits of the field prime p (448 for X448)"}
  time: {worst: Θ(m^3), average: Θ(m^3), best: Θ(m^3)}
  space: {extra: Θ(m)}
properties: {deterministic: true}
history:
  year: 2015
  people: [Mike Hamburg]
  note: Hamburg proposed the Goldilocks curve over p = 2^448 - 2^224 - 1 in 2015. RFC 7748 (2016) standardized its Montgomery form as Curve448 and the function X448.
prereqs: [x25519]
see_also: [x25519, ecdh, diffie-hellman, hybrid-key-exchange, small-subgroup-attack, elliptic-curve-cryptography, karatsuba-multiplication, tls-handshake]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc7748"
    title: Adam Langley, Mike Hamburg and Sean Turner, RFC 7748, Elliptic Curves for Security, January 2016
    locator: Section 4.2 (curve448), Section 5 (the X448 function and decodeScalar448), Section 5.2 (test vectors) and Section 6.2 (Diffie-Hellman with Curve448)
  - url: "https://eprint.iacr.org/2015/625"
    title: Mike Hamburg, Ed448-Goldilocks, a new elliptic curve, IACR Cryptology ePrint Archive 2015/625
    locator: the choice of the prime p = 2^448 - 2^224 - 1, its fast reduction, and the curve parameters
  - paper: doi:10.1007/11745853_14
    title: Daniel J. Bernstein, Curve25519, new Diffie-Hellman speed records, PKC 2006, LNCS 3958, pages 207 to 228
    locator: the design of the Montgomery-ladder Diffie-Hellman function that X448 follows (clamping, twist security, no validation)
  - paper: doi:10.1090/S0025-5718-1987-0866113-7
    title: Peter L. Montgomery, Speeding the Pollard and elliptic curve methods of factorization, Mathematics of Computation 48(177), pages 243 to 264, 1987
    locator: Section 10 (curves By^2 = x^3 + Ax^2 + x and the x-only formulas)
---

X448 is the [Diffie-Hellman](/diffie-hellman/) function on Curve448, the Montgomery curve $v^2 = u^3 + 156326u^2 + u$ over $\mathbb{F}_p$ with $p = 2^{448} - 2^{224} - 1$. It is the same algorithm as [X25519](/x25519/), the clamped Montgomery ladder on the $u$-coordinate, with 56-byte keys and a larger field, and it gives about 224 bits of security instead of about 128. RFC 7748 standardizes it, and TLS 1.3 (RFC 8446) and SSH (RFC 8731) offer it for users who want a margin above the 128-bit level.

**Notation.** $E$ is Curve448, with $A = 156326$ and $a_{24} = (A - 2)/4 = 39081$. $\#E(\mathbb{F}_p) = 4\ell$ with $\ell = 2^{446} - \texttt{0x8335dc163bb124b65129c96fde933d8d723a70aadc873d6d54a7bb0d}$ prime, so the cofactor is 4. The base point has $u = 5$ and order $\ell$. $u(O) = 0$ by convention, and $m$ is the size of $p$ in binary digits.

## In plain words

X448 does the same job as X25519 with bigger numbers. Each private key is 56 random bytes, and each public key is a fixed starting point "multiplied" by the private key, also 56 bytes.

The steps are the same as in X25519: walk through the key bits, keep two points, and for each bit double one and add the two, with the same work for every bit. Two bits of the key are cleared and the top bit is set before use, so any 56 bytes are a safe public key and no check is needed.

The numbers are almost twice as long, so the work is several times larger, and the work of an attacker is far larger still.

## The problem

Two parties exchange 56-byte public keys and must each compute the same 56-byte secret that an eavesdropper cannot compute: the [key agreement problem](/key-agreement-problem/). Alice's public key is $X448(a, 5)$, Bob's is $X448(b, 5)$, and both compute $X448(a, X448(b, 5)) = X448(b, X448(a, 5))$ (RFC 7748, Section 6.2).

## The algorithm

```pseudo id=main
X448(k, u)                                      ▷ two 56-byte strings, RFC 7748 Section 5
L1  k ← DECODE-SCALAR(k)                        ▷ clear bits 0 and 1, set bit 447
L2  x1 ← DECODE-U(u) mod p                      ▷ all 448 bits are used, then reduce
L3  (x2, z2, x3, z3, swap) ← (1, 0, x1, 1, 0)    ▷ (x2 : z2) = O, (x3 : z3) = the input point
L4  for t ← 447 down to 0 do
L5      k_t ← bit t of k
L6      swap ← swap ⊕ k_t
L7      CSWAP(swap, x2, x3); CSWAP(swap, z2, z3)
L8      swap ← k_t
L9      (x2, z2, x3, z3) ← LADDER-STEP(x1, x2, z2, x3, z3)
L10 CSWAP(swap, x2, x3); CSWAP(swap, z2, z3)
L11 return ENCODE-U(x2 · z2^(p − 2) mod p)      ▷ 56 little-endian bytes
```

**About the code.** LADDER-STEP is the one on the [X25519](/x25519/) page with $a_{24} = 39081$: it doubles $(x_2 : z_2)$ and adds the two points, using $x_1$, the $u$-coordinate of their difference. The two slots hold $mP$ and $(m + 1)P$ for the prefix $m$ of the scalar, and the lazy swap of lines L6 to L8 keeps track of their order. Clamping makes $k$ a multiple of the cofactor 4 and fixes bit 447, so the loop always runs 448 times. Unlike X25519, no bit of $u$ is masked, since 448 bits fill 56 bytes exactly; values from $p$ to $2^{448} - 1$ are reduced. Line L11 inverts by [Fermat's little theorem](/fermat-little-theorem/) and maps $z_2 = 0$ to 0. The Python code checks every vector of RFC 7748 Section 5.2 except the 1,000,000-iteration one, and the Section 6.2 example. It is for study only and is not constant time.

## Example

**RFC 7748, Section 6.2.** Alice's private key begins `9a8f4925d1519f57` and her public key, $X448(a, 5)$, is

$$\texttt{9b08f7cc31b7e3e67d22d5aea121074a273bd2b83de09c63faa73d2c22c5d9bbc836647241d953d40c5b12da88120d53177f80e532c41fa0}.$$

Bob's private key begins `1c306a7ac2a0e2e0` and his public key begins `3eb7a829b0cd20f5`. Both compute the shared secret

$$K = \texttt{07fff4181ac6cc95ec1c16a94a0f74d12da232ce40a77552281d282bb60c0b56fd2464c335543936521c24403085d59a449a5037514a879d}.$$

**Clamping.** Alice's first byte `0x9a` becomes `0x98` (bits 0 and 1 cleared), and her last byte `0x6b` becomes `0xeb` (bit 7 set).

**Small-order input.** For $u = 0$ (the point of order 2) or $u = 1$, and for their non-canonical forms $u = p$ and $u = p + 1$, the clamped scalar is a multiple of 4, so the output is 56 zero bytes for every key.

## Correctness

The proof is the one for [X25519](/x25519/), with $A = 156326$, $p = 2^{448} - 2^{224} - 1$ and 448 steps. Montgomery's formulas give $u(2R)$ from $u(R)$ and $u(R + S)$ from $u(R)$, $u(S)$ and $u(S - R)$; the ladder keeps the invariant that the two slots hold $u(mP)$ and $u((m + 1)P)$, where $m$ is the part of the scalar read so far; and after the last bit $m = k$. For a point $P$ of odd prime order the output is therefore $u(kP)$, and

$$X448(a, X448(b, 5)) = u(ab \cdot P_0) = X448(b, X448(a, 5)).$$

The full proof is below.

## Complexity

The loop has 448 steps, each with 5 multiplications, 4 squarings and one multiplication by $a_{24}$ in $\mathbb{F}_p$, and the inversion costs about 447 squarings and a few more multiplications: about 5,000 field operations, the same for every input. With schoolbook arithmetic each field operation costs $\Theta(m^2)$, so the time is $\Theta(m^3)$ and the state is $\Theta(m)$. The special form of $p$ lets a product be reduced with additions only: with $\varphi = 2^{224}$, $p = \varphi^2 - \varphi - 1$, so $\varphi^2 \equiv \varphi + 1$, and [Karatsuba](/karatsuba-multiplication/) splitting at $\varphi$ is cheap.

The best known attack is [Pollard's rho](/pollard-rho-discrete-logarithm/) in the subgroup of order $\ell \approx 2^{446}$, about $2^{223}$ group operations. A large quantum computer running [Shor's algorithm](/shor-algorithm/) breaks X448 as well as X25519.

## Properties

- **Every input is valid.** Any 56-byte string gives a $u$ on $E$ or on its twist, and the ladder is correct on both.
- **Twist secure.** The twist has order $4\ell'$ with $\ell'$ prime, so clamping to a multiple of 4 removes all small-order leakage.
- **Uniform and constant-time friendly**, as for X25519.
- **Deterministic** as a function; key generation draws 56 random bytes.

## Variants and improvements

- **[X25519](/x25519/)** is the faster, more common choice at the 128-bit level.
- **Ed448** signatures (RFC 8032) use the Edwards form of the same curve, Ed448-Goldilocks.
- **Decaf** (decaf448) builds a prime-order group from the curve by a special encoding, which removes the cofactor in protocols that need one.
- **Hybrid post-quantum** use joins X448 with a post-quantum KEM and feeds both secrets to one KDF ([hybrid key exchange](/hybrid-key-exchange/)).

## When to use it

Use X448 when a policy asks for more than 128-bit security from the classical key exchange, for example to pair with AES-256 and SHA-512, or for long-lived secrets. In most other cases [X25519](/x25519/) is faster and enough, and against quantum attackers neither helps: add a post-quantum KEM.

## Pitfalls

- **Not masking is correct here.** Code ported from X25519 that clears the top bit of $u$ is wrong for X448.
- **Skipping the all-zero check.** As for X25519, small-order inputs give an all-zero output; protocols that need both parties to contribute must reject it.
- **Constant time.** The field arithmetic and CSWAP must not branch on secret data. The Python code does not meet this.
- **Raw output as a key.** Feed the output and the transcript to a KDF such as [HKDF](/hkdf/).

## Implementations

## History

Mike Hamburg proposed the Goldilocks curve over $p = 2^{448} - 2^{224} - 1$ in 2015, choosing a prime whose shape makes Karatsuba multiplication and reduction cheap. The IRTF Crypto Forum Research Group selected it with Curve25519, and RFC 7748 (January 2016) defined X25519 and X448. RFC 8032 (2017) added Ed448, and TLS 1.3 (RFC 8446, 2018) lists x448 as a named group.

## References
