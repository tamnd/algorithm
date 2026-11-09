---
tag: S0ZCHV
kind: definition
slug: multinomial-coefficient
name: Multinomial coefficient
aliases:
- multinomial
- multinomial number
area: combinatorics/counting-algorithms
level: intro
summary: Ways to split n objects into labeled groups of given sizes.
prereqs: [binomial-coefficient, factorial]
see_also: [binomial-theorem, permutation, stars-and-bars, binomial-coefficient-computation, lucas-theorem, multiset-permutations]
sources:
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Chapter 1, Section 1.2, Sets and multisets (permutations of a multiset and the multinomial coefficient)
  - book: isbn:9780136020400
    title: Richard A. Brualdi, Introductory Combinatorics, fifth edition
    locator: Chapter 5, The Binomial Coefficients (Section 5.4, The multinomial theorem)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.6, Binomial Coefficients (the part on multinomial coefficients)
---

The multinomial coefficient $\binom{n}{k_1, k_2, \ldots, k_m} = \frac{n!}{k_1!\,k_2!\cdots k_m!}$, for nonnegative integers with $k_1 + \cdots + k_m = n$, is the number of ways to split $n$ distinct objects into $m$ labeled groups of sizes $k_1, \ldots, k_m$. Equivalently, it is the number of distinct arrangements of a word with $k_i$ copies of letter $i$, and the coefficient of $x_1^{k_1} \cdots x_m^{k_m}$ in $(x_1 + \cdots + x_m)^n$. With $m = 2$ it is the [binomial coefficient](/binomial-coefficient/) $\binom{n}{k_1}$.

## Definition

Notation: $[n] = \{1, \ldots, n\}$, $m \ge 1$ is the number of groups, and $k_1, \ldots, k_m$ are integers. $C(n, k)$ or $\binom{n}{k}$ is the binomial coefficient.

Let $n \ge 0$ and let $k_1, \ldots, k_m \ge 0$ be integers with $k_1 + \cdots + k_m = n$. The **multinomial coefficient** $\binom{n}{k_1, \ldots, k_m}$ is the number of sequences $(S_1, \ldots, S_m)$ of pairwise disjoint sets with $S_1 \cup \cdots \cup S_m = [n]$ and $|S_i| = k_i$ for each $i$. If some $k_i < 0$ or the sum is not $n$, the coefficient is $0$.

The groups are labeled: $(S_1, S_2)$ and $(S_2, S_1)$ are different when $S_1 \ne S_2$. A sequence $(S_1, \ldots, S_m)$ is the same as a function $f : [n] \to [m]$ with $|f^{-1}(i)| = k_i$, and the same as a word $f(1) f(2) \cdots f(n)$ over the alphabet $[m]$ with $k_i$ copies of letter $i$.

**The factorial formula.** $\binom{n}{k_1, \ldots, k_m} = \dfrac{n!}{k_1!\,k_2! \cdots k_m!}$.

*Proof.* Count the $n!$ [permutations](/permutation/) of $[n]$. Cut a permutation into consecutive blocks of lengths $k_1, \ldots, k_m$, and let $S_i$ be the set of elements in block $i$. Each split $(S_1, \ldots, S_m)$ arises from exactly $k_1! \cdots k_m!$ permutations, one for each choice of an order inside each block, by the [rule of product](/rule-of-product/). So $n! = \binom{n}{k_1, \ldots, k_m} \cdot k_1! \cdots k_m!$. $\square$

**Product of binomials.** $\binom{n}{k_1, \ldots, k_m} = \binom{n}{k_1}\binom{n - k_1}{k_2}\binom{n - k_1 - k_2}{k_3} \cdots \binom{k_m}{k_m}$.

*Proof.* Choose $S_1$ among the $n$ elements, then $S_2$ among the $n - k_1$ elements left, and so on, and apply the rule of product. $\square$

This form is the safe way to compute the value: each factor is an integer, and the product formula for each binomial avoids the large factorials; see [computing binomial coefficients](/binomial-coefficient-computation/).

**The multinomial theorem.** For elements $x_1, \ldots, x_m$ of a commutative ring and $n \ge 0$,
$$(x_1 + \cdots + x_m)^n = \sum_{\substack{k_1 + \cdots + k_m = n \\ k_i \ge 0}} \binom{n}{k_1, \ldots, k_m} x_1^{k_1} \cdots x_m^{k_m}.$$

*Proof.* Expand the product of $n$ factors by choosing one term from each factor. A choice is a word $f(1) \cdots f(n)$ over $[m]$, and it gives the monomial $x_1^{k_1} \cdots x_m^{k_m}$, where $k_i$ is the number of copies of $i$ in the word, because the $x_i$ commute. The number of words with these counts is $\binom{n}{k_1, \ldots, k_m}$. $\square$ For $m = 2$ this is the [binomial theorem](/binomial-theorem/).

**Basic facts.**

