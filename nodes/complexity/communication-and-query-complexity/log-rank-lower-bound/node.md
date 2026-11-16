---
tag: Y9M627
kind: theorem
slug: log-rank-lower-bound
name: Log-rank lower bound
aliases:
- rank lower bound
- log-rank bound
- Mehlhorn-Schmidt rank bound
area: complexity/communication-and-query-complexity
level: advanced
summary: "The deterministic communication cost of a Boolean function is at least log2 of the rank of its communication matrix over the reals: D^cc(f) >= log2 rank(M_f) (Mehlhorn and Schmidt, 1982)."
prereqs: [deterministic-communication-complexity, communication-matrix, rank]
see_also: [log-rank-conjecture, fooling-set-method, nondeterministic-communication-complexity, randomized-communication-complexity, sign-rank, inner-product-problem, equality-problem, gaussian-elimination]
sources:
  - paper: doi:10.1145/800070.802208
    title: "Kurt Mehlhorn and Erik M. Schmidt, Las Vegas is better than determinism in VLSI and distributed computing (extended abstract), Proceedings of the 14th Annual ACM Symposium on Theory of Computing (STOC 1982), pages 330-337"
    locator: the rank lower bound on deterministic communication
  - book: isbn:9780521560672
    title: Eyal Kushilevitz and Noam Nisan, Communication Complexity, Cambridge University Press, 1997
    locator: Chapter 1, Basics (Section 1.4, Rank Lower Bound), and Chapter 2 (Section 2.5, On Rank and Covers)
  - book: isbn:9781108497985
    title: Anup Rao and Amir Yehudayoff, Communication Complexity and Applications, Cambridge University Press, 2020
    locator: Chapter 2, Rank (sections Communication Complexity and Rank, and Lower Bounds Based on Rank)
  - paper: doi:10.1137/16M1059369
    title: "Mika Göös, Toniann Pitassi and Thomas Watson, Deterministic communication vs. partition number, SIAM Journal on Computing 47(6) (2018), pages 2435-2450 (FOCS 2015)"
    locator: Theorem 2 and its corollary (a function with deterministic cost about the square of the log of the rank)
---

The log-rank lower bound says that a deterministic protocol for a Boolean function $f$ must send at least $\log_2 \operatorname{rank}(M_f)$ bits, where $M_f$ is the [communication matrix](/communication-matrix/) and the rank is over the real numbers. Mehlhorn and Schmidt proved it in 1982. The proof shows that each leaf of a protocol adds a matrix of rank at most 1, so the measure it bounds is the number of leaves, the same count as the [fooling set method](/fooling-set-method/), but through linear algebra. This page proves the bound; the [log-rank conjecture](/log-rank-conjecture/) asks whether it is tight up to a polynomial, which is open.

## Statement

Let $f : X \times Y \to \{0,1\}$, let $M_f$ be its communication matrix, and let $J$ be the all-ones matrix of the same size. All ranks are over $\mathbb{R}$. Let $D^{cc}(f)$ be the [deterministic communication complexity](/deterministic-communication-complexity/) of $f$, where both players know the answer at the end.

**Theorem (Mehlhorn and Schmidt).** Every deterministic protocol for $f$ has at least $\operatorname{rank}(M_f)$ leaves with output 1. Hence

$$D^{cc}(f) \ge \log_2 \operatorname{rank}(M_f).$$

**Refined form.** Every deterministic protocol for $f$ has at least $\operatorname{rank}(M_f) + \operatorname{rank}(J - M_f)$ leaves, so for $f$ that is not constant

$$D^{cc}(f) \ge \big\lceil \log_2 \big( \operatorname{rank}(M_f) + \operatorname{rank}(J - M_f) \big) \big\rceil \ge \big\lceil \log_2 \big( 2 \operatorname{rank}(M_f) - 1 \big) \big\rceil.$$

The bound holds with the rank over any field. For a 0-1 matrix the rank over $\mathbb{R}$ is at least the rank over any other field, so the real rank gives the strongest bound.

