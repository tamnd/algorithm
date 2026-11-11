---
tag: HTEPPM
kind: concept
slug: elliptic-curve-cryptography
name: Elliptic-curve cryptography
aliases:
area: cryptography/public-key
level: advanced
summary: Public-key cryptography in the group of points of an elliptic curve over a finite field. No subexponential discrete log attack is known on good curves, so 256-bit keys suffice.
prereqs: [public-key-cryptography, cyclic-group, discrete-logarithm-problem]
see_also: [elliptic-curve-discrete-logarithm-problem, ecdh, ecdsa, ed25519, x25519, ecies, bilinear-pairing, quantum-elliptic-curve-discrete-log]
sources:
  - paper: "Neal Koblitz, Elliptic curve cryptosystems, Mathematics of Computation 48(177), 1987, pages 203 to 209"
    locator: the proposal of elliptic curve groups for Diffie-Hellman and ElGamal
  - paper: "Victor S. Miller, Use of elliptic curves in cryptography, CRYPTO 1985, LNCS 218, pages 417 to 426"
    locator: the independent proposal, and the argument that index calculus does not carry over to curves
  - book: isbn:9780387952734
    title: Darrel Hankerson, Alfred Menezes and Scott Vanstone, Guide to Elliptic Curve Cryptography, Springer, 2004
    locator: Chapter 3 (elliptic curve arithmetic, coordinates and scalar multiplication) and Chapter 4 (the discrete logarithm problem, domain parameters and protocols)
  - book: isbn:9781420071467
    title: Lawrence C. Washington, Elliptic Curves, Number Theory and Cryptography, second edition, CRC Press, 2008
    locator: Chapter 2 (the group law), Chapter 4 (curves over finite fields and the Hasse bound), Chapter 5 (the discrete logarithm problem, including MOV and anomalous curves)
  - url: "https://doi.org/10.6028/NIST.SP.800-186"
    title: NIST SP 800-186, Recommendations for Discrete Logarithm-based Cryptography, Elliptic Curve Domain Parameters, 2023
    locator: the domain parameters of P-256 and of Curve25519 and Edwards25519
  - url: "https://www.rfc-editor.org/rfc/rfc6979"
    title: Thomas Pornin, RFC 6979, Deterministic Usage of the Digital Signature Algorithm (DSA) and Elliptic Curve Digital Signature Algorithm (ECDSA), 2013
    locator: Appendix A.2.5, the P-256 key pair and the signature with SHA-256 on the message sample
  - url: "https://www.rfc-editor.org/rfc/rfc7748"
    title: Adam Langley, Mike Hamburg and Sean Turner, RFC 7748, Elliptic Curves for Security, 2016
    locator: Section 4.1 (Curve25519) and Section 5 (the X25519 function and its Montgomery ladder)
  - url: "https://doi.org/10.1109/18.259647"
    title: Alfred Menezes, Tatsuaki Okamoto and Scott Vanstone, Reducing elliptic curve logarithms to logarithms in a finite field, IEEE Transactions on Information Theory 39(5), 1993, pages 1639 to 1646
    locator: the MOV reduction with the Weil pairing, and its use against supersingular curves
  - paper: "Nigel P. Smart, The discrete logarithm problem on elliptic curves of trace one, Journal of Cryptology 12(3), 1999, pages 193 to 196"
    locator: the polynomial-time attack on anomalous curves, with exactly p points
  - url: "https://safecurves.cr.yp.to/"
    title: Daniel J. Bernstein and Tanja Lange, SafeCurves, choosing safe curves for elliptic-curve cryptography
    locator: the criteria for the discrete logarithm problem (rho, transfer, discriminant, rigidity) and for implementations (ladder, twist, completeness, indistinguishability)
---

Elliptic-curve cryptography (ECC) is public-key cryptography in which the group is the set of points of an elliptic curve over a finite field. Miller (1985) and Koblitz (1987) proposed it independently. For well chosen curves, the best known attack on the [elliptic curve discrete logarithm problem](/elliptic-curve-discrete-logarithm-problem/) is a generic one that takes about $n^{1/2}$ group operations, so a curve over a 256-bit field gives about the same security as 3072-bit [RSA](/rsa-cryptosystem/), with much shorter keys and faster operations. [ECDH](/ecdh/), [ECDSA](/ecdsa/), [Ed25519](/ed25519/), [X25519](/x25519/) and [ECIES](/ecies/) all work in this group.

