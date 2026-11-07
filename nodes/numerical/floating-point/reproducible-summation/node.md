---
tag: R755YZ
kind: algorithm
slug: reproducible-summation
name: Reproducible floating-point summation
aliases:
- ExBLAS
- order-independent summation
- ReproBLAS
- pre-rounded summation
- K-fold reproducible summation
area: numerical/floating-point
level: research
summary: Gives bitwise identical sums regardless of the order of summation or the parallel decomposition.
model: floating-point-model
complexity:
  vars: {n: "the number of summands", K: "the number of folds (levels of extraction)"}
  time: {worst: Θ(K·n), average: Θ(K·n), best: Θ(n)}
  space: {extra: Θ(K)}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 2013
  people: [James Demmel, Hong Diep Nguyen]
  note: Demmel and Nguyen gave the K-fold pre-rounding method in 2013 and its parallel form in 2015. It became the ReproBLAS library, while Collange and coauthors built ExBLAS on long accumulators.
prereqs: [floating-point-summation, sterbenz-lemma, error-free-transformations]
see_also: [kulisch-accumulator, kahan-summation, pairwise-summation, neumaier-summation, two-sum, accurate-dot-product, shewchuk-expansion-sum, block-floating-point]
sources:
  - paper: doi:10.1109/ARITH.2013.9
    title: James Demmel and Hong Diep Nguyen, Fast reproducible floating-point summation, 21st IEEE Symposium on Computer Arithmetic (ARITH 2013), 163-172
    locator: the extraction of each summand against a boundary derived from max |x_i| and n, the K-fold algorithm, and its error bound
  - paper: doi:10.1109/TC.2014.2345391
    title: James Demmel and Hong Diep Nguyen, Parallel reproducible summation, IEEE Transactions on Computers 64(7) (2015), 2060-2070
    locator: the one-reduction parallel algorithm with boundaries at fixed exponent bins, so that no global maximum is needed
  - paper: doi:10.1145/3389360
    title: Peter Ahrens, James Demmel and Hong Diep Nguyen, Algorithms for efficient reproducible floating point summation, ACM Transactions on Mathematical Software 46(3) (2020), article 22
    locator: the binned representation used by ReproBLAS, its error bound, and the handling of overflow, underflow and exceptions
  - paper: doi:10.1137/050645671
    title: Siegfried M. Rump, Takeshi Ogita and Shin'ichi Oishi, Accurate floating-point summation part I, faithful rounding, SIAM Journal on Scientific Computing 31(1) (2008), 189-224
    locator: Section 3, the error-free extraction q = fl(fl(σ + p) - σ) against a power of two σ and the bound on the remainder
  - paper: doi:10.1016/j.parco.2015.09.001
    title: Sylvain Collange, David Defour, Stef Graillat and Roman Iakymchuk, Numerical reproducibility for the parallel reduction on multi- and many-core architectures, Parallel Computing 49 (2015), 83-97
    locator: ExBLAS, reproducible sums from floating-point expansions backed by a long accumulator
  - url: https://doi.org/10.1109/IEEESTD.2019.8766229
    title: IEEE Std 754-2019, IEEE Standard for Floating-Point Arithmetic
    locator: Clause 11, Reproducible floating-point results
---

Reproducible summation returns the same floating-point sum of $x_1, \ldots, x_n$ for every order of the terms and for every way of splitting them across threads or processors. Ordinary [floating-point summation](/floating-point-summation/) is not associative, so a parallel reduction can give a different answer on each run. The K-fold method of Demmel and Nguyen rounds every summand against the same power-of-two boundaries, chosen from $\max|x_i|$ and $n$ alone. The rounded parts then add up with no error at all, so their sums cannot depend on the order. Each fold costs about four floating-point operations per summand, and three folds give an error far below that of plain summation.

## In plain words

Imagine adding up a long list of amounts written with many decimals, where several people each add part of the list. If everyone rounds as they go, the grand total depends on who added what and in which order. The fix is to agree on a rounding grid first, based only on the largest amount and the length of the list. Everyone rounds each amount to that grid before adding, and the rounded amounts are coarse enough that adding them never needs rounding again. The leftovers are handled the same way on a finer grid, a few times. Everyone gets the same total, whatever order they use.

## The problem

Given binary64 numbers $x_1, \ldots, x_n$, compute a binary64 value $R$ that depends only on the multiset $\{x_1, \ldots, x_n\}$, not on its order or partition, and that approximates $S = \sum_i x_i$ well. Plain recursive summation fails the first requirement. For $x = (10^{16}, 1, -10^{16}, 1)$, the 24 orders give the three different results $0$, $1$ and $2$. Fixing the order, as Intel's conditional numerical reproducibility mode does, works only if the number of threads and the data layout are also fixed. Correctly rounded summation, for example with a [Kulisch accumulator](/kulisch-accumulator/) or with `math.fsum`, is reproducible, but it costs more. The K-fold method sits in between: it is reproducible by construction and is accurate, though not correctly rounded.

