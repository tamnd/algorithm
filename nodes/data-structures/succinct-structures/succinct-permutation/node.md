---
tag: EAVGSD
kind: data-structure
slug: succinct-permutation
name: Succinct permutation representation
aliases:
- succinct permutation
area: data-structures/succinct-structures
level: research
summary: A representation of a permutation in about n log n bits that supports both pi and its inverse quickly.
model: word-ram
complexity:
  vars: {n: the number of elements, t: the shortcut spacing}
  time: {apply: O(1), inverse: O(t), build: O(n)}
  space: {total: "n log n + O((n / t) log n + n)"}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 2003
  people: [J. Ian Munro, Rajeev Raman, Venkatesh Raman, S. Srinivasa Rao]
  note: Munro, Raman, Raman and Rao introduced the shortcut representation at ICALP 2003, with pi in O(1) time and its inverse in O(1/epsilon) time in (1 + epsilon) n lg n + O(n) bits; the journal version appeared in Theoretical Computer Science in 2012.
prereqs: [permutation, permutation-cycles, rank-select-dictionary]
see_also: [permutation-inverse, succinct-data-structures, wavelet-tree, static-sequence, compressed-data-structure, patrascu-succinct-lower-bound, bit-vector, cell-probe-model]
sources:
  - paper: doi:10.1016/j.tcs.2012.03.005
    title: J. Ian Munro, Rajeev Raman, Venkatesh Raman and S. Srinivasa Rao, Succinct representations of permutations and functions, Theoretical Computer Science 438, 2012, 74-88
    locator: the shortcut method for pi and its inverse, and the representation of arbitrary powers via the cycle decomposition
  - paper: doi:10.1007/3-540-45061-0_29
    title: J. Ian Munro, Rajeev Raman, Venkatesh Raman and S. Srinivasa Rao, Succinct representations of permutations, Automata, Languages and Programming (ICALP 2003), LNCS 2719, 345-356
    locator: the conference version of the shortcut method
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, A Practical Approach, Cambridge University Press, 2016
    locator: Chapter 5 (Permutations), Section 5.1 (Inverse Permutations), the shortcut method and its space-time trade-off
  - paper: "Alexander Golynski, Cell probe lower bounds for succinct data structures, Proceedings of the 20th ACM-SIAM Symposium on Discrete Algorithms (SODA 2009), 625-634"
    locator: the lower bound showing that the trade-off between the redundancy and the time of the inverse is optimal for representations that store pi in plain form
---

A succinct permutation representation stores a [permutation](/permutation/) $\pi$ of $\{0, \ldots, n-1\}$ so that both $\pi(i)$ and the [inverse](/permutation-inverse/) $\pi^{-1}(i)$ are fast, in little more than the $\lg n! = n \lg n - O(n)$ bits that any representation needs. Storing $\pi$ and $\pi^{-1}$ as two arrays doubles the space to $2n \lg n$ bits. The shortcut method of Munro, Raman, Raman and Rao keeps only the array of $\pi$ and adds, on every [cycle](/permutation-cycles/) longer than $t$, a back pointer at every $t$-th element. Then $\pi^{-1}(i)$ is found by walking the cycle of $i$ for at most $2t + 1$ steps, in $n \lg n + O((n / t) \lg n + n)$ bits. With $t = 1/\varepsilon$ this is $(1 + \varepsilon) n \lg n + O(n)$ bits, $O(1)$ time for $\pi$ and $O(1/\varepsilon)$ time for $\pi^{-1}$, and Golynski proved this trade-off optimal. Succinct permutations appear inside text indexes, inverted indexes and representations of functions and graphs.

## In plain words

A permutation is a shuffle: it tells, for each position, where its item goes. Going forward is a lookup in the list. Going backward, from where an item ended up to where it came from, normally needs a second list of the same size.

Every shuffle breaks into loops: follow where 0 goes, then where that goes, and you come back to 0. To go backward from an item, you can walk forward around its loop until you come back to just before it. On a long loop that is slow, so plant signposts: every few steps along a long loop, write down which signpost lies a fixed number of steps behind. Then walk forward to the next signpost, jump back one signpost, and walk forward to the item. The walk is short and the signposts take little room.

