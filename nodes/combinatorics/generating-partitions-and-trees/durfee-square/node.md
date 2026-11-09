---
tag: CT6XJQ
kind: definition
slug: durfee-square
name: Durfee square
aliases:
- Durfee side
- Frobenius rank
area: combinatorics/generating-partitions-and-trees
level: advanced
summary: The largest d by d square of cells in the Ferrers diagram of a partition; its side is the largest i with lambda_i at least i.
prereqs: [ferrers-diagram, conjugate-partition]
see_also: [integer-partitions, integer-partition-function, euler-partition-theorem, generating-functions, young-tableau, bijective-proof]
sources:
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Section 1.8, Partition identities (the Durfee square and the generating function it gives)
  - book: isbn:9780521600903
    title: George E. Andrews and Kimmo Eriksson, Integer Partitions, Cambridge University Press, 2004
    locator: the chapter on Durfee squares
  - book: isbn:9780521637664
    title: George E. Andrews, The Theory of Partitions, Cambridge University Press, 1998 (first published 1976)
    locator: Chapter 2, Infinite series generating functions (identities from the decomposition of a Ferrers graph at its Durfee square)
---

The Durfee square of a [partition](/integer-partitions/) $\lambda$ is the largest square of cells that fits in the upper left corner of its [Ferrers diagram](/ferrers-diagram/). Its side $d(\lambda)$ is the largest $i$ with $\lambda_i \ge i$. Removing the square cuts the diagram into a partition with at most $d$ parts on the right and a partition with parts at most $d$ below, and this gives a second formula for the generating function of all partitions. The square is named after W. P. Durfee, a student of Sylvester.

## Definition

**Notation.** A partition of $n \ge 0$ is $\lambda = (\lambda_1 \ge \cdots \ge \lambda_\ell \ge 1)$ with $|\lambda| = n$, and $\lambda_i = 0$ for $i > \ell$. Its diagram is $D(\lambda) = \{(i, j) : 1 \le i \le \ell,\ 1 \le j \le \lambda_i\}$, and $\lambda'$ is the [conjugate partition](/conjugate-partition/).

**Durfee square.** The side of the Durfee square of $\lambda$ is

$$d(\lambda) = \max\{\, i \ge 0 : \lambda_i \ge i \,\},$$

with the convention that $i = 0$ always qualifies, so $d(()) = 0$. The Durfee square is the set of cells $\{(i, j) : 1 \le i, j \le d(\lambda)\}$.

**Basic facts.** For each partition $\lambda$ of $n$, with $d = d(\lambda)$:

1. *The condition $\lambda_i \ge i$ holds exactly for $i = 1, \ldots, d$.* If $\lambda_i \ge i$ and $1 \le i' < i$, then $\lambda_{i'} \ge \lambda_i \ge i > i'$. So the set of $i$ with $\lambda_i \ge i$ is an initial segment, and $d$ is also the number of such $i$.
2. *The $d \times d$ square is the largest square of cells contained in $D(\lambda)$.* The square lies in $D(\lambda)$ because $\lambda_i \ge d$ for $i \le d$. If a $k \times k$ square lies in $D(\lambda)$ anywhere, its lowest row $i_0 \ge k$ has $\lambda_{i_0} \ge k$, so $\lambda_k \ge \lambda_{i_0} \ge k$, and $k \le d$.
3. *$d(\lambda') = d(\lambda)$.* The transpose of the square is the same square, and transposing maps $D(\lambda)$ onto $D(\lambda')$, so the largest square is the same.
4. *$d^2 \le n$ and $d \le \min(\ell, \lambda_1)$.* The square has $d^2$ cells of the diagram, and it needs $d$ rows and $d$ columns.

**Decomposition.** Remove the square from $D(\lambda)$. What remains is two pieces:

- the part to the right, $\alpha = (\lambda_1 - d, \ldots, \lambda_d - d)$ with zeros dropped, a partition with at most $d$ parts;
- the part below, $\beta = (\lambda_{d+1}, \lambda_{d+2}, \ldots)$, a partition with each part at most $d$, since $\lambda_{d+1} < d + 1$ by the definition of $d$.

The map $\lambda \mapsto (d, \alpha, \beta)$ is a bijection from the partitions of $n$ with Durfee side $d$ onto the triples with $\ell(\alpha) \le d$, $\beta_1 \le d$ and $|\alpha| + |\beta| = n - d^2$. *Proof.* The inverse puts $\alpha_i + d$ for $i = 1, \ldots, d$ and then the parts of $\beta$. The result is non-increasing because $\alpha_d + d \ge d \ge \beta_1$, and its Durfee side is $d$ because row $d$ has at least $d$ cells and row $d + 1$ has $\beta_1 \le d$ cells. The two maps undo each other. $\square$

**The Durfee identity.** The partitions with at most $d$ parts and those with parts at most $d$ have the same generating function $\prod_{k=1}^{d} (1 - x^k)^{-1}$, by conjugation. So the decomposition gives, as [formal power series](/generating-functions/),

