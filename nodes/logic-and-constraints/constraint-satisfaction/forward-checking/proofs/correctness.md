---
title: Forward checking is sound and complete, and its tree is part of the backtracking tree
proves: [correctness]
status: full
---

We use the pseudocode of the page, with the static order $x_1, \ldots, x_n$. For a partial assignment $\sigma$ to $x_1, \ldots, x_k$, a value $b \in D(x_j)$ with $j > k$ is *compatible with* $\sigma$ if $(\sigma(x_i), b) \in C_{ij}$ for every $i \le k$ with a constraint $C_{ij}$. Write $\sigma_k$ for the restriction of $\sigma$ to $x_1, \ldots, x_k$.

**Lemma 1 (invariant).** Each time line L4 runs at level $i$, with $\sigma_{i-1}$ the current assignment to $x_1, \ldots, x_{i-1}$:

1. for each $j \ge i$, $CD[j]$ is the set of values of $D(x_j)$ compatible with $\sigma_{i-1}$;
2. $\sigma_{i-1}$ is consistent;
3. the untried values of $x_i$ are a subset of $CD[i]$, and they are the values of $CD[i]$ that level $i$ has not taken since $\sigma_{i-1}$ was set.

*Proof.* By induction on the number of iterations. At the start, $i = 1$, $\sigma_0$ is empty, $CD[j] = D(x_j)$ and $pruned[1]$ is empty, so all three parts hold.

Assume the invariant holds for the levels $1, \ldots, i$ in the state when level $i$ was entered with $\sigma_{i-1}$, in the following sense: just after line L3 at level $i$, $CD[j]$ for $j \ge i$ is the set of values compatible with $\sigma_{i-1}$. Line L7 sets $x_i = a$ with $a \in CD[i]$. Lines L8 and L9 remove from $CD[j]$, $j > i$, exactly the values $b$ with $(a, b) \notin C_{ij}$, and record them in $pruned[i]$. Since $CD[j]$ held the values compatible with $\sigma_{i-1}$, it now holds the values compatible with $\sigma_i$. If the search goes deeper at line L12, the new level $i + 1$ has $pruned[i+1]$ empty (it was emptied when the search last left that level through line L3 and L5, or it was never used), so after line L3 at level $i + 1$ part 1 holds for $\sigma_i$. Part 2 holds because $a \in CD[i]$ is compatible with $\sigma_{i-1}$, and $\sigma_{i-1}$ is consistent. Part 3 holds because line L12 sets the untried values of $x_{i+1}$ to $CD[i+1]$.

If the search does not go deeper, the next iteration runs line L3 at level $i$ (after a wipe-out, or after a solution in the all-solutions mode) or at level $i - 1$ (after line L5, which runs only after line L3 at level $i$ has run). In both cases line L3 puts back exactly the pairs that the last value at that level removed, and nothing else changed the current domains of the later variables since then, because every deeper level has already put back its own removals before the search returned through line L5. So the current domains are again those compatible with the assignment to the earlier variables. Part 3 holds because the untried values only lose the values that line L7 takes. $\square$

**Lemma 2 (pruning is safe).** If line L9 removes $b$ from $CD[j]$ while $x_i = a$, then no solution extends $\sigma_i$ and gives $b$ to $x_j$. If line L10 finds $CD[j] = \emptyset$, then no solution extends $\sigma_i$.

*Proof.* The value $b$ is removed because $(a, b) \notin C_{ij}$, so an assignment with $x_i = a$ and $x_j = b$ violates $C_{ij}$. By Lemma 1, after line L9 the set $CD[j]$ is the set of values compatible with $\sigma_i$. If it is empty, every value of $x_j$ violates some constraint with $x_1, \ldots, x_i$, so no extension of $\sigma_i$ is a solution. $\square$

**Theorem 1 (soundness).** Each assignment that line L11 returns or records is a solution.

*Proof.* At line L11, $i = n$ and $x_n = a$ with $a \in CD[n]$. By Lemma 1, $\sigma_{n-1}$ is consistent and $a$ is compatible with $\sigma_{n-1}$, so $\sigma_n$ satisfies every constraint. $\square$

**Theorem 2 (completeness).** If the CSP has a solution, FORWARD-CHECKING returns one. In the all-solutions mode it records every solution exactly once.

*Proof.* Let $\tau$ be a solution. We show by induction on $k$ that the search sets $\sigma_k = \tau_k$ at some time, or stops earlier with another solution. For $k = 0$ this is true. Assume the search sets $\sigma_{k-1} = \tau_{k-1}$ and enters level $k$. By Lemma 1, $CD[k]$ is then the set of values compatible with $\tau_{k-1}$, which contains $\tau(x_k)$ because $\tau$ is a solution. The untried values of $x_k$ are $CD[k]$, and the level is left through line L5 only when no untried value is left. Values are tried one at a time, and while the search is below level $k$ the value of $x_k$ does not change. So, unless the search stops with a solution first, line L7 takes $a = \tau(x_k)$ at some time. Then $\sigma_k = \tau_k$. For $k < n$, the future domains after line L9 are the values compatible with $\tau_k$, and each holds the value of $\tau$, so line L10 passes and the search enters level $k + 1$. For $k = n$, line L11 records $\tau$.

Each value is taken at most once at a level for a fixed assignment to the earlier variables, and a solution is recorded only at the node where $\sigma_n$ equals it, so no solution is recorded twice. The loop ends. Each iteration either makes a new node at line L7 or moves up one level at line L5. A node is a partial assignment $\sigma_i$, and by the remark above no node is made twice, so there are at most $d + d^2 + \cdots + d^n$ of them. A level is left upward at most once after each entry, and each entry follows a node, so the number of moves up is at most the number of nodes plus one. So if no solution exists, the algorithm returns failure at line L13. $\square$

**Theorem 3 (fewer nodes than backtracking).** With the same variable order and the same value order, each node of the forward checking tree (each assignment made at line L7) is a node of the tree of chronological backtracking, and the first solution is the same.

*Proof.* A node of forward checking is an assignment $\sigma_i$ whose last value $\sigma(x_i)$ is in $CD[i]$, so by Lemma 1 $\sigma_{i-1}$ is consistent and $\sigma_i$ is consistent. Chronological backtracking tries, at level $i$, every value of $D(x_i)$ below every consistent $\sigma_{i-1}$, and it goes below exactly the consistent assignments. By induction on $i$, every consistent $\sigma_{i-1}$ whose prefixes forward checking enters is a node that backtracking enters, and $\sigma_i$ is one of its children. Both trees are traversed depth first with the same value order, and both meet the solutions in the order of the full tree of all assignments, so the first solution is the same. $\blacksquare$
