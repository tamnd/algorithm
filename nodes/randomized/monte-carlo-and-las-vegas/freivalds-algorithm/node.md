---
tag: Z43DEG
kind: algorithm
slug: freivalds-algorithm
name: Freivalds' algorithm
aliases:
- Freivalds' randomized matrix verification
- Freivalds' randomized verification
- Freivalds' check
area: randomized/monte-carlo-and-las-vegas
level: core
summary: Checks AB = C by comparing A(Br) with Cr for random vectors r, in O(n^2) time per round, with one-sided error at most 1/2 per round.
solves: [matrix-product-verification]
model: word-ram
complexity:
  vars: {n: the dimension of the square matrices, k: the number of rounds}
  time: {worst: Θ(k n^2)}
  space: {extra: Θ(n)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 1977
  people: [Rusins Freivalds]
  note: Freivalds described the check at the IFIP Congress in 1977, as an example of a probabilistic machine that is faster than a deterministic one.
prereqs: [matrix-product-verification, one-sided-error, naive-matrix-multiplication]
see_also: [matrix-product-verification, schwartz-zippel-lemma, polynomial-identity-testing, error-amplification, one-sided-error, monte-carlo-algorithm, fingerprinting, strassen-algorithm]
sources:
  - paper: "Rusins Freivalds, Probabilistic machines can use less running time, Information Processing 77, Proceedings of the IFIP Congress 1977, North-Holland, 1977"
    title: Rusins Freivalds, Probabilistic machines can use less running time
    locator: pages 839 to 842 (the check of a matrix product with random vectors)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 1, Section 1.3 (verifying matrix multiplication, the error bound with the principle of deferred decisions, and repetition)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Chapter 7, Section 7.1 (fingerprinting and Freivalds' technique)
  - paper: "Kuang-Hua Huang and Jacob A. Abraham, Algorithm-based fault tolerance for matrix operations, IEEE Transactions on Computers C-33(6), 1984"
    title: Kuang-Hua Huang and Jacob A. Abraham, Algorithm-based fault tolerance for matrix operations
    locator: pages 518 to 528 (checksum rows and columns, a fixed-vector form of the same check)
---

Freivalds' algorithm checks whether $AB = C$ for $n \times n$ matrices without computing $AB$. It picks a random vector $r \in \{0, 1\}^n$ and compares $A(Br)$ with $Cr$, which costs three matrix-vector products, $\Theta(n^2)$ operations. If $AB = C$ the two vectors are always equal. If $AB \ne C$ they differ with probability at least $1/2$, so $k$ independent rounds miss the error with probability at most $2^{-k}$. It is a [Monte Carlo algorithm](/monte-carlo-algorithm/) with [one-sided error](/one-sided-error/) for the problem of [matrix product verification](/matrix-product-verification/), and it is faster than every known deterministic method for that problem.

## In plain words

To test a claimed product of two tables, do not redo the product. Pick a random column of zeros and ones. Multiply it by the second table, then multiply the result by the first table. Separately, multiply the same column by the claimed product. Each of these steps costs about one pass over a table.

If the claim is right, the two answers are the same, every time. If the claim is wrong, at least half of all random columns give two different answers. So one try catches a wrong claim with at least even odds, and twenty tries miss it less than once in a million.

## The problem

Given matrices $A$ ($n \times m$), $B$ ($m \times p$) and $C$ ($n \times p$) over a ring $R$, decide whether $AB = C$. Usually $n = m = p$ and $R$ is $\mathbb{Z}$, $\mathbb{Z}/q\mathbb{Z}$ or a finite field. See [matrix product verification](/matrix-product-verification/) for the problem, its variants and its bounds.

Notation on this page: $D = AB - C$, $k$ is the number of rounds, and $\Pr$ is over the random vectors only. Randomness model: each coordinate of $r$ is one uniform random bit, so a round uses $p$ fresh bits. For the variant with a set $S$, each coordinate is uniform on $S$, drawn by rejection from uniform bits when $|S|$ is not a power of 2.

## The algorithm

```pseudo id=main
FREIVALDS(A, B, C, k)
L1  for t ← 1 to k do
L2      r ← a vector of p independent uniform bits
L3      x ← B · r                     ▷ m by p times p: O(mp)
L4      y ← A · x                     ▷ n by m times m: O(nm)
L5      z ← C · r                     ▷ n by p times p: O(np)
L6      if y ≠ z then return NOT-EQUAL      ▷ always correct
L7  return EQUAL                       ▷ wrong with probability at most 2^-k
```

The order of the products in lines L3 and L4 is the whole point. $A(Br)$ costs two matrix-vector products. $(AB)r$ would first compute $AB$, which is the work the algorithm avoids.

## Example

Let

$$A = \begin{pmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{pmatrix}, \quad B = \begin{pmatrix} 9 & 8 & 7 \\ 6 & 5 & 4 \\ 3 & 2 & 1 \end{pmatrix}, \quad C = \begin{pmatrix} 30 & 24 & 18 \\ 84 & 69 & \mathbf{55} \\ 138 & 114 & 90 \end{pmatrix}.$$

The true product has 54 in row 2, column 3, so $D = AB - C$ has the single nonzero entry $D_{23} = -1$.

| $r$ | $Br$ (line L3) | $A(Br)$ (line L4) | $Cr$ (line L5) | line L6 |
| --- | --- | --- | --- | --- |
| $(1, 0, 1)$ | $(16, 10, 4)$ | $(48, 138, 228)$ | $(48, 139, 228)$ | NOT-EQUAL |
| $(1, 1, 0)$ | $(17, 11, 5)$ | $(54, 153, 252)$ | $(54, 153, 252)$ | next round |

$Dr = (0, -r_3, 0)$, so a round detects the error exactly when $r_3 = 1$. That is 4 of the 8 vectors in $\{0, 1\}^3$, so the error of one round is exactly $1/2$, and the bound of the theorem is reached. Three rounds miss with probability $1/8$; the tests check both rates over 4000 runs.

## Correctness

A round with vector $r$ computes $y - z = A(Br) - Cr = Dr$, so it says NOT-EQUAL exactly when $Dr \ne 0$. If $AB = C$, then $D = 0$ and every round passes, so the answer EQUAL is right. A NOT-EQUAL answer is right because it shows $D \ne 0$. If $AB \ne C$, pick $D_{ij} \ne 0$ and pair each $r$ with the vector that differs from it in bit $j$. In each pair the values $(Dr)_i$ differ by $D_{ij} \ne 0$, so at most one of the two has $Dr = 0$. Hence one round misses with probability at most $1/2$, and $k$ independent rounds with probability at most $2^{-k}$. With $r$ uniform on $S^p$ over an integral domain, the bound per round is $1/|S|$, by the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/) for the linear polynomial $\sum_j D_{ij} x_j$. The [full proof](proofs/correctness.md) covers both bounds and shows that both are tight.

## Complexity

- **Time.** Lines L3, L4 and L5 cost $mp$, $nm$ and $np$ multiplications and about as many additions, so one round costs $O(nm + mp + np)$, which is $\Theta(n^2)$ for square matrices. $k$ rounds cost $\Theta(k n^2)$ in the worst case, when $AB = C$. Reading the input already costs $\Theta(n^2)$, so for constant $k$ the algorithm is optimal up to a constant.
- **Rounds for a target error.** Error $\delta$ needs $k = \lceil \log_2(1/\delta) \rceil$ rounds: 7 for $10^{-2}$, 20 for $10^{-6}$, 30 for $10^{-9}$ and 64 for $2^{-64}$. See [error amplification](/error-amplification/).
- **Space.** $\Theta(n)$ extra words for $r$, $x$, $y$ and $z$.
- **Random bits.** $p$ bits per round with $r \in \{0, 1\}^p$, or $p \lceil \log_2 |S| \rceil$ bits per round for a set $S$ that is a power of 2.
- **Bit size.** Over $\mathbb{Z}$ with entries of $b$ bits, the entries of $Br$ and $A(Br)$ have $O(b + \log n)$ more bits, so the word-RAM cost stays $\Theta(n^2)$ when $b$ fits in a word. Over $\mathbb{Z}/q\mathbb{Z}$ every value stays below $q$.

## Properties

- **One-sided error.** NOT-EQUAL is always right. EQUAL is wrong with probability at most $2^{-k}$, and only when $AB \ne C$.
- **A witness.** A NOT-EQUAL answer comes with the vector $r$, which anyone can check in $O(n^2)$ time.
- **Independent of the algorithm that computed $C$.** The check works for any claimed product, including one from a fast method such as [Strassen's algorithm](/strassen-algorithm/) or from untrusted hardware.
- **Works over every ring with bits.** The pairing argument needs only subtraction. The stronger bound $1/|S|$ needs an integral domain.
- **No error location.** A failed round shows that some entry of row $i$ of $C$ is wrong, for any $i$ with $(Dr)_i \ne 0$, but not which entry.

## Variants and improvements

- **Larger sets $S$.** Over a field, draw each coordinate from a set $S$ of size $2^t$. One round then has error at most $2^{-t}$, so one round with $t = 20$ gives error $10^{-6}$ with the same three matrix-vector products. Over a finite field $\mathbb{F}_q$ take $S = \mathbb{F}_q$.
- **Few random bits.** Kimbrel and Sinha (1993) take $r = (1, x, x^2, \dots, x^{n-1})$ over a field, with one random $x$ from a set of size at least $2n$. Then $Dr = 0$ means that each row of $D$, read as the coefficients of a polynomial of degree less than $n$, has $x$ as a root, which happens with probability at most $(n - 1)/|S| < 1/2$. Each round uses only about $\log_2 n + 1$ random bits.
- **Products of many matrices.** Check $A_1 A_2 \cdots A_t = C$ with $A_1(A_2(\cdots(A_t r)))$ in $O(t n^2)$ time per round.
- **Pairwise independent rounds.** Rounds with pairwise independent vectors save random bits but give error only $O(1/k)$, see [error amplification](/error-amplification/).
- **Deterministic versions.** A fixed vector, such as the all-ones vector of checksum methods, can be fooled by an adversary who knows it. Korec and Wiedermann (2014) gave a deterministic $O(n^2)$ check for integer matrices in a model with arithmetic on large integers, see [matrix product verification](/matrix-product-verification/).

## When to use it

- After a matrix product from code you do not fully trust: a new fast multiplication routine, a parallel or GPU kernel, or an outsourced computation.
- In tests of matrix code, as an oracle that is cheaper than a reference product.
- When matrices are large enough that $n^3$ is costly but $n^2$ is not. For small $n$, computing $AB$ directly is simpler and exact.
- Not for floating-point matrices without care: rounding makes $A(Br)$ and $Cr$ differ slightly even when $C$ is the correctly rounded product. Compare with a tolerance that depends on the norms of $A$, $B$ and $r$, and accept that the one-sided guarantee is lost.

## Pitfalls

- **Computing $(AB)r$.** Evaluating the products in the wrong order makes the algorithm cost $\Theta(n^3)$.
- **Reusing $r$.** All rounds must use fresh, independent vectors. A fixed or repeated $r$ gives no more than one round of protection, and an adversary who knows $r$ can choose $C$ with $Dr = 0$.
- **Zero divisors with large $S$.** Over $\mathbb{Z}/2^{64}\mathbb{Z}$ (machine integers with wraparound) and $D = (2^{63})$, every even $r$ gives $Dr = 0$. With $S = \{0, 1, 2, 3\}$ the error is $1/2$, not $1/4$. Use bits, or work modulo a prime.
- **Overflow.** With exact integers in fixed-width words, $A(Br)$ can overflow when $C$ does not, or the reverse. Reduce modulo a prime $q$, which is safe for the one-sided guarantee but adds the event $q \mid (Dr)_i$; with a random prime from a large range this event is rare.
- **Too few rounds.** One round has error up to $1/2$. Choose $k$ from the target error, not by habit.

## Implementations

## History

Rusins Freivalds presented the method at the IFIP Congress in 1977, in a paper on the power of probabilistic machines, as a problem where a probabilistic machine is provably faster than any known deterministic method. Huang and Abraham (1984) used checksum rows and columns, which is the same check with fixed vectors, to detect hardware faults in matrix operations. The method became the first example of randomized verification in textbooks, such as Motwani and Raghavan (1995) and Mitzenmacher and Upfal (2005). Kimbrel and Sinha (1993) reduced the number of random bits to about $\log_2 n$ per round.

## References
