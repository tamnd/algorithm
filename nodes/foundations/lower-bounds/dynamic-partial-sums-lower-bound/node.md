---
tag: 7QYDSF
kind: theorem
slug: dynamic-partial-sums-lower-bound
name: Dynamic partial sums lower bound
aliases:
- dynamic prefix sums lower bound
- Fredman partial sums bound
- Patrascu-Demaine partial sums bound
area: foundations/lower-bounds
level: research
summary: In the cell-probe model, keeping prefix sums of n word-sized numbers under point updates needs max(t_u, t_q) = Omega(log n), even amortized and randomized.
prereqs: [cell-probe-model, prefix-sums, amortized-cost]
see_also: [fenwick-tree, segment-tree, point-update-range-sum-query, cell-probe-lower-bound, predecessor-lower-bound, dynamic-connectivity-lower-bound, yao-minimax-principle, information-theoretic-bound]
sources:
  - paper: doi:10.1137/S0097539705447256
    title: "Mihai Patrascu and Erik D. Demaine, Logarithmic Lower Bounds in the Cell-Probe Model, SIAM Journal on Computing 35(4) (2006), 932-963"
    locator: Section 2.1 (Theorems 2.1, 2.2 and 2.3), Section 3 (previous work), Section 5 (the information transfer proof) and Section 5.6 (the bit-reversal sequence)
  - paper: doi:10.1145/73007.73040
    title: "Michael L. Fredman and Michael E. Saks, The cell probe complexity of dynamic data structures, Proceedings of the 21st Annual ACM Symposium on Theory of Computing (STOC 1989), 345-354"
    locator: the chronogram method and the Omega(log n / log b) bound for partial sums over Z/2Z
  - paper: doi:10.1145/322290.322305
    title: "Michael L. Fredman, The Complexity of Maintaining an Array and Computing Its Partial Sums, Journal of the ACM 29(1) (1982), 250-260"
    locator: the logarithmic bound for oblivious algorithms in the group model
  - paper: doi:10.1137/0214022
    title: "Andrew C. Yao, On the Complexity of Maintaining Partial Sums, SIAM Journal on Computing 14(2) (1985), 277-288"
    locator: the semigroup model with additive updates
  - paper: doi:10.1137/S0097539795291598
    title: "Haripriyan Hampapuram and Michael L. Fredman, Optimal Biweighted Binary Trees and the Complexity of Maintaining Partial Sums, SIAM Journal on Computing 28(1) (1998), 1-9"
    locator: the Omega(log n) bound in the semigroup model with additive updates
  - paper: doi:10.1002/spe.4380240306
    title: "Peter M. Fenwick, A new data structure for cumulative frequency tables, Software: Practice and Experience 24(3) (1994), 327-336"
    locator: the binary indexed tree with O(log n) update and prefix sum
---

The dynamic partial sums problem keeps an array $A[1..n]$ under two operations: add a value to one entry, and return the sum of a prefix. In the [cell-probe model](/cell-probe-model/), Patrascu and Demaine (2006) proved that every structure with word-sized values has $\max\{t_u, t_q\} = \Omega(\lg n)$, even with amortization and Las Vegas randomization, and they proved the full trade-off between $t_u$ and $t_q$. The [Fenwick tree](/fenwick-tree/) and the [segment tree](/segment-tree/) reach $O(\lg n)$, so the bound is tight. This page states the theorem exactly and proves a version with explicit constants by the information transfer method.

## Statement

**The problem.** Fix $n \ge 1$ and $\delta \ge 1$. The array $A[1..n]$ holds elements of the group $\mathbb{Z}/2^\delta$ (integers modulo $2^\delta$), and every entry is $0$ at the start.

- `update(k, Δ)` with $1 \le k \le n$ and $\Delta \in \mathbb{Z}/2^\delta$ sets $A[k] \leftarrow A[k] + \Delta$.
- `sum(k)` with $1 \le k \le n$ returns $A[1] + \dots + A[k]$ in $\mathbb{Z}/2^\delta$.

**The model.** The [cell-probe model](/cell-probe-model/) with $w$-bit cells and $\delta \le w$. The memory has at most $2^w$ cells, so an address fits in one cell. The initial memory contents are fixed. Each operation is a decision tree that reads and writes cells, and its cost is the number of cells it probes. All other computation is free. The costs $t_u$ and $t_q$ are *amortized*: every sequence of $n_u$ updates and $n_q$ sums, started from the initial memory, costs at most $n_u t_u + n_q t_q$ probes in total. For a Las Vegas structure (random choices, answers always correct) the bound is on the expected total.