## The abstract type

A fixed permutation $\pi$ of $[n] = \{0, \ldots, n-1\}$ with `apply(i)` $= \pi(i)$ and `inverse(i)` $= \pi^{-1}(i)$. The general form, $\pi^k(i)$ for any integer $k$, is treated under Variants.

## Representation

Let $t \ge 1$ be the spacing.

- $\Pi[0..n-1]$: the array of $\pi$, $n \lceil \lg n \rceil$ bits.
- For each cycle $(c_0, c_1, \ldots, c_{L-1})$ of $\pi$, with $c_{k+1} = \pi(c_k)$ and $L > t$: the elements $c_0, c_t, c_{2t}, \ldots$ are *marked*, and each marked $c_{qt}$ gets the shortcut $\text{back}(c_{qt}) = c_{(q-1)t}$, with $c_0$ pointing to the last marked element of its cycle. Cycles of length at most $t$ get no marks.
- $B[0..n-1]$: a [bit vector](/bit-vector/) with $B[x] = 1$ when $x$ is marked, with a [rank](/rank-select-dictionary/) index.
- $S$: the shortcuts, with $S[\text{rank}_1(B, x)] = \text{back}(x)$ for each marked $x$.

The invariant: on every cycle longer than $t$, going forward from any element reaches a marked element within $t$ steps, and the shortcut of a marked element points at most $t$ steps back along the cycle, to the previous marked element.

## Operations

```pseudo id=main
INVERSE(i)
L1  j ← i;  jumped ← false
L2  while Π[j] ≠ i do
L3      if B[j] = 1 and not jumped then j ← S[RANK1(B, j)];  jumped ← true
L4      else j ← Π[j]
L5  return j

APPLY(i)
    return Π[i]
```

**Inverse.** The walk follows the cycle of $i$ forward. If the cycle has length at most $t$, it comes back to the predecessor of $i$ within $t$ steps, and line L2 stops there. On a longer cycle, it meets a marked element $j$ within $t$ steps, unless it finds the predecessor first. The shortcut of $j$ leads to the previous mark, which lies before $i$ on the cycle and at most $t$ steps behind it, so walking forward from there reaches the predecessor of $i$ within $t$ more steps. The flag `jumped` makes sure that only one shortcut is taken.

**Build.** One pass over the cycles, marking every $t$-th element and recording the shortcuts, takes $O(n)$ time.

## Example

Let $n = 11$ and

| $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $\pi(i)$ | 3 | 5 | 7 | 6 | 0 | 2 | 1 | 4 | 8 | 10 | 9 |

The cycles are $(0\ 3\ 6\ 1\ 5\ 2\ 7\ 4)$ of length 8, the fixed point $(8)$ and $(9\ 10)$. With $t = 3$, only the first cycle is long. Its elements at cycle indices 0, 3 and 6 are $0$, $1$ and $7$, which are marked, with shortcuts $\text{back}(0) = 7$, $\text{back}(1) = 0$ and $\text{back}(7) = 1$. So $B = 11000001000$ and $S = [7, 0, 1]$, in the order of the marked positions 0, 1, 7.

INVERSE$(2)$:

- $j = 2$: $\Pi[2] = 7 \ne 2$, and 2 is not marked, so $j \leftarrow 7$.
- $j = 7$: $\Pi[7] = 4 \ne 2$, and 7 is marked, so $j \leftarrow S[\text{rank}_1(B, 7)] = S[2] = 1$.
- $j = 1$: $\Pi[1] = 5 \ne 2$; 1 is marked, but a shortcut was already used, so $j \leftarrow 5$.
- $j = 5$: $\Pi[5] = 2$, so $\pi^{-1}(2) = 5$.

Four reads of $\Pi$ replace the seven forward steps of a plain walk around the cycle. INVERSE$(9)$ on the short cycle reads $\Pi[9] = 10$ and $\Pi[10] = 9$ and returns 10.

## Correctness

The walk only ever moves along the cycle of $i$, forward by $\Pi$ or backward by a shortcut, so the loop can only stop at the predecessor of $i$, which is $\pi^{-1}(i)$. The proof bounds the number of steps by $2t + 1$, using the spacing of the marks. See [the proof of correctness](proofs/correctness.md).

