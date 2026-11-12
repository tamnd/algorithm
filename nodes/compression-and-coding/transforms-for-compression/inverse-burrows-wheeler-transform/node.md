---
tag: 411QAF
kind: algorithm
slug: inverse-burrows-wheeler-transform
name: Inverse Burrows-Wheeler transform
aliases:
- BWT inversion
- LF-mapping decoding
area: compression-and-coding/transforms-for-compression
level: core
summary: Recover a text from its Burrows-Wheeler transform in linear time. The LF mapping, found by counting, steps from each row to the row of the previous text position.
model: word-ram
complexity:
  vars: {n: the length of the text over an integer alphabet of size at most n}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false, comparison: false}
history:
  year: 1994
  people: [Michael Burrows, David Wheeler]
  note: The reverse transform with a count of the symbols is in SRC Research Report 124 of Digital Equipment Corporation, 1994.
prereqs: [burrows-wheeler-transform, counting-sort]
see_also: [bijective-burrows-wheeler-transform, fm-index, rank-select-problem, wavelet-tree, suffix-array, move-to-front-transform]
sources:
  - paper: "Michael Burrows and David J. Wheeler, A block-sorting lossless data compression algorithm, SRC Research Report 124, Digital Equipment Corporation, Palo Alto, California, 1994"
    title: Burrows and Wheeler 1994
    locator: Section 2 (the reverse transform from the last column and the index, with the counts of the symbols)
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, A Practical Approach, Cambridge University Press, 2016
    locator: Chapter 11 (the LF mapping, the inversion of the BWT and backward search)
  - paper: "Paolo Ferragina and Giovanni Manzini, Opportunistic data structures with applications, Proceedings of the 41st Annual Symposium on Foundations of Computer Science (FOCS 2000), IEEE, 2000"
    title: Ferragina and Manzini 2000
    locator: the LF mapping computed from the counts C and rank queries on the last column, and backward search
---

The inverse Burrows-Wheeler transform recovers a text $T$ from its [Burrows-Wheeler transform](/burrows-wheeler-transform/) $L$. It uses the LF mapping: the row of the sorted rotations that ends with the $k$-th copy of a symbol $c$ goes to the row that starts with the $k$-th copy of $c$, and that row is the rotation one position earlier in the text. One pass of counting gives the mapping, and a walk of $n$ steps writes the text from right to left, so the inverse takes $\Theta(n)$ time. The same mapping, with rank queries in place of the table, is the step of backward search in the [FM-index](/fm-index/).

## In plain words

The output of the forward transform is the last column of a sorted list of the rotations of the text. If you sort that column, you get the first column. Each line of the list is a circle of the text, so the last symbol of a line comes just before its first symbol in the text.

The key fact is that equal symbols appear in the same order in both columns. The second "a" from the top in the last column is the same text position as the second "a" from the top in the first column. So from any line you can jump to the line that starts one step earlier in the text. Start at the line that begins with the end marker, read its last symbol, which is the last symbol of the text, then jump, read, jump, and so on. You get the text backwards.

## The problem

The input is $L = L[0 \ldots n]$, the BWT of $T\$$ in the sentinel convention: $L$ holds the sentinel $\$$ exactly once, and $\$$ is smaller than each other symbol. The output is the text $T[0 \ldots n-1]$ with $\mathrm{BWT}(T) = L$. In the convention without a sentinel, the input is the last column $L_{\mathrm{rot}}[0 \ldots n-1]$ and the index $I$ of a row equal to $T$; the same method works with $I$ as the start row.

**Notation.** $N = n + 1$. $F$ is $L$ in sorted order, the first column. For a symbol $c$, $C[c]$ is the number of symbols of $L$ that are smaller than $c$, and $\mathrm{rank}_c(L, i)$ is the number of occurrences of $c$ in $L[0 \ldots i-1]$. The LF mapping is

$$\mathrm{LF}(i) = C[L[i]] + \mathrm{rank}_{L[i]}(L, i), \qquad 0 \le i < N.$$

