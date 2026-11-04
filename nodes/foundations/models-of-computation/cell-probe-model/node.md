---
tag: 9BWWGW
kind: model
slug: cell-probe-model
name: Cell-probe model
aliases:
- Cell probe model
- cell probe model
- cell-probe complexity
area: foundations/models-of-computation
level: research
summary: Model in which only memory word reads are counted, giving the strongest known lower bounds for data structures.
prereqs: [word-ram, random-access-machine, asymptotic-notation]
see_also: [bit-probe-model, predecessor-problem, predecessor-lower-bound, pointer-machine, communication-complexity, union-find-lower-bound, fks-perfect-hashing, hash-table]
sources:
  - paper: "Andrew Chi-Chih Yao, Should tables be sorted?, Journal of the ACM 28(3) (1981)"
    locator: the definition of the model and the result on tables of n cells
  - paper: "Mihai Patrascu and Mikkel Thorup, Time-space trade-offs for predecessor search, Proceedings of the 38th ACM Symposium on Theory of Computing (STOC 2006)"
    locator: the main theorem on the optimal query time for predecessor search
  - paper: "Mihai Patrascu and Mikkel Thorup, Randomization does not help searching predecessors, Proceedings of the 18th ACM-SIAM Symposium on Discrete Algorithms (SODA 2007)"
    locator: abstract (the same bound for randomized algorithms)
  - paper: "Paul Beame and Faith E. Fich, Optimal bounds for the predecessor problem and related problems, Journal of Computer and System Sciences 65(1) (2002)"
    locator: abstract (the bound for polynomial space)
  - paper: "Miklos Ajtai, A lower bound for finding predecessors in Yao's cell probe model, Combinatorica 8(3) (1988)"
    locator: abstract (the first super-constant bound)
  - paper: "Michael L. Fredman and Michael E. Saks, The cell probe complexity of dynamic data structures, Proceedings of the 21st ACM Symposium on Theory of Computing (STOC 1989)"
    locator: the chronogram technique and the bounds for partial sums and union-find
  - paper: "Mihai Patrascu and Erik D. Demaine, Logarithmic lower bounds in the cell-probe model, SIAM Journal on Computing 35(4) (2006)"
    locator: abstract (the bound of log n for partial sums)
  - paper: "Peter Bro Miltersen, Noam Nisan, Shmuel Safra and Avi Wigderson, On data structures and asymmetric communication complexity, Journal of Computer and System Sciences 57(1) (1998)"
    locator: the reduction from cell-probe schemes to communication protocols
  - paper: "Peter Bro Miltersen, Cell probe complexity: a survey, Advances in Data Structures Workshop (pre-conference workshop of FSTTCS 1999)"
    locator: the whole survey
  - paper: "Michael L. Fredman, Janos Komlos and Endre Szemeredi, Storing a sparse table with O(1) worst case access time, Journal of the ACM 31(3) (1984)"
    locator: abstract (the static dictionary with constant query time)
  - paper: "Kasper Green Larsen, The cell probe complexity of dynamic range counting, Proceedings of the 44th ACM Symposium on Theory of Computing (STOC 2012)"
    locator: abstract
  - paper: "Kasper Green Larsen, Higher cell probe lower bounds for evaluating polynomials, 53rd Annual Symposium on Foundations of Computer Science (FOCS 2012)"
    locator: abstract (the static lower bound for polynomial evaluation)
  - paper: "Kasper Green Larsen, Omri Weinstein and Huacheng Yu, Crossing the logarithmic barrier for dynamic Boolean data structure lower bounds, Proceedings of the 50th ACM Symposium on Theory of Computing (STOC 2018)"
    locator: abstract (the bound for dynamic Boolean problems)
---

The cell-probe model is a model of data structures that counts only the memory cells that an operation reads or writes. Computation is free. Each cell holds $w$ bits. Yao introduced it in 1981 in the paper "Should tables be sorted?". A lower bound in this model holds for every data structure on a [word RAM](/word-ram/) with the same cell size, whatever instructions the structure uses, so it is the strongest kind of lower bound that is known for data structures.

## The machine

A *data structure problem* is given by a set $\mathcal D$ of data, a set $\mathcal Q$ of queries, and a function $f : \mathcal D \times \mathcal Q \to \mathcal A$. The structure stores $d \in \mathcal D$ and answers each query $q$ with $f(d, q)$. An example: $\mathcal D$ is the family of subsets of size $n$ of a universe $\{1, \dots, m\}$, $\mathcal Q$ is the universe, and $f(d, q) = 1$ if $q \in d$ and $0$ otherwise (membership).

