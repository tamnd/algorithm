---
tag: YG3XV5
kind: theorem
slug: fredman-saks-partial-sums-lower-bound
name: Fredman-Saks lower bound for partial sums
aliases:
- Fredman-Saks cell-probe lower bound
- partial sums lower bound
area: sequences/prefix-sums-and-differences
level: research
summary: In the cell-probe model, any dynamic partial-sums structure needs Omega(log n / log log n) time per operation.
prereqs: [partial-sums-problem, cell-probe-model]
see_also: [fredman-saks-lower-bound, dynamic-partial-sums-lower-bound, cell-probe-lower-bound, fenwick-tree, shannon-entropy, source-coding-theorem, binary-entropy-function, union-find-lower-bound]
sources:
  - paper: doi:10.1145/73007.73040
    title: "Michael L. Fredman and Michael E. Saks, The cell probe complexity of dynamic data structures, Proceedings of the 21st Annual ACM Symposium on Theory of Computing (STOC 1989), 345-354"
    locator: the chronogram method and the lower bound for partial sums modulo 2 (prefix parity), with the bounds for list indexing and subset rank
  - paper: doi:10.1145/322290.322305
    title: "Michael L. Fredman, The Complexity of Maintaining an Array and Computing Its Partial Sums, Journal of the ACM 29(1) (1982), 250-260"
    locator: the earlier logarithmic bound in the group model
  - paper: doi:10.1137/S0097539705447256
    title: "Mihai Patrascu and Erik D. Demaine, Logarithmic Lower Bounds in the Cell-Probe Model, SIAM Journal on Computing 35(4) (2006), 932-963"
    locator: Section 2.1 (the tight bound Theta(log n / log(b/delta)) for delta-bit values) and Section 3 (the chronogram method and its limit)
  - paper: "Peter Bro Miltersen, Cell probe complexity - a survey, Advances in Data Structures Workshop, FSTTCS 1999"
    locator: the section on dynamic problems and the chronogram method
---

The Fredman-Saks lower bound for partial sums says that a data structure which keeps $n$ bits under flips and answers the parity of any prefix must probe $\Omega(\log n / \log(b\, t_u))$ memory cells per query, where $b$ is the cell size in bits and $t_u$ is the cost of an update. With words of $\Theta(\log n)$ bits this gives $\Omega(\log n / \log \log n)$ time per operation for the [partial sums problem](/partial-sums-problem/), and the bound is tight for one-bit values. It was proved by Michael Fredman and Michael Saks in 1989 with the *chronogram method*, the first general technique for lower bounds on dynamic data structures in the [cell-probe model](/cell-probe-model/). This page proves the parity case, which needs a sharper count than the case of many-bit values on the page [Fredman-Saks lower bound](/fredman-saks-lower-bound/).

## Statement

**Problem.** Prefix parity on $n$ bits: an array $A[1..n]$ over $\mathbb{Z}/2$, all zero at the start. $\textsc{update}(k, v)$ adds $v \in \{0, 1\}$ to $A[k]$ modulo $2$, and $\textsc{sum}(x)$ returns $A[1] + \dots + A[x] \bmod 2$.

**Model.** A deterministic cell-probe structure with cells of $b \ge 1$ bits and at most $2^b$ cells. An operation is a decision tree that reads and writes cells, and its cost is the number of probes. Every update costs at most $t_u \ge 1$ probes.

**Theorem.** Let $\beta$ be the least power of $2$ that is at least $\max(64\, t_u b,\ 1024)$, and let $n = \beta^K$ for an integer $K \ge 1$. Then there is a sequence of fewer than $2n$ updates after which the average cost of $\textsc{sum}(x)$, over $x$ chosen uniformly from $\{1, \dots, n\}$ and with each query run on the memory left by the updates, is greater than

$$\frac{K}{8} = \frac{\lg n}{8 \lg \beta}.$$

**Corollary.** If $b = \Theta(\log n)$ and $t_u = (\log n)^{O(1)}$, then $\lg \beta = O(\log \log n)$, so queries cost $\Omega(\log n / \log \log n)$ on average. Hence every structure has $\max(t_u, t_q) = \Omega(\log n / \log \log n)$, and so does every structure for partial sums over $\mathbb{Z}/2^{\delta}$ or over the integers, since the low bit of an integer prefix sum is the prefix parity.

Fredman and Saks proved the bound also for amortized costs. The proof below is for worst-case updates, which keeps it short.

## In plain words

