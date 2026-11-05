---
title: The compact-forward algorithm lists every triangle exactly once
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a simple undirected graph, and let $\eta : V \to \{0, \ldots, n-1\}$ be the bijection of line L1. After line L2, each list $\mathrm{Adj}[x]$ holds the neighbours of $x$ in increasing order of $\eta$. For a vertex $v$ and a vertex $x$, write $N_{<v}(x) = \{y \in \mathrm{Adj}[x] : \eta(y) < \eta(v)\}$; since $\mathrm{Adj}[x]$ is sorted by $\eta$, $N_{<v}(x)$ is a prefix of $\mathrm{Adj}[x]$.

**Termination.** Lines L4 and L5 run over finite lists. Each pass of the loop of lines L7 to L11 increases $i$ or $j$ or both, and both are bounded by the lengths of the lists, so each merge stops. So the algorithm stops.

**Lemma 1 (the merge).** For an edge $\{v, u\}$ with $\eta(v) < \eta(u)$, lines L6 to L11 append $\{a, v, u\}$ exactly for the vertices $a \in N_{<v}(v) \cap N_{<v}(u)$, once each.

*Proof.* Write $p = \mathrm{Adj}[v]$ and $q = \mathrm{Adj}[u]$, and let $p'$ and $q'$ be their prefixes $N_{<v}(v)$ and $N_{<v}(u)$. The loop of line L7 runs while $i$ is inside $p'$ and $j$ is inside $q'$, since the entries of $p$ and $q$ with $\eta < \eta(v)$ are exactly the prefixes.

We show the invariant: every common element $c$ of $p'$ and $q'$ that is not yet appended has position at least $i$ in $p$ and at least $j$ in $q$, and no element is appended twice. At the start, $i = j = 0$ and nothing is appended. In a pass with $a = p[i]$ and $b = q[j]$:

- If $\eta(a) < \eta(b)$, then $a$ is not in $q'$ at a position $\ge j$, since $q$ is sorted and $q[j]$ already has a larger $\eta$; and by the invariant, $a$ is not a common element at a position $< j$ that is still to be found. So $a$ is not a common element still to be found, and skipping it keeps the invariant.
- The case $\eta(a) > \eta(b)$ is symmetric.
- If $\eta(a) = \eta(b)$, then $a = b$, since $\eta$ is injective. It is common to both prefixes, and it is appended now. Both indices move past it, and since the lists are sorted and have no repeated entries, it is not met again.

When the loop stops, $i$ has passed the end of $p'$ or $j$ the end of $q'$, so by the invariant no common element is left to find. An element appended is a common element by the third case. $\square$

**Theorem.** COMPACT-FORWARD$(G)$ returns each triangle of $G$ exactly once, and each set it returns is a triangle.

*Proof.* *Only triangles.* By Lemma 1, a returned set $\{a, v, u\}$ has $\{v, u\} \in E$ (line L5), $a \in \mathrm{Adj}[v]$ and $a \in \mathrm{Adj}[u]$, and $\eta(a) < \eta(v) < \eta(u)$, so the three vertices are distinct and pairwise adjacent.

*Each triangle at least once.* Let $\{x, y, z\}$ be a triangle, named so that $\eta(x) < \eta(y) < \eta(z)$. Line L4 reaches $v = y$, line L5 reaches $u = z$ since $z \in \mathrm{Adj}[y]$ and $\eta(z) > \eta(y)$, and $x \in N_{<y}(y) \cap N_{<y}(z)$. By Lemma 1, $\{x, y, z\}$ is appended in this merge.

*Each triangle at most once.* Every append of $\{x, y, z\}$ happens in the merge for some pair $(v, u)$ with $\{a, v, u\} = \{x, y, z\}$ and $\eta(a) < \eta(v) < \eta(u)$. This order is unique, so $a = x$, $v = y$, $u = z$. Line L5 visits each pair $(v, u)$ once, since $u$ occurs once in $\mathrm{Adj}[v]$, and Lemma 1 appends $x$ once in that merge. $\blacksquare$
