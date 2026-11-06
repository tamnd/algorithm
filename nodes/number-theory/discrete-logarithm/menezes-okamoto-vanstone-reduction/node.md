---
tag: HWKGB7
kind: algorithm
slug: menezes-okamoto-vanstone-reduction
name: MOV reduction
aliases:
- MOV attack
- Menezes-Okamoto-Vanstone attack
- MOV/FR reduction
- Frey-Rück reduction
area: number-theory/discrete-logarithm
level: advanced
summary: Transfers ECDLP to a finite-field DLP using pairings; effective for supersingular curves.
solves: [elliptic-curve-discrete-logarithm-problem]
model: word-ram
complexity:
  vars:
    p: the prime of the base field, with p = 3 mod 4
    n: the order of P, odd and dividing p + 1
    q: the size p^2 of the field that receives the logarithm
  time:
    average: O(n^(1/2) + log(p) log(log(p)))
    heuristic: exp(((64/9)^(1/3) + o(1)) (ln q)^(1/3) (ln ln q)^(2/3))
  space:
    extra: O(n^(1/2))
  bit_operations:
    average: O((n^(1/2) + log(p) log(log(p))) log(p)^2)
properties:
  deterministic: false
  recursive: false
prereqs: [elliptic-curve-discrete-logarithm-problem, bilinear-pairing, finite-field-discrete-logarithm-problem]
see_also: [miller-algorithm, index-calculus, number-field-sieve-discrete-logarithm, quasi-polynomial-discrete-logarithm, weil-descent-attack, baby-step-giant-step, bilinear-diffie-hellman, boneh-franklin-ibe]
sources:
  - paper: doi:10.1109/18.259647
    title: Alfred J. Menezes, Tatsuaki Okamoto and Scott A. Vanstone, Reducing elliptic curve logarithms to logarithms in a finite field, IEEE Transactions on Information Theory 39(5), 1993
    locator: pages 1639 to 1646 (the reduction by the Weil pairing, and the embedding degree of supersingular curves)
  - paper: doi:10.1090/S0025-5718-1994-1218343-6
    title: Gerhard Frey and Hans-Georg Rück, A remark concerning m-divisibility and the discrete logarithm in the divisor class group of curves, Mathematics of Computation 62(206), 1994
    locator: pages 865 to 874 (the reduction by the Tate pairing, and its non-degeneracy over finite fields)
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Chapter 26, Theorem 26.3.3 (bilinearity and non-degeneracy), Section 26.3.1 (Miller's algorithm, Definition 26.3.7 of the embedding degree, Exercise 26.3.8, Lemma 26.3.11 and Exercise 26.3.12 on omitting vertical lines), Section 26.4 (the MOV/FR attack, Theorems 26.4.1 and 26.4.2) and Section 26.6.1 (distortion maps)
  - paper: doi:10.1007/s001459900040
    title: R. Balasubramanian and Neal Koblitz, The improbability that an elliptic curve has subexponential discrete log problem under the Menezes-Okamoto-Vanstone algorithm, Journal of Cryptology 11(2), 1998
    locator: pages 141 to 145 (a random curve has a huge embedding degree, and E[r] lies in E(F_(q^k)) once r divides q^k - 1)
  - paper: doi:10.1007/s00145-004-0315-8
    title: Victor S. Miller, The Weil pairing, and its efficient calculation, Journal of Cryptology 17(4), 2004
    locator: pages 235 to 261 (the double and add evaluation of the functions with divisor k(P) - (kP) - (k - 1)(O))
---

The MOV reduction moves an instance of the [elliptic curve discrete logarithm problem](/elliptic-curve-discrete-logarithm-problem/) into the multiplicative group of a finite field. A [bilinear pairing](/bilinear-pairing/) $e$ satisfies $e(xP, R) = e(P, R)^x$, so if $Q = xP$ and $\alpha = e(P, R)$ has the same order $n$ as $P$, then $x$ is the logarithm of $\beta = e(Q, R)$ to base $\alpha$ in $\mathbb{F}_{p^k}^*$, where $k$ is the embedding degree, the least $k$ with $n \mid p^k - 1$. The pairing is computed in polynomial time by [Miller's algorithm](/miller-algorithm/), and the field logarithm can then be attacked by [index calculus](/index-calculus/) or the [number field sieve](/number-field-sieve-discrete-logarithm/) in subexponential time. For a random curve $k$ is enormous and the reduction is useless, but supersingular curves have $k \le 6$, and over $\mathbb{F}_p$ with $p > 3$ they have $k = 2$, so their discrete logarithm is no harder than one in $\mathbb{F}_{p^2}^*$.

## In plain words

On an elliptic curve the only known general way to find how many times a point was added to itself is a square root search. In a finite field there are much faster methods that use the factorization of numbers.

A pairing is a recipe that takes two points and gives a number in a finite field, and it turns repeated addition of points into repeated multiplication of numbers: adding a point to itself seven times multiplies the paired number by itself seven times. So pair both the base point and the target point with the same helper point, and the hidden count reappears as an exponent in the field, where the fast methods apply.

This only helps when the field is small. For most curves it is astronomically large, but for one special family of curves it is only twice as big, in digits, as the curve's own field.

## The problem

**Input.** A prime $p \equiv 3 \pmod 4$, the curve $E : y^2 = x^3 + x$ over $\mathbb{F}_p$, a point $P \in E(\mathbb{F}_p)$ of odd order $n$ with the factorization of $n$, and a point $Q \in E(\mathbb{F}_p)$.

**Output.** The $x \in \{0, \dots, n - 1\}$ with $xP = Q$, or NONE if $Q \notin \langle P \rangle$.

**Cost model.** The group of the instance is $E(\mathbb{F}_p)$, which here has order $p + 1$ and is cyclic, and $\langle P \rangle$ is its subgroup of order $n$. One group operation is a constant number of operations in $\mathbb{F}_p$, $O(\log^2 p)$ bit operations with schoolbook arithmetic (an inversion by the extended Euclidean algorithm costs the same). The algorithm is not generic: the pairing uses the coordinates of the points, so the [generic lower bound](/shoup-generic-lower-bound/) of $\sqrt n$ does not apply to it. The pairing values lie in $\mathbb{F}_{p^2} = \mathbb{F}_p(i)$ with $i^2 = -1$, where a multiplication is $3$ or $4$ multiplications in $\mathbb{F}_p$. The reduction itself is proved: an expected $O(\log p \log \log p)$ operations in $\mathbb{F}_{p^2}$, polynomial in $\log p$. The cost of the whole attack is that of the transferred logarithm in the subgroup of order $n$ of $\mathbb{F}_{p^2}^*$. With [baby-step giant-step](/baby-step-giant-step/), as in the implementation here, it is a proved $O(\sqrt n)$ field multiplications, no better than a generic attack on the curve. With the number field sieve it is a heuristic $L_{q}(1/3, (64/9)^{1/3})$ for $q = p^2$.

## The algorithm

The curve $E : y^2 = x^3 + x$ with $p \equiv 3 \pmod 4$ is supersingular with $\#E(\mathbb{F}_p) = p + 1$. Its own Tate pairing on $E(\mathbb{F}_p) \times E(\mathbb{F}_p)$ is trivial, because its values lie in $\mathbb{F}_p^*$ and are then raised to a multiple of $p - 1$. The distortion map $\psi(x, y) = (-x, iy)$ is a group homomorphism from $E(\mathbb{F}_p)$ to $E(\mathbb{F}_{p^2})$ that moves a point off the base field. The pairing used is the reduced Tate pairing $\hat t_m(T_0, R) = f_{m, T_0}(R)^{(p^2 - 1)/m}$, where $f_{m, T_0}$ is a function with divisor $m(T_0) - m(O)$, and $R = \psi(R_0)$ for a random $R_0 \in E(\mathbb{F}_p)$.

For a point $T$ and a second point $S$, let $\ell_{T,S}$ be the line through $T$ and $S$ (the tangent if $S = T$), with slope $\lambda$, evaluated at $R$ as $\ell_{T,S}(R) = y_R - y_T - \lambda (x_R - x_T)$. Miller's algorithm builds $f_{m, T_0}$ by double and add along the binary digits of $m$.

```pseudo id=main
MOV(P, Q, n, p)                     ▷ E: y² = x³ + x over F_p, p ≡ 3 mod 4; ord(P) = n odd; returns x with xP = Q, or NONE
L1  if nQ ≠ O then return NONE       ▷ E(F_p) is cyclic, so Q ∈ ⟨P⟩ iff nQ = O
L2  if Q = O then return 0
L3  d ← ord(Q); repeat
L4      R₀ ← a random point (x₀, y₀) of E(F_p) with y₀ ≠ 0; R ← ψ(R₀) = (−x₀, i·y₀)
L5      α ← TATE(P, R, n); if α^(n/r) = 1 for a prime r | n then try another R₀
L6      β ← TATE(Q, R, d)            ▷ equals the reduced pairing of Q and R of order n, so β = α^x
L7      x ← log_α β in the subgroup of order n of F_{p²}^*
L8      return x

TATE(T₀, R, m)                      ▷ T₀ ∈ E(F_p) of odd order m; returns f_{m,T₀}(R)^((p²−1)/m)
L9  f ← 1; T ← T₀
L10 for each binary digit b of m after the leading 1 do
L11     f ← f² · ℓ_{T,T}(R); T ← 2T
L12     if b = 1 then (if T ≠ −T₀ then f ← f · ℓ_{T,T₀}(R)); T ← T + T₀
L13 return f^((p²−1)/m)
```

Line L1 is the membership test, which works because $E(\mathbb{F}_p)$ is cyclic and so has only one subgroup of order $n$. Lines L4 and L5 draw helper points until the pairing $\alpha = \hat t_n(P, R)$ has exact order $n$, which is checked with the prime factors of $n$. Line L6 pairs the target with the same $R$; it uses $d = \operatorname{ord}(Q)$ in place of $n$ so that Miller's loop never reaches $O$ before its last step, and the two reduced pairings agree. Line L7 solves the logarithm in the field. The implementation uses baby-step giant-step there; in an attack this line is index calculus or the number field sieve.

TATE omits every vertical line $x - x_S$ of Miller's algorithm. Their values $x_R - x_S$ lie in $\mathbb{F}_p^*$, since $x_R = -x_0 \in \mathbb{F}_p$, and the final exponent $(p^2 - 1)/m = (p - 1)(p + 1)/m$ is a multiple of $p - 1$, so they would contribute $1$. The same argument removes the normalization constants. The only step where the line through $T$ and $T_0$ is vertical is the last one, at $T = -T_0$, and it is skipped in line L12. Since $m$ is odd, no intermediate $T$ is $O$ or has $y_T = 0$.

## Example

Take $p = 43$, so $\#E(\mathbb{F}_{43}) = 44 = 4 \cdot 11$, and $P = (4, 5)$ of order $n = 11$. Let $Q = (23, 8)$, which is $7P$. The membership test of line L1 passes since $11 Q = O$. Line L4 takes $R_0 = (2, 15)$, so $R = (41, 15i)$; it lies on the curve, because $(15i)^2 = -225 \equiv 33$ and $41^3 + 41 \equiv (-2)^3 - 2 = -10 \equiv 33$.

Line L5 runs TATE$(P, R, 11)$. The binary digits of $11$ are $1011$, so the loop sees $0, 1, 1$.

| digit | step | $\lambda$ | $\ell(R)$ | $f$ after | $T$ after |
|---|---|---|---|---|---|
| 0 | double $P$ | 35 | $33 + 15i$ | $33 + 15i$ | $2P = (13, 24)$ |
| 1 | double $2P$ | 7 | $38 + 15i$ | $8 + 12i$ | $4P = (23, 35)$ |
| 1 | add $P$ | 31 | $9 + 15i$ | $21 + 13i$ | $5P = (31, 18)$ |
| 1 | double $5P$ | 18 | $17 + 15i$ | $3 + 32i$ | $10P = (4, 38) = -P$ |
| 1 | add $P$ | vertical | skipped | $3 + 32i$ | $O$ |

The final exponent is $(43^2 - 1)/11 = 168$, and $(3 + 32i)^{168} = 2 + 30i = \alpha$. Since $11$ is prime and $\alpha \ne 1$, $\alpha$ has order $11$, and line L5 accepts $R$. The imaginary part of every $\ell(R)$ is $y_0 = 15$, so no line value is $0$.

Line L6 runs TATE$(Q, R, 11)$ with $Q = (23, 8)$ of order $d = 11$. The doublings and additions pass through $2Q = (14, 36)$, $4Q = (31, 25)$, $5Q = (13, 24)$ and $10Q = -Q$, with $f$ ending at $29 + 10i$, and $\beta = (29 + 10i)^{168} = 11 + 40i$.

The powers of $\alpha$ are $\alpha^1 = 2 + 30i$, $\alpha^2 = 7 + 34i$, $\alpha^3 = 26 + 20i$, $\alpha^4 = 11 + 3i$, $\alpha^5 = 18 + 35i$, $\alpha^6 = 18 + 8i$, $\alpha^7 = 11 + 40i$, so line L7 finds $x = 7$, and indeed $7P = (23, 8) = Q$. Every element of $\langle \alpha \rangle$ has norm $a^2 + b^2 \equiv 1$, since $11 \mid p + 1$; for example $\alpha^{10} = 2 + 13i$ is the conjugate of $\alpha$, so inversion in this subgroup is conjugation.

For a target outside $\langle P \rangle$, take $Q = (2, 15)$, of order $44$. Then $11 Q \ne O$ and line L1 returns NONE.

## Correctness

The membership test is exact because $E(\mathbb{F}_p)$ is cyclic: its $2$-torsion over $\mathbb{F}_p$ is only $\{O, (0, 0)\}$, since $x^2 + 1$ has no root when $p \equiv 3 \pmod 4$. The vertical lines and constants dropped in TATE lie in $\mathbb{F}_p^*$ and are killed by the final exponentiation, so TATE returns the reduced Tate pairing, which is bilinear. Hence $\beta = \hat t_n(xP, R) = \alpha^x$, and when $\alpha$ has order $n$ the field logarithm determines $x$ modulo $n$. For termination, every point of $E(\mathbb{F}_{p^2})$ is, modulo $n E(\mathbb{F}_{p^2})$, a sum of a point of $E(\mathbb{F}_p)$ and a point of $\psi(E(\mathbb{F}_p))$, and the first kind pairs trivially with $P$. Non-degeneracy then forces $R_0 \mapsto \hat t_n(P, \psi(R_0))$ to be a homomorphism onto the $n$-th roots of unity, so each trial succeeds with probability at least $\varphi(n)/n$. See [the correctness proof](proofs/correctness.md).

## Complexity

Line L1 is a scalar multiplication, $O(\log n)$ group operations. Computing $d = \operatorname{ord}(Q)$ with the known factorization of $n$ takes $O(\log^2 n)$ group operations. Each call to TATE makes $\lfloor \log_2 m \rfloor$ doublings and at most as many additions, each a constant number of operations in $\mathbb{F}_p$ and $\mathbb{F}_{p^2}$, and a final exponentiation by $(p^2 - 1)/m < p^2$, which is $O(\log p)$ multiplications in $\mathbb{F}_{p^2}$. So one pairing is $O(\log p)$ field operations and $O(\log^3 p)$ bit operations. Each trial of lines L4 and L5 succeeds with probability at least $\varphi(n)/n$, so the expected number of trials is at most $n/\varphi(n) = O(\log \log n)$, and finding a point $R_0$ takes an expected $2$ square root attempts, each $O(\log p)$ multiplications in $\mathbb{F}_p$. The whole reduction is therefore an expected $O(\log p \log \log p)$ field operations, $O(\log^3 p \log \log p)$ bit operations, and this bound is proved.

Line L7 dominates. Baby-step giant-step in the subgroup of order $n$ takes $O(\sqrt n)$ multiplications in $\mathbb{F}_{p^2}$ and $O(\sqrt n)$ stored elements, which gives the average bounds in the header. That is no faster than running baby-step giant-step on the curve. The gain comes from the structure of $\mathbb{F}_{q}^*$ with $q = p^2$: the number field sieve and its variants solve the discrete logarithm there in heuristic time $L_q(1/3, c)$, with $c = (64/9)^{1/3} \approx 1.923$ for the classical sieve in large characteristic and smaller constants for the tower variants at some sizes. A curve over a $256$-bit field whose group order is a $256$-bit prime has generic security near $2^{128}$, but with embedding degree $2$ its discrete logarithm sits in a $512$-bit field, which is within reach of the number field sieve. In general the field has $q^k$ elements, and the attack helps when $L_{q^k}(1/3)$ is much smaller than $\sqrt n$.

## Properties

- **A reduction, not a solver.** MOV changes the group, not the problem: lines L1 to L6 cost polynomial time and the difficulty moves to $\mathbb{F}_{p^k}^*$.
- **Las Vegas.** The output is always correct; only the number of helper points drawn is random.
- **Depends on the embedding degree.** The target field is $\mathbb{F}_{p^k}$ with $k$ the least integer such that $n \mid p^k - 1$. For prime $n \nmid p - 1$, the full $n$-torsion lies in $E(\mathbb{F}_{p^k})$ exactly when $n \mid p^k - 1$ (Balasubramanian and Koblitz).
- **Supersingular curves.** Every supersingular curve has $k \le 6$; over a prime field with $p > 3$ it has $\#E(\mathbb{F}_p) = p + 1$ and $k = 2$.
- **Not generic.** Like index calculus, it uses the representation of the group, which is why it can beat the $\sqrt n$ bound.
- **Same structure as pairing-based cryptography.** The pairing that breaks the discrete logarithm on these curves is what makes [bilinear Diffie-Hellman](/bilinear-diffie-hellman/) and [Boneh-Franklin identity-based encryption](/boneh-franklin-ibe/) possible. Those schemes choose the curve so that both the curve logarithm and the field logarithm are hard, and the decisional Diffie-Hellman problem becomes easy in the curve group.

## Variants and improvements

- **Weil pairing.** Menezes, Okamoto and Vanstone used the Weil pairing $e_n(P, R)$, which needs $R$ with $e_n(P, R)$ of order $n$, in general a point of $E[n]$ outside $\langle P \rangle$, possibly over a larger extension. Frey and Rück observed that the Tate pairing needs only a point of $E(\mathbb{F}_{p^k})$, and Balasubramanian and Koblitz showed that in most cases the Weil pairing also works over $\mathbb{F}_{p^k}$.
- **Distortion maps.** Verheul showed that on a supersingular curve every point $P \ne O$ has a distortion map, an endomorphism $\psi$ not defined over the base field with $\hat t_r(P, \psi(P)) \ne 1$. With the map of this page that holds for $P$ of prime order $r$ when $r^2 \nmid p + 1$, and pairing $P$ with $\psi(P)$ saves the search for $R_0$. This page pairs with $\psi$ of a random point instead, which also covers composite $n$ and $r^2 \mid p + 1$.
- **Small characteristic.** Supersingular curves over $\mathbb{F}_{2^m}$ and $\mathbb{F}_{3^m}$ have $k \le 4$ and $k \le 6$, and their field logarithms are in small characteristic, where the [quasi-polynomial algorithm](/quasi-polynomial-discrete-logarithm/) applies.
- **Anomalous curves.** When $\#E(\mathbb{F}_p) = p$ the pairing does not apply ($n = p$ is not prime to $p$), but a $p$-adic lift or the logarithmic derivative maps the problem to the additive group of $\mathbb{F}_p$ in polynomial time (Semaev, Satoh and Araki, Smart; Galbraith, Section 26.4.1).
- **Other transfers.** The [Weil descent attack](/weil-descent-attack/) moves the problem to the Jacobian of a curve of larger genus over a smaller field, which helps for some curves over extension fields.

## When to use it

Use it to check a curve before deploying it: compute the least $k$ with $n \mid p^k - 1$ and reject the curve if $k$ is small enough that $\mathbb{F}_{p^k}^*$ is weaker than $\sqrt n$. Standards for elliptic curve cryptography include this test. As an attack it applies only to curves with small embedding degree, mainly supersingular curves and curves built on purpose for pairings, and for those it turns a square root problem into a subexponential one. For a random curve $k$ is about as large as $n$ and the reduction cannot be carried out.

## Pitfalls

- **Pairing $P$ with itself.** On these curves $\hat t_n(P, P) = 1$ for every $P \in E(\mathbb{F}_p)$, so taking $R = P$ in line L4 always fails. Line L4 applies the distortion map $\psi$, which moves $R$ off the base field.
- **The self-pairing for composite orders.** Taking $R = \psi(P)$ is not enough either: $\hat t_r(P, \psi(P))$ is trivial when $r^2 \mid p + 1$, for example $p = 71$ and $r = 3$. Line L4 pairs with $\psi(R_0)$ for a random $R_0$, and line L5 checks the order of $\alpha$ with every prime factor of $n$.
- **Not checking that $\alpha$ has order $n$.** If $\alpha$ has smaller order, line L7 yields $x$ only modulo $\operatorname{ord}(\alpha)$, or no answer. Line L5 rejects such $R$.
- **Running Miller's loop with $n$ for a target of smaller order.** If $\operatorname{ord}(Q) = d < n$, the multiples in TATE$(Q, R, n)$ reach $O$ in the middle of the loop and the line formulas divide by zero. Line L6 uses $d$, which gives the same reduced pairing.
- **Keeping the last vertical line.** At $T = -T_0$ the chord is vertical and the slope is undefined. Line L12 skips it; its value lies in $\mathbb{F}_p^*$ and does not change the result.
- **Even $n$.** If $n$ is even, a multiple of $P$ inside Miller's loop can be the $2$-torsion point $(0, 0)$, whose tangent is vertical, and the proof of this page uses that $n$ is odd. The implementation rejects even $n$; the factor $2^e$ of the order has only the prime $2$, so [Pohlig-Hellman](/pohlig-hellman/) handles it cheaply before the reduction.

## Implementations

## History

Menezes, Okamoto and Vanstone presented the reduction at STOC in 1991 and published it in 1993, using the Weil pairing; they showed that supersingular curves, then proposed because their arithmetic is fast, have embedding degree at most $6$ and so a discrete logarithm in a small extension field. Frey and Rück, in 1994, gave the version with the Tate pairing for the Jacobians of curves of any genus and proved its non-degeneracy over finite fields. Balasubramanian and Koblitz showed in 1998 that a random curve has a huge embedding degree. The same pairings later became a tool for building schemes, starting with Joux's tripartite key agreement in 2000 and identity-based encryption by Boneh and Franklin in 2001. After the small characteristic algorithms of 2013 and 2014, Granger, Kleinjung and Zumbrägel used this reduction to break a supersingular binary curve that had been proposed at the $128$-bit level.

## References
