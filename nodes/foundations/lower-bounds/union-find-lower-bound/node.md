---
tag: GPNHZF
kind: theorem
slug: union-find-lower-bound
name: Union-find lower bound
aliases:
- Fredman-Saks bound
- inverse Ackermann lower bound
- set union lower bound
area: foundations/lower-bounds
level: research
summary: Every union-find structure in the cell-probe model with O(log n)-bit words needs Omega(m alpha(m,n)) probes for some n-1 unions and m finds, so union by rank with path compression is optimal.
prereqs: [cell-probe-model, pointer-machine, inverse-ackermann-function, disjoint-set-forest]
see_also: [union-find-amortized-bound, fredman-saks-lower-bound, union-by-rank, path-compression, ackermann-function, cell-probe-lower-bound, word-ram, incremental-connectivity]
sources:
  - paper: doi:10.1145/73007.73040
    title: "Michael L. Fredman and Michael E. Saks, The cell probe complexity of dynamic data structures, Proceedings of the 21st Annual ACM Symposium on Theory of Computing (1989), 345-354"
    locator: Theorem 5 and its proof in Section 4 (Lemmas 4 and 5, Remark 1), Theorem 6 (worst case per operation), and the discussion of separable algorithms and of the register size in Section 3
  - paper: doi:10.1016/0022-0000(79)90042-4
    title: "Robert Endre Tarjan, A class of algorithms which require nonlinear time to maintain disjoint sets, Journal of Computer and System Sciences 18(2) (1979), 110-127"
    locator: the lower bound for separable pointer algorithms
  - paper: doi:10.1145/321879.321884
    title: "Robert Endre Tarjan, Efficiency of a Good But Not Linear Set Union Algorithm, Journal of the ACM 22(2) (1975), 215-225"
    locator: the upper bound O(m alpha(m,n)) and the definition of alpha(m,n) used by Fredman and Saks
  - paper: doi:10.1145/100216.100221
    title: "Johannes A. La Poutré, Lower bounds for the union-find and the split-find problem on pointer machines, Proceedings of the 22nd Annual ACM Symposium on Theory of Computing (1990), 34-44"
    locator: abstract (the bound for all pointer machine algorithms, without the separation condition)
  - paper: doi:10.1006/jcss.1996.0008
    title: "J. A. La Poutré, Lower Bounds for the Union-Find and the Split-Find Problem on Pointer Machines, Journal of Computer and System Sciences 52(1) (1996), 87-99"
    locator: journal version of the STOC 1990 paper
  - paper: doi:10.1137/0215072
    title: "Norbert Blum, On the Single-Operation Worst-Case Time Complexity of the Disjoint Set Union Problem, SIAM Journal on Computing 15(4) (1986), 1021-1024"
    locator: the algorithm with O(log n/log log n) worst-case time per operation, and its optimality for separable algorithms
  - paper: doi:10.1016/0022-0000(85)90014-5
    title: "Harold N. Gabow and Robert Endre Tarjan, A linear-time algorithm for a special case of disjoint set union, Journal of Computer and System Sciences 30(2) (1985), 209-221"
    locator: the linear-time algorithm when the unions are known in advance
---

The union-find lower bound says that no data structure for disjoint sets can beat the inverse Ackermann cost of [union by rank](/union-by-rank/) with [path compression](/path-compression/). Fredman and Saks (1989) proved it in the [cell-probe model](/cell-probe-model/) with words of $O(\log n)$ bits, so it holds for every algorithm on a word RAM, with any data layout and any use of address arithmetic. Earlier, Tarjan (1979) had proved the same bound for a restricted class of [pointer machine](/pointer-machine/) algorithms. The bound is about the data structure, not about one algorithm.

## Statement

**The problem.** The *set union problem* on $n$ elements starts with the $n$ singleton sets $\{1\}, \ldots, \{n\}$, where the set $\{i\}$ has the name $i$. It supports two operations, online: $\mathrm{Find}(x)$ returns the name of the set that contains the element $x$, and $\mathrm{Union}(A, B, C)$ replaces the sets named $A$ and $B$ by their union, with the name $C$. Names are integers in a range of size $O(n)$, so a name fits in $O(\log n)$ bits.

**The cell-probe model.** Write CPROBE($b$) for the [cell-probe model](/cell-probe-model/) with registers of $b$ bits. The memory is an array of registers. The cost of an operation is the number of registers that it reads or writes. All other computation is free, and the algorithm may store anything in any register.

