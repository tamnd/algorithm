---
tag: Y89Q1Y
kind: theorem
slug: binomial-theorem
name: Binomial theorem
aliases:
- binomial expansion
- binomial formula
area: combinatorics/counting-algorithms
level: intro
summary: A formula that expands a power of a sum of two terms into a sum of terms weighted by binomial coefficients.
prereqs: [binomial-coefficient]
see_also: [binomial-coefficient, multinomial-coefficient, pascal-triangle-dp, inclusion-exclusion-principle, fermat-little-theorem, binomial-distribution, generating-functions, vandermondes-identity]
sources:
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 5.1, Basic Identities (the binomial theorem for integer and for general exponents)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.6, Binomial Coefficients (the binomial theorem and its history)
  - book: isbn:9780073383095
    title: Kenneth H. Rosen, Discrete Mathematics and Its Applications, seventh edition
    locator: Section 6.4, Binomial Coefficients and Identities (the binomial theorem with a combinatorial proof, and its corollaries)
---

The binomial theorem expands a power of a sum: $(x + y)^n = \sum_{k=0}^{n} \binom{n}{k} x^k y^{n-k}$ for every integer $n \ge 0$, where $\binom{n}{k}$ is the [binomial coefficient](/binomial-coefficient/). It holds for numbers, polynomials and any two elements of a ring that commute. It turns counting facts about subsets into algebra and back: it gives the sums of the rows of Pascal's triangle, the alternating sum behind [inclusion-exclusion](/inclusion-exclusion-principle/), the congruence behind [Fermat's little theorem](/fermat-little-theorem/), and the total probability of the [binomial distribution](/binomial-distribution/).

## Statement

Notation: $[n] = \{1, \ldots, n\}$, and $\binom{n}{k}$ is the number of $k$-element subsets of $[n]$.

**Theorem (binomial theorem).** Let $R$ be a ring, let $x, y \in R$ with $xy = yx$, and let $n \ge 0$ be an integer. Then

$$(x + y)^n = \sum_{k=0}^{n} \binom{n}{k} x^k y^{n-k},$$

where $x^0 = y^0 = 1$ and an integer coefficient $c$ means the sum of $c$ copies of the term. In particular the identity holds for all integers, rational, real and complex numbers, for polynomials and for commuting square matrices.

**Theorem (general exponent).** For every real $r$ and every real $z$ with $|z| < 1$,

$$(1 + z)^r = \sum_{k \ge 0} \binom{r}{k} z^k, \qquad \binom{r}{k} = \frac{r(r-1)\cdots(r-k+1)}{k!}.$$

