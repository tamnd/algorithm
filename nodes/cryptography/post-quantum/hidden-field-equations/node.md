---
tag: N046XB
kind: algorithm
slug: hidden-field-equations
name: Hidden field equations
aliases:
- HFE
- Patarin HFE
area: cryptography/post-quantum
level: advanced
summary: Patarin's 1996 multivariate scheme. It hides a low degree polynomial over GF(q^n) behind two affine maps. Broken as encryption, and its signature variant GeMSS fell in 2021.
solves: [public-key-encryption]
model: word-ram
complexity:
  vars: {n: "the degree of the extension field GF(2^n), also the number of variables", d: the degree of the central polynomial}
  time: {worst: O(n^2 d^3), average: O(n d^2 log d), best: O(n d^2)}
  space: {extra: O(n^3)}
properties: {deterministic: true, randomized: false}
history:
  year: 1996
  people: [Jacques Patarin]
  note: Patarin proposed HFE after he broke the C* scheme of Matsumoto and Imai with linearization equations in 1995. HFE and its variants were later broken by Gröbner basis and MinRank attacks.
prereqs: [multivariate-quadratic-problem, irreducible-polynomial]
see_also: [multivariate-cryptography, unbalanced-oil-and-vinegar, rainbow-signature, cantor-zassenhaus-algorithm, f5-algorithm, groebner-basis, xl-algorithm, public-key-encryption]
sources:
  - paper: "Jacques Patarin, Hidden fields equations (HFE) and isomorphisms of polynomials (IP): two new families of asymmetric algorithms, Eurocrypt 1996, LNCS 1070, pages 33 to 48"
    locator: the whole paper (the HFE central polynomial, encryption with redundancy, and signatures)
  - paper: "Tsutomu Matsumoto and Hideki Imai, Public quadratic polynomial-tuples for efficient signature-verification and message-encryption, Eurocrypt 1988, LNCS 330, pages 419 to 453"
    locator: the whole paper (the C* scheme with the monomial X^(q^theta + 1))
  - paper: "Jacques Patarin, Cryptanalysis of the Matsumoto and Imai public key scheme of Eurocrypt'88, Crypto 1995, LNCS 963, pages 248 to 261"
    locator: the whole paper (the bilinear linearization equations that decrypt C*)
  - paper: "Aviad Kipnis and Adi Shamir, Cryptanalysis of the HFE public key cryptosystem by relinearization, Crypto 1999, LNCS 1666, pages 19 to 30"
    locator: the whole paper (the public key as one univariate polynomial over the big field, and key recovery as a MinRank problem)
  - paper: "Jean-Charles Faugère and Antoine Joux, Algebraic cryptanalysis of hidden field equation (HFE) cryptosystems using Gröbner bases, Crypto 2003, LNCS 2729, pages 44 to 60"
    locator: the whole paper (the break of the first HFE challenge with F5, and the low degree of regularity of HFE systems)
  - paper: "Chengdong Tao, Albrecht Petzoldt and Jintai Ding, Efficient key recovery for all HFE signature variants, Crypto 2021, LNCS 12825, pages 70 to 93"
    locator: the whole paper (key recovery for HFEv- and the GeMSS parameters)
  - paper: "Jacques Patarin, Nicolas Courtois and Louis Goubin, QUARTZ, 128-bit long digital signatures, CT-RSA 2001, LNCS 2020, pages 282 to 297"
    locator: the whole paper (an HFEv- signature with short signatures)
  - book: isbn:9783540887010
    title: Daniel J. Bernstein, Johannes Buchmann and Erik Dahmen (editors), Post-Quantum Cryptography, Springer, 2009
    locator: the chapter Multivariate public key cryptography by Jintai Ding and Bo-Yin Yang (C*, HFE, the minus and vinegar modifiers, and the attacks)
---

Hidden field equations (HFE) is a [multivariate](/multivariate-cryptography/) public-key scheme by Jacques Patarin (1996). The secret is a univariate polynomial $F$ of low degree $d$ over the extension field $\mathbb{F}_{q^n}$, of a special form that is quadratic over $\mathbb{F}_q$. Seen in coordinates and hidden by two secret affine maps $S$ and $T$, it becomes the public key: $n$ quadratic polynomials in $n$ variables. Anyone encrypts by evaluating them. The owner decrypts by finding the roots of a univariate polynomial of degree $d$, which is fast. HFE generalizes the C* scheme of Matsumoto and Imai (1988), which Patarin broke in 1995. **HFE is broken.** Gröbner basis attacks solve its public systems much faster than random ones (Faugère and Joux, 2003), and key recovery attacks by MinRank broke its signature variants, the last being GeMSS (Tao, Petzoldt and Ding, 2021).