## In plain words

Write the answers to all input pairs in a table, with one row for each input of Alice and one column for each input of Bob. The rank of the table measures how many truly different patterns its rows have.

Each ending of a protocol covers a block of the table: some rows and some columns, all with the same answer. Such a block has the simplest possible pattern. Adding the blocks of all the endings with answer one gives back the whole table, and each block can add at most one new pattern. So the protocol needs at least as many endings as the table has patterns.

A talk of a given length has a limited number of endings. So a table with many patterns needs a long talk. The length is at least the number of binary digits of the rank.

## Proof

Fix a deterministic protocol $P$ for $f$. Let $L_1$ be the set of its leaves with output 1 and $L_0$ the set of its leaves with output 0.

**Step 1: leaves are rectangles.** For a leaf $\ell$, the inputs that reach $\ell$ form a rectangle $R_\ell = A_\ell \times B_\ell$, with $A_\ell \subseteq X$ and $B_\ell \subseteq Y$. This holds for every node, by induction from the root: the root has $X \times Y$, and an Alice node splits $A$ by the bit that Alice sends while $B$ stays the same, so both children again have rectangles; a Bob node splits $B$ in the same way. Every input reaches exactly one leaf, so the rectangles $R_\ell$ are disjoint and cover $X \times Y$.

**Step 2: a sum of rank-1 matrices.** Since $P$ computes $f$, the leaf $\ell(x, y)$ reached by $(x, y)$ is in $L_1$ exactly when $f(x, y) = 1$. Let $\mathbf{1}_A$ be the 0-1 column vector of a set $A \subseteq X$ and $\mathbf{1}_B$ the one of $B \subseteq Y$. The matrix $\mathbf{1}_{A_\ell} \mathbf{1}_{B_\ell}^{\mathsf T}$ has a 1 exactly on the entries of $R_\ell$, and its rank is at most 1. The rectangles are disjoint, so

$$M_f = \sum_{\ell \in L_1} \mathbf{1}_{A_\ell} \mathbf{1}_{B_\ell}^{\mathsf T}, \qquad J - M_f = \sum_{\ell \in L_0} \mathbf{1}_{A_\ell} \mathbf{1}_{B_\ell}^{\mathsf T}.$$

**Step 3: subadditivity.** The rank of a sum is at most the sum of the ranks. So $\operatorname{rank}(M_f) \le |L_1|$ and $\operatorname{rank}(J - M_f) \le |L_0|$, and the number of leaves is

$$|L_0| + |L_1| \ge \operatorname{rank}(M_f) + \operatorname{rank}(J - M_f).$$

**Step 4: depth.** A binary tree of depth $c$ has at most $2^c$ leaves. So $2^c \ge \operatorname{rank}(M_f)$, which gives the theorem, and $c \ge \lceil \log_2(\operatorname{rank}(M_f) + \operatorname{rank}(J - M_f)) \rceil$, since $c$ is an integer. For the last form, $M_f = J - (J - M_f)$ gives $\operatorname{rank}(M_f) \le 1 + \operatorname{rank}(J - M_f)$.

**The field.** Steps 2 to 4 use only that the rank is subadditive and that $\mathbf{1}_A \mathbf{1}_B^{\mathsf T}$ has rank at most 1, which hold over every field. For a matrix with integer entries, a nonzero minor modulo a prime $p$ is a nonzero integer, so the rank over $\mathrm{GF}(p)$ is at most the rank over $\mathbb{Q}$, which equals the rank over $\mathbb{R}$. $\blacksquare$

## Consequences

**Exact costs.** The refined form gives $D^{cc} = n + 1$ for several standard functions on $n$-bit inputs, with the trivial protocol as the matching upper bound:

