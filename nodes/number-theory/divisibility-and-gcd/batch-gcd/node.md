---
tag: FT9662
kind: algorithm
slug: batch-gcd
name: Batch GCD
aliases:
- Bernstein's batch GCD
- product tree GCD
area: number-theory/divisibility-and-gcd
level: research
summary: Finds all nontrivial pairwise gcds of n integers via product and remainder trees in quasi-linear time.
solves: [all-pairs-gcd]
model: word-ram
complexity:
  vars: {n: the number of inputs, m: the total number of binary digits of the inputs}
  time: {worst: O(m log(m)^2)}
  space: {extra: O(m log(n))}
  bit_operations: {worst: O(m log(m)^2), schoolbook: O(m^2)}
properties: {deterministic: true, recursive: false}
history:
  year: 2004
  people: [Daniel J. Bernstein]
  note: Product and remainder trees for many gcds at once; used in 2012 to factor RSA keys found on the internet.
prereqs: [all-pairs-gcd, subproduct-tree, euclidean-algorithm, integer-multiplication]
see_also: [scaled-remainder-tree, multipoint-evaluation, rsa-cryptosystem, integer-factorization, half-gcd, binary-gcd, trial-division, arbitrary-precision-arithmetic]
sources:
  - paper: "Daniel J. Bernstein, Fast multiplication and its applications, in Algorithmic Number Theory, MSRI Publications 44, Cambridge University Press, 2008"
    locator: pages 325 to 384 (product trees, remainder trees, scaled remainder trees and their costs)
  - paper: "Nadia Heninger, Zakir Durumeric, Eric Wustrow and J. Alex Halderman, Mining your Ps and Qs: detection of widespread weak keys in network devices, Proceedings of the 21st USENIX Security Symposium, 2012"
    locator: pages 205 to 220 (the batch gcd computation on 11 million moduli, with P mod N_i^2 and the follow-up for moduli with g_i = N_i)
  - paper: "Arjen K. Lenstra, James P. Hughes, Maxime Augier, Joppe W. Bos, Thorsten Kleinjung and Christophe Wachter, Ron was wrong, Whit is right, Advances in Cryptology (CRYPTO 2012), Lecture Notes in Computer Science 7417"
    locator: pages 626 to 642
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition
    locator: Chapter 10, Fast polynomial evaluation and interpolation (the subproduct tree and the descent of remainders, here for integers)
---

Batch GCD computes, for each of $n$ integers $N_1, \ldots, N_n$, the value $g_i = \gcd(N_i, \prod_{j \ne i} N_j)$, which is greater than $1$ exactly when $N_i$ shares a factor with some other input. It multiplies the inputs up a balanced [product tree](/subproduct-tree/) to $P = \prod N_j$, sends $P$ back down a remainder tree that reduces modulo the square of each node, so that leaf $i$ receives $P \bmod N_i^2$, and finishes with $g_i = \gcd(N_i, (P \bmod N_i^2)/N_i)$. With quasi-linear multiplication the cost is $O(m \log^2 m)$ bit operations for $m$ total input digits, instead of the $\binom n2$ gcds of the pairwise method. Bernstein described the method; in 2012 it factored tens of thousands of RSA keys collected from the internet that shared a prime with another key.

## In plain words

You have many large numbers and want to know which ones share a factor with any of the others. Comparing every pair takes too long when there are millions of numbers. Instead, multiply all the numbers together. A number shares a factor with the others exactly when it shares a factor with the product of all the others.

That product is gigantic, so it is never divided directly. The numbers are multiplied in pairs, then pairs of pairs, up to the top. The product then travels back down the same tree, and at each step only its remainder modulo the square of the current node is kept, which keeps the numbers small. At the bottom, one small common-divisor computation for each number gives the answer.

## The problem

