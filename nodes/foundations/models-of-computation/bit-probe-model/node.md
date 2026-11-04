---
tag: J7N6B1
kind: model
slug: bit-probe-model
name: Bit-probe model
aliases:
- bit probe model
area: foundations/models-of-computation
level: research
summary: Cell-probe variant where each probe reads a single bit of memory.
prereqs: [cell-probe-model, asymptotic-notation]
see_also: [word-ram, fks-perfect-hashing, hash-table, succinct-data-structures, communication-complexity, predecessor-problem, bloom-filter]
sources:
  - paper: "Harry Buhrman, Peter Bro Miltersen, Jaikumar Radhakrishnan and Srinivasan Venkatesh, Are bitvectors optimal?, Proceedings of the 32nd ACM Symposium on Theory of Computing (STOC 2000), 449 to 458; journal version in SIAM Journal on Computing 31(6) (2002), 1723 to 1744"
    locator: abstract of the journal version (the one-probe randomized bounds with two-sided and one-sided error, and the deterministic trade-offs between space and probes)
  - paper: "Peter Bro Miltersen, Cell probe complexity: a survey, Advances in Data Structures Workshop (pre-conference workshop of FSTTCS 1999)"
    locator: the sections on the bit-probe model and on membership
  - paper: "Andrew Chi-Chih Yao, Should tables be sorted?, Journal of the ACM 28(3) (1981)"
    locator: the definition of the cell-probe model
  - paper: "Michael L. Fredman, Janos Komlos and Endre Szemeredi, Storing a sparse table with O(1) worst case access time, Journal of the ACM 31(3) (1984)"
    locator: abstract (constant worst-case query time with linear space)
  - paper: "Andrej Brodnik and J. Ian Munro, Membership in constant time and almost-minimum space, SIAM Journal on Computing 28(5) (1999)"
    locator: abstract (space close to the information bound)
  - paper: "Rasmus Pagh, Low redundancy in static dictionaries with constant query time, SIAM Journal on Computing 31(2) (2001)"
    locator: abstract
  - book: "Marvin Minsky and Seymour Papert, Perceptrons: An Introduction to Computational Geometry, MIT Press, 1969"
    locator: the discussion of time versus memory for the exact match and best match problems
  - paper: "Peter Elias and Richard A. Flower, The complexity of some simple retrieval problems, Journal of the ACM 22(3) (1975)"
    locator: the model of retrieval by bit probes
  - paper: "Jaikumar Radhakrishnan, Venkatesh Raman and S. Srinivasa Rao, Explicit deterministic constructions for membership in the bitprobe model, Proceedings of the 9th European Symposium on Algorithms (ESA 2001), Lecture Notes in Computer Science 2161"
    locator: abstract (explicit schemes with few probes)
  - paper: "Mohit Garg and Jaikumar Radhakrishnan, Set membership with a few bit probes, arXiv:1504.02035 (2015)"
    locator: Section 1 (the summary of the bounds of Buhrman et al. and the improved bounds for two, three and more probes)
---

The bit-probe model is the [cell-probe model](/cell-probe-model/) with cells of one bit ($w = 1$). A data structure is a string of $s$ bits, and the cost of a query is the number of bits that it reads. The model measures what a structure must do when it can read only one bit at a time. The main problem in it is *set membership*, the [static dictionary problem](/static-dictionary-problem/) without values: store a set of $n$ elements of a universe of size $m$ so that the query "is $x$ in the set?" reads few bits. The model is older than the cell-probe model: Minsky and Papert (1969) studied membership with bit probes in *Perceptrons*, and Elias and Flower (1975) studied retrieval problems in it.

## The machine

**Static structures.** The data are drawn from a set $\mathcal D$. A *scheme* with $s$ bits and $t$ probes has a table function $T : \mathcal D \to \{0,1\}^s$, which is any function with no cost, and a query algorithm for each query $q$: a binary [decision tree](/decision-tree-model/) of depth at most $t$. Each internal node names a position in $\{1, \dots, s\}$, and its two children are for the value $0$ and the value $1$ of the bit at that position. Each leaf holds an answer. The scheme is correct if the leaf reached on $T(d)$ holds $f(d,q)$ for all $d$ and $q$. A scheme is *non-adaptive* if all the nodes of one level of the tree name the same position, so that the positions that the algorithm reads depend on $q$ only. A scheme is *adaptive* if the next position can depend on the bits read so far. A randomized scheme lets the query algorithm use random bits and allows an error probability.

