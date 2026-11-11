---
tag: J2GJN1
kind: algorithm
slug: x25519
name: X25519
aliases:
- Curve25519 ECDH
area: cryptography/key-exchange
level: core
summary: The Diffie-Hellman function on Curve25519 (RFC 7748). It clamps a 32-byte scalar and runs the Montgomery ladder on the u-coordinate, with no point validation needed.
solves: [key-agreement-problem]
model: word-ram
complexity:
  vars: {m: the number of binary digits of the field prime p (255 for X25519)}
  time: {worst: Θ(m^3), average: Θ(m^3), best: Θ(m^3)}
  space: {extra: Θ(m)}
properties: {deterministic: true}
history:
  year: 2006
  people: [Daniel J. Bernstein]
  note: Bernstein defined Curve25519 and its Diffie-Hellman function at PKC 2006. RFC 7748 (2016, Langley, Hamburg and Turner) standardized it as X25519.
prereqs: [diffie-hellman, elliptic-curve-cryptography]
see_also: [x448, ecdh, diffie-hellman, hybrid-key-exchange, ed25519, small-subgroup-attack, noise-protocol-framework, tls-handshake]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc7748"
    title: Adam Langley, Mike Hamburg and Sean Turner, RFC 7748, Elliptic Curves for Security, January 2016
    locator: Section 4.1 (curve25519), Section 5 (the X25519 function, decodeScalar25519 and the ladder), Section 5.2 (test vectors) and Section 6.1 (Diffie-Hellman with Curve25519 and the all-zero check)
  - paper: doi:10.1007/11745853_14
    title: Daniel J. Bernstein, Curve25519, new Diffie-Hellman speed records, PKC 2006, LNCS 3958, pages 207 to 228
    locator: the definition of the Curve25519 function, the choice of the curve, the security against twist and small-subgroup attacks, and the x-coordinate ladder formulas
  - paper: doi:10.1090/S0025-5718-1987-0866113-7
    title: Peter L. Montgomery, Speeding the Pollard and elliptic curve methods of factorization, Mathematics of Computation 48(177), pages 243 to 264, 1987
    locator: Section 10 (curves By^2 = x^3 + Ax^2 + x and the x-only formulas for doubling and differential addition)
  - paper: doi:10.1007/s13389-017-0157-6
    title: Craig Costello and Benjamin Smith, Montgomery curves and their arithmetic, Journal of Cryptographic Engineering 8, pages 227 to 240, 2018
    locator: the sections on x-only arithmetic and the Montgomery ladder
  - url: "https://www.rfc-editor.org/rfc/rfc8448"
    title: Martin Thomson, RFC 8448, Example Handshake Traces for TLS 1.3, January 2019
    locator: Section 3 (the X25519 key shares and the shared secret of the simple 1-RTT handshake)
---

X25519 is the [Diffie-Hellman](/diffie-hellman/) function on Curve25519, the [elliptic curve](/elliptic-curve-cryptography/) $v^2 = u^3 + 486662u^2 + u$ over $\mathbb{F}_p$ with $p = 2^{255} - 19$. It takes a 32-byte secret scalar and the 32-byte $u$-coordinate of a point, and returns the $u$-coordinate of the scalar multiple, computed with the Montgomery ladder. Daniel Bernstein designed it in 2006 so that a simple, constant-time program is also a correct and safe one: every 32-byte string is a valid public key, the scalar is clamped, and no point validation is needed. RFC 7748 standardizes it, and it is widely used in TLS 1.3, SSH, WireGuard and Signal.

**Notation.** $E$ is Curve25519, a Montgomery curve $Bv^2 = u^3 + Au^2 + u$ with $A = 486662$ and $B = 1$. $\#E(\mathbb{F}_p) = 8\ell$ with $\ell = 2^{252} + 27742317777372353535851937790883648493$ prime, so the cofactor is 8. The base point $P_0$ has $u = 9$ and order $\ell$. For a point $P$, $u(P)$ is its $u$-coordinate, with $u(O) = 0$ by convention. $k$ is a scalar, $a_{24} = (A - 2)/4 = 121665$, and $m$ is the size of $p$ in binary digits.

## In plain words

X25519 is Diffie-Hellman on one fixed, carefully chosen elliptic curve. Each private key is 32 random bytes. The public key is a fixed starting point "multiplied" by the private key, and it is also 32 bytes.

The function only uses one coordinate of each point, and it walks through the bits of the key with the same steps for every bit: it keeps two points, and at each step it doubles one and adds the two. The steps do not depend on the key bits, so a careful program takes the same time for every key.

Before use, a few bits of the private key are forced to fixed values. Because of this and the choice of curve, any 32 bytes are a safe input: the function never needs to check that a public key is "on the curve".

## The problem

