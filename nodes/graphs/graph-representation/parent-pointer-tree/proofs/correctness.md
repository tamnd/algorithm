---
title: The parent array keeps its invariant, walks up to the root and gives correct child lists
proves: [correctness]
status: full
---

We use the pseudocode of the page and the invariant:

> **(P1)** For each $x \in \{0, \ldots, n - 1\}$, $\text{parent}[x]$ is NIL or an index in $\{0, \ldots, n - 1\}$. **(P2)** For each $x$, the chain $x_0 = x$, $x_{i+1} = \text{parent}[x_i]$ reaches NIL: there is a $j \le n$ with $x_j = $ NIL and $x_0, \ldots, x_{j-1}$ are indices.

**The forest.** Assume (P1) and (P2). The chain of $x$ has distinct indices $x_0, \ldots, x_{j-1}$: if $x_a = x_b$ with $a < b < j$, the chain would repeat forever from $x_a$ and never reach NIL. Hence $j \le n$. Let $F$ be the undirected graph on $\{0, \ldots, n - 1\}$ with the edges $\{x, \text{parent}[x]\}$ for the non-roots $x$. Suppose $F$ had a cycle $C$. Give each edge $\{x, \text{parent}[x]\}$ the direction $x \to \text{parent}[x]$; each vertex has at most one outgoing edge. A cycle in which each vertex has at most one outgoing edge among its two cycle edges, with $|C|$ vertices and $|C|$ edges, has exactly one outgoing edge at each vertex, so its edges form a directed cycle, and following parents from a vertex of $C$ goes around $C$ forever, against (P2). So $F$ is a forest. Each non-root is joined to the root at the end of its chain, so the components of $F$ are in bijection with the roots, and $F$ is a tree when there is exactly one root.

**A new tree.** The array $[\text{NIL}]$ with $n = 1$ meets (P1) and (P2).

**ADD-CHILD.** Let (P1) and (P2) hold for $n$, and let $0 \le p < n$. Line L1 sets $x = n$, and line L2 sets $\text{parent}[x] = p$ and $n' = n + 1$. (P1) holds for the old entries, which are unchanged and lie in $\{0, \ldots, n - 1\} \subseteq \{0, \ldots, n'\!- 1\}$, and for $x$, since $p$ is an index. For (P2), no old entry equals $x$, so the chain of an old vertex $y$ never reaches $x$; it is the same chain as before and reaches NIL in at most $n \le n'$ steps. The chain of $x$ is $x$ followed by the chain of $p$, which reaches NIL in at most $n$ steps, so the chain of $x$ reaches it in at most $n + 1 = n'$ steps. So (P1) and (P2) hold after the call, and the tree of $p$ has gained the leaf $x$ as a child of $p$.

**PATH-TO-ROOT.** Lines L4 to L6 set $x$ to $x_0, x_1, \ldots$ and report each $x_i$ while $x_i \ne$ NIL. By (P2) the loop stops after $j \le n$ reports, and it has reported $x_0, \ldots, x_{j-1}$, the path from $x$ to the root $x_{j-1}$ of its tree in $F$. Each loop pass costs $O(1)$, so the time is $\Theta(j) = \Theta(1 + \text{depth}(x))$, where $\text{depth}(x) = j - 1$.

**CHILD-LISTS.** Call $x$ a *child* of $v$ when $\text{parent}[x] = v$, and let $c_v$ be the number of children of $v$. By (P1) each non-root has exactly one parent in $\{0, \ldots, n - 1\}$.

*After line L8:* $\text{off}[0] = 0$ and $\text{off}[v + 1] = c_v$ for $0 \le v < n$, since line L8 adds 1 to $\text{off}[\text{parent}[x] + 1]$ once for each non-root $x$, and nothing else changes $\text{off}$.

*After line L9:* $\text{off}[v] = \sum_{u < v} c_u$ for $0 \le v \le n$. The loop keeps the claim "for $v' < v$, $\text{off}[v'] = \sum_{u < v'} c_u$, and $\text{off}[v''] = c_{v'' - 1}$ for $v'' \ge v$", which holds at $v = 1$ and is carried from $v$ to $v + 1$ by $\text{off}[v] \leftarrow c_{v-1} + \sum_{u < v - 1} c_u$. In particular $\text{off}[n]$ is the number of non-roots, the length of $\text{kids}$, and the intervals $I_v = [\text{off}[v], \text{off}[v + 1])$ have length $c_v$ and partition $[0, \text{off}[n])$.

*Lines L10 to L14:* Line L10 sets $\text{next}[v] = \text{off}[v]$. We claim that before the pass of line L11 for $x$, for each $v$, $\text{next}[v] = \text{off}[v] + |\{y < x : \text{parent}[y] = v\}|$, and the positions $\text{off}[v], \ldots, \text{next}[v] - 1$ hold the children $y < x$ of $v$ in increasing order. This holds before $x = 0$. In the pass for $x$, if $x$ is a root nothing changes and the claim carries over. Otherwise, with $v = \text{parent}[x]$, line L13 writes $x$ at position $\text{next}[v]$, which is less than $\text{off}[v + 1]$ because $v$ has at least one child $\ge x$, namely $x$, not yet placed; and line L14 increments $\text{next}[v]$. The written position lies in $I_v$, so no other block is touched, and $x$ follows the smaller children of $v$. So the claim holds for $x + 1$.

After the pass for $x = n - 1$, each $I_v$ holds exactly the $c_v$ children of $v$ in increasing order, so $\text{kids}[\text{off}[v] \,..\, \text{off}[v + 1] - 1]$ is the list of children of $v$, as line L15 returns. Lines L7, L8, L9 and L10 each take $\Theta(n)$ time, and lines L11 to L14 take $\Theta(n)$, so CHILD-LISTS runs in $\Theta(n)$ time with $2n + 1$ words of output. $\square$