**Notation.** $p$ is the prime of the field $\mathbb{F}_p$ and $b$ its number of binary digits. $E(\mathbb{F}_p)$ is the group of points; it plays the role of the group $G$ of the other pages, and its base point is written $G$ in the standards, in the role of $g$. $n$ is the order of the base point, a prime on every curve here, and $h = \#E(\mathbb{F}_p)/n$ the cofactor. $O$ is the point at infinity, the identity. $kP$ is $P$ added to itself $k$ times. $\lambda$ is the security parameter, $\mathcal{A}$ an adversary that runs in time $t$, and $\mathrm{Adv}$ an advantage. The hardness assumptions (ECDLP, CDH and DDH on the curve) are in the standard model; protocols on this page name their own model.

## In plain words

An elliptic curve is the set of solutions of an equation like $y^2 = x^3 + ax + b$, where the numbers are taken modulo a prime. There is a rule that takes two points of the curve and gives a third point, and this rule behaves like multiplication of numbers modulo a prime: it has an identity, inverses, and the order of the inputs does not matter.

So every scheme that works with powers $g^x$ modulo a prime also works with multiples $xG$ of a point. Computing $xG$ from $x$ is fast. Getting $x$ back from $xG$ seems to be much harder on a curve than in the integers modulo a prime, because the shortcuts that work for integers do not work for points. That is why curve keys are short.

## The idea

### The curve and its points

Let $p > 3$ be a prime. A *short Weierstrass curve* over $\mathbb{F}_p$ is

$$E: \; y^2 = x^3 + ax + b, \qquad a, b \in \mathbb{F}_p, \quad 4a^3 + 27b^2 \ne 0.$$

The condition on $a$ and $b$ says the cubic has no repeated root, so the curve has no cusp or self-crossing. $E(\mathbb{F}_p)$ is the set of solutions $(x, y) \in \mathbb{F}_p^2$ together with one extra point $O$, the point at infinity.

### The group law

The *chord-and-tangent rule* defines $P + Q$. For $P = (x_1, y_1)$ and $Q = (x_2, y_2)$:

- $P + O = O + P = P$, and $-P = (x_1, -y_1)$; if $x_1 = x_2$ and $y_1 = -y_2$, then $P + Q = O$.
- Otherwise let $\ell = (y_2 - y_1)/(x_2 - x_1)$ if $P \ne Q$ (the chord), or $\ell = (3x_1^2 + a)/(2y_1)$ if $P = Q$ (the tangent). Then

$$x_3 = \ell^2 - x_1 - x_2, \qquad y_3 = \ell(x_1 - x_3) - y_1, \qquad P + Q = (x_3, y_3).$$

Geometrically, the line through $P$ and $Q$ meets the curve in a third point, and $P + Q$ is its mirror image in the x-axis. With this rule, $E(\mathbb{F}_p)$ is an abelian group. Closure and commutativity follow from the formulas; associativity needs a real proof (Washington, Chapter 2), and the test file checks it on all $19^3$ triples of the toy curve below.

**Size and shape.** Hasse's theorem bounds the number of points: $|\#E(\mathbb{F}_p) - (p + 1)| \le 2\sqrt{p}$. The group is cyclic or a product of two cyclic groups. Cryptography uses a base point $G$ of large prime order $n$, with a small cofactor $h$: $h = 1$ for P-256 and secp256k1, $h = 8$ for Curve25519.

### Scalar multiplication

The basic operation is $kP$ for a secret scalar $k$, the analogue of $g^k$. Double-and-add, the analogue of [binary exponentiation](/binary-exponentiation/), takes about $\log_2 k$ doublings and half as many additions. The *Montgomery ladder* does one addition and one doubling for every bit, which gives a fixed sequence of operations:

```pseudo id=main
LADDER(k, P)                        ▷ k = (k_{m−1} … k_0) in binary
L1  R0 ← O; R1 ← P                  ▷ invariant: R1 = R0 + P
L2  for i ← m − 1 down to 0
L3      if k_i = 0 then
L4          (R0, R1) ← (2 R0, R0 + R1)
L5      else (R0, R1) ← (R0 + R1, 2 R1)
L6  return R0                       ▷ R0 = k P
```

