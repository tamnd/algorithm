---
tag: Z7GN5H
kind: algorithm
slug: sobol-sequence
name: Sobol sequence
aliases:
- Sobol low-discrepancy sequence
- Sobol' sequence
- LP-tau sequence
- Sobol quasirandom sequence
area: numerical/random-number-generation
level: advanced
summary: A base-2 low-discrepancy sequence generated with direction numbers and XOR.
model: word-ram
complexity:
  vars: {s: the dimension, w: "the word size, 32 here"}
  time: {worst: Θ(s), amortized: Θ(s)}
  space: {extra: Θ(s w)}
properties: {deterministic: true, in_place: true, recursive: false}
prereqs: [quasi-monte-carlo-integration, discrepancy, primitive-polynomial]
see_also: [halton-sequence, gray-code, koksma-hlawka-inequality, monte-carlo-integration, linear-feedback-shift-register, equidistribution, pseudorandom-number-generator]
sources:
  - paper: doi:10.1016/0041-5553(67)90144-9
    title: I. M. Sobol', On the distribution of points in a cube and the approximate evaluation of integrals, USSR Computational Mathematics and Mathematical Physics 7(4), 1967, pages 86 to 112
    locator: the definition of the LP-tau sequences through primitive polynomials and direction numbers, and the theorem that they are (t, s)-sequences in base 2
  - paper: "I. A. Antonov and V. M. Saleev, An economic method of computing LP-tau-sequences, USSR Computational Mathematics and Mathematical Physics 19(1), 1979, pages 252 to 256"
    locator: the Gray-code ordering, with one XOR per coordinate per point
  - paper: "Paul Bratley and Bennett L. Fox, Algorithm 659, Implementing Sobol's quasirandom sequence generator, ACM Transactions on Mathematical Software 14(1), 1988, pages 88 to 100"
    locator: the Gray-code implementation and the first published table of initial direction numbers for up to 40 dimensions
  - paper: "Stephen Joe and Frances Y. Kuo, Constructing Sobol sequences with better two-dimensional projections, SIAM Journal on Scientific Computing 30(5), 2008, pages 2635 to 2654"
    locator: the search for initial direction numbers by t-values of two-dimensional projections, and the file new-joe-kuo-6.21201 used here
  - book: isbn:9780898712957
    title: Harald Niederreiter, Random Number Generation and Quasi-Monte Carlo Methods, SIAM, 1992
    locator: Chapter 4, (t, m, s)-nets and (t, s)-sequences, their discrepancy bounds, and the Sobol and Niederreiter constructions
---

The Sobol sequence is a sequence of points in the unit cube $[0, 1)^s$ that fills it far more evenly than independent random points. Introduced by Ilya Sobol' in 1967, it is the most widely used low-discrepancy sequence in quasi-Monte Carlo methods: in [quasi-Monte Carlo integration](/quasi-monte-carlo-integration/) the average of a function over the first $N$ Sobol points converges to the integral at a rate close to $1/N$, against $1/\sqrt{N}$ for [Monte Carlo](/monte-carlo-integration/). Each coordinate is built in base 2 from a [primitive polynomial](/primitive-polynomial/) over $\mathrm{GF}(2)$ and a table of direction numbers, and with the Gray-code ordering of Antonov and Saleev, each new point costs one XOR per coordinate. The sequence is completely deterministic; it is not a random number generator and must not be used as one.

## In plain words

Throw darts at a square at random, and some regions get several darts while others get none. The Sobol sequence places points one after another so that the gaps fill in evenly: after 4 points, each quarter of the square has one; after 16, each of the 16 small squares has one; and the same holds for many other ways of cutting the square into equal boxes.

Each coordinate is a binary fraction. Going from one point to the next flips a fixed pattern of binary digits in each coordinate, chosen from a short list prepared in advance. That makes every new point cost only a few machine operations. Averages of a smooth function over these points come close to the true average much faster than averages over random points.

## The problem

Given a dimension $s$ and a number of points $N$, produce points $x_0, x_1, \ldots \in [0, 1)^s$ whose star [discrepancy](/discrepancy/)

