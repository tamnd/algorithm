---
tag: A23CGW
kind: definition
slug: monotone-predicate
name: Monotone predicate
aliases:
- monotone feasibility predicate
- monotone decision predicate
area: searching/search-on-answers
level: intro
summary: A yes/no property that flips from false to true exactly once over an ordered domain, which makes binary search valid.
prereqs: [binary-search]
see_also: [lower-and-upper-bound-search, binary-search-on-answer, binary-search-on-real-numbers, optimization-to-decision-reduction, unimodal-function, lower-bound-query, decision-problem]
sources:
  - book: isbn:9783319725468
    title: Antti Laaksonen, Guide to Competitive Programming, first edition, Springer, 2017
    locator: Section 4.3.2, Finding Optimal Solutions
  - url: https://cp-algorithms.com/num_methods/binary_search.html
    title: cp-algorithms, Binary search
    note: the sections Search on arbitrary predicate and Binary search on the answer
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.1, Searching an ordered table
---

A monotone predicate is a test $P$ on a totally ordered set that, once it is true, stays true for every larger element. Its true elements form one final segment of the order, so the whole predicate is described by one *threshold*, the first element where it is true. This is the exact condition under which [binary search](/binary-search/) can find that threshold: the [lower bound search](/lower-and-upper-bound-search/) of a sorted array, [binary search on the answer](/binary-search-on-answer/) and [bisection](/binary-search-on-real-numbers/) all assume it and nothing more.

## Definition

Let $(D, \le)$ be a totally ordered set and let $P : D \to \{\text{false}, \text{true}\}$. The predicate $P$ is **monotone** (false then true) if

$$\forall x, y \in D:\quad x \le y \ \text{and}\ P(x) \implies P(y).$$

Equivalently, the set $T = \{x \in D : P(x)\}$ is an *up-set*: with each element it holds every larger element. The predicate is **antitone** (true then false) if $x \le y$ and $P(y)$ imply $P(x)$, that is, if $\neg P$ is monotone. Every statement below for monotone predicates holds for antitone ones after the order is reversed.

**Threshold form on a finite domain.** Let $D = \{d_0 < d_1 < \cdots < d_{n-1}\}$ with $n \ge 0$. Then $P$ is monotone if and only if there is an integer $k$ with $0 \le k \le n$ such that

$$P(d_i) \iff i \ge k \qquad \text{for all } 0 \le i < n.$$

*Proof.* If such a $k$ exists and $d_i \le d_j$ with $P(d_i)$, then $i \le j$ and $i \ge k$, so $j \ge k$ and $P(d_j)$. For the converse, let $P$ be monotone. If $T$ is empty, take $k = n$. Else let $k$ be the smallest index with $P(d_k)$. For $i < k$, $P(d_i)$ is false by the choice of $k$. For $i \ge k$, $d_k \le d_i$ and $P(d_k)$, so $P(d_i)$ by monotonicity. $\square$

The value $k$ is the **threshold** (or boundary) of $P$. The case $k = n$ means that $P$ is never true; the case $k = 0$ means that it is always true. So a monotone predicate on $n$ elements has exactly $n + 1$ possible shapes.

**Threshold form on an interval.** Let $D = [a, b]$ be a real interval with $a < b$ and let $P$ be monotone on it. If $T$ is not empty, let $c = \inf T$. Then $T$ is $[c, b]$ or $(c, b]$. *Proof.* For $x > c$, there is $t \in T$ with $t < x$ by the definition of the infimum, so $x \in T$. For $x < c$, $x \notin T$ since $c$ is a lower bound of $T$. So $T$ holds $(c, b]$, misses $[a, c)$, and may or may not hold $c$. $\square$ Whether $c \in T$ depends on $P$: it holds for $P(x) = (x \ge c)$ and fails for $P(x) = (x > c)$. A bisection finds $c$ only up to a tolerance, and it does not tell the two cases apart.

**What binary search needs.** Binary search on $[lo, hi)$ evaluates $P$ at a middle point $m$ and keeps $[lo, m]$ when $P(m)$ is true and $[m + 1, hi)$ when it is false. The threshold form shows that this is safe: a true value at $m$ means $k \le m$, and a false value means $k > m$. So, with the invariant "$k$ lies in $[lo, hi]$", the search returns $k$ after at most $\lceil \lg(n + 1) \rceil$ evaluations of $P$. No method that only evaluates $P$ can do better in the worst case: there are $n + 1$ possible thresholds, each evaluation has two outcomes, so a decision tree that tells them apart has depth at least $\lceil \lg(n+1) \rceil$.