**Notation.** $q = 2$ on this page. $K = \mathbb{F}_2[t]/(g(t)) = \mathbb{F}_{2^n}$ for an [irreducible polynomial](/irreducible-polynomial/) $g$ of degree $n$, and $\varphi : K \to \mathbb{F}_2^n$ takes coordinates. $F \in K[X]$ is the central polynomial of degree $d$, $S$ and $T$ are invertible affine maps of $\mathbb{F}_2^n$, and $\mathcal{P} = T \circ \varphi \circ F \circ \varphi^{-1} \circ S$ is the public map. $r$ is the number of redundancy bits and $H$ a hash function. $\lambda$ is the security parameter, $\mathcal{A}$ an adversary and $\mathrm{Adv}$ its advantage. **Security model.** Plain HFE encryption is deterministic, so at best it is one-way under chosen plaintext attack (OW-CPA): no efficient $\mathcal{A}$ should find $x$ from $(\mathcal{P}, \mathcal{P}(x))$ with non-negligible $\mathrm{Adv}$. That needs both the [MQ problem](/multivariate-quadratic-problem/) for the public system and the hardness of recovering $F$, $S$ and $T$. HFE meets neither for practical $d$.

## In plain words

A large finite field can be seen in two ways: as single numbers that you can multiply and raise to powers, or as lists of bits. A polynomial in one unknown is easy to solve in the first view, even in a huge field. Written in the second view, the same polynomial becomes many quadratic equations in many bit unknowns, which look hard to solve.

HFE publishes the second view, after mixing the input bits and the output bits with secret linear maps. To decrypt, the owner undoes the mixing, goes back to the one-unknown view, and solves there. The weak point is that the hidden polynomial must have a low degree to be solved fast, and attackers learned to exploit that low degree.

## The problem

Build a trapdoor one-way function from quadratic polynomials: a public map $\mathcal{P} : \mathbb{F}_2^n \to \mathbb{F}_2^n$ that is a random-looking quadratic system, and a secret that inverts it. Used as [public-key encryption](/public-key-encryption/), the message goes in with redundancy, the ciphertext is $\mathcal{P}(x)$, and decryption must find $x$.

## The algorithm

**The central polynomial.** Squaring is additive in characteristic 2, so $X \mapsto X^{2^i}$ is $\mathbb{F}_2$-linear on $K$. Hence $X^{2^i + 2^j} = X^{2^i} \cdot X^{2^j}$ is quadratic in the coordinates of $X$, and so is

$$F(X) = \sum_{2^i + 2^j \le d} a_{ij} X^{2^i + 2^j} + \sum_{2^i \le d} b_i X^{2^i} + c .$$

```pseudo id=main
KEYGEN(n, d, r)
L1  F ← a random polynomial of the HFE shape over K = F_{2^n}, of degree d
L2  S, T ← random invertible affine maps of F_2^n
L3  P ← the n quadratic polynomials of x ↦ T(F(S(x))), found by interpolation
L4  return pk = P and sk = (F, S, T)

ENCRYPT(pk, m)                               ▷ m has n − r bits
L5  x ← m ‖ H(m)_r                           ▷ r bits of redundancy
L6  return y = P(x)

DECRYPT(sk, y)
L7  Y ← T⁻¹(y), seen as an element of K
L8  for each root X of F(X) − Y in K         ▷ gcd with X^{2^n} − X, then trace splitting
L9      x ← S⁻¹(X); if the last r bits of x are H of the first n − r bits, return the first n − r bits
L10 return ⊥
```

**Interpolation (L3).** A quadratic map over $\mathbb{F}_2$ is fixed by its values on the points of weight at most 2: the constant is $\mathcal{P}(0)$, the linear coefficient of $x_j$ is $\mathcal{P}(e_j) + \mathcal{P}(0)$, and the coefficient of $x_j x_k$ is $\mathcal{P}(e_j + e_k) + \mathcal{P}(e_j) + \mathcal{P}(e_k) + \mathcal{P}(0)$.