**Theorem (Patrascu and Demaine 2006, Theorems 2.1 and 2.2).** Write $L(x) = \log_2(2 + x)$. Consider the problem over the integers with $b$-bit cells, $b = \Omega(\lg n)$, where every entry and every sum fits in a cell and an update argument has $\delta$ bits. Every cell-probe structure, with amortization and Las Vegas randomization allowed, satisfies

$$t_q \cdot \big(L(b/\delta) + L(t_u/t_q)\big) = \Omega(\lg n).$$

If moreover $\delta = \Omega(b)$, then also

$$t_q \cdot L(t_u/t_q) = \Omega(\lg n) \qquad\text{and}\qquad t_u \cdot L(t_q/t_u) = \Omega(\lg n),$$

so $\max\{t_u, t_q\} = \Omega(\lg n)$. In general $\max\{t_u, t_q\} = \Omega(\lg n / L(b/\delta))$. The same trade-offs hold for the `select` query, and the trade-offs between $t_u$ and $t_q$ also hold in the group model.

**Theorem (explicit form, proved below).** Let $n = 2^k$ with $k \ge 1$, let $2 \le \delta \le w$, and take the problem over $\mathbb{Z}/2^\delta$ in the model above. Then every structure, deterministic or Las Vegas, with amortized costs $t_u$ and $t_q$ satisfies

$$t_u + t_q \ \ge\ \frac{\delta \lg n}{4w + 8}.$$

For $\delta = w$ this gives $t_u + t_q \ge \lg n / 12$, so $\max\{t_u, t_q\} \ge \lg n / 24$. The constants are the ones this proof gives. The paper states the result up to constant factors only.

## In plain words

Keep a list of numbers. One operation adds to one number. The other asks for the total of the first few numbers. Any memory layout must pay about the logarithm of the list length per operation, counted as the number of memory words it touches. No cleverness in the layout avoids this cost, and neither do coin flips or averaging over many operations. The reason is a flow of information. Many recent updates carry fresh random values. Later queries must learn many of those values. Each word that the queries read can carry only one word of news. When you split the sequence of operations at every level of a balanced tree of time, each level forces its own share of reads. The levels add up, and the total grows with the logarithm of the list length.

## Proof

The proof follows Section 5 of Patrascu and Demaine and uses their deterministic access sequence of Section 5.6. The constants are worked out here.

**Step 1: a hard input.** For $0 \le i < n$ let $\pi(i)$ be the number whose $k$-bit binary form is the $k$-bit form of $i$ written backwards. The input is a sequence of $2n$ operations: for $i = 0, 1, \dots, n-1$ in turn, `update(π(i)+1, Δ_i)` then `sum(π(i)+1)`. The values $\Delta_0, \dots, \Delta_{n-1}$ are independent and uniform in $\mathbb{Z}/2^\delta$. Only the values are random. The indices are fixed.

**Step 2: reduce to deterministic structures.** Fix the random string of a Las Vegas structure. The result is a deterministic structure that is correct on every input. If each such structure has expected total cost at least $X$ on the random input of Step 1, then so does the Las Vegas structure, because the expectation over its random string is an average of numbers that are all at least $X$. This is the easy direction of the [minimax principle](/yao-minimax-principle/). From now on the structure is deterministic. Its total cost on any input of Step 1 is at most $n t_u + n t_q$.

**Step 3: the time tree.** Build a complete binary tree whose $2n$ leaves are the operations in time order. For an internal node $v$, let $\mathrm{left}(v)$ and $\mathrm{right}(v)$ be the sets of operations under its two children. Let $IT(v)$, the *information transfer* at $v$, be the number of reads made during $\mathrm{right}(v)$ of a cell whose last write before that read was made during $\mathrm{left}(v)$. A read of cell $x$ at time $r$, whose last earlier write to $x$ happened in a different operation at time $s$, is counted at exactly one node: the lowest common ancestor of the leaves $s$ and $r$. Other reads are not counted at all. So the total number of probes is at least $\sum_v IT(v)$.

**Step 4: interleaving.** For an internal node $v$, let $U$ be the set of indices updated in $\mathrm{left}(v)$, and let $q_1 < q_2 < \dots < q_m$ be the indices queried in $\mathrm{right}(v)$, with $q_0 = 0$. The *interleaving* $\ell(v)$ is the number of $j \in \{1, \dots, m\}$ such that $U$ meets the interval $(q_{j-1}, q_j]$.

*Claim.* A node at height $1$ has $\ell(v) = 1$. A node at height $h \ge 2$ has $\ell(v) = 2^{h-2}$. Hence $\sum_v \ell(v) = n + n k / 2$.

