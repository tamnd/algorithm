---
tag: Q0TYY4
kind: problem
slug: counting-integer-compositions
name: Counting integer compositions
aliases:
- ordered partitions of an integer
- counting compositions
- counting ordered sums
area: combinatorics/counting-algorithms
level: intro
summary: Counting ways to write n as an ordered sum of positive integers.
prereqs: [binomial-coefficient, stars-and-bars]
see_also: [integer-compositions, composition-generation, stars-and-bars, integer-partition-counting, coin-change-counting, fibonacci-numbers, linear-recurrence-nth-term, transfer-matrix-method]
sources:
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Chapter 1, Section 1.2, How to count (compositions, compositions with k parts and weak compositions)
  - book: isbn:9780521637664
    title: George E. Andrews, The Theory of Partitions, Cambridge University Press, 1998 (first published 1976)
    locator: Chapter 4, Compositions and Simon Newcomb's problem
  - book: isbn:9780521898065
    title: Philippe Flajolet and Robert Sedgewick, Analytic Combinatorics, Cambridge University Press, 2009
    locator: Chapter I, Section I.3, Integer compositions and partitions
---

Counting integer compositions asks for the number of ways to write $n$ as an ordered sum of positive integers, such as $1 + 3$ and $3 + 1$, which count as different. Without restrictions the answer is $2^{n-1}$, and with exactly $k$ parts it is the [binomial coefficient](/binomial-coefficient/) $C(n-1, k-1)$. When the parts must come from a set $S$, the count satisfies a linear recurrence, which gives an $O(n |S|)$ table and, for a finite $S$, a logarithmic-time matrix method. Many puzzles about stairs, tilings and codes are this problem in disguise.

## In plain words

You climb a staircase of a given height and may take steps of different sizes. A climb is the list of step sizes in the order you take them. The task is to count all the different climbs. If every step size is allowed, each gap between two stairs is either a stop or not, so the count doubles with each new stair. If only some step sizes are allowed, for example 1 and 2, the count follows a rule that adds a few earlier counts, here the Fibonacci rule.

## Definition

**Notation.** $n \ge 0$ and $k \ge 0$ are integers. $C(n, k)$ is a binomial coefficient. $S$ is a set of positive integers, the allowed parts.

A *composition* of $n$ with $k$ parts is a sequence $(a_1, \ldots, a_k)$ of positive integers with $a_1 + \cdots + a_k = n$. The empty sequence is the one composition of $0$.

**Input:** $n$, and in the variants $k$, the set $S$, or a modulus.

**Output:** the number $c(n)$ of compositions of $n$, or the number $c(n, k)$ with $k$ parts, or the number $c_S(n)$ with all parts in $S$.

**Theorem.** For $n \ge 1$, $c(n) = 2^{n-1}$ and $c(n, k) = C(n - 1, k - 1)$.

*Proof.* Write $n$ as a row of $n$ units with $n - 1$ gaps between them. A composition is fixed by the set of gaps where one part ends and the next starts: the partial sums $a_1, a_1 + a_2, \ldots, a_1 + \cdots + a_{k-1}$ form a subset of $\{1, \ldots, n-1\}$ of size $k - 1$, and each such subset comes from exactly one composition. So $c(n, k) = C(n-1, k-1)$, and summing over $k$ gives $2^{n-1}$. $\square$

**Theorem (allowed parts).** For any set $S$ of positive integers, $c_S(0) = 1$ and, for $n \ge 1$,

$$c_S(n) = \sum_{s \in S,\ s \le n} c_S(n - s), \qquad \sum_{n \ge 0} c_S(n)\, z^n = \frac{1}{1 - \sum_{s \in S} z^s}.$$

*Proof.* Split the compositions of $n \ge 1$ by the last part $s$. Removing it leaves a composition of $n - s$ with parts in $S$, and each one arises once. The [generating function](/generating-functions/) form is the same statement: a composition is a sequence of parts, and the sequence construction turns the series $\sum_{s \in S} z^s$ of one part into $1/(1 - \sum_{s \in S} z^s)$. $\square$

## Variants

- **Fixed number of parts.** $c(n, k) = C(n-1, k-1)$, by the first theorem.
- **Weak compositions.** If parts may be $0$, the number of sequences of $k$ non-negative integers with sum $n$ is $C(n + k - 1, k - 1)$. Add 1 to each part to get a composition of $n + k$ with $k$ parts. This is [stars and bars](/stars-and-bars/).
- **Allowed parts.** Parts from a set $S$: the recurrence above. Parts $\{1, 2\}$ give the Fibonacci numbers, $c_S(n) = F_{n+1}$. Odd parts give $F_n$ for $n \ge 1$. Parts at least 2 give $F_{n-1}$ for $n \ge 1$. Parts $\{1, 2, 3\}$ give the tribonacci numbers $1, 1, 2, 4, 7, 13, 24, 44, 81, 149, 274, 504, 927$ (OEIS A000073, shifted by 2).
- **Bounded parts and a fixed number of parts.** Compositions of $n$ into $k$ parts, each in $[1, m]$, number $\sum_j (-1)^j C(k, j)\, C(n - jm - 1, k - 1)$, by [inclusion-exclusion](/inclusion-exclusion-principle/) over the parts that exceed $m$.
- **Residues.** Any of these modulo a prime, for very large $n$.
- **Unordered.** If the order of the parts does not matter, the problem becomes [counting integer partitions](/integer-partition-counting/) or, with parts from $S$, [coin change counting](/coin-change-counting/).