Two parties exchange 32-byte public keys and must each compute the same 32-byte secret that an eavesdropper cannot compute: the [key agreement problem](/key-agreement-problem/). Alice's public key is $X25519(a, 9)$, Bob's is $X25519(b, 9)$, and the shared secret is $X25519(a, X25519(b, 9)) = X25519(b, X25519(a, 9))$ (RFC 7748, Section 6.1).

## The algorithm

```pseudo id=main
X25519(k, u)                                    ▷ two 32-byte strings, RFC 7748 Section 5
L1  k ← DECODE-SCALAR(k)                        ▷ clear bits 0, 1, 2 and 255, set bit 254
L2  x1 ← DECODE-U(u) mod p                      ▷ clear bit 255 of u, then reduce
L3  (x2, z2, x3, z3, swap) ← (1, 0, x1, 1, 0)    ▷ (x2 : z2) = O, (x3 : z3) = the input point
L4  for t ← 254 down to 0 do
L5      k_t ← bit t of k
L6      swap ← swap ⊕ k_t
L7      CSWAP(swap, x2, x3); CSWAP(swap, z2, z3)
L8      swap ← k_t
L9      (x2, z2, x3, z3) ← LADDER-STEP(x1, x2, z2, x3, z3)
L10 CSWAP(swap, x2, x3); CSWAP(swap, z2, z3)
L11 return ENCODE-U(x2 · z2^(p − 2) mod p)      ▷ 32 little-endian bytes
```

LADDER-STEP doubles the point $(x_2 : z_2)$ and adds the two points, using $x_1$, the $u$-coordinate of their difference:

$$\begin{aligned} A &= x_2 + z_2, & B &= x_2 - z_2, & E &= A^2 - B^2, & C &= x_3 + z_3, & D &= x_3 - z_3,\\ x_3' &= (DA + CB)^2, & z_3' &= x_1 (DA - CB)^2, & x_2' &= A^2 B^2, & z_2' &= E\,(A^2 + a_{24} E). \end{aligned}$$

**About the code.** Points are kept in projective form $(X : Z)$ with $u = X/Z$, and $O = (1 : 0)$, so the loop has no inversion; line L11 does one, by Fermat's little theorem, and maps $Z = 0$ to the output 0. The two slots always hold $mP$ and $(m+1)P$ for the prefix $m$ of the scalar; line L7 swaps them when the next bit differs from the last, so that LADDER-STEP always doubles the first slot. CSWAP uses a mask, $\mathrm{dummy} = (-\mathrm{swap}) \wedge (x_2 \oplus x_3)$, instead of a branch. Clamping in line L1 makes $k$ a multiple of the cofactor 8 and fixes bit 254, so the loop always runs 255 times. The Python code checks every vector of RFC 7748 Section 5.2 except the 1,000,000-iteration one, the Section 6.1 example and the RFC 8448 TLS 1.3 trace. It is for study only and is not constant time, since Python integers leak timing through their size.

## Example

**The ladder on a short scalar.** For $k = 13 = 1101_2$ and a point $P$, the two slots $(R_0, R_1)$ go through

| bit | 1 | 1 | 0 | 1 |
|---|---|---|---|---|
| after the step | $(P, 2P)$ | $(3P, 4P)$ | $(6P, 7P)$ | $(13P, 14P)$ |

starting from $(O, P)$. A bit 0 doubles $R_0$ and sets $R_1 = R_0 + R_1$; a bit 1 sets $R_0 = R_0 + R_1$ and doubles $R_1$. The difference $R_1 - R_0$ is always $P$, so the $x$-only addition formula, which needs $u(R_1 - R_0)$, always has it as $x_1$.

**RFC 7748, Section 6.1.** Alice's private key is

$$a = \texttt{77076d0a7318a57d3c16c17251b26645df4c2f87ebc0992ab177fba51db92c2a}.$$

$X25519(a, 9)$ gives her public key `8520f0098930a754748b7ddcb43ef75a0dbf3a0d26381af4eba4a98eaa9b4e6a`. Bob's private key `5dab087e...ff88e0eb` gives `de9edb7d7b7dc1b4d35b61c2ece435373f8343c85b78674dadfc7e146f882b4f`. Both then compute the shared secret

$$K = \texttt{4a5d9d5ba4ce2de1728e3bf480350f25e07e21c947d19e3376f09b3c1e161742}.$$

**Clamping.** The first byte of $a$ is `0x77`; line L1 clears its low three bits and gives `0x70`. The last byte `0x2a` has bit 7 clear already, and bit 6 is set, giving `0x6a`.

## Correctness

The ladder keeps the invariant that after the bits $k_{254} \dots k_t$ have been processed, the two slots hold $u(mP)$ and $u((m+1)P)$ in projective form, where $m = \lfloor k/2^t \rfloor$; the lazy swap of lines L6 to L8 keeps track of which slot holds which. After the last bit, $m = k$. The two formulas of LADDER-STEP are Montgomery's: $u(2R) = (u^2 - 1)^2 / (4u(u^2 + Au + 1))$, and $u(R + S)\,u(R - S) = (u(R)u(S) - 1)^2 / (u(R) - u(S))^2$. So for a point $P$ of odd prime order, such as an honest public key, the output is $u(kP)$, and then