**Membership.** The data are the subsets $S$ of size $n$ of the universe $\{0, \dots, m-1\}$, the queries are the elements $x$, and the answer is $1$ if $x \in S$. Write $B = \lceil \lg\binom{m}{n} \rceil$ for the [information bound](/information-theoretic-bound/).

## What it counts

The cost is the number of probes $t$ (bits read) and the space $s$ in bits. Computation is free, as in the cell-probe model. So the model has two parameters, and the interest is in the trade-off between $s$ and $t$.

**Space.** A table of $s$ bits has $2^s$ contents. For membership, two different sets differ on some element, so a correct scheme gives them different tables. Hence $2^s \ge \binom{m}{n}$ and $s \ge B$, whatever the number of probes.

**Example.** Let $m = 2^{20}$ and $n = 1000$. Then $B = 11\,470$. A bit vector (one bit for each element) uses $2^{20} = 1\,048\,576$ bits and 1 probe. A sorted table of $n$ keys of $20$ bits uses $20\,000$ bits, and binary search reads at most $\lceil \lg 1001 \rceil = 10$ keys, so at most $200$ bits.

## Relation to other models

- **Cell-probe model.** The [cell-probe model](/cell-probe-model/) with cells of $w$ bits is related to the bit-probe model by two simple facts. A scheme with $t$ probes of $w$-bit cells is a bit-probe scheme with at most $tw$ probes, because a probe reads the $w$ bits of the cell one by one. A bit-probe scheme with $t$ probes is a cell-probe scheme with $t$ probes, if the $s$ bits are grouped in cells of $w$ bits. So, with $s$ bits on one side matched by $\lceil s/w \rceil$ cells of $w$ bits on the other, the bit-probe time of a problem is at least its cell-probe time and at most $w$ times its cell-probe time.
- **Word RAM.** A bit-probe lower bound on the time $t$ gives a lower bound of $t/w$ probes of $w$-bit cells, and so a lower bound for the [word RAM](/word-ram/) of $t/w$ steps.
- **Communication complexity.** A bit-probe scheme with $s$ bits and $t$ probes gives a protocol for [communication complexity](/communication-complexity/) with $t\lceil \lg s \rceil$ bits from Alice (the query) and $t$ bits from Bob (the data).

## Known results in the model

Here $m$ is the size of the universe, $n$ is the size of the set, and $B = \lceil \lg\binom{m}{n} \rceil$.

**The bit vector.** The bit vector has $s = m$ and $t = 1$. Buhrman, Miltersen, Radhakrishnan and Venkatesh (2000) asked whether it is optimal: can a scheme use fewer than $m$ bits with a small number of probes?

**One deterministic probe: the bit vector is optimal.** Claim: if $m \ge 3$ and $1 \le n \le m - 1$, every deterministic scheme for membership with $t = 1$ probe has $s \ge m$. Proof. The query algorithm for $x$ reads one position $p(x)$, which depends on $x$ only, and the answer is a function $g_x$ of the bit that it read. There are four functions of one bit. The function $g_x$ is not constant: the sets of size $n$ that contain $x$ and the sets that do not contain $x$ both exist (since $1 \le n \le m-1$), and a constant answer is wrong for one of the two kinds. So $g_x$ is the identity or the negation, and there is a constant $c_x$ with $[x \in S] = T(S)_{p(x)} \oplus c_x$ for every set $S$. Suppose that $x \ne y$ and $p(x) = p(y)$. Then $[x \in S] \oplus [y \in S] = c_x \oplus c_y$ for every $S$. If $n \ge 2$, a set with both $x$ and $y$ exists (it gives $0$), and since $n \le m-1$ a set with $x$ and without $y$ exists (it gives $1$). If $n = 1$, the set $\{x\}$ gives $1$, and the set $\{z\}$ with $z \ne x, y$, which exists since $m \ge 3$, gives $0$. In both cases this is a contradiction. So the positions $p(x)$ for different $x$ are different, and $s \ge m$. $\square$

