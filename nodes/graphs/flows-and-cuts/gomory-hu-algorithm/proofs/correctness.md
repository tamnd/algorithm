---
title: The Gomory-Hu algorithm returns a cut tree
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be undirected with weights $w \ge 0$. For $A \subseteq V$ write $c(A)$ for the total weight of edges with exactly one end in $A$, and $\lambda(a, b)$ for the least $c(A)$ over sets $A$ with $a \in A$, $b \notin A$. A *minimum $a$-$b$ cut* is such a set $A$ with $c(A) = \lambda(a, b)$, or its complement.

**Fact 1 (submodularity).** For all $A, B \subseteq V$, $c(A) + c(B) \ge c(A \cap B) + c(A \cup B)$. *Proof.* Check each edge $(p, q)$ by where its ends lie. An edge counted on the right is counted at least as often on the left; for example an edge from $A \setminus B$ to $B \setminus A$ counts twice on the left and zero times on the right, and an edge from $A \cap B$ to $V \setminus (A \cup B)$ counts twice on each side. Also $c(A) = c(V \setminus A)$.

**Fact 2 (triangle inequality).** $\lambda(a, c) \ge \min(\lambda(a, b), \lambda(b, c))$. *Proof.* A minimum $a$-$c$ cut $A$ with $a \in A$, $c \notin A$ separates $a$ from $b$ if $b \notin A$, and $b$ from $c$ if $b \in A$.

**Fact 3 (contraction keeps cuts).** Each vertex set of $G_X$ corresponds to the vertex set of $G$ obtained by expanding the contracted vertices, with the same cut value. So every cut of $G_X$ is a cut of $G$, and $\lambda_{G_X}(s, t) \ge \lambda_G(s, t)$.

For a tree edge $e = (X, Y)$ let $D_e^Y$ be the union of the nodes on the $Y$ side of $T - e$.

**Invariant.** Before each test of line L2, the nodes of $T$ partition $V$, $T$ is a tree, and every tree edge $e = (X, Y)$ of weight $\lambda_e$ has a witness pair $x \in X$, $y \in Y$ with $\lambda(x, y) = \lambda_e = c(D_e^Y)$.

It holds at the start, when $T$ has one node and no edge. Assume it holds before a round on node $X$ with $s, t \in X$.

**Claim A.** Some minimum $s$-$t$ cut of $G$ does not split $D_C$, the vertex set of any component $C$ of $T - X$. *Proof.* Let $Z$ be a minimum $s$-$t$ cut with $s \in Z$. Take a component $C$, joined to $X$ by the tree edge $e = (X, Y)$ with $Y \in C$, witness $x \in X$, $y \in Y$, and $D = D_e^Y = D_C$. Then $s, t, x \notin D$, $y \in D$, and $D$ is a minimum $x$-$y$ cut. If $y \in Z$: $Z \cap D$ contains $y$ but not $x$, so $c(Z \cap D) \ge c(D)$, and Fact 1 gives $c(Z \cup D) \le c(Z)$; the set $Z \cup D$ contains $s$, not $t$, so it is a minimum $s$-$t$ cut containing $D$. If $y \notin Z$: apply Fact 1 to $Z$ and $V \setminus D$, which contains $x$, $s$, $t$. The union $Z \cup (V \setminus D)$ contains $x$ and not $y$, so its value is at least $c(D) = c(V \setminus D)$, and so $c(Z \setminus D) \le c(Z)$; the set $Z \setminus D$ contains $s$, not $t$, and is disjoint from $D$. Either way $Z$ is replaced by a minimum $s$-$t$ cut that does not split $D_C$. The sets $D_C$ of different components are disjoint, so adding or removing one of them does not split another that was whole. Repeat for each component. $\square$

By Claim A and Fact 3, $\lambda_{G_X}(s, t) = \lambda_G(s, t)$, and the set $S$ of line L5, expanded, is a minimum $s$-$t$ cut $\hat S$ of $G$ that splits no $D_C$.

**The new edge.** After line L8, the side of the edge $(X_s, X_t)$ that contains $X_s$ is $X_s$ together with every $D_C$ with $v_C \in S$, which is $\hat S$. So its value $c(\hat S) = \lambda = \lambda(s, t)$, and $(s, t)$ is a witness pair with $s \in X_s$, $t \in X_t$.

**The old edges.** Let $e = (X, Y)$ be an old edge with witness $x, y$ and $D = D_e^Y$. After line L8 the $Y$ side of the edge is still $D$, since only $X$ was split, so $c(D) = \lambda(x, y)$ still holds. If the half that $Y$ is attached to contains $x$, the witness stays. Otherwise say $Y$ is attached to $X_t$ while $x \in X_s$; then $D \cap \hat S = \emptyset$ and $x \in \hat S$. We show that $(t, y)$ is a witness. The set $D$ contains $y$ and not $t$, so $\lambda(t, y) \le c(D)$. Let $Z$ be a minimum $t$-$y$ cut with $y \in Z$, $t \notin Z$. If $x \notin Z$, then $Z$ separates $x$ from $y$ and $c(Z) \ge \lambda(x, y)$. If $x \in Z$, the set $Z \cup \hat S$ contains $s$ and not $t$, so $c(Z \cup \hat S) \ge c(\hat S)$, and Fact 1 gives $c(Z \cap \hat S) \le c(Z)$; the set $Z \cap \hat S$ contains $x$ and not $y$, so $c(Z) \ge \lambda(x, y)$. Hence $\lambda(t, y) = \lambda(x, y) = c(D)$. The case where $Y$ is attached to $X_s$ while $x \in X_t$ is the same with $s$ and $t$ swapped and $\hat S$ replaced by $V \setminus \hat S$, which is a minimum $t$-$s$ cut.

The nodes still partition $V$, and $T$ is still a tree: a node was split in two joined by one edge, and every old edge has one end moved to one of the halves. So the invariant holds after the round.

**Termination.** Each round increases the number of nodes by one, since $X_s \ni s$ and $X_t \ni t$ are both nonempty. A partition of $V$ has at most $n$ parts, so after $n - 1$ rounds every node is a single vertex and line L2 fails.

**The result.** At the end each tree edge $(a, b)$ joins single vertices, so its witness is $(a, b)$ itself: $\lambda(a, b) = \lambda_e = c(D_e^b)$. Take $u \ne v$ and the tree path $u = x_0, x_1, \dots, x_k = v$. Every edge $e_i = (x_{i-1}, x_i)$ of the path has a side that contains exactly one of $u$ and $v$, so $\lambda(u, v) \le \lambda_{e_i}$ for each $i$. By Fact 2 applied $k - 1$ times, $\lambda(u, v) \ge \min_i \lambda(x_{i-1}, x_i) = \min_i \lambda_{e_i}$. So $\lambda(u, v)$ is the least weight on the path, and the side of a lightest path edge is a cut of that value separating $u$ from $v$, a minimum $u$-$v$ cut. $\blacksquare$
