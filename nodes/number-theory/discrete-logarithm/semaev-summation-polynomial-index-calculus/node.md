---
tag: WAPFC0
kind: algorithm
slug: semaev-summation-polynomial-index-calculus
name: Summation polynomial index calculus
aliases:
- Semaev's index calculus for elliptic curves
- Gaudry's index calculus for elliptic curves over extension fields
- Summation polynomial attack
area: number-theory/discrete-logarithm
level: research
summary: Index-calculus approach for ECDLP using summation polynomials to find relations.
solves: [elliptic-curve-discrete-logarithm-problem]
model: word-ram
complexity:
  vars:
    p: the characteristic, with the curve over F_(p^2)
    N: the order of E(F_(p^2)), about p^2
    s: the largest prime power r^e dividing ord(P) with r^2 dividing N, or 1
  time:
    heuristic: O(p^3 log(N) + s^(1/2))
  space:
    extra: O(p^2 + s^(1/2))
  bit_operations:
    heuristic: O((p^3 log(N) + s^(1/2)) log(p)^2)
properties:
  deterministic: false
  recursive: false
prereqs: [elliptic-curve-discrete-logarithm-problem, index-calculus, resultant]
see_also: [weil-descent-attack, factor-base, groebner-basis, cantor-zassenhaus-algorithm, gaussian-elimination-modular, pollard-rho-discrete-logarithm, pohlig-hellman, menezes-okamoto-vanstone-reduction]
sources:
  - url: https://eprint.iacr.org/2004/031
    title: Igor Semaev, Summation polynomials and the discrete logarithm problem on elliptic curves, IACR Cryptology ePrint Archive, Report 2004/031
    locator: the summation polynomials, their definition by resultants and the property that they vanish exactly at the x-coordinates of points that sum to zero, and the index calculus over a prime field with a factor base of points with small x
  - paper: doi:10.1016/j.jsc.2008.08.005
    title: Pierrick Gaudry, Index calculus for abelian varieties of small dimension and the elliptic curve discrete logarithm problem, Journal of Symbolic Computation 44(12), 2009
    locator: pages 1690 to 1702 (the factor base of points with x in F_q, the Weil restriction of the summation polynomial solved by Groebner bases, and the heuristic bounds O~(q^(4/3)) for n = 3 and O~(q^(3/2)) for n = 4)
  - paper: doi:10.1112/s0010437x10005075
    title: Claus Diem, On the discrete logarithm problem in elliptic curves, Compositio Mathematica 147(1), 2011
    locator: pages 75 to 104 (the factor base defined through an automorphism of the projective line, the dimension of the systems, and the proved expected subexponential bound when n grows like (log q)^(1/2))
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Section 15.8 (Definition 15.8.1 and Theorem 15.8.2 on summation polynomials, Section 15.8.2 on Gaudry's variant and equation (15.15), Theorem 15.8.4 for Diem's bound), numbered as in version 2.0 of the online chapters
---

Summation polynomial index calculus is an [index calculus](/index-calculus/) for the [elliptic curve discrete logarithm problem](/elliptic-curve-discrete-logarithm-problem/). Semaev's summation polynomial $S_m(x_1, \dots, x_m)$ vanishes exactly when there are points with these $x$-coordinates whose sum is $O$, so to write a random point $R = aP + bQ$ as a sum of $m - 1$ points from a [factor base](/factor-base/) one looks for roots of $S_m(x_1, \dots, x_{m-1}, x_R)$ with every $x_i$ in a fixed small set. Enough such relations give a linear dependency, and the dependency gives $\log_P Q$. Over a prime field no fast way to find these roots is known. Over an extension field $\mathbb{F}_{q^n}$, Gaudry took the factor base of points with $x \in \mathbb{F}_q$; writing $S_{n+1} = 0$ in a basis of $\mathbb{F}_{q^n}$ over $\mathbb{F}_q$ gives $n$ equations in $n$ unknowns over $\mathbb{F}_q$, which a [Gröbner basis](/groebner-basis/) solves. For fixed $n$ the heuristic cost is $\tilde O(q^{2 - 2/n})$ with the double large prime variation, below the $q^{n/2}$ of [Pollard rho](/pollard-rho-discrete-logarithm/) for $n \ge 3$. Diem proved a subexponential bound when $n$ grows like $\sqrt{\log q}$. This page implements the smallest case, $n = 2$, completely.

