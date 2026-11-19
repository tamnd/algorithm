---
title: Lattice alignment gives a totally ordered network whose consensus minimizes the expected slot errors
proves: [correctness]
status: full
---

We use the notation of the page. The lattice has node times, and every arc $e$ goes from a node $u$ to a node $v$ with $\mathrm{time}(u) < \mathrm{time}(v)$. We write $I(e)$ and $F(e)$ for these two times. A path is a sequence of arcs from the start to a final node, and $P(\pi) = e^{\kappa S(\pi)} / Z$ is its posterior. The posterior of an arc is $\gamma(e) = \sum_{\pi \ni e} P(\pi)$. Line L1 computes it exactly by forward-backward, as proved on the page [word lattice](/word-lattice/). We take the threshold $\theta = 0$ until the last remark, so the kept arcs are the arcs with $\gamma(e) > 0$, that is, the arcs on at least one path.

For two kept arcs, $e \prec f$ means that a path of kept arcs leads from the end node of $e$ to the start node of $f$ (line L2). If $e \prec f$, then $F(e) \le I(f)$, so $I(e) < F(e) \le I(f)$.

**Lemma 0.** For kept arcs $e \neq f$, $e \prec f$ if and only if some path of the lattice holds both, with $e$ first.

*Proof.* If a path holds $e$ and later $f$, its arcs between them lead from the end of $e$ to the start of $f$, and they are kept because they lie on a path. Conversely, let $e \prec f$ through kept arcs. Take a path through $e$ and cut it after $e$, take the connecting arcs, and take a path through $f$ from the start node of $f$ on. Since every arc moves forward in time, this is a path, and it holds $e$ and then $f$. $\square$

A class order is a relation $<$ on the classes that is irreflexive and transitive. It is *consistent* if $e \prec f$ implies $[e] < [f]$, where $[e]$ is the class of $e$. The code stores $<$ as the sets $\mathrm{succ}(c) = \{ d : c < d \}$.

**Lemma 1 (initial order).** After line L3, the sets $\mathrm{succ}$ are a consistent class order.

*Proof.* Every class has one start time, and $c$ gets $d$ as a successor only if $d$ starts later. Line L3 adds $d$ if some arc of $c$ precedes some arc of $d$, together with all successors of $d$, which were computed earlier because $d$ starts later. By induction on the start time from the last, $\mathrm{succ}(c)$ is the transitive closure of this direct relation, and it is irreflexive since start times strictly increase along it. If $e \prec f$, then $I(e) < I(f)$, so $[e] \neq [f]$, the class of $f$ starts later, and line L3 puts $[f]$ in $\mathrm{succ}([e])$. $\square$

**Lemma 2 (merging).** Let $<$ be a consistent class order and let $a \neq b$ be unordered: neither $a < b$ nor $b < a$. After $\mathrm{MERGE}(a, b)$ the sets $\mathrm{succ}$ are again a consistent class order on the new classes.

*Proof.* Let $P = \{ x : x < a \text{ or } x < b \}$ and $S = \{ y : a < y \text{ or } b < y \}$. The code sets $\mathrm{succ}(m) = S$ for the merged class $m$ and adds $S \cup \{m\}$ to $\mathrm{succ}(x)$ for each $x \in P$. Other classes keep their sets, and none of them held $b$, since all classes before $b$ are in $P$. So the new relation is: $x <' y$ if $x < y$ for old classes, $x <' m$ for $x \in P$, $m <' y$ for $y \in S$, and $x <' y$ for $x \in P$ and $y \in S$.

$P$ and $S$ are disjoint, and neither contains $a$ or $b$. If $z \in P \cap S$, then one of $a < z < a$, $b < z < b$, $a < z < b$ or $b < z < a$ holds. The first two break irreflexivity by transitivity, and the last two order $a$ and $b$. If $a \in S$, then $a < a$ or $b < a$, which is excluded, and the other cases are alike.

Irreflexive: $m <' m$ would need $m \in S$, and $x <' x$ for an old class $x$ would need $x < x$ or $x \in P \cap S$.

Transitive: let $x <' y <' z$. If both steps are old pairs, $x < z$. If $y = m$, then $x \in P$ and $z \in S$, so $x <' z$. If $x <' y$ is a $P \times S$ pair or $x = m$, then $y \in S$, and $y <' z$ is either an old pair, which gives $z \in S$ by transitivity, or a $P \times S$ pair or a step into $m$, and both need $y \in P$, which is impossible. So $x <' z$. The case where $y <' z$ is a $P \times S$ pair or $z = m$ is symmetric, with $y \in P$.

Consistent: if $e \prec f$, the old order has $[e] < [f]$. If neither class is $a$ or $b$, the pair is kept. If $[e] \in \{a, b\}$, then $[f] \in S$, so $m <' [f]$, and if $[f] \in \{a, b\}$, then $[e] \in P$. Both cannot be in $\{a, b\}$, because $a$ and $b$ are unordered and $<$ is irreflexive. $\square$

