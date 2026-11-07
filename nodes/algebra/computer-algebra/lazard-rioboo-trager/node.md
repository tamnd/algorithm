---
tag: J2RB9Z
kind: algorithm
slug: lazard-rioboo-trager
name: Lazard-Rioboo-Trager algorithm
aliases:
- LRT algorithm
- Lazard-Rioboo-Trager formula
- subresultant method for the logarithmic part
area: algebra/computer-algebra
level: advanced
summary: Gives the logarithmic part of a rational integral explicitly via subresultants.
solves: [integration-of-rational-functions]
model: blum-shub-smale-machine
complexity:
  vars: {n: the degree of the square-free denominator D}
  time: {worst: O(n^4)}
  space: {extra: O(n^3)}
properties: {deterministic: true, recursive: false, in_place: false, online: false}
history:
  year: 1990
  people: [Daniel Lazard, Renaud Rioboo, Barry M. Trager]
  note: Lazard and Rioboo published the subresultant formula for the logarithmic part in 1990; Trager had found it independently and implemented it in Scratchpad, so the method carries all three names.
prereqs: [rothstein-trager, subresultant, resultant, square-free-factorization, integration-of-rational-functions]
see_also: [horowitz-ostrogradsky, hermite-reduction, risch-algorithm, subresultant-prs, liouville-theorem, partial-fraction-decomposition, polynomial-gcd, yun-square-free-factorization]
sources:
  - book: isbn:9783540214939
    title: Manuel Bronstein, Symbolic Integration I, Transcendental Functions, second edition, Springer, 2005
    locator: Chapter 2, Integration of rational functions, Section 2.5 (the Lazard-Rioboo-Trager algorithm, with the subresultant theorem it relies on) and Section 2.4 (the Rothstein-Trager resultant)
  - paper: "Daniel Lazard and Renaud Rioboo, Integration of rational functions: rational computation of the logarithmic part, Journal of Symbolic Computation 9(2), 1990"
    locator: the theorem that the subresultant of index i specializes to gcd(D, A - alpha D') at each root alpha of multiplicity i
  - book: isbn:9780792392590
    title: Keith O. Geddes, Stephen R. Czapor and George Labahn, Algorithms for Computer Algebra, Kluwer, 1992
    locator: Chapter 11, Integration of rational functions (the Rothstein-Trager method and the Lazard-Rioboo-Trager improvement)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 6, The resultant and gcd computation (subresultants and their gcd property) and Chapter 22, Symbolic integration (the logarithmic part)
  - paper: "Thom Mulders, A note on subresultants and the Lazard/Rioboo/Trager formula in rational function integration, Journal of Symbolic Computation 24(1), 1997"
    locator: the choice of subresultant in defective cases
---

The Lazard-Rioboo-Trager algorithm computes the logarithmic part of $\int A/D \, dx$, for $A, D \in K[x]$ over a field $K$ of characteristic $0$ with $D$ square-free and $\deg A < \deg D$, without computing in any algebraic extension of $K$. The [Rothstein-Trager](/rothstein-trager/) theorem says
$$\int \frac{A}{D}\, dx = \sum_{R(\alpha) = 0} \alpha \log \gcd(D, A - \alpha D'), \qquad R(t) = \operatorname{res}_x(D, A - tD').$$
Computed literally, that needs a gcd over $K(\alpha)$ for every root $\alpha$. Lazard, Rioboo and Trager observed that the gcds come for free from the [subresultants](/subresultant/) of $D$ and $A - tD'$ with respect to $x$, computed once over $K[t]$. If $R = c \prod_i Q_i^i$ is the [square-free factorization](/square-free-factorization/), then at every root $\alpha$ of $Q_i$ the $i$-th subresultant $S_i(t, x)$ specializes to a constant multiple of $\gcd(D, A - \alpha D')$. The output is a finite list of pairs $(Q_i, S_i)$, all with coefficients in $K$.

## In plain words

When a fraction has only simple poles, its integral is a sum of logarithms, one for each pole. The coefficient in front of each logarithm is the residue at that pole. Poles that share a residue can be grouped into one logarithm of a polynomial. The residues are the roots of a polynomial $R$, and each group is a gcd. Computing these gcds root by root would need arithmetic with algebraic numbers such as $\sqrt{2}$ or $i$. This algorithm avoids it. One subresultant computation, done with $t$ kept as a symbol, gives a polynomial $S_i(t, x)$. Substituting any residue $\alpha$ of the right kind for $t$ then gives exactly the logarithm's argument.

## The problem

**Input.** A field $K$ of characteristic $0$, such as $\mathbb{Q}$, and $A, D \in K[x]$ with $D$ square-free, $n = \deg D \ge 1$ and $\deg A < n$. This is the input left over after [Hermite reduction](/hermite-reduction/) or the [Horowitz-Ostrogradsky method](/horowitz-ostrogradsky/).

