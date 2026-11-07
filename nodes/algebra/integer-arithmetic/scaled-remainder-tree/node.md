---
tag: T3AFQR
kind: algorithm
slug: scaled-remainder-tree
name: Scaled remainder tree
aliases:
- Bernstein's radix conversion
- scaled remainder tree algorithm
- fraction remainder tree
area: algebra/integer-arithmetic
level: research
summary: Subquadratic radix conversion using a tree of scaled remainders.
model: word-ram
complexity:
  vars: {n: the total number of limbs of the moduli (x has at most n limbs), k: the number of moduli, M: the cost M(j) of multiplying two integers of j limbs}
  time: {worst: O(M(n) log k), average: O(M(n) log k), best: O(M(n) log k)}
  space: {extra: O(n log k)}
properties: {deterministic: true, recursive: true, in_place: false}
prereqs: [subproduct-tree, newton-raphson-division, multiprecision-integer]
see_also: [radix-conversion, batch-gcd, all-pairs-gcd, subproduct-tree, multipoint-evaluation, fast-multipoint-evaluation, chinese-remainder-theorem, newton-raphson-division]
sources:
  - url: https://cr.yp.to/papers.html#scaledmod
    title: Daniel J. Bernstein, Scaled remainder trees, 2004
    locator: the whole paper (the scaled tree, its precision analysis, and the speedup over the remainder tree)
  - paper: Daniel J. Bernstein, Fast multiplication and its applications, in Algorithmic Number Theory, MSRI Publications 44, Cambridge University Press, 2008
    title: Daniel J. Bernstein, Fast multiplication and its applications
    locator: pp. 325 to 384 (product trees, remainder trees and the scaled variant, with their costs)
  - paper: doi:10.1145/860854.860870
    title: Alin Bostan, Grégoire Lecerf and Éric Schost, Tellegen's principle into practice, ISSAC 2003
    locator: pp. 37 to 44 (the transposed multipoint evaluation of polynomials, the polynomial analogue)
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 1.7, Base conversion (the subquadratic divide and conquer conversion that the tree speeds up)
---

A scaled remainder tree computes $x \bmod m_1, \ldots, x \bmod m_k$ for one integer $x$ and many moduli, using multiplications instead of divisions. The plain remainder tree pushes $x \bmod Q$ down the [product tree](/subproduct-tree/) of the moduli, with a division at every node. Bernstein's scaled tree, from 2004, pushes the fraction $x/Q \bmod 1$ instead, kept as a fixed-point number. Since $x/Q_c = Q_s \cdot x/Q$ when $Q = Q_c Q_s$, the fraction for a child is the fractional part of a product with the sibling's modulus, so each node costs one multiplication and a truncation. Only the root needs a division, and at a leaf $x \bmod m = m \cdot (x/m \bmod 1)$. With all truncations rounded down and a few guard digits, every remainder comes out exact. On the [word RAM](/word-ram/) the cost is $O(M(n) \log k)$ limb operations, where $n$ is the total length of the moduli, like the plain tree, with a smaller constant. The same descent of fractions by multiplications is a fast way to convert a large integer to decimal, the method referred to as Bernstein's radix conversion.

## In plain words

Suppose you need the remainders of one huge number $x$ by thousands of moduli. Dividing $x$ by each one is slow. A remainder tree multiplies the moduli in pairs, then pairs of pairs, up to one product $P$, and walks back down: the remainder by a node is the remainder of the parent's remainder, which is smaller.

The scaled tree walks down with fractions instead. It computes $x/P$ once, keeping only the digits after the point. To get $x$ divided by half of $P$, multiply that fraction by the other half and again keep only the part after the point. So every step down is a multiplication. At the bottom, the fraction for $m$ times $m$ is the remainder. Cutting the fractions short is safe if a few extra digits are kept.

## The problem

The input is an integer $x \ge 0$ and moduli $m_1, \ldots, m_k \ge 1$, with $n$ limbs in all in radix $\beta = 2^w$, and $x$ of at most $n$ limbs; a longer $x$ is first reduced modulo the product. The output is the $k$ remainders $x \bmod m_i$. For polynomials this is [multipoint evaluation](/multipoint-evaluation/); for integers it appears in batch factoring and [batch gcd](/batch-gcd/) computations, in [Chinese remaindering](/chinese-remainder-theorem/), and in [radix conversion](/radix-conversion/).

**Cost model.** Word RAM with $w$-bit words. Costs are in limb operations, with $M(j)$ the cost of a $j$-limb product, assumed to satisfy $M(a) + M(b) \le M(a + b)$. The bound $O(M(n) \log k)$ and the exactness are proved; the constant-factor speedup over the plain tree is Bernstein's analysis and depends on how the middle products are done.

## The algorithm