## Complexity

| operation | time | reads of $\Pi$ |
|---|---|---|
| apply | $O(1)$ | 1 |
| inverse | $O(t)$ | at most $2t + 1$ |
| build | $O(n)$ | $n$ |

**Space.** A cycle of length $L > t$ has $\lceil L / t \rceil \le L / t + 1$ marks, and long cycles number at most $n / (t + 1)$, so there are at most $n/t + n/(t+1) < 2n/t$ shortcuts of $\lceil \lg n \rceil$ bits. With $B$ and its rank index, the total is $n \lceil \lg n \rceil + O((n / t) \lg n) + n + o(n)$ bits; a sharper placement of marks brings the shortcut count down to $n / t$. For $t = \lceil 1 / \varepsilon \rceil$ the space is $(1 + \varepsilon) n \lg n + O(n)$.

**Lower bound.** Golynski showed that if $\pi$ is stored as a plain array and $\pi^{-1}$ is computed with $t$ probes, the extra space must be $\Omega((n / t) \lg n)$ bits, for $t$ up to about $\lg n / \lg \lg n$; so the shortcut method is optimal in that range, up to constant factors.

## Variants

- **Arbitrary powers.** Munro et al. also store $\pi$ through its cycle decomposition: a bit vector marks the cycle starts in a permuted order, and then $\pi^k(i)$ for any integer $k$ takes $O(\lg n / \lg \lg n)$ time in $n \lg n + o(n \lg n)$ bits.
- **Functions.** A function $f : [n] \to [n]$ is a set of trees hanging from cycles. Munro et al. combine a succinct tree for the trees with a succinct permutation for the cycles, and answer $f^k(i)$, and list the elements of $f^{-k}(i)$, in time close to optimal, in $n \lg n + O(n)$-type space.
- **Compressible permutations.** Barbay and Navarro compress permutations with few ascending runs, using a wavelet-tree-like merge structure, to about $n H$ bits, where $H$ is the entropy of the run lengths, with both $\pi$ and $\pi^{-1}$ in $O(\lg \rho)$ time for $\rho$ runs.
- **As a sequence.** A permutation is a sequence over the alphabet $[n]$ where each symbol occurs once; a [wavelet tree](/wavelet-tree/) gives $\pi$ and $\pi^{-1}$ as access and select in $O(\lg n)$ time in $n \lg n + o(n \lg n)$ bits.
- **Sampling in compressed suffix arrays.** A compressed suffix array samples the suffix array and its inverse at regular steps and walks the $\Psi$ function between samples, the same walk-to-a-sample idea.

## When to use it

Use the shortcut method when a permutation is large, both directions are needed, and the second array would not fit: document reorderings in inverted indexes, node renumberings of compressed graphs, the suffix array and its inverse, and reversible mappings between two orders of the same items. With $t$ between 4 and 16, the inverse costs a few cache misses more than a lookup and the extra space is 6 to 25 percent of the array.

## Pitfalls

- **One shortcut only.** After a jump, the walk passes over the mark it jumped to; taking a second shortcut there can loop forever, going back and forth between two marks.
- **The wrap of a cycle.** The first mark of a cycle points to the last mark, which may be fewer than $t$ steps behind; the bound $2t + 1$ still holds, but a version that assumes exactly $t$ steps between marks miscounts.
- **Short cycles.** Cycles of length at most $t$ need no marks; marking them wastes space, and skipping marks on longer cycles breaks the time bound.
- **Shortcuts in rank order.** $S$ is indexed by the rank of the marked element in $B$, not by the element or by its position on the cycle.
- **Random access cost.** Each step is a random access into $\Pi$; on large inputs the time is dominated by cache misses, about $t$ to $2t$ of them per inverse.

## Implementations

## History

Munro, Raman, Raman and Rao presented the shortcut representation, together with the representation of arbitrary powers and of functions, at ICALP 2003; the journal version appeared in Theoretical Computer Science in 2012. Golynski proved the matching cell-probe lower bound at SODA 2009. Barbay and Navarro introduced compressed representations of permutations with few runs in 2009.

## References
