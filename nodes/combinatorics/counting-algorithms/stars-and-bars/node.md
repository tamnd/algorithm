---
tag: 915W1R
kind: technique
slug: stars-and-bars
name: Stars and bars
aliases:
- balls into bins with identical balls
- sticks and stones
- balls and urns
area: combinatorics/counting-algorithms
level: intro
summary: Counts distributions of identical items into distinct bins.
prereqs: [binomial-coefficient, bijective-proof]
see_also: [combinations-with-repetition, bounded-integer-solutions-counting, counting-integer-compositions, multinomial-coefficient, inclusion-exclusion-principle, hockey-stick-identity, generating-functions, counting-lattice-paths]
sources:
  - book: isbn:9780471257080
    title: William Feller, An Introduction to Probability Theory and Its Applications, Volume 1, third edition
    locator: Chapter II, Section 5, Application to occupancy problems (the representation by stars and bars, and Bose-Einstein statistics)
  - book: isbn:9780136020400
    title: Richard A. Brualdi, Introductory Combinatorics, fifth edition
    locator: Chapter 2, Permutations and Combinations (Section 2.5, Combinations of multisets)
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Chapter 1, Section 1.2, Sets and multisets (the number of multisets and of compositions)
---

Stars and bars counts the ways to put $n$ identical items into $k$ distinct bins. Write the items as $n$ stars in a row and separate the bins by $k - 1$ bars; each distribution is one arrangement of these $n + k - 1$ symbols, so there are $\binom{n + k - 1}{k - 1}$ of them. The same count gives the number of solutions of $x_1 + \cdots + x_k = n$ in nonnegative integers, the number of multisets of size $n$ from $k$ kinds, and the number of monomials of degree $n$ in $k$ variables. Lower bounds on the $x_i$ are handled by a shift, and upper bounds by [inclusion-exclusion](/inclusion-exclusion-principle/).

## In plain words

You have ten identical candies and four children, and you want to know how many ways there are to share them. Put the candies in a row and draw three dividing lines among them. The candies before the first line go to the first child, the candies between the first and second lines go to the second child, and so on. Every way of sharing gives exactly one picture of candies and lines, and every picture gives one way of sharing.

So the count is the number of ways to choose which places in the row hold the lines. This changes a question about sharing into a question about choosing places, which has a known answer.

## When it applies

- The objects are tuples $(x_1, \ldots, x_k)$ of integers with a fixed sum $n$ and simple lower bounds, such as $x_i \ge 0$ or $x_i \ge 1$.
- The items are identical and the bins are distinct (labeled). If the items are distinct, the count is $k^n$ by the [rule of product](/rule-of-product/). If the bins are identical too, the count is a number of integer partitions, not a binomial coefficient.
- The objects are multisets, sorted sequences $a_1 \le \cdots \le a_n$ with values in $[k]$, or monomials: a multiset is determined by the number $x_i$ of copies of each kind $i$.
- The constraint is an inequality $x_1 + \cdots + x_k \le n$: add a slack variable $x_{k+1} = n - (x_1 + \cdots + x_k) \ge 0$.

It does not apply alone when the $x_i$ have upper bounds; see [bounded integer solutions](/bounded-integer-solutions-counting/).

## The template

Notation: $n \ge 0$ is the number of identical items (the required sum), $k \ge 1$ is the number of bins (the number of variables), $[k] = \{1, \ldots, k\}$, and $\binom{a}{b}$ or $C(a, b)$ is the [binomial coefficient](/binomial-coefficient/), $0$ when $b < 0$ or $b > a$. Answers are exact integers, or residues modulo a prime when they are large; the cost is that of one [binomial coefficient](/binomial-coefficient-computation/).

**Theorem (stars and bars).** Let $n \ge 0$ and $k \ge 1$ be integers.

1. The number of $(x_1, \ldots, x_k) \in \mathbb{Z}_{\ge 0}^k$ with $x_1 + \cdots + x_k = n$ is $\binom{n + k - 1}{k - 1}$.
2. The number of $(x_1, \ldots, x_k) \in \mathbb{Z}_{\ge 1}^k$ with $x_1 + \cdots + x_k = n$ is $\binom{n - 1}{k - 1}$ for $n \ge 1$, and $0$ for $n = 0$.