Do many bit flips, then ask for the parity of a random front part of the array. Group the flips into eras, looking back in time from the question: a short recent era, an older era many times longer, an even older era many times longer again, and so on.

All the eras after a given era wrote only a few cells, far fewer than the number of flips in that era. Suppose the questions could mostly avoid the cells that the era wrote. Then the few later cells plus a short list of exceptions would be enough to rebuild every flip of the era. But random flips cannot be squeezed into fewer bits than their number. So a random question must read a cell from that era with a fair chance. This holds for every era at once, and the eras are many, so a question reads many cells.

## Proof

**The update sequence.** For $i = K, K - 1, \dots, 1$, in this order, do *epoch* $i$: $N_i = \beta^i$ updates at the positions $j\, n / \beta^i$ for $j = 1, \dots, N_i$, with values $v^{(i)}_1, \dots, v^{(i)}_{N_i}$ that are independent and uniform in $\{0, 1\}$. There are $\sum_i \beta^i < 2n$ updates. Epoch $1$ is the last one. Every probe of a query that reads a cell, which the query has not itself written before, sees a value whose last write by an update lies in at most one epoch. Call the read *bad for epoch $i$* if that last write was in epoch $i$, and call the query bad for epoch $i$ if it makes such a read. A query that is bad for $r$ epochs probes at least $r$ cells. So it is enough to prove, for each $i$, that a uniform random query is bad for epoch $i$ with probability more than $1/8$; linearity of expectation then gives an expected cost above $K/8$, and some choice of the update values reaches it.

**An encoding.** Fix $i$, fix the values of all other epochs, and fix an offset $y \in \{1, \dots, n/\beta^i\}$. Let $N = N_i$, and consider the $N$ queries $x_l = (l - 1)\, n / \beta^i + y$ for $l = 1, \dots, N$. As $y$ and $l$ vary, $x_l$ takes each value in $\{1, \dots, n\}$ once. An encoder who knows $v^{(i)}$ sends a message with these fields:

1. the number $s$ of cells written by epochs $i - 1, \dots, 1$, in $b + 1$ bits;
2. the address and final content of each of these cells, in $2bs$ bits;
3. the number $c$ of queries $x_l$ that are bad for epoch $i$, in $\lg N + 1$ bits;
4. which of the $N$ queries these are, as an index into a list of the $\binom{N}{c}$ subsets, in $\lceil \lg \binom{N}{c} \rceil$ bits;
5. the answers of the bad queries, in $c$ bits.

Each field has a length that is known from the fields before it, so the code is prefix-free.

**Decoding.** The decoder knows the structure and all epochs except $i$. It runs epochs $K, \dots, i + 1$ and gets the memory $M_0$ just before epoch $i$. It runs each good query $x_l$ and serves each read of a cell $c$ that the query has not written as follows: the sent content if $c$ is in field 2, otherwise $M_0[c]$. Since the query is good, $c$ was not last written in epoch $i$, so this is the true content, and the simulation returns the true answer. Fields 4 and 5 give the answers of the bad queries. From the answer of $\textsc{sum}(x_l)$ the decoder subtracts the part of the other epochs, which it knows, and gets $\sum_{j \,:\, j n/\beta^i \le x_l} v^{(i)}_j$. This is the prefix of length $l - 1$ of $v^{(i)}$ if $y < n/\beta^i$, or of length $l$ if $y = n/\beta^i$. The differences of consecutive prefixes give at least $N - 1$ of the bits $v^{(i)}_j$.

**Counting.** The message determines $N - 1$ independent uniform bits, so its entropy is at least $N - 1$, and by the [source coding theorem](/source-coding-theorem/) a prefix-free message has expected length at least its entropy. Epochs $i - 1, \dots, 1$ have fewer than $2\beta^{i-1}$ updates, so $s < 2 t_u \beta^{i-1}$, and field 2 has fewer than $4 t_u b \beta^{i-1} \le N/16$ bits, by $\beta \ge 64 t_u b$. Also $b + 1 \le N/64 + 1$, and $\lg N + 4 \le N/64$ because $N \ge \beta \ge 1024$. Let $g(c) = \lg \binom{N}{c} + c$. Then

$$N - 1 \le \mathbb{E}[\text{length}] \le \frac{N}{16} + \frac{N}{64} + \frac{N}{64} - 1 + \mathbb{E}[g(c)].$$

