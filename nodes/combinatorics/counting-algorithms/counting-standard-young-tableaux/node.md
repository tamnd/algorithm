---
tag: 36XEWM
kind: problem
slug: counting-standard-young-tableaux
name: Counting standard Young tableaux
aliases:
- number of SYT of a shape
- counting SYT
- computing f^lambda
area: combinatorics/counting-algorithms
level: advanced
summary: Counts fillings of a Young diagram that increase along rows and columns.
prereqs: [hook-length-formula, young-tableau]
see_also: [hook-length-formula, standard-young-tableaux, young-tableau, youngs-lattice, generating-involutions, longest-increasing-subsequence, lindstrom-gessel-viennot-lemma, reflection-principle]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, Sorting and Searching, second edition
    locator: Section 5.1.4, Tableaux and involutions (the hook formula, the Robinson-Schensted correspondence and the number of involutions)
  - book: isbn:9780521560696
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 2, Cambridge University Press, 1999
    locator: Chapter 7, Section 7.16, The Jacobi-Trudi identity (the determinant for skew shapes), and Section 7.21, The hook-length formula
  - paper: doi:10.4153/CJM-1954-030-1
    title: J. S. Frame, G. de B. Robinson and R. M. Thrall, The hook graphs of the symmetric group, Canadian Journal of Mathematics 6 (1954), 316-324
    locator: the whole paper (the hook length formula)
---

Counting standard Young tableaux asks for the number $f^\lambda$ of ways to fill the Young diagram of a partition $\lambda$ of $n$ with $1, \ldots, n$ so that the entries increase along rows and down columns. The [hook length formula](/hook-length-formula/) answers it with $O(n)$ multiplications, and a product over the rows answers it with $O(k^2)$ for a shape with $k$ rows. The related counts, for all shapes of size $n$, for skew shapes and for shapes with few rows, need a recurrence, a determinant or a [reflection](/reflection-principle/) argument. The numbers are the dimensions of the irreducible representations of the symmetric group, and they appear in the distribution of the [longest increasing subsequence](/longest-increasing-subsequence/).

## In plain words

Draw rows of boxes, each row no longer than the one above, all starting at the same left edge. Put the numbers from 1 up to the number of boxes into the boxes, one per box, so that numbers grow from left to right and from top to bottom. The question is how many such fillings there are for a given shape. Listing them works only for small shapes, because the counts grow very fast. A formula based on the "hook" of each box gives the count with one multiplication per box, and related questions, such as counting over all shapes at once, have their own short recurrences.

## Definition

**Notation.** $n \ge 0$ is an integer, $[n] = \{1, \ldots, n\}$, and $C(n, k)$ is the binomial coefficient. A partition $\lambda = (\lambda_1 \ge \cdots \ge \lambda_k > 0)$ of $n$ has $k$ rows, and $\lambda \vdash n$ means that $\lambda$ is a partition of $n$. The cells of its Ferrers diagram are $(i, j)$ with $1 \le j \le \lambda_i$, and $h(i, j)$ is the hook length of cell $(i, j)$. For $\mu \subseteq \lambda$, the skew shape $\lambda/\mu$ is the set of cells of $\lambda$ not in $\mu$, and $N = |\lambda/\mu|$ is its number of cells.

A *standard Young tableau* of shape $\lambda$ (or $\lambda/\mu$) is a bijection from its cells to $[n]$ (or $[N]$) that increases along each row and down each column. $f^\lambda$ and $f^{\lambda/\mu}$ are their numbers, see [Young tableau](/young-tableau/).

**Input:** a partition $\lambda$, given by its rows; in the variants an integer $n$, an inner shape $\mu$, a bound on the number of rows, or a modulus.

**Output:** $f^\lambda$, or $t(n) = \sum_{\lambda \vdash n} f^\lambda$, or $f^{\lambda/\mu}$, exactly or modulo the given number.

**Theorem 1 (hook length formula).** $f^\lambda = n! / \prod_{(i, j) \in \lambda} h(i, j)$. With $\ell_i = \lambda_i + k - i$, equivalently $f^\lambda = n! \prod_{i < j} (\ell_i - \ell_j) / \prod_i \ell_i!$.

*Proof.* See [hook length formula](/hook-length-formula/) for the first form, and Knuth, Section 5.1.4, for the equivalence with the second. $\square$

