---
title: Offline variable substitution keeps the least solution of the subset constraints
proves: [correctness, termination, complexity]
status: full
---

**Setting.** The program is a set $S$ of $m$ statements in the four forms over $n$ variables, each variable also a location. $L$ is the least solution of the subset constraints of [Andersen's analysis](/andersen-analysis/): `p = &a` gives $a \in L(p)$, `p = q` gives $L(q) \subseteq L(p)$, `p = *q` gives $L(a) \subseteq L(p)$ for $a \in L(q)$, and `*p = q` gives $L(q) \subseteq L(a)$ for $a \in L(p)$. $L$ lies inside every solution. The copy graph $G$ has an edge $q \to p$ for each copy `p = q` with $p \ne q$. The set $X$ of line L2 holds every $p$ with a statement `p = &a` or `p = *q`, and every $a$ with a statement `p = &a`. A variable not in $X$ is *direct*.

Every element of $L(p)$ is a location $a$ with a statement `x = &a`, since the set of such locations, given to every variable, is a solution. So $L(p) \subseteq X$ for all $p$, and a store `*p = q` adds only to the sets of variables in $X$.

**Lemma 1 (a direct component gets only what its sources give).** Let $C$ be a strongly connected component of $G$ with no variable of $X$, and let $U$ be the union of $L(q)$ over the edges $q \to x$ with $x \in C$ and $q \notin C$. Then $L(x) = U$ for every $x \in C$.

*Proof.* Each such edge is a copy, so $U \subseteq L(x)$ for some $x \in C$, and since the members of $C$ lie on cycles of copies, $L$ is the same on all of $C$ and contains $U$. For the other direction, let $T$ be $L$ with every set of $C$ replaced by $U$, so $T \le L$. We show that $T$ is a solution; then $L \le T$ by minimality, and $L = T$ on $C$. Take the constraints that involve a member $x$ of $C$.

- On the left. $x$ is direct, so the only statements with $x$ on the left are copies `x = q`. If $q \in C$, then $T(q) = U = T(x)$. If not, $T(q) = L(q) \subseteq U$. No store adds to $T(x)$, since $x \notin X$ and the sets of $T$ hold only locations in $X$.
- On the right. For `p = x`, $T(x) = U \subseteq L(x) \subseteq L(p)$, and if $p \in C$ then $T(p) = U$ too. For `p = *x` and `*x = q`, each $a \in T(x) \subseteq L(x)$ is in $X$, so $a \notin C$, and the constraints of $L$ for $a$ give what is needed. For `*p = x`, each $a \in T(p)$ has $T(x) \subseteq L(x) \subseteq L(a) = T(a)$, since $a \in X$.
- $x$ is never a location in a set, since $x \notin X$. $\square$

**Lemma 2 (equal labels mean equal sets).** If two variables get the same label in lines L3 to L8, they have the same least set. Every variable with the label EMPTY has an empty least set.

*Proof.* By induction over the components in topological order, which puts each component after all components with an edge into it. All members of a component have the same $L$, since they lie on cycles of copies. A component that gets a fresh label (lines L4 and L8) is the only one with that label. A component with the label EMPTY (line L6) is direct and every component with an edge into it has the label EMPTY, so by Lemma 1 and the induction hypothesis its set is a union of empty sets. A component that takes the label $l$ in line L7 is direct, and every component with an edge into it has the label $l$ or EMPTY; by the induction hypothesis these have one common set $L_l$ or the empty set, and by Lemma 1 the component has the set $L_l$. $\square$

**Theorem 1 (correctness).** Let $S'$ be the statements of $S$ rewritten by line L10, and let $M$ be the least solution of $S'$ with the set of a location $a$ kept at the node $rep(a)$. Then $M(rep(v)) = L(v)$ for every variable $v$.

*Proof.* In $S'$ each statement `p = &a` becomes `rep(p) = &a`, `p = q` becomes `rep(p) = rep(q)`, `p = *q` gives $M(rep(a)) \subseteq M(rep(p))$ for $a \in M(rep(q))$, and `*p = q` gives $M(rep(q)) \subseteq M(rep(a))$ for $a \in M(rep(p))$.

First, $L$ read on the nodes, $N(r) = L(r)$ for each representative $r$, is a solution of $S'$. By Lemma 2, $L(rep(v)) = L(v)$ for every $v$, so each rewritten constraint for $N$ is the original constraint for $L$, with each variable $v$ replaced by $rep(v)$ and the same sets. So $M \le N$, that is, $M(rep(v)) \subseteq L(v)$.

Second, $T(v) = M(rep(v))$ is a solution of $S$, since each original constraint for $T$ is exactly the rewritten constraint for $M$. So $L \le T$, that is, $L(v) \subseteq M(rep(v))$. $\square$

So the substitution keeps the least solution, and any correct solver for the smaller system, such as Andersen's worklist solver, gives Andersen's result after the map back in line L12.

**Theorem 2 (time).** Lines L1 to L10 take $O(n + m)$ time and space, with hashing to drop repeated statements. With the worklist solver of Andersen's analysis on the rewritten system, the total time is $O(n'^2 n + n + m)$, where $n' \le n$ is the number of representatives. This is within the $O(n^3 + m)$ bound of Andersen's analysis.

*Proof.* The copy graph has at most $m$ edges. Tarjan's algorithm finds its components in $O(n + m)$ time. Line L5 looks at each edge into each component once, so all labels cost $O(n + m)$. Lines L9 and L10 take $O(n + m)$. The rewritten system has $n'$ nodes, and its sets hold at most $n$ locations. After the repeats are dropped, each node has at most $n'$ loads, $n'$ stores and $n'$ successors. Each of the at most $n'^2$ edges is added once, and its first transfer of a set costs $O(n)$. Each location enters the set of each node once, so each of the $n' n$ pairs of a node and a location is handled once, at a cost of $O(n')$ for the loads, the stores and the successors of the node. The total is $O(n'^2 n)$ for the solver. $\square$

The substitution does not lower the worst case of Andersen's analysis. Its gain is that real programs have many direct variables, often temporaries, and the solver then works on far fewer nodes and edges.
