---
title: With the flat ball kernel every mean shift path stops at a fixed point, and the regions are connected and well separated
proves: [correctness]
status: full
---

Scale every pixel point $x_j = (x_j^s, x_j^r)$ to $p_j = (x_j^s / h_s, x_j^r / h_r)$. Then the window of a point $y$ (in scaled coordinates) is $W(y) = \{ j : \lVert p_j - y \rVert^2 \le 1 \}$, a mean shift step is $y' = \frac{1}{|W(y)|} \sum_{j \in W(y)} p_j$, and scaling back is a bijection, so it is enough to argue in scaled coordinates. Let

$$f(y) = \sum_j k\bigl(\lVert p_j - y \rVert^2\bigr), \qquad k(u) = \max(1 - u, 0),$$

the Epanechnikov density estimate without its constant factor.

**Lemma 1 (each step goes uphill).** If $W(y) \ne \emptyset$ and $y'$ is the mean of $W(y)$, then $f(y') - f(y) \ge |W(y)| \, \lVert y' - y \rVert^2$.

*Proof.* Write $u_j = \lVert p_j - y \rVert^2$ and $u_j' = \lVert p_j - y' \rVert^2$. For $j \in W(y)$, $u_j \le 1$, so $k(u_j) = 1 - u_j$, and $k(u_j') \ge 1 - u_j'$ because $k(u) \ge 1 - u$ for every $u$. So $k(u_j') - k(u_j) \ge u_j - u_j'$. For $j \notin W(y)$, $k(u_j) = 0 \le k(u_j')$. Adding up,

$$f(y') - f(y) \ge \sum_{j \in W(y)} \bigl(\lVert p_j - y \rVert^2 - \lVert p_j - y' \rVert^2\bigr) = |W(y)| \, \lVert y - y' \rVert^2,$$

where the last step is the identity $\sum_{j \in S} \lVert p_j - y \rVert^2 = \sum_{j \in S} \lVert p_j - \bar p \rVert^2 + |S| \lVert \bar p - y \rVert^2$ for the mean $\bar p$ of a finite set $S$. $\square$

**Lemma 2 (windows are never empty).** On a path that starts at a pixel point, every window is nonempty.

*Proof.* At the start $y = p_i$, and $i \in W(p_i)$. By Lemma 1, $f$ does not decrease along the path, so $f(y) \ge f(p_i) \ge k(0) = 1$ at every later point. Then some $j$ has $k(\lVert p_j - y \rVert^2) > 0$, that is $\lVert p_j - y \rVert^2 < 1$, so $j \in W(y)$. $\square$

**Theorem 1 (finite convergence).** Every path of lines L2 to L4 stops after finitely many steps at a point $y$ with $y$ equal to the mean of $W(y)$.

*Proof.* After the first step, every point of the path is the mean of a nonempty subset of the $N$ pixel points, and there are at most $2^N - 1$ such means. As long as the path moves, $y' \ne y$, so by Lemma 1 and Lemma 2, $f(y') > f(y)$. The values of $f$ along a moving path are therefore strictly increasing, so no point repeats, and a path that never stopped would visit infinitely many distinct points of a finite set. So the path stops, and the test $y = y_{\text{old}}$ at line L4 holds, which says that $y$ is the mean of its own window. With exact arithmetic the test is exact. $\square$

The proof uses only that $k$ is convex and decreasing with $k(u) = 1 - u$ inside the window, which is the case of Theorem 1 of Comaniciu and Meer for the Epanechnikov profile. It does not apply to a window that tests position and color separately, which is not a ball in the joint space. The tests give an image where that window makes a path of period 2.

**Theorem 2 (the regions).** Let $z_i$ be the mode of pixel $i$. After line L7, every region is 4-connected, all its pixels lie in one cluster of line L6, and two 4-adjacent pixels in different regions lie in different clusters. After line L8, either one region is left or every region has at least $M$ pixels, and every region is still connected.

*Proof.* Line L6 builds the graph on the pixels with an edge between $i$ and $j$ when $\lVert z_i^s - z_j^s \rVert < h_s$ and $\lVert z_i^r - z_j^r \rVert < h_r$, and takes its connected components; pixels with the same mode are joined, since their distance is 0. Line L7 takes, for each cluster, the connected components of its pixels in the image grid. So each region is connected and lies in one cluster. If two adjacent pixels were in the same cluster, the flood of line L7 would have put them in the same region, so adjacent pixels in different regions are in different clusters. Line L8 merges a region into an adjacent region; the union of two connected sets that touch is connected. Each merge lowers the number of regions by one, so the loop ends, and it ends only when the smallest region has at least $M$ pixels or a single region is left. $\square$
