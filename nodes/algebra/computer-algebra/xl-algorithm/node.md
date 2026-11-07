---
tag: JSBYXR
kind: algorithm
slug: xl-algorithm
name: XL algorithm
aliases: [extended linearization, XL, eXtended Linearization, Courtois-Klimov-Patarin-Shamir algorithm]
area: algebra/computer-algebra
level: research
summary: Solves polynomial systems by multiplying equations by monomials and linearizing, mainly over small finite fields.
solves: [multivariate-quadratic-problem, polynomial-system-solving]
model: blum-shub-smale-machine
complexity:
  vars: {m: "the number of equations", n: "the number of variables", D: "the XL degree", T: "the number of monomials of degree at most D"}
  time: {worst: O(m T^3)}
  space: {extra: O(m T^2)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [macaulay-matrix, gaussian-elimination, multivariate-quadratic-problem]
see_also: [f4-algorithm, f5-algorithm, groebner-basis, hilbert-series, block-wiedemann-algorithm, wiedemann-algorithm, buchberger-algorithm, wu-characteristic-set-method]
sources:
  - paper: doi:10.1007/3-540-45539-6_27
    title: Nicolas Courtois, Alexander Klimov, Jacques Patarin and Adi Shamir, Efficient algorithms for solving overdefined systems of multivariate polynomial equations, EUROCRYPT 2000, LNCS 1807
    locator: pp. 392 to 407 (the XL and FXL algorithms and their estimated complexity)
  - paper: doi:10.1007/3-540-48405-1_2
    title: Aviad Kipnis and Adi Shamir, Cryptanalysis of the HFE public key cryptosystem by relinearization, CRYPTO 1999, LNCS 1666
    locator: pp. 19 to 30 (relinearization, the predecessor of XL)
  - paper: doi:10.1007/978-3-540-30539-2_24
    title: Gwénolé Ars, Jean-Charles Faugère, Hideki Imai, Mitsuru Kawazoe and Makoto Sugita, Comparison between XL and Gröbner basis algorithms, ASIACRYPT 2004, LNCS 3329
    locator: pp. 338 to 353 (XL as a redundant form of F4)
  - paper: doi:10.1007/978-3-540-30539-2_23
    title: Claus Diem, The XL-algorithm and a conjecture from commutative algebra, ASIACRYPT 2004, LNCS 3329
    locator: pp. 323 to 337 (the success degree and Fröberg's conjecture)
  - paper: doi:10.1007/11496618_7
    title: Bo-Yin Yang and Jiun-Ming Chen, All in the XL family, theory and practice, ICISC 2004, LNCS 3506
    locator: pp. 67 to 86 (the success degree of XL and its variants from the Hilbert series)
  - paper: doi:10.1007/978-3-540-88403-3_14
    title: Mohamed Saied Emam Mohamed, Wael Said Abd Elmageed Mohamed, Jintai Ding and Johannes Buchmann, MXL2, solving polynomial equations over GF(2) using an improved mutant strategy, PQCrypto 2008, LNCS 5299
    locator: pp. 203 to 215
  - book: isbn:9783319167206
    title: David A. Cox, John Little and Donal O'Shea, Ideals, Varieties, and Algorithms, 4th edition, Springer, 2015
    locator: Chapter 3, Section 1 (elimination ideals) and Chapter 2, Section 10 (linear algebra in Buchberger's algorithm)
---

XL (extended linearization) solves a system of polynomial equations over a finite field by linear algebra alone. It multiplies every equation by all monomials up to some degree, treats each monomial of the products as a new unknown, and runs Gaussian elimination with the monomials in one variable placed last. When the degree is large enough, the elimination produces a polynomial in that one variable; its roots give the possible values, and the rest of the system is solved by substitution. Courtois, Klimov, Patarin and Shamir introduced it in 2000 for the overdefined quadratic systems of multivariate cryptography.

## In plain words

You have many equations with many unknowns, and the unknowns are multiplied together, so the usual school method does not work. XL makes the problem bigger to make it easier. It multiplies every equation by every product of unknowns up to some size, which gives many more equations. Then it pretends that each product of unknowns, such as the first unknown times the second, is a brand new unknown. Now all equations are of the simple straight kind, and ordinary elimination can be used. If there are enough independent equations, the elimination leaves an equation with only one unknown. You find its values by trying them all, put each value back, and repeat with one unknown fewer.

## The problem

Let $\mathbb{F}_q$ be a finite field; the code uses $\mathbb{F}_p = \mathbb{Z}/p\mathbb{Z}$ for a small prime $p$. Given $f_1, \ldots, f_m \in \mathbb{F}_q[x_1, \ldots, x_n]$, usually of degree $2$ (the [multivariate quadratic problem](/multivariate-quadratic-problem/)), find the solutions $a \in \mathbb{F}_q^n$ with $f_i(a) = 0$ for all $i$. The system is overdefined when $m > n$. Only solutions with coordinates in $\mathbb{F}_q$ are wanted, so one may add the field equations $x_i^q - x_i = 0$, which is the same as working in $A = \mathbb{F}_q[x_1, \ldots, x_n]/(x_1^q - x_1, \ldots, x_n^q - x_n)$, where every exponent is at most $q - 1$. The code does this; over $\mathbb{F}_2$ all monomials are then products of distinct variables. Throughout, $D$ is the XL degree, $T$ the number of reduced monomials of degree at most $D$, and $\pi(S)$ the set of first coordinates of the solution set $S$. No monomial order is needed except the column order below; it is a degree order with the powers of $x_1$ last, so the leading monomial LM of each echelon row is the first column where it is nonzero.

## The algorithm

```pseudo id=main
XL-STEP(f_1..f_m, D)                       ▷ one XL step at degree D
L1  rows ← { u · f_i : u a monomial, deg u ≤ D - deg f_i }, reduced by x^p = x
L2  columns ← the monomials of degree ≤ D, the powers of x_1 last (1 at the very end)
L3  E ← reduced row echelon form of the matrix rows × columns over F_p
L4  G ← the rows of E that are zero outside the columns of 1, x_1, ..., x_1^(p-1)
L5  if some g ∈ G is a nonzero constant: return none
L6  if G is not empty: return G            ▷ univariate polynomials in x_1
L7  return fail                            ▷ raise D and try again
```

```pseudo id=solve
XL-SOLVE(f_1..f_m)                         ▷ all solutions in F_p^n
S1  D ← max deg f_i; while XL-STEP fails and D < n(p-1) + max deg f_i: D ← D + 1
S2  values ← common roots of G in F_p, or all of F_p if the last step failed
S3  for each value c: substitute x_1 ← c and solve the system in x_2..x_n (a stack, no recursion)
S4  with no variables left, keep the point if every equation became 0
```

The matrix in L3 is the [Macaulay matrix](/macaulay-matrix/) of degree $D$ of the system, restricted to the reduced monomials. The univariate polynomials are found by [Gaussian elimination](/gaussian-elimination/) over $\mathbb{F}_p$. Over $\mathbb{F}_p$ the roots in S2 are found by trying all $p$ values; over a large field one takes the gcd with $x^q - x$ and factors.

## Example

Over $\mathbb{F}_2$ with $n = 3$, take

$$f_1 = x_1 x_2 + x_3, \quad f_2 = x_1 + x_2 x_3 + 1, \quad f_3 = x_1 x_3 + x_2 + x_3.$$

At $D = 2$ there are only the $3$ rows $f_1, f_2, f_3$ in the $7$ monomials $x_1 x_2, x_1 x_3, x_2 x_3, x_1, x_2, x_3, 1$, and no row is free of the non-univariate columns, so the step fails. At $D = 3$ the multipliers are $1, x_1, x_2, x_3$, which gives $12$ rows in all $8$ reduced monomials (the extra one is $x_1 x_2 x_3$). Elimination finds the univariate row $x_1 + 1$. One combination that shows it: with $x_i^2 = x_i$,

$$x_2 f_1 + f_2 + x_1 f_3 = (x_1 x_2 + x_2 x_3) + (x_1 + x_2 x_3 + 1) + (x_1 x_3 + x_1 x_2 + x_1 x_3) = x_1 + 1.$$

So $x_1 = 1$. Substituting gives $x_2 + x_3$, $x_2 x_3$ and $x_2$. The last one already gives $x_2 = 0$ at degree $1$, and then $x_3 = 0$. The only solution is $(1, 0, 0)$, which agrees with trying all $8$ points. The test file runs this example and records the degrees used at each level, $3$, $2$ and $1$.

## Correctness

Every row is a multiple of some $f_i$, so every row of the echelon form lies in the ideal $I$ of the system, and a univariate row vanishes at the first coordinate of every solution. A nonzero constant row shows that there is no solution. In $A$ every function from $\mathbb{F}_p^n$ to $\mathbb{F}_p$ is a polynomial, and $I$ is exactly the set of functions vanishing on the solution set. At the full degree $D = n(p-1) + \max \deg f_i$ the rows span all of $I$, and the echelon rows that are zero outside the univariate columns span $I \cap \mathbb{F}_p[x_1]$, so their common roots are exactly $\pi(S)$, and the step fails only when every value of $\mathbb{F}_p$ occurs. Substitution then reduces the number of variables by one. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

The cost model is operations in $\mathbb{F}_q$. One step at degree $D$ builds at most $R \le m T$ rows with $T$ columns. Elimination costs $O(R\, T \min(R, T)) \subseteq O(m T^3)$ operations and $O(m T^2)$ space for a dense matrix; this is proved, and with fast matrix multiplication the exponent $3$ drops to $\omega$. For quadratic equations over a large field, $T = \binom{n + D}{D}$; over $\mathbb{F}_2$ with field equations, $T = \sum_{j \le D} \binom{n}{j}$.

The open question is the degree $D$ at which XL first succeeds. With the field equations, the full degree $n(q-1) + 2$ always works, so XL never needs more than $O(m q^{3n})$ operations, but that is worse than trying all $q^n$ points. For random systems the success degree is not proved. Yang and Chen (2004) and Diem (2004) express it through the [Hilbert series](/hilbert-series/) of the system: for semi-regular systems it is close to the degree of regularity, which also governs [F4](/f4-algorithm/) and [F5](/f5-algorithm/), and Diem's analysis depends on a conjecture of Fröberg. Courtois and coauthors (2000) estimated polynomial time when $m \ge \varepsilon n^2$ for a fixed $\varepsilon > 0$, which agrees with these analyses, while their estimates for $m$ close to $n$ were later found to be too optimistic. For general [Gröbner basis](/groebner-basis/) computation the worst case is doubly exponential in $n$ (Mayr and Meyer 1982); with field equations the ideal is zero-dimensional and the degrees are at most $n(q-1)$, which is why XL and F4 stay singly exponential here.

## Properties

- Deterministic, and uses only Gaussian elimination and univariate root finding.
- The matrices are very sparse: a row has at most as many entries as its equation has terms.
- XL is a special strategy for F4: Ars, Faugère, Imai, Kawazoe and Sugita (2004) showed that when XL succeeds at degree $D$, a version of F4 also succeeds at degree $D$ with smaller matrices, so XL does redundant work.
- Without field equations, XL works with the solutions in the algebraic closure and needs the system to have finitely many of them. The field equations restrict it to solutions in $\mathbb{F}_q$.

## Variants and improvements

- **Relinearization.** Kipnis and Shamir (1999) introduced the idea for HFE: treat products $x_i x_j$ as new unknowns and add the relations among them. XL generalizes and simplifies it.
- **FXL.** Fix $f$ variables by guessing their values, then run XL on the smaller, more overdefined system; the guesses multiply the cost by $q^f$ but can lower $D$ a lot.
- **XL2, XFL and MutantXL.** Variants that find extra equations at the same degree. MutantXL and MXL2 multiply low-degree "mutant" rows found during elimination, which often solves the system at a lower degree, as in F4 with a good selection strategy.
- **Sparse XL with Wiedemann.** Instead of dense elimination, find a univariate polynomial with the [block Wiedemann algorithm](/block-wiedemann-algorithm/), which needs only matrix times vector products and little memory. Large instances from multivariate cryptography have been attacked in this way.
- **Gröbner algorithms.** [F4](/f4-algorithm/) and [F5](/f5-algorithm/) choose only useful rows and avoid the reductions to zero that XL keeps; they are the usual choice outside very overdefined cases.

## When to use it

Use XL for overdefined systems over small finite fields, mainly quadratic systems from multivariate cryptography, when you want a simple method whose cost is set by one large sparse matrix. It is also a clear way to estimate the cost of algebraic attacks. For general systems, systems over the rational numbers, or when you need the whole ideal, use F4 or F5 instead.

## Pitfalls

- **Success degree.** The degree that works is not known in advance. Raising $D$ by one multiplies the matrix size by about $n/D$, so a wrong guess is costly.
- **Rank is not enough.** XL needs a univariate row, not just a large rank. Count the free monomials: as long as the number of independent rows is less than the number of non-univariate monomials, no univariate row can be forced.
- **Field equations.** Without them, solutions in an extension field also count, and over $\mathbb{F}_2$ the monomial count is wrong. With them, use reduced exponents everywhere, including in the multipliers.
- **Column order.** The univariate columns must be the last ones. A different order gives correct echelon rows but hides the univariate polynomial.
- **Underdefined systems.** When $m < n$ there are many solutions, and the elimination cannot isolate one variable. Fix some variables first, as in FXL.
- **Memory.** Dense elimination needs $T^2$ entries. Use sparse elimination or Wiedemann methods for large $T$.

## Implementations

## History

Linearization, treating each monomial as a new unknown, is old. Kipnis and Shamir (1999) used relinearization to attack the HFE cryptosystem, and Courtois, Klimov, Patarin and Shamir (2000) turned it into XL and FXL and estimated that very overdefined quadratic systems can be solved in polynomial time. The algorithm drew attention as a possible threat to multivariate cryptography and to block ciphers through algebraic attacks. In 2004 Ars, Faugère, Imai, Kawazoe and Sugita related XL to F4, and Diem and Yang and Chen analyzed its success degree through the Hilbert series. Mutant variants by Ding, Buchmann, Mohamed and others followed from 2008, and sparse XL with block Wiedemann is used to estimate the security of multivariate signature schemes.

## References
