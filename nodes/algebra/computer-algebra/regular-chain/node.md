---
tag: 1VMKVR
kind: data-structure
slug: regular-chain
name: Regular chain
aliases: [regular triangular set, regular set, regular system of polynomials, Kalkbrener triangular set]
area: algebra/computer-algebra
level: research
summary: A triangular set with a non-degeneracy condition, used to represent components of polynomial systems.
implements: [polynomial]
model: blum-shub-smale-machine
complexity:
  vars: {r: "the number of polynomials in the chain", d: "the degree bound for the chain in all variables", D: "the degree of the input polynomial"}
  time: {worst: O(D (d+1)^(r-1))}
  space: {extra: O(d^r)}
prereqs: [pseudo-division, resultant, polynomial-ideal]
see_also: [triangular-decomposition, characteristic-set, wu-characteristic-set-method, lazard-structure-theorem, groebner-basis, rational-univariate-representation, primary-decomposition, cylindrical-algebraic-decomposition]
sources:
  - paper: doi:10.1006/jsco.1993.1011
    title: Michael Kalkbrener, A generalized Euclidean algorithm for computing triangular representations of algebraic varieties, Journal of Symbolic Computation 15(2), 1993
    locator: pp. 143 to 167 (regular triangular sets and the generalized gcd modulo a chain)
  - paper: doi:10.1006/jsco.1999.0269
    title: Philippe Aubry, Daniel Lazard and Marc Moreno Maza, On the theories of triangular sets, Journal of Symbolic Computation 28(1-2), 1999
    locator: pp. 105 to 124 (regular chains and the theorem that p is in sat(T) if and only if prem(p, T) = 0)
  - paper: doi:10.1006/jsco.1999.0355
    title: Dongming Wang, Computing triangular systems and regular systems, Journal of Symbolic Computation 30(2), 2000
    locator: pp. 221 to 236 (regular systems)
  - paper: doi:10.1016/j.jsc.2011.12.023
    title: Changbo Chen and Marc Moreno Maza, Algorithms for computing triangular decompositions of polynomial systems, Journal of Symbolic Computation 47(6), 2012
    locator: pp. 610 to 642 (regularity test, regular gcd and the Triangularize algorithm)
  - paper: doi:10.1016/j.jsc.2008.04.019
    title: Xin Li, Marc Moreno Maza and Éric Schost, Fast arithmetic for triangular sets, from theory to practice, Journal of Symbolic Computation 44(7), 2009
    locator: pp. 891 to 907 (multiplication modulo a zero-dimensional triangular set)
  - paper: doi:10.1145/1113439.1113456
    title: François Lemaire, Marc Moreno Maza and Yuzhen Xie, The RegularChains library in Maple, ACM SIGSAM Bulletin 39(3), 2005
    locator: pp. 96 to 97
  - book: isbn:9783319167206
    title: David A. Cox, John Little and Donal O'Shea, Ideals, Varieties, and Algorithms, 4th edition, Springer, 2015
    locator: Chapter 6, Section 5 (Wu's method, triangular sets, pseudo-division and the saturation ideal)
---

A regular chain is a triangular set of polynomials $T_1, \ldots, T_r$ in which each initial (leading coefficient in the main variable) is not a zero divisor modulo the earlier polynomials. It represents the variety of its saturated ideal $\operatorname{sat}(T)$, and it gives exact answers to two questions: whether a polynomial lies in $\operatorname{sat}(T)$ (pseudo-divide and test for zero) and whether it is a zero divisor there (an iterated resultant). Triangular decompositions write the solutions of any polynomial system as a finite union of regular chains.

## In plain words

A regular chain is a list of equations that you can solve one variable at a time. The first equation contains only the first unknown. The next one adds one more unknown, and so on, like a staircase. To use such a staircase you divide by the leading coefficient of each step. The rule of a regular chain says that this coefficient can never be zero on the solutions found so far, on any of their pieces. With this rule the staircase answers questions without error. A polynomial vanishes on all the solutions exactly when repeated division by the steps leaves nothing. A polynomial vanishes on no piece exactly when a chain of resultants is not zero. Programs that solve systems of equations split the solutions into a few such staircases.

## The abstract type

The abstract type is a [polynomial](/polynomial/) system in $K[x_1, \ldots, x_n]$ over a field $K$, read as the ideal it defines, with the variables ordered $x_1 < x_2 < \cdots < x_n$. For a nonconstant polynomial $p$, the main variable $\operatorname{mvar}(p)$ is the largest variable in $p$, the main degree is $\deg_{\operatorname{mvar}(p)} p$, and the initial $\operatorname{init}(p)$ is the leading coefficient of $p$ as a polynomial in its main variable. (These replace LT, LM and LC of a monomial order: here the leading coefficient is itself a polynomial in the smaller variables.) A triangular set $T = (T_1, \ldots, T_r)$ is a list of nonconstant polynomials with $\operatorname{mvar}(T_1) < \cdots < \operatorname{mvar}(T_r)$. Let $h_T$ be the product of the initials, and

$$\operatorname{sat}(T) = (T) : h_T^{\infty} = \{ p : h_T^e\, p \in (T) \text{ for some } e \ge 0 \}.$$

$T$ is a **regular chain** when, for $k = 2, \ldots, r$, $\operatorname{init}(T_k)$ is regular (not a zero divisor, and not zero) modulo $\operatorname{sat}(T_1, \ldots, T_{k-1})$. The operations are: test whether a triangular set is a regular chain, reduce a polynomial by the chain, test membership $p \in \operatorname{sat}(T)$, and test whether $p$ is regular modulo $\operatorname{sat}(T)$. The variety $V(\operatorname{sat}(T))$ is the Zariski closure of the quasi-component $W(T) = V(T) \setminus V(h_T)$. For a regular chain, $\operatorname{sat}(T)$ is unmixed of dimension $n - r$, and the variables that are not main variables are algebraically independent modulo it (Aubry, Lazard and Moreno Maza 1999).

## Representation

A chain is a list of polynomials in sparse form, sorted by main variable. A polynomial is a dictionary from exponent vectors to coefficients in $K$; the code uses Python `Fraction` for $K = \mathbb{Q}$. The variable $x_i$ of the page is the index $i$ of the exponent vector. Nothing else is stored: the main variables, degrees and initials are read from the polynomials. Larger systems also store the initials and the saturated-ideal dimension, and for zero-dimensional chains a dense representation of $K[x]/(T)$ with $\prod_k d_k$ coefficients (Li, Moreno Maza and Schost 2009).

## Operations

### Reduction and membership

```pseudo id=main
IN-SAT(p, T = (T_1..T_r))                 ▷ is p in sat(T)? T must be a regular chain
L1  for k ← r down to 1                   ▷ top variable first: PREM-CHAIN
L2    p ← prem(p, T_k)                    ▷ pseudo-remainder in mvar(T_k)
L3  return p = 0
```

The pseudo-remainder $\operatorname{prem}(p, T_k)$ repeats $p \leftarrow \operatorname{init}(T_k)\, p - c\, y^{m - d} T_k$, where $y = \operatorname{mvar}(T_k)$, $m = \deg_y p \ge d = \deg_y T_k$ and $c$ is the leading coefficient of $p$ in $y$, until $\deg_y p < d$. See [pseudo-division](/pseudo-division/). Reducing from the top down keeps the earlier reductions valid. The result $r$ is reduced (its degree in each $\operatorname{mvar}(T_k)$ is below the main degree of $T_k$), and $h_T^e\, p - r \in (T)$.

### Regularity test

```pseudo id=reg
IS-REGULAR(p, T)                          ▷ is p a non-zero-divisor modulo sat(T)?
R1  p ← PREM-CHAIN(p, T); if p = 0: return false
R2  for k ← r down to 1: if deg_{mvar(T_k)} p > 0: p ← res_{mvar(T_k)}(p, T_k); return p ≠ 0
IS-REGULAR-CHAIN(T)
R3  if some T_k is constant, or the main variables are not increasing: return false
R4  for k ← 2 to r
R5    if not IS-REGULAR(init(T_k), (T_1..T_{k-1})): return false;  return true
```

The [resultant](/resultant/) is the determinant of the Sylvester matrix, computed with fraction-free Bareiss elimination over the polynomial ring. The value after the last step contains only the free variables, so the test is exact. Production systems avoid the full iterated resultant: they compute regular gcds modulo the chain and split it when an initial turns out to be a zero divisor (the D5 principle of dynamic evaluation), which is how [triangular decomposition](/triangular-decomposition/) algorithms proceed (Chen and Moreno Maza 2012).

## Example

Take $K = \mathbb{Q}$, $n = 3$, and

$$T_1 = x_1^2 - 2, \quad T_2 = x_1 x_2 - 1, \quad T_3 = x_2 x_3^2 - x_1.$$

The main variables are $x_1 < x_2 < x_3$ and the initials are $1$, $x_1$ and $x_2$.

- **Is it a regular chain?** $\operatorname{res}_{x_1}(x_1, x_1^2 - 2) = -2 \ne 0$, so $x_1$ is regular modulo $(T_1)$. For $x_2$, $\operatorname{prem}(x_2, T_2) = x_1 x_2 - (x_1 x_2 - 1) = 1$, which is regular. So $T$ is a regular chain.
- **Membership of $x_3^2 - 2$.** Reduce by $T_3$: $x_2 (x_3^2 - 2) - T_3 = x_1 - 2 x_2$. Reduce by $T_2$: $x_1 (x_1 - 2x_2) + 2 T_2 = x_1^2 - 2$. Reduce by $T_1$: $0$. So $x_3^2 - 2 \in \operatorname{sat}(T)$.
- **Non-membership of $x_3^2$.** The same steps give $\operatorname{prem}(x_3^2, T) = x_1 \ne 0$.
- **A zero divisor.** For $p = x_3 - x_1$ the pseudo-remainder is $p$. Then $\operatorname{res}_{x_3}(p, T_3) = x_1^2 x_2 - x_1$ and $\operatorname{res}_{x_2}(x_1^2 x_2 - x_1, x_1 x_2 - 1) = 0$. So $p$ is a zero divisor: it vanishes on the two of the four points of $V(T)$ where $x_3 = x_1$.
- **A regular element.** For $p = x_3 + 1$ the resultants are $x_2 - x_1$, then $x_1^2 - 1$, then $\operatorname{res}_{x_1}(x_1^2 - 1, x_1^2 - 2) = 1 \ne 0$. So $x_3 + 1$ is invertible modulo $\operatorname{sat}(T)$.

The saturation matters when an initial can vanish on $V(T)$. For the chain $(x_1 x_2 - x_1)$ with $x_1$ free, $(T)$ describes the line $x_2 = 1$ and the extra line $x_1 = 0$, while $\operatorname{sat}(T) = (x_2 - 1)$ keeps only the first. Here $x_2 - 1 \in \operatorname{sat}(T)$ but $x_2 - 1 \notin (T)$.

## Correctness

Let $F = K(U)$, where $U$ are the variables that are not main variables. If $T$ is a regular chain, then each initial is a unit of $R_{k-1} = F[y_1, \ldots, y_{k-1}]/(T_1, \ldots, T_{k-1})$, so $R_k = R_{k-1}[y_k]/(T_k)$ is a free $R_{k-1}$-module with basis $1, \ldots, y_k^{d_k - 1}$. A reduced polynomial is a combination of basis monomials, so it lies in $\operatorname{sat}(T)$ only if it is $0$; this gives $p \in \operatorname{sat}(T) \iff \operatorname{prem}(p, T) = 0$. Regular modulo $\operatorname{sat}(T)$ means invertible in the finite-dimensional algebra $R_r$, and for a monic $M$ the resultant $\operatorname{res}(M, a)$ is the determinant of multiplication by $a$, so invertibility passes down the tower one resultant at a time. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

Costs are counted in operations of $K$ on polynomials in sparse form, and the counts of steps below are proved. The time bound in the summary counts pseudo-division steps, and the space bound counts the monomials in the main variables of a reduced polynomial, at most $d^r$; each such monomial has a coefficient in the free variables.

| operation | cost |
|---|---|
| chain test | $r - 1$ regularity tests |
| pseudo-remainder by one $T_k$ | at most $m - d_k + 1$ steps, each a product and a difference |
| reduction by the chain (L1 to L2) | $O(D (d+1)^{r-1})$ pseudo-division steps |
| regularity test | one reduction and at most $r$ resultants, each the determinant of a Sylvester matrix of size at most the degree of the current polynomial plus $d$ |
| zero-dimensional chain, product modulo $T$ | $O(4^r \delta)$ operations in $K$ up to logarithmic factors, $\delta = d_1 \cdots d_r$ |

The bound on reduction steps holds because every step by $T_k$ multiplies by $\operatorname{init}(T_k)$, which raises the degree in the smaller main variables by at most $d$, so the degree in $y_{k-1}$ after level $k$ is at most $D (d+1)^{r-k+1}$. The degrees and coefficient sizes of iterated resultants grow multiplicatively: $\operatorname{res}(p, T)$ can have degree $\prod_k d_k$ times that of $p$, so over $\mathbb{Q}$ the bit cost of the plain test is exponential in $r$. The last line of the table is the result of Li, Moreno Maza and Schost (2009) for monic zero-dimensional chains with fast univariate multiplication; it is proved. In practice the RegularChains library uses modular methods and regular gcds, and the observed costs are far below the plain bounds above for most systems.

## Variants

- **Triangular sets in the sense of Wu and Ritt.** A [characteristic set](/characteristic-set/) is an ascending set without the regularity condition. It can have $\operatorname{sat}(T) = (1)$, and membership by pseudo-division is then only a sufficient test. See [Wu's method](/wu-characteristic-set-method/).
- **Squarefree regular chains.** In addition, each $T_k$ is squarefree modulo $\operatorname{sat}(T_{<k})$. Then $\operatorname{sat}(T)$ is radical, so it is the ideal of the closure of $W(T)$.
- **Normalized and simple chains.** In a normalized chain every initial involves only free variables. A simple system (Wang) and a Lazard triangular set have initials that never vanish on the solutions, so $W(T) = V(T)$ and the chain describes points exactly, not only up to closure. A zero-dimensional normalized chain has constant initials, so after scaling it is monic, and it is a lex [Gröbner basis](/groebner-basis/) because its leading monomials $y_k^{d_k}$ are pairwise coprime. [Lazard's structure theorem](/lazard-structure-theorem/) describes the general shape of such bases.
- **Regular semi-algebraic systems.** For real solutions, a regular chain is combined with inequalities, as in cylindrical algebraic decomposition by triangular decomposition (Chen and Moreno Maza).
- **Differential regular chains.** Boulier and others extend the notion to differential polynomial rings, which is the base of the RosenfeldGroebner algorithm.

## When to use it

Use regular chains to describe the solutions of a polynomial system component by component, when you need the dimension, generic points or a parametric description of each component, and when a lex Gröbner basis would be too large. Triangular decompositions into regular chains are often much smaller than a Gröbner basis for systems with many positive-dimensional components. For a single zero-dimensional radical system a [rational univariate representation](/rational-univariate-representation/) or a Gröbner basis is usually simpler.

## Pitfalls

- **Saturation, not the ideal.** $V(T)$ can contain extra components where an initial vanishes. A regular chain describes $V(\operatorname{sat}(T))$, which is the closure of $W(T)$, not $V(T)$.
- **Regularity is not non-vanishing.** An initial can be regular and still vanish at some solutions, as $x_1$ does for the chain $(x_1 x_2 - x_1)$ with $x_1$ free. Then the chain misses the line $x_1 = 0$ of $V(T)$, which a decomposition must cover by other chains.
- **The membership test needs regularity.** For a triangular set that is not a regular chain, $\operatorname{prem}(p, T) = 0$ implies $p \in \operatorname{sat}(T)$, but the converse can fail.
- **Order of reduction.** Reduce by the polynomial with the largest main variable first. Reducing bottom up leaves the result not reduced.
- **Coefficient growth.** Iterated resultants and repeated multiplication by initials blow up quickly. Work modulo primes or use regular gcds when the chain is long.
- **Zero divisors in towers.** Over a chain that is not a tower of fields (for example $T_1 = x_1^2 - 1$), an element can be nonzero and still not invertible, so a gcd computation must be ready to split the chain.

## Implementations

## History

Ritt introduced characteristic sets of differential and algebraic polynomials in the 1930s and 1950, and Wu Wen-Tsün made them practical for geometry theorem proving from 1977 on. The regularity condition came in the early 1990s from two directions. Yang Lu and Zhang Jingzhong defined regular sets around 1991, and Kalkbrener (1993) defined regular triangular sets and gave a generalized Euclidean algorithm for gcds modulo such a set. Lazard (1991, 1992) gave a related theory for zero-dimensional systems. Aubry, Lazard and Moreno Maza (1999) showed that these definitions agree and proved the membership theorem by pseudo-division. Wang (2000) gave regular systems. The test of regularity by iterated resultants is used by Wang and by Chen and Moreno Maza (2012). Moreno Maza and coauthors built the RegularChains library in Maple, which is the main implementation, and Chen and Moreno Maza (2012) described incremental algorithms for triangular decomposition based on regularity tests and regular gcds.

## References
