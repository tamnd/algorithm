---
tag: E4WS9H
kind: algorithm
slug: sparse-fourier-transform
name: Sparse Fourier transform
aliases:
- sparse FFT
- sFFT
- sparse DFT
- sparse discrete Fourier transform
area: algebra/fast-transforms
level: research
summary: Recovers the k largest DFT coefficients of a length-n signal in time sublinear in n when the spectrum is sparse.
solves: [discrete-fourier-transform]
model: real-ram
complexity:
  vars: {n: the transform length (a product of pairwise coprime factors), K: the bound on the number of nonzero DFT coefficients, F: the sum of the factors, d: the number of factors}
  time: {worst: O((K + d) F (F + K + d + log n))}
  space: {extra: O(F (K + d))}
  additions: {worst: O((K + d) F (F + K + d + log n))}
  multiplications: {worst: O((K + d) F (F + K + d + log n))}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 2012
  people: [H. Hassanieh, P. Indyk, D. Katabi, E. Price]
  note: Kushilevitz and Mansour (1993) found the large Fourier coefficients of Boolean functions with queries, and Gilbert, Guha, Indyk, Muthukrishnan and Strauss (2002) gave a randomized algorithm for the DFT polynomial in the sparsity and log n. Hassanieh, Indyk, Katabi and Price (2012) reached O(k log n) time for exactly k-sparse spectra, and Pawar and Ramchandran (2018) gave the FFAST peeling decoder with O(k log k) time for random supports.
prereqs: [discrete-fourier-transform, fast-fourier-transform, chinese-remainder-theorem]
see_also: [chinese-remainder-theorem-fft, number-theoretic-transform, goertzel-algorithm, compressed-sensing, prony-method, ben-or-tiwari-algorithm, sparse-polynomial-interpolation, walsh-hadamard-transform]
sources:
  - paper: doi:10.1137/0222080
    title: Eyal Kushilevitz and Yishay Mansour, Learning decision trees using the Fourier spectrum, SIAM Journal on Computing 22(6), 1993
    locator: pp. 1331 to 1348
  - paper: doi:10.1145/509907.509933
    title: A. C. Gilbert, S. Guha, P. Indyk, S. Muthukrishnan and M. Strauss, Near-optimal sparse Fourier representations via sampling, STOC 2002
    locator: pp. 152 to 161
  - paper: doi:10.1007/s10208-009-9057-1
    title: M. A. Iwen, Combinatorial sublinear-time Fourier algorithms, Foundations of Computational Mathematics 10(3), 2010
    locator: pp. 303 to 338
  - paper: doi:10.1137/1.9781611973099.93
    title: Haitham Hassanieh, Piotr Indyk, Dina Katabi and Eric Price, Simple and practical algorithm for sparse Fourier transform, SODA 2012
    locator: pp. 1183 to 1194
  - paper: doi:10.1145/2213977.2214029
    title: Haitham Hassanieh, Piotr Indyk, Dina Katabi and Eric Price, Nearly optimal sparse Fourier transform, STOC 2012
    locator: pp. 563 to 578 (O(k log n) time for exactly k-sparse spectra)
  - paper: doi:10.1109/TIT.2017.2746568
    title: Sameer Pawar and Kannan Ramchandran, FFAST, an algorithm for computing an exactly k-sparse DFT in O(k log k) time, IEEE Transactions on Information Theory 64(1), 2018
    locator: pp. 429 to 450 (subsampling with coprime factors and the peeling decoder)
  - paper: doi:10.1109/FOCS.2014.61
    title: Piotr Indyk and Michael Kapralov, Sample-optimal Fourier sampling in any constant dimension, FOCS 2014
    locator: pp. 514 to 523
  - paper: doi:10.1109/MSP.2014.2329131
    title: Anna C. Gilbert, Piotr Indyk, Mark Iwen and Ludwig Schmidt, Recent developments in the sparse Fourier transform, IEEE Signal Processing Magazine 31(5), 2014
    locator: pp. 91 to 100 (survey)
  - paper: doi:10.1145/62212.62241
    title: Michael Ben-Or and Prasoon Tiwari, A deterministic algorithm for sparse multivariate polynomial interpolation, STOC 1988
    locator: pp. 301 to 309
---

