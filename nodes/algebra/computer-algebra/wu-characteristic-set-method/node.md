---
tag: RYT59J
kind: algorithm
slug: wu-characteristic-set-method
name: Wu's characteristic set method
aliases: [Wu's method, Ritt-Wu method, Ritt-Wu characteristic set algorithm, Wu-Ritt decomposition, Wu's zero decomposition]
area: algebra/computer-algebra
level: research
summary: Decomposes polynomial systems into characteristic sets and proves geometric theorems mechanically.
solves: [polynomial-system-solving]
model: blum-shub-smale-machine
complexity:
  vars: {m: "the number of input polynomials", n: "the number of variables", d: "the degree bound of the input polynomials"}
  time: {worst: "(m d)^(n^(O(1)))"}
  space: {extra: "(m d)^(n^(O(1)))"}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [characteristic-set, pseudo-division]
see_also: [regular-chain, triangular-decomposition, groebner-basis, buchberger-algorithm, ideal-membership-problem, hilbert-nullstellensatz, primary-decomposition, quantifier-elimination]
sources:
  - paper: "Wu Wen-Tsün, On the decision problem and the mechanization of theorem-proving in elementary geometry, Scientia Sinica 21, 1978"
    title: On the decision problem and the mechanization of theorem-proving in elementary geometry
    locator: pp. 159 to 172 (the method for geometry theorems)
  - paper: doi:10.1007/BF02328447
    title: Wu Wen-Tsün, Basic principles of mechanical theorem proving in elementary geometries, Journal of Automated Reasoning 2(3), 1986
    locator: pp. 221 to 252 (characteristic sets, the well-ordering principle and the zero decomposition)
  - book: doi:10.1090/coll/033
    title: Joseph Fels Ritt, Differential Algebra, AMS Colloquium Publications 33, 1950
    locator: Chapter 1 and Chapter 4 (ascending sets, characteristic sets and the algebraic case)
  - book: isbn:9783319167206
    title: David A. Cox, John Little and Donal O'Shea, Ideals, Varieties, and Algorithms, 4th edition, Springer, 2015
    locator: Chapter 6, Section 5 (Wu's method) and Section 4 (automatic geometric theorem proving)
  - book: doi:10.1007/978-94-009-4037-6
    title: Shang-Ching Chou, Mechanical Geometry Theorem Proving, Reidel, 1988
    locator: Chapters 1 to 4 (Wu's method and 512 theorems proved by it)
  - book: doi:10.1007/978-1-4612-4344-1
    title: Bhubaneswar Mishra, Algorithmic Algebra, Springer, 1993
    locator: Chapter 5 (characteristic sets and geometry theorem proving)
  - paper: doi:10.1007/978-1-4612-0441-1_8
    title: Giovanni Gallo and Bhubaneswar Mishra, Efficient algorithms and bounds for Wu-Ritt characteristic sets, Effective Methods in Algebraic Geometry, Progress in Mathematics 94, 1991
    locator: pp. 119 to 142 (singly exponential degree bounds and algorithms by linear algebra)
  - paper: doi:10.1007/3-540-52885-7_89
    title: Shang-Ching Chou and Xiao-Shan Gao, Ritt-Wu's decomposition algorithm and geometry theorem proving, CADE 10, LNCS 449, 1990
    locator: pp. 207 to 220
---

Wu's method computes a [characteristic set](/characteristic-set/) of a system of polynomial equations: a triangular set $C$ of polynomials from the ideal whose zeros contain the zeros of the system, and which contain them back away from the zeros of the initials. Repeating it on the initials gives Wu's zero decomposition, which writes the zero set of any system as a finite union of quasi-varieties of triangular sets. To prove a geometry theorem, one writes the hypotheses and the conclusion as polynomials in coordinates, computes a characteristic set of the hypotheses and checks that the conclusion pseudo-divides to zero; the initials give the non-degeneracy conditions under which the theorem holds.

## In plain words

You want to know whether a statement about a figure is true, for example that the diagonals of a parallelogram cut each other in half. Put the figure on a grid and write each condition as an equation in the coordinates of the points. First rearrange the conditions into a staircase: one equation for the first unknown point coordinate, the next for the second, and so on. Then take the claim and divide it step by step by the staircase, from the top down. If nothing is left, the claim follows from the conditions, except in flat or collapsed figures, which the method lists for you. The same staircase idea splits the solutions of any system of equations into simple pieces.

## The problem

Let $K$ be a field (the code uses $\mathbb{Q}$, the integers inside $\mathbb{Q}$, or $\mathbb{Z}/p\mathbb{Z}$), $\bar K$ an algebraic closure, and $K[x_1, \ldots, x_n]$ with the variable order $x_1 < \cdots < x_n$. For a set $P$ of polynomials let $\operatorname{Zero}(P) \subseteq \bar K^n$ be the set of common zeros, and $\operatorname{Zero}(P / h) = \operatorname{Zero}(P) \setminus \operatorname{Zero}(h)$. For a nonconstant $p$, the main variable is the largest variable in $p$, the class $\operatorname{cls}(p)$ is its index, and the initial $\operatorname{init}(p)$ is the leading coefficient of $p$ in the main variable; this is the analogue of LC for the recursive representation, and no monomial order is used. An ascending set (a Ritt chain) is a list $C_1, \ldots, C_r$ with strictly increasing classes in which each $C_j$ has lower degree than $C_i$ in the main variable of $C_i$ for $i < j$. Let $I_C = \prod_k \operatorname{init}(C_k)$.

The tasks are:

- **Characteristic set.** Given finite $P$, find an ascending set $C \subseteq (P)$ with $\operatorname{prem}(p, C) = 0$ for all $p \in P$. Then $\operatorname{Zero}(C / I_C) \subseteq \operatorname{Zero}(P) \subseteq \operatorname{Zero}(C)$ (Wu's well-ordering principle).
- **Zero decomposition.** Find ascending sets $C^{(1)}, \ldots, C^{(s)}$ with $\operatorname{Zero}(P) = \bigcup_i \operatorname{Zero}(C^{(i)} / I_{C^{(i)}})$.
- **Theorem proving.** Given hypotheses $H$ and a conclusion $g$, decide whether $g$ vanishes on $\operatorname{Zero}(H)$ outside the zeros of some non-degeneracy conditions.

## The algorithm

The basic set of $P$ is an ascending set of lowest rank inside $P$: go through $P$ by increasing rank (class, then degree in the main variable) and keep each polynomial whose class is larger than the last one kept and which is reduced with respect to those kept. A nonzero constant alone is the lowest basic set. Pseudo-division by a chain, $\operatorname{prem}(p, C)$, reduces by $C_r$, then $C_{r-1}$, down to $C_1$, using [pseudo-division](/pseudo-division/) in each main variable.

```pseudo id=main
CHARSET(P)                                  ▷ Ritt-Wu characteristic set of P
L1  loop
L2    B ← BASIC-SET(P)
L3    if B is a nonzero constant: return B  ▷ Zero(P) is empty
L4    R ← { prem(p, B) : p ∈ P \ B } \ {0}
L5    if R = ∅: return B
L6    P ← P ∪ R
```

```pseudo id=dec
DECOMPOSE(P)                                ▷ Zero(P) = ∪ Zero(C / I_C)
D1  stack ← [P]; out ← []; while stack is not empty: Q ← pop(stack)
D2    C ← CHARSET(Q), and Q' ← Q with all remainders added
D3    if C is a nonzero constant: continue
D4    append C to out
D5    for each C_k whose initial h_k is not a constant
D6      push Q' ∪ {h_k}
```

```pseudo id=prove
WU-PROVE(H, g)                              ▷ does g follow from H generically?
W1  C ← CHARSET(H); if C is a constant: return true
W2  r ← prem(g, C)
W3  return (r = 0, the nonconstant initials of C)
```

The decomposition uses an explicit stack, not recursion. Practical versions split polynomials into irreducible factors before they are added, which keeps the pieces small and makes each piece irreducible (Wu's irreducible decomposition).

## Example

The diagonals of a parallelogram bisect each other. Put $A = (0, 0)$, $B = (u_1, 0)$, $D = (u_2, u_3)$, $C = (x_1, x_2)$ and the intersection of the diagonals $O = (x_3, x_4)$. The parameters $u_1, u_2, u_3$ are free, and the order is $u_1 < u_2 < u_3 < x_1 < x_2 < x_3 < x_4$. The hypotheses are

$$h_1 = x_2 - u_3, \quad h_2 = (x_1 - u_1) u_3 - x_2 u_2, \quad h_3 = x_4 x_1 - x_3 x_2, \quad h_4 = x_4 (u_2 - u_1) - u_3 (x_3 - u_1),$$

for $DC \parallel AB$, $BC \parallel AD$, $O \in AC$ and $O \in BD$. CHARSET adds remainders in three rounds and stops in the fourth, with

$$C_1 = u_3 x_1 - u_3 (u_1 + u_2), \quad C_2 = x_2 - u_3, \quad C_3 = u_1 u_3^2 (2 x_3 - u_1 - u_2), \quad C_4 = u_1 u_3^3 (u_1 + u_2)(2 x_4 - u_3).$$

The conclusion $g = 2 x_3 - x_1$ (O is the midpoint of $AC$) reduces to $0$: by $C_3$, $2 u_1 u_3^2\, g - 2 C_3 = -2 u_1 u_3^2 x_1 + 2 u_1 u_3^2 (u_1 + u_2)$, and by $C_1$, $u_3$ times this plus $2 u_1 u_3^2 C_1$ is $0$. The same holds for $2 x_4 - x_2$. So the theorem holds when the initials $u_3$, $2 u_1 u_3^2$ and $2 u_1 u_3^3 (u_1 + u_2)$ are nonzero: $D$ is not on the line $AB$, $A \ne B$, and $C$ is not on the vertical axis ($x_1 = u_1 + u_2 \ne 0$). The last condition comes from the way $h_3$ was written. The false claim $x_3 = x_4$ leaves a nonzero remainder of degree $9$ in the parameters. The test file checks all of these by script.

## Correctness

Every remainder is an element of the ideal $(P)$, so the sets keep the same zeros. A nonzero remainder is reduced with respect to the basic set, so adding it makes the basic set strictly lower in the rank order on ascending sets, and this order has no infinite descending sequences; hence CHARSET stops. When it stops, every $p$ has remainder $0$, so $I_C^e\, p \in (C)$, which gives $\operatorname{Zero}(C / I_C) \subseteq \operatorname{Zero}(P)$, while $C \subseteq (P)$ gives $\operatorname{Zero}(P) \subseteq \operatorname{Zero}(C)$. A zero of $P$ either avoids all initials or is a zero of $P \cup \{h_k\}$ for some $k$; each $h_k$ is reduced with respect to $C$, so the branches go down in rank and the decomposition tree is finite. The prover is sound by the first inclusion. The full proof is in [proofs/correctness.md](proofs/correctness.md).

The prover is not complete as stated. If $\operatorname{Zero}(C)$ is reducible, $g$ can vanish on the component that matters and not on the others, and then $\operatorname{prem}(g, C) \ne 0$ although the theorem is true there. Wu's full method decomposes into irreducible ascending sets and tests each one; over $\mathbb{C}$ it is then complete for the generic truth of theorems of this kind.

## Complexity

The cost model is operations in $K$. Over $\mathbb{Z}$ or $\mathbb{Q}$ the code counts operations on exact integers, whose size can grow exponentially with the number of pseudo-division steps, so the bit cost is larger.

- **One round.** A pseudo-remainder by an ascending set of $r \le n$ polynomials takes at most $D (d+1)^{r-1}$ pseudo-division steps for a polynomial of degree $D$, by the same count as for [regular chains](/regular-chain/). This bound is proved.
- **The plain loop.** The number of rounds is bounded only through the well-ordering of ascending sets, and Gallo and Mishra (1991) state that Ritt's algorithm and Wu's modifications have a non-elementary worst-case time.
- **Better algorithms.** Gallo and Mishra (1991) proved singly exponential degree bounds for a characteristic set and derived from them an algorithm by linear algebra with singly exponential sequential time, $(m d)^{n^{O(1)}}$ in the notation of the summary; this is the bound in the front matter. The exact exponent is in their paper.
- **Decomposition.** The tree can have many branches; its size has no good proved bound. Because it computes a superset of all components including embedded ones, the decomposition is at least as hard as listing the irreducible components, which can be exponential in number. For [Gröbner bases](/groebner-basis/) the worst case is doubly exponential (Mayr and Meyer 1982); Wu's method avoids this in typical geometry problems because it never computes a basis of the ideal.
- **In practice.** For geometry theorems the hypotheses are often already triangular, and the method is fast: Chou (1988) proved 512 theorems this way, most in seconds on the machines of that time.

## Properties

- Deterministic, with no randomness; the code uses only ring operations and zero tests, so it runs over $\mathbb{Z}$ without fractions.
- The output depends on the variable order; a good order puts the free parameters first.
- The characteristic set describes $\operatorname{Zero}(P)$ only up to the zeros of the initials; the decomposition makes the description exact.
- Membership $\operatorname{prem}(p, C) = 0$ is sufficient for $p$ to vanish on $\operatorname{Zero}(C / I_C)$, but it is not a test for membership in $(P)$ or in its radical.

## Variants and improvements

- **Weak characteristic sets.** Wu's original version only asks that the initial of each polynomial be reduced, not the whole polynomial, which gives smaller sets and faster rounds.
- **Irreducible decomposition.** Factor over algebraic extensions given by the earlier polynomials, so that every ascending set is irreducible and its saturated ideal is prime. Then the prover is complete for generic truth.
- **Regular chains.** Requiring each initial to be regular modulo the earlier polynomials gives [regular chains](/regular-chain/), for which pseudo-division decides membership in the saturated ideal; modern [triangular decomposition](/triangular-decomposition/) builds on them.
- **Finite fields.** Gao, Huang and coauthors adapted characteristic sets to equations over finite fields with the field equations $x^q - x$, for algebraic cryptanalysis.
- **Differential and difference algebra.** Ritt's original setting was differential polynomials; characteristic sets of differential and difference systems use the same loop with differential pseudo-division.
- **Gröbner methods.** Kapur and Kutzler used Gröbner bases for the same geometry problems; they decide membership in the radical of the hypothesis ideal saturated by the degeneracy conditions.

## When to use it

Use Wu's method to prove or explore geometry statements that are equalities between coordinates, and to split a polynomial system into triangular pieces when a lex Gröbner basis is too costly. For exact ideal membership use a [Gröbner basis](/groebner-basis/). For statements with inequalities or over the real numbers, use [quantifier elimination](/quantifier-elimination/) instead, since Wu's method works over an algebraically closed field.

## Pitfalls

- **Degenerate cases.** The theorem is proved only away from the zeros of the initials. Some conditions are real degeneracies, others are artifacts of how the hypotheses were written, as $u_1 + u_2 \ne 0$ in the example. Read them before trusting the proof.
- **Reducible configurations.** A true theorem can give a nonzero remainder when the hypotheses describe several configurations, for example the two bisectors of an angle. Decompose into irreducible pieces before deciding.
- **Real geometry.** Results hold over the complex numbers. A statement that needs a point to be between two others, or a length to be positive, is outside the method.
- **Coefficient growth.** Each pseudo-division multiplies by an initial, so contents such as $u_1 u_3^3$ pile up, as in $C_4$ above. Remove contents and factor as you go.
- **Order of reduction.** Pseudo-divide by the polynomial of the largest class first; the other order leaves a result that is not reduced.
- **Variable order.** A bad order can make the characteristic set huge. Put parameters first and the dependent coordinates in the order the construction defines them.

## Implementations

## History

Ritt defined characteristic sets for differential polynomials in his books of 1932 and 1950, as a constructive approach to the decomposition of differential varieties. Wu Wen-Tsün took up Ritt's algebraic case in 1977 and 1978, made it into an algorithm for proving theorems of elementary geometry, and proved many theorems with it on the computers of the Chinese Academy of Sciences. His 1986 paper in the Journal of Automated Reasoning described the method for a wide audience. Chou (1988) implemented it in the United States and proved 512 theorems, which made it the best-known algebraic method of automated geometry. Chou and Gao (1990) gave the Ritt-Wu decomposition algorithm in a complete form, and Gallo and Mishra (1991) gave the first complexity bounds. Work on characteristic sets led to the theory of [regular chains](/regular-chain/) and to triangular decompositions in the 1990s.

## References
