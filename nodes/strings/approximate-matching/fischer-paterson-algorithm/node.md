---
tag: PNQWEP
kind: algorithm
slug: fischer-paterson-algorithm
name: Fischer-Paterson algorithm
aliases:
- FFT Hamming matching
area: strings/approximate-matching
level: advanced
summary: Computes Hamming distances at all alignments with one FFT-based convolution per alphabet symbol, in O(σ n log m) time.
solves: [hamming-string-matching, k-mismatch-problem]
model: word-ram
complexity:
  vars: {m: the pattern length, n: the text length, σ: the number of distinct symbols in the pattern}
  time: {worst: Θ(σ n log m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1974
  people: [Michael J. Fischer, Michael S. Paterson]
  note: Fischer and Paterson reduced string matching with don't cares to convolutions computed by fast multiplication. The count of agreements per symbol is the same reduction applied to Hamming distances.
prereqs: [hamming-string-matching, fast-fourier-transform, number-theoretic-transform]
see_also: [hamming-string-matching, k-mismatch-problem, amir-lewenstein-porat-algorithm, bitap-algorithm, landau-vishkin-algorithm, fast-fourier-transform, number-theoretic-transform, polynomial-multiplication]
sources:
  - paper: "Michael J. Fischer and Michael S. Paterson, String-matching and other products, in Complexity of Computation, SIAM-AMS Proceedings 7, 1974"
    locator: the reduction of string matching with don't cares to Boolean products, computed with fast integer multiplication
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 4 (the match-count problem, one indicator convolution per alphabet symbol, computed by the fast Fourier transform)
  - paper: doi:10.1137/0216067
    title: Karl Abrahamson, Generalized string matching, SIAM Journal on Computing 16(6), 1987
    locator: pages 1039 to 1051 (convolutions for the frequent symbols, which reduces the dependence on the alphabet)
---

The Fischer-Paterson algorithm computes the [Hamming distance](/hamming-distance/) between a pattern and every text window of the same length, by one convolution of 0 or 1 vectors for each symbol of the pattern. Each convolution counts, at all alignments at once, the positions where both strings hold that symbol, and the [fast Fourier transform](/fast-fourier-transform/) computes it in $O(n \log m)$ time on blocks of the text. The total is $O(\sigma\, n \log m)$ time for $\sigma$ distinct pattern symbols, which beats the direct $O(nm)$ count for small alphabets such as DNA. Fischer and Paterson introduced this reduction of string matching to convolutions in 1974, for matching with don't cares.

## In plain words

Pick one letter, say the letter a. Write a list for the pattern with a 1 where the pattern has an a and a 0 elsewhere, and the same kind of list for the text. Put the pattern list under the text list at some position and count the places where both have a 1: these are the places where both have the letter a.

Doing this for every position by hand is slow. But this count, for all positions at once, is exactly what you get when you multiply two polynomials whose coefficients are the two lists, one of them reversed. Fast multiplication of polynomials takes little more than linear time.

Repeat for each letter of the pattern and add the counts. The sum is the number of places that agree. The pattern length minus this sum is the number of places that differ.

## The problem

The input is a pattern $P = P[0 \ldots m-1]$ and a text $T = T[0 \ldots n-1]$ over an alphabet $\Sigma$. The edit model is the Hamming distance: only substitutions count. Indices are 0-based. The output is the array $h[0 \ldots n-m]$ with $h[i] = |\{ q : P[q] \ne T[i+q] \}|$, indexed by the start position $i$ of the window. A [k-mismatch](/k-mismatch-problem/) search reports the starts $i$ with $h[i] \le k$. When $m = 0$, $h$ has $n + 1$ zeros, and when $m > n$, $h$ is empty.

## The algorithm

For a symbol $c$, let $x_c[q] = [P[m-1-q] = c]$ be the reversed indicator of $c$ in $P$, and $y_c[j] = [T[j] = c]$ its indicator in $T$. The convolution $z_c = x_c * y_c$ has

$$z_c[i + m - 1] = \sum_{q=0}^{m-1} x_c[q]\, y_c[i + m - 1 - q] = \sum_{r=0}^{m-1} [P[r] = c]\,[T[i + r] = c],$$

with $r = m - 1 - q$. This is the number of positions $r$ where both $P[r]$ and $T[i + r]$ are $c$. A symbol that does not occur in $P$ adds nothing, so only the symbols of $P$ are needed.

To keep the transforms short, the text is cut into blocks $T[b \ldots b + 2m - 1)$ for $b = 0, m, 2m, \ldots$. The block at $b$ contains the windows that start at $b, \ldots, b + m - 1$, and the linear convolution of a block with $x_c$ has length at most $3m - 2$.

```pseudo id=main
FP-HAMMING(P, T)                             ▷ 1 ≤ m ≤ n; h is indexed by start positions
L1  A[0 .. n − m] ← 0                        ▷ agreements
L2  for each distinct symbol c of P do
L3      x ← the reversed indicator of c in P, padded to length N ≥ 3m − 2; X ← FFT(x)
L4      for b ← 0, m, 2m, ... while b ≤ n − m do
L5          y ← the indicator of c in T[b .. b + 2m − 1), padded to length N
L6          z ← FFT⁻¹(X · FFT(y))            ▷ the linear convolution x * y
L7          for t ← 0 to min(m, n − m + 1 − b) − 1 do A[b + t] ← A[b + t] + z[t + m − 1]
L8  return h with h[i] = m − A[i]
```

Line L3 transforms the pattern vector once per symbol. Line L6 multiplies the transforms pointwise, which gives the cyclic convolution of length $N$, and this equals the linear convolution because $N \ge 3m - 2$. Line L7 adds the counts of the windows that start in the block. The implementation computes the transforms modulo the prime $998244353$ with a [number-theoretic transform](/number-theoretic-transform/), which is exact because every count is at most $m$, below the prime. A floating-point FFT also works when it rounds the results to the nearest integer.

## Example

$P = \texttt{abc}$ and $T = \texttt{abxabcbc}$, so $m = 3$, $n = 8$, and the blocks are $T[0 \ldots 5) = \texttt{abxab}$ (windows 0 to 2) and $T[3 \ldots 8) = \texttt{abcbc}$ (windows 3 to 5).

| symbol $c$ | $x_c$ | $y_c$ on $T$ | agreements at $i = 0, \ldots, 5$ |
|---|---|---|---|
| a | 0, 0, 1 | 1, 0, 0, 1, 0, 0, 0, 0 | 1, 0, 0, 1, 0, 0 |
| b | 0, 1, 0 | 0, 1, 0, 0, 1, 0, 1, 0 | 1, 0, 0, 1, 0, 1 |
| c | 1, 0, 0 | 0, 0, 0, 0, 0, 1, 0, 1 | 0, 0, 0, 1, 0, 1 |
| sum $A$ | | | 2, 0, 0, 3, 0, 2 |

So $h = 3 - A = (1, 3, 3, 0, 3, 1)$. The exact occurrence is at $i = 3$, and the windows with at most one mismatch start at 0, 3 and 5. The symbol $\texttt{x}$ of the text does not occur in $P$ and needs no convolution.

## Correctness

By the displayed identity, $z_c[i + m - 1]$ counts the positions where $P$ and the window at $i$ both hold $c$. Each position $r$ with $P[r] = T[i + r]$ is counted for exactly one symbol, $c = P[r]$, and a position with $P[r] \ne T[i + r]$ is counted for none. So the sum over the symbols of $P$ is $m - h[i]$. The blocks cover each start $i \in \{0, \ldots, n - m\}$ exactly once, and a block contains the whole window of each of its starts. The full proof, with the exactness of the modular transform, is below.

## Complexity

A transform of length $N < 6m$ takes $O(m \log m)$ time. For each symbol of $P$, the algorithm does one transform for $x_c$ and three for each of the $\lceil (n - m + 1)/m \rceil$ blocks, so it takes $O((n/m + 1)\, m \log m) = O(n \log m)$ time per symbol, and $\Theta(\sigma\, n \log m)$ time in total for $\sigma$ distinct symbols of $P$, in the worst case and in every case. The space is $\Theta(n)$ for $A$ and $\Theta(m)$ for the vectors of one block. A single transform over the whole text instead of blocks costs $O(n \log n)$ per symbol, which is the same up to the factor $\log n / \log m$.

## Properties

- **Independent of the data.** The work does not depend on the text or on the distances, only on $n$, $m$ and $\sigma$.
- **All distances.** It gives every $h[i]$, not only the small ones, so it solves the k-mismatch problem for every $k$ at once.
- **Alphabet dependence.** The time grows with the number of distinct pattern symbols. For a large alphabet it can be slower than the direct count.
- **Offline.** Each block needs $2m - 1$ text characters before it gives results, so the method is not online.

## Variants and improvements

- **Don't cares.** Fischer and Paterson solved exact matching where a wildcard matches every symbol, with Boolean products computed by fast integer multiplication. A later simple method uses three convolutions of integer vectors: with $p_q = 0$ and $t_j = 0$ for wildcards and distinct positive integers for the other symbols, $\sum_q p_q t_{i+q} (p_q - t_{i+q})^2 = 0$ exactly at the matches.
- **Counts with don't cares.** Count the positions where both symbols are not wildcards with one more convolution, and subtract the agreements.
- **Abrahamson's split.** Use convolutions only for the symbols with more than $\sqrt{m \log m}$ occurrences in $P$ and count the rare symbols directly. This gives $O(n \sqrt{m \log m})$ time for any alphabet. See [Hamming string matching](/hamming-string-matching/).
- **Few mismatches.** For small $k$, the [Amir-Lewenstein-Porat algorithm](/amir-lewenstein-porat-algorithm/) combines convolutions with periodicity and takes $O(n \sqrt{k \log k})$ time, and the [Landau-Vishkin algorithm](/landau-vishkin-algorithm/) takes $O(nk)$ time.
- **Bit parallelism.** For a short pattern, [bitap](/bitap-algorithm/) with wide counters computes all distances in $O(n)$ word operations.

## When to use it

Use it when all Hamming distances are needed, the alphabet is small, and the pattern is long, for example DNA or binary data with $m$ in the thousands. For a short pattern, bitap is faster. For few allowed mismatches, use Landau-Vishkin or Amir-Lewenstein-Porat. For a large alphabet, use Abrahamson's split.

## Pitfalls

- **Linear versus cyclic convolution.** The transform length must be at least the length of the linear result, $3m - 2$ for a block of length $2m - 1$. A shorter transform wraps values around and gives wrong counts.
- **Rounding.** With a floating-point FFT, round each count to the nearest integer. For very long inputs the error can exceed $1/2$; a modular transform avoids this.
- **The reversal.** Convolution reverses one operand. Without the reversal of the pattern vector, the result is a correlation with the reversed pattern.
- **The offset.** The count of the window at $i$ is at index $i + m - 1$ of the block result, relative to the start of the block.
- **Symbols outside the pattern.** They add nothing, but the text indicator must be 0 there; a code that maps them to some pattern symbol gives false agreements.

## Implementations

## History

Fischer and Paterson presented "String-matching and other products" in 1974. They showed that matching with don't cares reduces to a few Boolean products of vectors, and that fast integer multiplication computes these products. The count of agreements by one convolution per symbol is the same reduction, and Gusfield presents it as the match-count problem. In 1987 Abrahamson combined convolutions for frequent symbols with direct counting for rare ones, which removed the dependence on the alphabet size.

## References
