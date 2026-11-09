---
tag: T9XS87
kind: definition
slug: derangement
name: Derangement
aliases:
- Derangements
- derangement number
- fixed-point-free permutation
- fixed-point-free permutations
- subfactorial
- problème des rencontres
area: combinatorics/counting-algorithms
level: intro
summary: A permutation with no fixed points; their count is about n!/e.
prereqs: [permutation, inclusion-exclusion-principle]
see_also: [inclusion-exclusion-principle, permutation, factorial, permutation-cycle-decomposition, exponential-generating-functions, generating-involutions, binomial-coefficient, linearity-of-expectation]
sources:
  - book: isbn:9780136020400
    title: Richard A. Brualdi, Introductory Combinatorics, fifth edition
    locator: Chapter 6, The Inclusion-Exclusion Principle and Applications (Section 6.3, Derangements)
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Chapter 2, Sieve Methods (Section 2.2, Examples and special cases, the derangement problem)
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 5.3, Tricks of the trade (the subfactorial n¡ and its recurrences)
---

A derangement of a set is a [permutation](/permutation/) that moves every element: no element stays in its own place. The number of derangements of $n$ elements, written $D_n$ or $!n$ (the subfactorial), is $n!\sum_{j=0}^{n} (-1)^j/j!$, which is the integer closest to $n!/e$ for $n \ge 1$. So a uniformly random permutation has no fixed point with probability close to $1/e \approx 0.3679$, already to six decimal places for $n = 10$. The count is the standard first example of the [inclusion-exclusion principle](/inclusion-exclusion-principle/), and the question goes back to Montmort's *problème des rencontres* of 1708.

## Definition

Notation: $[n] = \{1, \ldots, n\}$, $S_n$ is the set of the $n!$ permutations of $[n]$, and $\binom{n}{k}$ is the [binomial coefficient](/binomial-coefficient/).

A **fixed point** of $\sigma \in S_n$ is an $i \in [n]$ with $\sigma(i) = i$. A **derangement** is a permutation with no fixed point. The **derangement number** $D_n$ is the number of derangements of $[n]$. For $n = 0$, the empty permutation has no fixed point, so $D_0 = 1$; and $D_1 = 0$.

In cycle notation, a permutation is a derangement exactly when its [cycle decomposition](/permutation-cycle-decomposition/) has no cycle of length 1.

**Formula.** For $n \ge 0$,
$$D_n = \sum_{j=0}^{n} (-1)^j \binom{n}{j}(n-j)! = n!\sum_{j=0}^{n} \frac{(-1)^j}{j!}.$$

*Proof.* Let $A_i$ be the set of permutations that fix $i$. A permutation in $\bigcap_{i \in J} A_i$ fixes the $j = |J|$ points of $J$ and permutes the other $n - j$ freely, so there are $(n - j)!$ of them. By the symmetric form of inclusion-exclusion, $D_n = \sum_{j} (-1)^j\binom{n}{j}(n-j)!$, and $\binom{n}{j}(n-j)! = n!/j!$. $\square$

**Recurrences.** $D_n = (n - 1)(D_{n-1} + D_{n-2})$ for $n \ge 2$, and $D_n = n D_{n-1} + (-1)^n$ for $n \ge 1$.

*Proof of the first.* Let $\sigma$ be a derangement of $[n]$, $n \ge 2$, and let $i = \sigma(n)$, so $i \ne n$: there are $n - 1$ choices of $i$. Fix $i$. If $\sigma(i) = n$, then $\sigma$ swaps $i$ and $n$, and its restriction to the other $n - 2$ elements is any derangement of them: $D_{n-2}$ cases. If $\sigma(i) \ne n$, let $a = \sigma^{-1}(n)$; then $a \ne n$ and $a \ne i$. Define $\tau$ on $[n-1]$ by $\tau(a) = i$ and $\tau(x) = \sigma(x)$ for $x \ne a$. This removes $n$ from its cycle ($a \to n \to i$ becomes $a \to i$), so $\tau$ is a permutation of $[n-1]$, and it has no fixed point, since $\tau(a) = i \ne a$ and $\tau(x) = \sigma(x) \ne x$ otherwise. Conversely, from a derangement $\tau$ of $[n-1]$, let $a = \tau^{-1}(i)$ and set $\sigma(a) = n$, $\sigma(n) = i$ and $\sigma(x) = \tau(x)$ otherwise. Then $\sigma$ is a derangement with $\sigma(n) = i$, and $\sigma(i) \ne n$ because $\sigma(i) = n$ would mean $i = a$, that is $\tau(i) = i$. The two maps are inverse, so this case has $D_{n-1}$ elements. Summing over the $n - 1$ values of $i$ gives the recurrence. $\square$

