---
tag: 83GQX3
kind: algorithm
slug: weil-descent-attack
name: Weil descent attack
aliases:
- GHS attack
- Gaudry-Hess-Smart attack
- Covering attack on elliptic curves
area: number-theory/discrete-logarithm
level: research
summary: Reduces ECDLP over extension fields of small degree to a hyperelliptic DLP.
solves: [elliptic-curve-discrete-logarithm-problem]
model: word-ram
complexity:
  vars:
    q: the odd prime with the curve over F_(q^2)
    N: the order of E(F_(q^2)), about q^2
    s: the largest prime power r^e dividing ord(P) that is not handled by the descent, or 1
  time:
    heuristic: O(q^3 + s^(1/2))
  space:
    extra: O(q^2 + s^(1/2))
  bit_operations:
    heuristic: O((q^3 + s^(1/2)) log(q)^2)
properties:
  deterministic: false
  recursive: false
prereqs: [elliptic-curve-discrete-logarithm-problem, index-calculus, polynomial-extended-euclidean-algorithm]
see_also: [semaev-summation-polynomial-index-calculus, factor-base, gaussian-elimination-modular, pohlig-hellman, baby-step-giant-step, pollard-rho-discrete-logarithm, menezes-okamoto-vanstone-reduction, tonelli-shanks]
sources:
  - paper: doi:10.1007/s00145-001-0011-x
    title: Pierrick Gaudry, Florian Hess, Nigel P. Smart, Constructive and destructive facets of Weil descent on elliptic curves, Journal of Cryptology 15(1), 2002
    locator: pages 19 to 46 (the covering construction with the conorm and norm maps, and the genus of the descended curve for curves over binary fields)
  - paper: doi:10.1007/3-540-45539-6_2
    title: Pierrick Gaudry, An algorithm for solving the discrete log problem on hyperelliptic curves, EUROCRYPT 2000, Lecture Notes in Computer Science 1807
    locator: pages 19 to 34 (index calculus in the Jacobian with a factor base of degree one divisors, for fixed genus)
  - paper: doi:10.1090/S0025-5718-1987-0866101-0
    title: David G. Cantor, Computing in the Jacobian of a hyperelliptic curve, Mathematics of Computation 48(177), 1987
    locator: pages 95 to 101 (composition and reduction of divisors in Mumford representation)
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Section 15.7 (Weil descent as a covering attack, with the conorm and norm maps and Frey's 1998 idea), Section 15.6.3 (Gaudry's algorithm, Exercises 15.6.4 and 15.6.5, equation (15.11) and the double large prime bound), numbered as in version 2.0 of the online chapters
---

The Weil descent attack moves an [elliptic curve discrete logarithm](/elliptic-curve-discrete-logarithm-problem/) in $E(\mathbb{F}_{q^n})$ to a discrete logarithm in the Jacobian of a curve $C_0$ over the smaller field $\mathbb{F}_q$, and solves it there by [index calculus](/index-calculus/). Frey proposed the idea in 1998, and Gaudry, Hess and Smart (GHS) made it explicit: find a curve $C$ over $\mathbb{F}_{q^n}$ with a map $C \to E$, such that the Frobenius extends to $C$ and $C$ descends to a curve $C_0$ over $\mathbb{F}_q$. Pulling a point back to a divisor on $C$ and taking the norm down to $C_0$ gives a group homomorphism $E(\mathbb{F}_{q^n}) \to \operatorname{Jac}(C_0)(\mathbb{F}_q)$. If it does not kill the subgroup of interest and the genus $g$ of $C_0$ is small, the hyperelliptic index calculus beats [Pollard rho](/pollard-rho-discrete-logarithm/). This page implements the smallest case completely: $n = 2$, odd $q$, and an explicit genus $2$ cover of a family of curves with a $2$-torsion point over $\mathbb{F}_{q^2} \setminus \mathbb{F}_q$, with Gaudry's index calculus on the Jacobian.

## In plain words