*Proof of 1.* A word of length $n + k - 1$ over $\{\star, |\}$ with exactly $k - 1$ bars is determined by the set of positions of its bars, so there are $\binom{n+k-1}{k-1}$ such words. Map a solution $(x_1, \ldots, x_k)$ to the word $\star^{x_1} | \star^{x_2} | \cdots | \star^{x_k}$, which has $n$ stars and $k - 1$ bars. Map a word back to the tuple of the numbers of stars before the first bar, between consecutive bars, and after the last bar. These numbers are nonnegative and sum to $n$, and the two maps are inverse, so by the [bijective proof](/bijective-proof/) lemma the sets have the same size. $\square$

*Proof of 2.* For $n \ge 1$, put $n$ stars in a row; there are $n - 1$ gaps between neighbors. A solution in positive integers corresponds to the choice of $k - 1$ of these gaps for the bars, at most one bar per gap, by the same pair of maps; so there are $\binom{n-1}{k-1}$ solutions. Equivalently, substitute $y_i = x_i - 1 \ge 0$ with $\sum y_i = n - k$ and apply part 1: $\binom{n - k + k - 1}{k - 1} = \binom{n-1}{k-1}$. For $n = 0$ and $k \ge 1$ there is no positive solution. $\square$

The template reduces a problem to part 1 in steps; the holes are the encoding and the bounds.

```pseudo id=main
STARS-AND-BARS(S)
L1  encode each object of S as a tuple (x_1, ..., x_k) of integers  ▷ hole: the encoding
L2  check: the encoding is a bijection onto {x : Σ x_i = n, x_i ≥ l_i}  ▷ hole: n, k and the bounds l_i
L3  if the constraint is "≤ n" then add x_(k+1) ≥ 0 and set k ← k + 1
L4  n' ← n − (l_1 + ... + l_k)                                        ▷ shift: y_i = x_i − l_i ≥ 0
L5  if n' < 0 then return 0
L6  return C(n' + k − 1, k − 1)
```

Line L2 is the step that fails most often: the encoding must cover each object once. Lines L3 and L4 are bijections between solution sets (adding a slack variable, and a translation), so they keep the count.

## Classic examples

**1. Candies.** Ten identical candies for four children: $\binom{10 + 3}{3} = \binom{13}{3} = 286$ ways. If each child gets at least one: $\binom{9}{3} = 84$ ways.

**2. Lower bounds.** The solutions of $x_1 + x_2 + x_3 = 10$ with $x_1 \ge 2$, $x_2 \ge 1$, $x_3 \ge 0$: line L4 gives $n' = 7$, and the count is $\binom{7 + 2}{2} = 36$.

**3. An inequality.** The nonnegative solutions of $x_1 + x_2 + x_3 + x_4 \le 5$: with a slack variable, $k = 5$ and the count is $\binom{5 + 4}{4} = 126$.

**4. Dice.** Three identical dice show a multiset of size 3 from 6 values, so there are $\binom{3 + 5}{5} = 56$ distinguishable outcomes. They are not equally likely: the 216 ordered outcomes are, which is why the multiset count is not a probability space for fair dice. Physicists call the uniform model on multisets Bose-Einstein statistics (Feller, Chapter II, Section 5).

**5. Monomials.** The monomials of degree $n$ in $k$ variables are $x_1^{a_1} \cdots x_k^{a_k}$ with $\sum a_i = n$, so there are $\binom{n + k - 1}{k - 1}$; for $n = 3$ and $k = 3$ there are $\binom{5}{2} = 10$, the terms of $(x + y + z)^3$ on the page [multinomial coefficient](/multinomial-coefficient/). The polynomials of degree at most $n$ in $k$ variables have $\binom{n + k}{k}$ coefficients, by example 3's slack variable.