The function $\alpha(m, n)$ is the two-argument inverse of the [Ackermann function](/ackermann-function/), as on the [inverse Ackermann function](/inverse-ackermann-function/) page. Fredman and Saks use Tarjan's 1975 form, which has other constants inside. The forms differ by additive constants, which the bounds below hide.

**Theorem A (Fredman and Saks, 1989, Theorem 5 and Remark 1).** Let $m \ge n$. For every deterministic algorithm for the set union problem in CPROBE($\lceil \lg n \rceil$), there is a sequence of $n - 1$ unions and $m$ finds, starting from $n$ singletons, on which the algorithm makes $\Omega(m\,\alpha(m, n))$ probes. So the amortized cost of an operation is $\Omega(\alpha(m, n))$.

**Theorem B (Tarjan, 1979; La Poutré, 1990).** Tarjan proved the bound $\Omega(m\,\alpha(m,n))$ for $n - 1$ unions and $m \ge n$ finds for every *separable* pointer machine algorithm. Informally, the nodes of the structure for each set form their own component, and no pointer joins two sets. The exact conditions are in the paper. La Poutré removed the separability condition, and extended the bound to $\Omega(n + m\,\alpha(m, n))$ for all $m$ and $n$, for every pointer machine algorithm.

**Theorem C (worst case of one operation).** Fredman and Saks (Theorem 6): if $b \le (\log n)^c$ for a constant $c$, every algorithm in CPROBE($b$) that starts from $n$ singletons has an operation with worst-case cost $\Omega(\log n / \log\log n)$. Blum (1986) gave an algorithm with worst-case cost $O(\log n / \log\log n)$ per operation, and proved its optimality for separable algorithms. So Blum's bound is tight in both models.

## In plain words

A structure for disjoint sets answers questions of the form "which group is this item in?" while groups keep merging. The well-known forest method with two simple tricks does each step in a time that grows so slowly that it never passes five in practice, but it does grow. The theorem says that this slow growth cannot be removed. Every possible structure, with any memory layout and any arithmetic, must sometimes pay that much on average.

The reason is a contest between merges and questions. After each wave of merges, the structure can either pay now to record the new group of each item, or keep the old records and pay later, when a question has to look through the record of each wave. An adversary always picks the option that costs more. Balancing these two costs over many waves gives the inverse of a very fast-growing function.

## Proof

This is a sketch of the proof of Fredman and Saks for $m = n$. It states their lemmas and the counting that combines them. The proofs of the two lemmas are long, and only their ideas are given. Fix an algorithm $\mathcal{A}$ in CPROBE($\lceil \lg n \rceil$), with $n \ge 10^5$, and let $n$ be a power of 2.

**Step 1: hard sequences.** Use sequences that build the sets evenly. In *union round* $k$, the $n/2^k$ sets of size $2^k$ are paired in some way, and each pair is merged, which gives $n/2^{k+1}$ sets of size $2^{k+1}$. Stop before any set has more than $\sqrt n$ elements, so there are at most $\frac12 \lg n$ rounds. Finds happen only between rounds. A word $S$ over the letters $\mathtt U$ and $\mathtt F$ describes the shape of a sequence: the $k$-th $\mathtt U$ is round $k - 1$, and each $\mathtt F$ is one find. The family $R(S)$ is the set of all operation sequences of shape $S$, with any pairing in each round and any element in each find. Costs below are averages over $R(S)$, with all sequences equally likely. A bound on the average gives a sequence that costs at least as much.

**Step 2: the adversary and its epochs.** Choose an integer $q \ge 2$. The adversary builds $S$ one letter at a time, starting with $\mathtt U$. It keeps a division of the word into at most $q$ contiguous *epochs*, each starting with a $\mathtt U$. If there are $q$ epochs, the next letter is $\mathtt F$, and it joins the last epoch. Otherwise the next letter is $\mathtt U$, which starts a new epoch. Call an epoch $e$ that starts with the $k$-th $\mathtt U$ *compressed* if, on average, $\mathcal{A}$ writes at least $n/(100\,q\,2^{k-1})$ registers after the end of $e$. After each letter, the adversary takes the leftmost compressed epoch, if there is one, and merges into it all the epochs to its right. The adversary stops when it would need more than $\frac12 \lg n$ letters $\mathtt U$ or more than $n$ letters $\mathtt F$.