A hard problem on a curve over a big field is moved to a related problem over a smaller field. The price is that the new object is no longer a curve's own points but a larger group made from a curve of higher genus.

The move works by a change of coordinates. Each point of the elliptic curve corresponds to a pair of points on a second curve, and the pair together with its "conjugate" pair gives an element of the new group. Adding points on the old curve corresponds to adding elements of the new group, so a logarithm on one side is a logarithm on the other.

The new group has a simple building block: single points of the second curve. Many elements are sums of two such points, and collecting enough of these sums solves the problem by linear algebra.

## The problem

**Input.** An odd prime $q$, and an elliptic curve $E : y^2 = g(x)(x - \beta)$ over $K = \mathbb{F}_{q^2}$ with $g(x) = x^2 - sx + t_0 \in \mathbb{F}_q[x]$ squarefree, $\beta \in K \setminus \mathbb{F}_q$ and $g(\beta) \ne 0$. Points $P, Q \in E(K)$.

**Output.** The $x \in \{0, \dots, n - 1\}$ with $xP = Q$, where $n = \operatorname{ord}(P)$, or NONE if $Q \notin \langle P \rangle$.

**Cost model.** The group is $E(K)$, of order $N$ with $|N - q^2 - 1| \le 2q$. It contains the full $2$-torsion, because $g$ splits over $K$, so it is never cyclic. One group operation is a constant number of operations in $K$, $O(\log^2 q)$ bit operations. The descent targets the prime $r > q$ with $r \,\|\, n$, if there is one; there is at most one, since two primes above $q$ multiply to more than $N$. Its logarithm is computed in $J(\mathbb{F}_q)$, the Jacobian of a genus $2$ curve over $\mathbb{F}_q$, where one operation by Cantor's algorithm costs $O(1)$ operations in $\mathbb{F}_q$. All other prime powers go to [baby-step giant-step](/baby-step-giant-step/), $O(\sqrt{r^e})$ group operations, proved. Correctness and termination with probability $1$ are proved. The time bound is heuristic: it assumes that a random reduced divisor splits over $\mathbb{F}_q$ with probability bounded below, about $1/g! = 1/2$. Counting the two group orders is a toy $O(q^2)$ step. The attack is not generic, so the [generic lower bound](/shoup-generic-lower-bound/) does not bind it.

## The algorithm

Let $T = \beta + \beta^q$ and $N_\beta = \beta^{q+1}$, both in $\mathbb{F}_q$. The substitution $x = (N_\beta - u^2)/(T - 2u)$ gives $x - \beta = -(u - \beta)^2/(T - 2u)$, and $g(x) = G(u)/(T - 2u)^2$ with

$$G(u) = (N_\beta - u^2)^2 - s(N_\beta - u^2)(T - 2u) + t_0 (T - 2u)^2 \in \mathbb{F}_q[u].$$

So with $H(u) = -(T - 2u)\,G(u)$, of degree $5$, the curve $C_0 : Y^2 = H(u)$ is a genus $2$ curve over $\mathbb{F}_q$, and

$$\varphi(u, Y) = \left(\frac{N_\beta - u^2}{T - 2u},\ \frac{Y(u - \beta)}{(T - 2u)^2}\right)$$

is a map $C_0 \to E$ of degree $2$ defined over $K$. The descent map is $\psi = (1 + \sigma) \circ \varphi^*$, where $\varphi^*$ pulls a point back to the divisor of its two preimages and $\sigma$ is the Frobenius of $K$ acting on coefficients. It is a homomorphism $E(K) \to J(\mathbb{F}_q)$. Divisor classes are written in Mumford form $[U, V]$: $U$ monic with $\deg U \le 2$, $\deg V < \deg U$ and $U \mid H - V^2$.

