---
title: Similarity flooding builds the propagation graph, keeps similarities in [0, 1], converges for the basic formula and returns a stable matching
proves: [correctness, termination]
status: full
---

Similarity flooding is a heuristic, so there is no "right" answer to prove against. This file proves what the procedure itself guarantees. It shows that lines L1 to L3 build the propagation graph of the definition, that each step keeps the values in $[0, 1]$, that the basic formula converges and where it converges to, that the loop stops, and that lines L11 and L12 return a stable matching. Nothing here says that the pairs found are the correct correspondences; that is a heuristic, and only measurements can support it.

**Notation.** The input graphs have edge sets $E_A$ and $E_B$ of labeled edges $a \xrightarrow{l} a'$. A map pair is a pair $(a, b)$ of a node of $A$ and a node of $B$. Let $V$ be the set of map pairs that are an end of an edge of the pairwise connectivity graph or that have a value in $\sigma^0$. We write a vector $\sigma : V \to \mathbb{R}_{\ge 0}$. For a node $x$ and a label $l$, $\mathrm{out}_l(x)$ is the number of $l$-edges out of $x$ in the pairwise connectivity graph and $\mathrm{in}_l(x)$ is the number of $l$-edges into $x$.

**Lemma 1 (construction).** After line L1, the list holds exactly the edges $(a, b) \xrightarrow{l} (a', b')$ with $a \xrightarrow{l} a'$ in $E_A$ and $b \xrightarrow{l} b'$ in $E_B$, each one time. After lines L2 and L3, the propagation graph has, for each such edge, a forward edge with weight $1/\mathrm{out}_l((a, b))$ and a backward edge from $(a', b')$ to $(a, b)$ with weight $1/\mathrm{in}_l((a', b'))$, and no other edge.

*Proof.* The code puts the edges of $B$ in lists by label. For each edge $a \xrightarrow{l} a'$ of $A$ it adds one edge for each entry $(b, b')$ of the list of $l$. So each pair of edges with the same label gives one edge, and no other pair gives an edge. Both inputs pass through a set first, so a repeated input edge counts one time. The counts $\mathrm{out}_l$ and $\mathrm{in}_l$ are computed over this list before line L2, and lines L2 and L3 add exactly two weighted edges for each list entry. $\square$

Let $M$ be the $V \times V$ matrix with $M_{yx}$ equal to the sum of the weights of the edges $x \to y$ of the propagation graph. Then $\varphi(\sigma) = M\sigma$ is the vector that the function `_phi` computes. $M$ is nonnegative. For each label $l$ and each node $x$ with $\mathrm{out}_l(x) > 0$, the forward edges of label $l$ out of $x$ have weights that sum to 1, and the same holds for the backward edges into a node. So each column of $M$ sums to at most twice the number of labels at that node.

**Lemma 2 (range).** Assume $\sigma^0 \ge 0$. After each step, all values are in $[0, 1]$, and the largest value is 1, unless all values are 0.

*Proof.* By induction on the steps. At the start, $\sigma = \sigma^0 \ge 0$. In a step, the base and the argument of line L6 are sums of nonnegative vectors, and $M$ is nonnegative, so the vector of line L7 is nonnegative. If its largest value $t$ is positive, line L8 divides by $t$, so the values are in $[0, 1]$ and the largest is 1. If $t = 0$, all values are 0. $\square$

The vector can become 0 only for formula B, which drops the base: if no node with a positive value has an edge, then $\varphi(\sigma^0 + \sigma) = 0$. For the other formulas the base keeps a positive value.

**Lemma 3 (termination).** The loop of lines L5 to L10 stops after at most the step limit of steps.

*Proof.* Each pass increases the step count by 1, and line L10 stops the loop when the count reaches the limit. $\square$

**Theorem (the basic formula).** Assume that the undirected graph under the propagation graph is connected, that it has at least one edge, and that $\sigma^0 \ge 0$ is not zero. Let $\sigma^k$ be the vector after $k$ steps of the basic formula $\sigma^{k+1} = (\sigma^k + M\sigma^k)/\max(\sigma^k + M\sigma^k)$. Then $\sigma^k$ converges to $u / \max u$, where $u$ is the positive Perron vector of $I + M$. The limit does not depend on $\sigma^0$.

