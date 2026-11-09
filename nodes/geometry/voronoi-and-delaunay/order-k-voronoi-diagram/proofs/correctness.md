---
title: The level-by-level construction of the order-k Voronoi diagram is correct
proves: [correctness]
status: full
---

**Claim.** Let $P$ be a set of $n$ distinct sites in the plane, $k \ge 1$, and $B$ a closed axis-parallel box of positive area. If $n < k$, ORDER-K-BUILD returns no cell. Otherwise it returns, for each $S \subseteq P$ with $|S| = k$ such that $V(S) \cap B$ has positive area, exactly the polygon $V(S) \cap B$ with its corners in counterclockwise order, and no other set. For every $q \in B$, $\mathrm{locate}(q)$ returns a nonempty list of sets, each a set of $k$ nearest sites of $q$, and it returns exactly $[S]$ when $S$ is the only set of $k$ nearest sites of $q$.

No general position is assumed. For $j \ge 0$ and $|T| = j$ let $V(T) = \{x : |x - s| \le |x - u| \text{ for all } s \in T, u \in P \setminus T\}$, with $V(\emptyset)$ the whole plane. Each $V(T)$ is an intersection of closed half-planes, hence closed and convex.

**Lemma 1 (refinement).** Let $|S| = j + 1 \le n$. For $t \in S$ let $W_t(S) = V(S \setminus \{t\}) \cap \{x : |x - t| \le |x - u| \text{ for all } u \in P \setminus S\}$. Then $V(S) = \bigcup_{t \in S} W_t(S)$.

*Proof.* Let $x \in W_t(S)$. For $s \in S \setminus \{t\}$ and $u \in P \setminus S$, we have $u \notin S \setminus \{t\}$, so $|x - s| \le |x - u|$ because $x \in V(S \setminus \{t\})$. For $s = t$ the inequality is the second condition. So $x \in V(S)$.

Conversely let $x \in V(S)$, and let $t$ be a site of $S$ at the largest distance from $x$ among the sites of $S$. For $s \in S \setminus \{t\}$ and $u \notin S \setminus \{t\}$: if $u \notin S$ then $|x - s| \le |x - u|$ because $x \in V(S)$, and if $u = t$ then $|x - s| \le |x - t|$ by the choice of $t$. So $x \in V(S \setminus \{t\})$, and $|x - t| \le |x - u|$ for $u \notin S$ because $x \in V(S)$. So $x \in W_t(S)$. $\square$

In the code, for a cell $C$ of the set $T$ and a site $t \notin T$, line L5 computes $C \cap \{x : |x - t| \le |x - u| \text{ for all } u \notin T \cup \{t\}\}$. With $S = T \cup \{t\}$, this is $C \cap \{x : |x - t| \le |x - u|, u \in P \setminus S\}$, which is $W_t(S) \cap B$ when $C = V(T) \cap B$.

**Lemma 2 (the cutting step).** For a convex polygon $C$ given by its corners in counterclockwise order and a closed half-plane $\{a x + b y \le c\}$, the routine $\mathrm{clip}$ returns the corners of $C \cap \{a x + b y \le c\}$ in counterclockwise order, with no repeated corner and no corner inside a side, when this set has positive area, and returns no polygon otherwise.

*Proof.* Walking around $C$, the routine keeps each corner with $a x + b y \le c$ and adds the crossing point of each side whose two ends are strictly on different sides of the line. The intersection of a convex polygon with a half-plane is a convex polygon whose corners are the kept corners and the crossing points, met in this order along the boundary of $C$. The cleanup removes repeated points and points between two collinear neighbours, and a list of fewer than three points left after this has no area. The arithmetic is exact, so all signs are right. $\square$

**Lemma 3 (zero-area parts do not matter).** Let $K$ be a convex polygon of positive area, and let $K = Z \cup \bigcup_i A_i$, where $Z$ is a finite union of closed sets of zero area that are convex, so points and segments, and each $A_i$ is a closed convex polygon. Then $K = \bigcup_i A_i$, and $K$ is the convex hull of the corners of the $A_i$.

*Proof.* The union $A = \bigcup_i A_i$ is closed. A point $y$ of the interior of $K$ that is not in $A$ has a small open disc around it that misses $A$, so the disc lies in $Z$, which is a finite union of points and segments and contains no disc. So $A$ contains the interior of $K$, and being closed it contains its closure, which is $K$. Then $K = A$ is the convex hull of the corners of the $A_i$, since each $A_i$ is the convex hull of its corners and $K$ is convex. $\square$