**Corollary 1 (classes hold no ordered arcs).** At every step, two arcs $e \neq f$ in one class satisfy neither $e \prec f$ nor $f \prec e$. So by Lemma 0, no path holds two arcs of one class.

*Proof.* Consistency gives $[e] < [f]$ from $e \prec f$, and $<$ is irreflexive. $\square$

**Lemma 3 (termination and a total order).** The two loops stop after at most $E - 1$ merges, and at the end every two classes are ordered.

*Proof.* Each merge removes one class. The loop of line L6 merges whenever some pair is unordered, with any similarity, so it stops only when every pair is ordered. $\square$

With a total strict order on $L$ classes, the $i$-th class from the left has exactly $L - 1 - i$ successors, so sorting by the number of successors gives the order. These classes are the slots.

**Theorem 1 (every path is a network path).** For every path $\pi = e_1 e_2 \cdots e_m$ of the lattice, the slots of its arcs strictly increase. So $\pi$ is a path of the network that takes the word of $e_j$ in the slot of $e_j$ and $\varepsilon$ in every other slot.

*Proof.* All arcs of $\pi$ are kept, and $e_j \prec e_{j+1}$, so consistency gives that the slot of $e_j$ is before the slot of $e_{j+1}$. $\square$

**Theorem 2 (slot posteriors).** For a slot $C_i$ and a word $w$, line L8 computes

$$p_i(w) = \sum_{e \in C_i,\ \mathrm{word}(e) = w} \gamma(e) = \Pr_\pi\big[\pi \text{ has an arc with the word } w \text{ in } C_i\big],$$

the slot mass $\sum_w p_i(w)$ is at most 1, and $p_i(\varepsilon)$ from line L9 is the posterior of the paths with no arc in $C_i$.

*Proof.* Expand $\gamma(e) = \sum_\pi P(\pi) [e \in \pi]$ and swap the sums. By Corollary 1, a path has at most one arc in $C_i$, so $\sum_{e \in C_i, \mathrm{word}(e) = w} [e \in \pi]$ is 0 or 1, and it is 1 exactly when $\pi$ has an arc with the word $w$ in $C_i$. For the same reason the events for different words are disjoint, so the mass is the probability that $\pi$ has an arc in $C_i$, which is at most 1, and $1$ minus it is the probability of no arc. $\square$

**Theorem 3 (consensus).** Map each path $\pi$ to its slot sequence $r(\pi) = (r_1, \ldots, r_L)$, with a word or $\varepsilon$ in each slot, as in Theorem 1. For a choice $c = (c_1, \ldots, c_L)$ of a word or $\varepsilon$ per slot, let the slot error be $\mathrm{SE}(c, r) = |\{ i : c_i \neq r_i \}|$. Then

$$\mathbb{E}_\pi\big[\mathrm{SE}(c, r(\pi))\big] = \sum_{i=1}^L \big(1 - p_i(c_i)\big),$$

which is what `expected_errors` returns, and the choice of line L10, the largest $p_i$ in each slot, minimizes it. Moreover, $\mathrm{SE}(c, r) \ge d(c, r)$, the word edit distance between the two word sequences after the $\varepsilon$ are dropped.

*Proof.* By linearity of expectation, the expected slot error is $\sum_i \Pr[r_i \neq c_i] = \sum_i (1 - \Pr[r_i = c_i])$, and $\Pr[r_i = c_i] = p_i(c_i)$ by Theorem 2, for words and for $\varepsilon$. The terms depend on different $c_i$, so the sum is smallest when each $c_i$ maximizes $p_i(c_i)$. For the bound, the slots align the two sequences: a slot with $\varepsilon$ in both is skipped, equal words are matches, and the other slots are substitutions, insertions or deletions. This is one alignment, its cost is $\mathrm{SE}(c, r)$, and the edit distance is the smallest cost of any alignment. $\square$

So the consensus minimizes the expected slot error exactly, and the expected slot error is an upper bound on the expected word error of the same hypothesis. The consensus therefore only approximately minimizes the expected word error. The bound is tight when the alignment by slots is optimal for the pairs that carry most of the posterior mass, which the clustering tries to achieve but does not guarantee: the problem of the best multiple alignment has no known efficient solution, and the clustering is a heuristic.

**Remark (a threshold $\theta > 0$).** The order of line L2 then uses only the kept arcs, which is the purpose of pruning: unlikely paths no longer force likely words into different slots. Lemma 0 fails, two arcs in a class can lie on one lattice path through pruned arcs, and the slot mass can exceed 1 by at most the posterior of such paths. Lemmas 1 to 3 and the minimization in Theorem 3 over the computed slot posteriors still hold. The code sets $p_i(\varepsilon)$ to 0 when the mass is above $1 - 10^{-12}$, which also absorbs rounding. Theorem 1 holds for the paths that use only kept arcs.