A sparse Fourier transform computes the [discrete Fourier transform](/discrete-fourier-transform/) of a signal whose spectrum has only a few nonzero coefficients, reading far fewer than $n$ samples and doing far fewer than $n$ operations. The version on this page is exact and deterministic. It factors $n$ into pairwise coprime parts, reads the signal on a few short arithmetic progressions, and takes small DFTs of these subsamples. Each small DFT sorts the frequencies into buckets by their residue modulo one factor. A bucket that holds a single frequency reveals it: shifted reads give its residues modulo the other factors, and the [Chinese remainder theorem](/chinese-remainder-theorem/) gives the frequency. Found frequencies are subtracted from every bucket, which can free other buckets, and the process repeats. This is the peeling scheme of FFAST (Pawar and Ramchandran 2018), with a verification step that makes every reported coefficient provably correct.

## In plain words

Suppose a long recording contains only a handful of pure tones and you want to know which ones. Listening to every sample is wasteful. Instead, listen only to every hundredth sample: tones then blur together, but in a predictable way, and each tone lands in one of a hundred bins fixed by its pitch. Do the same with a different spacing, so each tone lands in other bins. A bin that holds just one tone gives it away completely. Write down that tone and erase it from all the bins it touched. Some bins that held two tones now hold one, so they can be read too. Keep going until every bin is empty. If some tones are tangled so that no bin ever holds one of them alone, the method says so honestly instead of guessing.

## The problem

**Notation.** As on all pages of fast transforms, $X_k = \sum_{j=0}^{n-1} x_j \omega^{jk}$ for $0 \le k < n$, and the inverse is $x_j = \frac1n \sum_k X_k \omega^{-jk}$; there is no factor on the forward transform. Over $\mathbb{C}$, $\omega = \omega_n = e^{-2\pi i/n}$ (the sign of signal processing, FFTW and NumPy; CLRS uses the other sign). Over $\mathbb{Z}/p\mathbb{Z}$, as for the [number-theoretic transform](/number-theoretic-transform/), $\omega$ is a principal $n$-th root of unity, which in a field means an element of order exactly $n$, and $p \nmid n$. The length $n$ need not be a power of two: it is a product $n = f_1 f_2 \cdots f_d$ of pairwise coprime factors, and $F = f_1 + \cdots + f_d$.

**Input.** Access to the samples $x_j$, $0 \le j < n$, as a function that returns $x_j$ for a given $j$; a bound $K$; and a number of verification shifts $T$ (default $T = K$).

**Output.** A set of pairs $(k, v)$ and a flag. Every reported pair has $X_k = v$. If the spectrum has at most $K$ nonzero coefficients, the flag says whether the set is the whole spectrum, and it is in the cases described under Correctness, which include almost all supports when the factors are large compared with $K$.

**Cost model.** The [real RAM](/real-ram/) over $\mathbb{C}$, and unit-cost operations in $\mathbb{Z}/p\mathbb{Z}$. Additions (with subtractions) and multiplications are counted separately, and so are the samples read. Over $\mathbb{C}$, comparisons with zero use a tolerance, and rounding is not part of the proof.

## The algorithm

Write $S = \{0, 1, \ldots, T\} \cup \{n/f_1, \ldots, n/f_d\}$ for the shifts. Stage $i$ reads, for each $s \in S$, the $f_i$ samples $z_t = x_{t n/f_i + s}$ (indices modulo $n$) and takes their DFT of length $f_i$ with the root $\omega_{f_i} = \omega^{n/f_i}$:

$$Z^{(i,s)}_b = \sum_{t=0}^{f_i - 1} x_{t n/f_i + s}\, \omega_{f_i}^{tb} = \frac{f_i}{n} \sum_{k \equiv b \ (\mathrm{mod}\ f_i)} X_k\, \omega^{-sk}, \qquad 0 \le b < f_i.$$

The right side, proved below, is aliasing: subsampling by $n/f_i$ folds the spectrum modulo $f_i$, and the shift $s$ multiplies each frequency by $\omega^{-sk}$. If bucket $b$ of stage $i$ holds one frequency $k$ with value $v$, then $Z^{(i,s)}_b = \frac{f_i}{n} v \omega^{-sk}$ for every $s$. The ratio of the shifts $n/f_j$ and $0$ is $\omega^{-(n/f_j)k} = \omega_{f_j}^{-(k \bmod f_j)}$, which gives $k \bmod f_j$ by looking it up among the $f_j$ powers of $\omega_{f_j}$, and $k \equiv b \pmod{f_i}$ is known.