**Root finding (L8).** Since $X^{2^n} - X$ is the product of all $X - a$ for $a \in K$, $h = \gcd(F - Y, X^{2^n} - X)$ is the product of $X - a$ over the roots $a$. The code computes $X^{2^n} \bmod (F - Y)$ by $n$ squarings. To split $h$, it uses the trace $\mathrm{Tr}(z) = \sum_{i<n} z^{2^i}$, which takes values in $\{0, 1\}$: $\gcd(h, \mathrm{Tr}(\beta X) \bmod h)$ collects the roots $a$ with $\mathrm{Tr}(\beta a) = 0$. Some $\beta$ in the basis $1, t, \ldots, t^{n-1}$ separates any two roots. This is the Berlekamp trace algorithm, a close relative of [Cantor-Zassenhaus](/cantor-zassenhaus-algorithm/).

**C\* and Patarin's attack.** C* is the case $F(X) = X^{2^\theta + 1}$ with $\gcd(2^\theta + 1, 2^n - 1) = 1$. Then $F$ is a permutation, and decryption is $Y \mapsto Y^h$ with $h(2^\theta + 1) \equiv 1 \pmod{2^n - 1}$. Patarin found the flaw in 1995. Write $A = S(x)$ and $B = T^{-1}(y)$, so $B = A^{2^\theta + 1}$. Raising this to the power $2^\theta - 1$ and multiplying by $AB$ gives

$$A \cdot B^{2^\theta} = A^{2^{2\theta}} \cdot B,$$

and both sides are bilinear in $(x, y)$ over $\mathbb{F}_2$. So there are at least $n$ independent relations $\sum \gamma_{ij} x_i y_j + \sum \alpha_i x_i + \sum \beta_j y_j + \delta = 0$ that hold for all pairs $(x, \mathcal{P}(x))$.

```pseudo id=attack
PATARIN-ATTACK(P, y*)                        ▷ only the public key
A1  for (n + 1)² + 40 random x: record the vector of all products x_i·y_j, x_i, y_j, 1 with y = P(x)
A2  R ← a basis of the vectors (γ, α, β, δ) orthogonal to all records   ▷ Gaussian elimination
A3  put y = y* in every relation of R; this gives linear equations in x
A4  solve them; test each solution x with P(x) = y*; return the one that matches
```

## Example

**C\* in $\mathbb{F}_8$.** Take $K = \mathbb{F}_2[t]/(t^3 + t + 1)$ and $\theta = 1$, so $F(X) = X^3$ and $\gcd(3, 7) = 1$. For $A = t$, $A^3 = t^3 = t + 1$. The inverse exponent is $h = 5$, since $3 \cdot 5 = 15 \equiv 1 \pmod 7$. Check: $(t + 1)^2 = t^2 + 1$, $(t + 1)^4 = t^4 + 1 = t^2 + t + 1$, and $(t + 1)^5 = (t^2 + t + 1)(t + 1) = t^3 + 1 = t$. Patarin's relation with $\theta = 1$ is $AB^2 = A^4 B$. With $A = t$ and $B = t + 1$, the left side is $t(t^2 + 1) = t^3 + t = 1$, and the right side is $(t^2 + t)(t + 1) = t^3 + t = 1$.

**Toy HFE.** For $n = 11$ and $d = 24$ the central polynomial has the monomials $X^0, X, X^2, X^4, X^8, X^{16}$ and $X^3, X^5, X^6, X^9, X^{10}, X^{12}, X^{17}, X^{18}, X^{20}, X^{24}$. With $r = 5$ redundancy bits, a message has 6 bits. The public key has 11 polynomials with $55 + 11 + 1 = 67$ coefficients each. The tests run this case, and $n = 16$ with $r = 8$. They also check that a toy HFE key at $n = 11$ has no bilinear relation of Patarin's kind, while C* at $n = 7, 9, 11$ has at least $n$, and that the attack then decrypts every test ciphertext.

## Correctness

Squaring is linear in characteristic 2 and multiplication is bilinear, so $x \mapsto T(F(S(x)))$ is quadratic and the interpolation in line L3 gives it exactly. If $y = \mathcal{P}(x)$, then line L7 gives $Y = F(S(x))$, so $S(x)$ is a root of $F - Y$. Line L8 finds all roots, and line L9 recovers $x$ from $S(x)$, which passes the check. Decryption fails only if another root, found first, also passes the check; if $H$ acts like a random function, this has probability at most $(d - 1) 2^{-r}$. The proof file has the details, including why the trace splitting always works.

## Complexity

All counts are operations in $K$ unless stated.

