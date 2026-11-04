---
tag: H94MFN
kind: theorem
slug: fredman-saks-lower-bound
name: Fredman-Saks lower bound
aliases:
- cell-probe lower bound for union-find
- chronogram method
area: data-structures/disjoint-sets
level: research
summary: The chronogram method gives cell-probe lower bounds for dynamic problems, Omega(log n / log log n) for partial sums, and the union-find bounds that make Tarjan and Blum tight.
prereqs: [cell-probe-model, union-find-lower-bound, amortized-cost]
see_also: [union-find-lower-bound, cell-probe-lower-bound, dynamic-partial-sums-lower-bound, cell-probe-model, union-find-amortized-bound, blum-union-find, dynamic-connectivity-lower-bound, bit-probe-model]
sources:
  - paper: doi:10.1145/73007.73040
    title: "Michael L. Fredman and Michael E. Saks, The cell probe complexity of dynamic data structures, Proceedings of the 21st Annual ACM Symposium on Theory of Computing (1989), 345-354"
    locator: the chronogram method, the bound for partial sums modulo 2, Theorem 5 (set union, amortized) and Theorem 6 (set union, worst case)
  - paper: doi:10.1137/S0097539705447256
    title: "Mihai Patrascu and Erik D. Demaine, Logarithmic Lower Bounds in the Cell-Probe Model, SIAM Journal on Computing 35(4) (2006), 932-963"
    locator: Section 3 (previous work and the limits of the chronogram method)
  - paper: doi:10.1145/2213977.2213987
    title: "Kasper Green Larsen, The cell probe complexity of dynamic range counting, Proceedings of the 44th Annual ACM Symposium on Theory of Computing (STOC 2012), 85-94"
    locator: the chronogram method combined with cell sampling
  - paper: doi:10.1137/0215072
    title: "Norbert Blum, On the Single-Operation Worst-Case Time Complexity of the Disjoint Set Union Problem, SIAM Journal on Computing 15(4) (1986), 1021-1024"
    locator: the matching upper bound for the worst case of one union-find operation
---

The Fredman-Saks lower bound is the result of a 1989 paper that founded the study of lower bounds for *dynamic* data structures in the [cell-probe model](/cell-probe-model/). Its tool, the *chronogram method*, splits the past updates into epochs that grow geometrically backwards in time, and shows that a query must read a cell written in each epoch, because the cells written later are too few to hold the information of that epoch. This gives $\Omega(\log n/\log\log n)$ per operation for dynamic partial sums and prefix parity with words of $O(\log n)$ bits. The same paper proves that union-find needs $\Omega(\alpha(m, n))$ amortized time per operation, which makes [Tarjan's bound](/union-find-amortized-bound/) tight, and $\Omega(\log n/\log\log n)$ for the worst single operation, which makes [Blum's structure](/blum-union-find/) tight. This page states the general method and proves its basic form. The union-find theorem, its proof and its history are on the page of the [union-find lower bound](/union-find-lower-bound/).

## Statement

**Model.** The [cell-probe model](/cell-probe-model/) with cells of $b$ bits and at most $2^b$ cells, so that an address fits in one cell. The cost of an operation is the number of cells it reads or writes; all computation is free.

**Theorem 1 (chronogram bound, explicit form).** Consider dynamic partial sums over $\mathbb{Z}/2^\delta$ on $n$ entries: `update(k, Δ)` adds $\Delta$ to $A[k]$, and `sum(k)` returns $A[1] + \cdots + A[k]$. Let $4 \le \delta \le b$. Suppose every update probes at most $t_u \ge 1$ cells, in the worst case. Let $\beta$ be the least power of 2 that is at least $32\,t_u b/\delta$, and suppose $n = \beta^K$ for an integer $K \ge 1$. Then there is a sequence of updates after which the average cost of `sum(x)`, over a uniformly random $x \in \{1, \ldots, n\}$, is at least

$$\frac{K}{2} = \frac{\lg n}{2 \lg \beta} \ \ge\ \frac{\lg n}{2\,(6 + \lg(t_u b/\delta))}.$$

For $\delta = b = \Theta(\log n)$ this says that $t_q = \Omega(\log n/\log t_u)$, so $\max(t_u, t_q) = \Omega(\log n/\log\log n)$.

**Theorem 2 (Fredman and Saks, 1989).** The chronogram method also gives:

- *Prefix parity.* For partial sums modulo 2, with cells of $b$ bits, $\Omega(\log n/\log b)$ amortized time per operation; for $b = \Theta(\log n)$ this is $\Omega(\log n/\log\log n)$. With one-bit values the argument needs more care than in Theorem 1, because the information of an epoch is only one bit per update.
- *Set union, amortized.* With cells of $\lceil \lg n \rceil$ bits, some sequence of $n - 1$ unions and $m \ge n$ finds costs $\Omega(m\,\alpha(m, n))$ (their Theorem 5). See the [union-find lower bound](/union-find-lower-bound/).
- *Set union, worst case.* With cells of $(\log n)^{O(1)}$ bits, some single operation costs $\Omega(\log n/\log\log n)$ (their Theorem 6).

## In plain words

A data structure takes changes and answers questions. Look back from the moment of a question. Group the past changes into eras: the most recent era is short, the one before it longer, and each earlier era much longer than the one after it.