## In plain words

To find how many times a point was added to itself, index calculus first collects many "relations": random combinations of the two given points that are equal to short sums of a few fixed points. Once there are more relations than fixed points, some combination of them cancels the fixed points, and the hidden count can be read from what remains.

On an elliptic curve the hard part is to see whether a point is such a short sum. Semaev found a polynomial that is zero exactly when three points add up to nothing. So "is this point a sum of two fixed points" becomes "does this polynomial have a root of a special kind".

Over a field that contains a smaller field, take as fixed points those whose first coordinate lies in the smaller field. Then the condition splits into two easy equations over the small field.

## The problem

**Input.** A prime $p > 3$, an elliptic curve $E : y^2 = x^3 + ax + b$ with $a, b \in \mathbb{F}_{p^2}$ and $4a^3 + 27b^2 \ne 0$, and points $P, Q \in E(\mathbb{F}_{p^2})$.

**Output.** The $x \in \{0, \dots, n - 1\}$ with $xP = Q$, where $n = \operatorname{ord}(P)$, or NONE if $Q \notin \langle P \rangle$.

**Cost model.** The group is $E(\mathbb{F}_{p^2})$, of order $N$ with $|N - p^2 - 1| \le 2p$, and it need not be cyclic. One group operation is a constant number of operations in $\mathbb{F}_{p^2}$, where an inversion is one inversion in $\mathbb{F}_p$ through the norm, so it costs $O(\log^2 p)$ bit operations. The relation step works in the subgroup $\langle P_r \rangle$ of prime order $r$ for each prime $r$ with $r \mid n$ and $r^2 \nmid N$; other prime powers go to [baby-step giant-step](/baby-step-giant-step/), $O(\sqrt{r^e})$ group operations, proved. The algorithm is not generic: it uses the $x$-coordinates of points, so the [generic lower bound](/shoup-generic-lower-bound/) does not apply. Correctness and termination with probability $1$ are proved. The time bound in the header is heuristic: it assumes that a random point is a sum of at most two factor base points with probability bounded below by a constant, about $1/2$ (it is $1/n!$ for general $n$). Gaudry's bound $\tilde O(q^{2 - 2/n})$ for $E(\mathbb{F}_{q^n})$ is heuristic too, while Diem's subexponential bound is proved. Counting the points of $E$ (line L1) is done here by an $O(p^2)$ count, a toy step that Schoof-type algorithms replace by polynomial time.

## The algorithm

Write $\mathbb{F}_{p^2} = \mathbb{F}_p(t)$ with $t^2 = \nu$, a non-residue mod $p$. The factor base is $\mathcal{B} = \{x \in \mathbb{F}_p : x^3 + ax + b \text{ is a square in } \mathbb{F}_{p^2}\}$, with one fixed point $P_x = (x, y_x)$ for each $x \in \mathcal{B}$, so about $p/2$ elements. Semaev's third summation polynomial is

$$S_3(x_1, x_2, x_3) = (x_1 - x_2)^2 x_3^2 - 2\big((x_1 + x_2)(x_1 x_2 + a) + 2b\big) x_3 + (x_1 x_2 - a)^2 - 4b(x_1 + x_2),$$

and for affine points $P_1, P_2, P_3$ it vanishes at their $x$-coordinates exactly when $P_1 \pm P_2 \pm P_3 = O$ for some signs. It is symmetric in $x_1, x_2$, so with $s_1 = x_1 + x_2$ and $s_2 = x_1 x_2$ and $x_3 = x_R$,

$$S_3 = x_R^2 s_1^2 - 2 x_R s_1 s_2 + s_2^2 - (2a x_R + 4b) s_1 - (4 x_R^2 + 2a) s_2 + a^2 - 4b x_R.$$

Writing every coefficient as $u + vt$ splits $S_3 = G_0 + G_1 t$ with $G_0, G_1 \in \mathbb{F}_p[s_1, s_2]$. This is the Weil restriction for $n = 2$. The coefficient of $s_2^2$ is $1$, so $G_1 = c_1(s_1) s_2 + c_0(s_1)$ is linear in $s_2$ and $G_0 = s_2^2 + d_1(s_1) s_2 + d_0(s_1)$, with $\deg c_1, \deg d_1 \le 1$ and $\deg c_0, \deg d_0 \le 2$.

