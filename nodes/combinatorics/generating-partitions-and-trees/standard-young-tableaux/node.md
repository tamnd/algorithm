---
tag: X6G57J
kind: problem
slug: standard-young-tableaux
name: Standard Young tableaux enumeration
aliases:
- Generating standard Young tableaux
- Listing standard Young tableaux
- SYT generation
area: combinatorics/generating-partitions-and-trees
level: core
summary: List every standard Young tableau of a given shape lambda, of which there are f^lambda by the hook length formula, or every tableau with n cells, of which there are as many as involutions of [n].
complexity:
  vars: {n: the number of cells, N: "the number of tableaux, f^lambda for one shape"}
  time: {worst: Ω(N)}
prereqs: [young-tableau]
see_also: [hook-length-formula, counting-standard-young-tableaux, youngs-lattice, generating-involutions, integer-partition-generation, dyck-word, longest-increasing-subsequence, generic-backtracking-algorithm]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, Sorting and Searching, second edition, Addison-Wesley, 1998
    locator: Section 5.1.4, Tableaux and involutions (the Robinson-Schensted correspondence, the hook formula, and the number of involutions)
  - book: isbn:9780125192606
    title: Albert Nijenhuis and Herbert S. Wilf, Combinatorial Algorithms for Computers and Calculators, second edition, Academic Press, 1978
    locator: the chapter on Young tableaux (a random tableau of a given shape)
  - paper: doi:10.1016/0001-8708(79)90023-9
    title: Curtis Greene, Albert Nijenhuis and Herbert S. Wilf, A probabilistic proof of a formula for the number of Young tableaux of a given shape, Advances in Mathematics 31 (1979), 104-109
    locator: the hook walk and its corner probabilities
  - book: isbn:9780521560696
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 2, Cambridge University Press, 1999
    locator: Section 7.11, The RSK algorithm, and Corollary 7.21.6 (the hook length formula)
  - book: isbn:9780387950679
    title: Bruce E. Sagan, The Symmetric Group, second edition, Springer, 2001
    locator: Chapter 3, Combinatorial algorithms (the Robinson-Schensted algorithm, the hook formula and the hook walk)
---

The standard Young tableaux problem asks for a list of all [standard Young tableaux](/young-tableau/) of a given shape $\lambda$, or of all shapes with $n$ cells. The entry $n$ of a tableau always sits in a corner of the shape, so a recursion that places $n$ in each corner and fills the rest lists the $f^\lambda$ tableaux of one shape in $O(n)$ time for each tableau. The [hook length formula](/hook-length-formula/) gives the length of the list in advance, and the same recursion with addable cells lists all tableaux of size $n$, which are as many as the involutions of $[n]$.

## In plain words

Draw a staircase of boxes: rows that get shorter from top to bottom, all pushed to the left. Write the numbers 1, 2, 3 and so on in the boxes, one number in each box, so that numbers grow to the right in each row and grow downward in each column. The task is to list every such filling once.

The largest number must be in a box with nothing to its right and nothing below it. So try each such end box for the largest number, remove that box, and fill the smaller staircase in the same way. Every choice leads to at least one full filling, so the search never wastes work on a dead end.

## Definition

**Notation.** $\lambda = (\lambda_1 \ge \cdots \ge \lambda_\ell \ge 1)$ is a partition of $n$, $D(\lambda)$ is its [Ferrers diagram](/ferrers-diagram/), and $f^\lambda$ is the number of standard Young tableaux (SYT) of shape $\lambda$. A corner of $\lambda$ is a cell $(i, \lambda_i)$ with $\lambda_{i+1} < \lambda_i$, and an addable cell is a cell $(i, \lambda_i + 1)$ with $i = 1$ or $\lambda_{i-1} > \lambda_i$, or the cell $(\ell + 1, 1)$.

**Problem (one shape).** Given $\lambda$, output each SYT of shape $\lambda$ exactly once. An SYT is a bijection $T : D(\lambda) \to [n]$ that increases along rows and down columns.

**Problem (one size).** Given $n$, output each SYT with $n$ cells exactly once, over all shapes $\lambda \vdash n$.

**Encodings.** An SYT of shape $\lambda$ is the same as