- *Symmetry.* The value does not change when the $k_i$ are permuted.
- *Recurrence.* For $n \ge 1$, $\binom{n}{k_1, \ldots, k_m} = \sum_{i=1}^{m} \binom{n-1}{k_1, \ldots, k_i - 1, \ldots, k_m}$, by the group of the element $n$. This is Pascal's rule for $m$ groups.
- *Sum.* With $x_1 = \cdots = x_m = 1$, the coefficients of size $n$ with $m$ parts sum to $m^n$, the number of functions $[n] \to [m]$.
- *Number of terms.* The number of tuples $(k_1, \ldots, k_m)$ of nonnegative integers with sum $n$ is $\binom{n + m - 1}{m - 1}$, by [stars and bars](/stars-and-bars/).

## Examples and non-examples

**Example 1 (letters of a word).** The word MISSISSIPPI has 11 letters: one M, four I, four S and two P. The number of distinct arrangements is
$$\binom{11}{1, 4, 4, 2} = \frac{11!}{1!\,4!\,4!\,2!} = 34650,$$
and the product of binomials gives the same value: $\binom{11}{1}\binom{10}{4}\binom{6}{4}\binom{2}{2} = 11 \cdot 210 \cdot 15 \cdot 1 = 34650$.

**Example 2 (expansion).** $(x + y + z)^3$ has $\binom{5}{2} = 10$ terms:
$$x^3 + y^3 + z^3 + 3(x^2 y + x^2 z + x y^2 + y^2 z + x z^2 + y z^2) + 6xyz.$$
The coefficient of $xyz$ is $\binom{3}{1,1,1} = 3! = 6$, and the coefficients sum to $3^3 = 27$.

**Example 3 (card deals).** A bridge deal gives 13 cards to each of four labeled players North, East, South and West. The number of deals is $\binom{52}{13, 13, 13, 13} = 52!/(13!)^4 = 53644737765488792839237440000$, a number of 96 bits.

**Example 4 (all distinct).** With all $k_i = 1$ and $m = n$, the coefficient is $n!$, the number of permutations: each group holds one element, and the order of the labeled groups is the permutation.

**Example 5 (parity).** A multinomial coefficient is odd exactly when the binary forms of $k_1, \ldots, k_m$ have no 1 bit in common, by the generalization of [Lucas's theorem](/lucas-theorem/) with $p = 2$ (equivalently, adding the $k_i$ in base 2 gives no carry). For example $\binom{7}{1, 2, 4} = 105$ is odd, since $1$, $2$ and $4$ use different bits, and $\binom{10}{3, 3, 4} = 4200$ is even, since $3 = 011_2$ appears twice.

**Non-example 1 (unlabeled groups).** The number of ways to split 4 people into two pairs is not $\binom{4}{2,2} = 6$ but 3. The multinomial coefficient counts ordered pairs (first pair, second pair), and each split into two unlabeled pairs appears twice. In general, when $j$ groups of the same size are unlabeled, divide by $j!$.

**Non-example 2 (identical objects).** The number of ways to put $n$ identical balls into $m$ labeled boxes is not a multinomial coefficient but $\binom{n + m - 1}{m - 1}$, the number of tuples $(k_1, \ldots, k_m)$; see [stars and bars](/stars-and-bars/). The multinomial coefficient counts the ways for distinct balls with fixed box sizes.

**Non-example 3 (sizes that do not add up).** $\binom{5}{2, 2}$ is not defined by the formula $5!/(2!\,2!) = 30$: the sizes sum to 4, not 5, so no split exists, and the coefficient is $0$ under the definition above.

## Related definitions

- The [binomial coefficient](/binomial-coefficient/) is the case $m = 2$: $\binom{n}{k, n-k} = \binom{n}{k}$.
- The [factorial](/factorial/) $n!$ is the case where all $k_i = 1$, and the number of [permutations](/permutation/) of a multiset with multiplicities $k_1, \ldots, k_m$ is the multinomial coefficient. [Multiset permutations](/multiset-permutations/) lists these arrangements, and the area [generating permutations](/generating-permutations/) has related algorithms.
- The multinomial distribution gives the probability $\binom{n}{k_1, \ldots, k_m} p_1^{k_1} \cdots p_m^{k_m}$ of the counts $k_i$ in $n$ independent trials with $m$ outcomes.
- The [Stirling numbers of the second kind](/stirling-numbers-second-kind/) count splits into unlabeled nonempty groups of any sizes; $m!\,S(n, m)$ is the sum of $\binom{n}{k_1, \ldots, k_m}$ over all tuples with every $k_i \ge 1$.
- [Exponential generating functions](/exponential-generating-functions/) multiply as $\frac{x^{k_1}}{k_1!} \cdots \frac{x^{k_m}}{k_m!} = \binom{n}{k_1, \ldots, k_m}\frac{x^n}{n!}$, which is why they count labeled structures.

## References