```pseudo id=main
SUMMATION-INDEX-CALCULUS(E, P, Q)   ▷ E: y² = x³ + ax + b over F_{p²}; returns x with xP = Q, or NONE
L1  N ← #E(F_{p²}); n ← ord(P)
L2  if nQ ≠ O then return NONE
L3  for each prime power r^e ∥ n do
L4      P_r ← (n/r^e)P; Q_r ← (n/r^e)Q
L5      if r² | N then x_r ← BSGS(P_r, Q_r, r^e); if x_r = NONE then return NONE
L6      else x_r ← RELATIONS(P_r, Q_r, r)                 ▷ here e = 1 and Q_r ∈ ⟨P_r⟩
L7  return the x mod n with x ≡ x_r (mod r^e) for every r  ▷ Chinese remainder theorem

RELATIONS(P, Q, r)                  ▷ ord(P) = r prime and r ∥ N
L8  ℬ ← {x ∈ F_p : x³ + ax + b is a square in F_{p²}}; fix P_x = (x, y_x) for x ∈ ℬ
L9  K ← empty; repeat
L10     draw a_j, b_j in [0, r) and a random point U; R_j ← a_j P + b_j Q + rU
L11     e_j ← DECOMPOSE(R_j); if e_j = NONE then continue
L12     reduce e_j mod r against the rows of K, keeping the combination c of relations used
L13     if it reduces to 0 then A ← Σ c_i a_i mod r; C ← Σ c_i b_i mod r
L14         if C ≠ 0 then return −A·C⁻¹ mod r
L15     else scale the reduced row to a leading 1 and add it to K

DECOMPOSE(R)                        ▷ a row e with R = Σ e_x P_x and Σ |e_x| ≤ 2, or NONE
L16 if R = O then return NONE; if x_R ∈ ℬ then return ±1 at x_R, with the sign of R = ±P_{x_R}
L17 split S₃(s₁, s₂, x_R) = G₀ + G₁t and form ρ(s₁) = c₀² − c₀c₁d₁ + c₁²d₀
L18 for each (s₁, s₂) ∈ F_p² with G₀ = G₁ = 0, in increasing order do
L19     if T² − s₁T + s₂ = (T − x₁)(T − x₂) with x₁, x₂ ∈ ℬ then
L20         for (ε₁, ε₂) in (1,1), (1,−1), (−1,1), (−1,−1): if ε₁P_{x₁} + ε₂P_{x₂} = R then return ε₁ at x₁ plus ε₂ at x₂
L21 return NONE
```

Lines L1 to L7 are a [Pohlig-Hellman](/pohlig-hellman/) frame. Line L2 is only a necessary condition for $Q \in \langle P \rangle$, because the group may not be cyclic. For a prime $r$ with $r \,\|\, N$ the Sylow $r$-subgroup has order $r$, so it is $\langle P_r \rangle$ and $Q_r$ lies in it. For $r^2 \mid N$, baby-step giant-step decides membership and solves the logarithm (line L5).

In RELATIONS, line L10 draws $U$ by taking random $x \in \mathbb{F}_{p^2}$ until $x^3 + ax + b$ is a square and then a random square root. The term $rU$ makes $R_j$ range over the whole group: since $r \,\|\, N$, $E(\mathbb{F}_{p^2}) = \langle P \rangle \oplus rE(\mathbb{F}_{p^2})$. Without it, $R_j$ would stay in $\langle P \rangle$, which may be a small subgroup with no decomposable points. Lines L12 to L15 are incremental [Gaussian elimination mod r](/gaussian-elimination-modular/): every new row is reduced against the stored rows, and a row that reduces to $0$ gives a vector $c$ with $\sum c_i e_i \equiv 0 \pmod r$. Multiplying $\sum c_i R_i$ by the cofactor $h = N/r$ kills both the factor base part and the $rU$ terms, and leaves $h(A + xC)P = O$, so $A + xC \equiv 0 \pmod r$. When $C = 0$ the dependency says nothing and the loop goes on.

