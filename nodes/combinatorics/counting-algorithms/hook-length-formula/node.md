---
tag: 9QFFY8
kind: theorem
slug: hook-length-formula
name: Hook length formula
aliases:
- Frame-Robinson-Thrall formula
- hook formula
area: combinatorics/counting-algorithms
level: advanced
summary: Gives the number of standard Young tableaux of a shape as n! over the product of hook lengths.
prereqs: [young-tableau, ferrers-diagram]
see_also: [counting-standard-young-tableaux, standard-young-tableaux, young-tableau, youngs-lattice, lindstrom-gessel-viennot-lemma, catalan-numbers, longest-increasing-subsequence, generating-involutions]
sources:
  - paper: doi:10.4153/CJM-1954-030-1
    title: J. S. Frame, G. de B. Robinson and R. M. Thrall, The hook graphs of the symmetric group, Canadian Journal of Mathematics 6 (1954), 316-324
    locator: the whole paper (the first statement and proof of the hook length formula)
  - paper: doi:10.1016/0001-8708(79)90023-9
    title: Curtis Greene, Albert Nijenhuis and Herbert S. Wilf, A probabilistic proof of a formula for the number of Young tableaux of a given shape, Advances in Mathematics 31 (1979), 104-109
    locator: the whole paper (the hook walk proof given here)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, Sorting and Searching, second edition
    locator: Section 5.1.4, Tableaux and involutions (the hook formula and its equivalent product over rows)
  - book: isbn:9780521560696
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 2, Cambridge University Press, 1999
    locator: Chapter 7, Section 7.21, The hook-length formula (and the hook-content formula for semistandard tableaux)
---

The hook length formula counts the standard Young tableaux of a given shape: $f^\lambda = n! / \prod_c h(c)$, where the product runs over the cells of the Young diagram and $h(c)$ is the number of cells in the hook of $c$. Frame, Robinson and Thrall found it in 1954. The proof below is the hook walk of Greene, Nijenhuis and Wilf, which shows that both sides satisfy the same recurrence by a probability argument. The formula gives the Catalan numbers, the dimensions of the irreducible representations of the symmetric group, and an $O(n)$ algorithm for [counting standard Young tableaux](/counting-standard-young-tableaux/).

## Statement

**Notation.** $n \ge 0$ is an integer and $[n] = \{1, \ldots, n\}$. A partition $\lambda = (\lambda_1 \ge \lambda_2 \ge \cdots \ge \lambda_k > 0)$ of $n$ has $\lambda_1 + \cdots + \lambda_k = n$. Its [Ferrers diagram](/ferrers-diagram/) is the set of cells $(i, j)$ with $1 \le i \le k$ and $1 \le j \le \lambda_i$, with row $i$ counted from the top and column $j$ from the left. $\lambda'_j$ is the length of column $j$, the $j$-th part of the [conjugate partition](/conjugate-partition/). $C(n, k)$ is the binomial coefficient.

**Hooks.** The *hook* of cell $(i, j)$ is the cell itself, the cells to its right in row $i$ (the arm) and the cells below it in column $j$ (the leg). Its *hook length* is