The increments $g(c+1) - g(c) = \lg \frac{N - c}{c + 1} + 1$ decrease in $c$, so $g$ is concave, and $\binom{N}{c} \le 2^{N H(c/N)}$, where $H$ is the [binary entropy function](/binary-entropy-function/). Let $p = \mathbb{E}[c]/N$. By Jensen's inequality, $\mathbb{E}[g(c)] \le N\big(H(p) + p\big)$, so $H(p) + p \ge 1 - 3/32 = 29/32 > 0.9$. The function $H(p) + p$ increases on $[0, 1/2]$ and equals $0.669$ at $p = 1/8$, so $p > 1/8$. This $p$ is the probability that a uniform $x_l$ is bad for epoch $i$, given the fixed values and $y$. Averaging over $y$ and over the other epochs, a uniform query $x$ is bad for epoch $i$ with probability more than $1/8$. $\blacksquare$

## Consequences

- **Fenwick trees are nearly optimal.** The [Fenwick tree](/fenwick-tree/) and the segment tree use $O(\log n)$ probes per operation, and no structure with words of $O(\log n)$ bits uses $o(\log n / \log \log n)$. The remaining factor of $\log \log n$ for word-sized values was closed by the [dynamic partial sums lower bound](/dynamic-partial-sums-lower-bound/) of Patrascu and Demaine.
- **A trade-off.** The theorem says $t_q \ge \lg n / (8 \lg \beta)$ with $\lg \beta \le \max(\lg(t_u b) + 7,\ 11)$. Fast queries need very slow updates: $t_q = O(1)$ forces $\lg(t_u b) = \Omega(\log n)$, that is $t_u \ge n^{\Omega(1)} / b$.
- **Related problems.** A structure for dynamic subset rank, or for list indexing, gives a prefix parity structure with at most a constant factor more probes per operation: a flip at $k$ is an insertion or a deletion, decided by two rank queries, and a parity query is a rank query modulo $2$. So these problems have the same $\Omega(\log n / \log \log n)$ bound, as Fredman and Saks showed.
- **The pattern of the method.** The proof uses only that the epochs are disjoint in time, that later epochs write few cells, and that a random query must learn a constant fraction of the information of each epoch. The same pattern gives the union-find bounds on the page [union-find lower bound](/union-find-lower-bound/).

## Tightness

**The bound is tight for parity.** Store a tree of fan-out $B = b$ over the array. Each node keeps, in one word, the prefix parities of its $B$ children. A query reads one word and extracts one bit per level. An update flips a suffix of bits in one word per level, which is one read and one write. So $t_u$ and $t_q$ are $O(\log n / \log b)$, which is $O(\log n / \log \log n)$ for $b = \Theta(\log n)$.

**The trade-off is tight too.** With fan-out $B \ge b$, a node keeps its $B$ prefix parities in $B/b$ words. A query reads one word per level, so $t_q = O(\log n / \log B)$, and an update rewrites up to $B/b$ words per level, so $t_u = O((B/b) \log n / \log B)$. Then $\lg(t_u b) = O(\log B)$ when $\log n \le B$, and $t_q \lg(t_u b) = O(\log n)$, which matches the theorem up to a constant.

**The method cannot go higher.** The epochs grow by a factor $\beta \ge t_u b$, so there are only $\log n / \log(t_u b)$ of them, and each adds a constant to the cost. For word-sized values and $t_u = O(\log n)$ this caps the method at $O(\log n / \log \log n)$. Patrascu and Demaine reached $\Omega(\log n)$ for word-sized values by a different argument, information transfer over a tree of time, in which every level of the tree contributes. For values of $\delta$ bits they proved the tight bound $\Theta(\log n / \log(b/\delta))$, which for $\delta = 1$ is the bound of this page.

**Randomization and amortization.** The proof above is for deterministic structures with worst-case updates. Fredman and Saks handle amortized costs, and the later information transfer bounds allow Las Vegas randomization as well.

## History

Fredman posed the partial sums problem in 1982 and proved a logarithmic bound in an algebraic model, in which the structure may only add and subtract stored values. In 1989 Fredman and Saks moved to the cell-probe model of Yao, in which any computation is free, and introduced the chronogram method. With it they proved $\Omega(\log n / \log \log n)$ for prefix parity, list indexing and subset rank, and the $\Omega(\alpha(m, n))$ amortized bound for union-find. Dietz gave matching structures for list indexing and subset rank in the same year. The gap between $\log n / \log \log n$ and $\log n$ for word-sized partial sums stayed open for fifteen years. Miltersen's survey of cell-probe complexity listed it as a challenge, and Patrascu and Demaine closed it in 2004.

## References