- its ballot sequence $r_1 \ldots r_n$, where $r_k$ is the row of $k$: a word with $\lambda_i$ letters $i$ in which each prefix has at least as many letters $i$ as letters $i + 1$;
- a saturated chain $\varnothing \subset \lambda^{(1)} \subset \cdots \subset \lambda^{(n)} = \lambda$ in [Young's lattice](/youngs-lattice/).

Lexicographic order of ballot sequences is a natural output order.

**Counts.** By the corner rule and the hook length formula,

$$f^\varnothing = 1, \qquad f^\lambda = \sum_{\text{corners } c} f^{\lambda \setminus c} = \frac{n!}{\prod_{u \in D(\lambda)} h(u)},$$

where $h(u)$ is the hook length of the cell $u$. Over all shapes, $\sum_{\lambda \vdash n} f^\lambda = I_n$, the number of involutions of $[n]$, with $I_0 = I_1 = 1$ and $I_{k+1} = I_k + k\, I_{k-1}$.

## Variants

- **One shape or one size.** List $\mathrm{SYT}(\lambda)$, or list all SYT with $n$ cells.
- **Skew shapes.** List the SYT of a skew shape $\lambda / \mu$. The corner recursion works unchanged; only the count has no product formula.
- **Rectangles and two rows.** The SYT of shape $(k, k)$ are [Dyck words](/dyck-word/), counted by the [Catalan numbers](/catalan-numbers/). The SYT with $a$ rows of length $b$ are the ballot sequences with $b$ copies of each of the letters $1, \ldots, a$.
- **Semistandard tableaux.** List the SSYT of shape $\lambda$ with entries at most $m$. Their number is $\prod_{u} (m + c(u)) / h(u)$, where $c(i, j) = j - i$ is the content of the cell.
- **Counting.** Compute $f^\lambda$ exactly. See [counting standard Young tableaux](/counting-standard-young-tableaux/).
- **Ranking and unranking.** Map an SYT to its position in the lexicographic list of ballot sequences and back.
- **Random generation.** Output one SYT of shape $\lambda$, uniform among the $f^\lambda$.

## Examples

**Shape $(3, 2)$.** In lexicographic order of ballot sequences, the $f^{(3,2)} = 5$ tableaux are

| ballot sequence | row 1 | row 2 |
| --- | --- | --- |
| $11122$ | $1\ 2\ 3$ | $4\ 5$ |
| $11212$ | $1\ 2\ 4$ | $3\ 5$ |
| $11221$ | $1\ 2\ 5$ | $3\ 4$ |
| $12112$ | $1\ 3\ 4$ | $2\ 5$ |
| $12121$ | $1\ 3\ 5$ | $2\ 4$ |

The corner recursion sees the same list from the other end. The corners of $(3, 2)$ are $(1, 3)$ and $(2, 2)$. With $5$ at $(1, 3)$ the rest is an SYT of $(2, 2)$, which has $2$ tableaux. With $5$ at $(2, 2)$ the rest is an SYT of $(3, 1)$, which has $3$. So $f^{(3,2)} = 2 + 3$.

**All tableaux with $4$ cells.** $f^\lambda$ for $\lambda = (4), (3, 1), (2, 2), (2, 1, 1), (1, 1, 1, 1)$ is $1, 3, 2, 3, 1$. The total is $10 = I_4$, and the sum of squares is $24 = 4!$.

**Sizes of the lists.**

| $n$ | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ | $6$ | $7$ | $8$ | $9$ | $10$ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $I_n = \sum_\lambda f^\lambda$ | $1$ | $1$ | $2$ | $4$ | $10$ | $26$ | $76$ | $232$ | $764$ | $2620$ | $9496$ |

For $n = 10$, the largest $f^\lambda$ is $768$, at $\lambda = (4, 3, 2, 1)$. For larger shapes, $f^{(4,4,4)} = 462$ and $f^{(5,4,3,2,1)} = 292864$.

## Known algorithms

| method | output | time | notes |
| --- | --- | --- | --- |
| Corner recursion | $\mathrm{SYT}(\lambda)$ | $O(n)$ for each tableau | place $n$ in each corner; no dead ends |
| Ballot sequence successor | $\mathrm{SYT}(\lambda)$ in lexicographic order | $O(n \ell)$ for each tableau with a plain scan | every ballot prefix that fits in $\lambda$ can be completed |
| Addable cell recursion | all SYT with $n$ cells | $O(n)$ for each tableau | each node of the search tree is an SYT |
| Partitions, then shapes | all SYT with $n$ cells | $O(n)$ for each tableau | [partition generation](/integer-partition-generation/), then the corner recursion |
| [Involutions](/generating-involutions/) and Robinson-Schensted | all SYT with $n$ cells | $O(n^2)$ for each tableau with plain insertion | the insertion tableau of an involution $w$ has $Q(w) = P(w)$ |
| Hook length formula | $f^\lambda$ | $O(n)$ big integer operations | the hook lengths take $O(n)$ time to compute |
| Hook walk (Greene, Nijenhuis, Wilf) | one uniform random SYT of shape $\lambda$ | $O(n (\lambda_1 + \ell))$ | each walk ends in corner $c$ with probability $f^{\lambda \setminus c} / f^\lambda$ |

**Corner recursion.** To list $\mathrm{SYT}(\lambda)$: if $n = 0$, output the empty tableau. Otherwise, for each corner $c$ of $\lambda$, write $n$ in $c$ and list $\mathrm{SYT}(\lambda \setminus c)$ in the remaining cells.

*Correctness.* In an SYT the cell of $n$ has no larger entry to its right or below it, so it is a corner, and removing it leaves an SYT of $\lambda \setminus c$. Conversely, an SYT of $\lambda \setminus c$ with $n$ added in $c$ increases along rows and columns, since $n$ is the largest entry and $c$ has no cell to its right or below. Different corners give different tableaux. $\square$

*Cost.* Every partition $\mu$ has $f^\mu \ge 1$, so every node of the search tree has a leaf below it. Distinct nodes at the same depth have disjoint sets of leaves, so each of the $n + 1$ depths has at most $f^\lambda$ nodes, and the tree has at most $(n + 1) f^\lambda$ nodes. Keep the corners in a list. Removing the corner $(i, \lambda_i)$ can only make $(i, \lambda_i - 1)$ and $(i - 1, \lambda_{i-1})$ new corners, so the list changes in $O(1)$ time for each edge of the tree. The total time is $O(n f^\lambda)$, which is $O(n)$ for each tableau, and the depth of the recursion is $n$. The bound is tight in this model: for $\lambda = (n)$ the tree is a path of $n + 1$ nodes for one tableau.

**Addable cell recursion.** Start from the empty tableau. At depth $k$, for each addable cell $a$ of the current shape, write $k + 1$ in $a$ and go on. Each node at depth $k$ is an SYT with $k$ cells, by the chain encoding, so the tree has $\sum_{k=0}^{n} I_k$ nodes. Since $I_{k+2} = I_{k+1} + (k + 1) I_k \ge 2 I_k$ and $I_{k+1} \ge I_k$, this sum is at most $4 I_n$. With $O(n)$ work for each node the total is $O(n\, I_n)$.

**Hook walk.** Choose a cell of $\lambda$ uniformly at random. While the cell is not a corner, move to a uniformly random other cell of its hook. Greene, Nijenhuis and Wilf proved that the walk stops at corner $c$ with probability $f^{\lambda \setminus c} / f^\lambda$. So writing $n$ in $c$ and repeating on $\lambda \setminus c$ gives a uniform random SYT. Each move goes right or down, so a walk has at most $\lambda_1 + \ell - 1$ moves. The same paper uses the walk to prove the hook length formula.

## Bounds

- **Output.** One shape needs $\Omega(f^\lambda)$ time, and $\Omega(n f^\lambda)$ if each tableau is written in full. The corner recursion meets the second bound. All shapes of size $n$ need $\Omega(n\, I_n)$ to write in full, and the addable cell recursion meets it.
- **Size of $f^\lambda$.** Since $\sum_\lambda (f^\lambda)^2 = n!$, $f^\lambda \le \sqrt{n!}$, so $f^\lambda$ has at most $\frac{1}{2} \log_2 n!$ binary digits. For $n = 10$ the bound is $\lfloor \sqrt{10!} \rfloor = 1904$, and the true maximum is $768$.
- **Size of $I_n$.** Knuth (Section 5.1.4) gives $I_n \sim \frac{1}{\sqrt 2}\, e^{-1/4}\, (n/e)^{n/2}\, e^{\sqrt n}$. The ratio of $I_n$ to this expression is $1.083$ at $n = 10$ and $1.031$ at $n = 80$.
- **Counting.** The hook length formula computes $f^\lambda$ exactly with $2n$ multiplications and one division of integers of $O(n \log n)$ bits.

## Reductions

- **Involutions.** The Robinson-Schensted correspondence maps each permutation $w$ of $[n]$ to a pair $(P, Q)$ of SYT of the same shape, and $w$ is an involution exactly when $P = Q$. So listing all SYT with $n$ cells and listing the involutions of $[n]$ are equivalent, up to $O(n^2)$ time for each object.
- **Permutations.** The pairs $(P, Q)$ of SYT of the same shape match the $n!$ permutations, and the length of the first row is the length of a [longest increasing subsequence](/longest-increasing-subsequence/).
- **Chains in Young's lattice.** $\mathrm{SYT}(\lambda)$ is the set of saturated chains from $\varnothing$ to $\lambda$ in [Young's lattice](/youngs-lattice/).
- **Linear extensions.** An SYT of shape $\lambda$ is a linear extension of the poset of cells of $D(\lambda)$ under $(i, j) \le (i', j')$ when $i \le i'$ and $j \le j'$. Counting the linear extensions of a general poset is #P-complete (Brightwell and Winkler, 1991), so the hook length formula depends on the special shape.
- **Dyck words.** The SYT of shape $(k, k)$ match the Dyck words of length $2k$, through the ballot sequence.

## Applications

- **Representations of the symmetric group.** $f^\lambda$ is the dimension of the irreducible representation of $S_n$ indexed by $\lambda$, and the SYT of shape $\lambda$ index a basis of it. Lists of SYT are the input of the explicit constructions in Sagan, Chapter 2.
- **Increasing subsequences.** The number of permutations of $[n]$ whose longest increasing subsequence has length $k$ is $\sum_{\lambda_1 = k} (f^\lambda)^2$. This gives exact tables for small $n$.
- **Testing.** Brute force lists of SYT check implementations of the hook length formula, of Robinson-Schensted insertion, and of jeu de taquin.
- **Random sampling.** The hook walk samples large random tableaux to study their limit shapes.
- **Catalan objects.** Two-row and rectangular tableaux encode Dyck paths, ballot sequences and some lattice paths in higher dimension.

## References