$$D^*_N = \sup_{a \in [0, 1]^s} \Bigl| \frac{\#\{ n < N : x_n \in [0, a) \}}{N} - a_1 a_2 \cdots a_s \Bigr|$$

is small for every $N$, so that by the [Koksma-Hlawka inequality](/koksma-hlawka-inequality/) the integration error $|\frac1N \sum_{n<N} f(x_n) - \int f|$ is at most $V(f)\, D^*_N$ for every $f$ of bounded variation $V(f)$ in the sense of Hardy and Krause. The points should be cheap to compute one after another.

A base-2 tool for measuring evenness is the net. An elementary interval of order $(d_1, \ldots, d_s)$ is a box $\prod_j [a_j 2^{-d_j}, (a_j + 1) 2^{-d_j})$. A set of $2^m$ points is a $(t, m, s)$-net if every elementary interval of volume $2^{t-m}$ contains exactly $2^t$ points; a sequence is a $(t, s)$-sequence if every aligned block of $2^m$ consecutive points, $m \ge t$, is a $(t, m, s)$-net. Smaller $t$ is better, and $t = 0$ is perfect.

## The algorithm

**Direction numbers.** Coordinate $j$ uses a primitive polynomial $x^e + a_1 x^{e-1} + \cdots + a_{e-1} x + 1$ over $\mathrm{GF}(2)$ and odd initial integers $m_1, \ldots, m_e$ with $m_k < 2^k$. Further values follow from

$$m_k = 2 a_1 m_{k-1} \oplus 2^2 a_2 m_{k-2} \oplus \cdots \oplus 2^{e-1} a_{e-1} m_{k-e+1} \oplus 2^e m_{k-e} \oplus m_{k-e},$$

and the direction numbers are $V[k] = m_k 2^{w - k}$, that is $v_k = m_k / 2^k$ as binary fractions. The first coordinate has all $m_k = 1$, which gives the van der Corput sequence. The Sobol point of index $i$ has coordinate $\bigoplus_{k : i_k = 1} V[k]$, where $i_k$ is bit $k - 1$ of $i$.

**Gray-code generation.** The state is the current point $X$, as $s$ integers of $w$ bits, and its index $n$; initially $X = 0$ and $n = 0$.

```pseudo id=main
SOBOL-NEXT(X, n)          ▷ X: s words of w bits; V[j][1..w]: direction numbers
L1  out ← X
L2  c ← 1; k ← n
L3  while k is odd: k ← k ≫ 1; c ← c + 1        ▷ c = 1 + trailing ones of n
L4  for j ← 1 to s: X[j] ← X[j] ⊕ V[j][c]
L5  n ← n + 1
L6  return out / 2^w
```

The $(n+1)$-th call returns the Sobol point of index $g(n) = n \oplus \lfloor n/2 \rfloor$, the Gray code of $n$. Since $g$ permutes every aligned block of $2^m$ indices, the output in Gray-code order has the same blocks, hence the same nets, as the natural order. To start at index $n$ directly, compute the point of index $g(n)$ from the definition in $O(s w)$ operations.

## Example

Take the first three coordinates with the direction numbers of Joe and Kuo. Coordinate 1 has $m_k = 1, 1, 1, \ldots$. Coordinate 2 uses $x + 1$ with $m_1 = 1$, and the recurrence $m_k = 2 m_{k-1} \oplus m_{k-1}$ gives $1, 3, 5, 15, 17, 51, \ldots$. Coordinate 3 uses $x^2 + x + 1$ with $m_1 = 1$, $m_2 = 3$, and $m_3 = 2 \cdot 3 \oplus 4 \cdot 1 \oplus 1 = 3$, then $9, 29, 23, \ldots$. The first points are:

| $n$ | $c$ used next | point |
|---|---|---|
| 0 | 1 | $(0, 0, 0)$ |
| 1 | 2 | $(0.5, 0.5, 0.5)$ |
| 2 | 1 | $(0.75, 0.25, 0.25)$ |
| 3 | 3 | $(0.25, 0.75, 0.75)$ |
| 4 | 1 | $(0.375, 0.375, 0.625)$ |
| 5 | 2 | $(0.875, 0.875, 0.125)$ |
| 6 | 1 | $(0.625, 0.125, 0.875)$ |
| 7 | 4 | $(0.125, 0.625, 0.375)$ |

For instance, going from $n = 3$ to $n = 4$, $n = 3$ has two trailing ones, so $c = 3$, and the third coordinate becomes $0.11_2 \oplus 0.011_2 = 0.101_2 = 0.625$. The four points $n = 0, \ldots, 3$ have one point in each quarter of every coordinate, and in the first two coordinates the eight points put exactly one point in each of the boxes $\frac12 \times \frac14$, $\frac14 \times \frac12$, $\frac18 \times 1$ and $1 \times \frac18$: they form a $(0, 3, 2)$-net. The implementation reproduces the output of Joe and Kuo's reference program in 21 dimensions.

## Correctness

The full proof is in the proof file.

1. **The recurrence.** Consecutive Gray codes differ in exactly bit $c(n) - 1$, and the point map is linear over $\mathrm{GF}(2)$ in the bits of the index, so XORing $V[j][c]$ moves from the point of index $g(n)$ to that of index $g(n+1)$.
2. **One-dimensional stratification.** The recurrence keeps every $m_k$ odd and below $2^k$. Hence each generator matrix (column $k$ holds the binary digits of $v_k$) is upper triangular with ones on the diagonal, and every aligned block of $2^m$ points has exactly one point in each interval $[a 2^{-m}, (a+1) 2^{-m})$ of each coordinate.
3. **Nets by rank.** A block is a $(t, m, s)$-net exactly when, for every $d_1 + \cdots + d_s = m - t$, the top $d_j$ rows of the generator matrices are linearly independent over $\mathrm{GF}(2)$. The implementation computes the exact $t$-values this way.
4. **Sobol's theorem (cited).** With distinct primitive polynomials of degrees $e_1, \ldots, e_s$, the sequence is a $(t, s)$-sequence with $t = \sum_j (e_j - 1)$. The tests confirm the bound for $s \le 5$ and $m \le 10$.

## Complexity

Each point costs $\Theta(s)$ word operations: finding $c$ takes $O(1)$ amortized (on average one trailing one) or one count-trailing-zeros instruction on the complement of $n$, and then one XOR per coordinate. The direction table takes $\Theta(s w)$ words and is computed once in $\Theta(s w e)$ operations. The star discrepancy of a $(t, s)$-sequence in base 2 satisfies $D^*_N = O(2^t (\log N)^s / N)$, with a constant depending on $s$ (Niederreiter, Chapter 4).

## Properties

- **Proved.** Every aligned block of $2^m$ points is stratified in each coordinate, and the sequence is a $(t, s)$-sequence with $t \le \sum_j (e_j - 1)$. For the Joe and Kuo numbers, the exact $t$-values of the first $2^m$ points for $m = 1, \ldots, 10$ in 5 dimensions are $0, 1, 2, 2, 2, 3, 3, 3, 3, 3$, well below the bound 5; the first two coordinates alone give $t = 0$ for every $m$ tested, up to 12.
- **Discrepancy.** $D^*_N = O((\log N)^s / N)$, so quasi-Monte Carlo error decays almost like $1/N$ for integrands of bounded variation.
- **Measured.** For $f(x) = \prod_{j=1}^5 |4 x_j - 2|$, whose integral is 1, the first $2^{12}$ Sobol points give an error of about 0.003; the standard deviation of a plain Monte Carlo estimate with the same number of points is about 0.028.
- **Deterministic and not random.** The points are highly correlated with each other by design; they fail any test of independence.
- **Extensible.** The sequence can be extended in $N$ and, with more direction numbers, in $s$, without discarding earlier points.

## Variants and improvements

- **Direction numbers.** The initial $m_k$ are free; Bratley and Fox (1988) published a table for 40 dimensions, and Joe and Kuo (2003, 2008) chose them so that two-dimensional projections have small $t$-values, with tables up to 21201 dimensions. Different tables give different sequences.
- **Scrambling.** Owen's nested uniform scrambling and the cheaper random linear scrambling of Matoušek randomize the digits while keeping the net structure. This gives unbiased estimates with error estimates from independent replicates (randomized quasi-Monte Carlo), and for smooth integrands a root mean square error near $N^{-3/2}$ up to logarithmic factors.
- **Digital shift.** XORing all points with one random vector is the cheapest randomization; it keeps the nets but does not improve the rate.
- **Niederreiter and Niederreiter-Xing sequences.** Other digital $(t, s)$-sequences with smaller $t$ in high dimensions.
- **[Halton sequence](/halton-sequence/).** Uses a different prime base per coordinate; simpler, but its quality degrades faster with the dimension.

## When to use it

Use the Sobol sequence for numerical integration in moderate to high dimension when the integrand is reasonably smooth or has low effective dimension, as in option pricing, sensitivity analysis (Sobol indices) and computer graphics. Use a number of points that is a power of 2, and use a scrambled version when you need error estimates. Do not use it in place of a [pseudorandom number generator](/pseudorandom-number-generator/): simulations that assume independence, random sampling of decisions, shuffling and cryptography all need random-looking numbers, not evenly spread ones.

## Pitfalls

- **Using it as a random generator.** Consecutive points are strongly dependent, and in high dimensions some pairs of coordinates are badly correlated over small $N$. Algorithms that assume independent draws give wrong answers.
- **Burn-in and dropping points.** Skipping the first point, or a few hundred points, as is common with pseudorandom generators, breaks the net structure of the blocks and can make the error worse. Start at index 0 and take $N = 2^m$ points, or skip a power of 2.
- **Overflow of the index.** With $w$-bit direction numbers there are only $2^w$ points; after that, $c$ exceeds $w$. Use 64-bit words for very long runs.
- **Mixing tables.** The polynomials, the initial numbers and the order of the dimensions must come from the same table; mixing them gives an untested sequence that may have large $t$-values.
- **High nominal dimension.** The bound $t = \sum (e_j - 1)$ grows quickly with $s$, and the later coordinates have poor projections for small $N$. Put the most important variables in the first coordinates.

## Implementations

## History

Ilya M. Sobol' introduced the $LP_\tau$ sequences in 1967 and proved that they are $(t, s)$-sequences in base 2, two decades before Harald Niederreiter developed the general theory of $(t, m, s)$-nets and $(t, s)$-sequences (1987). Antonov and Saleev (1979) showed that the Gray-code order makes each point cost one XOR per coordinate. Bratley and Fox's Algorithm 659 (1988) brought the sequence into wide use, and Paskov and Traub's 1995 report of fast convergence on a 360-dimensional finance problem started its popularity in computational finance. Joe and Kuo published better direction numbers in 2003 and 2008, now the standard in libraries such as SciPy and many others; Owen's scrambling (1995) made it a tool for randomized quasi-Monte Carlo.

## References