$$X25519(a, X25519(b, 9)) = u(a \cdot b \cdot P_0) = X25519(b, X25519(a, 9)).$$

The full proof, with the special cases where a slot holds $O$, is below.

## Complexity

The loop has exactly 255 steps. Each LADDER-STEP costs 5 multiplications, 4 squarings and one multiplication by the small constant $a_{24}$ in $\mathbb{F}_p$; the final inversion costs about 254 squarings and 11 multiplications. That is about 2,800 field operations, the same for every input. With schoolbook arithmetic on $m$-digit numbers, each field operation costs $\Theta(m^2)$, and the ladder has $m$ steps, so the time is $\Theta(m^3)$. The state is five field elements, $\Theta(m)$ space. Public keys and shared secrets are 32 bytes.

The best known attack is [Pollard's rho](/pollard-rho-discrete-logarithm/) in the subgroup of order $\ell \approx 2^{252}$, which takes about $2^{126}$ group operations; RFC 7748 rates the curve at about 128 bits of security.

## Properties

- **Every input is valid.** Any 32-byte $u$ defines a point on $E$ or on its quadratic twist $E'$, and the ladder computes the right $u$-coordinate on either.
- **Twist secure.** The twist has order $4\ell'$ with $\ell'$ prime, so a point on the twist leaks at most the low bits of $k$, which clamping fixes. This is why no validation is needed.
- **Cofactor cleared by clamping.** $k$ is a multiple of 8, so a component of order dividing 8 in the input is killed: such inputs give the output 0.
- **Uniform and constant-time friendly.** The same operations run for each bit, and there are no special cases in the formulas for honest inputs.
- **Deterministic** as a function; key generation draws 32 random bytes.

## Variants and improvements

- **[X448](/x448/)** on Curve448, with $p = 2^{448} - 2^{224} - 1$, for about 224 bits of security.
- **[Ed25519](/ed25519/)** signatures use the twisted Edwards curve that is birationally equivalent to Curve25519, so one key can be converted between the two forms (as in XEdDSA for Signal).
- **Fixed-base speed-up.** Key generation computes $kP_0$ for a fixed point and can use precomputed tables on the Edwards form, which is several times faster than the ladder.
- **Hybrid post-quantum.** X25519MLKEM768 in TLS joins X25519 with ML-KEM-768 ([hybrid key exchange](/hybrid-key-exchange/)).
- **Implementations.** Field arithmetic in radix $2^{51}$ on 64-bit processors (five limbs) or $2^{25.5}$ on 32-bit ones; formally verified code such as HACL* and fiat-crypto.

## When to use it

Use X25519 as the default for ephemeral Diffie-Hellman in new protocols: TLS 1.3, SSH (curve25519-sha256), the [Noise](/noise-protocol-framework/) patterns, WireGuard, and [X3DH](/x3dh/). Add authentication, derive keys with [HKDF](/hkdf/), and add a post-quantum KEM if recorded traffic must stay secret against a future quantum computer. Use [ECDH](/ecdh/) on P-256 instead when a FIPS 140 module or a standard requires NIST curves.

## Pitfalls

- **Skipping the all-zero check.** If the peer sends a point of order 1, 2, 4 or 8 (or such a point plus a multiple of $p$), the output is 0 for every key. RFC 7748 Section 6.1 says that a protocol may check for the all-zero output and abort; protocols that need contributory behaviour, such as TLS 1.3, must do so.
- **Clamping twice or not at all.** Libraries clamp inside the function. Code that stores an unclamped scalar and uses it in another formula (for example a signature) gets a different key.
- **Non-canonical $u$.** Values $u \ge p$ must be reduced, and bit 255 must be ignored, as lines L2 and L11 do; otherwise two libraries disagree on rare inputs.
- **Timing.** CSWAP must not branch, and the field arithmetic must not depend on the size of the numbers. Python and most big-integer libraries fail this.
- **Raw output as a key.** The output is a field element. Hash it with the transcript.

## Implementations

## History

Peter Montgomery introduced the curves $By^2 = x^3 + Ax^2 + x$ and the $x$-only ladder in 1987, to speed up the elliptic curve factoring method. Daniel Bernstein chose Curve25519 and defined its Diffie-Hellman function at PKC 2006, with the clamping, the twist security and fast constant-time code. OpenSSH added curve25519-sha256 in 2014, RFC 7748 standardized X25519 and X448 in January 2016, and TLS 1.3 (RFC 8446, 2018) made x25519 one of its named groups. It is now used in many TLS connections, in WireGuard and in Signal, and NIST SP 800-186 (2023) lists Curve25519 among its recommended curves.

## References