**Static structures.** The memory is an array of $s$ cells with addresses $1, \dots, s$, and each cell holds a string of $w$ bits. A *scheme* with $t$ probes consists of two parts.

- A *table function* $T : \mathcal D \to (\{0,1\}^w)^s$. It writes the data into the memory. It is any function. It takes no cost.
- For each query $q$, a *query algorithm*: a decision tree of depth at most $t$. Each internal node holds an address in $\{1, \dots, s\}$ and has $2^w$ children, one for each value of the cell. Each leaf holds an answer. The algorithm starts at the root, reads the cell at the address of the current node, and moves to the child given by the value that it read.

The scheme is correct if for every $d$ and $q$ the leaf reached on the memory $T(d)$ holds $f(d,q)$. Because the address of a probe can depend on the values of the earlier probes, the algorithm is *adaptive*. The query algorithm for $q$ may depend on $q$ in any way. Variants allow randomized query algorithms with an error probability.

**Dynamic structures.** The data change by *updates*, and queries come between them. An update algorithm reads cells, writes cells, and decides which cells to read and write from the cell values read so far.

## What it counts

The *query time* $t_q$ of a scheme is the largest number of probes of a query. In a dynamic structure, the *update time* $t_u$ is the number of cells that an update reads or writes, and bounds are worst-case or amortized over a sequence. The *space* is the number of cells $s$, or $sw$ bits. The parameters are the problem size $n$, the cell size $w$ and the space.

Everything else is free: computing the address of the next probe, computing the table function, and the size of the program. So a cell-probe lower bound does not depend on a complexity assumption: it comes from the limit on the information that $t$ cells of $w$ bits can carry. A cell-probe upper bound is not always an algorithm, because the table function may be hard to compute.

**A space bound by counting.** A table of $s$ cells of $w$ bits has $2^{sw}$ contents. If the scheme is correct, $T$ must give different tables to two data $d \neq d'$ for which some query has different answers. For membership, two different subsets of size $n$ differ on some element. So $2^{sw} \ge \binom{m}{n}$, that is $sw \ge \lg\binom{m}{n}$, whatever the number of probes. Example: $m = 2^{20}$ and $n = 1000$. Then $\lg\binom{m}{n} \approx 11\,469.9$ bits, so a table of 64-bit cells needs at least $180$ cells. A sorted table of $n$ cells of $20$ bits has $20\,000$ bits.

**Example.** Binary search on a sorted table of $n = 1000$ cells, each holding one key, probes at most $\lceil \lg(n+1) \rceil = 10$ cells. Yao's question was whether some other order of the $n$ keys in the $n$ cells, with each cell holding one key, allows fewer probes. He showed that for a universe that is large enough compared with $n$ the answer is no: among such permutation schemes, binary search on the sorted table is optimal in the number of probes. If the cells may hold arbitrary bits, or if there is a little extra space, the answer changes. For example, the scheme of Fredman, Komlós and Szemerédi (1984) uses $O(n)$ cells and answers membership with a constant number of probes (see [FKS perfect hashing](/fks-perfect-hashing/) and [hash table](/hash-table/)).

## Relation to other models

- **Word RAM.** A [word RAM](/word-ram/) data structure with cells of $w$ bits is a cell-probe structure whose probes are the memory accesses. The cell-probe model leaves out the cost of the instructions, so its time is at most the time of the word RAM. A lower bound on probes is a lower bound on the time of the word RAM, for the same $w$ and the same space.
- **Pointer machine.** A [pointer machine](/pointer-machine/) program is also a cell-probe scheme, if each node is stored in a few cells with $O(\log n)$ bits per cell. So cell-probe lower bounds hold for pointer machines. The converse is false. Predecessor search on keys from a universe of size $U$ needs $\Omega(\log n)$ time on a pointer machine, but the van Emde Boas structure answers it in $O(\log\log U)$ time on the word RAM, so with $O(\log\log U)$ probes.
- **Bit-probe model.** The [bit-probe model](/bit-probe-model/) is the case $w = 1$. A scheme with $t$ probes of $w$-bit cells is a bit-probe scheme with $tw$ probes.
- **Communication complexity.** A static scheme with $s$ cells of $w$ bits and $t$ probes gives a protocol for [communication complexity](/communication-complexity/): Alice holds the query $q$ and Bob holds the data $d$. In each of $t$ rounds Alice sends the $\lceil \lg s \rceil$ bits of the next address and Bob sends the $w$ bits of the cell. Alice sends $t\lceil \lg s \rceil$ bits in all, and Bob sends $tw$ bits. Miltersen, Nisan, Safra and Wigderson (1998) used this to turn lower bounds on asymmetric communication into lower bounds on the number of probes.
- **Unit-cost and logarithmic-cost models.** The [random access machine](/random-access-machine/) with unit cost charges for each instruction. The cell-probe model charges for memory only. Under [logarithmic cost](/logarithmic-cost-model/), each access is charged by the bit length of its operands. The cell-probe model fixes the word length at $w$ and charges one for each access.