For an integer $r = n \ge 0$, the terms with $k > n$ vanish, and the series is the first theorem with $x = z$ and $y = 1$. This page proves the first theorem. The series for a general exponent needs analysis (the convergence of the series and the uniqueness of the solution of $(1+z) f'(z) = r f(z)$ with $f(0) = 1$); Concrete Mathematics, Section 5.1, and Knuth, Section 1.2.6, treat it.

## In plain words

To multiply out a power such as (x + y) times (x + y) times (x + y), you pick one of the two letters from each bracket and multiply your picks, in every possible way, and then add all the results. Each result is a product of some copies of x and some copies of y.

How many results have exactly two copies of x? That is the number of ways to choose which two brackets give x, out of three brackets, and the answer is three. So the term with two copies of x and one copy of y appears three times. The binomial theorem says this for every power: the number in front of each term is a binomial coefficient, the number of ways to choose the brackets.

## Proof

*Combinatorial proof.* Write $(x + y)^n = (x + y)(x + y) \cdots (x + y)$ with $n$ factors, numbered $1$ to $n$. By the distributive law, applied $n - 1$ times, the product is the sum over all choices of one term from each factor of the product of the chosen terms, in the order of the factors. A choice is given by the set $S \subseteq [n]$ of the factors from which $x$ is chosen, so

$$(x + y)^n = \sum_{S \subseteq [n]} w_S, \qquad w_S = z_1 z_2 \cdots z_n, \quad z_i = x \text{ if } i \in S, \ z_i = y \text{ if } i \notin S.$$

Since $xy = yx$, the factors of $w_S$ can be reordered, so $w_S = x^{|S|} y^{n - |S|}$. Group the subsets $S$ by their size $k$, by the [rule of sum](/rule-of-sum/). The group of size $k$ has $\binom{n}{k}$ members, and each contributes $x^k y^{n-k}$. This gives the formula. For $n = 0$, the empty product is 1 and the sum has the single term $\binom{0}{0} = 1$. $\square$

*Proof by induction.* For $n = 0$ both sides are 1. Assume the formula for $n - 1 \ge 0$. Then

$$(x + y)^n = (x + y)\sum_{k} \binom{n-1}{k} x^k y^{n-1-k} = \sum_k \binom{n-1}{k} x^{k+1} y^{n-1-k} + \sum_k \binom{n-1}{k} x^k y^{n-k},$$

where the sums run over all integers $k$ and $\binom{n-1}{k} = 0$ outside $0 \le k \le n-1$. The first step uses $y \cdot x^k = x^k y$, which follows from $xy = yx$. Shift $k$ to $k - 1$ in the first sum. The coefficient of $x^k y^{n-k}$ becomes $\binom{n-1}{k-1} + \binom{n-1}{k} = \binom{n}{k}$ by Pascal's rule (proved on the page [binomial coefficient](/binomial-coefficient/)). $\blacksquare$

## Consequences

Each identity follows by a choice of $x$ and $y$ in a commutative ring. Concrete values: $(x + y)^4 = x^4 + 4x^3 y + 6x^2y^2 + 4xy^3 + y^4$, and with $x = 10$, $y = 1$ this gives $11^4 = 14641$, the row $1, 4, 6, 4, 1$ read as digits.

- **Row sums.** With $x = y = 1$: $\sum_{k} \binom{n}{k} = 2^n$. With $x = 2$, $y = 1$: $\sum_k \binom{n}{k} 2^k = 3^n$, which counts the ways to color $[n]$ with three colors by the set of elements that do not get the third color; for $n = 4$ both sides are 81.
- **Alternating sum.** With $x = -1$, $y = 1$: $\sum_{k=0}^{n} (-1)^k \binom{n}{k} = 0^n$, which is 0 for $n \ge 1$ and 1 for $n = 0$. So a nonempty set has as many subsets of even size as of odd size. This is the key step in the proof of the [inclusion-exclusion principle](/inclusion-exclusion-principle/): an element that lies in $m \ge 1$ of the sets is counted $\sum_{k \ge 1} (-1)^{k-1}\binom{m}{k} = 1$ time.
- **Derivatives.** Take the derivative of $(1 + x)^n$ in $x$ and set $x = 1$: $\sum_k k \binom{n}{k} = n 2^{n-1}$. This is also a [double counting](/double-counting/) identity.
- **Fermat's little theorem.** For a prime $p$ and $0 < k < p$, $\binom{p}{k} = p!/(k!(p-k)!)$, and $p$ divides the numerator but not the denominator, so $p \mid \binom{p}{k}$ (for $p = 7$ the row is $1, 0, 0, 0, 0, 0, 0, 1$ modulo 7). So $(a + 1)^p \equiv a^p + 1 \pmod p$, and induction on $a$ gives $a^p \equiv a \pmod p$ for every integer $a \ge 0$. See [Fermat's little theorem](/fermat-little-theorem/).
- **Probability.** With $x = p$ and $y = 1 - p$ for $0 \le p \le 1$, the terms $\binom{n}{k} p^k (1-p)^{n-k}$ are nonnegative and sum to 1. They are the probabilities of the [binomial distribution](/binomial-distribution/).
- **Simple inequalities.** For real $x \ge 0$ all terms of $(1 + x)^n$ are nonnegative, so $(1 + x)^n \ge 1 + nx$ and $(1 + x)^n \ge \binom{n}{k} x^k$ for each $k$. The second inequality with $x = k/n$ gives $\binom{n}{k} \le (1 + k/n)^n (n/k)^k \le (en/k)^k$; see [binomial coefficient bounds](/binomial-coefficient-bounds/).
- **Generating functions.** The theorem says that $(1 + z)^n$ is the [generating function](/generating-functions/) of row $n$ of Pascal's triangle. Comparing coefficients in $(1 + z)^m (1 + z)^n = (1 + z)^{m+n}$ gives [Vandermonde's identity](/vandermondes-identity/).
- **The general exponent.** With $r = \tfrac12$: $\sqrt{1 + z} = 1 + \tfrac12 z - \tfrac18 z^2 + \tfrac1{16} z^3 - \tfrac{5}{128} z^4 + \cdots$. At $z = 0.1$ the first five terms give $1.0488088672$, against $\sqrt{1.1} = 1.0488088482$. With $r = -\tfrac12$ and $z = -4w$ the series gives $\sum_n \binom{2n}{n} w^n = (1 - 4w)^{-1/2}$, the generating function of the central coefficients used for the [Catalan numbers](/catalan-numbers/).
- **More terms.** The multinomial theorem expands $(x_1 + \cdots + x_m)^n$ with the [multinomial coefficients](/multinomial-coefficient/) and has the same proof.

## Tightness

The hypothesis $xy = yx$ cannot be dropped. Take the $2 \times 2$ matrices

$$A = \begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix}, \qquad B = \begin{pmatrix} 0 & 0 \\ 1 & 0 \end{pmatrix}.$$

Then $A^2 = B^2 = 0$, $AB = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}$ and $BA = \begin{pmatrix} 0 & 0 \\ 0 & 1 \end{pmatrix}$. So $(A + B)^2 = A^2 + AB + BA + B^2 = I$, while $A^2 + 2AB + B^2 = 2AB \ne I$. Without commutativity, the expansion has all $2^n$ words in $x$ and $y$, and the words with $k$ copies of $x$ cannot be merged into one term.

The general series needs $|z| < 1$ when $r$ is not a nonnegative integer. For $r = -1$ and $z = 1$ the series is $1 - 1 + 1 - \cdots$, which does not converge, while $(1 + 1)^{-1} = \tfrac12$.

## History

The coefficients of $(x + y)^n$, arranged as a triangle, were known for centuries before Pascal, in Indian, Persian, Chinese and European works; Pascal's treatise on the arithmetic triangle made them a standard tool in Europe, and Newton extended the expansion to fractional and negative exponents (Knuth, Section 1.2.6, gives the history). The combinatorial proof above, by choosing one term from each factor, is the standard modern proof (Rosen, Section 6.4).

## References