$$\prod_{k \ge 1} \frac{1}{1 - x^k} = \sum_{d \ge 0} \frac{x^{d^2}}{(1 - x)^2 (1 - x^2)^2 \cdots (1 - x^d)^2}.$$

The term for $d$ is the generating function of the partitions with Durfee side $d$. Each term starts at $x^{d^2}$, so only $d \le \sqrt n$ contribute to the coefficient of $x^n$.

**Frobenius coordinates.** Put $a_i = \lambda_i - i$ and $b_i = \lambda'_i - i$ for $i = 1, \ldots, d$, the arm and the leg of the diagonal cell $(i, i)$. Then $a_1 > \cdots > a_d \ge 0$, $b_1 > \cdots > b_d \ge 0$, and $n = d + \sum_i a_i + \sum_i b_i$, since the $d$ diagonal hooks cover the diagram without overlap. The pair $(a_1, \ldots, a_d \mid b_1, \ldots, b_d)$ determines $\lambda$, and $d$ is also called the Frobenius rank.

**Computation.** Given $\lambda$ as an array, scan $i = 1, 2, \ldots$ while $\lambda_i \ge i$, in $O(d) \subseteq O(\sqrt n)$ time. By fact 1 the predicate $\lambda_i \ge i$ is true and then false, so binary search finds $d$ in $O(\log \min(\ell, \lambda_1))$ comparisons.

## Examples and non-examples

**A small case.** For $\lambda = (4, 3, 1)$, $\lambda_1 = 4 \ge 1$ and $\lambda_2 = 3 \ge 2$ but $\lambda_3 = 1 < 3$, so $d = 2$.

```
■ ■ □ □
■ ■ □
□
```

The filled cells are the Durfee square. The piece to the right is $\alpha = (2, 1)$, with at most $2$ parts, and the piece below is $\beta = (1)$, with parts at most $2$. Indeed $4 + 3 + 1 = 8 = 2^2 + 3 + 1$. The conjugate $(3, 2, 2, 1)$ also has $d = 2$. The Frobenius coordinates are $(3, 1 \mid 2, 0)$, and $2 + 4 + 2 = 8$.

**Counts by Durfee side.** The partitions of $n$ split by $d$ as follows.

| $n$ | $d = 1$ | $d = 2$ | $d = 3$ | total $p(n)$ |
| --- | --- | --- | --- | --- |
| $8$ | $8$ | $14$ | $0$ | $22$ |
| $10$ | $10$ | $30$ | $2$ | $42$ |
| $12$ | $12$ | $55$ | $10$ | $77$ |

The partitions with $d = 1$ are the hooks $(a, 1^{n-a})$, one for each $a = 1, \ldots, n$. The two partitions of $10$ with $d = 3$ are $(4, 3, 3)$ and $(3, 3, 3, 1)$. For $n = 8$ and $d = 2$, the identity counts pairs $(\alpha, \beta)$ with $|\alpha| + |\beta| = 4$ and parts at most $2$ after conjugating $\alpha$. With $1, 1, 2, 2, 3$ such partitions of $0, 1, 2, 3, 4$, this is $1 \cdot 3 + 1 \cdot 2 + 2 \cdot 2 + 2 \cdot 1 + 3 \cdot 1 = 14$.

**The h-index.** Sort a list of citation counts in non-increasing order as $c_1 \ge c_2 \ge \cdots$. The h-index is the largest $h$ with $c_h \ge h$, so it is the Durfee side of the partition $(c_1, c_2, \ldots)$ with the zeros dropped.

**Non-examples.**

- The largest rectangle in the diagram is not the Durfee square in general. For $(5, 1)$ the largest rectangle is the first row, with $5$ cells, but $d = 1$.
- The number of parts $i$ with $\lambda_i = i$ is not $d$. For $(4, 3, 1)$ no part equals its index, but $d = 2$.
- $d(\lambda)$ is not determined by $n$ and $\ell$. The partitions $(3, 3)$ and $(5, 1)$ of $6$ both have two parts, with $d = 2$ and $d = 1$.

## Related definitions

- [Ferrers diagram](/ferrers-diagram/): the picture that contains the square, with the arm, leg and hook of each cell.
- [Conjugate partition](/conjugate-partition/): it has the same Durfee square. The diagonal hooks of a self-conjugate partition give a partition into distinct odd parts.
- [Partition function](/integer-partition-function/): the Durfee identity is a second formula for its generating function.
- [Euler's partition theorem](/euler-partition-theorem/): another identity with a proof by cutting diagrams.
- [Young tableau](/young-tableau/): the hook lengths of the diagonal cells $(i, i)$, $i \le d$, are $a_i + b_i + 1$ in Frobenius coordinates.
- [Bijective proof](/bijective-proof/): the decomposition at the square is a standard example.

## References
