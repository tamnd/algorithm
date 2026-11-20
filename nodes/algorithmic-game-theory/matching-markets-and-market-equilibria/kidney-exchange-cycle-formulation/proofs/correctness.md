---
title: Branch and price on the cycle formulation returns a maximum weight packing of short cycles
proves: [correctness, termination]
status: full
---

Let $\mathcal{C}$ be the set of directed cycles of $G$ with at most $L$ pairs, with integer weights $w_c \ge 1$. A *packing* is a set of pairwise vertex-disjoint cycles of $\mathcal{C}$, and its weight is the sum of $w_c$. A node of the search is given by a set $F$ of fixed cycles (pairwise disjoint) and a set $B$ of forbidden cycles. Its *feasible set* is the set of packings $P$ with $F \subseteq P$ and $P \cap B = \emptyset$. Let $V'$ be the pairs not on a cycle of $F$, and $\mathcal{C}'$ the cycles of $\mathcal{C}$ inside $V'$ that are not in $B$. A packing $P$ is feasible for the node exactly when $P = F \cup Q$ with $Q$ a packing of cycles of $\mathcal{C}'$.

For the node, let $\text{LP}'$ be the linear program $\max \sum_{c \in \mathcal{C}'} w_c x_c$ subject to $\sum_{c \ni v} x_c \le 1$ for $v \in V'$ and $x \ge 0$. Its dual is $\min \sum_{v \in V'} y_v$ subject to $\sum_{v \in c} y_v \ge w_c$ for $c \in \mathcal{C}'$ and $y \ge 0$.

**Claim 1 (column generation ends at the optimum of $\text{LP}'$).** The loop of lines L5 to L7 stops, and its last restricted LP has the optimal value of $\text{LP}'$. *Proof.* Each round that does not stop adds at least one cycle of the finite set $\mathcal{C}'$ that is not yet a column, so there are at most $|\mathcal{C}'| + 1$ rounds. Every restricted LP is feasible ($x = 0$) and bounded (each $x_c \le 1$), so it has an optimal solution $x$ and optimal duals $y \ge 0$, with equal values. When the loop stops, every $c \in \mathcal{C}'$ has $w_c - \sum_{v \in c} y_v \le 0$: for the new candidates this is the stopping test, and for the columns it is dual feasibility of the restricted LP. So $y$ is feasible for the dual of $\text{LP}'$. Extending $x$ by zeros gives a feasible solution of $\text{LP}'$ with the same value as $\sum_v y_v$. By weak duality both are optimal. $\square$

**Claim 2 (the node bound).** Every feasible packing $P = F \cup Q$ of the node has weight at most $w(F) + \lfloor \text{LP}' \rfloor$. *Proof.* The indicator vector of $Q$ satisfies the constraints of $\text{LP}'$, so $w(Q) \le \text{LP}'$. The weight $w(Q)$ is an integer, so $w(Q) \le \lfloor \text{LP}' \rfloor$. $\square$

**Claim 3 (integral leaves).** If the final $x$ of a node is integral, then $P = F \cup \{c : x_c = 1\}$ is a feasible packing of the node with the largest weight among them, equal to $w(F) + \text{LP}'$. *Proof.* An integral $x$ with $\sum_{c \ni v} x_c \le 1$ selects disjoint cycles of $\mathcal{C}'$, which are also disjoint from the cycles of $F$ because they lie inside $V'$. Its weight is $w(F) + \text{LP}'$, which by Claim 2 is the largest possible. $\square$

**Claim 4 (branching splits the feasible set).** At line L11, $c \in \mathcal{C}'$ has $0 < x_c < 1$. The feasible set of the node is the disjoint union of the feasible sets of the child $(F, B \cup \{c\})$ and the child $(F \cup \{c\}, B)$. *Proof.* $c$ is a column, so it lies inside $V'$ and is not in $B$; in particular $F \cup \{c\}$ is a set of disjoint cycles. A feasible packing either contains $c$, and is feasible for the second child, or does not, and is feasible for the first. $\square$

**Termination.** By Claim 4, each child has one more cycle in $F \cup B$ than its parent, and $F \cup B \subseteq \mathcal{C}$. So every path in the search tree has at most $|\mathcal{C}|$ branchings, and the tree has at most $2^{|\mathcal{C}| + 1}$ nodes. Each node ends by Claim 1. So the algorithm stops.

**Correctness.** Let $P^*$ be a maximum weight packing, with weight $\text{OPT}$. The variable $\text{best}$ is always the weight of a packing that was found, by Claim 3, so $\text{best} \le \text{OPT}$, and $\text{best\_set}$ is that packing. We show that $\text{best} = \text{OPT}$ at the end.

The root's feasible set is the set of all packings, so it contains $P^*$. Follow the nodes whose feasible set contains $P^*$: by Claim 4, when such a node branches, exactly one child contains $P^*$, and that child is pushed and later popped, since the loop runs until the stack is empty. The chain ends at a node $N$ that contains $P^*$ and does not branch. At $N$ there are two cases.

- Line L8 discards $N$. Then $w(F) + \lfloor \text{LP}' \rfloor \le \text{best}$, and by Claim 2, $\text{OPT} = w(P^*) \le \text{best}$ at that moment.
- Line L9 records $N$. By Claim 3, $\text{best}$ becomes the largest weight of a feasible packing of $N$, which is at least $w(P^*) = \text{OPT}$.

In both cases $\text{best} \ge \text{OPT}$ from that moment on, and $\text{best}$ never decreases, since line L9 only runs when the new value is larger than the old one (line L8 failed). So at the end $\text{best} = \text{OPT}$ and $\text{best\_set}$ is a maximum weight packing. $\blacksquare$

**Cost.** By termination there are at most $2^{|\mathcal{C}| + 1}$ nodes. At each node the cycles of $G[V']$ are enumerated in $O(n d^{L-1})$ time, where $d$ is the largest out-degree, and there are at most $|\mathcal{C}| + 1$ rounds of column generation. Each restricted LP has at most $n$ rows and $|\mathcal{C}|$ columns plus $n$ slacks, and the simplex method with Bland's rule never repeats a basis, so it makes at most $2^{n + |\mathcal{C}|}$ pivots of polynomial cost. The total is $2^{O(n + |\mathcal{C}|)}$ arithmetic operations. With $|\mathcal{C}| \le n^L$, the bound is exponential, as expected for an NP-hard problem.