The input is a list of integers $N_1, \ldots, N_n$. The output is $g_1, \ldots, g_n$ with $g_i = \gcd(N_i, \prod_{j \ne i} N_j)$: the detection form of the [all-pairs GCD](/all-pairs-gcd/) problem. Signs are dropped, since gcds do not depend on them. A zero input $N_i = 0$ has $g_i = |\prod_{j \ne i} N_j|$ and makes every other $g_j = |N_j|$; two zeros make every $g$ equal to $|N_j|$, with $0$ at the zeros. These cases are settled before the trees are built, and the trees then run on positive inputs. For $n = 1$ the empty product is $1$, and $g_1 = 1$.

**Cost model.** The inputs are [arbitrary-precision](/arbitrary-precision-arithmetic/) integers; $m = \sum_i \lceil \lg (N_i + 1) \rceil$ is the total input length in binary digits. $M(k)$ is the cost of a $k$-digit [multiplication](/integer-multiplication/); division with remainder costs $O(M(k))$ by Newton's method. With $M(k) = O(k \log k)$ (Harvey and van der Hoeven) and a [half-gcd](/half-gcd/), the bounds below are in bit operations; on the word RAM divide by the word size. With schoolbook arithmetic, $M(k) = O(k^2)$.

## The algorithm

```pseudo id=main
BATCH-GCD(N[1..n])                           ▷ all N[i] ≥ 1
L1  T[0] ← N                                  ▷ leaves of the product tree
L2  h ← 0
L3  while |T[h]| > 1
L4      T[h + 1] ← products of adjacent pairs of T[h], last element alone if |T[h]| is odd
L5      h ← h + 1
L6  R ← T[h]                                  ▷ [P], the product of all inputs
L7  for ℓ ← h − 1 downto 0
L8      R[j] ← R[parent(j)] mod T[ℓ][j]²  for each node j of level ℓ
L9  for i ← 1 to n
L10     g[i] ← gcd(N[i], R[i] / N[i])         ▷ R[i] = P mod N[i]², divisible by N[i]
L11 return g
```

Lines L1 to L5 build the product tree level by level; level $h$ is the single product $P$. Lines L6 to L8 are the remainder tree: each node receives its parent's value reduced modulo the square of the node. Because a node divides its parent, its square divides its parent's square, so $(P \bmod X^2) \bmod Y^2 = P \bmod Y^2$ whenever $Y \mid X$, and leaf $i$ ends up with $P \bmod N_i^2$. Since $N_i \mid P$, this remainder is $N_i \cdot ((P/N_i) \bmod N_i)$, and line L10 takes one gcd with the [Euclidean algorithm](/euclidean-algorithm/) on numbers no larger than $N_i$.

**Finding the pairs.** The $g_i$ say which inputs share a factor, not with whom. If $1 < g_i < N_i$, then $g_i$ is a proper factor of $N_i$; for RSA moduli $N_i = p_i q_i$ it is $p_i$ or $q_i$, a complete factorization. If $g_i = N_i$, every prime factor of $N_i$ occurs elsewhere, and pairwise gcds of $N_i$ with the other flagged inputs, which are few, split it. The implementation does this in `shared_factor_pairs`.

## Example

Take five RSA-style moduli, $N = (101 \cdot 103, 101 \cdot 107, 109 \cdot 113, 113 \cdot 127, 131 \cdot 137) = (10403, 10807, 12317, 14351, 17947)$.

| level | product tree |
|---|---|
| 3 | 356650402622014230629 |
| 2 | 19872424506715007, 17947 |
| 1 | 112425221, 176761267, 17947 |
| 0 | 10403, 10807, 12317, 14351, 17947 |

Going down, level 2 receives $P \bmod 19872424506715007^2 = P$ (the square exceeds $P$) and $P \bmod 17947^2 = 48151801$. Level 1 receives $3597370079634132$, $25160154377701983$ and $48151801$, and the leaves receive

