---
title: Correctness of the distance-driven projector
proves: [correctness]
status: full
---

We use the conventions of the page. The image is $n \times n$ on $[-1, 1]^2$ with $h = 2/n$, the view has $c = \cos\theta$ and $\sigma = \sin\theta$, and bin $q$ is $J_q = [s_0 + qw, s_0 + (q+1)w]$ for $0 \le q < d$. We treat the case $|c| \ge |\sigma|$, where the lines are rows and $\Delta = h/|c|$. The column case is the same with $x$ and $y$ exchanged. We work in exact arithmetic.

**The model.** For row $k$, let $g_k(s)$ be the value of the pixel of row $k$ whose part of the center line $y = y_k$ the ray $\{x c + y\sigma = s\}$ meets, and $0$ if it meets none. The model value of bin $q$ is
$$P_q = \frac{1}{w}\int_{J_q} \Delta \sum_{k=0}^{n-1} g_k(s)\,ds.$$
We prove that DD-VIEW returns $\text{out}[q] = P_q$ for all $q$, that the back projector is the transpose, and the two exact facts of the page.

**Lemma 1 (the borders, line L4).** On the center line of row $k$, pixel $(k, j)$ is the segment $-1 + jh \le x \le -1 + (j+1)h$. The ray with parameter $s$ meets it if and only if $s$ lies between $(-1 + jh)c + y_k\sigma$ and $(-1 + (j+1)h)c + y_k\sigma$.

*Proof.* On the line $y = y_k$, the map $x \mapsto x c + y_k\sigma$ is affine with slope $c \ne 0$ (since $|c| \ge |\sigma|$ and $c^2 + \sigma^2 = 1$, $|c| \ge 1/\sqrt{2}$). So it maps the segment of the pixel onto the interval between the images of its ends, one to one. $\square$

So the shadows of the $n$ pixels of row $k$ are the $n$ intervals between neighbors of the list $B$, each of length $h|c|$, and they tile the interval $[B[0], B[n]]$. If $c < 0$, the list decreases in $j$; line L4 reverses it, and pixel $p$ of the sorted list is column $n - 1 - p$. Lines L4 and L5 give two increasing lists. Call the cells $U_p = [B[p], B[p+1]]$ and $V_q = [D[q], D[q+1]] = J_q$.

**Lemma 2 (the sweep, lines L6 to L10).** The loop visits every pair $(p, q)$ with $|U_p \cap V_q| > 0$ exactly once, and line L8 sets $\ell = |U_p \cap V_q|$ for it.

*Proof.* For two closed intervals, $\min$ of the right ends minus $\max$ of the left ends is the length of the intersection when it is positive, and it is $\le 0$ when they overlap in at most one point. So line L8 is correct, and line L9 adds a term only for pairs with positive overlap.

Each step increases $p$ or $q$ by one, so no pair is visited twice, and the loop ends after at most $n + d$ steps. Invariant: when the loop is at $(p, q)$, every pair $(p', q')$ with positive overlap and with $p' < p$ or $q' < q$ was visited. It holds at $(0, 0)$. Suppose the loop moves from $(p, q)$ to $(p + 1, q)$, because $B[p+1] < D[q+1]$. The pairs that the move gives up are $(p, q')$ with $q' > q$. For those, $V_{q'}$ starts at $D[q'] \ge D[q+1] > B[p+1]$, so $U_p$ ends before $V_{q'}$ begins and the overlap is zero. The move to $(p, q+1)$ with $D[q+1] \le B[p+1]$ is the same with the roles exchanged: $U_{p'}$ with $p' > p$ starts at $B[p'] \ge B[p+1] \ge D[q+1]$, so it meets $V_q$ in at most one point. When the loop stops, $p = n$ or $q = d$. If $p = n$, every pair with a positive overlap has $p' < n$ and was visited. If $q = d$, the same holds for the bins. $\square$

**Theorem (the forward projector).** DD-VIEW returns $\text{out}[q] = P_q$.

