---
title: MAC is sound and complete, and its tree is part of the forward checking tree
proves: [correctness]
status: full
---

We use the pseudocode of the page, with the static order $x_1, \ldots, x_n$. For an assignment $\sigma_i$ to $x_1, \ldots, x_i$, a solution *extends* $\sigma_i$ if it agrees with $\sigma_i$ on $x_1, \ldots, x_i$. Write $S(\sigma_i, j)$ for the set of values that the solutions extending $\sigma_i$ give to $x_j$.

**Lemma 1 (arc consistency removes only unsupported values).** Let $CD$ be current domains, and assume every solution that extends $\sigma_i$ takes its values in $CD$. If line L11 removes $b$ from $CD[j]$, then no solution that extends $\sigma_i$ gives $b$ to $x_j$. So after lines L9 to L12, every solution that extends $\sigma_i$ still takes its values in $CD$. The same holds for line L1 with the empty assignment.

*Proof.* Line L11 removes $b$ because no $c \in CD[k]$ has $(b, c) \in C_{jk}$. A solution $\tau$ that extends $\sigma_i$ has $\tau(x_k) \in CD[k]$ by the assumption, and $(\tau(x_j), \tau(x_k)) \in C_{jk}$. So $\tau(x_j) \ne b$. The removals happen one at a time, and the assumption holds again after each one, so the claim follows by induction on the number of removals. Line L8 sets $CD[i] = \{a\} = \{\sigma(x_i)\}$, which keeps every solution that extends $\sigma_i$. $\square$

**Lemma 2 (invariant).** Each time line L5 runs at level $i$, with $\sigma_{i-1}$ the current assignment:

1. $CD[k] = \{\sigma(x_k)\}$ for $k < i$;
2. every value of $CD[j]$, $j \ge i$, is compatible with $\sigma_{i-1}$: for each $k < i$ with a constraint $C_{kj}$, $(\sigma(x_k), b) \in C_{kj}$;
3. every solution that extends $\sigma_{i-1}$ takes its values in $CD$;
4. the untried values of $x_i$ are the values of $CD[i]$ at the time level $i$ was entered, minus those taken since.

*Proof.* At the start, after line L1, parts 1 and 2 are empty statements, part 3 is Lemma 1 for the empty assignment, and part 4 holds by line L2.

The state of the current domains at the entry to level $i$ is restored by line L4 every time the search comes back to level $i$: line L4 puts back exactly the pairs that the last value at level $i$ removed, and every deeper level has put back its own removals before the search returned through line L6. So it is enough to check that the invariant passes from level $i$ to level $i + 1$ through line L15.

Line L8 sets $CD[i] = \{a\}$ with $a \in CD[i]$. By part 2, $a$ is compatible with $\sigma_{i-1}$, so $\sigma_i$ is consistent. Line L9 puts the arcs $(x_j, x_i)$ with $j > i$ in the queue. When the arc $(x_j, x_i)$ is revised, $CD[i] = \{a\}$, so every $b$ with $(b, a) \notin C_{ji}$ is removed, and the values left in $CD[j]$ are compatible with $x_i = a$. Later removals only make the domains smaller. So part 2 holds for $\sigma_i$ at level $i + 1$. Part 1 holds because $CD[i] = \{a\}$ and lines L11 and L12 never change the domain of a variable $x_k$ with $k \le i$ (the queue only holds arcs $(x_l, \cdot)$ with $l > i$). Part 3 holds by Lemma 1. Part 4 holds by line L15. $\square$

**Theorem 1 (soundness).** Every assignment that line L14 returns or records is a solution.

*Proof.* At line L14, $i = n$ and line L13 passed. By part 2 of Lemma 2 at level $n$, the value $a$ is compatible with $\sigma_{n-1}$, and by the same part at each earlier level, $\sigma(x_k)$ is compatible with $\sigma_{k-1}$ for every $k$. So every constraint holds. $\square$

**Theorem 2 (completeness).** If a solution $\tau$ exists, MAC returns a solution. In the all-solutions mode it records every solution exactly once.

*Proof.* By Lemma 1, line L1 keeps $\tau$ inside the current domains, so it does not return failure. We show by induction on $k$ that the search sets $\sigma_k = \tau_k$, unless it stops with a solution before. For $k = 0$ there is nothing to show. Assume the search enters level $k$ with $\sigma_{k-1} = \tau_{k-1}$. By part 3 of Lemma 2, $\tau(x_k) \in CD[k]$, so $\tau(x_k)$ is an untried value of $x_k$ by part 4. Level $k$ is left upward only when no untried value is left, so line L8 takes $a = \tau(x_k)$ at some time. Then by Lemma 1 every domain still holds the value of $\tau$, so no domain is empty at line L13. If $k < n$, line L15 enters level $k + 1$ with $\sigma_k = \tau_k$. If $k = n$, line L14 returns or records $\tau$.

A solution is recorded only at the node where $\sigma_n$ equals it, and each value is taken at most once at a level for a fixed assignment to the earlier variables, so no solution is recorded twice. Each iteration makes a new node at line L8 or moves up at line L6. There are at most $d + d^2 + \cdots + d^n$ nodes, and each move up follows an entry to a level, so the loop ends, with failure at line L16 if no solution was returned. $\square$

**Theorem 3 (part of the forward checking tree).** With the same variable order and value order, every node of MAC is a node of [forward checking](/forward-checking/). So MAC never visits more nodes than forward checking, and both return the same first solution.

*Proof.* Write $CD^{F}$ for the current domains of forward checking. We show by induction on $i$: if both methods enter level $i$ with the same $\sigma_{i-1}$, then $CD[j] \subseteq CD^{F}[j]$ for every $j \ge i$ at that time. At level 1, $CD^{F}[j] = D(x_j)$ and $CD[j] \subseteq D(x_j)$. Assume the claim at level $i$, and let both methods take the value $a$ at level $i$. Forward checking removes from $CD^{F}[j]$, $j > i$, the values $b$ with $(a, b) \notin C_{ij}$. MAC revises every arc $(x_j, x_i)$ with $CD[i] = \{a\}$ (each such arc is in the queue of line L9, and it is revised unless a wipe-out stops the loop first), so it removes the same values from the smaller set $CD[j]$, and then possibly more. So if forward checking goes to level $i + 1$, then either MAC finds a wipe-out at this node, or it also goes to level $i + 1$ and the claim holds there.

Now every value that MAC takes at level $i$ is in $CD[i] \subseteq CD^{F}[i]$, so every node of MAC is a node of forward checking. Both traverse their trees depth first with the same value order, and both meet the solutions in the order of the full tree of all assignments, so the first solution they return is the same. $\blacksquare$