A change can write only a few memory cells. So all the eras after a given era together wrote fewer cells than that era has changes. Those few cells cannot carry the news of all the changes of the older era. A random question, which needs that news, must therefore read some cell from the older era itself.

This is true for every era. There are many eras, so the question must read many cells, one or more from each era.

## Proof

The full proof of Theorem 1 is in [the proof of the chronogram bound](proofs/main.md). Its outline:

1. **The epochs.** Do $\sum_{i=1}^K \beta^i$ updates, in the order epoch $K$, epoch $K - 1$, ..., epoch 1, and then one query. Epoch $i$ has $\beta^i$ updates, at the fixed positions $l \cdot n/\beta^i$ for $l = 1, \ldots, \beta^i$, with independent uniform values in $\mathbb{Z}/2^\delta$. So epoch $i$ holds $\delta\beta^i$ random bits.
2. **Later epochs write few cells.** The epochs $1, \ldots, i - 1$, which come after epoch $i$, write at most $t_u \sum_{j < i} \beta^j \le 2 t_u \beta^{i-1}$ cells.
3. **An encoding.** Fix the values of all epochs but $i$, and an offset $y$. An encoder sends the addresses and final contents of the cells written after epoch $i$, a mask of the queries at the positions $l \cdot n/\beta^i + y$ that read no cell last written in epoch $i$, and the answers of the other queries. A decoder who knows the other epochs runs the structure up to epoch $i$, simulates each good query correctly, and recovers the prefix sums of epoch $i$ at all its positions, so all its $\delta\beta^i$ random bits.
4. **Counting.** A prefix-free code for $\delta\beta^i$ uniform bits has expected length at least $\delta\beta^i$. The message has $\beta^i + 4 t_u b \beta^{i-1} + b + \delta \cdot (\text{number of bad queries})$ bits. With the choice of $\beta$ and $\delta \ge 4$, at least half of the queries must be bad on average: a random query reads a cell last written in epoch $i$ with probability at least $\frac12$.
5. **Summing over the epochs.** The epochs are disjoint in time, so each cell that the query reads has its last write in at most one epoch. By linearity of expectation, the expected number of cells read is at least $K/2$. $\blacksquare$

For Theorem 2, Fredman and Saks use the same epochs with a finer counting for one-bit values, and for union-find an adversary that chooses the next round of unions or the next find depending on the costs so far. Their proof for union-find is outlined on the [union-find lower bound](/union-find-lower-bound/) page.

## Consequences

- **Fenwick trees are almost optimal.** The [Fenwick tree](/fenwick-tree/) and the [segment tree](/segment-tree/) do partial sums in $O(\log n)$ time per operation. Theorem 1 shows that no structure does better than $O(\log n/\log\log n)$ with words of $O(\log n)$ bits. Patrascu and Demaine (2006) closed the gap with a bound of $\Omega(\log n)$, by a different method; see the [dynamic partial sums lower bound](/dynamic-partial-sums-lower-bound/).
- **Union-find is settled.** With Theorem 2, union by rank and path compression is optimal among all cell-probe structures with words of $O(\log n)$ bits, and Blum's $k$-UF trees are optimal for the worst case of one operation. So the [dynamic equivalence problem](/dynamic-equivalence-problem/) is solved up to constant factors in both senses.
- **A trade-off.** Theorem 1 gives a bound on $t_q$ that falls only slowly as $t_u$ grows: $t_q = \Omega(\log n/\log(t_u b/\delta))$. A structure with fast queries must have very slow updates.
- **Many dynamic problems.** The method applies to every problem in which a query must read information from many past epochs, for example [dynamic connectivity](/dynamic-connectivity/), whose lower bounds are on the [dynamic connectivity lower bound](/dynamic-connectivity-lower-bound/) page, and dynamic range counting.

## Tightness

- **Partial sums.** The method cannot give more than $\Omega(\log n/\log\log n)$ for problems with answers of one word, because there are only $O(\log n/\log\log n)$ epochs when each is $\log n$ times longer than the next. Patrascu and Demaine explain this limit, and their information transfer method gets $\Omega(\log n)$, which a Fenwick tree reaches.
- **Prefix parity.** The bound $\Omega(\log n/\log\log n)$ for one-bit values is tight: a tree of fan-out $\Theta(\log n)$ whose nodes keep the parities of their children in one word answers in $O(\log n/\log\log n)$ time.
- **Set union.** The amortized bound is matched by [Tarjan's analysis](/union-find-amortized-bound/) of union by rank with path compression, and the worst-case bound by [Blum's structure](/blum-union-find/).
- **Beyond.** Larsen (2012) combined the chronogram with cell sampling and got $\Omega((\log n/\log\log n)^2)$ for dynamic range counting, a bound above $\log n$ for a dynamic problem.

## History

Fredman (1982) had proved logarithmic bounds for partial sums in restricted algebraic models. Fredman and Saks (1989) introduced the chronogram method and proved the first lower bounds for dynamic problems in the cell-probe model, among them prefix parity and set union. Their union-find bound closed the question left open by Tarjan's bound of 1979 for separable pointer algorithms and by Gabow and Tarjan's linear algorithm for a special case. Later work refined the method: Patrascu and Demaine (2004, journal version 2006) went past its limit with the information transfer method, and Larsen (2012) combined it with cell sampling. The pages on [cell-probe lower bounds](/cell-probe-lower-bound/) collect these methods.

## References