DECOMPOSE handles one point (line L16) and two points (lines L17 to L20). The polynomial $\rho$ is the resultant of $G_0$ and $G_1$ in $s_2$, of degree at most $4$. Every solution $(s_1, s_2)$ of $G_0 = G_1 = 0$ has $\rho(s_1) = 0$: if $c_1(s_1) \ne 0$ then $\rho(s_1) = c_1^2 G_0(s_1, -c_0/c_1)$, and if $c_1(s_1) = 0$ then $c_0(s_1) = 0$ and $\rho(s_1) = 0$. So line L18 finds the roots of $\rho$ in $\mathbb{F}_p$ with the [Cantor-Zassenhaus algorithm](/cantor-zassenhaus-algorithm/), and for each root takes $s_2 = -c_0/c_1$, or the roots of $G_0(s_1, s_2)$ in $s_2$ when $c_1(s_1) = 0$. If $\rho$ is the zero polynomial, it tries every $s_1 \in \mathbb{F}_p$. Line L19 recovers $x_1, x_2$ from their sum and product, and line L20 finds the signs, since $S_3$ vanishes for $P_1 + P_2$ and for $P_1 - P_2$ alike.

## Example

Take $p = 7$, so $\nu = 3$, and $E : y^2 = x^3 + (1 + 2t)x + (2 + t)$ over $\mathbb{F}_{49}$. It has $N = 41$ points, a prime, so line L6 runs RELATIONS with $r = 41$ and $rU = O$. The factor base is $\mathcal{B} = \{0, 3, 4, 5, 6\}$ with

$P_0 = (0, 2 + 2t)$, $P_3 = (3, 2)$, $P_4 = (4, 3 + 5t)$, $P_5 = (5, 1 + 2t)$, $P_6 = (6, 1 + 3t)$.

Let $P = P_0$ and $Q = (1 + 5t, 1 + 3t)$, which is $23P$. Take the draws $(a_j, b_j) = (j, 1)$ for $j = 1, 2, 3, 4$.

| $j$ | $R_j = jP + Q$ | relation |
|---|---|---|
| 1 | $(6 + 4t, 6 + 5t)$ | $R_1 = 2P_4$ |
| 2 | $(5 + 5t, 6 + 2t)$ | $R_2 = -P_0 - P_6$ |
| 3 | $(6, 6 + 4t)$ | $R_3 = -P_6$ |
| 4 | $(1 + 2t, t)$ | $R_4 = P_4 + P_6$ |

Line L16 handles $R_3$, whose $x$ lies in $\mathcal{B}$, and $y = 6 + 4t = -(1 + 3t)$. For $R_4$, $x_R = 1 + 2t$, so $x_R^2 = 6 + 4t$, and line L17 gives

$G_1 = (1 + 3s_1) s_2 + (5 + 2s_1 + 4s_1^2)$ and $G_0 = s_2^2 + (2 + 5s_1) s_2 + (2 + s_1 + 6s_1^2)$,

$\rho(s_1) = 3 + 2s_1 + 4s_1^2 + s_1^3 + 3s_1^4$, with the roots $3$ and $6$ in $\mathbb{F}_7$.

For $s_1 = 3$: $c_1 = 3$, $c_0 = 5$, so $s_2 = -5 \cdot 3^{-1} = 3$, and $T^2 - 3T + 3$ has discriminant $4$ and the roots $4$ and $6$. Both lie in $\mathcal{B}$, and line L20 finds $R_4 = P_4 + P_6$. The second root $s_1 = 6$ gives $s_2 = 0$ and $\{x_1, x_2\} = \{0, 6\}$, another valid decomposition $R_4 = P_0 - P_6$, which the algorithm does not need.

Over the columns $(0, 3, 4, 5, 6)$ the rows are $(0,0,2,0,0)$, $(-1,0,0,0,-1)$, $(0,0,0,0,-1)$ and $(0,0,1,0,1)$. The first three are independent mod $41$, and the fourth reduces to $0$ with $c = (20, 0, 1, 1)$: indeed $20 \cdot 2 + 1 = 41$ in column $4$ and $-1 + 1 = 0$ in column $6$. Line L13 gives $A = 20 \cdot 1 + 3 + 4 = 27$ and $C = 20 + 1 + 1 = 22$. Since $22^{-1} \equiv 28 \pmod{41}$, line L14 returns $x = -27 \cdot 28 \bmod 41 = 23$, and $23P = Q$.

## Correctness

