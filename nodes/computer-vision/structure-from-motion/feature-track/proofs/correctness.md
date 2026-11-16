---
title: BUILD-TRACKS returns the connected components of the match graph with the right consistency flags
proves: [correctness]
status: full
---

We use the notation of the page. The match graph $G$ has the matched features as vertices and the matches as edges. Let $G_t$ be the graph on the same vertices with only the first $t$ matches as edges.

**Claim.** BUILD-TRACKS returns one group for each connected component of $G$, the group holds exactly the features of that component, and its flag is true if and only if no image occurs twice in it.

**Cost.** There are at most $2m$ vertices for $m$ matches. With union by size and path halving, the $O(m)$ operations of lines L1 to L5 take $O(m\,\alpha(m))$ time, where $\alpha$ is the inverse Ackermann function (Tarjan and van Leeuwen). Line L7 takes time linear in the size of the group with a hash set, so the whole run takes $O(m\,\alpha(m))$ expected time and $O(m)$ space.

**Invariant.** After line L3 has run for the first $t$ matches, two features $f$ and $g$ that have been added have the same root, $\mathrm{FIND}(f) = \mathrm{FIND}(g)$, if and only if they are connected in $G_t$.

**Proof of the invariant.** For $t = 0$ no feature has been added, so the claim is empty. Assume it for $t - 1$, and let the match $t$ be $(a, b)$. Line L2 adds $a$ and $b$ as singleton sets if they are new; a new feature has no edge in $G_{t-1}$, so it is alone in its component, and it is alone in its set, which keeps the invariant. Line L3 then calls $\mathrm{UNION}(a, b)$. Union by size makes one of the two roots a child of the other and changes no other parent pointer, and path halving only moves a pointer to a node higher on the same path, so it keeps every root. So after the union the sets are those before, with the set of $a$ and the set of $b$ merged into one. In the graph, adding the edge $(a, b)$ merges the component of $a$ and the component of $b$ and leaves the others as they are. By the induction hypothesis, the sets before the union were the components of $G_{t-1}$ on the added features, so the sets after the union are the components of $G_t$. $\square$

**Proof of the claim.** After the loop of lines L1 to L3, every vertex of $G$ has been added, because every vertex is an end of some match, and by the invariant with $t = m$, two vertices have the same root if and only if they are connected in $G$. Lines L4 and L5 put each vertex into the group of its root. So two vertices are in the same group if and only if they are in the same component, and each group is exactly one component. Line L7 compares the number of distinct images in the group with the size of the group. These two numbers are equal if and only if the map from a feature to its image is one to one on the group, which is the definition of a consistent track. Line L8 returns every group with its flag. $\blacksquare$