**Output.** Pairs $(Q_i, S_i)$ with $Q_i \in K[t]$ square-free and pairwise coprime and $S_i \in K[t][x]$, such that
$$\int \frac{A}{D}\, dx = \sum_i \sum_{Q_i(\alpha) = 0} \alpha \log S_i(\alpha, x).$$
The inner sum runs over the roots of $Q_i$ in an algebraic closure. Each $S_i$ is monic in $x$ of degree $i$, with coefficients reduced modulo $Q_i$.

## The algorithm

Write $B = A - tD' \in K[t][x]$, of formal degree $n - 1$ in $x$. The subresultants $S_j$ of $D$ and $B$ with respect to $x$, for $0 \le j < n$, are polynomials in $K[t][x]$ of degree at most $j$ in $x$, defined by determinants of submatrices of the Sylvester matrix. $S_0 = R$ is the resultant. They can be computed together by the [subresultant PRS](/subresultant-prs/) algorithm over $K[t]$.

```pseudo id=main
LRT(A, D)                              ▷ D square-free, deg A < deg D = n
L1  R(t) ← res_x(D, A − tD')                       ▷ the subresultant S_0
L2  (Q_1, ..., Q_n) ← square-free factorization:  R = c · Q_1 Q_2^2 ⋯ Q_n^n
L3  for each i with deg Q_i > 0 do
L4      if i = n then S_i ← D
L5      else S_i ← the i-th subresultant of D and A − tD' with respect to x
L6      (A_1, ..., A_q) ← square-free factorization of lc_x(S_i)
L7      for j = 1, ..., q do S_i ← S_i / gcd(A_j, Q_i)^j        ▷ coefficientwise in t
L8      reduce the coefficients of S_i modulo Q_i and make S_i monic in x
L9  return Σ_i Σ_{Q_i(α)=0} α log S_i(α, x)
```

Lines L6 and L7 remove factors of the leading coefficient that vanish at roots of $Q_i$. When $S_i$ is the subresultant defined by determinants, as here, the proof shows that $\gcd(\operatorname{lc}_x S_i, Q_i) = 1$, so these lines change nothing. They matter when $S_i$ is taken from a pseudo-remainder sequence that only gives it up to a factor in $K[t]$, as in Bronstein's presentation. Line L8 is possible because $\operatorname{lc}_x S_i$ is then invertible modulo $Q_i$.

## Example

Integrate $A/D$ with $A = x^4 - 3x^2 + 6$ and $D = x^6 - 5x^4 + 5x^2 + 4$ over $\mathbb{Q}$. $D$ is square-free.

| line | result |
|---|---|
| L1 | $R(t) = 45796\,(4t^2 + 1)^3$, and $45796 = 214^2$ |
| L2 | $Q_3 = t^2 + \tfrac{1}{4}$, all other $Q_i = 1$ |
| L5 | $S_3 = -214\,t\,x^3 + 107\,x^2 + 642\,t\,x - 214$, reduced modulo $Q_3$ |
| L6, L7 | $\operatorname{lc}_x S_3 = -214\,t$ is coprime to $Q_3$: no change |
| L8 | multiply by $(-214\,t)^{-1} \equiv \tfrac{2}{107}\, t \pmod{Q_3}$: $S_3 = x^3 + 2t x^2 - 3x - 4t$ |
| L9 | $\displaystyle \int \frac{A}{D}\, dx = \sum_{4\alpha^2 + 1 = 0} \alpha \log\bigl(x^3 + 2\alpha x^2 - 3x - 4\alpha\bigr)$ |

The residues are $\alpha = \pm i/2$, each shared by three of the six poles. The answer uses only rational numbers and the symbol $\alpha$. Rothstein-Trager would need a gcd over $\mathbb{Q}(i)$. A smaller case: for $1/(x^3 + x)$, $R$ is a constant multiple of $(t - 1)(t + \tfrac{1}{2})^2$, and the output is $(t - 1, x)$ and $(t + \tfrac{1}{2}, x^2 + 1)$, that is $\log x - \tfrac{1}{2} \log(x^2 + 1)$. The tests check both results with an exact certificate equivalent to differentiation.

## Correctness

Over a splitting field, $A/D = \sum_\beta r_\beta / (x - \beta)$ with residues $r_\beta = A(\beta)/D'(\beta)$, since $D$ is square-free. The resultant is $R(t) = c \prod_\beta (t - r_\beta)$, so a root $\alpha$ of $R$ of multiplicity $m$ is the residue at exactly $m$ poles. Those poles are the roots of $G_\alpha = \gcd(D, A - \alpha D')$, which therefore has degree $m$. The derivative of $\sum_\alpha \alpha \log G_\alpha$ is $\sum_\beta r_\beta / (x - \beta) = A/D$. By the gcd property of subresultants, $S_m(\alpha, x)$ is a nonzero constant multiple of $G_\alpha$, because $S_m$ specializes correctly under $t \mapsto \alpha$ and $\operatorname{lc}(D)$ does not depend on $t$. The roots of $Q_i$ are exactly the roots of $R$ of multiplicity $i$, so line L5 uses the right index. The full proof is in the proof file below.

