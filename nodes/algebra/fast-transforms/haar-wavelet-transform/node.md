---
tag: 5B1Q93
kind: algorithm
slug: haar-wavelet-transform
name: Haar wavelet transform
aliases:
- Haar transform
- discrete Haar transform
- Haar decomposition
area: algebra/fast-transforms
level: intro
summary: The simplest wavelet transform, computed by pairwise averages and differences.
model: real-ram
complexity:
  vars: {n: the length of the input (a power of two)}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
  additions: {worst: 2n - 2}
  multiplications: {worst: 2n - 2}
properties: {deterministic: true, recursive: false, in_place: false, exact: true}
history:
  year: 1910
  people: [Alfréd Haar]
  note: Haar defined the orthogonal system of step functions in his 1910 paper in Mathematische Annalen. The fast pyramid form for general wavelets is due to Mallat (1989).
prereqs: [haar-wavelet, orthogonal-transform, asymptotic-notation]
see_also: [fast-wavelet-transform, discrete-wavelet-transform, walsh-hadamard-transform, fast-walsh-hadamard-transform, parseval-theorem, lifting-scheme, butterfly-operation, jpeg-compression]
sources:
  - paper: doi:10.1109/38.376616
    title: Eric J. Stollnitz, Tony D. DeRose and David H. Salesin, Wavelets for computer graphics, a primer, part 1, IEEE Computer Graphics and Applications 15(3), 1995
    locator: pp. 76 to 84 (the one-dimensional Haar transform by averages and differences, the normalized basis, and compression by dropping small coefficients)
  - book: isbn:9780123743701
    title: Stéphane Mallat, A Wavelet Tour of Signal Processing, The Sparse Way, third edition, Academic Press, 2009
    locator: Chapter 7, Wavelet Bases (the Haar basis, multiresolution approximations, and the fast orthogonal wavelet transform)
  - book: isbn:9780961408879
    title: Gilbert Strang and Truong Nguyen, Wavelets and Filter Banks, Wellesley-Cambridge Press, 1996
    locator: Chapter 1 (the Haar filter bank of averages and differences and its inverse)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 2 (the standard model of floating-point arithmetic) and Chapter 3, Lemma 3.1 (the bound by γ_k of a product of k factors 1 + δ)
  - paper: doi:10.1007/BF01456326
    title: Alfred Haar, Zur Theorie der orthogonalen Funktionensysteme, Mathematische Annalen 69(3), 1910
    locator: pp. 331 to 371 (the orthogonal system of step functions and the uniform convergence of its expansions of continuous functions)
  - paper: doi:10.1109/34.192463
    title: Stéphane G. Mallat, A theory for multiresolution signal decomposition, the wavelet representation, IEEE Transactions on Pattern Analysis and Machine Intelligence 11(7), 1989
    locator: pp. 674 to 693 (the pyramid algorithm that computes the wavelet coefficients level by level)
---

The Haar wavelet transform writes a vector of length $n = 2^t$ in the basis of [Haar wavelets](/haar-wavelet/): one constant vector and $n - 1$ step vectors that are $+1$ on one half of a dyadic block and $-1$ on the other half. The fast algorithm replaces each pair of neighbours by a scaled sum and a scaled difference, keeps the differences, and repeats on the sums. It costs $2n - 2$ additions and $2n - 2$ multiplications, so $\Theta(n)$, which is less than the $\Theta(n \log n)$ of an [FFT](/fast-fourier-transform/). With the scale $1/\sqrt 2$ it is an [orthogonal transform](/orthogonal-transform/), so it keeps the length of the vector and its inverse is its transpose. It is the simplest [discrete wavelet transform](/discrete-wavelet-transform/), and the first example of a multiresolution analysis.

## In plain words

Take a list of numbers whose length is a power of two. Pair the first two, the next two, and so on. For each pair, write down its average and half of its difference. The averages form a list half as long, a blurred copy of the input. The differences say what the blur lost.

Keep the differences, and do the same with the list of averages. Repeat until one average is left: the mean of the whole list. The output is that mean and all the differences, from the coarsest to the finest.

Nothing is lost. From an average and a difference you get back the pair: the first number is their sum and the second is the average minus the difference. In smooth data most differences are close to zero, so dropping them compresses the data with a small error. This is the idea behind wavelet compression.

## The problem

**Input.** A vector $x = (x_0, \ldots, x_{n-1})$ of real numbers, with $n = 2^t$ and $t \ge 0$, and a scale $c$.

**Normalization.** Two scales are in use, and every statement on this page says which one it needs.

- *Orthonormal*: $c = 1/\sqrt 2$. This is the usual choice in signal processing (Mallat, Strang and Nguyen).
- *By averages*: $c = 1/2$. Then each pair gives its mean and half its difference. This is the first form of Stollnitz, DeRose and Salesin, and it is exact over the rationals.