If row $i$ is the rotation that starts at text position $p$, then row $\mathrm{LF}(i)$ is the rotation that starts at $p - 1$ (modulo $N$). In suffix array terms, $SA[\mathrm{LF}(i)] = (SA[i] - 1) \bmod N$.

## The algorithm

```pseudo id=main
INVERSE-BWT(L[0 .. n])                 ▷ L holds one $, the smallest symbol
L1  count[c] ← the number of i with L[i] = c, for each symbol c
L2  C[c] ← the sum of count[d] over d < c       ▷ prefix sums in symbol order
L3  seen[c] ← 0 for each symbol c
L4  for i ← 0 to n do
L5      LF[i] ← C[L[i]] + seen[L[i]]
L6      seen[L[i]] ← seen[L[i]] + 1
L7  r ← 0                                ▷ row 0 is the rotation $T
L8  for j ← n − 1 downto 0 do
L9      T[j] ← L[r]
L10     r ← LF[r]
L11 return T
```

Lines L1 and L2 are the first two passes of [counting sort](/counting-sort/): $C[c]$ is the first row of $F$ that holds $c$. Lines L3 to L6 compute $\mathrm{LF}$: when the loop reaches row $i$, $seen[c]$ is $\mathrm{rank}_c(L, i)$. Row 0 is the rotation $\$T$, because $\$$ is the smallest symbol, and its last symbol is $T[n-1]$. Each step of lines L9 and L10 writes one symbol and moves one position to the left in the text. The loop stops after $n$ steps, before it reads the $\$$ of the row of $T\$$.

**The backward walk and the forward walk.** The walk above is *backward*: it reads $T$ from the end. The inverse permutation $\Psi = \mathrm{LF}^{-1}$ moves one position to the right, so a *forward* walk starts at the row whose last symbol is $\$$ (the row of $T\$$ itself) and outputs $F[r]$, then sets $r \leftarrow \Psi(r)$, $n$ times. It needs $\Psi$, which one more pass computes from $\mathrm{LF}$. The forward walk is useful when the text must come out in order, for example to a stream.

## Example

Invert $L = \texttt{annb\$aa}$, the BWT of `banana`. The counts are $\${:}1$, $a{:}3$, $b{:}1$, $n{:}2$, so $C[\$] = 0$, $C[a] = 1$, $C[b] = 4$, $C[n] = 5$.

| row $i$ | $L[i]$ | $\mathrm{rank}_{L[i]}(L, i)$ | $\mathrm{LF}(i)$ | $F[i]$ |
|---|---|---|---|---|
| 0 | a | 0 | 1 | \$ |
| 1 | n | 0 | 5 | a |
| 2 | n | 1 | 6 | a |
| 3 | b | 0 | 4 | a |
| 4 | \$ | 0 | 0 | b |
| 5 | a | 1 | 2 | n |
| 6 | a | 2 | 3 | n |

The walk of lines L7 to L10:

| step | $r$ | $L[r]$ | written to |
|---|---|---|---|
| 1 | 0 | a | $T[5]$ |
| 2 | 1 | n | $T[4]$ |
| 3 | 5 | a | $T[3]$ |
| 4 | 2 | n | $T[2]$ |
| 5 | 6 | a | $T[1]$ |
| 6 | 3 | b | $T[0]$ |

After step 6, $r = \mathrm{LF}(3) = 4$, the row of `banana$`, and the loop has ended. The output is $T = \texttt{banana}$. In the same way, $\texttt{ard\$rcaaaabb}$ gives `abracadabra`, and the pair $(\texttt{nnbaaa}, 3)$ of the convention without a sentinel gives `banana` when the walk starts at row 3.

## Correctness

The method rests on the *LF property*: among the rows that end with a symbol $c$, and among the rows that start with $c$, the order is the same. If row $i$ is the rotation $x c$, then $c x$ is also a rotation, and $x c < y c$ implies $c x < c y$ for two rotations of the same length. So the $k$-th row that ends with $c$ maps to the $k$-th row that starts with $c$, which is row $C[c] + k$. The invariant of the loop of line L8 is: at the start of the step for $j$, row $r$ is the rotation that starts at position $j + 1$ of $T\$$, so $L[r] = T[j]$. The full proof is below.