Every row returned by DECOMPOSE is checked by explicit point arithmetic in line L16 or L20, so $R_j = \sum_x e_{j,x} P_x$ holds. A vector $c$ with $\sum c_i e_i \equiv 0 \pmod r$ gives $\sum c_i R_i = rW$ for a point $W$ in the span of the factor base. Multiplying by $h = N/r$ turns $rW$ and every $rU_i$ into multiples of $N$, which are $O$, so $h(A + xC)P = O$. As $r \nmid h$ and $P$ has order $r$, this means $A + xC \equiv 0 \pmod r$, and line L14 returns the right residue when $C \ne 0$. For termination, each factor base point $P_x$ is decomposed by line L16. Every point of the group is drawn with positive probability, and given $R_j$ the value $b_j$ is still uniform. So some $P_x$ is drawn twice with different $b$, and the two equal rows give a dependency with $C = b_j - b_k \ne 0$. Since the elimination checks a basis of all dependencies, it stops by then. The Pohlig-Hellman frame and the membership test of line L5 complete the argument. See [the correctness proof](proofs/correctness.md).

## Complexity

The factor base has about $p/2$ elements, because $x^3 + ax + b$ is a square in $\mathbb{F}_{p^2}$ for about half of the $x \in \mathbb{F}_p$. The sums $\pm P_{x_1} \pm P_{x_2}$ give about $2|\mathcal{B}|^2 \approx p^2/2$ distinct points, about half the group, so a random $R_j$ decomposes with probability near $1/2$. Measured over $400$ random points, the rate was $0.44$ for $p = 101$ ($|\mathcal{B}| = 51$) and $0.40$ for $p = 307$ ($|\mathcal{B}| = 157$). This is the heuristic step. A dependency with $C \ne 0$ appears after at most $|\mathcal{B}| + 1$ relations plus, on average, $r/(r - 1)$ more, so the expected number of draws is $O(p)$.

Each draw costs three scalar multiplications, $O(\log N)$ group operations, and DECOMPOSE costs $O(\log p)$ multiplications of polynomials of degree at most $4$ over $\mathbb{F}_p$ for the root finding, plus a few square roots. The fallback over all of $\mathbb{F}_p$ when $\rho = 0$ costs $O(p)$ and is rare. Reducing one row against $K$ costs $O(|\mathcal{B}|)$ row operations on vectors of length $O(p)$, so the dense elimination costs $O(p^3)$ operations mod $r$ for each prime $r$, and there are $O(\log N)$ primes. The space is $O(p^2)$ residues for $K$. With baby-step giant-step for the prime powers with $r^2 \mid N$, this gives the header bounds. The rows have at most two nonzero entries, so a sparse method such as structured Gaussian elimination or Wiedemann's algorithm brings the linear algebra to $\tilde O(p^2)$.

For $n = 2$ this is no gain: Pollard rho needs about $\sqrt N \approx p$ group operations on the same group. Galbraith's equation (15.15) gives the general picture for $E(\mathbb{F}_{q^n})$: $\tilde O(2^{c n(n-1)} n!\, q + q^{2 + o(1)})$ bit operations, where the first term is relation search with Gröbner bases and the second is linear algebra on about $q$ columns. For fixed $n$ this is $\tilde O(q^2)$, below rho's $q^{n/2}$ for $n \ge 5$. A double large prime variation lowers it to a heuristic $\tilde O(q^{2 - 2/n})$, which is $\tilde O(q^{4/3})$ for $n = 3$ and $\tilde O(q^{3/2})$ for $n = 4$, against $q^{3/2}$ and $q^2$ for rho. Diem proved that for $a\sqrt{\log q} \le n \le b\sqrt{\log q}$ the logarithm in $E(\mathbb{F}_{q^n})$ costs an expected $e^{O((\log q^n)^{2/3})}$ bit operations, subexponential in the size of the group.

## Properties

- **Las Vegas.** The answer is always correct; only the number of draws is random.
- **Not generic.** The algorithm uses the $x$-coordinates of points and the subfield $\mathbb{F}_p \subset \mathbb{F}_{p^2}$, so the $\sqrt N$ lower bound for generic algorithms does not bind it.
- **Very sparse relations.** Each row has at most $n$ nonzero entries, here $2$, with values $\pm 1$ or $\pm 2$.
- **Degrees grow fast.** $S_m$ has degree $2^{m-2}$ in each variable, so the Weil restriction of $S_{n+1}$ has degree $2^{n-1}$ in each of $n$ unknowns, and the Gröbner basis step is exponential in $n^2$.
- **Needs an extension field.** The factor base comes from a subfield. Over a prime field, Semaev's factor base of points with $0 \le x \le p^{1/m}$ leads to a modular equation with small solutions, and no efficient method to solve it is known.