*Proof of the second.* From the formula, $D_n - nD_{n-1} = n!\bigl(\sum_{j=0}^{n} \frac{(-1)^j}{j!} - \sum_{j=0}^{n-1}\frac{(-1)^j}{j!}\bigr) = n!\frac{(-1)^n}{n!} = (-1)^n$. $\square$

**Nearest integer.** For $n \ge 1$, $|D_n - n!/e| < 1/(n+1) \le \tfrac12$, so $D_n$ is the integer closest to $n!/e$.

*Proof.* $n!/e - D_n = n!\sum_{j > n} (-1)^j/j!$. This is an alternating series with decreasing terms, so its absolute value is at most the first term $n!/(n+1)! = 1/(n+1)$, and strictly less since the second term is nonzero. $\square$

## Examples and non-examples

**Example 1 (small values).** $D_0, D_1, \ldots, D_{10}$ are $1, 0, 1, 2, 9, 44, 265, 1854, 14833, 133496, 1334961$ (OEIS A000166). The derangements of $[3]$ in one-line notation are $231$ and $312$, the two 3-cycles.

**Example 2 ($n = 4$).** The nine derangements of $[4]$ are $2143$, $2341$, $2413$, $3142$, $3412$, $3421$, $4123$, $4312$, $4321$. Three of them, $2143$, $3412$ and $4321$, are products of two 2-cycles, and six are 4-cycles. The formula gives $24 - 24 + 12 - 4 + 1 = 9$, and the recurrence gives $3 \cdot (2 + 1) = 9$.

**Example 3 (hat check).** Ten people leave their hats and get them back in a uniformly random order. The probability that nobody gets their own hat is $D_{10}/10! = 1334961/3628800 \approx 0.3678795$, while $1/e \approx 0.3678794$. In a Secret Santa draw among 10 people, the same number is the probability that a random draw needs no redraw.

**Example 4 (exactly $k$ fixed points).** The permutations of $[n]$ with exactly $k$ fixed points number $\binom{n}{k}D_{n-k}$: choose the fixed points, then derange the rest. For $n = 5$ the counts for $k = 0, \ldots, 5$ are $44, 45, 20, 10, 0, 1$, which sum to $120 = 5!$. No permutation has exactly $n - 1$ fixed points, since $D_1 = 0$.

**Example 5 (expected fixed points).** The expected number of fixed points of a random permutation is $1$, by [linearity of expectation](/linearity-of-expectation/): each $i$ is fixed with probability $1/n$. In example 4, $(45 + 2 \cdot 20 + 3 \cdot 10 + 5)/120 = 1$.

**Non-example 1.** The identity permutation, and every permutation with a fixed point, such as $2134$ (which fixes 3 and 4), is not a derangement.

**Non-example 2.** A derangement need not be one cycle. $2143$ is a derangement made of two 2-cycles. The permutations that are one $n$-cycle are only $(n-1)!$ of the $D_n$ derangements, for example 6 of the 9 for $n = 4$.

**Non-example 3.** $n!/e$ is not $D_n$: it is not an integer. For $n = 0$ it gives $1/e$, and rounding gives $0$, while $D_0 = 1$; the nearest-integer rule needs $n \ge 1$.

## Related definitions

- **Rencontres numbers.** $D_{n,k} = \binom{n}{k}D_{n-k}$, the number of permutations with exactly $k$ fixed points, as in example 4.
- **Exponential generating function.** $\sum_{n \ge 0} D_n \frac{x^n}{n!} = \frac{e^{-x}}{1 - x}$, because a permutation is a set of fixed points together with a derangement of the rest, so $\frac{1}{1-x} = e^x \cdot \sum_n D_n x^n/n!$; see [exponential generating functions](/exponential-generating-functions/).
- **Permutations with forbidden positions.** A derangement avoids the positions on the diagonal of an $n \times n$ board. Other forbidden sets lead to rook polynomials and the ménage problem, solved by the same inclusion-exclusion.
- **Fixed-point-free involutions.** The involutions with no fixed point are the perfect matchings of $[n]$, $(n-1)(n-3)\cdots 1$ of them for even $n$; listed in [generating involutions](/generating-involutions/).
- The [factorial](/factorial/) $n!$ counts all permutations, and $D_n/n! \to 1/e$.

## References
