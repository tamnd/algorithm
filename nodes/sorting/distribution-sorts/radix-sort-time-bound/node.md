---
tag: RGJHNS
kind: theorem
slug: radix-sort-time-bound
name: Radix sort running time
area: sorting/distribution-sorts
level: core
summary: LSD radix sort on d-digit keys with base b runs in Θ(d(n+b)) time and sorts correctly by stability.
prereqs: [radix-sort, counting-sort, stable-sort]
see_also: [radix-sort, counting-sort, msd-radix-sort, integer-sorting, word-ram, comparison-sort-lower-bound]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 8, Section 8.3, Radix sort, Lemma 8.3 (the Θ(d(n + k)) bound) and Lemma 8.4 (b-bit keys and r-bit digits), with the choice of r that follows
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Chapter 5, Section 5.1, String Sorts, the proposition on LSD string sort (stability and the cost proportional to W(N + R))
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.5, Sorting by Distribution (radix sorting and its running time)
---

This theorem says that [LSD radix sort](/radix-sort/) sorts $n$ keys of $d$ digits in base $b$ correctly, provided each pass uses a [stable sort](/stable-sort/), and that it takes $\Theta(d(n + b))$ time when each pass is a [counting sort](/counting-sort/). For keys of $w$ bits cut into digits of $r$ bits, the time is $\Theta(\lceil w/r \rceil (n + 2^r))$, and the best choice $r \approx \min(w, \lg n)$ gives $\Theta(n)$ for $w \le \lg n$ and $\Theta(w n / \log n)$ for larger $w$. So integers in $\{0, \ldots, n^c - 1\}$ sort in $\Theta(c\,n)$ time, below the comparison bound.

## Statement

Let $b \ge 2$ and $d \ge 1$ be integers, and let each of $n$ items have a key $x \in \{0, \ldots, b^d - 1\}$ with digits $x_t = \lfloor x / b^t \rfloor \bmod b$ for $0 \le t < d$. Let RADIX-SORT do $d$ passes, where pass $t = 0, 1, \ldots, d-1$ sorts the sequence by the digit $x_t$.

**Theorem 1 (correctness).** If the sort of each pass is stable, then after pass $d - 1$ the items are in non-decreasing order of key, and items with equal keys are in their input order.

**Theorem 2 (time).** If each pass is a counting sort with $b$ buckets, which takes $\Theta(n + b)$ time on the [word RAM](/word-ram/), then RADIX-SORT takes $\Theta(d(n + b))$ time on every input, and $\Theta(n + b)$ extra space.

**Theorem 3 (bits).** Let the keys be $w$-bit integers, $w \ge 1$, and let $1 \le r \le w$. With base $b = 2^r$ and $d = \lceil w / r \rceil$, the time is $\Theta(\lceil w / r \rceil (n + 2^r))$. For $n \ge 2$, let $\lambda = \lfloor \lg n \rfloor$.

- If $w \le \lambda$, then $r = w$ gives $\Theta(n)$ time, and no $r$ is better by more than a constant factor.
- If $w > \lambda$, then $r = \lambda$ gives $\Theta(w n / \log n)$ time, and each $r$ gives $\Omega(w n / \log n)$.

## In plain words

Sorting by the last digit, then by the one before it, and so on, works only if each pass keeps ties in the order the earlier passes gave them. Then after each pass the items are sorted by the digits seen so far, and after the last pass by the whole key. Each pass looks at every item once and at every possible digit value once, so the cost is the number of digits times the sum of the number of items and the number of digit values.

The digit size is a choice. Large digits mean few passes, but each pass must prepare one bucket for each value of a digit. The best size makes the number of buckets about equal to the number of items. With that choice, numbers up to a fixed power of the input size sort in a fixed number of passes.

## Proof

**Theorem 1.** For $0 \le t \le d$, let $x^{(t)} = x \bmod b^t$, the value of the lowest $t$ digits. We use the identity $x^{(t+1)} = x_t b^t + x^{(t)}$ with $0 \le x^{(t)} < b^t$. From it: $x^{(t+1)} < y^{(t+1)}$ if and only if $x_t < y_t$, or $x_t = y_t$ and $x^{(t)} < y^{(t)}$. Indeed, if $x_t < y_t$ then $x^{(t+1)} \le x_t b^t + b^t - 1 < y_t b^t \le y^{(t+1)}$, and if $x_t = y_t$ the difference is $x^{(t)} - y^{(t)}$.

We prove by induction on $t = 0, \ldots, d$ that after $t$ passes the sequence is sorted by $x^{(t)}$, with ties in input order. For $t = 0$, each $x^{(0)} = 0$ and nothing has moved. Assume the claim after $t$ passes, and take items $u$ before $v$ after pass $t$ (the $(t+1)$-th pass), with keys $x$ and $y$. If $x_t \ne y_t$, the pass put $u$ first, so $x_t < y_t$ and $x^{(t+1)} < y^{(t+1)}$. If $x_t = y_t$, stability says $u$ was before $v$ after $t$ passes, so $x^{(t)} \le y^{(t)}$ by the hypothesis, hence $x^{(t+1)} \le y^{(t+1)}$; if equal, then $x^{(t)} = y^{(t)}$ and $u$ came first in the input by the hypothesis. This proves the claim for $t + 1$. For $t = d$, $x^{(d)} = x$ because $x < b^d$. $\square$