## Variants and improvements

- **Gaudry's method for general $n$.** Over $\mathbb{F}_{q^n}$, take $\mathcal{B} = \{P : x(P) \in \mathbb{F}_q\}$ and solve $S_{n+1}(x_1, \dots, x_n, x_R) = 0$ with $x_i \in \mathbb{F}_q$ by writing it in a basis of $\mathbb{F}_{q^n}$ over $\mathbb{F}_q$ and computing a Gröbner basis. A point decomposes with probability about $1/n!$. The same paper treats abelian varieties of small dimension in general, so Galbraith calls it Weil descent without divisor class groups.
- **Large primes.** Single and double large prime variations, as in factoring, take a smaller factor base and allow one or two extra points outside it, which balances relation search against linear algebra.
- **Diem's subexponential algorithm.** Diem lets $n$ grow with $q$, uses a factor base defined through an automorphism of the projective line, and proves that the systems have dimension $0$ often enough. With $n \approx \sqrt{\log q}$ he obtains a proved expected subexponential running time.
- **Binary fields and symmetries.** Later work applies the method to curves over $\mathbb{F}_{2^n}$ with a factor base from a vector subspace and uses the symmetry of $S_m$ to shrink the systems. Claims of subexponential time there rest on assumptions about the degrees reached in Gröbner basis computations, and later work questioned these assumptions.
- **Through curves of higher genus.** The [Weil descent attack](/weil-descent-attack/) moves the problem from $E(\mathbb{F}_{q^n})$ to the Jacobian of a curve over $\mathbb{F}_q$ and runs index calculus there.

## When to use it

Use it to study curves over extension fields $\mathbb{F}_{q^n}$ with small $n \ge 3$. For such curves the method, with large primes, is heuristically faster than Pollard rho, and this is one reason why standard curves are defined over prime fields or binary fields of prime degree. For curves over prime fields it gives nothing better than [Pollard rho](/pollard-rho-discrete-logarithm/), and for $n = 2$, as in the code here, it is slower than rho; the toy shows the mechanism, not a speed-up.

## Pitfalls

- **Drawing relations only inside $\langle P \rangle$.** If $\langle P \rangle$ is a small subgroup, none of its points may be a short sum of factor base points, and the loop never ends. Line L10 adds $rU$, which spreads $R_j$ over the whole group and is killed by the cofactor.
- **A prime with $r^2 \mid N$.** Then multiplying by $N/r$ also kills $P$, and a dependency mod $r$ says nothing. Line L5 sends such primes to baby-step giant-step; an alternative is linear algebra mod $r^f$.
- **Taking $nQ = O$ as proof of membership.** The group may be $\mathbb{Z}/m_1 \times \mathbb{Z}/m_2$, and for $r^2 \mid N$ a point of order $r$ need not lie in $\langle P_r \rangle$. Line L5 decides membership there; for $r \,\|\, N$ it is automatic.
- **Dependencies with $C = 0$.** They give $0 = 0$. Lines L13 and L14 check every dependency found, and these form a basis, so the first useful one is never missed.
- **Trusting a root of $S_3$ without the signs.** $S_3$ vanishes for $P_1 + P_2$ and for $P_1 - P_2$, and a root $(s_1, s_2)$ may give $x_1, x_2 \notin \mathbb{F}_p$ or outside $\mathcal{B}$. Lines L19 and L20 check both.
- **A zero resultant.** If $G_0$ and $G_1$ share a factor, for example when the curve and $x_R$ are defined over $\mathbb{F}_p$, then $\rho = 0$ and its roots say nothing. Line L18 then tries every $s_1 \in \mathbb{F}_p$; skipping this step loses relations but gives no wrong answer.

## Implementations

## History

Semaev introduced summation polynomials in 2004 and proposed an index calculus over prime fields with a factor base of points with small $x$, leaving open how to find the small solutions. Gaudry saw that over extension fields the conditions become polynomial systems over the subfield and gave the algorithm for $E(\mathbb{F}_{q^n})$ with fixed $n$, in a preprint of 2004 published in 2009, with the heuristic bound $\tilde O(q^{2-2/n})$. Diem proved subexponential bounds for suitable families of $q$ and $n$ in 2011. Since then the method has been tested on curves over binary and prime power fields, and it has not given an attack on the curves used in standards.

## References