| $i$ | $N_i$ | $P \bmod N_i^2$ | divided by $N_i$ | $g_i$ |
|---|---|---|---|---|
| 1 | 10403 | 63042180 | 6060 | 101 |
| 2 | 10807 | 14189591 | 1313 | 101 |
| 3 | 12317 | 94643828 | 7684 | 113 |
| 4 | 14351 | 71353172 | 4972 | 113 |
| 5 | 17947 | 48151801 | 2683 | 1 |

So $N_1, N_2$ share $101$ and $N_3, N_4$ share $113$, and each of the four is factored. The fifth modulus shares nothing. For $(12, 18, 35, 49, 10)$ the output is $(12, 6, 35, 7, 10)$: here $g_1 = 12 = N_1$, so a pairwise follow-up is needed to see that $12$ shares $6$ with $18$ and $2$ with $10$.

## Correctness

The key fact is the congruence $(P \bmod X^2) \bmod Y^2 = P \bmod Y^2$ for $Y \mid X$, applied down the tree; it holds because $Y^2 \mid X^2$, so $P$ and $P \bmod X^2$ differ by a multiple of $Y^2$. By induction on the levels, each node $Y$ receives $P \bmod Y^2$, so leaf $i$ receives $r_i = P \bmod N_i^2$. Write $P = N_i Q_i$ with $Q_i = \prod_{j \ne i} N_j$ and $Q_i = s N_i + t$ with $0 \le t < N_i$. Then $P = s N_i^2 + N_i t$ with $0 \le N_i t < N_i^2$, so $r_i = N_i t$ and $r_i / N_i = t = Q_i \bmod N_i$. Finally $\gcd(N_i, Q_i \bmod N_i) = \gcd(N_i, Q_i) = g_i$, the step of the Euclidean algorithm. The full proof is in the proofs.

## Complexity

**Product tree.** There are $h = \lceil \lg n \rceil$ levels above the leaves. The numbers on one level have total length at most $m + n$ binary digits, because the length of a product is at most the sum of the lengths. So each level costs $O(M(m))$, and the tree costs $O(M(m) \log n)$.

**Remainder tree.** At a node $Y$ the input is less than the parent's square $X^2$ and the modulus is $Y^2$, of total length $O(\text{len}(X))$ per node, so a level costs $O(M(m))$ with fast division, and the tree costs $O(M(m) \log n)$.

**Gcds.** The $n$ gcds of line L10 are on numbers of $\beta_i$ digits with $\sum \beta_i = m$: $O(\sum \beta_i^2)$ with the Euclidean algorithm, or $O(\sum M(\beta_i) \log \beta_i) = O(M(m) \log m)$ with a half-gcd.

| part | bit operations, fast arithmetic | schoolbook |
|---|---|---|
| product tree | $O(m \log m \log n)$ | $O(m^2)$ |
| remainder tree | $O(m \log m \log n)$ | $O(m^2)$ |
| final gcds | $O(m \log^2 m)$ | $O(\sum \beta_i^2) \le O(m^2)$ |
| total | $O(m \log^2 m)$ | $O(m^2)$ |
| pairwise gcds, for comparison | $O(n^2 M(\beta) \log \beta)$ | $O(n^2 \beta^2)$ |

The schoolbook column holds because a schoolbook product of an $a$-digit and a $b$-digit number costs $O(ab)$, and over the whole tree each pair of inputs $i \ne j$ meets in exactly one product, at their lowest common ancestor, so the tree costs $O(\sum_{i < j} \beta_i \beta_j) = O(m^2)$; the remainder tree is bounded the same way. With inputs of equal length $\beta = m/n$, the pairwise method costs $\Theta(n^2 \beta^2) = \Theta(m^2)$ with schoolbook gcds, so batch GCD wins only with subquadratic multiplication, which libraries such as GMP use for large numbers.

**Space.** Keeping all levels of the product tree takes $O(m \log n)$ digits; the remainder tree can overwrite one level at a time. Large runs split the inputs into $k$ groups, multiply each group's product tree separately, and combine, trading time for memory.

