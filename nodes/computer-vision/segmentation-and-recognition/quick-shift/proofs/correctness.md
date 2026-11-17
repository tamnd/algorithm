---
title: Correctness of quick shift
proves: [correctness]
status: full
---

This proof covers lines L1 to L10 of the main page. The input is a gray image of $W \times H$ pixels, the kernel width $\sigma > 0$, the link limit $\tau > 0$ (possibly $\infty$) and the color weight $\lambda \ge 0$. Pixel $i = (u_i, v_i)$ has the feature $f_i = (u_i, v_i, \lambda I_i)$ and the density $P_i$ of line L3. The key of pixel $i$ is the pair $(P_i, i)$, compared in lexicographic order. The proof says what the output is. It does not say that the segments match objects; that is a matter of the image and the parameters.

**Definition (the quick shift forest).** For each pixel $i$, let $N_\tau(i)$ be the set of pixels $j$ with $(P_j, j) > (P_i, i)$ and $\lVert f_i - f_j \rVert \le \tau$. If $N_\tau(i)$ is empty, $i$ is a root and $\mathrm{parent}_\tau(i) = i$. Otherwise $\mathrm{parent}_\tau(i)$ is the $j \in N_\tau(i)$ with the least distance $\lVert f_i - f_j \rVert$, and among equal distances the least index $j$.

**Lemma 1 (the window search finds the defined parent).** Lines L4 to L8 set $\mathrm{parent}(i) = \mathrm{parent}_\tau(i)$ for each pixel $i$.

*Proof.* If $\lVert f_i - f_j \rVert \le \tau$, then $|u_i - u_j| \le \tau$ and $|v_i - v_j| \le \tau$, because these are two of the three coordinates of $f_i - f_j$. The differences are integers, so they are at most $\lceil \tau \rceil$, and $j$ lies in the square window of line L6. For $\tau = \infty$ the window is the whole image. So the loop of L6 visits every member of $N_\tau(i)$. Line L7 keeps exactly the members of $N_\tau(i)$. The window is visited in raster order, which is increasing index order, and line L8 replaces the best pixel only on a strictly smaller distance. So the loop ends with the nearest member of $N_\tau(i)$ and, among equal distances, the one with the least index. If $N_\tau(i)$ is empty, the loop keeps $\mathrm{parent}(i) = i$ and the distance $\infty$. $\square$

**Lemma 2 (the links form a forest).** Along each link $i \to \mathrm{parent}(i) \ne i$ the key strictly increases. So the links have no cycle, every walk along the links reaches a root after fewer than $WH$ steps, and each pixel belongs to the tree of exactly one root.

*Proof.* A link $i \to j$ needs $(P_j, j) > (P_i, i)$ by line L7. Keys are pairwise distinct, because the indices are. A cycle would need a key larger than itself. A walk along the links visits pixels with strictly increasing keys, so it visits each pixel at most once and stops at a pixel without a link, which is a root. $\square$

**Lemma 3 (labels).** Line L9 gives each pixel the root of its tree, and line L10 returns the label map of these roots.

*Proof.* The loop of L9 walks from $i$ until it meets a pixel whose root is already known or a root. By Lemma 2 the walk stops. It then gives the found root to every pixel on the walk. Each of these pixels is on the walk from $i$ to that root, so the root is correct for all of them. Each pixel enters a walk list at most once, because after that its root is known. $\square$

**Lemma 4 (roots are local maxima of the density).** A pixel $i$ is a root if and only if no pixel within feature distance $\tau$ has a larger key. For $\tau = \infty$ there is exactly one root, the pixel with the largest key.

*Proof.* This is the definition of $N_\tau(i) = \emptyset$. For $\tau = \infty$ every pixel except the one with the largest key has a pixel with a larger key, and all pixels are within distance $\infty$. $\square$

**Theorem (one tree gives all the segmentations).** Let $\tau' \le \tau$. For each pixel $i$, $\mathrm{parent}_{\tau'}(i) = \mathrm{parent}_\tau(i)$ if $d_\tau(i) = \lVert f_i - f_{\mathrm{parent}_\tau(i)} \rVert \le \tau'$, and $\mathrm{parent}_{\tau'}(i) = i$ otherwise. So cutting the links longer than $\tau'$ in the forest for $\tau$ gives the forest for $\tau'$, and each segment for $\tau'$ lies inside one segment for $\tau$.

*Proof.* The densities do not depend on $\tau$. $N_{\tau'}(i) = \{ j \in N_\tau(i) : \lVert f_i - f_j \rVert \le \tau' \}$. If the nearest member of $N_\tau(i)$ is within $\tau'$, it is also the nearest member of $N_{\tau'}(i)$, with the same tie rule. If it is farther than $\tau'$, every member of $N_\tau(i)$ is farther than $\tau'$, so $N_{\tau'}(i)$ is empty and $i$ is a root for $\tau'$. Each link of the forest for $\tau'$ is a link of the forest for $\tau$, so each tree for $\tau'$ lies inside one tree for $\tau$. $\square$

With $\tau = \infty$ the forest is one tree over the whole image (Lemma 4), and the theorem says that the segmentations for all smaller $\tau$ come from it by cutting long links. This is the hierarchy that Vedaldi and Soatto describe.

**Cost.** Let $r_1 = \lceil 3 \sigma \rceil$ and $r_2 = \lceil \tau \rceil$. Lines L2 and L3 do $O((2 r_1 + 1)^2)$ work per pixel, and lines L4 to L8 do $O((2 r_2 + 1)^2)$ work per pixel. Line L9 is $O(WH)$ in total by Lemma 3. With $k = (2 r_1 + 1)^2 + (2 r_2 + 1)^2$, the total is $O(W H k)$ time in the real-RAM model, with one exponential and one square root counted as $O(1)$, and $O(WH)$ extra space.