**Theorem 2.** Pass $t$ computes the digit of each item in $O(1)$ time on the word RAM (a division and a remainder by $b^t$ and $b$, or a shift and a mask when $b$ is a power of 2), and runs counting sort on $n$ items with $b$ key values. Counting sort takes $\Theta(n + b)$ time on every input: it has two loops of exactly $n$ steps and two of exactly $b$ steps. So each pass takes $\Theta(n + b)$ time, and $d$ passes take $\Theta(d(n + b))$. The counting array and the output array take $\Theta(b)$ and $\Theta(n)$ space, and each pass can reuse them. $\square$

**Theorem 3.** A $w$-bit key is a $d$-digit number in base $2^r$ for $d = \lceil w / r \rceil$, since $2^{rd} \ge 2^w$. Theorem 2 gives $\Theta(\lceil w/r \rceil (n + 2^r))$. Write $f(r) = \lceil w / r \rceil (n + 2^r)$.

- *Case $w \le \lambda$.* With $r = w$, $f(w) = n + 2^w \le n + 2^{\lambda} \le 2n$. Each $r$ has $f(r) \ge n$. So $r = w$ is optimal up to a factor 2, and the time is $\Theta(n)$.
- *Case $w > \lambda$.* With $r = \lambda \ge 1$, $f(\lambda) = \lceil w / \lambda \rceil (n + 2^\lambda) \le (w/\lambda + 1) \cdot 2n \le 4 w n / \lambda$, using $1 \le w / \lambda$. Since $\lambda > \lg n - 1$ and $\lambda \ge 1$, we have $\lambda \ge (\lg n)/2$, so $f(\lambda) = O(w n / \log n)$. For the lower bound on every $r$: if $r \le \lg n$, then $f(r) \ge (w/r) n \ge w n / \lg n$. If $r > \lg n$, then $2^r > n$, and since $2^r / r$ does not decrease for $r \ge 1$ (because $2^{r+1}/(r+1) \ge 2^r / r$ if and only if $2r \ge r + 1$), $f(r) \ge (w/r) 2^r \ge w \cdot 2^{r_0} / r_0$ where $r_0 = \lceil \lg n \rceil \le r$, and $2^{r_0}/r_0 \ge n / (\lg n + 1)$. So $f(r) \ge w n / (\lg n + 1)$ for each $r$, which is $\Omega(w n / \log n)$. $\blacksquare$

## Consequences

- **Polynomial ranges.** Keys in $\{0, \ldots, n^c - 1\}$ for a constant $c \ge 1$ have $w = \lceil c \lg n \rceil$ bits. Base $b = n$ gives $d = c$ passes (rounding $n$ up to a power of 2 adds a constant), so the time is $\Theta(c\,n) = \Theta(n)$. For example, $n$ integers below $n^3$ sort in three passes of counting sort with $n$ buckets. This is the basic linear-time result for [integer sorting](/integer-sorting/).
- **The word size matters.** For $w = 64$ and $n = 10^6$, $\lambda = 19$; the formula $\lceil 64/r \rceil (n + 2^r)$ is $8\,002\,048$ for $r = 8$, $4\,262\,144$ for $r = 16$ and $6\,097\,152$ for $r = 19$. So $r = \lambda$ is optimal only up to a constant factor, and the exact best $r$ comes from the formula.
- **Strings of fixed length.** $n$ strings of length $W$ over an alphabet of size $R$ sort in $\Theta(W(n + R))$ time, the form in Sedgewick and Wayne.
- **Variable length.** For keys of different lengths, LSD needs padding to the longest key. [MSD radix sort](/msd-radix-sort/) and the method of the problem [sorting variable-length items](/sorting-variable-length-items/) avoid this cost.

## Tightness

- **Stability is necessary.** With an unstable digit sort, Theorem 1 fails: for the keys $[12, 11]$ in base 10, the first pass gives $[11, 12]$, and a second pass on the tens digit that reverses ties gives $[12, 11]$, which is not sorted.
- **The time bound is exact for the algorithm.** Each pass of counting sort does exactly $n$ steps in two loops and $b$ steps in two loops, for every input, so the bound $\Theta(d(n + b))$ is also a lower bound on the time of this algorithm on each input, not only in the worst case.
- **The choice of $r$ in Theorem 3 is optimal** up to a constant factor, as the lower bound for every $r$ shows. The bound $\Theta(w n/\log n)$ is not the best possible for integer sorting on the word RAM: for $w$ much larger than $\log n$, faster methods exist, see [integer sorting](/integer-sorting/).

## History

CLRS state the two lemmas of Section 8.3 in this form and derive the choice $r = \lfloor \lg n \rfloor$. The use of a stable sort per digit and the analysis of radix sorting with counting go back at least to the methods discussed by Knuth in Section 5.2.5.

## References
