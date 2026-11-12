---
title: Correctness of distributed ray tracing
proves: [correctness]
status: full
---

**Claim.** For every pixel, the value stored by line L7 is an unbiased estimate of the pixel integral $\bar V_{ij}$ of the problem: its expectation over the random numbers is exactly $\bar V_{ij}$. This holds in exact arithmetic with exact uniform random numbers, given closest-hit and shadow queries that answer exactly at the time $t$, as the definition of $V_k$ assumes.

**Step 1, the stack walk.** Fix the random numbers. For a node $\nu$ of the ray tree, that is a ray with a depth $k$ and the numbers it draws, let $\hat\lambda(\nu)$ be the amount that lines L11 to L14 would add for it with the weight 1, and let its children be the rays pushed by lines L16 and L17, with the coefficients $k_s$ and $k_t$. Define the recursive estimate $\hat V(\nu) = \hat\lambda(\nu) + \sum_{\text{children } \mu} c_\mu\,\hat V(\mu)$. The walk of lines L8 to L18 keeps the invariant that $I$ plus the sum of $w \cdot \hat V$ over the stack equals $\hat V$ of the root: popping $(\nu, w)$ adds $w\,\hat\lambda(\nu)$ to $I$ and pushes the children with the weights $w\,c_\mu$, which is one unfolding of the definition. This is the argument of Whitted ray tracing word for word, since the only change is how the directions are chosen. The loop ends after at most $2^{D+1} - 1$ pops, and TRACE returns $\hat V$ of the root.

**Step 2, one node in expectation.** We show by induction on $j = D - k$ that for a node with $j$ levels left, the expectation of $\hat V$ over the numbers that the node and its descendants draw, given its ray and the time, is $V_j$.

*The local estimate.* The terms of $k_a$ and of the point lights are not random and equal those of $V_j$. For a disk light, the point $q$ comes from a uniform point of the unit square by $r = R_\ell\sqrt{u_1}$ and $\phi = 2\pi u_2$. The area of the disk inside the radius $r$ is $\pi r^2 = A_\ell\,u_1$, so $q$ is uniform on the disk, with the density $1/A_\ell$. Hence

$$\mathbb E\Big[\frac{k_d}{\pi}\,L_\ell A_\ell\,\frac{\cos\theta\cos\theta_\ell}{|q - p|^2}\,\mathrm{vis}(p, q)\Big] = \frac{k_d}{\pi}\int_{A_\ell} L_\ell\,\frac{\cos\theta\cos\theta_\ell}{|q - p|^2}\,\mathrm{vis}(p, q)\,dq,$$

which is the disk term of $V_j$; the factor is zero where a cosine is not positive, as the definition requires.

*The leaves.* For $j = 0$, line L15 pushes nothing and $V_0$ is the local term, so the claim is the statement just shown.

*The children.* For $j \ge 1$, line L16 draws $\omega$ by $\cos\alpha = u_1^{1/(e+1)}$ and $\phi = 2\pi u_2$ around the mirror direction. The angle is at most $\alpha$ exactly when $u_1 \ge \cos^{e+1}\alpha$, which has the probability $1 - \cos^{e+1}\alpha$. Its derivative in $\alpha$ is $(e + 1)\cos^e\alpha\,\sin\alpha$, and with the uniform $\phi$ and the solid angle element $\sin\alpha\,d\alpha\,d\phi$ the density of $\omega$ is $\frac{e + 1}{2\pi}\cos^e\alpha$, the lobe. The child is pushed only when $n \cdot \omega > 0$, which multiplies the lobe by the indicator of the upper side and gives $g_s$. The child draws its numbers from fresh calls to the generator, independent of $\omega$, so by the induction hypothesis its conditional expectation given $\omega$ is $V_{j-1}(\omega)$, and

$$\mathbb E\big[k_s\,[n\cdot\omega > 0]\,\hat V(\text{child})\big] = k_s \int g_s(\omega)\,V_{j-1}(\omega)\,d\omega.$$

The transmitted child of line L17 gives the term of $k_t$ in the same way. A sharp lobe returns the axis itself, and the integral is the value at that direction. Adding the local term and the two children gives $V_j$ by linearity of expectation.

At the first hit the numbers for the light and the lobe come from the patterns of line L2, not from fresh calls. The argument above uses only that each of them is uniform on the unit square and that they are independent of each other and of the numbers of the deeper nodes, which is shown next.

**Step 3, the samples of a pixel.** Line L2 draws each pattern as one uniform point in each of the $q^2$ cells and then puts it in a uniformly random order. The member at a fixed position $s$ is then in each cell with the probability $1/q^2$ and uniform within it, so it is uniform on the unit square; the same holds for the time slices on $[0, 1)$. The five patterns are drawn and shuffled with separate numbers, so the members at position $s$ are independent of each other, and the deeper nodes use numbers drawn after them. So sample $s$ has a uniform film point $x$ in the pixel, a uniform point $u$ of the lens disk by the same area argument as for the light, a uniform time $t$, and uniform first-hit numbers. By Step 2 the conditional expectation of TRACE given $x$, $u$ and $t$ is $V_D(\mathrm{ray}(x, u), t)$, and averaging over the uniform $x$, $u$ and $t$ gives $\bar V_{ij}$.

**Conclusion.** Each of the $q^2$ terms of line L6 has the expectation $\bar V_{ij}$, so their mean at line L7 has it too, by linearity. The samples of one pixel are not independent, since the cells of a pattern are shared out among them, but linearity of expectation does not need independence. $\blacksquare$