```pseudo id=main
WEIL-DESCENT-LOG(E, P, Q)   ▷ E: y² = g(x)(x − β) over F_{q²}; returns x with xP = Q, or NONE
L1  T ← β + β^q; N_β ← β^{q+1}; H(u) ← −(T − 2u)·G(u); C₀: Y² = H(u) over F_q, J its Jacobian
L2  n ← ord(P); if nQ ≠ O then return NONE
L3  for each prime power r^e ∥ n do
L4      P_r ← (n/r^e)P; Q_r ← (n/r^e)Q
L5      if e = 1 and r > q and r² ∤ #J(F_q) and ψ(P_r) ≠ 0 then
L6          y ← GAUDRY(ψ(P_r), ψ(Q_r), r)
L7          if yP_r ≠ Q_r then return NONE else x_r ← y
L8      else x_r ← BSGS(P_r, Q_r, r^e); if x_r = NONE then return NONE
L9  return the x mod n with x ≡ x_r (mod r^e) for every r   ▷ Chinese remainder theorem

ψ(R)                        ▷ the descent map E(F_{q²}) → J(F_q)
L10 if R = O or x_R = β then return 0
L11 U ← u² − 2x_R u + (x_R T − N_β); V ← y_R (T − 2u)² (u − β)⁻¹ mod U
L12 return [U, V] + [U^σ, V^σ]   ▷ Cantor's algorithm over F_{q²}; the sum has coefficients in F_q

GAUDRY(D₁, D₂, r)           ▷ ord(D₁) = r, r ∥ #J(F_q), D₂ ∈ ⟨D₁⟩
L13 ℬ ← {u₀ ∈ F_q : H(u₀) is a square}; F_{u₀} ← [u − u₀, Y₀] with Y₀² = H(u₀); fix u* ∈ ℬ
L14 K ← empty; repeat
L15     draw a_j, b_j in [0, r) and c_j in [0, #J/r); R_j ← a_j D₁ + b_j D₂ + r c_j F_{u*}
L16     write R_j = [U, V]; if U splits over F_q then e_j ← for each root u₀, ±1 (±2 if double) with the sign of V(u₀) = ±Y₀
L17     else continue
L18     reduce e_j mod r against the rows of K, keeping the combination c of relations used
L19     if it reduces to 0 then A ← Σ c_i a_i; C ← Σ c_i b_i mod r; if C ≠ 0 then return −A·C⁻¹ mod r
L20     else scale the reduced row to a leading 1 and add it to K
```

Lines L1 to L9 are a [Pohlig-Hellman](/pohlig-hellman/) frame, as in the [summation polynomial index calculus](/semaev-summation-polynomial-index-calculus/). Line L2 is only a necessary condition for membership, because $E(K)$ is not cyclic. For $r \,\|\, N$ the Sylow $r$-subgroup has order $r$, so $Q_r \in \langle P_r \rangle$, and line L5 sends such a prime to the descent when it is large. Small primes and repeated primes go to baby-step giant-step at line L8, which also decides membership. Line L7 is a cheap check that the proof shows always passes.

Line L11 computes $\varphi^*(R)$: the preimages of $R$ have the $u$-coordinates of the roots of $U$, since $x(\varphi(u, Y)) = x_R$ means $N_\beta - u^2 = x_R(T - 2u)$, and $Y = y_R(T - 2u)^2/(u - \beta)$ at these roots. For $x_R = \beta$ the polynomial $U$ is $(u - \beta)^2$ and $u - \beta$ is not invertible, so line L10 sends this $2$-torsion point to $0$, which is consistent with the homomorphism. Line L12 adds the conjugate divisor. The sum is fixed by $\sigma$, so its reduced form has coefficients in $\mathbb{F}_q$. Galbraith describes this composite of a conorm map and a norm map as the core of Weil descent.

GAUDRY is index calculus in $J(\mathbb{F}_q)$ with Gaudry's factor base of degree one divisors. The factor base has one class $F_{u_0}$ for each $u_0$ with a point $(u_0, \pm Y_0)$ on $C_0$, so it has about $q/2$ elements. A reduced class $[U, V]$ is a sum of factor base elements exactly when $U$ splits over $\mathbb{F}_q$, and then each root $u_0$ gives $\pm F_{u_0}$, with the sign read off from $V(u_0)$ (line L16). The term $r c_j F_{u^*}$ at line L15 is killed by the cofactor $\#J/r$; it varies the part of $R_j$ outside the $r$-subgroup, which the termination proof needs. Lines L18 to L20 are incremental [Gaussian elimination mod r](/gaussian-elimination-modular/), and line L19 reads off the logarithm from a dependency.