After the step for bit $i$, $R_0$ is $\lfloor k / 2^i \rfloor P$ and $R_1 = R_0 + P$, so line L6 returns $kP$. A constant-time implementation replaces the branch of line L3 by a conditional swap without branches, as RFC 7748 does for X25519.

**Coordinates.** Each affine addition needs a field inversion, which costs as much as many multiplications. *Jacobian coordinates* $(X, Y, Z)$ stand for $(X/Z^2, Y/Z^3)$ and use only multiplications; one inversion at the end converts back. With schoolbook arithmetic a field multiplication costs $\Theta(b^2)$, a point operation a constant number of multiplications, and a scalar multiplication $\Theta(b)$ point operations, so $\Theta(b^3)$ in total. Windowed methods with the [non-adjacent form](/non-adjacent-form/) (wNAF) cut the number of additions, and precomputed tables speed up multiples of the fixed $G$.

**Point compression.** A point can be sent as $x$ and one bit of $y$, since $y$ is a square root of $x^3 + ax + b$; for $p \equiv 3 \pmod 4$ the root is $(x^3 + ax + b)^{(p+1)/4}$. SEC 1 uses the prefix byte 02 or 03 for the parity of $y$, and 04 for an uncompressed point.

### Why curves give short keys

The security of ECC rests on the [ECDLP](/elliptic-curve-discrete-logarithm-problem/): given $G$ and $Q = kG$, find $k$. For the integers modulo $p$, index calculus methods such as the [number field sieve](/number-field-sieve-discrete-logarithm/) solve the [discrete logarithm problem](/discrete-logarithm-problem/) in subexponential time. Miller (1985) argued that there is no analogue for points, and none is known for good curves over prime fields. So the best attack is generic: [Pollard rho](/pollard-rho-discrete-logarithm/) needs about $(\pi n / 4)^{1/2}$ group operations, and [Pohlig-Hellman](/pohlig-hellman/) reduces the work to the largest prime factor of the group order. A 256-bit $n$ gives about $2^{128}$ operations. NIST SP 800-57 Part 1 puts 256-bit curves at the same level as 3072-bit RSA and finite-field Diffie-Hellman.

### Weak curves

Some curves have structure that breaks the ECDLP:

- **Small embedding degree.** The MOV attack (Menezes, Okamoto and Vanstone 1993) uses the Weil pairing to map the ECDLP into $\mathbb{F}_{p^k}^*$, where $k$ is the smallest integer with $n \mid p^k - 1$. For supersingular curves $k \le 6$, and the finite-field logarithm is then subexponential. Pairing-based cryptography uses such curves on purpose, with larger fields; see [bilinear pairings](/bilinear-pairing/).
- **Anomalous curves.** If $\#E(\mathbb{F}_p) = p$, Smart (1999), and independently Satoh and Araki and Semaev, solve the ECDLP in polynomial time.
- **Composite group order.** If $n$ is not prime, Pohlig-Hellman splits the problem into small ones.
- **Curves over extension fields.** [Weil descent](/weil-descent-attack/) breaks some curves over $\mathbb{F}_{2^m}$ with composite $m$.

Standards choose $n$ prime, the embedding degree large and $\#E \ne p$. SafeCurves (Bernstein and Lange) adds criteria for implementations: twist security, a ladder, complete formulas, and parameters derived in a rigid way so that nobody can hide a weak choice.

## Examples

**A toy curve.** $E: y^2 = x^3 + 2x + 2$ over $\mathbb{F}_{17}$ has $4 \cdot 8 + 27 \cdot 4 = 140 \equiv 4 \pmod{17}$, so it is non-singular. It has 19 points including $O$, within the Hasse interval $18 \pm 8.2$. Since 19 is prime, the group is cyclic and every point other than $O$ generates it. Take $G = (5, 1)$.

| computation | steps | result |
|---|---|---|
| $2G$ | $\ell = (3 \cdot 25 + 2)/(2 \cdot 1) = 77 \cdot 2^{-1} = 9 \cdot 9 = 13$; $x_3 = 169 - 10 = 6$; $y_3 = 13(5 - 6) - 1 = -14$ | $(6, 3)$ |
| $3G = G + 2G$ | $\ell = (3 - 1)/(6 - 5) = 2$; $x_3 = 4 - 5 - 6 = -7$; $y_3 = 2(5 - 10) - 1 = -11$ | $(10, 6)$ |
| $7G$ | ladder over the bits 111 of 7 | $(0, 6)$ |
| $19G$ | $n = 19$ | $O$ |

