---
title: Df-pn stops with the right answer on finite trees and always expands a most-proving node
proves: [correctness, termination, complexity]
status: full
---

We use the pseudocode DFPN and MID of the page, without the 1 + ε trick except where we say so. The input is a finite AND/OR tree: each node is an OR node or an AND node, the types alternate, each terminal node is *proved* or *disproved*, and a node that is not terminal has at least one child. Distinct nodes have distinct table keys, and the table never loses an entry. We use the definitions and Lemma 1 of the [correctness proof of proof-number search](/proof-number-search/proofs/correctness/).

**The explored tree.** A node is *expanded* once line L4 has run for it. At any time let $T$ be the tree that holds the root, every expanded node and all children of expanded nodes. A leaf of $T$ is a terminal node or a *frontier node*, one that is neither terminal nor expanded. Let $\mathrm{pn}_T$ and $\mathrm{dn}_T$ be the proof and disproof numbers of $T$ computed from scratch by the rules of the page: $(0, \infty)$ and $(\infty, 0)$ at proved and disproved terminal nodes, $(1, 1)$ at frontier nodes, minimum and sum at expanded nodes. The *current pair* of a node is its table entry if it has one, else $(1, 1)$; terminal nodes get their fixed pair the first time they are looked at.

**The stack.** When MID runs on $n$, it calls MID only on children of $n$. So at any time the active calls are on a path $n_0, n_1, \ldots, n_k$ from the root, where $n_{j+1}$ is a child of $n_j$, and a node below $n$ can be expanded or written to the table only while the call on $n$ is active.

**Lemma 1 (the table holds the numbers of $T$).** At any time, every node $x$ of $T$ that is not on the stack has the current pair $(\mathrm{pn}_T(x), \mathrm{dn}_T(x))$. Inside the call on $n_k$, the pair that line L6 computes for $n_k$ is $(\mathrm{pn}_T(n_k), \mathrm{dn}_T(n_k))$.

*Proof.* Terminal and frontier nodes have the right pair by definition. Let $x$ be an expanded node not on the stack. Then a call on $x$ has run line L4 and has returned, and its last act was line L7: it stored the pair computed in line L6 from the current pairs of its children, with no child call after that computation. Since the call returned, no node below $x$ has been expanded or written to the table, so the children of $x$ in $T$ and their current pairs are the same as then. By induction on the height of $x$ in $T$, those children have the pairs $(\mathrm{pn}_T, \mathrm{dn}_T)$, so the pair stored for $x$ is the rule applied to them, which is $(\mathrm{pn}_T(x), \mathrm{dn}_T(x))$. For the second part, the children of $n_k$ are not on the stack, so line L6 applies the rule to their numbers in $T$. $\square$

**Lemma 2 (a child is entered below its thresholds).** Every call MID$(c, t_p, t_d)$ made in line L10 or L13 starts with $\mathrm{pn}_T(c) < t_p$ and $\mathrm{dn}_T(c) < t_d$. This also holds with the 1 + ε trick.

*Proof.* Let $n$ be the parent of $c$, with thresholds $(\mathrm{thpn}, \mathrm{thdn})$, and let $(p, q)$ be the pair of $n$ in the last line L6; by Lemma 1 the pair of each child is its pair in $T$. Line L7 did not return, so $p < \mathrm{thpn}$ and $q < \mathrm{thdn}$. Let $n$ be an OR node; the AND case is the dual. Then $\mathrm{pn}_T(c) = p < \mathrm{thpn}$, and $\mathrm{pn}_T(c) \le p_2 < p_2 + 1$ when $p_2$ is finite, while $p_2 + 1 = \infty > p$ when $p_2 = \infty$; the 1 + ε bound is at least $p_2 + 1$. So $\mathrm{pn}_T(c) < t_p$. Next $q = \sum \mathrm{dn}_T \ge \mathrm{dn}_T(c)$ and $q < \mathrm{thdn}$. If $\mathrm{thdn} = \infty$, then $t_d = \infty$ and $\mathrm{dn}_T(c) \le q < \infty$. Otherwise $\mathrm{dn}_T(c) < \mathrm{thdn} - q + \mathrm{dn}_T(c) = t_d$ is the same as $q < \mathrm{thdn}$. $\square$

In particular the call is never on a terminal node, since $(0, \infty)$ and $(\infty, 0)$ are not below any pair of thresholds.

**Lemma 3 (each call expands a new node).** A call MID$(n, t_p, t_d)$ that starts with $\mathrm{pn}_T(n) < t_p$ and $\mathrm{dn}_T(n) < t_d$ expands at least one node that was not expanded before it started.

*Proof.* By induction on the height of $n$ in the full tree. If $n$ is a frontier node, line L4 expands it. Otherwise $n$ is expanded and not on the stack before the call, so by Lemma 1 the first line L6 gives $(\mathrm{pn}_T(n), \mathrm{dn}_T(n))$, which is below the thresholds. So line L7 does not return, and the call makes a child call, which by Lemma 2 starts below its thresholds and by the induction hypothesis expands a new node. $\square$

**Theorem 1 (termination and correctness).** On a finite tree with $N$ interior nodes and depth $d$, DFPN makes at most $(d + 1) N + 1$ calls of MID, and it returns true exactly when the root is proved.