**The basis.** For a level $j$ with $0 \le j < t$, let $L_j = n/2^j$ be the block length, and for $0 \le k < 2^j$ let the block $B_{j,k} = [kL_j, (k+1)L_j)$ have left half $B^-_{j,k}$ and right half $B^+_{j,k}$. The orthonormal Haar vectors are

$$\varphi_i = \frac{1}{\sqrt n}, \qquad \psi_{j,k}(i) = \frac{1}{\sqrt{L_j}} \begin{cases} +1 & i \in B^-_{j,k}, \\ -1 & i \in B^+_{j,k}, \\ 0 & \text{otherwise.} \end{cases}$$

These $1 + \sum_{j<t} 2^j = n$ vectors are orthonormal: two of them on disjoint blocks have disjoint supports, and a vector of a finer level is constant on the support of each coarser vector that overlaps it, so its sum of $\pm 1$ entries cancels.

**Output.** With $c = 1/\sqrt 2$, the vector $y$ with $y_0 = \langle x, \varphi \rangle = \frac{1}{\sqrt n}\sum_i x_i$ and $y_{2^j + k} = \langle x, \psi_{j,k} \rangle$. So $y = Wx$ for the orthogonal matrix $W$ whose rows are these vectors. With $c = 1/2$, $y_0$ is the mean of $x$, and $y_{2^j+k}$ is half the mean of $x$ on $B^-_{j,k}$ minus half the mean on $B^+_{j,k}$. The two outputs differ only by a fixed scale on each entry: the orthonormal $y_{2^j+k}$ is $\sqrt{L_j}$ times the one by averages, and the orthonormal $y_0$ is $\sqrt n$ times the mean.

**Cost model.** The [real RAM](/real-ram/): each addition, subtraction and multiplication of reals costs one step. Additions and subtractions are counted together, apart from multiplications. In floating point, the [standard model](/floating-point-model/) $\mathrm{fl}(a \circ b) = (a \circ b)(1 + \delta)$ with $|\delta| \le u$ applies.

## The algorithm

```pseudo id=main
HAAR(x, c)                         ▷ x[0 .. n − 1], n = 2^t; c = 1/√2 or 1/2
L1  n ← |x|, m ← n                 ▷ x[0 .. m − 1] holds the scaling coefficients of the current level
L2  while m ≥ 2 do
L3      for i ← 0 to m/2 − 1 do
L4          T[i] ← c · (x[2i] + x[2i + 1])           ▷ scaled sum
L5          T[m/2 + i] ← c · (x[2i] − x[2i + 1])     ▷ scaled difference
L6      x[0 .. m − 1] ← T[0 .. m − 1]
L7      m ← m/2

INVERSE-HAAR(y, c)
L8  m ← 2
L9  while m ≤ n do
L10     for i ← 0 to m/2 − 1 do
L11         T[2i] ← (y[i] + y[m/2 + i]) / (2c)
L12         T[2i + 1] ← (y[i] − y[m/2 + i]) / (2c)
L13     y[0 .. m − 1] ← T[0 .. m − 1]
L14     m ← 2m
```

Each pass of the loop of line L2 is one level. It reads the $m$ scaling coefficients at the front of $x$, and writes $m/2$ new scaling coefficients at the front and $m/2$ details behind them. The part $x[m \ldots n-1]$ holds the details of the finer levels and is not touched again. The buffer $T$ of length $n$ is needed because line L4 writes position $i$ while position $2i$ or $2i + 1$ may still be unread. INVERSE-HAAR runs the levels in the opposite order. It undoes one butterfly by the identities $s + d = 2ca$ and $s - d = 2cb$ for $s = c(a + b)$ and $d = c(a - b)$.

## Example

Take $x = (4, 6, 10, 12, 8, 6, 5, 5)$ and the scale $c = 1/2$, by averages.

| level | m | the array after the pass |
|---|---|---|
| input | | 4 6 10 12 8 6 5 5 |
| $j = 2$, pairs | 8 | 5 11 7 5 \| −1 −1 1 0 |
| $j = 1$ | 4 | 8 6 \| −3 1 \| −1 −1 1 0 |
| $j = 0$ | 2 | 7 \| 1 \| −3 1 \| −1 −1 1 0 |

In the first pass the pair $(4, 6)$ gives the mean $5$ and the half difference $(4 - 6)/2 = -1$, and $(5, 5)$ gives $5$ and $0$. The last pass gives the mean $7$ of all eight entries, and $1 = (8 - 6)/2$, half the difference of the means $8$ and $6$ of the two halves. INVERSE-HAAR goes back up: $7 + 1 = 8$ and $7 - 1 = 6$, then $8 \pm (-3)$ gives $5, 11$, and so on.

