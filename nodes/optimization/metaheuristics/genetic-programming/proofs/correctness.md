---
title: GP keeps well-formed trees within the depth limit, never loses its best error, and finds a zero-error tree with probability 1 when one is reachable by mutation
proves: [correctness]
status: full
---

We use the pseudocode of the page with function set $F$, terminal set $T$, at most $a_{\max}$ arguments per function, error $E(t) = \sum_i |t(x_i) - y_i|$, and the preconditions $N > e \ge 1$, $2 \le D_{\text{init}} \le D_{\max}$, $D_{\text{mut}} \le D_{\max}$ and $p_c + p_m \le 1$. We assume closure: each function of $F$ is defined on all values that trees can return. Let $P_g$ be the population after generation $g$, with $P_0$ from line L1.

**Claim 1 (closure).** Every element of every $P_g$ is a well-formed tree over $F \cup T$: a terminal, or a function of $F$ with exactly as many subtrees as it has arguments, each a well-formed tree. Hence $E(t)$ is defined for each tree.

*Proof.* Full and grow make a terminal or a function with one recursive call per argument, so their trees are well formed. Let $t$ and $s$ be well-formed trees, and let $t[u \leftarrow s]$ be $t$ with the subtree at node $u$ replaced by $s$. This tree is well formed: the nodes outside the subtree keep their functions and their number of children, and the new subtree is well formed. Lines L6 and L7 build trees of this form with $s$ a subtree of a well-formed tree or a grow tree. Lines L4, L8 and L9 copy trees of the previous population. By induction on $g$, all trees are well formed. Closure gives a value at each node, from the leaves up, so $t(x_i)$ and $E(t)$ are defined. $\square$

**Claim 2 (depth).** Every tree in every $P_g$ has depth at most $D_{\max}$.

*Proof.* Full and grow with limit $d$ give trees of depth at most $d$, so $P_0$ has depth at most $D_{\text{init}} \le D_{\max}$. In generation $g \ge 1$, the elites of line L4 and the parent $a$ of lines L6 to L8 come from $P_{g-1}$ and have depth at most $D_{\max}$ by induction. Line L9 keeps a child only if its depth is at most $D_{\max}$, and otherwise replaces it by $a$. $\square$

**Claim 3 (elitism).** For $g \ge 1$, $\min_{t \in P_g} E(t) \le \min_{t \in P_{g-1}} E(t)$. Line L12 returns a tree whose error is the smallest error in any population of the run.

*Proof.* Line L4 copies a tree of $P_{g-1}$ with the smallest error into $P_g$ unchanged, and $E$ depends only on the tree. So the minimum over $P_g$ is at most that error. Then the minimum over $P_g$ is the smallest over $P_0, \ldots, P_g$, by induction, and line L12 returns a tree with it. $\square$

**Claim 4 (a lower bound for grow).** Let $t$ be a tree of depth at most $d$, and let $r = |F| + |T|$. Then grow with limit $d$ returns $t$ with probability at least $r^{-\text{size}(t)}$.

*Proof.* By induction on $d$. Grow returns $t$ if it makes the right choice at each node of $t$, and these choices are independent. A node above depth $d$ is drawn uniformly from $F \cup T$, which gives the right element with probability $1/r$. A node at depth $d$ is a terminal of $t$, since $t$ has depth at most $d$, and it is drawn uniformly from $T$, with probability $1/|T| \ge 1/r$. The product over the $\text{size}(t)$ nodes is at least $r^{-\text{size}(t)}$. $\square$

**Claim 5 (convergence).** Let $t^*$ be a tree with $E(t^*) = 0$ and depth at most $D_{\text{mut}}$, let $p_m > 0$, and let
$$S = \sum_{j=0}^{D_{\max}} a_{\max}^j, \qquad q = \frac{p_m}{S \, r^{\text{size}(t^*)}}.$$
Then in each generation, given the past, the population after the generation contains a tree of error 0 with probability at least $q$. Hence the probability that no population up to $P_g$ contains a tree of error 0 is at most $(1 - q)^g$, and with $G \to \infty$, the run returns a tree of error 0 with probability 1.

*Proof.* A tree with depth at most $D_{\max}$ and at most $a_{\max}$ arguments per node has at most $a_{\max}^j$ nodes at depth $j$, so its size is at most $S$; for binary functions $S = 2^{D_{\max}+1} - 1$. Since $N > e$, line L5 creates at least one child. For that child, line L7 is taken with probability $p_m$. Its parent $a$ has at most $S$ nodes by Claim 2, so the root of $a$ is the chosen node with probability at least $1/S$, and then the child is the grow tree itself. By Claim 4 it equals $t^*$ with probability at least $r^{-\text{size}(t^*)}$. Its depth is at most $D_{\text{mut}} \le D_{\max}$, so line L9 keeps it. These three steps use independent random draws, so the child is $t^*$ with probability at least $q$. If a tree of error 0 enters a population, then by Claim 3 every later population contains one, and the loop of line L3 stops. Let $A_g$ be the event that $P_0, \ldots, P_g$ contain no tree of error 0. Then $P(A_g \mid A_{g-1}) \le 1 - q$, so $P(A_g) \le (1 - q)^g$ by the chain rule, which tends to 0. $\square$

**Remark.** The bound $q$ is exponentially small in $\text{size}(t^*)$ and in $D_{\max}$, so Claim 5 does not give a useful time bound. It shows only that GP with elitism and subtree mutation cannot get stuck forever when a solution exists within the mutation depth. Without mutation ($p_m = 0$), the claim can fail: if no tree of the population contains the terminal $x$, crossover cannot create it. $\blacksquare$