*Proof of the claim.* A node at height $1$ holds one update and one sum on the same index, so $\ell = 1$. A node at height $h \ge 2$ holds the pairs $i = c \cdot 2^{h-1} + r$ for one fixed $c$ and all $0 \le r < 2^{h-1}$. Reversing the $k$ bits of $i$ gives $\pi(i) = \bar r \cdot 2^{k-h+1} + \bar c$, where $\bar r$ is the $(h-1)$-bit reversal of $r$ and $\bar c$ depends only on $c$. As $r$ runs over its range, $\bar r$ runs over all of $\{0, \dots, 2^{h-1} - 1\}$. The left child holds the pairs with $r < 2^{h-2}$, that is with top bit of $r$ equal to $0$, that is with $\bar r$ even. The right child holds the pairs with $\bar r$ odd. So in sorted order the indices alternate: left, right, left, right, and so on, starting with left. Every query index of the right child has an update index of the left child just below it, so $\ell(v) = 2^{h-2}$. There are $2n / 2^h$ nodes at height $h$, so each height $h = 2, \dots, k+1$ contributes $n/2$, and height $1$ contributes $n$. $\square$

**Step 5: entropy of the answers.** Fix an internal node $v$. Let $G$ be the values $\Delta_i$ of all updates outside $\mathrm{left}(v)$, and let $Y$ be the list of answers of the sums in $\mathrm{right}(v)$. Write $H$ for Shannon entropy in bits.

*Claim.* $H(Y \mid G) \ge \ell(v)\,\delta$.

*Proof of the claim.* Fix $G = g$. The answer to `sum(q_j)` equals a number fixed by $g$ (the values of all updates outside $\mathrm{left}(v)$ that come before this query and touch an index at most $q_j$) plus the sum $S_j$ of the values of the updates in $\mathrm{left}(v)$ with index at most $q_j$. So $Y$ determines $S_1, \dots, S_m$ and hence the differences $D_j = S_j - S_{j-1}$, which are the sums of the values of the updates in $\mathrm{left}(v)$ with index in $(q_{j-1}, q_j]$. The $\ell(v)$ differences with a nonempty index set are sums over disjoint nonempty sets of independent uniform elements of $\mathbb{Z}/2^\delta$, so they are independent and uniform. Their joint entropy is $\ell(v)\,\delta$, and they are a function of $Y$ given $g$. $\square$

**Step 6: an encoding.** Fix $v$ and $G = g$. Let $C$ be the set of distinct cells that are read during $\mathrm{right}(v)$ with their last earlier write in $\mathrm{left}(v)$, and let $c = |C|$. Then $c \le IT(v)$. The encoder writes the number $c + 1$ in the Elias gamma code ($2\lfloor \lg(c+1) \rfloor + 1$ bits, prefix-free), then for each cell of $C$ its address and its contents at the end of $\mathrm{left}(v)$, at $2w$ bits per cell.

The decoder knows $g$ and the structure. It runs every operation before $\mathrm{left}(v)$; these depend only on $g$. It skips $\mathrm{left}(v)$. It then runs the operations of $\mathrm{right}(v)$. When one of them reads a cell $x$, the decoder takes the contents from its own record if $x$ was already written during $\mathrm{right}(v)$, else from the code if $x \in C$, else from the memory state before $\mathrm{left}(v)$. In the third case the last write to $x$ was not in $\mathrm{left}(v)$ or $\mathrm{right}(v)$, so the state before $\mathrm{left}(v)$ is correct. The updates in $\mathrm{right}(v)$ have values in $g$. So the decoder reproduces every read, and hence $Y$.

The code length is a function of the values in $\mathrm{left}(v)$, and $Y$ is a function of the code word given $g$. So, by Jensen's inequality for the concave function $\lg(x+1)$ and by $\lg(x+1) \le 2x$ for $x \ge 0$,

$$\ell(v)\,\delta \le H(Y \mid G = g) \le \mathbb{E}[2wc + 2\lg(c+1) + 1] \le (2w + 4)\,\mathbb{E}[c] + 1.$$

Average over $g$ to get $\mathbb{E}[IT(v)] \ge (\ell(v)\,\delta - 1) / (2w + 4)$.

**Step 7: add up.** There are $2n - 1$ internal nodes. By Steps 3, 4 and 6,

$$n(t_u + t_q) \ \ge\ \sum_v \mathbb{E}[IT(v)] \ \ge\ \frac{\delta(n + nk/2) - (2n - 1)}{2w + 4} \ >\ \frac{\delta n k / 2 + (\delta - 2)n}{2w + 4}.$$