*Proof.* If the root is terminal, there is one call. Otherwise the root call starts with $(1, 1)$ or with its pair in $T$, below $(\infty, \infty)$, and every other call starts below its thresholds by Lemma 2. So by Lemma 3 every call expands a new node during its run. Give each call the first new node that it expands. A node $m$ is expanded once for the first time, at a moment when at most $d + 1$ calls are active, so at most $d + 1$ calls get $m$. There are at most $N$ nodes to expand, so there are at most $(d + 1) N$ calls. The loop of each call makes a child call in each turn except the last, so every call ends.

The root call returns only in line L7 with $\mathrm{pn} \ge \infty$ or $\mathrm{dn} \ge \infty$. At that time the stack is empty, so by Lemma 1 every node of $T$ has its pair in $T$, and the rules hold at every node of $T$. By Lemma 1 of proof-number search, $\mathrm{dn}(\text{root}) = \infty$ means $\mathrm{pn}(\text{root}) = 0$ and the root is proved, and $\mathrm{pn}(\text{root}) = \infty$ means $\mathrm{dn}(\text{root}) = 0$ and the root is disproved. Line L2 returns true exactly in the first case. $\square$

**Theorem 2 (most-proving nodes, Nagai).** Without the 1 + ε trick, when df-pn expands a frontier node $m$ on the stack $n_0, \ldots, n_k = m$, then for each $j < k$, $n_{j+1}$ has the smallest $\mathrm{pn}_T$ among the children of $n_j$ if $n_j$ is an OR node, and the smallest $\mathrm{dn}_T$ if it is an AND node, where $T$ is the explored tree just before $m$ is expanded. So the path is a selection path of proof-number search in $T$, and $m$ is a most-proving node of $T$.

*Proof.* Write $(t_p^j, t_d^j)$ for the thresholds of the call on $n_j$. We show from $j = k$ down to $j = 0$ that $\mathrm{pn}_T(n_j) < t_p^j$ and $\mathrm{dn}_T(n_j) < t_d^j$, and that $n_{j+1}$ is a best child of $n_j$. For $j = k$, the call on $m$ started below its thresholds by Lemma 2 (or $m$ is the root), and $m$ has not changed.

Let $j < k$ and let $n_j$ be an OR node; the AND case is the dual. When $n_j$ called $n_{j+1}$, it computed $p_2$, the smallest proof number of the other children, and the sum $S$ of their disproof numbers. Those children are not on the stack and nothing below them has changed since, so they still have these numbers in $T$. By the induction hypothesis $\mathrm{pn}_T(n_{j+1}) < t_p^{j+1} = \min(t_p^j, p_2 + 1)$. This gives $\mathrm{pn}_T(n_{j+1}) \le p_2$, so $n_{j+1}$ has the smallest proof number, and $\mathrm{pn}_T(n_j) = \mathrm{pn}_T(n_{j+1}) < t_p^j$. For the disproof number, $\mathrm{dn}_T(n_j) = S + \mathrm{dn}_T(n_{j+1})$. At the time of the call, the parent's disproof number $q$ was below $t_d^j$, so $S \le q$ is finite. If $t_d^j = \infty$, then $\mathrm{dn}_T(n_{j+1}) < t_d^{j+1} = \infty$ and $\mathrm{dn}_T(n_j) < \infty$. Otherwise $t_d^{j+1} = t_d^j - q + \mathrm{dn}(n_{j+1}) = t_d^j - S$ with the old numbers, and $\mathrm{dn}_T(n_j) = S + \mathrm{dn}_T(n_{j+1}) < S + t_d^{j+1} = t_d^j$.

So each step of the path goes to a child with the smallest proof number at an OR node and the smallest disproof number at an AND node. The proof of Theorem 2 of proof-number search uses only this property of the path, so it applies, and $m$ lies in a smallest proof set and in a smallest disproof set of the root of $T$. $\square$

With the 1 + ε trick, $t_p^{j+1}$ can be larger than $p_2 + 1$, and the first step of the argument fails: df-pn may stay in a child after a sibling has become the better one. Theorems 1 and 3 still hold, because Lemma 2 and Lemma 3 do. When two children tie, proof-number search and df-pn may break the tie in different ways, so the two can expand different most-proving nodes.

**Theorem 3 (cost).** Let $b$ be the largest number of children. The time is $O(N b d)$, with each move generation, terminal test and table access counted as $O(1)$ per position, and the space is $O(N b)$ table entries and $O(b d)$ for the recursion.

*Proof.* Each turn of the loop of a call costs $O(b)$ for line L6 and the choice in line L9 or L12, and each call costs $O(b)$ for lines L3 and L4. Each turn either returns, once per call, or makes a child call, once per call except the root call. So there are at most twice as many turns as calls, and by Theorem 1 the time is $O(b ((d + 1) N + 1)) = O(N b d)$. The table holds entries only for nodes of $T$, at most $1 + N b$. The stack has at most $d + 1$ frames, each holding the children of its node. $\square$

When the root is an OR node with a proved terminal child, the root call sees $\mathrm{dn} = \infty$ in its first line L6 and returns, which costs $O(b)$: the best case of the page.

**Graphs.** On a directed acyclic graph a node can have several parents, so it can change while a call on one parent is not active, and Lemma 1 fails: a stored pair can be out of date. Kishimoto and Müller showed that df-pn is still complete on finite acyclic graphs with an unbounded table, and that it is not complete on graphs with cycles.