Write $\lambda(Q)$ for the binary length of $Q$, and represent a fraction $y \in [0, 1)$ at a node $v$ by an integer $Y_v$ with $y \approx Y_v / 2^{p_v}$, where $p_v = \lambda(Q_v) + G$.

```pseudo id=main
SCALED-REMAINDERS(x, m_1, …, m_k)
L1  build the product tree; the root holds P = m_1 ⋯ m_k, a node v holds Q_v
L2  d ← the height of the tree;  G ← ⌈log2 (d + 1)⌉, at least 1      ▷ guard digits
L3  Y_root ← ⌊(x mod P) · 2^(p_root) / P⌋                            ▷ the one division
L4  for each node v, from the root down, and each child c of v with sibling s do
L5      Y_c ← ⌊((Q_s · Y_v) mod 2^(p_v)) / 2^(p_v − p_c)⌋             ▷ frac(Q_s y), truncated
L6  for each leaf with modulus m and value Y at precision p do r ← ⌈m · Y / 2^p⌉ mod m
L7  return the remainders r, in the order of the leaves
```

Line L5 is a product of $Q_s$, of $\lambda(Q_s)$ binary digits, by $Y_v$, of about $\lambda(Q_s) + \lambda(Q_c) + G$ digits, of which only the digits from position $p_v - p_c$ to $p_v$ are kept: a middle product. The reduction modulo $2^{p_v}$ and the division by $2^{p_v - p_c}$ are a mask and a shift.

## Example

Let $x = 123456$ and the moduli be $7, 11, 13, 17$. The product tree has $77 = 7 \cdot 11$, $221 = 13 \cdot 17$ and $P = 17017$, so $d = 2$ and $G = 2$. With $\lambda(P) = 15$, $p_{\text{root}} = 17$, and $x \bmod P = 4337$ gives $Y_{\text{root}} = \lfloor 4337 \cdot 2^{17} / 17017 \rfloor = 33405$.

| node | sibling | precision $p$ | $(Q_s Y_{\text{parent}}) \bmod 2^{p_{\text{parent}}}$ | $Y$ | remainder $\lceil mY/2^p \rceil \bmod m$ |
|---|---|---|---|---|---|
| 77 | 221 | 9 | 42473 | 165 | |
| 221 | 77 | 10 | 81817 | 639 | |
| 7 | 11 | 5 | 279 | 17 | $\lceil 3.72 \rceil = 4$ |
| 11 | 7 | 6 | 131 | 16 | $\lceil 2.75 \rceil = 3$ |
| 13 | 17 | 6 | 623 | 38 | $\lceil 7.72 \rceil = 8$ |
| 17 | 13 | 7 | 115 | 14 | $\lceil 1.86 \rceil = 2$ |

Indeed $123456 = 17636 \cdot 7 + 4 = 11223 \cdot 11 + 3 = 9496 \cdot 13 + 8 = 7262 \cdot 17 + 2$. For example, in the row of 77, $221 \cdot 33405 = 7382505$, which is $42473$ modulo $2^{17}$, and $\lfloor 42473 / 2^{8} \rfloor = 165$. The run used 13 products (3 to build the tree, 6 to descend, 4 at the leaves) and one division. All values were computed by script and are checked by the test of this page.

## Correctness

Let $y_v = x/Q_v \bmod 1$, the exact fraction at node $v$. Write $\delta_v$ for the error: $y_v \equiv Y_v/2^{p_v} + \delta_v \pmod 1$, with $0 \le \delta_v$. Line L3 gives $0 \le \delta_{\text{root}} < 2^{-p_{\text{root}}}$. For a child $c$ of $v$ with sibling $s$, $y_c \equiv Q_s y_v$, so line L5 gives $0 \le \delta_c < Q_s \delta_v + 2^{-p_c}$: the error is multiplied by $Q_s$, and the truncation adds less than $2^{-p_c}$, always in the same direction. Multiply by $Q_c$ and put $e_v = Q_v \delta_v$: then $e_c < e_v + Q_c 2^{-p_c} < e_v + 2^{-G}$, since $Q_c < 2^{\lambda(Q_c)}$. The scaled errors grow by less than $2^{-G}$ per level, and $e_{\text{root}} < 2^{-G}$, so at a leaf $m$ at depth at most $d$, $e < (d + 1) 2^{-G} \le 1$. Since $y = r/m$ for the remainder $r$, $mY/2^p \equiv r - e \pmod m$ with $0 \le e < 1$, so its ceiling is $r$ modulo $m$, as line L6 computes. The full proof is below.

## Complexity

**Products, proved.** The tree has $k - 1$ internal nodes. Line L1 makes $k - 1$ products, line L5 two per internal node, and line L6 one per leaf, so $4k - 3$ products in all; the example has $k = 4$ and 13 products. Only line L3 divides.