**Invariant.** After the $j$-th pass of line L2, for $j \le \min(k, n)$, the dictionary holds, for each $T$ with $|T| = j$ and $V(T) \cap B$ of positive area, the polygon $V(T) \cap B$, and no other key. For $j = 0$ this is line L1, because $V(\emptyset) \cap B = B$.

Assume it after pass $j$, and let $|S| = j + 1$. By Lemma 1, $V(S) \cap B = \bigcup_{t \in S} (W_t(S) \cap B)$, and $W_t(S) \cap B \subseteq V(S \setminus \{t\}) \cap B$. Split the sets $W_t(S) \cap B$ into those that line L6 adds and the others. A set $W_t(S) \cap B$ is not added either because $V(S \setminus \{t\}) \cap B$ has zero area, and then $W_t(S) \cap B$ is a convex set of zero area, or because the piece itself has zero area (Lemma 2, applied $n - j - 1$ times; once a cutting step returns nothing, the code stops cutting and adds nothing). So $V(S) \cap B$ is the union of the added pieces and of finitely many convex sets of zero area.

If $V(S) \cap B$ has positive area, Lemma 3 shows that it is the union of the added pieces and the convex hull of their corners, which line L7 computes; the monotone chain method returns the corners in counterclockwise order and drops points inside sides. If $V(S) \cap B$ has zero area, then every piece inside it has zero area, none is added, and $S$ is not a key. A key $S$ of line L7 always has an added piece of positive area, so $V(S) \cap B$ has positive area. This proves the invariant for pass $j + 1$.

The loop makes $\min(k, n)$ passes. If $n \ge k$, the claim on the cells follows. If $n < k$, the code returns no cell, and indeed no set of $k$ sites exists.

**locate.** By the invariant the stored polygons are the sets $V(S) \cap B$ of positive area. The test with $\mathrm{orient}$ against each side of a counterclockwise convex polygon decides exactly whether $q$ is in the closed polygon. If it is in $V(S)$, then $S$ is a set of $k$ nearest sites of $q$, by the definition of $V(S)$. The cells $V(S) \cap B$ over all $S$ cover $B$, since every point has some set of $k$ nearest sites; by Lemma 3 with $K = B$, the cells of positive area already cover $B$, so the list is not empty. If $S$ is the only set of $k$ nearest sites of $q$, every returned set is such a set and so equals $S$, and the list is $[S]$ because the keys are distinct.

**Neighbouring cells.** Let $V(S)$ and $V(S')$, $S \ne S'$, share a segment $\sigma$ of positive length. Two different sites have one bisector, and the bisectors of $p, q$ and of $p, s$ for $q \ne s$ are different lines, so they meet in at most one point. So all but finitely many points $x$ of $\sigma$ lie on no two of the finitely many bisectors. Fix such an $x$, and let $\delta$ be the $k$-th smallest distance from $x$ to the sites, $L$ the sites at distance less than $\delta$ and $E$ the sites at distance exactly $\delta$. Both $S$ and $S'$ are sets of $k$ nearest sites, so both contain $L$ and are inside $L \cup E$. As $S \ne S'$, $|E| \ge 2$; as $x$ is on no two bisectors, $|E| = 2$, say $E = \{p, q\}$. Then $|L| = k - 1$, and $S = L \cup \{p\}$, $S' = L \cup \{q\}$ or the reverse. So $S \setminus S' = \{p\}$ and $S' \setminus S = \{q\}$ (or the reverse) and $x$ is on the bisector of $p$ and $q$. The sites $p$ and $q$ are fixed by $S$ and $S'$, so every point of $\sigma$ but finitely many is on this bisector, and since $\sigma$ is a closed segment and the bisector a closed line, all of $\sigma$ is on it. With $A = S \cap S'$, $|A| = k - 1$, $S = A \cup \{p\}$ and $S' = A \cup \{q\}$.

**Extremes.** For $k = 1$, $V(\{p\})$ is the Voronoi cell of $p$ by definition. For $k = n - 1$, $V(P \setminus \{p\}) = \{x : |x - s| \le |x - p| \text{ for all } s \ne p\}$, the farthest cell of $p$. For $k = n$ the only set is $P$ and $V(P)$ is the plane, since there is no condition. $\blacksquare$
