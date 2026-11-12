---
title: Pineda rasterization outputs exactly the pixels whose centers the triangle covers
proves: [correctness]
status: full
---

We use the names of the pseudocode. The vertices are integers in units of $1/s$ pixel, $s$ is even, and the center of pixel $(i, j)$ is the integer point $c_{ij} = (s i + s/2,\ s j + s/2)$. "Covered" means covered under the [top-left fill rule](/top-left-fill-rule/): after the triangle is oriented so that $E_k > 0$ inside, $p$ is covered if for each $k$, $E_k(p) > 0$, or $E_k(p) = 0$ and edge $k$ is top-left. All arithmetic is on integers and is exact, by property 7 of the [edge function](/edge-function/).

**Claim.** For each pixel $(i, j)$ with $0 \le i < W$ and $0 \le j < H$, PINEDA-RASTERIZE outputs $(i, j)$ if and only if the triangle covers $c_{ij}$, and it outputs $(i, j)$ at most once.

**Step 1: the degenerate case.** If $S_2 = 0$, the three vertices are on one line and the triangle has an empty interior. Line L2 returns the empty set, and by the definition of the problem a triangle with zero area covers no pixel.

**Step 2: the orientation.** After line L3, $E_{v_0 v_1}(v_2) > 0$. Swapping $v_1$ and $v_2$ does not change the set of points of the triangle, so it does not change which centers are covered, and the rule is defined for this orientation. By property 5 of the edge function, $E_0(p) + E_1(p) + E_2(p) = S_2$, and $E_k(v_k) = S_2 > 0$, so $E_k > 0$ holds at the vertex opposite edge $k$ and the inside of the triangle is the set where all $E_k > 0$.

**Step 3: the setup.** Line L5 computes $A_k$, $B_k$ and $C_k$ such that $E_k(p) = A_k p_x + B_k p_y + C_k$ for the edge from $v_{k+1}$ to $v_{k+2}$; this is the expansion in the definition of the edge function. Line L6 sets $\mathrm{bias}_k = 0$ exactly when edge $k$ is top-left. For an integer $E$ and this bias,

$$E + \mathrm{bias}_k \ge 0 \iff \big(E > 0 \text{ or } (E = 0 \text{ and edge } k \text{ is top-left})\big),$$

because for a top-left edge both sides say $E \ge 0$, and otherwise both sides say $E \ge 1$. So the triangle covers $c_{ij}$ if and only if $E_k(c_{ij}) + \mathrm{bias}_k \ge 0$ for $k = 0, 1, 2$. Call this test $(\ast)$.

**Step 4: the skipped pixels.** Let $x_{\min}$ and $x_{\max}$ be the least and greatest $x$ of the vertices. A covered point is in the closed triangle, so its $x$ is in $[x_{\min}, x_{\max}]$. The $x$ of $c_{ij}$ is $s i + s/2$, which is in $[x_{\min}, x_{\max}]$ if and only if $\lceil (x_{\min} - s/2)/s \rceil \le i \le \lfloor (x_{\max} - s/2)/s \rfloor$. Line L7 takes this range and clips it to $0 \le i \le W - 1$, and does the same for $j$. So each pixel of the screen that is not in $\{i_0, \ldots, i_1\} \times \{j_0, \ldots, j_1\}$ has a center that is not covered, and the algorithm does not output it, which is correct. If the clipped range is empty, no pixel of the screen is covered and the output is empty.

**Step 5: the invariant.** We show that when line L11 runs for row $j$,

$$R_k = E_k(c_{i_0 j}) + \mathrm{bias}_k \quad (k = 0, 1, 2), \tag{R}$$

and that when line L13 runs for pixel $(i, j)$,

$$e_k = E_k(c_{ij}) + \mathrm{bias}_k \quad (k = 0, 1, 2). \tag{e}$$

For the first row, line L8 sets $(x, y) = c_{i_0 j_0}$ and line L9 sets $R_k = E_k(c_{i_0 j_0}) + \mathrm{bias}_k$, so (R) holds. If (R) holds for row $j$, line L11 sets $e_k = R_k$, which is (e) for $i = i_0$. If (e) holds for pixel $(i, j)$, line L14 adds $s A_k$, and $c_{i+1, j} = c_{ij} + (s, 0)$, so by property 4 of the edge function $E_k(c_{i+1, j}) = E_k(c_{ij}) + s A_k$, and (e) holds for pixel $(i + 1, j)$. In the same way, line L15 adds $s B_k$, $c_{i_0, j+1} = c_{i_0 j} + (0, s)$, and (R) holds for row $j + 1$. By induction on the rows, and inside a row on $i$, (e) holds at each run of line L13.

**Step 6: the conclusion.** By (e), line L13 outputs $(i, j)$ if and only if $(\ast)$ holds at $c_{ij}$, that is, if and only if the triangle covers $c_{ij}$. Each pair $(i, j)$ of the box is visited by the loops exactly once, so it is output at most once. With step 4, this proves the claim for every pixel of the screen.

**Termination.** The loop of line L10 runs $j_1 - j_0 + 1$ times and the loop of line L12 runs $i_1 - i_0 + 1$ times per row, both finite numbers fixed before the loops start. $\blacksquare$