**6. Sorted sequences and multisets.** A non-decreasing sequence $1 \le a_1 \le \cdots \le a_n \le k$ is determined by the numbers $x_i$ of entries equal to $i$, so there are $\binom{n + k - 1}{n}$ of them. These are the [combinations with repetition](/combinations-with-repetition/), and nested loops `for i1 ≤ i2 ≤ ... ≤ in` over $[k]$ run that many times.

**7. Compositions.** An ordered sum $n = c_1 + \cdots + c_k$ of positive parts is a solution of part 2, so $n$ has $\binom{n-1}{k-1}$ compositions into $k$ parts and $\sum_k \binom{n-1}{k-1} = 2^{n-1}$ compositions in all; see [counting integer compositions](/counting-integer-compositions/).

## Variations

- **Upper bounds.** With $0 \le x_i \le u_i$, count the solutions that break a set $J$ of bounds, which is a stars and bars count after the shift $x_i \ge u_i + 1$ for $i \in J$, and combine with inclusion-exclusion: $\sum_{J \subseteq [k]} (-1)^{|J|} \binom{n - \sum_{i \in J}(u_i + 1) + k - 1}{k - 1}$. See [bounded integer solutions](/bounded-integer-solutions-counting/).
- **Generating functions.** The count of part 1 is the coefficient of $z^n$ in $(1 + z + z^2 + \cdots)^k = (1 - z)^{-k}$, whose coefficients are $\binom{n + k - 1}{k - 1}$ by the general [binomial theorem](/binomial-theorem/). Other constraints on each $x_i$ (even, at most 3, from a set) change one factor; see [generating functions](/generating-functions/).
- **Lattice paths.** A word of stars and bars is a monotone [lattice path](/counting-lattice-paths/) with $n$ right steps and $k - 1$ up steps, and $x_i$ is the length of the $i$-th horizontal run.
- **The recurrence.** Splitting by the value of $x_k$ gives $\binom{n+k-1}{k-1} = \sum_{j=0}^{n} \binom{j + k - 2}{k - 2}$, the [hockey-stick identity](/hockey-stick-identity/), and a DP over the bins that also works when each $x_i$ has its own allowed set.
- **Distinct items.** With distinct items and labeled bins, the count is $k^n$; with bin sizes fixed, it is the [multinomial coefficient](/multinomial-coefficient/); with nonempty unlabeled bins, the [Stirling numbers of the second kind](/stirling-numbers-second-kind/).

## Pitfalls

- **Identical or distinct.** Stars and bars counts identical items. Ten distinct candies for four children give $4^{10} = 1048576$ ways, not 286.
- **Labeled bins.** If the bins are identical, $(3, 1)$ and $(1, 3)$ are the same distribution, and stars and bars overcounts. Unlabeled bins lead to integer partitions.
- **Empty bins.** Part 1 allows empty bins and part 2 does not. Mixing them up changes $\binom{13}{3} = 286$ into $\binom{9}{3} = 84$.
- **Off by one.** The bars are $k - 1$, not $k$: the answer is $\binom{n + k - 1}{k - 1}$, equivalently $\binom{n + k - 1}{n}$, and not $\binom{n + k}{k}$, which is the count for "$\le n$".
- **No bins.** With $k = 0$ there is one solution (the empty tuple) if $n = 0$ and none otherwise; the formula $\binom{n - 1}{-1} = 0$ is wrong for $n = 0$. Treat $k = 0$ apart.
- **Negative shifted sum.** If the lower bounds sum to more than $n$, line L5 must return 0; a library function for $\binom{a}{b}$ with $a < 0$ can return a nonzero generalized value.

## Exercises

1. How many solutions does $x_1 + x_2 + x_3 + x_4 = 20$ have with every $x_i$ odd and positive? (Write $x_i = 2y_i + 1$.)
2. Show that the number of multisets of size $n$ from $[k]$ equals the number of $n$-subsets of $[n + k - 1]$ by the map $a_i \mapsto a_i + i - 1$, and compare with the proof of part 1.
3. In how many ways can 12 identical balls go into 5 distinct boxes so that box 1 gets at most 3 balls? Use one complement.

## References