**Lemma 4 (Fredman and Saks).** For each $\mathtt F$ of $S$, the average number of probes of $\mathcal{A}$ for the corresponding find is at least $q/10$.

*Idea (informal).* A find comes only when there are $q$ epochs and none of them is compressed. The epoch that starts with round $k - 1$ decides which of the $n/2^{k-1}$ sets of that time an element joins. Too few registers were written after the epoch to store this information again, so a find on a random element must, with constant probability, read a register that was last written during that epoch. This holds for each of the $q$ epochs. The proof tags each register with the time of its last write (a *chronogram*) and counts the registers whose tag falls in each epoch.

**Lemma 5 (Fredman and Saks).** Define $h_r(0) = 1$, $h_2(m) = m + 1$, and $h_r(m) = h_r(m - 1) + h_{r-1}\big(2^{h_r(m-1)}\big)$ for $r > 2$ and $m > 0$. If the adversary generates at least $h_q(m)$ letters $\mathtt U$, then the leftmost epoch has been compressed at least $m$ times.

*Idea (informal).* The lemma is about the adversary only, not about $\mathcal{A}$. While there are fewer than $q$ epochs, each new $\mathtt U$ makes a new epoch, and each compression merges a suffix of the epochs into one. With $q$ epochs, finds are added until some epoch is compressed. The proof is an induction on $r$ and $m$ for the epoch in position $q + 1 - r$ from the left, and the recursion of $h_r$ follows the nesting of the epochs.

**Step 3: count.** Suppose that $h_q(q^2) \le \frac12 \lg n$. The adversary stops in one of two ways.

- It has generated $n$ letters $\mathtt F$. By Lemma 4, the finds cost at least $qn/10$ probes on average.
- It has generated $\frac12 \lg n \ge h_q(q^2)$ letters $\mathtt U$. By Lemma 5, the leftmost epoch was compressed at least $q^2$ times. The leftmost epoch starts with the first $\mathtt U$, so $k = 1$, and each compression means at least $n/(100q)$ writes after the end of that epoch. These writes happen in disjoint stretches of the sequence, because the epoch grows past the writes that compressed it. A prefix of a sequence in $R(S)$ is a uniformly random sequence of the shorter family, so the averages add. The total is at least $q^2 \cdot n/(100q) = qn/100$ writes.

In both cases the cost is at least $qn/100$. Taking the largest $q$ with $h_q(q^2) \le \frac12 \lg n$ gives $\Omega(zn)$ for $z = \max\{q : h_q(q^2) \le \frac12 \lg n\}$.

**Step 4: from $z$ to $\alpha$.** The function $h_q$ grows like Ackermann's function in $q$, and Fredman and Saks show that $z = \Omega(\alpha(n, n))$. For $m \ge n$ (Remark 1), the adversary may use $m$ letters $\mathtt F$, and $\lceil q^2 m/n \rceil$ compressions account for $\Omega(qm)$ writes. This gives $\Omega(z' m)$ with $z' = \max\{q : h_q(\lceil q^2 m/n\rceil) \le \frac12 \lg n\}$ and $z' = \Omega(\alpha(m,n))$. The sequences have fewer than $n - 1$ unions. Adding the missing unions at the end does not lower the cost. $\square$

Fredman and Saks add that a simpler adversary suffices: if a find at this point costs more than $q/10$ on average, do a find, and otherwise do another round of unions.

**Theorem B.** The proofs of Tarjan and of La Poutré work on the graph of the pointer machine. They are not given here.

## Consequences

- **The forest is optimal.** [Union by rank](/union-by-rank/) with [path compression](/path-compression/) costs $O(m\,\alpha(m,n))$ (see Tightness). It stores parent indices and ranks, which fit in $O(\log n)$ bits, so it runs in CPROBE($O(\log n)$). Theorem A says that no structure in that model has a better order of cost.
- **The word RAM.** A word RAM with words of $O(\log n)$ bits does $O(1)$ probes per instruction, so Theorem A holds for it. Bit tricks, hashing and tables of precomputed answers do not help. A word of $c \lceil \lg n \rceil$ bits for a constant $c$ is $c$ registers of CPROBE($\lceil \lg n \rceil$), so the bound holds for such words too.
- **Separable algorithms are not optimal for all cases.** Gabow and Tarjan (1985) solve the special case in which the unions are known in advance in linear time on a RAM. Fredman and Saks point out that Tarjan's bound for separable algorithms holds even for this special case. So separable algorithms are not optimal for that case, and before 1989 the same could have been true for the general problem. Theorem A excludes it.
- **Consequences for algorithms.** Algorithms that use union-find as a black box, such as Kruskal's algorithm for the [minimum spanning tree](/minimum-spanning-tree/) or [incremental connectivity](/incremental-connectivity/), cannot get a faster union-find part. This is not a lower bound for those problems: another algorithm may avoid union-find.