**Building monotone predicates.** These rules follow at once from the definition.

- If $g : D \to \mathbb{R}$ is non-decreasing and $c$ is a constant, then $P(x) = (g(x) \ge c)$ and $P(x) = (g(x) > c)$ are monotone. If $g$ is non-increasing, then $P(x) = (g(x) \le c)$ is monotone.
- If $P$ and $Q$ are monotone, then $P \wedge Q$ and $P \vee Q$ are monotone. The negation $\neg P$ is antitone.
- If $P$ is monotone on $E$ and $f : D \to E$ is non-decreasing, then $P \circ f$ is monotone on $D$.

## Examples and non-examples

**Sorted array.** For a sorted array $A[0 \ldots n-1]$ and a key $x$, the test $P(i) = (A[i] \ge x)$ is monotone on the indices, by the first rule with $g(i) = A[i]$. Its threshold is the answer of the [lower bound query](/lower-bound-query/). The test $A[i] = x$ is not monotone: it is false, then true on a block, then false.

**Capacity of a ship.** Packages of weights $1, 2, \ldots, 10$ go out in this order, and a day's load may not exceed the capacity $c$. Let $\mathrm{days}(c)$ be the number of days that the greedy loading needs (fill each day until the next package does not fit). A larger capacity never needs more days, so $\mathrm{days}$ is non-increasing and $P(c) = (\mathrm{days}(c) \le 5)$ is monotone in $c$. The values are $\mathrm{days}(10) = 7$, $\mathrm{days}(11) = \cdots = \mathrm{days}(14) = 6$ and $\mathrm{days}(15) = \mathrm{days}(16) = 5$, so the threshold is $c = 15$. A binary search on $[10, 56)$ tests $c = 33, 21, 15, 12, 14$ and returns 15.

**Feasibility of a deadline.** "All jobs can be done by time $t$" is monotone in $t$ for any schedule model in which a schedule that ends by $t$ also ends by each $t' > t$. This is the form that [binary search on the answer](/binary-search-on-answer/) uses.

**Non-example: a square.** On the integers $-5, -4, \ldots, 5$, the test $P(x) = (x^2 \ge 4)$ is true at $-5$, false at $0$ and true at $5$, so it is not monotone. A first-true binary search on $[-5, 6)$ tests $0$ (false), $3$ (true), $2$ (true) and $1$ (false), and returns $2$. The first true element is $-5$. The search is wrong because it assumed that a false value at $0$ means that all smaller elements are false.

**Non-example: primality.** "$x$ is prime" on the positive integers is true at 2 and false at 4, so it is not monotone. No threshold exists.

**Non-example: a test that changes direction.** On the integers $0$ to $10$, the test "$|x - 4| \le 2$" is false, then true on $2$ to $6$, then false again. Its true set is an interval but not a final segment, so it is neither monotone nor antitone. It is the conjunction of the monotone test $x \ge 2$ and the antitone test $x \le 6$; each of the two bounds can be found by its own binary search.

## Related definitions

- **Threshold.** The first true element $k$ of the finite form. The search problem "find $k$" is the general form of the [lower bound query](/lower-bound-query/).
- **Monotone function.** A map $g$ between ordered sets with $x \le y \Rightarrow g(x) \le g(y)$. A monotone predicate is a monotone function into $\{\text{false} < \text{true}\}$.
- **Monotone Boolean function.** A different use of the word: a function on $\{0, 1\}^n$ that is monotone for the componentwise order. That order is not total, and a monotone Boolean function in general has no single threshold.
- **[Unimodal function](/unimodal-function/).** A function that rises and then falls. When $f$ strictly increases and then strictly decreases on the integers, the predicate "$f(x) < f(x + 1)$" is antitone, which reduces the search for the maximum to a threshold search.
- **Decision version.** The predicate "the optimum is at most $t$" of an optimization problem. It is monotone in $t$, which is the basis of the [optimization-to-decision reduction](/optimization-to-decision-reduction/) and of the [decision problem](/decision-problem/) view of optimization.

## References
