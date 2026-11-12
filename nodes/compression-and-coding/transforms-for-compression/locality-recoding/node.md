---
tag: K1G2D0
kind: problem
slug: locality-recoding
name: Recoding for locality
aliases:
- locality-preserving recoding
area: compression-and-coding/transforms-for-compression
level: core
summary: Map a sequence online and invertibly to integers that are small when a symbol was used recently, so that a later coder gains from local repetition.
prereqs: [move-to-front-transform]
see_also: [burrows-wheeler-transform, reuse-distance, mattson-stack-algorithm, fenwick-tree, elias-delta-coding, list-update-problem, locality-of-reference, adaptive-modeling]
sources:
  - paper: doi:10.1109/TIT.1987.1057262
    title: Peter Elias, Interval and recency rank source coding, two on-line adaptive variable-length schemes, IEEE Transactions on Information Theory 33(1), 1987
    locator: pages 3 to 10 (interval coding and recency rank coding, and their expected code lengths for stationary sources)
  - paper: doi:10.1145/5684.5688
    title: Jon Louis Bentley, Daniel D. Sleator, Robert E. Tarjan and Victor K. Wei, A locally adaptive data compression scheme, Communications of the ACM 29(4), 1986
    locator: pages 320 to 330 (the move-to-front scheme and its bounds in terms of symbol frequencies)
  - paper: "Ziya Arnavut and Spyros S. Magliveras, Block sorting and compression, Proceedings of the Data Compression Conference (DCC 1997), IEEE, 1997"
    title: Arnavut and Magliveras, Block sorting and compression
    locator: inversion frequencies as a replacement for move-to-front after the Burrows-Wheeler transform (exact pages not checked)
  - paper: "R. L. Mattson, J. Gecsei, D. R. Slutz and I. L. Traiger, Evaluation techniques for storage hierarchies, IBM Systems Journal 9(2), 1970"
    title: Mattson, Gecsei, Slutz and Traiger 1970
    locator: the LRU stack distance of a reference string (exact pages not checked)
---

Recoding for locality is the problem of mapping a sequence of symbols, online and invertibly, to a sequence of integers that are small when the current symbol was used a short time ago. The recoded sequence has the same length and carries the same information, but its values follow a distribution that a simple coder handles well when the input has local repetition. The two classic solutions are the *recency rank* (the [move-to-front transform](/move-to-front-transform/)), which counts the distinct symbols since the last use, and the *interval*, which counts all steps since the last use. Elias (1987) analyzed both. The name "recoding for locality" is a label used on this site; the literature has no fixed name for the problem as a whole, and the methods are usually described one by one, most often as the second stage of a [Burrows-Wheeler](/burrows-wheeler-transform/) compressor.

## In plain words

Many kinds of data use the same few things again and again within a short stretch, then move on to other things. A count of how often each thing occurs overall misses this.

So instead of writing each symbol, write how long ago you last saw it. You can count the steps back, or you can count how many different symbols came in between. Either way, a symbol you just saw gets a small number, and one you have not seen for a long time gets a big number.

The receiver keeps what it has decoded so far, so it can always look back and find which symbol you meant. The numbers then go to a coder that makes small numbers short.

## Definition

**Input.** A sequence $X = X[0 \ldots n-1]$ over an alphabet $\Sigma$ of $\sigma$ symbols, and an order $A[0 \ldots \sigma-1]$ of $\Sigma$ known to both sides.

**Virtual prefix.** Before time 0, the symbols $A[\sigma-1], \ldots, A[1], A[0]$ are used at the times $-\sigma, \ldots, -2, -1$, so each symbol has a last use. Let $\mathrm{last}_t(x)$ be the time of the last use of $x$ before time $t$.

**Output.** A sequence $Y = Y[0 \ldots n-1]$ of nonnegative integers such that:

- $Y[t]$ depends only on $X[0 \ldots t]$ (the map is online), and $X[t]$ can be found from $Y[0 \ldots t]$ (the map is invertible symbol by symbol);
- $Y[t]$ is small when $t - \mathrm{last}_t(X[t])$ is small.

The two standard choices are the **interval** $Y[t] = t - \mathrm{last}_t(X[t]) \ge 1$ and the **recency rank** $Y[t] = $ the number of distinct symbols used at the times $\mathrm{last}_t(X[t]) + 1, \ldots, t - 1$, which is in $\{0, \ldots, \sigma - 1\}$.

## Variants

- **Online or by block.** The interval and the recency rank are online. Inversion frequencies need the whole block, because they are grouped by symbol.
- **What counts as recent.** Some methods count steps, some count distinct symbols, and some order the symbols by recent counts, as in the weighted frequency count used after the BWT.
- **Without a virtual prefix.** The encoder can instead send each new symbol with an escape code the first time it occurs. The virtual prefix makes the first use cost at most about $\log \sigma$ bits and removes the special case.

## Examples

Take $X = \texttt{abracadabra}$ and $A = a, b, c, d, r$, so the virtual prefix is $r, d, c, b, a$ at the times $-5$ to $-1$.