## Example

Take $q = 7$, so $K = \mathbb{F}_7(t)$ with $t^2 = 3$, and $E : y^2 = (x^2 + 1)(x - 2 - t)$, that is $s = 0$, $t_0 = 1$ and $\beta = 2 + t$. Then $T = 4$ and $N_\beta = 4 - 3 = 1$, so

$G(u) = 3 + 5u + 2u^2 + u^4$ and $H(u) = 2 + 2u^2 + 4u^3 + 3u^4 + 2u^5$.

Counting gives $\#E(K) = \#J(\mathbb{F}_7) = 52 = 4 \cdot 13$. The values $H(0), \dots, H(6)$ are $2, 6, 0, 3, 5, 4, 1$, so $\mathcal{B} = \{0, 2, 5, 6\}$ with $Y_0 = 3$, $Y_2 = 0$, $Y_5 = 2$ and $Y_6 = 1$. The class $F_2$ is the Weierstrass point $(T/2, 0)$, of order $2$, while $F_0$, $F_5$ and $F_6$ have order $26$.

Let $P = (0, 3 + t)$, of order $13$, and $Q = (t, 4t)$. Line L5 applies to $r = 13$: $13 > 7$, $13^2 \nmid 52$, and line L11 gives $\varphi^*(P) = [u^2 - 1, (4 + 5t)u + (3 + 5t)]$, whose sum with its conjugate is

$D_1 = \psi(P) = [u^2 + 2u + 1, 4u + 3] \ne 0$, and $D_2 = \psi(Q) = [u^2 + 6u + 5, 2u + 3]$.

For the example take the draws $(a_j, b_j) = (j, 1)$ and $c_j = 0$.

| $j$ | $R_j = jD_1 + D_2$ | roots of $U$ | relation |
|---|---|---|---|
| 0 | $[u^2 + 6u + 5, 2u + 3]$ | $2, 6$ | $F_2 + F_6$ |
| 1 | $[u^2 + 6u + 5, 5u + 4]$ | $2, 6$ | $F_2 - F_6$ |
| 2 | $[u^2 + 4u + 4, 5u + 5]$ | $5$ twice | $2F_5$ |
| 3 | $[u^2 + 4, 2u + 4]$ | none | |
| 4 | $[u^2 + u + 3, 2u + 1]$ | none | |
| 5 | $[u^2, 4]$ | $0$ twice | $-2F_0$ |
| 6 | $[u^2 + 2u + 1, 3u + 4]$ | $6$ twice | $2F_6$ |

For $j = 0$: $V(6) = 15 \equiv 1 = Y_6$ and $V(2) = 7 \equiv 0 = Y_2$. For $j = 5$: $V(0) = 4 = -Y_0$. The discriminants for $j = 3, 4$ are $5$ and $3$, non-residues mod $7$. Over the columns $(0, 2, 5, 6)$ the first five rows are independent mod $13$, and the row for $j = 6$ reduces to $0$ with the combination $c = (1, -1, -1)$ at $j = 0, 1, 6$: $(0,1,0,1) - (0,1,0,-1) - (0,0,0,2) = 0$. Line L19 gives $A = 0 - 1 - 6 \equiv 6$ and $C = 1 - 1 - 1 \equiv 12 \pmod{13}$, so $x = -6 \cdot 12^{-1} \equiv 6$. Indeed $6P = Q$, and line L7 confirms it.

## Correctness