```pseudo id=main
SPARSE-DFT(x, (f_1, …, f_d), K, T)       ▷ n = f_1 ⋯ f_d pairwise coprime; at most K nonzero X_k
L1  S ← {0, 1, …, T} ∪ {n/f_1, …, n/f_d}
L2  for i ← 1 to d and s ∈ S do  Z^(i,s) ← DFT_(f_i)(x_(s), x_(s + n/f_i), …, x_(s + (f_i − 1) n/f_i))
L3  found ← empty map
L4  repeat until a whole pass changes nothing or K peels were made
L5      for i ← 1 to d and b ← 0 to f_i − 1 with Z^(i,0)_b ≠ 0 do
L6          r_i ← b; for j ≠ i find r_j with Z^(i, n/f_j)_b = ω^(−(n/f_j) r_j) · Z^(i,0)_b, else skip this bucket
L7          k ← the CRT solution of k ≡ r_j (mod f_j) for all j; v ← (n/f_i) · Z^(i,0)_b
L8          if Z^(i,s)_b ≠ (f_i/n) · v · ω^(−s k) for some s ∈ S then skip this bucket       ▷ verify
L9          found[k] ← found[k] + v; for l ← 1 to d and s ∈ S do  Z^(l,s)_(k mod f_l) ← Z^(l,s)_(k mod f_l) − (f_l/n) · v · ω^(−s k)
L10 success ← every Z^(i,s)_b is 0
L11 return found, success
```

Line L9 subtracts the found frequency from all stages and shifts, so the tables always hold the aliasing of the residual spectrum $X - \text{found}$. Over $\mathbb{C}$, "$= 0$" and "$=$" at lines L5, L6, L8 and L10 mean equal up to a tolerance relative to the largest bucket value.

## Example

Over $\mathbb{Z}/13\mathbb{Z}$ with $n = 12 = 4 \cdot 3$ and $\omega = 2$, which has order $12$. The spectrum is $X_1 = 1$, $X_5 = 3$, $X_6 = 2$ and zero elsewhere, so the signal is $x = (7, 1, 2, 8, 6, 9, 2, 3, 7, 9, 3, 8)$. Take $K = T = 3$, so $S = \{0, 1, 2, 3, 4\}$ (the shifts $n/4 = 3$ and $n/3 = 4$ are already there). The tables, with rows $s$ and columns $b$:

| s | stage f = 4: Z_0, Z_1, Z_2, Z_3 | stage f = 3: Z_0, Z_1, Z_2 |
|---|---|---|
| 0 | 0, 10, 5, 0 | 7, 10, 4 |
| 1 | 0, 9, 8, 0 | 6, 5, 5 |
| 2 | 0, 3, 5, 0 | 7, 9, 3 |
| 3 | 0, 11, 8, 0 | 6, 11, 7 |
| 4 | 0, 6, 5, 0 | 7, 12, 12 |

Modulo $13$, $\omega^{-1} = 7$, $f/n = 4/12 = 9$ for the first stage and $3/12 = 10$ for the second.

- Stage $f = 4$, bucket $1$ (frequencies $1$ and $5$ alias here). The ratio of shift $4$ to shift $0$ is $6 \cdot 10^{-1} = 6 \cdot 4 = 11$, which is not among the powers $\omega^{-4r} \in \{1, 9, 3\}$, so the bucket is skipped at line L6.
- Stage $f = 4$, bucket $2$. The ratio is $5/5 = 1 = \omega^{0}$, so $k \equiv 0 \pmod 3$ and $k \equiv 2 \pmod 4$, hence $k = 6$, and $v = 3 \cdot 5 = 2$. Verification: $9 \cdot 2 \cdot \omega^{-6s} = 5 \cdot (-1)^s$ gives $5, 8, 5, 8, 5$, the column. Peel $(6, 2)$: in the stage $f = 3$, bucket $0$ loses $10 \cdot 2 \cdot (-1)^s = 7, 6, 7, 6, 7$ and becomes zero.
- Stage $f = 3$, bucket $1$. The ratio of shift $3$ to shift $0$ is $11 \cdot 4 = 5 = \omega^{-3}$, so $k \equiv 1 \pmod 4$, $k \equiv 1 \pmod 3$, $k = 1$, $v = 4 \cdot 10 = 1$; it verifies and is peeled, which leaves only frequency $5$ in bucket $1$ of the first stage.
- Stage $f = 3$, bucket $2$. The ratio is $7 \cdot 10 = 5$, so $k \equiv 1 \pmod 4$, $k \equiv 2 \pmod 3$, $k = 5$, $v = 4 \cdot 4 = 3$; it verifies and is peeled.