## The algorithm

Let $p = 53$, and let $c = \lceil \log_2 n \rceil + 1$, so that $2^{c} \ge 2n$. The boundaries are powers of two, $M_1 = 2^{\lceil \log_2 m \rceil + c}$ with $m = \max_i |x_i|$, and $M_{j+1} = M_j \cdot 2^{c - p}$. For each summand, fold $j$ splits off the part $q$ of $v$ that lies on the grid $M_j 2^{-p}\mathbb{Z}$, and passes the remainder on to fold $j + 1$.

```pseudo id=main
REPRODUCIBLE-SUM(x₁, …, xₙ, K)
L1  m ← max_i |x_i|;  if m = 0 then return 0
L2  c ← ⌈log₂ n⌉ + 1;  M_j ← 2^(⌈log₂ m⌉ + c + (j − 1)(c − p)) for j = 1, …, K
L3  T₁, …, T_K ← 0
L4  for i ← 1 to n
L5      v ← x_i
L6      for j ← 1 to K
L7          q ← fl(fl(M_j + v) − M_j)          ▷ exact: q is a multiple of M_j · 2^(−p)
L8          v ← fl(v − q)                      ▷ exact: |v| ≤ M_j · 2^(−p)
L9          T_j ← fl(T_j + q)                  ▷ exact, so independent of the order
L10 return fl(T₁ + fl(T₂ + ⋯ + fl(T_{K−1} + T_K)))
```

Lines L1 and L2 depend only on the maximum and the count, which every order and every partition agree on. In parallel, they cost one max-reduction. Each processor then runs L3 to L9 on its own part. The partial $T_j$ are added exactly across processors, and L10 combines the $K$ totals in one fixed order. The implementation also clamps the boundaries at $2^{-1021}$. Below that level it adds one last fold with $M = 0$ that takes the remaining residuals whole, since they are then multiples of $2^{-1074}$ that add exactly.

## Example

Take $x = (10^{16}, 1, -10^{16}, 1)$ with $K = 3$. Here $n = 4$, $c = 3$ and $\lceil \log_2 10^{16} \rceil = 54$, so $M_1 = 2^{57}$, $M_2 = 2^{7} = 128$ and $M_3 = 2^{-43}$.

| fold | boundary | grid unit $M_j 2^{-53}$ | extracted $q$ for $(10^{16}, 1, -10^{16}, 1)$ | residuals after the fold | $T_j$ |
|---|---|---|---|---|---|
| 1 | $2^{57}$ | 16 | $10^{16}, 0, -10^{16}, 0$ | $0, 1, 0, 1$ | 0 |
| 2 | $2^{7}$ | $2^{-46}$ | $0, 1, 0, 1$ | $0, 0, 0, 0$ | 2 |
| 3 | $2^{-43}$ | $2^{-96}$ | $0, 0, 0, 0$ | $0, 0, 0, 0$ | 0 |

The result is $0 + (2 + 0) = 2$ in every one of the 24 orders, and it is the exact sum. In fold 1, the 1s lie below half a grid unit of 16, so they are passed down whole. $10^{16}$ is a multiple of 16, so it is taken whole.

On a larger test, 10000 numbers with magnitudes between $10^{-8}$ and $10^{8}$ were summed in 20 random orders. Plain recursive summation gave 17 different results, with relative errors up to $1.8 \times 10^{-14}$. The K-fold method with $K = 3$ gave one result, and it equalled the correctly rounded sum. That run is an observation, not a guarantee.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Assume round to nearest in binary64 with any tie rule, $n \le 2^{p-2}$, and no overflow, which needs $M_1 \le 2^{1023}$. Each fold $j$ receives values with $|v| \le M_j / (2n)$. For fold 1 this holds because $2n m \le 2^{c} 2^{\lceil \log_2 m \rceil}$. For later folds it holds because the residual after fold $j$ satisfies $|v| \le M_j 2^{-p} = M_{j+1} 2^{-c} \le M_{j+1}/(2n)$.

The input bound gives three facts:

- $\mathrm{fl}(M_j + v)$ lies in $[M_j/2, 2M_j]$, so [Sterbenz's lemma](/sterbenz-lemma/) makes the subtraction in L7 exact.
- $v - q$ is the rounding error of an addition, which is a float, so L8 is exact. This is the extraction of Rump, Ogita and Oishi, a relative of [Fast2Sum](/fast-two-sum/).
- Every $q$ is a multiple of $M_j 2^{-p}$ with $|q| \le M_j/(2n) + M_j 2^{-p}$, so every partial sum of $q$s is a multiple of the unit of magnitude at most $M_j = 2^{p}$ units. All such numbers are floats.

So L9 is exact whatever the order, and $T_j$ is a function of the multiset of inputs. That is the reproducibility claim, and it is proved.

The accuracy bound is also proved. $S = T_1 + \cdots + T_K + E$, where $E$ is the sum of the final residuals, and $|E| \le n M_K 2^{-p} < 2nm(4n 2^{-p})^{K}$. The combination in L10 adds at most $\gamma_{K-1}\sum_j |T_j|$. For $n = 10^{6}$ and $K = 3$, the first term is below $1.8 \times 10^{-22} \, m$.

## Complexity

The method makes one pass to find $m$ and one pass that does $4K$ floating-point operations per summand: two additions and a subtraction in L7 and L8, and the accumulation in L9. That is $\Theta(Kn)$ time. If $m = 0$, the first pass alone decides, in $\Theta(n)$. The state is the $K$ accumulators, $\Theta(K)$ extra space, and the input is read only. Recursive summation costs $n - 1$ additions, so with $K = 3$ the method does about 12 times as many operations. In practice it is often limited by memory bandwidth, and the slowdown that Demmel and Nguyen measured is smaller than the operation count suggests.

## Properties

- **Reproducible by proof.** The result is invariant under every permutation and every partition of the input, given the same $K$, as long as the partial sums are merged with the same boundaries.
- **Accurate.** For $K \ge 2$ the error is dominated by the final combination, which is about $u|S|$ when $T_1$ dominates. When there is heavy cancellation, $|S| \ll \sum |x_i|$, the bound $2nm(4n 2^{-p})^{K}$ is what counts.
- **Not correctly rounded.** The residuals below the last fold are discarded, and L10 rounds. In the tests, three folds matched `math.fsum` on at least 95% of random inputs. That figure is observed, not proved.
- **Only additions.** No branches on data, no sorting, and no division.
- **Needs two passes, or one with fixed bins.** The boundary depends on $\max|x_i|$. The parallel and streaming versions remove this need by using fixed exponent bins, as described under variants.

## Variants and improvements

- **Fixed exponent bins (ReproBLAS).** Instead of boundaries derived from $m$, use boundaries at fixed exponents that are multiples of a bin width $W$ (for example $W = 40$). Keep the $K$ highest bins that are nonzero, and shift them when a larger summand arrives. This allows one-pass and streaming sums and merging of partial results without a max-reduction (Demmel and Nguyen 2015; Ahrens, Demmel and Nguyen 2020).
- **Long accumulator (ExBLAS).** Add every summand exactly into a [Kulisch accumulator](/kulisch-accumulator/), with an expansion of [TwoSum](/two-sum/) results as a fast cache in front. The result is correctly rounded and therefore reproducible, at a higher cost.
- **Fixed reduction tree.** Fix the order of the reduction and the number of threads, as in Intel MKL's conditional numerical reproducibility. Results are reproducible only on the same configuration.
- **Dot products and BLAS.** Apply the method to the products of an [accurate dot product](/accurate-dot-product/), using TwoProduct for exactness or rounding the products first, and build reproducible matrix operations on top of it.
- **Integer conversion.** Scale all summands by a common power of two and convert them to wide integers. This is a coarse form of one fold.

## When to use it

Use it when results have to be bit-identical across runs, thread counts or machines: for debugging parallel codes, for regression testing, for consensus in distributed systems, and wherever regulations demand identical reruns. It also applies when a reduction runs on hardware whose scheduling order is not under the program's control, such as GPU atomics. When only accuracy matters, [pairwise summation](/pairwise-summation/) or [Kahan summation](/kahan-summation/) is cheaper. When both accuracy and reproducibility matter, use a correctly rounded sum.

## Pitfalls

- **Overflow of the boundary.** $M_1$ is $2nm$ rounded up to a power of two, so data near the top of the range, above about $2^{1023 - c}$, overflows. Implementations then scale or use a top bin. The Python implementation raises an error.
- **Same $K$ and same boundaries everywhere.** Partial sums computed with different $K$, or with boundaries from different local maxima, cannot be merged reproducibly.
- **Compiler reassociation.** Flags such as `-ffast-math` let the compiler simplify $(M + v) - M$ to $v$. That destroys the extraction. Extended-precision registers break it too.
- **Exceptional values.** Infinities and NaNs have to be handled before folding. Otherwise $M + \infty$ and $\infty - \infty$ produce a NaN whose presence depends on the data but whose sign or payload may depend on the order.
- **Reproducible is not correct.** A reproducible result can still be far from $S$ if $K$ is too small for the cancellation in the data.

## Implementations

## History

The need for reproducibility grew with parallel computing. Results that changed with the number of processors made it hard to debug and to verify. Rump, Ogita and Oishi's 2008 work on accurate summation introduced the extraction of a summand against a power-of-two boundary, as a step towards faithfully rounded sums. Demmel and Nguyen turned it into a reproducible method in 2013, with a fixed number of folds and boundaries chosen from the maximum and the count. In 2015 they gave the parallel binned version, which became the ReproBLAS library. Collange, Defour, Graillat and Iakymchuk took the long-accumulator route in ExBLAS. IEEE 754-2019 added Clause 11 on reproducible results. It asks for language support for reproducible modes, but it does not require reproducible reductions.

## References
