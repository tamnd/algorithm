---
title: Criminisi inpainting stops, keeps the known pixels, copies only source values, and fills in best-first order
proves: [correctness]
status: full
---

Let the image have $W \times H$ pixels, let $\Omega$ be the target region and $\Phi$ the other pixels, and let $r \ge 0$ be the patch radius, with $a = (2r+1)^2$. Assume $\Phi$ contains at least one source patch, a full square of side $2r + 1$ inside the image with no pixel of $\Omega$. The claims are about the procedure of lines L1 to L12; they say nothing about the visual quality of the result.

**Claim 1 (the front exists).** At the start of any pass of the loop, if some pixel is unfilled, then the front $\delta\Omega$ of line L4 is not empty.

*Proof.* Filled pixels are never unmarked, and the pixels of a source patch are filled at the start, so a filled pixel exists. The pixel grid with 4-neighbor edges is connected. Take a path from a filled pixel to an unfilled one; the first unfilled pixel on it has a filled 4-neighbor, the pixel before it on the path. $\square$

**Claim 2 (termination).** Each pass fills at least one pixel and at most $a$ pixels, so the loop stops after at most $|\Omega|$ passes, with every pixel filled.

*Proof.* The pixel $\hat p$ of line L7 is in $\delta\Omega$, so it is unfilled, and the offset $u = 0$ puts it in the loop of line L9; line L10 marks it filled. The loop of line L9 has at most $a$ offsets. The number of unfilled pixels falls by at least one per pass, and by Claim 1 the loop stops only when it is zero. $\square$

**Claim 3 (known pixels are kept).** For every $p \in \Phi$, the output value at $p$ is $I(p)$.

*Proof.* Line L10 writes only at offsets where $\hat p + u$ is unfilled. A pixel of $\Phi$ is filled at line L1 and stays filled, so it is never written. $\square$

**Claim 4 (copied values come from the source).** For every $p \in \Omega$, the output value at $p$ is $I(s)$ for some $s \in \Phi$.

*Proof.* Line L10 reads $I(\hat q + u)$, where $\hat q$ is a source center and $|u_x|, |u_y| \le r$, so $\hat q + u$ is a pixel of the source patch at $\hat q$, which lies in $\Phi$. By Claim 3 the value there is still the input value. Each pixel of $\Omega$ is written once, at the pass that fills it, and keeps that value. $\square$

**Claim 5 (best-first order).** At each pass, $P(\hat p) \ge P(p)$ for every $p \in \delta\Omega$, and $d(\hat p, \hat q) \le d(\hat p, q)$ for every source center $q$.

*Proof.* Lines L7 and L8 take a maximum and a minimum over finite sets that are not empty (Claim 1 and the assumption on $\Phi$). The tie rules choose one element of the set of maximizers and of minimizers. $\square$

**Claim 6 (confidence).** Every confidence stays in $[0, 1]$, and every confidence set at line L11 is at most $(a - 1)/a$.

*Proof.* By induction on the passes. At the start the values are 0 and 1. At line L6, $C(p)$ is a sum of at most $|\Psi_p|$ values in $[0, 1]$, divided by $|\Psi_p|$, so it is in $[0, 1]$. The center $p$ is unfilled and adds nothing, so the sum has at most $|\Psi_p| - 1$ terms and $C(p) \le 1 - 1/|\Psi_p|$; with $|\Psi_p| \le a$ this is at most $1 - 1/a$. Line L11 copies $C(\hat p)$. $\square$

**Claim 7 (exact fill of stripes).** Let the full image be $I^\ast(x, y) = g(x \bmod k)$ for a period $k \ge 1$ and values $g(0), \ldots, g(k - 1)$ that are all different, let $I = I^\ast$ on $\Phi$, let $r \ge 1$, and assume that for every residue $j$ there is a source center $q$ with $q_x \equiv j \pmod k$. Then the output equals $I^\ast$.

*Proof.* By induction on the passes, every filled pixel holds its value of $I^\ast$; this holds at the start. At a pass, $\hat p$ has a filled 4-neighbor, which lies in $\Psi_{\hat p}$ because $r \ge 1$. Take a source center $q$ with $q_x \equiv \hat p_x \pmod k$. For each filled $\hat p + u$, the values $I(\hat p + u) = g((\hat p_x + u_x) \bmod k)$ and $I(q + u) = g((q_x + u_x) \bmod k)$ are equal, so $d(\hat p, q) = 0$, and by Claim 5 $d(\hat p, \hat q) = 0$. Then at the filled neighbor $\hat p + u$, $g((\hat q_x + u_x) \bmod k) = g((\hat p_x + u_x) \bmod k)$, and since the values of $g$ are different, $\hat q_x \equiv \hat p_x \pmod k$. So every copied value $I(\hat q + u) = g((\hat p_x + u_x) \bmod k) = I^\ast(\hat p + u)$. $\square$

**Not a global optimum.** The procedure does not minimize a total cost over the hole. A pixel filled at one pass is never revised, and both choices of a pass depend on the values copied before. A different order can give a different output, and on structured images the output can differ from the true image, as in the diagonal edge example on the page.

**Cost.** Line L3 checks $a$ pixels for each of at most $WH$ centers. One pass scans the image for the front in $\Theta(WH)$ time, computes each priority in $O(a)$ time, and each distance in $O(a)$ time. With at most $WH$ front pixels and source patches, a pass takes $O(WHa)$, and by Claim 2 there are at most $|\Omega|$ passes, for $O(|\Omega| WHa)$ in total. The flags, the confidences, the copy of the image and the list of sources take $\Theta(WH)$ space.