| $t$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $X[t]$ | a | b | r | a | c | a | d | a | b | r | a |
| interval | 1 | 3 | 7 | 3 | 7 | 2 | 10 | 2 | 7 | 7 | 3 |
| recency rank | 0 | 1 | 4 | 2 | 3 | 1 | 4 | 1 | 4 | 4 | 2 |

At $t = 6$, the last use of `d` is at time $-4$, so the interval is $6 - (-4) = 10$. In between, the four distinct symbols `a`, `b`, `r`, `c` are used, so the recency rank is 4. In every column, the rank plus one is at most the interval.

**Inversion frequencies.** For each symbol in the order of $A$, and for each of its uses, count the symbols larger than it since its previous use (or since the start). For `abracadabra` this gives $a: 0, 2, 1, 1, 2$; $b: 0, 3$; $c: 1$; $d: 1$; $r: 0, 0$. The decoder places the symbols from the largest down, each into the gaps between the symbols already placed.

## Known algorithms

```pseudo id=main
INTERVAL-ENCODE(X[0 .. n − 1], A[0 .. σ − 1])
L1  last[A[k]] ← −1 − k for each k                  ▷ the virtual prefix
L2  for t ← 0 to n − 1 do
L3      Y[t] ← t − last[X[t]]
L4      last[X[t]] ← t
L5  return Y
```

The decoder keeps the decoded history $H$ with the virtual prefix in front, and sets $X[t] = H[t - Y[t]]$. With a hash map for $\mathrm{last}$, both directions take $O(1)$ expected time per symbol.

- **Interval coding** (Elias, 1987): the method above. It needs no list, but the values can be as large as $n + \sigma$.
- **Recency rank coding, or move-to-front** (Ryabko, 1980; Bentley, Sleator, Tarjan and Wei, 1986; Elias, 1987): see the [move-to-front transform](/move-to-front-transform/). With a list in an array, a step costs $O(1 + Y[t])$. With a [Fenwick tree](/fenwick-tree/) over the times that marks the last use of each symbol, the rank is the number of marks after $\mathrm{last}_t(X[t])$, which one prefix sum gives, so each step takes $O(\log(n + \sigma))$ time.
- **Inversion frequencies** (Arnavut and Magliveras, 1997): as in the example. The decoder must know the number of uses of each symbol.
- **Ordering by counts.** Frequency count and weighted frequency count keep the list in the order of (recent, weighted) counts instead of last use.

## Bounds

- **Rank and interval.** For every $t$, $Y_{\mathrm{rank}}[t] + 1 \le Y_{\mathrm{interval}}[t]$: at most $t - \mathrm{last}_t(x) - 1$ symbols are used strictly between the two uses, and they include each distinct one. So with any code whose length grows with the value, the recency rank never costs more than the interval.
- **Against the order-0 entropy.** Code each value $v$ with the [Elias delta code](/elias-delta-coding/) of $v$ (interval) or $v + 1$ (rank), at most $f(v) = 1 + \log_2 v + 2 \log_2(1 + \log_2 v)$ bits. The intervals of one symbol add up to at most $n + \sigma$, and $f$ is concave, so Jensen's inequality bounds the total by $n\,(1 + H_0 + 2 \log_2(1 + H_0))$ plus a term of order $\sigma \log \sigma$, where $H_0$ is the empirical entropy of order 0 of $X$. The proof for the rank is on the [move-to-front page](/move-to-front-transform/); Elias (1987) proves bounds of this kind for both codes.
- **Below $H_0$.** On input with locality, both codes can do much better than $H_0$: $a^{100} b^{100}$ has $H_0 = 1$ bit per symbol, but all values after the first use of each symbol are 1 (interval) or 0 (rank).
- **No gain on random data.** If $X$ is uniform and independent, no invertible recoding lowers the expected code length below $\log_2 \sigma$ bits per symbol, by the source coding theorem.

## Reductions

- **To counting distinct elements in a range.** The recency rank at $t$ is the number of distinct symbols used strictly between the times $\mathrm{last}_t(X[t])$ and $t$, with the virtual prefix included. Any structure that answers this query, such as the Fenwick tree method above, computes the recency ranks.
- **The same quantity in caching.** The recency rank is the [reuse distance](/reuse-distance/), or LRU stack distance, of Mattson, Gecsei, Slutz and Traiger (1970): an access hits in an LRU cache of size $k$ if and only if its rank is less than $k$. The [Mattson stack algorithm](/mattson-stack-algorithm/) is the move-to-front list.
- **To list update.** The recency rank is the access cost of the [move-to-front heuristic](/move-to-front-heuristic/) in the [list update problem](/list-update-problem/), less one.

## Applications

- **Block-sorting compression.** After the BWT, the output has runs and local repetition. A recoding step (MTF in bzip2, or inversion frequencies, or a weighted frequency count) turns it into mostly small numbers for the entropy coder.
- **Adaptive coding of sources with memory.** Elias proposed interval and recency rank coding as universal schemes that adapt to the source online without counts.
- **Cache analysis.** The histogram of the recency ranks of a memory trace gives the miss ratio of an LRU cache of each size in one pass.

## References
