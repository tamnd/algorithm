---
title: Each step of Misra-Gries colors one more edge and keeps the coloring proper
proves: [correctness, termination]
status: full
---

Let $k = \Delta + 1$. A partial edge coloring is *proper* when two colored edges with a common end have different colors. A color is free at $x$ when no colored edge at $x$ has it. Every vertex has at most $\Delta < k$ edges, so it always has a free color.

We show: if before a turn of line L1 the colored edges form a proper partial coloring and $uv$ is uncolored, then after the turn the same holds with $uv$ colored and no colored edge uncolored. The loop runs once per edge, so it terminates, and by induction the final coloring is proper with all edges colored and colors in $\{1, \ldots, k\}$.

**Rotation.** Let $(f_0, \ldots, f_j)$ be a fan at $u$. After the rotation, $u f_i$ has the old color of $u f_{i+1}$ for $i < j$, and $u f_j$ is uncolored. At $u$, the edges $u f_0, \ldots, u f_{j-1}$ now carry the old colors of $u f_1, \ldots, u f_j$, and $u f_j$ carries none, so the set of colors at $u$ is unchanged and no color repeats. At $f_i$ for $i < j$, the new color of $u f_i$ was free at $f_i$ by the fan condition, and $f_i$ has no other changed edge. So the result is proper.

**Swap.** For colors $c \ne d$, the edges colored $c$ or $d$ form vertex-disjoint paths and cycles. Swapping $c$ and $d$ on one whole component keeps the coloring proper: inside the component, consecutive edges still differ, and at an end $x$ of a path, the color that the end edge gets was free at $x$, since $x$ is an end. If $c$ is free at $u$, then $u$ meets at most one edge of color $c$ or $d$, so $u$ is an end of its component, which is the cd-path at $u$ (empty if $d$ is also free at $u$). If $c = d$, then $d$ is free at $u$ and the path is empty.

**Line L4 frees $d$ at $u$.** If $d$ was free at $u$, nothing changes. Otherwise the first edge of the path is the edge at $u$ of color $d$, which becomes $c$, and $c$ was free at $u$. So after line L4, $d$ is free at $u$.

**Line L5 succeeds.** Let $F = (f_0, \ldots, f_t)$ be the maximal fan of line L2, $c$ free at $u$ and $d$ free at $f_t$, all before line L4. It suffices to exhibit one $j$ such that, after line L4, $(f_0, \ldots, f_j)$ is a fan and $d$ is free at $f_j$; the first such $j$ also qualifies.

- *$d$ was free at $u$.* The path is empty, $F$ is unchanged and $d$ is free at $f_t$. Take $j = t$.
- *$d$ was not free at $u$.* Let $ux$ be the edge of color $d$. Since $d$ is free at $f_t$, the vertex $x$ would extend $F$ if $x \notin F$, and $x \ne f_0$ because $u f_0$ is uncolored. So $x = f_{s+1}$ with $0 \le s < t$, and $d$ is free at $f_s$ by the fan condition. No edge $u f_i$ with $i \ne s + 1$ has color $c$ or $d$, as $c$ is free at $u$ and $d$ is used at $u$ only by $u f_{s+1}$. The swap changes only colors $c$ and $d$, so for $i \ne s + 1$, the edge $u f_i$ keeps its color, and that color stays free or not free at each vertex as before. Let $P$ be the cd-path at $u$; it starts with the edge $u f_{s+1}$.
  - *$P$ does not end at $f_s$.* Since $d$ is free at $f_s$, the vertex $f_s$ meets at most one edge of $P$'s colors, so if it were on $P$ it would be an end; the ends are $u$ and some vertex other than $f_s$. So $f_s \notin P$, and $d$ stays free at $f_s$. The conditions for $(f_0, \ldots, f_s)$ involve only the edges $u f_1, \ldots, u f_s$, which keep their colors, so it is still a fan. Take $j = s$.
  - *$P$ ends at $f_s$.* The last edge of $P$ at $f_s$ had color $c$, because $d$ was free there, so after the swap $c$ is free at $f_s$, and $u f_{s+1}$ now has color $c$. So the condition for $f_{s+1}$ holds again, and the conditions for the other indices are unchanged: $F$ is still a fan. The vertex $f_t$ is not on $P$: it would have to be an end, since $d$ is free at $f_t$, and the ends are $u$ and $f_s \ne f_t$. So $d$ is still free at $f_t$. Take $j = t$.

**Lines L6 and L7.** Let $w = f_j$ be the vertex found at line L5. Rotating the fan $(f_0, \ldots, w)$ keeps the coloring proper, colors $u f_0 = uv$, and uncolors $uw$. The rotation does not add any color at $u$, and at $w$ it only removes the color of $uw$, so $d$ is still free at both $u$ and $w$. Line L7 colors $uw$ with $d$, which keeps the coloring proper. All edges colored before the turn are colored after it, and $uv$ is now colored too. ∎