- **Decryption.** Computing $X^{2^n} \bmod (F - Y)$ takes $n$ squarings of polynomials of degree below $d$, $O(n d^2)$ with schoolbook arithmetic. Splitting takes $O(n d^2)$ per trial of $\beta$. With few roots, which is the usual case, the total is $O(n d^2)$ to $O(n d^2 \log d)$. In the worst case every one of up to $d - 1$ splits tries $n$ values of $\beta$, which gives $O(n^2 d^3)$.
- **Encryption.** Evaluating $n$ polynomials with $O(n^2)$ terms costs $O(n^3)$ bit operations.
- **Key generation.** Interpolation needs $1 + n + \binom{n}{2}$ evaluations of $T \circ F \circ S$.
- **Space.** The public key has $n \left(\binom{n}{2} + n + 1\right)$ bits, which is $O(n^3)$.

So $d$ must stay small, at most a few hundred in proposed parameters. That is exactly what the attacks exploit.

## Properties

- **Deterministic encryption** with redundancy; the redundancy picks the right root when $F(X) = Y$ has several.
- **Not a permutation.** A random polynomial of the HFE shape has on average about one root per value, but some values have none and some have several. For signatures this means retrying with a new salt until $F(X) = Y$ has a root.
- **Small ciphertexts and signatures**, of about $n$ bits, but public keys of $O(n^3)$ bits.
- **Low rank.** Seen as a quadratic form over $K$, the central map has rank about $\log_2 d$. Kipnis and Shamir turned this into a MinRank attack on the key.

## Variants and improvements

- **C\*** (Matsumoto and Imai, 1988) is the case $d = 2^\theta + 1$ with one monomial. Broken by Patarin's linearization equations, as above.
- **HFE-** (minus) drops some public polynomials, and **HFEv** adds vinegar variables to $F$. HFEv- combines both and is a signature scheme: Quartz (Patarin, Courtois and Goubin, 2001) and GeMSS, an alternate in round 3 of the NIST process.
- **Attacks.** Kipnis and Shamir (1999) recovered keys through MinRank. Faugère broke the first HFE challenge of Patarin with F5, and Faugère and Joux (2003) showed that HFE systems have a low degree of regularity, so Gröbner bases solve them much faster than random systems. Tao, Petzoldt and Ding (2021) gave key recovery for all HFE signature variants and brought the GeMSS parameters below their claimed security. Granboulan, Joux and Stern (2006) argued that inverting HFE with a fixed $d$ takes quasi-polynomial time.
- **Odd characteristic and multi-HFE** change the field or use several big field variables; they were also attacked.

## When to use it

Do not use HFE, C* or HFEv- to protect data: they are broken as proposed, and the signature variants failed in the NIST process. Study HFE to understand big field multivariate schemes and the attacks on them. For real encryption use a reviewed library, for example libsodium or a FIPS 140 validated module with ML-KEM; for multivariate signatures, follow the UOV family, which is still in the NIST process.

## Pitfalls

- **Large $d$ makes decryption slow, small $d$ makes the system easy.** No choice of $d$ was found that is both practical and secure.
- **Several roots.** Without enough redundancy, decryption can return a wrong message.
- **Invertibility of C\*.** The map $X^{2^\theta + 1}$ is a permutation only if $\gcd(2^\theta + 1, 2^n - 1) = 1$.
- **Linear relations in general.** Any central map with a simple algebraic relation between input and output, like C*, can give relations that hold for all plaintext and ciphertext pairs. Test new designs with the attack of this page.

## Implementations

The Python code is for study only. It is not constant time, it uses the random module, and the sizes ($n = 7$ to 16) give no security. It has the field $\mathbb{F}_{2^n}$, affine maps and Gaussian elimination over $\mathbb{F}_2$, interpolation of the public key, root finding by the Berlekamp trace algorithm, toy HFE encryption with SHA-256 redundancy, C*, and Patarin's attack. There are no official test vectors for HFE or C*, because neither was standardized; the toy parameters are ours. The tests check the field against a carry-less multiplication oracle, root finding against brute force, the hand example above, the round trips, and the attack under fixed seeds.

## History

Matsumoto and Imai published C* at Eurocrypt 1988. Patarin broke it in 1995 with his linearization equations, and in 1996 proposed HFE as a repair, with a general central polynomial in place of one monomial. He also posted HFE challenges with prize money. Kipnis and Shamir attacked the key in 1999, and Faugère solved the first challenge with F5; Faugère and Joux published the analysis in 2003. Signature variants such as Quartz (2001) and GeMSS (in the NIST process from 2017) used the minus and vinegar modifiers. In 2021 Tao, Petzoldt and Ding gave key recovery attacks for all HFE signature variants, and GeMSS was not selected.

## References