## Known results in the model

**Predecessor search.** The [predecessor problem](/predecessor-problem/) is as follows. Store a set of $n$ keys of $\ell$ bits, and for a query $x$ return the largest key that is at most $x$. Ajtai (1988) proved the first lower bound that grows with the size of the problem. Beame and Fich (2002) proved bounds that are tight for polynomial space in some ranges of the parameters. Pătraşcu and Thorup (2006) found the tight bound for the whole range of parameters that their paper treats. Let the space be $S$ cells of $w$ bits, and set $a = \lg(Sw/n)$, so that $2^a$ is the number of bits of space for each key. Then the optimal query time of a static structure is
$$\Theta\!\left(\min\left\{\ \log_w n,\quad \lg\frac{\ell - \lg n}{a},\quad \frac{\lg(\ell/a)}{\lg\!\big(\frac{a}{\lg n}\lg\frac{\ell}{a}\big)},\quad \frac{\lg(\ell/a)}{\lg\!\big(\lg\frac{\ell}{a} \,/\, \lg\frac{\lg n}{a}\big)}\ \right\}\right),$$
where the lower bound is in the cell-probe model and matching upper bounds are known. Pătraşcu and Thorup (2007) proved that randomized query algorithms do no better. The first term is the cost of a [fusion tree](/fusion-tree/), whose fan-out is $w^{\Theta(1)}$, so its depth is $\Theta(\log_w n)$. The second term is the cost of a van Emde Boas style recursion, in which each probe halves the number of bits of the key. With linear space, $2^a = \Theta(w)$ and so $a = \Theta(\lg w)$. The first and second terms match the fusion tree and the van Emde Boas recursion of the [word RAM](/word-ram/) page. See [predecessor lower bound](/predecessor-lower-bound/) for the statement and the proof technique.

**Dynamic partial sums.** The problem: keep an array $A[1..n]$ of $w$-bit integers under *update*$(i, \Delta)$, which adds $\Delta$ to $A[i]$, and *query*$(i)$, which returns $A[1] + \dots + A[i]$. A balanced binary tree gives $O(\log n)$ cells for each operation. Fredman and Saks (1989) proved a lower bound for it in the model with the *chronogram* technique. The idea: look at the last updates before a query in epochs whose sizes grow geometrically, with a ratio that depends on $w$ and $t_u$. The answer of a query depends on all epochs. A query must read a cell last written in each epoch that matters, and there are about $\log n / \log(w\,t_u)$ such epochs. The bound is $t_q = \Omega(\lg n / \lg(w\,t_u))$, and for cells of $O(\log n)$ bits the largest of the amortized update time and the query time is $\Omega(\log n / \log\log n)$. Pătraşcu and Demaine (2006) proved $\Omega(\log n)$, which matches the tree, for partial sums with enough bits for each item. The highest lower bounds known for explicit problems are about $(\lg n / \lg\lg n)^2$ for dynamic problems (Larsen 2012, for dynamic range counting; Larsen, Weinstein and Yu 2018, for Boolean queries) and about $\lg n / \lg(Sw/n)$ for static problems with space $S$ (Larsen 2012, for polynomial evaluation). Proving a bound of $\omega(\lg n)$ for an explicit static problem with linear space is open.

**Union-find.** Fredman and Saks (1989) proved that the union-find problem needs $\Omega(\alpha(m,n))$ amortized time per operation in the model, for cells of $O(\log n)$ bits. This is the matching bound for the algorithm of Tarjan, and it holds with no condition on the structure (see [union-find lower bound](/union-find-lower-bound/) and the weaker condition of separability on the [pointer machine](/pointer-machine/)).

## References