**Theorem 2 (the corner recurrence).** $f^\emptyset = 1$ and $f^\lambda = \sum_c f^{\lambda - c}$ over the corners $c$ of $\lambda$, the cells that end both their row and their column.

*Proof.* The entry $n$ has no larger neighbour to its right or below, so it is in a corner, and removing it is a bijection onto the tableaux of the smaller shapes. $\square$

## Variants

- **All shapes of size $n$.** $t(n) = \sum_{\lambda \vdash n} f^\lambda$ equals the number of involutions of $[n]$, the permutations $\pi$ with $\pi = \pi^{-1}$. The Robinson-Schensted correspondence maps a permutation to a pair of tableaux of the same shape, and a permutation is an involution exactly when the two tableaux are equal (Knuth, Section 5.1.4). So $t(0) = t(1) = 1$ and $t(n) = t(n-1) + (n - 1)\, t(n-2)$, because $n$ is either a fixed point or paired with one of the other $n - 1$ elements. See [generating involutions](/generating-involutions/).
- **Sum of squares.** $\sum_{\lambda \vdash n} (f^\lambda)^2 = n!$, since the Robinson-Schensted correspondence is a bijection from the permutations of $[n]$ onto the pairs of tableaux of the same shape.
- **At most two rows.** The tableaux with at most two rows and $n$ cells number $C(n, \lfloor n/2 \rfloor)$. Write U when the next number is in row 1 and D when it is in row 2. The result is a walk that never goes below 0, and the [reflection principle](/reflection-principle/) counts these walks by $C(n, \lfloor n/2 \rfloor)$.
- **At most $k$ rows.** Sum $f^\lambda$ over the partitions of $n$ with at most $k$ rows, by the corner recurrence restricted to such shapes. These count the involutions of $[n]$ with no decreasing subsequence of length $k + 1$, by Schensted's theorem.
- **Skew shapes.** Aitken's determinant: $f^{\lambda/\mu} = N! \det\big[ 1/(\lambda_i - \mu_j - i + j)! \big]_{i, j = 1}^{k}$, with $1/m! = 0$ for $m < 0$ and $\mu_j = 0$ for $j$ beyond the length of $\mu$ (Stanley, EC2, Section 7.16). With $\mu = \emptyset$ it is the row form of Theorem 1. The [Lindström-Gessel-Viennot lemma](/lindstrom-gessel-viennot-lemma/) gives a proof by nonintersecting lattice paths.
- **Modulo a prime.** For $p > n$, compute the hook product and $n!$ modulo $p$ and divide once. For $p \le n$, first compare the exponents of $p$ in $n!$ and in the hook product. The first is never smaller, since $f^\lambda$ is an integer. If it is larger, $f^\lambda \equiv 0$. If they are equal, remove the factors $p$ from every term and then divide.

## Examples

**Example 1.** For $\lambda = (3, 2)$ there are $f^\lambda = 5$ tableaux. Rows separated by a slash: 123/45, 124/35, 125/34, 134/25 and 135/24. The hook lengths are $4, 3, 1, 2, 1$, and $5!/24 = 5$.

**Example 2: all shapes of size 4.** $f^{(4)} = 1$, $f^{(3,1)} = 3$, $f^{(2,2)} = 2$, $f^{(2,1,1)} = 3$ and $f^{(1,1,1,1)} = 1$. The sum is $10 = t(4)$, and the sum of squares is $1 + 9 + 4 + 9 + 1 = 24 = 4!$.

**Example 3: the totals.** $t(n)$ for $n = 0, \ldots, 11$ is $1, 1, 2, 4, 10, 26, 76, 232, 764, 2620, 9496, 35696$ (OEIS A000085). With at most two rows, the counts for $n = 0, \ldots, 12$ are $1, 1, 2, 3, 6, 10, 20, 35, 70, 126, 252, 462, 924$ (OEIS A001405).

**Example 4: large values.** The shape $(10, 10, 10)$ has $f^\lambda = 7646001090$ (OEIS A005789). Among the 42 partitions of $10$, the largest $f^\lambda$ is $768$, for the staircase $(4, 3, 2, 1)$.

**Example 5: a skew shape.** For $(3, 3)/(1)$, Aitken's determinant and a listing both give $f^{\lambda/\mu} = 5$.

## Known algorithms