With $c = 1/\sqrt 2$ the output is $(14\sqrt 2, 2\sqrt 2, -6, 2, -\sqrt 2, -\sqrt 2, \sqrt 2, 0)$, the output above scaled by $\sqrt 8, \sqrt 8, 2, 2, \sqrt 2, \sqrt 2, \sqrt 2, \sqrt 2$. Its sum of squares is $392 + 8 + 36 + 4 + 2 + 2 + 2 + 0 = 446$, the same as $16 + 36 + 100 + 144 + 64 + 36 + 25 + 25 = 446$ for $x$, as an orthogonal transform must give. Dropping the four finest details changes $x$ to $(5, 5, 11, 11, 7, 7, 5, 5)$, with a squared error of $6$, which is the sum of the squares of the dropped orthonormal coefficients.

## Correctness

For a level count $q$ with $0 \le q \le t$, let $m = n/2^q$ and $L = 2^q$. The invariant of line L2, for $c = 1/\sqrt 2$, is: $x[i] = \frac{1}{\sqrt L}\sum_{r \in [iL, (i+1)L)} x^{\mathrm{in}}_r$ for $i < m$, and $x[2^j + k] = \langle x^{\mathrm{in}}, \psi_{j,k} \rangle$ for each level $j$ with $2^j \ge m$. At the start $L = 1$ and the first part is the input itself. One pass maps two neighbouring block sums $S_1/\sqrt L$ and $S_2/\sqrt L$ to $(S_1 + S_2)/\sqrt{2L}$, a block sum of the next level, and to $(S_1 - S_2)/\sqrt{2L}$, which is the inner product with $\psi$ on that block of length $2L$. When $m = 1$, $x[0] = \langle x^{\mathrm{in}}, \varphi \rangle$. For $c = 1/2$ the same proof works with block means. INVERSE-HAAR undoes each pass, in the opposite order. The [full proof](#proof-correctness) is below.

## Complexity

**Operations.** The pass with length $m$ does $m/2$ additions and $m/2$ subtractions on lines L4 and L5, and $m$ multiplications by $c$. The lengths are $m = n, n/2, \ldots, 2$, and $n + n/2 + \cdots + 2 = 2n - 2$. So HAAR uses exactly $2n - 2$ additions and $2n - 2$ multiplications, and INVERSE-HAAR the same with divisions by $2c$ (which is $1$ for $c = 1/2$, so then it needs no multiplications). The copies of line L6 move $2n - 2$ entries in total. The time is $\Theta(n)$ in each case, since the work does not depend on the values, and the extra space is the buffer, $\Theta(n)$. Each output depends on at least one input and the outputs differ, so no algorithm reads fewer than $n$ inputs, and the bound $\Theta(n)$ is optimal.

**Rounding errors (proved).** In floating point with unit roundoff $u$, let $\gamma_k = ku/(1 - ku)$ for $ku < 1$.

- With $c = 1/2$ in binary arithmetic, multiplication by $c$ is exact unless it underflows. So each output entry of a pass is $\mathrm{fl}(a \pm b) \cdot \frac12$, with one relative error of at most $u$.
- With $c = 1/\sqrt 2$, let $\hat c = \mathrm{fl}(1/\sqrt 2) = c(1 + \delta_0)$. A computed entry is $\hat c\,(a \pm b)(1 + \delta_1)(1 + \delta_2) = c(a \pm b)(1 + \theta)$ with $|\theta| \le \gamma_3$ (Higham, Lemma 3.1). So pass $q$ gives $\hat v_{q+1} = Q_q \hat v_q + e_q$, where $Q_q$ is the exact orthogonal map of the pass and $|e_q| \le \gamma_3 |Q_q \hat v_q|$ entry by entry. Hence $\lVert e_q \rVert_2 \le \gamma_3 \lVert \hat v_q \rVert_2$ and $\lVert \hat v_q \rVert_2 \le (1 + \gamma_3)^q \lVert x \rVert_2$. The error after $t$ passes is $\sum_q Q_{t-1} \cdots Q_{q+1} e_q$, and orthogonal maps keep norms, so

$$\frac{\lVert \hat y - y \rVert_2}{\lVert y \rVert_2} \le \sum_{q=0}^{t-1} \gamma_3 (1 + \gamma_3)^q = (1 + \gamma_3)^t - 1 \le \gamma_{3t}, \qquad t = \lg n.$$

The last step uses $1 + \gamma_k = 1/(1 - ku)$ and $(1 - 3u)^t \ge 1 - 3tu$. So the proved normwise bound is about $3u \lg n$. The direct product $Wx$ with the matrix has a bound that grows with $n$, not with $\lg n$. This is a worst-case bound; on random data the observed error is usually much smaller, which is an observation and not a theorem.

## Properties

- **Orthogonal.** With $c = 1/\sqrt 2$, $W$ is orthogonal, so $\lVert Wx \rVert_2 = \lVert x \rVert_2$, which is the form of [Parseval's theorem](/parseval-theorem/) for this basis, and $W^{-1} = W^{T}$.
- **Exact over the rationals.** With $c = 1/2$, all values stay rational, and HAAR followed by INVERSE-HAAR gives back the input exactly. Over the integers, the integer variant below is exact too.
- **Local.** The coefficient $\psi_{j,k}$ depends only on the $L_j$ entries of its block. A change of one input entry changes $t + 1$ outputs.
- **Not in place.** This form uses a buffer of $n$ entries. The lifting form below is in place.
- **Not shift invariant.** Shifting the input by one place can change the details a lot, as with all decimated wavelet transforms.

## Variants and improvements

- **In place, interleaved order.** Store the sum in $x[2i]$ and the difference in $x[2i+1]$, then work on the even positions with stride $2$, then $4$, and so on. This needs only $O(1)$ extra space. The output is in an interleaved order: the coefficient of level $j$ and block $k$ is at index $(2k + 1) \cdot n/2^{j+1}$, and the mean at index $0$. The [lifting scheme](/lifting-scheme/) writes this step as $d = a - b$, then $s = b + d/2$, which gives the mean and twice the detail of the form by averages.
- **Integer Haar transform (S transform).** $d = a - b$ and $s = b + \lfloor d/2 \rfloor$. It maps integers to integers, and $b = s - \lfloor d/2 \rfloor$, $a = b + d$ invert it exactly. It is used in lossless image coding.
- **Partial transform.** Stop after $q < t$ levels. The output then holds $n/2^q$ block sums and the details of the $q$ finest levels.
- **Two dimensions.** Apply the transform to each row and then to each column (the standard decomposition), or one level of rows and columns at a time (the nonstandard decomposition of Stollnitz, DeRose and Salesin). Each costs $\Theta(n^2)$ for an $n \times n$ image.
- **Other wavelets.** The [fast wavelet transform](/fast-wavelet-transform/) replaces the pair $(c, c)$ and $(c, -c)$ by longer filters, for example the Daubechies filters, with the same pyramid of levels.
- **The Walsh-Hadamard transform.** Applying the sum and the difference again to the *details* at each level, and not only to the sums, gives the [Walsh-Hadamard transform](/walsh-hadamard-transform/) with $n \lg n$ additions. The Haar transform does only the part of that work that falls on the sums.

## When to use it

Use the Haar transform when the data is piecewise constant, when the transform must be cheap, or when a coefficient must depend on a short block of the input, as in progressive transmission of images, multiresolution editing of curves and fast approximate queries over large tables of counts. Its basis vectors are not continuous, so for smooth signals the details decay slowly and longer wavelets compress better. For a spectrum by frequency, use the [DFT](/discrete-fourier-transform/) or the [DCT](/discrete-cosine-transform/).

## Pitfalls

- **Mixing the two normalizations.** Coefficients computed with $c = 1/2$ and inverted with $1/\sqrt 2$, or the other way, give back $x$ times a wrong factor on each level. INVERSE-HAAR must divide by $2c$ with the same $c$ as the forward transform. The round-trip tests use both scales.
- **Overwriting before reading.** Writing $x[i] \leftarrow c(x[2i] + x[2i+1])$ without the buffer $T$ destroys $x[2]$ when $i = 1$ before the pair $(x[2], x[3])$ is read. Write into $T$ and copy, as in lines L4 to L6, or use the interleaved in-place order.
- **Thresholds on the unnormalized form.** Dropping all details below a fixed size works as a least-squares choice only in the orthonormal basis. With $c = 1/2$, a coarse detail stands for more entries than a fine one, so scale it by $\sqrt{L_j}$ before the test.
- **Length not a power of two.** The pairing fails at the last entry. Pad the input, or treat the last odd entry as its own block.

## Implementations

The Python code follows the main block. The tests compare it with the closed form of the coefficients, computed in $\Theta(n^2)$ time, exactly over `Fraction` with $c = 1/2$ and with a tolerance scaled by $n$ in floating point with $c = 1/\sqrt 2$.

## History

Alfréd Haar defined the orthogonal system of step functions in his 1910 paper in Mathematische Annalen. He used it to show that, unlike the trigonometric system, an orthonormal system can have Fourier series that converge uniformly for each continuous function. The fast computation of wavelet coefficients level by level, with a pair of filters and decimation by two at each level, is the pyramid algorithm of Mallat (1989), and the Haar transform is its case with filters of length two. Stollnitz, DeRose and Salesin (1995) made the transform by averages and differences a standard tool in computer graphics.

## References
