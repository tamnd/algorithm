---
title: BUILD keeps the partition invariant and BACK-TO-FRONT gives a painter's order
proves: [correctness, termination]
status: full
---

We use the names of the pseudocode. The input is a list $S$ of segments of positive length, no two of which cross or touch. For a node $t$, the function $\sigma_t$ is affine, so on a segment from $p$ to $q$ its value at the point $p + \lambda(q - p)$ is $(1 - \lambda)\sigma_t(p) + \lambda \sigma_t(q)$.

**Invariant (P).** For each node $t$: (1) each fragment of $t.on$ lies on $t.line$; (2) each fragment of the subtree $t.front$ has $\sigma_t \ge 0$ at both ends, and not $\sigma_t = 0$ at both ends; (3) the same for $t.back$ with $\sigma_t \le 0$; (4) the fragments of each input segment cover it and meet only at their ends.

**Fact 1.** Let a fragment $f$ have $\sigma_t \ge 0$ at both ends and not $0$ at both. Then $\sigma_t > 0$ at each point of the relative interior of $f$. *Proof.* At such a point the value is a combination of the two end values with positive weights, both at least 0 and one positive. $\square$ The mirror statement holds for $\le 0$.

**BUILD.** By induction on $|S|$, BUILD$(S)$ returns a tree that satisfies (P) and whose fragments, for each segment of $S$, cover it and meet only at their ends. Line L1 handles $S$ empty. Otherwise each segment $r \ne s$ goes to exactly one case. If $\sigma_t$ is 0 at both ends, $r$ lies on the line and joins $t.on$ (part 1). If the end values are both $\ge 0$ and not both 0, $r$ goes to $F$; if both $\le 0$ and not both 0, to $K$. Otherwise one value is positive and the other negative, so line L8 cuts $r$ at the point with $\lambda = \sigma_t(p) / (\sigma_t(p) - \sigma_t(q)) \in (0, 1)$, where $\sigma_t = 0$. The front part has end values $\sigma_t(p) > 0$ and $0$, the back part $0$ and a negative value, so parts 2 and 3 hold for them, and the two parts cover $r$ and meet only at the cut point, so part 4 holds. The lists $F$ and $K$ have at most $|S| - 1$ entries each, since $s$ goes to neither, so the induction applies to them and the recursion stops. The argument for BUILD does not use the condition that the segments do not cross; only the claim below does. Parts 2 and 3 for $t$ hold because every fragment in the subtree $t.front$ is a part of a member of $F$, which lies in the closed front half-plane, and a part of a segment with both end values $\ge 0$ has both end values $\ge 0$ and, by Fact 1, does not lie on the line. INSERT is the same filter for one segment, so it keeps (P) too.

**Hiding.** For a viewpoint $v$, say that a fragment $f$ *hides* a point $y$ if $v$ is not on the line of $f$ and the open segment from $v$ to $y$ meets the relative interior of $f$. When $v$ is on the line of $f$, the fragment is seen edge on and covers nothing. A list of fragments is a *painter's order* for $v$ if no fragment hides a point of the relative interior of a fragment that comes later.

**Claim.** BACK-TO-FRONT$(t, v)$ outputs the fragments of the subtree $t$ in a painter's order for $v$.

*Proof.* By induction on the height. The empty tree is clear. Let $t$ have children with outputs that are painter's orders by induction. A pair of fragments from one child keeps its order. For the list $t.on$: its fragments all lie on $t.line$. If $v$ is not on the line, the segment from $v$ to a point $y$ of the line meets the line only at $y$, so it misses the other fragments of $t.on$ except at $y$, which is not on the open segment. If $v$ is on the line, no fragment of $t.on$ hides anything by definition. It remains to treat pairs from different parts.

*Case $\sigma_t(v) > 0$, order back, on, front (line L11).* Let $f$ come from the back subtree, and $g$ from $t.on$ or the front subtree, and let $y$ be in the relative interior of $g$. By parts 1 and 2 and Fact 1, $\sigma_t(y) \ge 0$. Each point of the open segment from $v$ to $y$ has $\sigma_t = (1 - \lambda)\sigma_t(v) + \lambda\sigma_t(y) > 0$ with $\lambda \in (0, 1)$. By part 3 and Fact 1, the relative interior of $f$ has $\sigma_t < 0$. So the open segment misses it, and $f$ does not hide $y$. Let $f$ come from $t.on$ and $g$ from the front subtree: the interior of $f$ has $\sigma_t = 0$, and the same computation shows the open segment has $\sigma_t > 0$, so again $f$ does not hide $y$.

*Case $\sigma_t(v) < 0$ (line L12)* is the mirror image, with front and back swapped.

*Case $\sigma_t(v) = 0$, order front, on, back (line L13).* Let $f$ come from the front subtree and $g$ from $t.on$ or the back subtree, with $y$ in the relative interior of $g$. By parts 1 and 3 and Fact 1, $\sigma_t(y) \le 0$. If $\sigma_t(y) < 0$, each point of the open segment has $\sigma_t = \lambda\sigma_t(y) < 0$, while the interior of $f$ has $\sigma_t > 0$, so they do not meet. If $\sigma_t(y) = 0$, then $g$ is in $t.on$ by Fact 1, and the whole segment from $v$ to $y$ lies on $t.line$, where $\sigma_t = 0$; the interior of $f$ has $\sigma_t > 0$, so they do not meet. Let $f$ come from $t.on$ and $g$ from the back subtree: then $v$ is on the line of $f$, so $f$ hides nothing.

In every case no earlier fragment hides a point of a later one, which proves the claim. Each node is expanded once, so the walk stops after $O(m)$ steps. $\blacksquare$