## Properties

- **Deterministic and exact.** No randomness and no factoring algorithm; it finds only factors that occur in two inputs.
- **One-sided.** $g_i > 1$ certifies a shared factor with a witness $g_i$; $g_i = 1$ certifies that $N_i$ is [coprime](/coprime-integers/) to all other inputs.
- **Output is not pairwise.** $g_i$ mixes the contributions of all other inputs, as $g_1 = 12$ in the example shows.
- **Parallel.** Each level of both trees is a set of independent multiplications or reductions.
- **Batch only.** Adding one new input means recomputing the root path, or a separate remainder-tree pass of the new input against the old product.

## Variants and improvements

- **Scaled remainder tree.** Bernstein's [scaled remainder tree](/scaled-remainder-tree/) replaces the reductions modulo $Y^2$ by multiplications with a precomputed approximation of $1/P$ and short products, saving a constant factor in the remainder tree.
- **Remainders instead of squares.** Reducing $P$ modulo $N_i$ only gives $0$; the square is what keeps the information of $P/N_i$. An alternative computes $\prod_{j \ne i} N_j \bmod N_i$ by a remainder tree with products of siblings, at a similar cost.
- **Coprime base.** Bernstein's factoring into coprimes turns the inputs into a set of pairwise coprime numbers whose products give each input, in essentially linear time, a stronger output than the detection values.
- **Distributed and grouped versions.** Large runs split the moduli into groups that fit in memory, compute each group's product tree, and reduce each group's leaves against the products of the other groups; the levels of one tree can also be spread over several machines.
- **Polynomial analogue.** For polynomials over a field the same trees give $\gcd(f_i, \prod_{j \ne i} f_j)$; this is [multipoint evaluation](/multipoint-evaluation/) with polynomial moduli.

## When to use it

Use it to test a large set of RSA moduli, or other numbers that should be pairwise coprime, for shared factors: certificate collections, key generator audits, or datasets of public keys. It pays off for thousands of inputs and more, and only with a big number library that has subquadratic multiplication. For a few dozen inputs, or when the full table of pairwise gcds is wanted, pairwise gcds are simpler. It does not find factors of a single number; for that, use [integer factorization](/integer-factorization/) methods such as [trial division](/trial-division/) or the elliptic curve method.

## Pitfalls

- **Reducing modulo $N_i$ instead of $N_i^2$.** $P \bmod N_i = 0$ always, and the gcd step then returns $N_i$ for every input.
- **Forgetting the division by $N_i$.** $\gcd(N_i, P \bmod N_i^2)$ is a multiple of $N_i$, because both are; the division of line L10 is required.
- **Zero inputs.** A zero makes $P = 0$ and every reduction meaningless; settle zeros before building the trees.
- **Duplicates.** Two equal moduli give $g_i = N_i$ for both, which is correct but is not a factorization; remove exact duplicates first and report them separately.
- **Memory.** The top levels of the product tree hold numbers of $m$ digits. For millions of 2048-digit moduli this is several gigabytes per level; group the inputs.
- **Quadratic arithmetic.** With schoolbook multiplication, as in naive big number code, the method is no faster than pairwise gcds.

## Implementations

## History

Product trees and remainder trees come from fast polynomial evaluation in the 1970s. Bernstein adapted them to integers and to gcds against a product, in his work on smooth parts of integers and on factoring into coprimes in the early 2000s, and surveyed the techniques in "Fast multiplication and its applications" (2008). In 2012 Heninger, Durumeric, Wustrow and Halderman ran batch GCD on 11 million RSA moduli from TLS and SSH hosts and obtained the private keys of $0.50\%$ of the TLS hosts; Lenstra, Hughes, Augier, Bos, Kleinjung and Wachter found the same weakness independently. The cause was devices that generated keys right after boot, with too little entropy, and so chose the same first prime.

## References