*Proof.* By Lemma 1, $g_k(s) = f[k][j(p)]$ for $s$ in the interior of $U_p$, where $j(p)$ is the column of sorted pixel $p$, and $g_k(s) = 0$ outside $[B[0], B[n]]$. The ends of the intervals are a finite set and do not change the integral. So
$$\frac{1}{w}\int_{J_q}\Delta g_k(s)\,ds = \sum_{p} \frac{\Delta\,|U_p \cap V_q|}{w}\, f[k][j(p)].$$
By Lemma 2, line L9 adds exactly the terms of this sum with positive overlap, for each row $k$ that line L3 visits. Summing over $k$ gives $P_q$. $\square$

**Theorem (the transpose).** Let $W$ be the list of triples $(q, \text{pixel}, \Delta\ell/w)$ that line L9 uses for all views. The forward projector is $y_q = \sum_{(q, \pi, \omega) \in W} \omega f_\pi$, and the back projector of the code is $z_\pi = \sum_{(q, \pi, \omega) \in W} \omega\, g_q$. Then $\langle y, g\rangle = \sum_W \omega f_\pi g_q = \langle f, z\rangle$ for all $f$ and $g$, so the back projector is $A^T$. A pixel and a bin may appear in two triples only if they come from two views, which are different rows of $A$, so the sum over $W$ is the sum over the nonzero entries of $A$. $\square$

**Corollary 1 (mass).** If $s_0 \le \min_k B[0]$ and $s_0 + dw \ge \max_k B[n]$ for a view, then $w \sum_q \text{out}[q] = h^2 \sum_{i,j} f[i][j]$.

*Proof.* Under the hypothesis, the bins tile an interval that contains each $U_p$. So $\sum_q |U_p \cap V_q| = |U_p| = h|c|$. Then $w\sum_q \text{out}[q] = \sum_{k,p} \Delta\, h|c|\, f[k][j(p)] = \sum_{k,p} h^2 f[k][j(p)]$. $\square$

**Corollary 2 (a constant image).** Let $f \equiv 1$ and let bin $J_q$ lie inside every interval $[B[0], B[n]]$, $k = 0, \ldots, n - 1$. Then $\text{out}[q] = n\Delta = 2/|c|$.

*Proof.* For each row, the $U_p$ tile an interval that contains $J_q$, so $\sum_p |U_p \cap J_q| = w$, and the row adds $\Delta$. $\square$

The intervals $[B[0], B[n]]$ of the rows are $[-|c| + y_k\sigma, |c| + y_k\sigma]$, and $|y_k| < 1$. So the condition of Corollary 2 holds for every bin with $|s_{\text{center}}| + w/2 \le |c| - |\sigma|$, which is the condition that the test uses.

**Corollary 3 (axis-aligned rays).** At $\theta = 0$, $\text{out}[q]$ is the average over $J_q$ of the exact line integral of the pixel-square image $\sum f[i][j]\chi_{ij}$.

*Proof.* At $\theta = 0$ the ray is the vertical line $x = s$. For $s$ inside column $j$, it crosses every row in a segment of length $h = \Delta$ inside pixel $(k, j)$, so the line integral is $\sum_k \Delta f[k][j] = \Delta\sum_k g_k(s)$. Integrate over $J_q$ and divide by $w$. $\square$

**Remark (the approximation).** For other angles the model differs from the line integral of the pixel-square image. The ray crosses row $k$ along a segment of length $\Delta$, which may pass through two pixels of the row, while the model gives the whole length $\Delta$ to the pixel at the center line. For one row, the difference is at most $\Delta$ times the jump of $f$ between the two neighbors, and it occurs only for the rays whose segment in the row crosses a pixel border. For an image with a bounded gradient the jump is $O(h)$, so the difference per row is $O(h^2)$ and the sum over the $n$ rows is $O(h)$. This is a property of the model, not of the code.

**Cost.** By Lemma 2 the sweep of one line takes at most $n + d$ steps of $O(1)$ work, and lines L4 and L5 take $O(n + d)$. With $n$ lines per view and $a$ views, the time is $O(a n (n + d))$ in the real-RAM model, and the extra space is that of the two lists, $O(n + d)$.
