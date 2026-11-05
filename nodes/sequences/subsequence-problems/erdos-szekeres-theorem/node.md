---
tag: WGAGCG
kind: theorem
slug: erdos-szekeres-theorem
name: Erdős-Szekeres theorem
aliases:
- monotone subsequence theorem
area: sequences/subsequence-problems
level: intro
summary: Every sequence of n·m + 1 distinct numbers has an increasing subsequence of length n+1 or a decreasing one of length m+1.
prereqs: [longest-increasing-subsequence, pigeonhole-principle]
see_also: [dilworth-theorem, patience-sorting, young-tableau, ramsey-theorem, counting-standard-young-tableaux, subsequence]
sources:
  - paper: "Paul Erdős and George Szekeres, A combinatorial problem in geometry, Compositio Mathematica 2, 1935, 463-470"
    locator: the lemma on monotone subsequences, used for points in convex position
  - paper: "A. Seidenberg, A simple proof of a theorem of Erdős and Szekeres, Journal of the London Mathematical Society 34, 1959, 352"
    locator: the proof by labels (the lengths of the longest increasing and decreasing subsequences that end at each position) and the pigeonhole principle
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.1.4, Tableaux and involutions (Schensted's theorem and its consequence for monotone subsequences)
  - paper: "C. Schensted, Longest increasing and decreasing subsequences, Canadian Journal of Mathematics 13, 1961, 179-191"
    locator: the main theorem (rows and columns of the insertion tableau)
---

The Erdős-Szekeres theorem says that each sequence of $nm + 1$ distinct real numbers has an increasing [subsequence](/subsequence/) of length $n + 1$ or a decreasing subsequence of length $m + 1$, and that $nm + 1$ cannot be lowered. So each sequence of $N$ distinct numbers has a monotone subsequence of length at least $\lceil \sqrt{N} \rceil$. Erdős and Szekeres proved it in 1935 as a step in a problem about points in convex position, and Seidenberg's 1959 proof by the [pigeonhole principle](/pigeonhole-principle/) is now the standard one. It is a lower bound on the answer of the [longest increasing subsequence](/longest-increasing-subsequence/) problem and its mirror.

## Statement

**Theorem.** Let $n, m \ge 0$ be integers, and let $a_1, \ldots, a_N$ be distinct real numbers with $N \ge nm + 1$. Then there are indices $i_1 < \cdots < i_{n+1}$ with $a_{i_1} < \cdots < a_{i_{n+1}}$, or indices $j_1 < \cdots < j_{m+1}$ with $a_{j_1} > \cdots > a_{j_{m+1}}$.

**Product form.** For each sequence $A$ of $N$ distinct numbers, with $L_{\uparrow}(A)$ and $L_{\downarrow}(A)$ the lengths of its longest increasing and longest decreasing subsequences,

$$L_{\uparrow}(A) \cdot L_{\downarrow}(A) \ge N.$$

**Tightness.** For all $n, m \ge 1$ there is a sequence of $nm$ distinct numbers with no increasing subsequence of length $n + 1$ and no decreasing subsequence of length $m + 1$.

## In plain words

Write down a list of different numbers in any order. If the list is long enough, you can always cross out numbers so that the rest goes up, or so that the rest goes down, and the rest is long. For example, any ten different numbers contain four that go up or four that go down.

The proof gives each number two labels: how long a rising run you can end at it, and how long a falling run you can end at it. Two different numbers never get the same two labels. If no run is long, there are only a few possible label pairs, and too many numbers must share them, which is not possible.

## Proof

**Labels.** For each position $i$, let $u_i$ be the length of a longest increasing subsequence that ends at $a_i$, and $d_i$ the length of a longest decreasing subsequence that ends at $a_i$. Both are at least 1.

**Claim.** If $i < j$, then $(u_i, d_i) \ne (u_j, d_j)$.

*Proof of the claim.* The numbers are distinct, so $a_i < a_j$ or $a_i > a_j$. If $a_i < a_j$, add $a_j$ to the end of a longest increasing subsequence that ends at $a_i$. This gives an increasing subsequence of length $u_i + 1$ that ends at $a_j$, so $u_j \ge u_i + 1 > u_i$. If $a_i > a_j$, the same argument with a decreasing subsequence gives $d_j > d_i$. In both cases the pairs differ.

**Theorem.** Suppose that no increasing subsequence has length $n + 1$ and no decreasing subsequence has length $m + 1$. Then $1 \le u_i \le n$ and $1 \le d_i \le m$ for each $i$, so the pairs $(u_i, d_i)$ take at most $nm$ values. By the claim the $N$ pairs are distinct, so $N \le nm$. This contradicts $N \ge nm + 1$. (If $n = 0$ or $m = 0$, the statement holds at once, since $N \ge 1$ gives an increasing and a decreasing subsequence of length 1.)

**Product form.** Take $n = L_{\uparrow}(A)$ and $m = L_{\downarrow}(A)$. Then $u_i \le n$ and $d_i \le m$ for each $i$, and the claim gives $N$ distinct pairs in a set of size $nm$, so $N \le nm$.

**Tightness.** Let $B_k$, for $k = 1, \ldots, n$, be the decreasing block $km, km - 1, \ldots, km - m + 1$ of $m$ numbers, and let $A = B_1 B_2 \cdots B_n$. This is a permutation of $1, \ldots, nm$. Each number of $B_k$ is smaller than each number of $B_{k+1}$. An increasing subsequence takes at most one number from each block, because each block decreases, so it has length at most $n$. A decreasing subsequence cannot take a number from $B_k$ and then a later number from $B_{k'}$ with $k' > k$, because that number is larger, so it stays in one block and has length at most $m$. $\blacksquare$

## Consequences

- **Square root bound.** With $n = m = \lceil \sqrt{N} \rceil - 1$, $nm + 1 \le N$, so each sequence of $N$ distinct numbers has a monotone subsequence of length at least $\lceil \sqrt{N} \rceil$. For $N = 10 = 3 \cdot 3 + 1$, there is a monotone subsequence of length 4.
- **Non-distinct numbers.** If the numbers may repeat, the same proof with "non-decreasing" in place of "increasing" and "strictly decreasing" kept shows: each sequence of $nm + 1$ numbers has a non-decreasing subsequence of length $n + 1$ or a strictly decreasing one of length $m + 1$. The claim still holds, because $a_i \le a_j$ gives $u_j > u_i$.
- **A test for LIS code.** On a permutation of length $N$, the outputs of an LIS routine and of its mirror must have a product of at least $N$.
- **Schensted's theorem.** The insertion of a permutation into a [Young tableau](/young-tableau/) gives a shape whose first row has length $L_{\uparrow}$ and whose first column has length $L_{\downarrow}$. The shape has $N$ cells inside an $L_{\downarrow} \times L_{\uparrow}$ rectangle, which is a second proof of the product form.
- **Geometry.** Erdős and Szekeres used the lemma to show that among many points in general position in the plane, some $k$ of them are in convex position. This is the "happy ending" problem.

## Tightness

The bound $nm + 1$ is exact, by the construction in the proof. The extremal sequences are many, not only the block sequence. By the Robinson-Schensted correspondence, the permutations of $1, \ldots, nm$ with $L_{\uparrow} \le n$ and $L_{\downarrow} \le m$ are in bijection with pairs of [standard Young tableaux](/standard-young-tableaux/) of the $m \times n$ rectangular shape. So their number is $(f^{(n^m)})^2$, where $f^{\lambda}$ counts the standard tableaux of shape $\lambda$.

| $n$ | $m$ | $nm$ | permutations with $L_{\uparrow} \le n$ and $L_{\downarrow} \le m$ |
| --- | --- | --- | --- |
| 2 | 2 | 4 | 4 = $2^2$ |
| 2 | 3 | 6 | 25 = $5^2$ |
| 3 | 3 | 9 | 1764 = $42^2$ |

For $n = m = 2$ the four permutations are 2143, 2413, 3142 and 3412. Each permutation of 5 numbers has a monotone subsequence of length 3.

An example of the labels for $A = \langle 5, 2, 8, 6, 9, 1, 10, 3, 7, 4 \rangle$, $N = 10$:

| $a_i$ | 5 | 2 | 8 | 6 | 9 | 1 | 10 | 3 | 7 | 4 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $u_i$ | 1 | 1 | 2 | 2 | 3 | 1 | 4 | 2 | 3 | 3 |
| $d_i$ | 1 | 2 | 1 | 2 | 1 | 3 | 1 | 3 | 2 | 3 |

The ten pairs are distinct, as the claim says. Since $u_7 = 4$, there is an increasing subsequence of length 4 (5, 8, 9, 10).

## History

Erdős and Szekeres published the theorem in 1935 in a paper on a problem of geometry: how many points in general position in the plane force $k$ of them to be the vertices of a convex polygon. Seidenberg gave the short proof by pairs of labels in 1959. Schensted's 1961 paper on longest increasing and decreasing subsequences gives a second proof through the shape of the insertion tableau, and Knuth presents this connection in Section 5.1.4 of Volume 3.

## References