## Complexity

The cost model counts operations in $K$, as on a [BSS machine](/blum-shub-smale-machine/) over $K$, with classical polynomial arithmetic. Let $n = \deg D$. Each $S_j$ has degree at most $j$ in $x$ and at most $n - j$ in $t$. These bounds are proved:

- **Lines L1 and L5.** The subresultant PRS over $K[t]$ takes $O(n^2)$ operations on polynomials in $t$ of degree $O(n)$, each costing $O(n^2)$, so $O(n^4)$ in all, and it stores the sequence in $O(n^3)$ space.
- **Line L2.** Yun's square-free factorization of $R$, of degree $n$ in $t$, costs $O(n^2)$.
- **Lines L6 to L8.** At most $n$ coefficients of degree $O(n)$ per $S_i$ are divided and reduced, $O(n^3)$ in all.

The total is $O(n^4)$ operations and $O(n^3)$ space. Over $\mathbb{Q}$ the bit cost also depends on coefficient growth, which subresultants keep polynomial. Evaluation and interpolation in $t$ with fast arithmetic lower the cost. The implementation below computes each needed $S_i$ by determinants at $n + 1$ values of $t$ followed by interpolation, which is simpler and costs about $n^5$ operations per subresultant. No factorization over $K$ is needed at any step, which in practice is the main gain over Rothstein-Trager. That is an observation about typical inputs.

## Properties

- **No algebraic extensions.** Every computation is in $K[t]$ and $K[t][x]$, and the output is in $K$.
- **Minimal extension.** The answer is expressed over the splitting fields of the $Q_i$. Trager showed that no antiderivative needs a smaller extension of $K$, so this one is optimal.
- **Same answer as Rothstein-Trager.** The pairs give exactly $\sum_\alpha \alpha \log \gcd(D, A - \alpha D')$, grouped by multiplicity.
- **No factorization needed.** Only a square-free factorization of $R$ is computed. Factoring the $Q_i$ further is optional and only splits the sums.

## Variants and improvements

- **Rothstein-Trager.** Factor $R$ into irreducibles over $K$ and compute $\gcd(D, A - \alpha D')$ over $K[t]/(P)$ for each irreducible factor $P$. This is [Rothstein-Trager](/rothstein-trager/), and it needs arithmetic in the extension fields.
- **Real form.** Rioboo's algorithm turns pairs of complex conjugate logarithms into real arctangents of polynomials, without introducing new algebraic numbers.
- **Fast subresultants.** With evaluation and interpolation in $t$, or the half-gcd approach to subresultants, the subresultant step can be done with fewer operations.
- **Risch algorithm.** The same subresultant idea computes the logarithmic part in the transcendental cases of the [Risch algorithm](/risch-algorithm/).

## When to use it

Use it for the logarithmic part of every rational integral, after removing the rational part with [Hermite reduction](/hermite-reduction/) or [Horowitz-Ostrogradsky](/horowitz-ostrogradsky/). It is the method used in modern computer algebra systems, because it needs neither factorization over $K$ nor arithmetic in algebraic extensions.

## Pitfalls

- **Non-square-free $D$.** The resultant then vanishes identically or the residue argument fails. Remove the rational part first.
- **Wrong subresultant index.** The argument for the roots of $Q_i$ is the subresultant of index $i$, not the $i$-th polynomial of a remainder sequence. With a defective sequence they can differ.
- **Leading coefficient vanishing at a root.** A remainder sequence can produce $S_i$ with $\operatorname{lc}_x S_i$ sharing a factor with $Q_i$. Then $S_i(\alpha, x)$ has the wrong degree or is zero. Lines L6 and L7 remove such factors.
- **Ignoring the case $i = n$.** If a single residue is shared by all poles, then $A = \alpha D'$, the integral is $\alpha \log D$, and the argument is $D$ itself.
- **Not reducing modulo $Q_i$.** The coefficients of $S_i$ can be large polynomials in $t$. Reducing modulo $Q_i$ keeps them below $\deg Q_i$ without changing $S_i(\alpha, x)$.

## Implementations

## History

Rothstein (1976) and Trager (1976) found the resultant formula for the logarithmic part. Trager also showed that it uses the smallest possible algebraic extension. Lazard and Rioboo published the subresultant version in 1990. Trager had found it independently and implemented it in Scratchpad, the predecessor of Axiom, but did not publish it, so it is called the Lazard-Rioboo-Trager algorithm. Mulders (1997) clarified which subresultant must be used. Bronstein, Chapter 2, gives the standard modern account.

## References