*Proof.* Each step multiplies by $T = I + M$ and then divides by a positive number. Scaling commutes with multiplication by $T$, so $\sigma^k = T^k \sigma^0 / \max(T^k \sigma^0)$.

$T$ is nonnegative. Each forward edge $x \to y$ has a backward edge $y \to x$, and the weights are positive, so $M_{yx} > 0$ if and only if $M_{xy} > 0$. The undirected graph is connected, so the directed graph of $M$ is strongly connected, and $M$ is irreducible. Then $T = I + M$ is irreducible and has a positive diagonal, so it is primitive: some power $T^m$ has only positive entries.

By the Perron-Frobenius theorem for primitive matrices, $T$ has a simple eigenvalue $\rho > 0$ that is larger in absolute value than each other eigenvalue, with a positive right eigenvector $u$ and a positive left eigenvector $w$, and $T^k / \rho^k \to u w^\top / (w^\top u)$ as $k \to \infty$. So
$$\frac{T^k \sigma^0}{\rho^k} \to \frac{w^\top \sigma^0}{w^\top u}\, u.$$
The number $w^\top \sigma^0$ is positive, because $w > 0$, $\sigma^0 \ge 0$ and $\sigma^0 \neq 0$. The map $v \mapsto v / \max v$ is continuous at each nonzero nonnegative vector and does not change under positive scaling. So $\sigma^k \to u / \max u$. $\blacksquare$

**Consequence.** Under the assumptions of the theorem, the basic formula keeps no information from $\sigma^0$ in the limit. The limit is fixed by the shape of the two graphs alone. With the stopping test of line L10, the procedure returns a vector close to this limit when $\varepsilon$ is small and the step limit is large. This is why the formulas A, B and C add $\sigma^0$ back in each step. For these three formulas this file proves only Lemmas 2 and 3. Their convergence is not proved here, and the loop relies on the step limit.

**Theorem (filter).** Lines L11 and L12 return a set $P$ of pairs with these properties. Each node of $A$ and each node of $B$ is in at most one pair of $P$. Each pair $(a, b)$ in $P$ has $\sigma(a, b) \ge \theta$ and $\sigma(a, b) > 0$. There is no blocking pair: no pair $(a, b)$ with $\sigma(a, b) \ge \theta$ and $\sigma(a, b) > 0$, not in $P$, such that $a$ is free or prefers $b$ to its partner and $b$ is free or prefers $a$ to its partner.

Here $a$ prefers $b$ to $b'$ when $\sigma(a, b) > \sigma(a, b')$, or the two values are equal and $b$ comes before $b'$ in the node order. In the same way $b$ prefers $a$ to $a'$ when $\sigma(a, b) > \sigma(a', b)$, or the values are equal and $a$ comes before $a'$. The ties are broken, so both orders are strict.

*Proof.* The acceptable pairs are those with $\sigma \ge \theta$ and $\sigma > 0$, and lines L11 and L12 run the Gale-Shapley proposal algorithm on them with the strict orders above. Each node of $A$ proposes to each acceptable partner at most one time, in its order of preference, so the loop stops after at most the number of acceptable pairs of proposals. A node of $B$ holds at most one proposal, and it changes only to a partner that it prefers. So the result is a matching of acceptable pairs.

Assume that $(a, b)$ blocks it. Since $a$ is free or prefers $b$ to its final partner, $a$ proposed to $b$ at some time: a free node of $A$ at the end has proposed to each acceptable partner, and a matched node of $A$ proposed to each partner it prefers to its final one. When $b$ got the proposal of $a$, it kept $a$ or a node it prefers to $a$, and its partner only gets better after that. So at the end $b$ has a partner that it prefers to $a$, or $a$ itself. This contradicts that $(a, b)$ blocks. $\blacksquare$