**Hook length formula.** Compute the column lengths $\lambda'_j$ in $O(n)$ time, then each $h(i, j) = \lambda_i - j + \lambda'_j - i + 1$ in $O(1)$, then $n!$ and the hook product, and divide once. This is $O(n)$ multiplications. Exactly, $n!$ has $\Theta(n \log n)$ bits, so multiplying one small factor at a time costs $O(n^2 \log n)$ bit operations with schoolbook arithmetic, and a product tree with fast multiplication costs $O(M(n \log n) \log n)$, where $M(m)$ is the cost of multiplying two $m$-bit numbers. Modulo a prime $p > n$ it is $O(n)$ word operations and one modular inverse.

**Row form.** Theorem 1 with the $\ell_i$ uses $O(k^2)$ multiplications for the product of differences, and factorials up to $\ell_1 = \lambda_1 + k - 1$. Cancelling the factorials against $n!$ is natural when $k$ is small and the rows are long.

**Corner recurrence.** Compute $f^\mu$ for all $\mu \subseteq \lambda$ by Theorem 2, in order of size. The shapes inside $\lambda$ number at most $C(\lambda_1 + k, k)$, the lattice paths that form their boundaries, and each has at most $k$ corners. This is the method when cells have extra constraints, for example some entries fixed in advance, and it also gives $f^{\lambda/\mu}$ as the number of paths from $\mu$ to $\lambda$ in [Young's lattice](/youngs-lattice/).

**Aitken's determinant.** For skew shapes, a $k \times k$ determinant with rational entries, $O(k^3)$ field operations, or exact integer arithmetic after multiplying row $i$ by a common factorial.

**Total count.** $t(n)$ by its recurrence in $O(n)$ operations, exactly or modulo $p$. The values have $O(n \log n)$ bits.

**Listing.** [Standard Young tableaux enumeration](/standard-young-tableaux/) lists the tableaux in time proportional to $f^\lambda$ times the cost per tableau, so use it only for small checks.

## Bounds

- **Size.** $\sum_{\lambda \vdash n} (f^\lambda)^2 = n!$ gives $f^\lambda \le \sqrt{n!}$, so $f^\lambda$ has at most $\frac{1}{2} \log_2 n! = O(n \log n)$ bits.
- **The total.** Since all $f^\lambda \ge 0$, $t(n) \ge \sqrt{\sum (f^\lambda)^2} = \sqrt{n!}$. By the Cauchy-Schwarz inequality, $t(n) \le \sqrt{p(n)\, n!}$, where $p(n)$ is the number of partitions of $n$. For $n = 10$: $\sqrt{10!} \approx 1905$, $t(10) = 9496$ and $\sqrt{42 \cdot 10!} \approx 12345$.
- **Lower bound on work.** An exact answer can have $\Theta(n \log n)$ bits, for example for the staircase shapes, so writing it costs that many bit operations.

## Reductions

- A standard tableau of shape $\lambda$ is a maximal chain from $\emptyset$ to $\lambda$ in Young's lattice: add the cell of $1$, then of $2$, and so on. So $f^\lambda$ counts paths in a graded poset.
- A standard tableau with $k$ rows is a lattice word: the sequence of the rows of $1, 2, \ldots, n$, in which every prefix contains at least as many $i$ as $i + 1$. So $f^\lambda$ counts the ballot sequences of an election with $k$ candidates and $\lambda_i$ votes for candidate $i$, and the multi-dimensional reflection principle gives the row form of Theorem 1.
- $f^\lambda$ is the number of linear extensions of the poset on the cells of $\lambda$ ordered by "weakly above and to the left". Counting linear extensions of a general poset is #P-complete, so the hook formula uses the special structure.
- The Robinson-Schensted correspondence reduces the counting of permutations by the length of their longest increasing subsequence to sums of $(f^\lambda)^2$.

## Applications

- **Representation theory.** $f^\lambda$ is the dimension of the irreducible representation of the symmetric group $S_n$ indexed by $\lambda$, and the identity $\sum (f^\lambda)^2 = n!$ is the sum of the squares of these dimensions.
- **Longest increasing subsequences.** The number of permutations of $[n]$ whose longest increasing subsequence has length at most $k$ is $\sum (f^\lambda)^2$ over the $\lambda \vdash n$ with $\lambda_1 \le k$, by Schensted's theorem. This is the starting point of the study of their distribution.
- **Catalan objects.** Two-row rectangles give the Catalan numbers, and three-row rectangles give the counts of three-candidate ballot sequences.
- **Random sampling.** The hook walk samples a uniform random tableau of a given shape, which gives random test inputs for algorithms on tableaux.

## References
