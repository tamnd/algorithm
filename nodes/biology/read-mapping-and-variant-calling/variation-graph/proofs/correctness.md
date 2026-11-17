---
title: The paths of the built graph are exactly the haplotypes of the variant subsets, and FIND returns every exact match along a walk
proves: [correctness]
status: full
---

**Setting.** The reference is a string $\mathit{ref}$ of length $n$. A variant $(p, a, b)$ replaces $\mathit{ref}[p{:}p + |a|]$, which must equal $a$, by $b$, with $a \ne b$. The variants $(p_1, a_1, b_1), \ldots, (p_v, a_v, b_v)$ are sorted by position and do not touch: $p_1 \ge 1$, $p_{t+1} \ge p_t + |a_t| + 1$, and $p_v + |a_v| \le n - 1$. For a set $C$ of variant indices, $\mathit{ref}^C$ is the string with the variants of $C$ applied and the others not. A *walk* is a path that follows the edges of the graph.

**Lemma 1 (the nodes).** Every node of BUILD holds a non-empty string. No cut lies strictly inside the reference allele $\mathit{ref}[p_t{:}p_t + |a_t|]$ of a variant, so a variant with $a_t$ non-empty has one reference node, whose string is $a_t$. Each variant has a reference node that ends at $p_t$ and one that starts at $p_t + |a_t|$.

*Proof.* Line L2 makes a node for each two adjacent distinct cuts, so its string has at least one base. Line L3 makes an alt node only for a non-empty $b$. The cuts are $0$, $n$ and the two ends of each variant. The ends of another variant lie at least one base outside $[p_t, p_t + |a_t|]$, because the variants do not touch, so no cut lies strictly inside. The cuts $p_t \ge 1$ and $p_t + |a_t| \le n - 1$ are not the ends of the reference, so there is a node on each side. $\square$

Call the reference nodes that are not a reference allele the *backbone*. The source (the node at 0) and the sink (the node that ends at $n$) are in the backbone. Between two backbone nodes that are next to each other on the reference there is at most one variant, because two variants are separated by at least one backbone base.

**Lemma 2 (the bubbles).** For variant $t$, let $u_t$ be the backbone node that ends at $p_t$ and $w_t$ the backbone node that starts at $p_t + |a_t|$. The walks from $u_t$ to $w_t$ are exactly two: the *reference route*, through the node of $a_t$ (or the direct edge $u_t \to w_t$ if $a_t$ is empty), and the *alternative route*, through the node of $b_t$ (or the direct edge if $b_t$ is empty). The two routes are different and spell $a_t$ and $b_t$ between the two backbone nodes.

*Proof.* Line L4 joins the reference nodes in order, which gives the reference route, and lines L5 to L7 add the alternative route. No other line adds an edge out of $u_t$, out of the allele nodes, or into $w_t$ from inside the bubble, since the other variants have their own $u$ and $w$ nodes outside $[p_t, p_t + |a_t|]$. At least one of $a_t$, $b_t$ is non-empty, and if both are, they are two different nodes, so the routes differ. $\square$

**Lemma 3 (topological ids).** Every edge goes from a smaller id to a larger id.

*Proof.* The ids follow the start position on the reference, with an inserted node before the reference node at the same start and an alt node after the reference allele at the same start. A reference edge goes to a node that starts later. An edge $u_t \to$ alt goes to a node that starts at $p_t$, after the start of $u_t$. An edge alt $\to w_t$ goes to a node that starts at $p_t + |a_t|$, which is later for a non-empty $a_t$; for an insertion the two start at the same place, and the inserted node has the smaller id by its order. A direct edge $u_t \to w_t$ goes to a later start. $\square$

So the graph is a directed acyclic graph, and the walks are finite.

**Theorem 1 (the paths are the haplotypes).** The map from a set $C \subseteq \{1, \ldots, v\}$ to the walk that takes the alternative route at the variants of $C$ and the reference route at the others is a one-to-one map onto the walks from the source to the sink. The walk of $C$ spells $\mathit{ref}^C$. In particular the reference path spells $\mathit{ref}$, and there are $2^v$ walks from the source to the sink.

*Proof.* A walk from the source must leave each backbone node by one of its edges. A backbone node that is not some $u_t$ has one out-edge, to the next backbone node. At $u_t$, by Lemma 2, the walk takes one of the two routes and comes to $w_t$. So every walk from the source to the sink visits all backbone nodes in order and picks one route at each bubble, and the set of bubbles where it takes the alternative route is its $C$. Different sets give different walks, because the routes differ. The spelled string is the backbone strings in order with $a_t$ or $b_t$ put between $u_t$ and $w_t$, which is $\mathit{ref}^C$. $\square$

**Lemma 4 (one step of FIND).** If a walk is at base $k$ of node $i$, its next base is base $k + 1$ of node $i$ when $k + 1 < |\mathit{seq}(i)|$, and otherwise base 0 of a successor of $i$, one for each out-edge.

*Proof.* A walk spells the strings of its nodes one after the other, and every node is non-empty by Lemma 1, so base 0 of each successor exists. $\square$

**Theorem 2 (FIND).** After line L8 and $t$ runs of lines L9 to L11, the state set holds $(i_0, k_0, i, k)$ exactly when some walk has $s[0{:}t+1]$ as the bases from base $k_0$ of node $i_0$ to base $k$ of node $i$. Line L12 returns every place $(i_0, k_0)$ where $s$ starts along some walk, and every node lies on a walk from the source to the sink, so these are also the places where $s$ starts in the string of some haplotype path, mapped to the graph.

*Proof.* For $t = 0$, line L8 keeps the places whose base is $s[0]$, each as its own start. For the step, a walk that matches $s[0{:}t+2]$ is a walk that matches $s[0{:}t+1]$, ending at $(i, k)$, followed by the next base of Lemma 4, which must be $s[t+1]$. Lines L10 and L11 make every such next base and keep the ones equal to $s[t+1]$. Every node is a backbone node or on a route of a bubble, so by the proof of Theorem 1 it lies on a walk from the source to the sink, and every walk from a node can be extended to such a walk on both sides. $\square$

The test compares FIND with a search of $s$ in the strings of all $2^v$ haplotype paths.

**Cost.** BUILD sorts the variants and the cuts in $O(v \log v)$ time and copies the reference in $O(n)$ time. It makes at most $2v + 1$ reference nodes and $v$ alt nodes, and at most $4v$ edges: $2v$ along the reference path and two for each variant. FIND keeps states of a start and a current place. With $N$ bases in the graph and out-degree at most $d$, each of the $|s| - 1$ steps costs $O(d)$ per state. A test for whether $s$ occurs at all needs only the current places, at most $N$ of them, so it costs $O(|s| N d)$ time; keeping the starts can raise the number of states up to $N^2$ in the worst case.
