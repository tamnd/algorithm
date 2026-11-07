---
title: Cost of the elimination tree algorithms
proves: [time.worst, space.extra, symbolic.worst]
status: full
---

**ETREE.** Lines L1 and L2 cost $\Theta(n)$. Each of the $m$ nonzeros starts one climb. The forest given by the pointers $\mathrm{anc}$ is a disjoint-set forest: a climb from $i$ is a find that follows pointers to the root $r$ of the set of $i$ and redirects every node passed, and setting $\mathrm{anc}[r] = k$ for the new singleton $k$ is a link with the new root on top, done before the compression it accompanies. So iteration $k$ performs finds and links of a sequence with $m$ finds and at most $n - 1$ links, with full path compression and arbitrary linking. Tarjan and van Leeuwen (1984) bound such a sequence by $O(n + m \log_{2 + m/n} n)$ pointer operations, which is $O(n + m \log n)$. Each find also costs $\Omega(1)$, so the time is at least $\Omega(n + m)$.

**ROW-PATTERN.** Lines L10 and L12 run once per nonzero of row $k$ of $A$ plus once per iteration of line L13. Each iteration of line L13 marks an unmarked node, which then appears in the output, so there are $|R|$ of them, and lines L9, L11, L14 and L15 cost $O(1 + |R|)$. Total $O(1 + |\text{row } k \text{ of } A| + |\text{row } k \text{ of } L|)$.

**Symbolic factorization.** Summing over $k$ gives $\Theta(n + m + z)$: at least the input and output, and at most a constant times their size.

**POSTORDER.** Building the child lists and the depth first search touch each node and each tree edge a constant number of times: $\Theta(n)$.

**Space.** $\mathrm{parent}$, $\mathrm{anc}$, the marks, the child lists and the explicit stack have $O(n)$ entries; outputs excluded, the extra space is $\Theta(n)$. $\blacksquare$