$$h(i, j) = (\lambda_i - j) + (\lambda'_j - i) + 1.$$

A *corner* is a cell with $h = 1$, that is, the last cell of its row and of its column.

**Tableaux.** A *standard Young tableau* of shape $\lambda$ is a filling of the cells with the numbers of $[n]$, each used once, increasing along each row and down each column, see [Young tableau](/young-tableau/). $f^\lambda$ is their number.

**Theorem (hook length formula).** For every partition $\lambda$ of $n$,

$$f^\lambda = \frac{n!}{\prod_{(i, j) \in \lambda} h(i, j)}.$$

## In plain words

Draw the shape as rows of boxes, each row no longer than the one above it. Fill the boxes with the numbers from 1 up to the number of boxes so that the numbers grow to the right and downwards. To count the fillings, give each box its hook: the box, all boxes to its right and all boxes below it. Write the size of each hook in its box and multiply these sizes. The count of fillings is the factorial of the number of boxes divided by this product. The idea: in a good filling, each box holds the smallest number of its hook, and a random filling does this for one box with chance one over the hook size. The formula says that these chances multiply as if they were independent.

## Proof

**Step 1: the recurrence for $f$.** $f^\emptyset = 1$. For $n \ge 1$, the entry $n$ of a standard tableau has no larger entry to its right or below, so it sits in a corner. Removing it gives a standard tableau of shape $\lambda - c$ for that corner $c$, and putting $n$ back inverts this. So

$$f^\lambda = \sum_{c \text{ corner of } \lambda} f^{\lambda - c}.$$

**Step 2: the target.** Let $F(\lambda) = n! / \prod_{(i, j) \in \lambda} h(i, j)$, so $F(\emptyset) = 1$. By induction on $n$, it is enough to show that $F$ satisfies the same recurrence, that is,

$$\sum_{c \text{ corner of } \lambda} \frac{F(\lambda - c)}{F(\lambda)} = 1. \qquad (1)$$

**Step 3: the ratio.** Let $c = (\alpha, \beta)$ be a corner. Removing $c$ changes the hook of a cell $(i, j)$ only if $c$ is in its arm or leg, that is, for the cells $(i, \beta)$ with $i < \alpha$ and $(\alpha, j)$ with $j < \beta$, and each of these hooks loses exactly one cell. The hook of $c$ itself, of length 1, disappears. So

$$\frac{F(\lambda - c)}{F(\lambda)} = \frac{1}{n} \prod_{i=1}^{\alpha - 1} \frac{h(i, \beta)}{h(i, \beta) - 1} \prod_{j=1}^{\beta - 1} \frac{h(\alpha, j)}{h(\alpha, j) - 1}. \qquad (2)$$

The cells $(i, \beta)$ with $i < \alpha$ have $c$ in their leg, so $h(i, \beta) \ge 2$, and the same holds for $(\alpha, j)$ with $j < \beta$.

**Step 4: the hook walk.** Choose a cell of $\lambda$ uniformly at random. While the current cell $(a, b)$ is not a corner, move to a cell chosen uniformly from the other $h(a, b) - 1$ cells of its hook. Each move increases $a$ or $b$, so the walk stops at a corner after at most $\lambda_1 + k$ moves. So the probabilities that the walk stops at the corners add up to 1, and (1) follows if the walk stops at $c$ with probability (2).

**Step 5: a hook identity.** For a corner $(\alpha, \beta)$ we have $\lambda_\alpha = \beta$ and $\lambda'_\beta = \alpha$. So for every cell $(a, b)$ with $a \le \alpha$ and $b \le \beta$,

$$\big(h(a, \beta) - 1\big) + \big(h(\alpha, b) - 1\big) = (\lambda_a - \beta + \alpha - a) + (\beta - b + \lambda'_b - \alpha) = h(a, b) - 1. \qquad (3)$$

**Step 6: the walks that end at $c$.** A walk that ends at $c = (\alpha, \beta)$ never leaves the rectangle $[1, \alpha] \times [1, \beta]$, since its coordinates never decrease, and every cell of this rectangle is in $\lambda$. Let $A$ be the set of rows it visits and $B$ the set of columns. Then $\min A$ and $\min B$ are the coordinates of the start, $\max A = \alpha$ and $\max B = \beta$. Write $x_i = 1/(h(i, \beta) - 1)$ for $i < \alpha$ and $y_j = 1/(h(\alpha, j) - 1)$ for $j < \beta$.

*Claim.* For a start $(a, b)$, with $a = \min A$ and $b = \min B$, the probability $\pi(A, B)$ that the walk visits exactly the rows $A$ and the columns $B$ and ends at $c$ is

$$\pi(A, B) = \prod_{i \in A \setminus \{\alpha\}} x_i \prod_{j \in B \setminus \{\beta\}} y_j.$$

*Proof of the claim.* By induction on $|A| + |B|$. If $A = \{\alpha\}$ and $B = \{\beta\}$, the walk starts at the corner $c$ and stops, so $\pi = 1$, the empty product. Otherwise $(a, b) \ne c$, and $(a, b)$ is not a corner, because $(a + 1, b)$ or $(a, b + 1)$ is in the rectangle. Let $\Pi$ be the claimed product. The first move goes either down to the next row of $A$ or right to the next column of $B$, each with probability $1/(h(a, b) - 1)$. If $|A| \ge 2$ and $|B| \ge 2$, the induction hypothesis gives $\pi(A \setminus \{a\}, B) = \Pi\,(h(a, \beta) - 1)$ and $\pi(A, B \setminus \{b\}) = \Pi\,(h(\alpha, b) - 1)$, so by (3)

$$\pi(A, B) = \frac{\Pi\,(h(a, \beta) - 1) + \Pi\,(h(\alpha, b) - 1)}{h(a, b) - 1} = \Pi.$$

If $|B| = 1$, then $b = \beta$, the first move must go down, and $\pi(A, B) = \pi(A \setminus \{a\}, B) / (h(a, \beta) - 1) = \Pi$. The case $|A| = 1$ is the same with rows and columns exchanged. $\square$

**Step 7: summing.** The start is uniform, with probability $1/n$, and it is determined by $(A, B)$. So the walk stops at $c$ with probability

$$\frac{1}{n} \sum_{\substack{A \subseteq [\alpha] \\ \alpha \in A}} \sum_{\substack{B \subseteq [\beta] \\ \beta \in B}} \prod_{i \in A \setminus \{\alpha\}} x_i \prod_{j \in B \setminus \{\beta\}} y_j = \frac{1}{n} \prod_{i=1}^{\alpha - 1} (1 + x_i) \prod_{j=1}^{\beta - 1} (1 + y_j).$$

Since $1 + \frac{1}{h - 1} = \frac{h}{h - 1}$, this is (2). This proves (1), and with Step 1 and $F(\emptyset) = f^\emptyset = 1$, induction on $n$ gives $f^\lambda = F(\lambda)$. $\blacksquare$

## Consequences

- **Examples.** For $\lambda = (3, 2)$ the hook lengths are $4, 3, 1$ in the first row and $2, 1$ in the second, so $f^\lambda = 120/24 = 5$. For $(4, 3, 1)$ they are $6, 4, 3, 1$, then $4, 2, 1$, then $1$, so $f^\lambda = 40320/576 = 70$. For the $3 \times 3$ square they are $5, 4, 3$, then $4, 3, 2$, then $3, 2, 1$, so $f^\lambda = 362880/8640 = 42$.
- **Catalan numbers.** For $\lambda = (n, n)$ the hooks are $n + 1, n, \ldots, 2$ in the first row and $n, \ldots, 1$ in the second, so $f^{(n, n)} = \frac{(2n)!}{(n + 1)!\, n!} = C_n$, the [Catalan number](/catalan-numbers/). A tableau of this shape is a ballot sequence: write U when the next number is in row 1 and D when it is in row 2.
- **Three rows.** For $\lambda = (n, n, n)$, $f^\lambda = \frac{2\,(3n)!}{n!\,(n + 1)!\,(n + 2)!}$: $1, 1, 5, 42, 462, 6006, 87516$ for $n = 0, \ldots, 6$ (OEIS A005789), the counts of ballot sequences for three candidates.
- **Divisibility.** The product of the hook lengths divides $n!$.
- **Random tableaux.** Step 7 shows that the hook walk stops at corner $c$ with probability $f^{\lambda - c}/f^\lambda$, which is the probability that $n$ sits at $c$ in a uniformly random tableau. Running the walk, writing $n$ at the corner it finds, removing that corner and repeating with $n - 1$ gives a uniformly random standard tableau of shape $\lambda$.
- **Row form.** With $k$ rows and $\ell_i = \lambda_i + k - i$, the formula is equivalent to $f^\lambda = n! \prod_{i < j} (\ell_i - \ell_j) / \prod_i \ell_i!$, the form found by Frobenius (Knuth, Section 5.1.4). It needs $O(k^2)$ operations in place of $O(n)$.
- **Representations.** $f^\lambda$ is the dimension of the irreducible representation of the symmetric group indexed by $\lambda$, so the formula gives these dimensions, and $\sum_\lambda (f^\lambda)^2 = n!$ by the Robinson-Schensted correspondence, see [standard Young tableaux](/standard-young-tableaux/).

## Tightness

- **Skew shapes.** For a skew shape the same expression is not even an integer in general. For $(3, 3)/(1)$, the hooks inside the five cells have product $3 \cdot 2 \cdot 3 \cdot 2 \cdot 1 = 36$, and $5!/36$ is not an integer, while the true count is 5. Skew shapes need a determinant, such as Aitken's formula, see [counting standard Young tableaux](/counting-standard-young-tableaux/).
- **The corner property in (3).** Identity (3) uses $\lambda_\alpha = \beta$ and $\lambda'_\beta = \alpha$. For a cell that is not a corner it fails, which is why the walk must stop exactly at corners.
- **Other diagrams.** For shifted shapes the formula holds with shifted hooks (Thrall), and for semistandard tableaux with bounded entries it becomes Stanley's hook-content formula (Stanley, EC2, Section 7.21). For general posets in place of Young diagrams there is no hook formula: the count of linear extensions is #P-complete.

## History

Frobenius and Young found determinant and product formulas for $f^\lambda$ around 1900, in their work on the characters of the symmetric group. J. S. Frame, G. de B. Robinson and R. M. Thrall found the hook form in 1954. Greene, Nijenhuis and Wilf gave the hook walk proof in 1979, and Novelli, Pak and Stoyanovskii gave a bijective proof in 1997.

## References
