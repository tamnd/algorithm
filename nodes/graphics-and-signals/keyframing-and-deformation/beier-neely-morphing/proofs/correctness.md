---
title: The Beier-Neely warp reproduces its lines and rigid motions, and the morph starts and ends at the input images
proves: [correctness]
status: full
---

We use the notation of the page.
For a line $(P, Q)$ with $d = Q - P \ne 0$, let $\hat d = d/|d|$ and $\hat n = \operatorname{perp}(\hat d)$.
The pair $(\hat d, \hat n)$ is an orthonormal basis of the plane with the same orientation as the standard basis, because $\operatorname{perp}$ is the rotation by 90 degrees.

## One line pair

**Lemma 1.** For one line, lines L3 and L4 give $u = (X - P)\cdot\hat d/|d|$ and $v = (X - P)\cdot\hat n$, and $X = P + u\,d + v\,\hat n$.

*Proof.*
The first two equations are lines L3 and L4 with $\operatorname{perp}(d) = |d|\,\hat n$.
Since $(\hat d, \hat n)$ is orthonormal, $X - P = ((X - P)\cdot\hat d)\,\hat d + ((X - P)\cdot\hat n)\,\hat n = u\,d + v\,\hat n$. $\square$

**Lemma 2.** For one line pair, with $e = Q' - P'$, $\hat e = e/|e|$ and $\hat m = \operatorname{perp}(\hat e)$, line L5 is the map $X' = P' + R\,S\,(X - P)$, where $R$ is the rotation that takes $\hat d$ to $\hat e$ and $S$ scales the direction $\hat d$ by $|e|/|d|$ and fixes the direction $\hat n$. It takes $P$ to $P'$ and $Q$ to $Q'$.

*Proof.*
Line L5 is $X' = P' + u\,e + v\,\hat m = P' + (u|d|)\frac{|e|}{|d|}\hat e + v\,\hat m$.
By Lemma 1, $u|d|$ and $v$ are the coordinates of $X - P$ in the basis $(\hat d, \hat n)$.
$S$ multiplies the first coordinate by $|e|/|d|$, and $R$ maps $\hat d$ to $\hat e$ and, being a rotation, $\hat n = \operatorname{perp}(\hat d)$ to $\operatorname{perp}(\hat e) = \hat m$.
For $X = P$, $u = v = 0$ and $X' = P'$; for $X = Q$, $u = 1$, $v = 0$ and $X' = P' + e = Q'$. $\square$

**Corollary.** If the destination and source lines are the same, line L5 gives $X'_i = X$, by Lemma 1.

## Several line pairs

Let $w_i > 0$ be the weights of line L7 and $X'_i$ the points of line L5.
When the sum of line L9 is reached, $X' = X + \sum_i w_i(X'_i - X)/\sum_i w_i = \sum_i w_iX'_i/\sum_i w_i$, a convex combination of the $X'_i$.

**Lemma 3.** If there is a map $g$ with $X'_i = g(X)$ for every $i$, then the warp returns $g(X)$, whatever the weights.

*Proof.*
A convex combination of equal points is that point. $\square$

**Theorem 1.** If the same lines are used as destination and source, the warp is the identity. If every source line is the image of its destination line under one rigid motion $g(X) = RX + c$, the warp is $g$.

*Proof.*
The first claim follows from the corollary and Lemma 3.
For the second, $e_i = Rd_i$ and $|e_i| = |d_i|$, so $S = I$ in Lemma 2, and the rotation that takes $\hat d_i$ to $\hat e_i = R\hat d_i$ is $R$.
So $X'_i = P'_i + R(X - P_i) = RP_i + c + RX - RP_i = g(X)$ for every $i$, and Lemma 3 applies. $\square$

**Lemma 4.** The value $\text{dist}$ of line L6 is the distance from $X$ to the segment $P_iQ_i$.

*Proof.*
The closest point of the line to $X$ is $P_i + u\,d_i$, at the distance $|v|$, by Lemma 1.
If $0 < u < 1$, this point is on the segment.
If $u \le 0$, the distance to the points $P_i + s\,d_i$ with $s \in [0, 1]$ is $\sqrt{(u - s)^2|d_i|^2 + v^2}$, which is smallest at $s = 0$, so the distance is $|X - P_i|$; the case $u \ge 1$ is the same with $s = 1$. $\square$

**Theorem 2.** Let $X$ be a point of the segment $P_kQ_k$ that is not on any other destination segment. As $a \to 0$, the warp of $X$ tends to $X'_k$, the point at the same fraction $u$ of the source segment $P'_kQ'_k$. For $a = 0$ the implementation returns $X'_k$.

*Proof.*
By Lemma 4, $\text{dist}_k = 0$ and $\text{dist}_i > 0$ for $i \ne k$.
For $b > 0$, $w_k = (|d_k|^p/a)^b \to \infty$ as $a \to 0$, and the other weights stay bounded.
So the convex combination tends to $X'_k$.
On the segment $v = 0$, so $X'_k = P'_k + u\,e_k$ by line L5.
For $a = 0$, the implementation returns $X'_k$ as soon as it meets a line with $a + \text{dist} = 0$. $\square$

## The morph

**Theorem 3.** $M_0 = I_0$ and $M_1 = I_1$.

*Proof.*
At $t = 0$, line L10 gives $L^0$, so the warp of line L12 for $I_0$ has the same destination and source lines and returns $X_0 = X$ by Theorem 1.
Bilinear interpolation at a pixel center returns the pixel value, and line L13 has the weight 1 for $I_0$ and 0 for $I_1$.
The case $t = 1$ is the same with the roles of the images exchanged. $\square$

**Theorem 4.** Swapping $I_0$ with $I_1$ and $L^0$ with $L^1$, and replacing $t$ by $1 - t$, gives the same frame.

*Proof.*
The interpolated lines of line L10 are $(1 - (1 - t))L^1 + (1 - t)L^0 = (1 - t)L^0 + tL^1$, the same as before.
So the two warps of line L12 are the same, and line L13 gives $t\,I_1(X_1) + (1 - t)\,I_0(X_0)$, the same value. $\square$

No claim is made that the warp is one-to-one; with several lines it need not be.
