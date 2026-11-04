---
title: Depth-first branch and bound returns an optimal leaf
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. $T$ is a finite rooted tree, $f$ gives a value to each leaf, and $ub$ satisfies $ub(N) \ge f(x)$ for each node $N$ and each leaf $x$ in the subtree of $N$, which we write $x \preceq N$. Here a *leaf* is a node that the test of line L6 marks as a complete solution; an inner node can also have no children, and it is then a dead end, not a leaf. Let $z^* = \max \{ f(x) : x \text{ a leaf of } T \}$, with $z^* = -\infty$ if $T$ has no leaf.

**Claim 1 (the incumbent is real).** At each point of the run, either $z = -\infty$ and $best = \text{NIL}$, or $best$ is a leaf of $T$ and $z = f(best)$. *Proof.* This holds after line L1. Only line L7 changes $z$ and $best$, and it sets them to $f(N)$ and $N$ for a leaf $N$. $\square$

**Claim 2 (z only grows).** Line L7 changes $z$ only to a larger value. $\square$

**Claim 3 (invariant).** At the start of each iteration of line L3, every leaf $x$ with $f(x) > z$ satisfies $x \preceq M$ for some node $M$ on $S$.

*Proof.* Before the first iteration, $S = \{root\}$ and every leaf is below the root. Suppose the claim holds at the start of an iteration, let $z_0$ be the value of $z$ then, and let $N$ be the node popped at line L4. Let $x$ be a leaf with $f(x) > z_1$, where $z_1 \ge z_0$ is the value of $z$ at the end of the iteration. Then $f(x) > z_0$, so $x \preceq M$ for a node $M$ that was on $S$. If $M \ne N$, then $M$ is still on $S$. Suppose $M = N$, so $x \preceq N$.

- If line L5 drops $N$, then $f(x) \le ub(N) \le z_0 \le z_1$, which is false.
- If $N$ is a leaf, then $x = N$, and after line L7 we have $z_1 \ge f(N) = f(x)$, which is false.
- Otherwise $N$ is an inner node and $x \preceq C$ for a child $C$ of $N$. If line L10 pushes $C$, then $C$ is on $S$ at the end of the iteration. If it does not, then $ub(C) \le z_0$, so $f(x) \le ub(C) \le z_0 \le z_1$, which is false.

In each case the claim holds at the start of the next iteration. $\square$

**Claim 4 (termination).** Each node of $T$ is pushed at most once, so the loop runs at most $|T|$ times. *Proof.* The root is pushed once, at line L2. Any other node $C$ is pushed only at line L10, while its parent $N$ is expanded, and by induction on depth $N$ is popped at most once, so it is expanded at most once. $\square$

**Theorem.** DFBB stops and returns $(z^*, best)$, where $best$ is a leaf with $f(best) = z^*$, or $best = \text{NIL}$ when $T$ has no leaf.

*Proof.* By Claim 4 the loop ends, and then $S$ is empty. By Claim 3 no leaf $x$ has $f(x) > z$, so $z \ge z^*$. By Claim 1, either $z = -\infty \le z^*$, or $z = f(best) \le z^*$ for a leaf $best$. So $z = z^*$. If $T$ has a leaf, $z^* > -\infty$, so $best$ is a leaf with $f(best) = z^*$. If $T$ has no leaf, line L7 never runs, so $best = \text{NIL}$. $\blacksquare$