For $\delta \ge 2$ the last term is at least $\delta n k / (4w + 8)$. Divide by $n$ and use $k = \lg n$. $\blacksquare$

The bit-reversal order for $n = 8$ updates and queries the indices $1, 5, 3, 7, 2, 6, 4, 8$. The sums of $\ell(v)$ over the levels of its time tree are $8$ at height $1$ and $4$ at each of the heights $2, 3, 4$, for a total of $20 = 8 + 8 \cdot 3 / 2$.

## Consequences

- *Logarithmic time is optimal.* With word-sized values, no structure beats the [Fenwick tree](/fenwick-tree/) by more than a constant factor, in the worst case, amortized or in expectation.
- *Constant time on one side costs a polynomial on the other.* Let $\delta = \Omega(b)$. If $t_q = O(1)$, then $L(t_u/t_q) = \Omega(\lg n)$, so $t_u = n^{\Omega(1)}$. If $t_u = O(1)$, then $t_q = n^{\Omega(1)}$ in the same way. A prefix-sum array with $O(1)$ query and $O(n)$ update and a plain array with $O(1)$ update and $O(n)$ query are at the two ends of this curve.
- *Range sums.* A query for $A[i] + \dots + A[j]$ answers `sum(j)` when $i = 1$, so [point update range sum](/point-update-range-sum-query/) has the same bound.
- *Dynamic connectivity.* Patrascu and Demaine extend the method to queries with one-bit answers and prove $\Omega(\lg n)$ for dynamic connectivity, see [the dynamic connectivity lower bound](/dynamic-connectivity-lower-bound/).
- *A worked comparison.* For $n = 2^{20}$ and $\delta = w = 64$, the explicit bound gives $t_u + t_q \ge 64 \cdot 20 / 264 \approx 4.85$. A Fenwick tree on $2^{20}$ entries visits at most $21$ nodes in an update and at most $20$ in a sum. The constant in the proof is loose. The growth rate is exact.

### Pitfalls

- *Small values have a smaller bound.* For one-bit updates ($\delta = 1$) the tight bound is $\Theta(\lg n / \lg(w/\delta))$ by Theorem 2.2 and Theorem 2.3 of the paper, which is $\Theta(\lg n / \lg\lg n)$ when $w = \Theta(\lg n)$. The claim "$\Omega(\lg n)$ for every partial sums problem" is false.
- *The reverse trade-off needs large values.* For $\delta = o(b)$ the paper proves only the trade-off with $t_q$ on the left, not the one with $t_u$ on the left.
- *The model counts probes only.* The bound holds for every instruction set, because computation is free. It does not say anything about the instruction count of a RAM beyond the probes.
- *The memory size matters.* The proof writes an address in $w$ bits, so it needs at most $2^w$ cells.

## Tightness

The bound is tight. A balanced tree over $A$ that stores the sum of each subtree gives $t_u = t_q = O(\lg n)$ in the worst case, and so do the [Fenwick tree](/fenwick-tree/) and the [segment tree](/segment-tree/). The whole trade-off curve for `sum` is tight too. In a tree with fan-out $B$, let each node store the prefix sums of its children. An update rewrites up to $B$ values on each of $\log_B n$ levels, and a sum reads one value per level. So $t_q = O(\log_B n)$ and $t_u = O(B \log_B n)$, and $t_q \lg(t_u/t_q) = O(\log_B n \cdot \lg B) = O(\lg n)$. Patrascu and Demaine (Theorem 2.3) also give a deterministic worst-case RAM structure with $t_u = t_q = t_s = O(\lg n / L(b/\delta))$, which matches the bound for small $\delta$.

## History

Fredman (1982) gave a tight logarithmic bound in the group model for oblivious algorithms, whose behavior is a fixed matrix product. Yao (1985) proved $\Omega(\lg n / \lg\lg n)$ in the semigroup model with additive updates, and Hampapuram and Fredman (1998) raised this to $\Omega(\lg n)$. In the cell-probe model, Fredman and Saks (1989) introduced the chronogram method and proved $t_q \cdot \lg(b\, t_u) = \Omega(\lg n)$ for the problem over $\mathbb{Z}/2$, which gives $\Omega(\lg n / \lg\lg n)$ for $b = \Theta(\lg n)$. Alstrup, Husfeldt and Rauhe proved the stronger trade-off $t_q \lg t_u = \Omega(\lg n)$ for a version of the problem on trees, which is the limit of the chronogram method. Miltersen listed an $\Omega(\lg n)$ bound for partial sums as an open challenge. Patrascu and Demaine solved it at SODA 2004 with the information transfer method, and the journal version appeared in 2006.

## References