| Function | $\operatorname{rank}(M_f)$ | $\operatorname{rank}(J - M_f)$ | $\operatorname{rank}(M_f)$ over $\mathrm{GF}(2)$ | Bound on leaves | $D^{cc}$ |
|---|---|---|---|---|---|
| [Equality](/equality-problem/) | $2^n$ | $2^n$ | $2^n$ | $2^{n+1}$ | $n + 1$ |
| [Greater-than](/greater-than-problem/) | $2^n - 1$ | $2^n$ | $2^n - 1$ | $2^{n+1} - 1$ | $n + 1$ |
| [Disjointness](/disjointness-problem/) | $2^n$ | $2^n - 1$ | $2^n$ | $2^{n+1} - 1$ | $n + 1$ |
| [Inner product](/inner-product-problem/) | $2^n - 1$ | $2^n$ | $n$ | $2^{n+1} - 1$ | $n + 1$ |

The first two rank columns are over $\mathbb{R}$. The ranks agree with an exact computation for $n = 1$ to $5$, and the values $D^{cc} = n + 1$ agree with an exhaustive search over all protocols for $n = 1, 2, 3$. For inner product, the rank over $\mathrm{GF}(2)$ gives only $\log_2 n$, while the real rank gives $n + 1$. This is the example that shows why the field matters.

**An upper bound in terms of rank.** A 0-1 matrix of rank $r$ has at most $2^r$ distinct rows, because each row is fixed by its entries in $r$ columns that span the column space. Alice can send the type of her row with $r$ bits, and Bob replies with the answer. So

$$\log_2 \operatorname{rank}(M_f) \le D^{cc}(f) \le \operatorname{rank}(M_f) + 1.$$

The gap between the two sides is exponential. The [log-rank conjecture](/log-rank-conjecture/) says that the lower side is the truth, up to a polynomial.

**The bound is only for deterministic protocols.** The argument needs the leaf rectangles to be disjoint and exactly correct.

- For nondeterministic protocols the rectangles of a cover may overlap, and the bound fails. Non-equality $\mathrm{NE} = 1 - \mathrm{EQ}$ has $\operatorname{rank}(J - I) = 2^n$ for $n \ge 1$, but its 1-entries are covered by the $2n$ rectangles $\{x : x_i = b\} \times \{y : y_i \ne b\}$, so its [nondeterministic cost](/nondeterministic-communication-complexity/) is at most $\lceil \log_2(2n) \rceil$.
- For randomized protocols the bound fails too. Equality has rank $2^n$ but [randomized cost](/randomized-communication-complexity/) $O(1)$ with public coins. Randomized lower bounds use the approximate rank, the rank of a matrix that is close to $M_f$ entrywise, and unbounded-error protocols are described by the [sign rank](/sign-rank/).

## Tightness

The bound is tight for equality, greater-than, disjointness and inner product, where it gives the exact value $n + 1$.

It is not tight in general. Let $r = \operatorname{rank}(M_f)$.

- Kushilevitz (1994) gave a function with $D^{cc}(f) \ge \Omega((\log r)^{\log_3 6})$, where $\log_3 6 \approx 1.63$. This was the largest known gap for about twenty years.
- Göös, Pitassi and Watson (2018, Theorem 2 and its corollary) gave a function with $D^{cc}(f) \ge \tilde{\Omega}((\log r)^2)$, where $\tilde{\Omega}$ hides factors polylogarithmic in $\log r$.
- The best known general upper bound is $D^{cc}(f) = O(\sqrt{r})$, by Sudakov and Tomon (2024), after $O(\sqrt{r} \log r)$ by Lovett (2016).

So the truth for the worst function lies between $(\log r)^{2 - o(1)}$ and $O(\sqrt{r})$. The [log-rank conjecture](/log-rank-conjecture/) page gives these results with their sources.

## History

Mehlhorn and Schmidt proved the rank bound in their STOC 1982 paper, which compares Las Vegas (zero-error randomized) protocols with deterministic ones. Lovász and Saks stated the log-rank conjecture in 1988. The textbooks of Kushilevitz and Nisan (1997) and of Rao and Yehudayoff (2020) present the bound together with the fooling set method, and the comparison between the two methods goes back to Aho, Ullman and Yannakakis (1983).

## References