All arithmetic is modulo 17. A toy [ECDH](/ecdh/) exchange: Alice's secret is 3, so she sends $3G = (10, 6)$; Bob's secret is 7, so he sends $7G = (0, 6)$. Alice computes $3 \cdot (0, 6)$ and Bob computes $7 \cdot (10, 6)$; both get $21G = 2G = (6, 3)$. In this group a brute force search over 19 scalars finds each secret at once, which is why real curves have $n$ near $2^{256}$.

**P-256.** The NIST curve P-256 (also secp256r1) has $p = 2^{256} - 2^{224} + 2^{192} + 2^{96} - 1$, $a = -3$, a prime group order $n$ of 256 binary digits and $h = 1$. RFC 6979 Appendix A.2.5 uses the private key

`x = C9AFA9D845BA75166B5C215767B1D6934E50C3DB36E89B127B8A622B120F6721`

whose public key $xG$ has

`Ux = 60FED4BA255A9D31C961EB74C6356D68C049B8923B61FA6CE669622E60F29FB6`
`Uy = 7903FE1008B8BC99A41AE9E95628BC64F2F1B20C2D7E9F5177A3C294D4462299`.

$U_y$ is odd, so the compressed point is the byte 03 followed by $U_x$, 33 bytes in all. The test file computes $xG$ with the ladder and checks these values, checks $nG = O$, and checks the value $r$ of the appendix's signature on "sample" with SHA-256 as $x(kG) \bmod n$.

**Common curves.**

| curve | field | form | cofactor | main uses |
|---|---|---|---|---|
| P-256 | $2^{256} - 2^{224} + 2^{192} + 2^{96} - 1$ | short Weierstrass, $a = -3$ | 1 | TLS, ECDSA in FIPS 186-5, WebAuthn |
| secp256k1 | $2^{256} - 2^{32} - 977$ | short Weierstrass, $a = 0$, $b = 7$ | 1 | Bitcoin and Ethereum signatures |
| Curve25519 | $2^{255} - 19$ | Montgomery $y^2 = x^3 + 486662x^2 + x$ | 8 | X25519 key exchange (RFC 7748) |
| Edwards25519 | $2^{255} - 19$ | twisted Edwards, same group as Curve25519 | 8 | Ed25519 signatures (RFC 8032) |
| P-384 | $2^{384} - 2^{128} - 2^{96} + 2^{32} - 1$ | short Weierstrass, $a = -3$ | 1 | higher security levels |

Montgomery curves allow an x-only ladder, and twisted Edwards curves have a complete addition law with no special cases, which helps constant-time code.

## Where it is used

- **Key exchange.** [ECDH](/ecdh/) with X25519 or P-256 is the default key exchange in TLS 1.3, SSH and the Signal protocol.
- **Signatures.** [ECDSA](/ecdsa/) on P-256 and secp256k1, and [Ed25519](/ed25519/) (EdDSA), sign certificates, software updates, SSH keys and cryptocurrency transactions. [Schnorr signatures](/schnorr-signature/) on secp256k1 are used in Bitcoin since 2021.
- **Encryption.** [ECIES](/ecies/) and HPKE (RFC 9180) build [hybrid encryption](/hybrid-encryption/) from ECDH.
- **Pairings.** Pairing-friendly curves such as BLS12-381 support [BLS signatures](/bls-signature/) and many zero-knowledge proof systems.
- **The quantum threat.** Shor's algorithm solves the ECDLP in polynomial time on a large quantum computer ([quantum elliptic curve discrete log](/quantum-elliptic-curve-discrete-log/)), and estimates suggest it needs fewer qubits than factoring RSA keys of equal classical strength. Post-quantum schemes such as [ML-KEM](/crystals-kyber/) are now deployed next to ECDH in hybrid key exchange. [Isogeny-based cryptography](/isogeny-based-cryptography/) uses maps between curves, not the group of one curve.

**Implementation pitfalls.** Check that every received point is on the curve and in the right subgroup, or an invalid curve or [small subgroup attack](/small-subgroup-attack/) can leak the private key. Use constant-time scalar multiplication; a branch on the bits of $k$ leaks through [timing](/timing-attack/). For ECDSA, never reuse or bias the nonce, or a few signatures give the key. The Python code is for study only: it is not constant time and must not protect real data. Use a FIPS 140 validated module or libsodium.

## References