Three facts carry the proof. First, $\psi$ is a homomorphism, because $\varphi^*$ and $\sigma$ are homomorphisms on divisor classes and $\varphi^*(O) = W + \infty$ with $W = (T/2, 0)$, a point of order $2$ in $J$ that $1 + \sigma$ sends to $2[W - \infty] = 0$. Second, every row of line L16 is a true relation $R_j = \sum e_{j,u} F_u$ in $J(\mathbb{F}_q)$: a reduced class $[U, V]$ with $U = \prod (u - u_i)$ is the sum of the points $(u_i, V(u_i))$ minus $\deg U$ times $\infty$. Third, a dependency $\sum c_i e_i \equiv 0 \pmod r$ multiplied by $h = \#J/r$ kills the factor base part and the terms $r c_i F_{u^*}$, and leaves $h(A + xC)D_1 = 0$. Since $r \nmid h$, this gives $A + xC \equiv 0$. Because $\psi(P_r) \ne 0$ has order $r$, $\psi$ is injective on $\langle P_r \rangle$, so the logarithm of $\psi(Q_r)$ is that of $Q_r$. For termination, with suitable $c_j$ the draw equals $F_{u^*}$ with positive probability, and two such draws with different $b_j$ give a dependency with $C \ne 0$. See [the correctness proof](proofs/correctness.md).

## Complexity

The factor base has about $q/2$ elements, since $H(u_0)$ is a square for about half of the $u_0 \in \mathbb{F}_q$. A reduced class of degree $2$ splits with probability about $1/2! = 1/2$ (Galbraith, Exercise 15.6.4); measured over $400$ images $\psi(R)$ of random points, the rate was $0.54$ for $q = 101$ ($|\mathcal{B}| = 51$) and $0.56$ for $q = 307$ ($|\mathcal{B}| = 154$). This is the heuristic step. A dependency with $C \ne 0$ appears after at most $|\mathcal{B}| + 1$ relations plus, on average, about one more, so the expected number of draws is $O(q)$. Each draw costs three scalar multiplications with precomputed doublings, $O(\log N)$ Jacobian operations of $O(1)$ operations in $\mathbb{F}_q$ each, and a square root mod $q$. The dense elimination costs $O(q^3)$ operations mod $r$, and the space is $O(q^2)$ residues. Baby-step giant-step for the other prime powers costs $O(\sqrt s)$, and the toy point counts cost $O(q^2)$, which the $O(q^3)$ term covers. This gives the header bounds. The rows have at most two nonzero entries, so sparse linear algebra brings the index calculus to $\tilde O(q^2)$, which is Galbraith's equation (15.11) for fixed genus.

For this toy the descent gains nothing: $J(\mathbb{F}_q)$ has about $q^2$ elements, so Pollard rho on $E(K)$ costs about $q$ group operations, while Gaudry's algorithm in genus $2$ costs $\tilde O(q^2)$, or $\tilde O(q^{2 - 2/g}) = \tilde O(q)$ with the double large prime variation. The attack pays when the descended genus is small compared with the degree $n$: if $E(\mathbb{F}_{q^n})$ descends to genus $g = n$, the double large prime bound $\tilde O(q^{2 - 2/n})$ is below the $q^{n/2}$ of rho for $n \ge 3$, and for genus large compared with $\log q$ the hyperelliptic index calculus is subexponential in $q^g$. In general the genus of $C_0$ grows quickly with $n$ and depends on the curve, and for most curves it is too large for any gain.

## Properties

- **Las Vegas.** The answer is always correct; only the number of draws is random.
- **A group homomorphism, not an embedding.** $\psi$ maps $E(K)$ into a group of the same order, but it is not injective in general. In the tests its kernel only met points of $2$-power order, and line L5 checks $\psi(P_r) \ne 0$ before using it.
- **Not generic.** It uses the coordinates of points and the structure of the curve, so the generic $\sqrt N$ bound does not apply.
- **Depends on the curve.** Only special curves over $\mathbb{F}_{q^n}$ have a cover of small genus. The family here needs a $2$-torsion point with $x$-coordinate outside $\mathbb{F}_q$ and the rest of the cubic defined over $\mathbb{F}_q$.
- **Sparse relations.** Each row has at most $g$ nonzero entries, here $2$, with values $\pm 1$ or $\pm 2$.