**Limb operations, proved.** On one level of a balanced tree the moduli of the nodes have about $n$ limbs together, so line L1 costs $O(M(n))$ per level, by the superadditivity of $M$. A product at line L5 has factors of $O(\lambda(Q_v))$ digits, so the products of one level cost $O(M(n))$, and with $\lceil \log_2 k \rceil$ levels the total is $O(M(n) \log k)$. Line L3 is one division of $O(n)$ limbs, $O(M(n))$ by [Newton-Raphson division](/newton-raphson-division/). The recursion has depth $\lceil \log_2 k \rceil$.

**Against the plain tree.** The plain remainder tree has the same $O(M(n) \log k)$ bound, but each node does a division of a $2j$-limb number by a $j$-limb number, which costs a few multiplications even with precomputed reciprocals. The scaled tree replaces it by one middle product, which with FFT multiplication can be done by a cyclic convolution of the shorter length (the wrap-around trick, or the transposed product of Bostan, Lecerf and Schost). Bernstein's paper analyzes the resulting constant; we did not measure it, since a Python implementation with its built-in division does not reflect it.

**Space.** The product tree holds about $n$ limbs per level, $O(n \log k)$ in all, and the fractions on one path add $O(n)$.

## Properties

- **Exact.** The fixed-point fractions are truncated, but the remainders are exact, by the one-sided error bound and the guard digits.
- **Division-free below the root.** Every step down is a product, a mask and a shift.
- **The same tree for many $x$.** The product tree depends only on the moduli and can be reused; then each $x$ costs one division and $3k - 2$ products.
- **Recursive, logarithmic depth.** One level per halving of the set of moduli.

## Variants and improvements

- **Radix conversion.** To write $x < \beta^N$ in a radix $\beta$ such as 10, start from the fraction $x/\beta^N$ and split the digit positions in halves: the low half is the fractional part of the fraction times $\beta^{N/2}$, the high half is the fraction itself, cut to fewer digits. This uses multiplications by powers of $\beta$ only, and it is the method meant by Bernstein's radix conversion; it needs extra guard digits, because the high half carries the error of the low digits, and a final correction of the digits at the borders.
- **Remainders modulo squares.** In [batch gcd](/batch-gcd/), each leaf needs $P \bmod m_i^2$; the scaled tree runs on the tree of squares.
- **Polynomials.** For polynomials, the analogue computes the values $f(a_i)$ by pushing a truncated power series down the subproduct tree; this is the transposed form of [fast multipoint evaluation](/fast-multipoint-evaluation/) of Bostan, Lecerf and Schost.
- **Unbalanced trees.** Moduli of very different sizes are better combined by size, as in a Huffman tree, so that the large moduli sit near the root; the guard digits then follow the height of the tree.

## When to use it

Use the scaled remainder tree when one large integer must be reduced modulo many moduli, or many integers modulo the same set of moduli, at sizes where fast multiplication pays: batch trial division of many numbers by many primes, batch gcd on large sets of RSA moduli, and conversion of very large integers to decimal. For a few moduli, or small sizes, divide directly; for medium sizes, a plain remainder tree with Barrett or Montgomery reduction is simpler.

## Pitfalls

- **Rounding in both directions.** If some truncations round up and others down, the errors no longer telescope, and a remainder can be off by one; round every truncation down and take the ceiling at the leaves.
- **Too few guard digits.** The error grows by up to $2^{-G}$ per level. In our tests with up to 64 moduli, running with $G = 0$ or $G = 1$ instead of $\lceil \log_2(d + 1) \rceil$ gave wrong remainders in most runs.
- **The wrap at zero.** A remainder 0 has the fraction 0, and its approximation from below is just under 1; the ceiling then gives $m$, which must be reduced to 0.
- **Moduli of 1.** They are allowed, have one binary digit, and give remainder 0; moduli of 0 are not allowed.
- **Large $x$.** The bound $O(M(n) \log k)$ needs $x$ of $O(n)$ limbs; a longer $x$ needs its own reduction modulo $P$ first, which line L3 hides in one division.

## Implementations

## History

Remainder trees go back to the fast modular transforms of Moenck and Borodin (1972) and to Fiduccia, who reduced multipoint evaluation of polynomials to products along the [subproduct tree](/subproduct-tree/). Bernstein's paper "Scaled remainder trees" (2004) introduced the scaled version for integers, with the precision analysis, and his survey "Fast multiplication and its applications" (2008) placed it among the tree algorithms for products, remainders and gcds. In the same period, Bostan, Lecerf and Schost (2003) obtained the polynomial analogue from Tellegen's transposition principle. Product and remainder trees are used in batch factorization and batch gcd computations, such as the search for shared prime factors among RSA keys collected on the internet in 2012, and the scaled tree is a drop-in replacement for the remainder tree there.

## References
