---
title: Best-first branch and bound returns an optimal leaf and expands only nodes with bound at least the optimum
proves: [correctness, termination, optimality]
status: full
---

We use the pseudocode of the page. $T$ is a finite rooted tree. Some nodes are *leaves*, the feasible solutions, and $f$ gives each leaf a value; an inner node with no children is a dead end. The bound satisfies $ub(N) \ge f(x)$ for each node $N$ and each leaf $x$ in the subtree of $N$, which we write $x \preceq N$. Let $z^* = \max \{ f(x) : x \text{ a leaf of } T \}$, with $z^* = -\infty$ if $T$ has no leaf. In $H$ each node $N$ has the key $ub(N)$.

**Claim 1 (the incumbent is real).** At each point, either $z = -\infty$ and $best = \text{NIL}$, or $best$ is a leaf and $z = f(best)$. In particular $z \le z^*$. *Proof.* Only line L7 changes $z$ and $best$, and it sets them to $f(N)$ and $N$ for a leaf $N$. $\square$

**Claim 2 (invariant).** At the start of each iteration of line L3, every leaf $x$ with $f(x) > z$ satisfies $x \preceq M$ for some node $M$ in $H$.

*Proof.* At the start $H = \{root\}$. Suppose the claim holds at the start of an iteration that does not stop at line L5. Let $z_0$ and $z_1$ be the values of $z$ at the start and at the end of the iteration, so $z_0 \le z_1$, and let $N$ be the node taken at line L4. Let $x$ be a leaf with $f(x) > z_1$. Then $f(x) > z_0$, so $x \preceq M$ for a node $M$ that was in $H$. If $M \ne N$, then $M$ is still in $H$. If $M = N$ and $N$ is a leaf, then $x = N$ and line L7 gives $z_1 \ge f(x)$, which is false. If $M = N$ is an inner node, then $x \preceq C$ for a child $C$ of $N$; if line L10 inserts $C$, it is in $H$, and if not, $f(x) \le ub(C) \le z_0$, which is false. $\square$

**Claim 3 (termination).** Each node joins $H$ at most once: the root at line L2, and any other node only at line L10 while its parent is expanded, which happens at most once by induction on depth. So the loop runs at most $|T|$ times. $\square$

**Theorem 1.** The algorithm returns $(z^*, best)$, where $best$ is a leaf with $f(best) = z^*$, or $best = \text{NIL}$ when $T$ has no leaf.

*Proof.* By Claim 3 the loop ends, either because $H$ is empty or by the break at line L5. If $H$ is empty, Claim 2 says no leaf has $f(x) > z$. If line L5 breaks with node $N$, then $N$ had the largest key, so every node $M$ of $H$ and $N$ itself has $ub(M) \le ub(N) \le z$, and so every leaf $x \preceq M$ has $f(x) \le z$; by Claim 2, applied at the start of this iteration, no leaf has $f(x) > z$. In both cases $z \ge z^*$, and with Claim 1, $z = z^*$. If $T$ has a leaf, $z^* > -\infty$, so $best$ is a leaf of value $z^*$. If not, line L7 never runs and $best = \text{NIL}$. $\square$

**Theorem 2.** Every node $N$ that the algorithm expands has $ub(N) \ge z^*$.

*Proof.* When $N$ is expanded, line L5 did not break, so $ub(N) > z$. If $z = z^*$, then $ub(N) > z^*$. If $z < z^*$, then an optimal leaf $x^*$ has $f(x^*) > z$, so by Claim 2 $x^* \preceq M$ for a node $M$ that was in $H$ when $N$ was taken; $N$ had the largest key, so $ub(N) \ge ub(M) \ge f(x^*) = z^*$. $\square$

**Theorem 3.** Call $N$ critical if every node on the path from the root to $N$, including $N$, has $ub > z^*$. Any search that starts with only the root live, keeps $z$ equal to the value of a leaf or $-\infty$, makes live each child $C$ of an expanded node with $ub(C) > z$, and removes a live inner node only by expanding it or when $ub(N) \le z$, expands every critical inner node, provided it runs until no live node remains or until all live nodes have $ub \le z$.

*Proof.* By induction on depth, every critical node becomes live. The root is live at the start. If a critical node $N$ is live, then $ub(N) > z^* \ge z$ at all times, so the search cannot stop while $N$ is live and cannot remove $N$ by its bound; if $N$ is an inner node, it is expanded, and each critical child $C$ has $ub(C) > z^* \ge z$ and becomes live. $\blacksquare$