All tables are now zero, so the output is $\{1 \mapsto 1, 5 \mapsto 3, 6 \mapsto 2\}$ with success. The example reads $(4 + 3) \cdot 5 = 35$ samples, more than $n = 12$: it shows the mechanics, and the savings appear only when $n$ is much larger than $K$. The tables and the run were checked by script.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) works in a field with $\omega$ of order exactly $n$. The aliasing formula follows from the inverse DFT and the geometric sum $\sum_{t < f} \omega_f^{t(b - k)} = f$ or $0$. Every update at line L9 is exactly the change of the tables when $(k, v)$ is removed from the spectrum, so the tables always describe the residual spectrum $Y = X - \text{found}$.

*Soundness.* Suppose $Y$ has at most $K \le T$ nonzero entries, and bucket $b$ of stage $i$ passes line L8 with $(k, v)$. The difference between the residual in that residue class and $v$ at $k$ is supported on at most $K + 1$ frequencies, and its aliased sums vanish for the $T + 1 \ge K + 1$ consecutive shifts $0, \ldots, T$. The distinct values $\omega^{-k'}$ make this a Vandermonde system, so the difference is zero: the class holds only $k$, with value $v$. By induction every peel is correct, the residual support only shrinks, and every reported coefficient equals $X_k$, for every input with at most $K$ nonzero coefficients.

*Completeness.* A bucket holding exactly one residual frequency always passes lines L6 to L8. Call a set of frequencies a *stopping set* if every bucket of every stage contains none of them or at least two. The run ends with the residual support equal to the largest stopping set inside the support of $X$, and the flag is true exactly when that set is empty. For $d = 2$, four frequencies with residues $\{a, a'\} \times \{c, c'\}$ form a stopping set, and the tests check that the algorithm then reports nothing and the flag false. For a uniformly random support and suitable factors, Pawar and Ramchandran (2018) show that the probability of a nonempty stopping set tends to zero; that analysis is cited, not proved here.

## Complexity

Let $|S| \le T + 1 + d$ and $T = K$.

- **Samples.** $F \cdot |S| \le F (K + 1 + d)$, read once at line L2. With $d$ fixed and each $f_i$ about $c K$, this is $O(K^2)$ samples for a length $n$ of order $K^d$.
- **Line L2.** Direct DFTs of length $f_i$ for each shift: at most $|S| \sum_i f_i^2 \le |S| F^2$ multiplications and as many additions, plus the powers of $\omega_{f_i}$.
- **Peeling.** Each pass but the last peels at least one frequency, and there are at most $K$ peels, so at most $K + 1$ passes. A pass examines $F$ buckets; each costs $O(F)$ multiplications and comparisons for the lookups at line L6 (a scan of the $f_j$ powers; a hash table makes it $O(d)$) and $O(|S| + \log n)$ for line L8, which forms $\omega^{-k}$ by repeated squaring and its powers by repeated multiplication. Each peel costs $2d|S|$ multiplications and $d|S|$ subtractions.

In total $O((K + d) F (F + K + d + log n))$ additions and as many multiplications, and $O(F (K + d))$ extra space for the tables. For comparison, the FFT needs all $n$ samples and $\Theta(n \log n)$ operations. FFAST (Pawar and Ramchandran 2018) uses a constant number of shifts and FFTs for the stages, and reaches $O(K)$ samples and $O(K \log K)$ operations with high probability over random supports; it gives up the check of every peel that the $K + 1$ consecutive shifts provide here.

**Error.** *Proved:* in exact arithmetic (over $\mathbb{Z}/p\mathbb{Z}$), every reported coefficient is exact for every $K$-sparse input, and success means the whole spectrum was found. *Observed:* over $\mathbb{C}$ with $n = 124950 = 49 \cdot 50 \cdot 51$ and $K = 12$, the recovered coefficients had errors about $5 \cdot 10^{-11}$ times their size, with a relative tolerance of $10^{-7}$. No bound on rounding is proved here.

## Properties

- **Exact, deterministic and verified.** No randomness is used, and no coefficient is reported unless it is proved by the $T + 1$ consecutive shifts.
- **Sublinear.** With $n$ much larger than $F (K + d)$, only a small fraction of the samples is read.
- **Nonadaptive sampling.** The sample positions depend only on $n$, the factors and $T$, not on the signal, so they can be fixed in hardware.
- **Any field with the roots.** The same code runs over $\mathbb{C}$ and over $\mathbb{Z}/p\mathbb{Z}$ with $n \mid p - 1$.
- **Can fail.** Some supports cannot be peeled; the algorithm then returns a correct partial answer and says so.

## Variants and improvements

- **Approximately sparse signals.** The general problem asks for an approximation $\hat X$ with $\lVert X - \hat X \rVert_2 \le C \min_{k\text{-sparse } Y} \lVert X - Y \rVert_2$. Gilbert, Guha, Indyk, Muthukrishnan and Strauss (2002) gave a randomized algorithm with time polynomial in $k$, $\log n$ and $1/\epsilon$ for the $(1 + \epsilon)$ factor. Hassanieh, Indyk, Katabi and Price (2012) used filters to hash frequencies into buckets, with $O(k \log n \log(n/k))$ time for general signals and $O(k \log n)$ for exactly sparse ones.
- **Sample optimality.** Indyk and Kapralov (2014) reached $O(k \log n)$ samples for approximately sparse signals in any constant dimension.
- **Deterministic algorithms.** Iwen (2010) gave deterministic sublinear-time algorithms with a guarantee for every input.
- **Peeling with few shifts.** FFAST (Pawar and Ramchandran 2018) uses the same coprime subsampling with a constant number of shifts, and its analysis is that of peeling decoders for sparse-graph codes.
- **Boolean cube.** Kushilevitz and Mansour (1993) found the large coefficients of the [Walsh-Hadamard transform](/walsh-hadamard-transform/) of a Boolean function with queries, in time polynomial in the number of variables.
- **Prony-type methods.** With $2K$ consecutive samples, the support of a $K$-sparse spectrum is the set of roots of a polynomial found from a linear recurrence, as in [Prony's method](/prony-method/) and the [Ben-Or and Tiwari algorithm](/ben-or-tiwari-algorithm/) for sparse polynomial interpolation (1988). This needs no factorization of $n$, but it solves a dense $K \times K$ system and finds roots.

## When to use it

Use it when $n$ is very large and the spectrum is known to be sparse: spectrum sensing over wide bands, GPS acquisition, and other signals made of a few tones, as surveyed by Gilbert, Indyk, Iwen and Schmidt (2014). The exact form on this page suits exact arithmetic and settings where a wrong coefficient is worse than a missing one. When the spectrum is not sparse, or $n$ is only a modest multiple of $K^2$, an ordinary [FFT](/fast-fourier-transform/) is faster and simpler. For a few known frequencies, the [Goertzel algorithm](/goertzel-algorithm/) evaluates them directly.

## Pitfalls

- **Coprime factors.** The Chinese remainder step needs pairwise coprime factors; otherwise residues do not determine $k$.
- **Too few shifts.** With $T < K$, a bucket holding several frequencies can pass the test, and wrong coefficients appear. Keep $T \ge K$, or accept the probabilistic guarantee of FFAST.
- **Stopping sets.** Frequencies that share residues in every stage cannot be separated by peeling. Larger or more factors make this rarer, but never impossible for adversarial supports.
- **Tolerance.** Over $\mathbb{C}$ the zero tests need a tolerance relative to the signal size; too tight and singletons are missed, too loose and noise becomes coefficients.
- **Normalization.** The aliased sums carry a factor $f_i/n$; forgetting it gives coefficients off by $n/f_i$.

## Implementations

The Python implementation in [impl/python/sparse_fourier_transform.py](impl/python/sparse_fourier_transform.py) follows the main block over $\mathbb{C}$ or $\mathbb{Z}/p\mathbb{Z}$, reads samples through a function, and returns the found coefficients, the flag and the number of samples read. The tests compare it with the $O(n^2)$ DFT over $\mathbb{Z}/998244353\mathbb{Z}$ (with $n = 952$ and $1904$), $\mathbb{Z}/97\mathbb{Z}$ and $\mathbb{Z}/17\mathbb{Z}$ with exact equality, and over $\mathbb{C}$ with $n = 504$ and $n = 124950$ with a tolerance, all with fixed seeds. They cover the stopping-set failure, $n = 1$ and $2$, the zero signal, a constant, an impulse (whose flat spectrum is not sparse), a single tone, the inverse DFT of the result, and the worked example.

## History

Kushilevitz and Mansour (1993) learned decision trees by finding the large Fourier coefficients of a Boolean function from queries. Gilbert, Guha, Indyk, Muthukrishnan and Strauss (2002) gave the first algorithm for the DFT of length $n$ with time polynomial in the number of terms and $\log n$, sampling nonadaptively. Iwen (2010) gave deterministic sublinear-time algorithms. Hassanieh, Indyk, Katabi and Price (2012) gave a simpler algorithm based on filters at SODA and, at STOC, $O(k \log n)$ time for exactly $k$-sparse spectra. Pawar and Ramchandran (2018) gave FFAST, which subsamples with coprime factors, peels singleton buckets, and computes an exactly $k$-sparse DFT with $O(k)$ samples and $O(k \log k)$ operations for a uniformly random support. Gilbert, Indyk, Iwen and Schmidt (2014) survey the field.

## References