## Variants and improvements

- **The GHS construction in characteristic $2$.** For ordinary curves $y^2 + xy = x^3 + ax^2 + b$ over $\mathbb{F}_{2^{ln}}$, GHS build an Artin-Schreier cover through the function field and give the genus of $C_0$ over $\mathbb{F}_{2^l}$ in terms of a "magic number" $m \le n$, as $2^{m-1}$ or $2^{m-1} - 1$. For small $m$ the descent is effective.
- **Other covers.** Odd characteristic, non-hyperelliptic covers and isogenies to curves with a better cover extend the set of weak curves. Composing with an isogeny can move a curve without a good cover to one that has it.
- **Index calculus on the Jacobian.** Gaudry's algorithm, the large prime variants of Thériault and the double large prime variant of Gaudry, Thériault, Thomé and Diem, and for large genus the subexponential algorithms of Enge, Gaudry and Thomé, all apply after the descent.
- **Without divisor class groups.** Gaudry's summation polynomial method works directly on the Weil restriction of $E$ and needs no cover; see the [summation polynomial index calculus](/semaev-summation-polynomial-index-calculus/).
- **Transfer by pairings.** The [MOV reduction](/menezes-okamoto-vanstone-reduction/) is another transfer, to a finite field instead of a Jacobian, and works for curves with a small embedding degree.

## When to use it

Use it to check whether an elliptic curve over an extension field $\mathbb{F}_{q^n}$ is weak: compute the genus of the best available cover, and compare index calculus in that Jacobian with Pollard rho. This is one reason why standard binary curves are defined over $\mathbb{F}_{2^p}$ with $p$ prime, and why curves over composite degree extensions are avoided. For curves over prime fields there is no subfield and the attack does not apply. For $n = 2$, as in the code here, it is slower than rho, and the toy only shows the mechanism.

## Pitfalls

- **A descent map that kills the subgroup.** If $\psi(P_r) = 0$, every relation says nothing about $P_r$. Line L5 tests it and falls back to baby-step giant-step at line L8.
- **A prime with $r^2 \mid \#J(\mathbb{F}_q)$.** Then the cofactor kills $\psi(P_r)$ too, and a dependency mod $r$ gives nothing. Line L5 sends such primes to line L8.
- **Using index calculus for small primes.** For $r \le q$ baby-step giant-step costs $O(\sqrt q)$, far less than the $O(q)$ draws of GAUDRY. Line L5 requires $r > q$.
- **The point $(\beta, 0)$.** For $x_R = \beta$ the formula of line L11 divides by $u - \beta$ modulo $(u - \beta)^2$. Line L10 maps this point to $0$, which the homomorphism requires.
- **Signs and double roots.** A root $u_0$ of $U$ gives $+F_{u_0}$ or $-F_{u_0}$ according to $V(u_0) = \pm Y_0$, and a double root gives $\pm 2$. Line L16 must read both off; for $Y_0 = 0$ the two signs agree.
- **Dropping the term $r c_j F_{u^*}$.** Without it every $R_j$ lies in $\langle D_1 \rangle$, a subgroup of order $r$, and the proof of termination at line L15 fails.
- **Dependencies with $C = 0$.** They give $0 = 0$. Line L19 checks every dependency, and these form a basis, so the first useful one is never missed.

## Implementations

## History

Frey proposed Weil restriction of scalars as an attack on elliptic curves over extension fields in a lecture at the ECC conference in 1998, and Galbraith and Smart worked out details. Gaudry gave the index calculus for hyperelliptic curves of fixed genus with a factor base of points in 2000, and Gaudry, Hess and Smart published the explicit covering construction for binary fields in 2002, which made the descent practical for curves over $\mathbb{F}_{2^{ln}}$ with small magic number. Menezes and Qu then analyzed the attack and found that it fails for curves over $\mathbb{F}_{2^p}$ with $p$ prime in the range used in practice. Later work by Diem, Hess, Menezes, Teske and others extended the covers to more curves and to odd characteristic.

## References