## Examples

**Example 1.** The $2^3 = 8$ compositions of $4$ are $4$, $3 + 1$, $1 + 3$, $2 + 2$, $2 + 1 + 1$, $1 + 2 + 1$, $1 + 1 + 2$ and $1 + 1 + 1 + 1$. By number of parts, $1 + 3 + 3 + 1$, the row $C(3, k - 1)$.

**Example 2: stairs.** A staircase of 10 steps climbed 1 or 2 steps at a time has $c_{\{1, 2\}}(10) = F_{11} = 89$ climbs. The counts for $n = 0$ to $10$ are $1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89$ (OEIS A000045).

**Example 3: fixed number of parts.** There are $C(9, 2) = 36$ ways to write $10$ as an ordered sum of 3 positive parts, and $C(12, 2) = 66$ ways with 3 non-negative parts.

**Example 4: tilings.** The tilings of a $1 \times n$ strip with tiles of lengths in $S$ are the compositions of $n$ with parts in $S$, read from left to right. With tiles of length 1, 2 and 3, a strip of length 12 has $927$ tilings.

## Known algorithms

**Closed forms.** $2^{n-1}$ and $C(n-1, k-1)$ give the unrestricted counts directly. Exactly, $2^{n-1}$ is a shift with $n$ bits of output, and $C(n-1, k-1)$ costs $O(k)$ multiplications and divisions of numbers with $O(k \log n)$ bits.

**Table.** For a set $S$, fill $c_S(0), \ldots, c_S(n)$ by the recurrence in $O(n |S|)$ additions, a [tabulation](/tabulation/) over the last part. The values grow at most like $2^{n}$, so they have $O(n)$ bits and the exact bit cost is $O(n^2 |S|)$. Modulo a prime the cost is $O(n |S|)$ word operations.

**Matrix power and linear recurrences.** If $S$ is finite with largest element $d$, the recurrence has order $d$. The companion matrix $T$ of size $d \times d$ gives $c_S(n)$ from $T^n$ with [matrix exponentiation](/matrix-exponentiation/) in $O(d^3 \log n)$ operations, or with polynomial arithmetic modulo the characteristic polynomial in $O(d^2 \log n)$, as in the [n-th term of a linear recurrence](/linear-recurrence-nth-term/). This is the method for $n$ up to $10^{18}$ modulo a prime. It is the [transfer-matrix method](/transfer-matrix-method/) on a path of $d$ states.

**Power series.** For a long prefix modulo a suitable prime, invert $1 - \sum_{s \in S} z^s$ with [power series inversion](/power-series-inversion/) in $O(n \log n)$ operations, when $S$ is large.

**Listing.** [Composition generation](/composition-generation/) lists them one at a time, which takes time at least the count. Use it only to test.

## Bounds

- **Size.** $c(n) = 2^{n-1}$ has exactly $n$ bits. For a finite $S$ with $\gcd(S) = 1$, $c_S(n) = \Theta(\rho^{-n})$, where $\rho$ is the unique positive root of $\sum_{s \in S} z^s = 1$. For $S = \{1, 2\}$, $\rho^{-1}$ is the golden ratio $1.618\ldots$.
- **Time.** For fixed finite $S$ modulo a prime, $O(\log n)$ operations suffice, by the matrix method. In exact arithmetic the output has $\Theta(n)$ bits, so $\Omega(n)$ bit operations are needed.

## Reductions

- Compositions of $n$ correspond one to one to subsets of $\{1, \ldots, n-1\}$, by partial sums, and to binary strings of length $n - 1$ (a 1 marks the end of a part).
- Compositions of $n$ with parts in $S$ correspond to the paths from $0$ to $n$ in the graph on $\{0, \ldots, n\}$ with an edge $i \to i + s$ for each $s \in S$, so counting them is counting paths in a DAG.
- Weak compositions of $n$ into $k$ parts correspond to multisets of size $n$ from $k$ kinds of items.
- Compositions with parts in $S$ are the words over an alphabet of letters with lengths in $S$, so they count the strings of total length $n$ in a variable-length code.

## Applications

- **Stairs and tilings.** Puzzles that count climbs or tilings of a strip with pieces of given lengths are compositions with allowed parts.
- **Codes and channels.** Shannon counted the messages of total duration $n$ over symbols of given durations in this way, and the growth rate $\rho^{-1}$ gives the capacity of the channel.
- **Dynamic programming.** The recurrence over the last part is the pattern behind many DP problems that count ordered choices, such as decoding a digit string into letters.
- **Probability.** The number of ways to reach a total of $n$ with ordered dice rolls is a count of compositions with parts in $\{1, \ldots, 6\}$.

## References
