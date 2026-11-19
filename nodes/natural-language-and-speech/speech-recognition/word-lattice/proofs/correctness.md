---
title: The lattice queries compute path sums, posteriors and beam pruning exactly
proves: [correctness]
status: full
---

We use the notation of the page. A lattice is a finite directed acyclic graph with a start node $s$ and a set $F$ of final nodes. A path is a sequence of arcs from $s$ to a node of $F$. For an arc weight $w$ in a commutative semiring $(K, \oplus, \otimes, \bar 0, \bar 1)$, the weight of a path is the $\otimes$-product of its arc weights. Since the graph is acyclic, there are finitely many paths, and all sums below are finite.

**Lemma 1 (forward).** After LATTICE-FORWARD, for every node $v$,

$$\alpha(v) = \bigoplus_{\pi : s \leadsto v} w(\pi),$$

the sum over all arc sequences from $s$ to $v$, with $\alpha(s) = \bar 1$ for the empty sequence.

*Proof.* Line L1 gives an order in which every arc goes from an earlier node to a later one. We show by induction along this order that when line L3 reaches $u$, $\alpha(u)$ already has its final value. A path to $u$ is empty (only for $u = s$, which gives the $\bar 1$ of line L2) or ends with an arc $a$ from some $u'$ that comes before $u$ in the order. When $u'$ was processed, $\alpha(u')$ was final by induction, and line L4 added $\alpha(u') \otimes w(a)$ to $\alpha(u)$. By distributivity, $\alpha(u') \otimes w(a)$ is the sum over the paths to $u$ whose last arc is $a$. Each path to $u$ has exactly one last arc, so the sum over all arcs into $u$ is the sum over all paths to $u$. No later step changes $\alpha(u)$, since line L4 changes only the targets of arcs out of the node being processed, and they come after it. $\square$

**Lemma 2 (backward).** After LATTICE-BACKWARD, $\beta(v) = \bigoplus_{\pi : v \leadsto F} w(\pi)$, the sum over the arc sequences from $v$ to any final node, with the empty sequence counting $\bar 1$ when $v \in F$.

*Proof.* The same induction in reverse order, with line L5 for the empty paths and line L7 for the first arc. $\square$

**Corollary 1 (the three totals).** The sum $\bigoplus_{q \in F} \alpha(q)$ is

- the number of paths, in the counting semiring with all weights 1;
- the best combined score $\max_\pi \sum_{a \in \pi} s(a)$, in the Viterbi semiring $(\max, +)$;
- $\log \sum_\pi e^{\kappa S(\pi)}$, in the log semiring $(\mathrm{logadd}, +)$ with weights $\kappa\, s(a)$, where $S(\pi) = \sum_{a \in \pi} s(a)$.

The best path is read back from the arcs that gave each maximum, and by the same induction it is a path with the best score.

**Lemma 3 (arc posteriors).** Define the posterior of a path as $P(\pi) = e^{\kappa S(\pi)} / Z$ with $Z = \sum_\pi e^{\kappa S(\pi)}$. Then, for every arc $a$ from $u$ to $v$, line L8 gives

$$\gamma(a) = \exp\big(\alpha(u) + \kappa s(a) + \beta(v) - \log Z\big) = \sum_{\pi \ni a} P(\pi).$$

*Proof.* A path that uses $a$ uses it once, since the graph is acyclic, and it splits uniquely into a path from $s$ to $u$, the arc $a$, and a path from $v$ to $F$. Every such triple is a path through $a$. So

$$\sum_{\pi \ni a} e^{\kappa S(\pi)} = \Big(\sum_{s \leadsto u} e^{\kappa S}\Big) e^{\kappa s(a)} \Big(\sum_{v \leadsto F} e^{\kappa S}\Big) = e^{\alpha(u)} e^{\kappa s(a)} e^{\beta(v)}$$

by Lemmas 1 and 2 in the log semiring, and dividing by $Z = e^{\log Z}$ gives the claim. $\square$

**Corollary 2 (posteriors at a time).** If every path covers each frame $t$ with exactly one arc, that is, the node times increase from $0$ at $s$ to the last time $T$ at every final node, then for every $t < T$ the arcs $a$ with $\mathrm{time}(u) \le t < \mathrm{time}(v)$ have posteriors that add up to 1.

*Proof.* Each path contains exactly one such arc, so the sum of $\gamma(a)$ over them is $\sum_\pi P(\pi) = 1$. $\square$

**Lemma 4 (beam pruning).** Let $B$ be the best path score. With $\alpha$ and $\beta$ in the Viterbi semiring, an arc $a$ from $u$ to $v$ is kept by line L9 if and only if some path through $a$ has a score of at least $B - b$, where $b$ is the beam. The pruned lattice keeps every path with a score of at least $B - b$, and its best path has the score $B$.

*Proof.* By the same split as in Lemma 3, $\alpha(u) + s(a) + \beta(v)$ is the best score of a path through $a$, which gives the first claim. A path with score at least $B - b$ has, for each of its arcs, a path through that arc (itself) with score at least $B - b$, so all its arcs are kept, and its nodes and final node are kept by line L10. The best path is such a path, and the pruned lattice has no new paths with a better score, since its paths are paths of the original lattice. $\square$

The pruned lattice can also hold paths with a score below $B - b$, made of kept arcs from different good paths. Lemma 4 says only that no good path is lost.

**Remark (floating point).** The code compares $\alpha(u) + s(a) + \beta(v)$ with $B - b$ with a tolerance of $10^{-9}(1 + |B|)$, because the two sides add the same numbers in different orders. Without it, a beam of 0 can drop an arc of the best path by rounding.