### Worked example

The constants in the proof are small, but $h_q$ grows very fast. Computed from the definition:

| $m$ | $0$ | $1$ | $2$ | $3$ | $4$ |
|---|---|---|---|---|---|
| $h_2(m)$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| $h_3(m)$ | $1$ | $4$ | $21$ | $2\,097\,174$ | about $2^{2\,097\,174}$ |

For $q = 2$ the condition $h_2(4) = 5 \le \frac12 \lg n$ holds when $n \ge 2^{10}$. For $q = 3$ it needs $h_3(9) \le \frac12 \lg n$, and $h_3(9)$ is a tower of powers of 2. So for every $n$ that fits in any computer, the proof gives $z = 2$, and Theorem A says only that the cost is a constant times $m$. Also $\alpha$ itself is tiny: with the definition of the inverse Ackermann page, $\alpha(m, n)$ for $n = 2^{32}$ is $4$ for $m = n$, $3$ for $m = 2n$, $2$ for $3n \le m \le 5n$, and $1$ for $m \ge 6n$. Theorem A is a statement about growth, and it does not say that a real structure must be slow.

### Pitfalls

- **The model and the word size.** Theorem A is for CPROBE($O(\log n)$). Fredman and Saks do not know whether it holds for registers of $(\log n)^{O(1)}$ bits. The hard sequences of the proof can be done in linear time with registers of $\log^2 n$ bits. Theorem C holds for registers up to $(\log n)^{O(1)}$ bits.
- **Not a bound on path compression.** The theorem is a bound for every data structure. Bounds on one algorithm, such as Tarjan's 1975 lower bound for union by rank with path compression, are different statements and use other sequences.
- **Amortized and worst case.** Theorem A bounds the total cost of a sequence. One operation can cost more: Theorem C gives $\Omega(\log n/\log\log n)$ for the worst single operation, a different and much larger quantity.
- **Online.** The operations come one at a time. If the unions are known in advance, the cost is linear (Gabow and Tarjan).
- **The definition of $\alpha$.** $\alpha(m, n)$ falls as $m/n$ grows. With the definition of the inverse Ackermann page, $\alpha(m, n) = 1$ for $m \ge n(\lg\lg n + 1)$, and then the bound is $\Omega(m)$, which is trivial. The variants of $\alpha$ in the literature differ by constants. Say which one a bound uses.
- **Pointer machine and cell probe are different.** Theorem B forbids address arithmetic and has no word size. Theorem A allows any arithmetic but needs words of $O(\log n)$ bits. Neither theorem implies the other.

## Tightness

Tarjan (1975) proved that a [disjoint-set forest](/disjoint-set-forest/) with [union by rank](/union-by-rank/) and [path compression](/path-compression/) does $n - 1$ unions and $m \ge n$ finds in $O(m\,\alpha(m, n))$ time (see [union-find amortized bound](/union-find-amortized-bound/)). With Theorem A, the amortized cost of the set union problem in CPROBE($O(\log n)$) is $\Theta(\alpha(m, n))$, and with Theorem B the same holds on the pointer machine. The worst-case cost of one operation is $\Theta(\log n/\log\log n)$, by Theorem C and Blum's algorithm.

## History

Tarjan (1975) proved the upper bound $O(m\,\alpha(m,n))$ for the forest with union by rank and path compression, and showed that this algorithm is no better. Tarjan (1979) proved the bound for the class of separable pointer algorithms. Gabow and Tarjan (1985) showed that a special case is linear on a RAM, which raised the question whether a RAM could beat $\alpha$ in general. Blum (1986) settled the worst case of one operation for separable algorithms. Fredman and Saks (1989) introduced the chronogram method and proved the bound in the cell-probe model, which covers every RAM algorithm with words of $O(\log n)$ bits. La Poutré (1990, journal version 1996) proved the bound for all pointer machine algorithms. The same chronogram method gave Fredman and Saks their bounds for dynamic partial sums (see [cell-probe lower bound](/cell-probe-lower-bound/)).

## References