## Complexity

- **Time.** Lines L1 to L6 make two passes over $L$ and one pass over the alphabet: $\Theta(n + \sigma)$. The walk makes $n$ steps of $O(1)$ each. With $\sigma \le n$, the total is $\Theta(n)$ in the worst case. A version that sorts the distinct symbols instead of indexing an array by them takes $O(n + \sigma \log \sigma)$.
- **Space.** The array $\mathrm{LF}$ takes $n + 1$ words, and the counts take $\sigma$ words.
- **Memory access.** The walk visits the rows in the order of the text, which is close to random in $L$. On large blocks, most steps are cache misses, so the walk, not the counting, sets the speed in practice.

## Properties

- **Not every string is a BWT.** A string with one smallest $\$$ is the BWT of a text only if the permutation $\mathrm{LF}$ is one cycle. For example $L = \texttt{a\$b}$ gives $\mathrm{LF} = (1, 0, 2)$, with the fixed point 2. The walk of $n$ steps then outputs a string whose BWT is not $L$. A decoder of untrusted data should check that the walk ends at the row of $\$$ after exactly $n$ steps.
- **The same mapping for search.** With rank queries on $L$ in place of the array (for example a [wavelet tree](/wavelet-tree/), see the [rank and select problem](/rank-select-problem/)), $\mathrm{LF}$ needs no extra $n$ words. This is the setting of the [FM-index](/fm-index/), where backward search applies the same formula to a range of rows.
- **Partial inversion.** If the positions $SA[i]$ of some rows are stored (for example each $s$-th text position), a walk of at most $s$ steps from any row reaches a stored position. This gives random access to the text from the index.

## Variants and improvements

- **The convention without a sentinel.** Start the walk at row $I$, the row of $T$; the first symbol read is $L_{\mathrm{rot}}[I] = T[n-1]$.
- **The byte form.** Many coders store $L$ without the $\$$ and keep its row $k$ as the index. Put a code below all bytes, such as $-1$, back at row $k$, or adjust $C$ and the ranks by hand.
- **Forward output.** Compute $\Psi$ and walk forward, as above. The 1994 report computes the counts in the same way and also writes the text from the end.
- **Faster walks.** Decoders interleave several independent walks, or decode two symbols per step, to hide the cache misses. The bijective variant needs the same $\mathrm{LF}$ but walks each cycle separately; see [bijective Burrows-Wheeler transform](/bijective-burrows-wheeler-transform/).

## When to use it

Use this method in every BWT decoder. It is the standard inverse: it needs only $L$, the index, and $\Theta(n)$ words of memory. When memory is tight, rank queries on a compressed $L$ replace the $\mathrm{LF}$ array, at the cost of a slower step. When the block is decoded only for search, do not invert at all: keep $L$ in an [FM-index](/fm-index/).

## Pitfalls

- **Ranks that are not 0-based or that include row $i$.** Line L5 uses $seen[L[i]]$ before line L6 adds one. If the order is swapped, every $\mathrm{LF}$ value is one too large and the walk leaves the range.
- **A start row that is not the row of $\$T$.** Line L7 starts at row 0 because $\$$ is the smallest symbol. If the sentinel is not the smallest (for example a `$` in a text with spaces), the row of $\$T$ is not row 0, and the output is a rotation of the text, or garbage. Start at the row whose first symbol is $\$$, which is $C[\$]$.
- **Reading $F$ in the backward walk.** Line L9 reads $L[r]$. Reading $F[r]$ gives the text shifted by one position.
- **Recursion.** The walk is a loop. A recursive version has depth $n$ and fails on large blocks.
- **Trusting the input.** As shown above, a string with one $\$$ need not be a valid BWT. Check that $r$ is the row of $\$$ after the loop.

## Implementations

## History

Burrows and Wheeler gave the reverse transform together with the forward transform in their 1994 report: it counts the symbols, computes for each row the row of the previous position, and writes the text from the end. Ferragina and Manzini (FOCS 2000) used the same mapping, with rank queries on a compressed last column, to search a pattern in the transformed text without inverting it, which is the FM-index.

## References
