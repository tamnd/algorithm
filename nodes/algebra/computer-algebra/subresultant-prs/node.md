---
tag: ESA0T9
kind: algorithm
slug: subresultant-prs
name: Subresultant PRS algorithm
aliases: [Collins-Brown subresultant GCD, subresultant chain algorithm, Brown-Traub subresultant PRS]
area: algebra/computer-algebra
level: advanced
summary: Polynomial GCD over Z with bounded coefficient growth via subresultants.
solves: [polynomial-gcd]
model: blum-shub-smale-machine
complexity:
  vars: {m: the degree of f, n: "the degree of g, with 1 <= n <= m"}
  time: {worst: O(m n)}
  space: {extra: O(n^2)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [subresultant, pseudo-division, sylvester-matrix, primitive-prs]
see_also: [subresultant-gcd, resultant, polynomial-gcd, brown-modular-gcd, sturm-sequence, cylindrical-algebraic-decomposition, hadamard-bound, discriminant]
sources:
  - paper: doi:10.1145/321371.321381
    title: George E. Collins, Subresultants and reduced polynomial remainder sequences, Journal of the ACM 14(1), 1967
    locator: pp. 128 to 142 (subresultants as determinants, and the reduced and subresultant sequences)
  - paper: doi:10.1145/321662.321665
    title: W. S. Brown and J. F. Traub, On Euclid's algorithm and the theory of subresultants, Journal of the ACM 18(4), 1971
    locator: pp. 505 to 514 (the fundamental theorem of subresultants, and the gap structure)
  - paper: doi:10.1145/355791.355795
    title: W. S. Brown, The subresultant PRS algorithm, ACM Transactions on Mathematical Software 4(3), 1978
    locator: pp. 237 to 249 (the recurrences for beta and psi, and the proof that every division is exact)
  - paper: doi:10.1016/S0022-4049(98)00081-4
    title: Lionel Ducos, Optimizations of the subresultant algorithm, Journal of Pure and Applied Algebra 145(2), 2000
    locator: pp. 149 to 163 (Lazard's formula for the gap, and a cheaper step after a gap)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 11.2, Subresultants (the structure theorem and the size bounds)
  - book: isbn:9783540330981
    title: Saugata Basu, Richard Pollack and Marie-Françoise Roy, Algorithms in Real Algebraic Geometry, second edition, Springer, 2006
    locator: Chapter 8, Complexity of Basic Algorithms (the signed subresultant sequence and its cost)
  - book: isbn:9780792392590
    title: Keith O. Geddes, Stephen R. Czapor and George Labahn, Algorithms for Computer Algebra, Kluwer, 1992
    locator: Chapter 7, Polynomial GCD Computation (the subresultant PRS)
---

The subresultant PRS algorithm runs the Euclidean algorithm on two polynomials over an integral domain, such as $\mathbb{Z}[x]$, with [pseudo-division](/pseudo-division/), and divides each pseudo-remainder by a factor $\beta$ that is known in advance. The division is exact, and every polynomial it produces is a [subresultant](/subresultant/) of the inputs, a polynomial whose coefficients are determinants of submatrices of the [Sylvester matrix](/sylvester-matrix/). With the gap formula of Brown, Traub and Lazard, the same pass fills in the whole subresultant chain $S_{n-1}, \ldots, S_0$, including the members that are zero, and $S_0$ is the [resultant](/resultant/). The coefficients grow only linearly with the degree, and no gcd of coefficients is needed inside the loop.

## In plain words

To find the common factor of two polynomials with whole-number coefficients, one can divide them repeatedly, as in the school method. To stay with whole numbers, each division first multiplies by a power of a leading number, and then the numbers grow very fast. One cure is to divide each remainder by the gcd of its numbers, but that gcd is costly to find.

This method knows in advance a number that always divides the remainder exactly, and it divides by that. The results are not arbitrary: each one is a determinant built from the two input polynomials, so its size is under control. The same run also gives every member of a list of such determinants, and the last one tells whether the two polynomials have a common root.

## The problem

**Notation.** $R$ is an integral domain with exact division, usually $\mathbb{Z}$ or $K[y]$ for a field $K$. $f, g \in R[x]$ have degrees $m \ge n \ge 1$. $\operatorname{LC}$ is the leading coefficient and $\operatorname{prem}(A, B) = \operatorname{LC}(B)^{\deg A - \deg B + 1} A \bmod B$ is the pseudo-remainder. For $0 \le j < n$, the $j$-th subresultant $S_j \in R[x]$ is the polynomial of degree at most $j$ whose coefficient of $x^i$ is the determinant of the matrix formed by the rows of $x^{n-1-j} f, \ldots, f, x^{m-1-j} g, \ldots, g$, in this order, on the columns of $x^{m+n-j-1}, \ldots, x^{j+1}$ and the column of $x^i$. Its coefficient of $x^j$ is $s_j$, the $j$-th principal subresultant coefficient. $S_j$ is *regular* when $\deg S_j = j$, and *defective* otherwise. We set $s_n = \operatorname{LC}(g)^{m-n}$.

**Input.** $f$ and $g$. **Output.** The chain $S_0, \ldots, S_{n-1}$ and the last nonzero member of the subresultant PRS, which is an associate over the fraction field of $\gcd(f, g)$. $S_0 = \operatorname{Res}(f, g)$.

## The algorithm

```pseudo id=main
SUBRESULTANT-CHAIN(f, g)          ▷ deg f = m ≥ deg g = n ≥ 1
L1  S_j ← 0 for j = 0 .. n - 1
L2  A ← f; B ← g
L3  s ← LC(g)^(m - n)                  ▷ s = s_(deg B)
L4  β ← (-1)^(m - n + 1)
L5  loop
L6      C ← prem(A, B) / β              ▷ exact; C = S_(deg B - 1)
L7      if C = 0 then return S, B
L8      S_(deg B - 1) ← C
L9      e ← deg B - deg C; if e ≥ 2 then S_(deg C) ← LC(C)^(e - 1) C / s^(e - 1)   ▷ exact
L10     if deg C = 0 then return S, C
L11     β ← -LC(B) · (-s)^e
L12     s ← LC(S_(deg C))
L13     A ← B; B ← C
```

The pair $(A, B)$ moves along the subresultant PRS $f, g, S_{n-1}, \ldots$: each new $C$ is the subresultant of index $\deg B - 1$. When the degree drops by $e \ge 2$, $C$ is defective, the subresultants of indices strictly between $\deg C$ and $\deg B - 1$ are zero (they stay 0 from line L1), and the regular subresultant $S_{\deg C}$ is a multiple of $C$, given by line L9. Line L11 is Brown's $\beta$, written with $s = s_{\deg B}$, which is $-\psi$ in Brown's notation. In the normal case, where every $e = 1$, line L9 does nothing and line L11 gives $\beta = -\operatorname{LC}(B) \cdot (-s_{\deg B})$.

To get $\gcd(f, g)$ in $\mathbb{Z}[x]$, take $c = \gcd(\operatorname{cont} f, \operatorname{cont} g)$. If the returned $B$ has degree 0, the gcd is $c$; otherwise it is $c \cdot \operatorname{pp}(B)$, which needs one content computation at the end.

## Example

Let $f = x^5 - x^4 - x^3 - x^2 + 1$ and $g = x^4 - x^3 - x$, so $m = 5$ and $n = 4$.

| pass | $A$ | $B$ | $s$ | $\beta$ | $\operatorname{prem}(A, B)$ | $C$ | $e$ | chain entries set |
|---|---|---|---|---|---|---|---|---|
| 1 | $f$ | $g$ | $1$ | $1$ | $-x^3 + 1$ | $-x^3 + 1$ | 1 | $S_3 = -x^3 + 1$ |
| 2 | $g$ | $-x^3 + 1$ | $-1$ | $1$ | $-1$ | $-1$ | 3 | $S_2 = -1$, $S_0 = -1$ |

In pass 1, $s = \operatorname{LC}(g)^1 = 1$ and $\beta = (-1)^2 = 1$; $f - x g = -x^3 + 1$. In pass 2, line L11 gave $\beta = -1 \cdot (-1)^1 = 1$ and line L12 gave $s = \operatorname{LC}(S_3) = -1$. The pseudo-remainder of $g$ by $-x^3 + 1$ is $(-1)^2 (g \bmod (x^3 - 1)) = -1$, so $C = -1 = S_2$, which is defective: its index is 2 and its degree is 0. So $S_1 = 0$, and line L9 gives $S_0 = (-1)^2 \cdot (-1) / (-1)^2 = -1$. The chain is $S_3 = -x^3 + 1$, $S_2 = -1$, $S_1 = 0$, $S_0 = -1$, and each entry equals its determinant definition. So $\operatorname{Res}(f, g) = -1$ and $\gcd(f, g) = 1$.

## Correctness

Two facts give correctness. The first is the structure theorem of subresultants (Brown and Traub 1971; von zur Gathen and Gerhard, Section 11.2). Put $S_n = \operatorname{LC}(g)^{m-n-1} g$, a polynomial over the fraction field with leading coefficient $s_n$. Let $S_{j+1}$ be regular, and let $S_j \ne 0$ have degree $d \le j$. Then $S_k = 0$ for $d < k < j$, $S_d = (\operatorname{LC}(S_j) / s_{j+1})^{j-d} \, S_j$, and, if $d \ge 1$, $S_{d-1} = \operatorname{prem}(S_{j+1}, S_j) / (-s_{j+1})^{j-d+2}$. If $S_j = 0$, then $S_k = 0$ for all $k < j$. The second fact is the first step, $S_{n-1} = \operatorname{prem}(f, g) / (-1)^{m-n+1}$. The algorithm applies these rules with the previous PRS member $B$ in place of $S_{j+1}$; $B$ is a nonzero multiple of $S_{j+1}$, and the factor cancels between $\operatorname{prem}(B, C)$ and $\operatorname{LC}(B)$. The full argument is in the proof file below. Over the fraction field each $C$ is a nonzero multiple of the Euclidean remainder, so the last nonzero $B$ is an associate of the gcd.

## Complexity

**Cost model.** Ring operations in $R$, including exact divisions, each counted as 1. Over $\mathbb{Z}$ the bit cost also depends on the sizes of the integers.

- **Pseudo-divisions.** The pass with $\deg A = a$ and $\deg B = b$ costs $O((a - b + 1) \, b)$ ring operations. The sum of $a - b + 1$ over the passes is at most $m - n + 1 + n$, and $b \le n$, so the total is $O(n (m + n)) = O(mn)$.
- **Exact divisions and the gap formula.** Line L6 divides $b$ coefficients; line L9 multiplies and divides $\deg C + 1$ coefficients and takes two powers. Over all passes this is $O(n)$ divisions per pass and $O(mn)$ in total, plus $O(\log e)$ multiplications per power.
- **Space.** The chain has $n$ members of degree below $n$, so $O(n^2)$ ring elements; the PRS alone needs $O(m)$.
- **Sizes over $\mathbb{Z}$.** Each $S_j$ is a polynomial whose coefficients are minors of the Sylvester matrix, so by the [Hadamard bound](/hadamard-bound/) they are at most $\|f\|_2^{\,n} \|g\|_2^{\,m}$ in absolute value. For coefficients of $L$ digits this is $O((m + n)(L + \log(m + n)))$ digits. The pseudo-remainder before the division on line L6 is $\beta$ times a subresultant, a product of a few such numbers.

These bounds are proved. With classical integer arithmetic the total bit cost is therefore polynomial in $m$ and $L$: $O(mn)$ operations on integers of $O((m + n)(L + \log(m + n)))$ digits. In practice the [modular gcd](/brown-modular-gcd/) is faster for large dense inputs over $\mathbb{Z}$, and the subresultant PRS wins for small or sparse inputs and when the chain itself is needed.

## Properties

- Deterministic, and division-free except for exact divisions in $R$.
- Every polynomial in the output is a subresultant, so the sizes are bounded as above. The [primitive PRS](/primitive-prs/) gives smaller members but needs a content gcd at each step.
- The degrees in the PRS are those of the Euclidean algorithm over the fraction field.
- The chain, not only the gcd, comes out of one pass. The principal coefficients $s_j$ decide the degree of the gcd: $\deg \gcd(f, g)$ is the least $j$ with $s_j \ne 0$.

## Variants and improvements

- **Subresultant gcd.** The same recurrence, used only to find the gcd, in the form of Cohen's book; see [subresultant gcd](/subresultant-gcd/).
- **Lazard and Ducos.** After a gap of length $e$, line L9 can be computed with $e - 1$ steps of multiply-then-divide, which keeps the intermediate numbers small, and Ducos gives a cheaper formula for the next member after a gap.
- **Signed subresultants.** Basu, Pollack and Roy use the rows of $g$ in reverse order. The signs change in a fixed pattern, and the signs of the principal coefficients then count real roots, as in Sturm-Habicht sequences; see [Sturm sequence](/sturm-sequence/).
- **Fast subresultants.** Over a field, the half-gcd method computes any one subresultant, or the whole chain in a compact form, in $O(M(n) \log n)$ field operations (von zur Gathen and Gerhard, Chapter 11).
- **Modular methods.** Compute the chain modulo many primes and reconstruct each coefficient by the Chinese remainder theorem, which works because the subresultants are polynomials in the coefficients.

## When to use it

Use it when the subresultants themselves are needed: for resultants and discriminants with polynomial coefficients, for the projection step of [cylindrical algebraic decomposition](/cylindrical-algebraic-decomposition/), and for counting real roots with signed subresultants. Use it for gcds over $\mathbb{Z}[x]$ or $K[y][x]$ when the inputs are small or sparse and no prime selection is wanted. For large dense gcds over $\mathbb{Z}$, the modular algorithm is faster.

## Pitfalls

- **The first step is special.** $\beta = (-1)^{m-n+1}$ and $s_n = \operatorname{LC}(g)^{m-n}$. Using the general rule of line L11 for the first step gives wrong signs or an inexact division.
- **Forgetting the gap.** When the degree drops by more than one, $C$ is the subresultant of index $\deg B - 1$, not of index $\deg C$. Code that stores $C$ at index $\deg C$ gets the wrong chain and, for $\deg C = 0$, the wrong resultant.
- **Sign conventions.** Books order the rows of the Sylvester matrix in different ways, which changes the signs of some $S_j$. Compare with a determinant in the same convention before relying on the signs, for example to count real roots.
- **Inexact division means a bug.** Every division on lines L6 and L9 is exact in $R$. If one is not, the recurrence is wrong; truncating the quotient hides the bug.
- **Equal degrees.** For $m = n$, $s_n = 1$ and $\beta = -1$, and the first pseudo-remainder is $\operatorname{LC}(g) f - \operatorname{LC}(f) g$, negated.

## Implementations

## History

Sylvester defined the subresultants as determinants in 1853. Collins introduced polynomial remainder sequences into computer algebra in 1967, proved that the subresultants are, up to known factors, the members of the Euclidean sequence, and gave the reduced and subresultant sequences. Brown and Traub stated the fundamental theorem of subresultants in 1971, and Brown gave the recurrences for $\beta$ and $\psi$ and proved that all divisions are exact in 1978. Lazard noticed the cheap formula for the regular subresultant after a gap, and Ducos published it with further savings in 2000.

## References