**More probes can save space.** Example with $m = 4$ and $n = 2$. There are $6$ sets, so $B = 3$. The claim says that a scheme with $3$ bits cannot have one probe, and the bit vector uses $4$ bits. But $3$ bits suffice with at most $2$ probes. List the sets as $r = 0, \dots, 5$ in this order: $\{0,1\}, \{0,2\}, \{0,3\}, \{1,2\}, \{1,3\}, \{2,3\}$. Store $r$ in binary as bits $u_2 u_1 u_0$. Then the queries are as follows.

- $x = 2$: $x \in S$ if and only if $u_0 = 1$.
- $x = 0$: read $u_1$. If $u_1 = 0$, then $x \in S$ if and only if $u_2 = 0$. If $u_1 = 1$, then $x \in S$ if and only if $u_0 = 0$.
- $x = 1$: read $u_0$. If $u_0 = 0$, then $x \in S$ if and only if $u_1 = 0$. If $u_0 = 1$, then $x \in S$ if and only if $u_1 = 1$.
- $x = 3$: read $u_1$. If $u_1 = 0$, then $x \in S$ if and only if $u_2 = 1$. If $u_1 = 1$, then $x \in S$ if and only if $u_0 = 0$.

The scheme is adaptive. By the claim, a scheme with $3$ bits cannot have one probe, so $2$ probes are the least for $3$ bits.

**Randomized one-probe schemes.** Buhrman, Miltersen, Radhakrishnan and Venkatesh showed that randomization changes the answer for one probe. With two-sided error $\varepsilon$ on each query, one probe suffices with $O\big(\frac{n}{\varepsilon^2} \log m\big)$ bits, and $\Omega\big(\frac{n}{\varepsilon \log(1/\varepsilon)} \log m\big)$ bits are necessary. For a constant $\varepsilon$ this is $\Theta(n \log m)$ bits, which is much less than $m$ for $n \ll m / \log m$. The scheme is shown to exist by a probabilistic argument and is not explicit. With one-sided error (no error on the elements of the set, error $\varepsilon$ on the others), one-probe schemes need $\Omega\big(\frac{n^2}{\varepsilon^2 \log(n/\varepsilon)} \log m\big)$ bits, and $O\big(\frac{n^2}{\varepsilon^2} \log m\big)$ bits suffice, so the space is roughly quadratic in $n$. The claim does not hold for randomized schemes: its proof needs every answer to be correct.

**Near-optimal space with $O(\log m)$ bit probes.** Hashing gives schemes with about $n \lg m$ bits. The scheme of Fredman, Komlós and Szemerédi (1984) reads $O(1)$ cells of $\lceil \lg m \rceil$ bits, so it reads $O(\log m)$ bits, and it uses $O(n)$ cells, that is $O(n \log m)$ bits. Brodnik and Munro (1999) and Pagh (2001) reduced the space to a number of bits close to $B$ (the information bound plus a lower-order term), with a constant number of probes of cells of $O(\log m)$ bits. In the bit-probe model this is $O(\log m)$ probes. See [FKS perfect hashing](/fks-perfect-hashing/) and [succinct data structures](/succinct-data-structures/).

**The trade-off for a few probes.** Buhrman et al. also study deterministic schemes with $t \ge 2$ probes. Their lower bound holds for adaptive schemes, and so for non-adaptive ones: if $n \le m^{1-\varepsilon}$ for a constant $\varepsilon > 0$ and $t$ is small compared with $\lg m$, then $s = \Omega(t\, m^{1/t} n^{1-1/t})$. Their upper bound is a non-adaptive scheme with $O(t\, m^{4/(t+1)} n)$ bits for odd $t \ge 5$ and $n \le m^{1-\varepsilon}$, shown to exist by a probabilistic argument. So for a constant $t \ge 5$ and a small $n$, the space is $o(m)$, and the number of bits for each element falls as $t$ grows. The gap between these bounds is the subject of later work. Radhakrishnan, Raman and Rao (2001) gave explicit deterministic schemes for few probes. Garg and Radhakrishnan (2015) improved the bounds for two and three probes and gave better adaptive and non-adaptive schemes for larger odd $t$.

## References
