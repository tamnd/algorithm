---
tag: VWBGTF
kind: algorithm
slug: berlekamp-massey
name: Berlekamp-Massey algorithm
aliases:
- Massey algorithm
- Berlekamp iterative algorithm
area: compression-and-coding/error-correcting-codes
level: advanced
summary: Find a shortest LFSR that generates a finite sequence over any field in O(n^2) operations. It gives the error locator in BCH and Reed-Solomon decoding.
solves: [lfsr-synthesis]
model: word-ram
complexity:
  vars: {n: the length of the sequence}
  time: {worst: Θ(n^2), average: Θ(n^2), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 1968
  people: [Elwyn R. Berlekamp, James L. Massey]
  note: Berlekamp gave the iterative decoder for BCH codes in 1968. Massey showed in 1969 that it finds a shortest linear feedback shift register for any sequence.
prereqs: [lfsr-synthesis]
see_also: [reed-solomon-decoding, peterson-gorenstein-zierler, chien-search, forney-algorithm, bch-code, linear-feedback-shift-register, polynomial-extended-euclidean-algorithm, wiedemann-algorithm]
sources:
  - paper: doi:10.1109/TIT.1969.1054260
    title: J. L. Massey, Shift-register synthesis and BCH decoding, IEEE Transactions on Information Theory 15(1), 1969
    locator: pp. 122 to 127 (the LFSR synthesis algorithm, the theorem on the length change, and its use for BCH decoding)
  - book: isbn:9789814635899
    title: Elwyn R. Berlekamp, Algebraic Coding Theory, revised edition, World Scientific, 2015 (first edition McGraw-Hill, 1968)
    locator: The chapters on the decoding of BCH codes (the iterative solution of the key equation)
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 6 (the iterative algorithm for the error-location polynomial of binary BCH codes) and Chapter 7 (the nonbinary case)
  - book: isbn:9780521845045
    title: Ron M. Roth, Introduction to Coding Theory, Cambridge University Press, 2006
    locator: Chapter 6 (decoding of Reed-Solomon codes, the key equation and the Berlekamp-Massey algorithm)
---

The Berlekamp-Massey algorithm finds a shortest [linear feedback shift register](/linear-feedback-shift-register/) (LFSR) that generates a given finite sequence $s_0, \ldots, s_{n-1}$ over any field. It reads the terms one at a time, keeps a shortest register for the prefix read so far, and corrects it with an older register each time the prediction fails. It uses $O(n^2)$ field operations. In [Reed-Solomon](/reed-solomon-decoding/) and [BCH](/bch-code/) decoding, the syndromes form such a sequence, and the shortest register is the error locator polynomial. Massey also proved that the length it finds is the linear complexity of the sequence, so the algorithm solves [LFSR synthesis](/lfsr-synthesis/) exactly.

## In plain words

You have a list of numbers, and you want the shortest rule of the form "each number is a fixed mix of the few numbers just before it" that produces the whole list. Start with the empty rule. Read the numbers one by one, and each time use the rule to predict the next number. If the prediction is right, keep the rule. If it is wrong, mix in an older rule, the one you had just before the last time the rule had to grow. The mix is chosen so that the error cancels, and the old prefix stays correct. Sometimes the rule must become longer. The algorithm knows exactly how much longer, and it never makes the rule longer than necessary.

## The problem

An LFSR of length $L$ is a pair $(L, C)$ with a connection polynomial $C(x) = 1 + c_1 x + \cdots + c_L x^L$ over a field $F$; $c_L$ may be zero. It *generates* $s_0, \ldots, s_{n-1}$ if

$$s_j + c_1 s_{j-1} + \cdots + c_L s_{j-L} = 0 \qquad \text{for } L \le j < n.$$

The first $L$ terms are free: they are the initial contents of the register. The *linear complexity* $L_n(s)$ is the smallest $L$ for which some LFSR of length $L$ generates the first $n$ terms. The problem is to find $L_n(s)$ and a connection polynomial that achieves it. See [LFSR synthesis](/lfsr-synthesis/) for the equivalent forms of the problem.

## The algorithm

The algorithm keeps the current register $(L, C)$, an older register $B$ with the nonzero discrepancy $b$ that it had when it failed, and the distance $m$ from that failure. All arithmetic is in $F$.

```pseudo id=main
BERLEKAMP-MASSEY(s_0 .. s_{n−1})          ▷ terms in a field F
L1  C(x) ← 1, B(x) ← 1, L ← 0, m ← 1, b ← 1
L2  for r ← 0 to n − 1 do
L3      d ← s_r + c_1 s_{r−1} + … + c_L s_{r−L}     ▷ the discrepancy
L4      if d = 0 then m ← m + 1
L5      else if 2L ≤ r then                   ▷ the length must grow
L6          T(x) ← C(x)
L7          C(x) ← C(x) − (d / b) x^m B(x)
L8          L ← r + 1 − L, B(x) ← T(x), b ← d, m ← 1
L9      else
L10         C(x) ← C(x) − (d / b) x^m B(x)
L11         m ← m + 1
L12 return (L, C(x))
```

Line L3 is the prediction error of the current register on the new term $s_r$. If it is zero (line L4), the register already generates $s_0, \ldots, s_r$. If not, lines L7 and L10 subtract a multiple of $x^m B(x)$. The register $B$ failed at step $r - m$ with discrepancy $b$, so the shifted copy has discrepancy $b$ at step $r$ and zero discrepancy before it, from a certain point on. The factor $d/b$ makes the two errors cancel. The new register needs length $\max(L, r + 1 - L)$. When $2L \le r$, this is $r + 1 - L > L$, so the length grows (line L8), and the old $C$ becomes the new $B$. When $2L > r$, the length stays the same.

At the start, $B = 1$ and $b = 1$ act as a register that "failed" just before $s_0$. The first nonzero term $s_r$ then gives $C = 1 - s_r x^{r+1}$ and $L = r + 1$.

**Decoding use.** For a [Reed-Solomon](/reed-solomon-code/) or BCH code with zeros $\alpha^b, \ldots, \alpha^{b+2t-1}$, let the received word have $\nu$ errors with locators $X_k = \alpha^{i_k}$ and values $Y_k$. The syndromes are $S_j = \sum_{k=1}^{\nu} Y_k X_k^{\,j}$. The error locator $\Lambda(x) = \prod_k (1 - X_k x)$ has the roots $X_k^{-1}$, so each $X_k^{\,j}$ satisfies the recurrence with connection polynomial $\Lambda$, and so does every linear combination: $\Lambda$ generates $S_b, S_{b+1}, \ldots$ with length $\nu$. If $\nu \le t$, the sequence $S_b, \ldots, S_{b+2t-1}$ has $2t \ge 2\nu$ terms, the shortest register is unique, and BERLEKAMP-MASSEY returns $\Lambda$. The [Chien search](/chien-search/) then finds its roots and the [Forney algorithm](/forney-algorithm/) the error values. If the result has $L > t$, or $\deg \Lambda \ne L$, or fewer than $L$ roots, the decoder reports a failure.

## Example

Take the binary sequence $s = 1, 0, 1, 0, 0, 1, 1, 1, 0, 1$ over $\mathrm{GF}(2)$, where $-1 = 1$.

| $r$ | $s_r$ | $d$ | lines | $L$ | $C(x)$ | $B(x)$ | $m$ |
|---|---|---|---|---|---|---|---|
| 0 | 1 | 1 | L6 to L8 | 1 | $1 + x$ | $1$ | 1 |
| 1 | 0 | 1 | L10, L11 | 1 | $1$ | $1$ | 2 |
| 2 | 1 | 1 | L6 to L8 | 2 | $1 + x^2$ | $1$ | 1 |
| 3 | 0 | 0 | L4 | 2 | $1 + x^2$ | $1$ | 2 |
| 4 | 0 | 1 | L6 to L8 | 3 | $1$ | $1 + x^2$ | 1 |
| 5 | 1 | 1 | L10, L11 | 3 | $1 + x + x^3$ | $1 + x^2$ | 2 |
| 6 to 9 | | 0 | L4 | 3 | $1 + x + x^3$ | $1 + x^2$ | 3 to 6 |

The result is $L = 3$ and $C(x) = 1 + x + x^3$: $s_j = s_{j-1} + s_{j-3}$ for $3 \le j \le 9$. The linear complexity profile is $1, 1, 2, 2, 3, 3, 3, 3, 3, 3$. At $r = 4$ the register $(3, 1)$ has $c_3 = 0$: it says nothing about $s_3$ and $s_4$ except that they are zero, which is true. Since $10 \ge 2 \cdot 3$, this shortest register is the only one.

A decoding example over $\mathrm{GF}(16)$, with $\alpha$ a root of $x^4 + x + 1$: the code RS(15, 11) with $b = 1$ and $t = 2$ receives the errors $\alpha^5$ at position 2 and $\alpha^{11}$ at position 7. The syndromes are $S_1, \ldots, S_4 = \alpha^4, \alpha^{13}, \alpha^9, \alpha^{10}$. The algorithm passes through $C = 1 + \alpha^4 x$, $1 + \alpha^9 x$, $1 + \alpha^9 x + \alpha^{11} x^2$, and ends with $L = 2$ and

$$C(x) = 1 + \alpha^{12} x + \alpha^9 x^2 = (1 - \alpha^2 x)(1 - \alpha^7 x),$$

whose inverse roots $\alpha^2$ and $\alpha^7$ give the error positions 2 and 7.

## Correctness

At the start of step $r$, $(L, C)$ is a shortest LFSR for $s_0, \ldots, s_{r-1}$, and $B$ is a shortest LFSR for an earlier prefix that failed with discrepancy $b$ exactly $m$ steps ago. The key fact is Massey's theorem: if a register of length $L$ generates $s_0, \ldots, s_{r-1}$ but not $s_r$, then every register that generates $s_0, \ldots, s_r$ has length at least $r + 1 - L$. Lines L7 and L10 build a register of length $\max(L, r + 1 - L)$ that does generate $s_0, \ldots, s_r$, so the length is optimal at each step. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

Step $r$ computes the discrepancy with $L + 1$ products and updates $C$ with at most $r + 1$ products, so the total is $O(n^2)$ field operations, and $\Theta(n^2)$ when $L$ grows with $r$, as it does for a typical sequence, where $L_r \approx r/2$. For the zero sequence each step costs $O(1)$. The space is $\Theta(n)$ for $C$, $B$ and $T$. Over $\mathrm{GF}(2^m)$ with log tables, one field operation is $O(1)$ word operations.

In decoding, $n = 2t$, so the cost is $O(t^2)$, against $O(t^3)$ for each matrix solve of the method of [Peterson, Gorenstein and Zierler](/peterson-gorenstein-zierler/), and $\Theta(t^4)$ in its worst case. Divide and conquer variants (the half-GCD form of the [extended Euclidean algorithm](/polynomial-extended-euclidean-algorithm/)) take $O(M(n) \log n)$ operations, where $M(n)$ is the cost of a polynomial product.

## Properties

- **Any field.** Only the four field operations are used. The algorithm works over $\mathrm{GF}(2)$, $\mathrm{GF}(p)$, $\mathrm{GF}(2^m)$ and the rationals.
- **Online.** Step $r$ uses only $s_0, \ldots, s_r$, so the algorithm gives the whole linear complexity profile $L_1, \ldots, L_n$ in one pass.
- **Profile rule.** At each step $L_{r+1} = L_r$ if $d = 0$, and $L_{r+1} = \max(L_r, r + 1 - L_r)$ if $d \ne 0$.
- **Unique result when $2L \le n$.** Then every shortest register is the one returned. When $2L > n$, other shortest registers can exist, and the algorithm returns one of them.

## Variants and improvements

- **Binary BCH codes.** Over $\mathrm{GF}(2^m)$ with binary errors, $S_{2j} = S_j^2$, and every second discrepancy is zero. Berlekamp's binary form skips these steps and does $t$ iterations instead of $2t$.
- **Errors and erasures.** Start with $C(x)$ and $B(x)$ equal to the erasure locator $\Gamma(x)$, and $L$ equal to the number $\rho$ of erasures. Then process the plain syndromes from $r = \rho$, with the test $2L \le r + \rho$ at L5 and $L \leftarrow r + 1 + \rho - L$ at L8. The result is $\Lambda(x)\Gamma(x)$. The other method runs the plain algorithm on the modified syndromes, the coefficients $\rho$ to $2t - 1$ of $S(x)\Gamma(x)$, and gives $\Lambda(x)$. Do not use both, because that counts the erasures twice. See [Reed-Solomon decoding](/reed-solomon-decoding/).
- **Inversion-free forms.** Burton (1971) and later authors scale $C$ and $B$ instead of dividing by $b$. This removes the field inversion from the inner loop, which is useful in hardware decoders.
- **The Euclidean form.** Sugiyama, Kasahara, Hirasawa and Namekawa (1975) solve the same key equation with the extended Euclidean algorithm on $x^{2t}$ and $S(x)$. Dornstetter (1987) showed that the two methods compute the same sequence of polynomials.
- **Other rings.** Reeds and Sloane (1985) extended the algorithm to sequences over $\mathbb{Z}/m\mathbb{Z}$.
- **Linear algebra.** The [Wiedemann algorithm](/wiedemann-algorithm/) uses Berlekamp-Massey to find the [minimal polynomial](/minimal-polynomial-computation/) of a sparse matrix from a projected Krylov sequence, and the same step finds the shortest recurrence of a [linear recurrence](/linear-recurrence-nth-term/) from its first terms.

## When to use it

Use Berlekamp-Massey to find the error locator in a BCH or Reed-Solomon decoder, where it is the standard choice in hardware and software. Use it in cryptanalysis to measure the linear complexity of a keystream: $2L$ consecutive output bits of an [LFSR-based](/lfsr/) generator with linear complexity $L$ reveal the whole stream. Use it in sparse linear algebra to find a minimal polynomial from $2n$ terms. For very long sequences, a fast half-GCD method is faster.

## Pitfalls

- **Wrong length test.** Line L5 must test $2L \le r$ with $r$ counted from 0. With $2L < r$ the length is not updated on some steps, and the register stops being shortest.
- **Forgetting to save C.** Line L6 copies $C$ before line L7 changes it. If $B$ is set to the new $C$, later corrections cancel nothing.
- **Reading $L$ from $\deg C$.** The length is the variable $L$, not the degree of $C$: $c_L$ can be zero, as at step 4 of the example. A decoder that uses $\deg \Lambda$ instead of $L$ misses the failure $\deg \Lambda < L$.
- **No failure check in decoding.** If more than $t$ errors occur, BERLEKAMP-MASSEY still returns some polynomial. The decoder must check that $L \le t$ and that $\Lambda$ has exactly $L$ distinct roots among the code positions.
- **The syndrome order.** The sequence must start with $S_b$, the syndrome of the first consecutive zero, in increasing order. A reversed sequence gives the reciprocal polynomial.

## Implementations

## History

Elwyn Berlekamp found an iterative algorithm for the error locator of BCH codes in the mid 1960s and published it in his book *Algebraic Coding Theory* in 1968. It replaced the cubic matrix method of Peterson, Gorenstein and Zierler. James Massey saw that the algorithm solves a more general problem: it synthesizes a shortest linear feedback shift register for any finite sequence over any field. In his 1969 paper he gave a short form of the algorithm, the theorem on the length change, and the proof that the result is shortest. The name Berlekamp-Massey comes from this pair of works.

## References
