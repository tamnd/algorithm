---
title: The four-point scheme interpolates, reproduces cubics for w = 1/16, and converges to a continuous curve for |w| < 1/4
proves: [correctness, convergence]
status: full
---

We use the pseudocode of the page for a closed polygon $P_0, \dots, P_{m-1}$, indices modulo $m$, and a real tension $w$. Write $P^{(k)}_i$ for the polygon after $k$ rounds, so $P^{(0)} = P$ and

$$P^{(k+1)}_{2i} = P^{(k)}_i, \qquad P^{(k+1)}_{2i+1} = \big(\tfrac12 + w\big)\big(P^{(k)}_i + P^{(k)}_{i+1}\big) - w \big(P^{(k)}_{i-1} + P^{(k)}_{i+2}\big).$$

We attach $P^{(k)}_i$ to the parameter $t = i / 2^k$, and write $f_k$ for the polygon through these points, linear between consecutive parameters.

**Lemma 1 (interpolation).** For all $j \le k$ and all $i$, $P^{(k)}_{2^{k-j} i} = P^{(j)}_i$. So every point that a round computes stays in all later polygons, at the same parameter.

*Proof.* Line L3 copies $P^{(k)}_i$ to index $2i$ of the next polygon, which is the same parameter $2i / 2^{k+1} = i / 2^k$. Induction on $k - j$ gives the claim. $\square$

**Lemma 2 (linear data).** If $P^{(0)}_i = a + b\, i$ for vectors $a, b$, then $P^{(k)}_i = a + b\, i / 2^k$ for all $k$, for every $w$.

*Proof.* The weights of line L4 are $\tfrac12 + w, \tfrac12 + w, -w, -w$, which sum to 1, and they are symmetric about the midpoint of the edge. So the rule maps the values of a linear function at $i - 1, i, i + 1, i + 2$ to its value at $i + \tfrac12$. $\square$

**Lemma 3 (cubic data).** Let $w = \tfrac1{16}$. If $P^{(0)}_i = g(i)$ for a polynomial $g$ of degree at most 3, then $P^{(k)}_i = g(i / 2^k)$ for all $k$. For $w \ne \tfrac1{16}$ this fails already for $g(t) = t^2$.

*Proof.* The Lagrange polynomials for the nodes $-1, 0, 1, 2$ at $t = \tfrac12$ are

$$\ell_{-1} = \frac{(\frac12)(-\frac12)(-\frac32)}{(-1)(-2)(-3)} = -\tfrac1{16}, \qquad \ell_0 = \frac{(\frac32)(-\frac12)(-\frac32)}{(1)(-1)(-2)} = \tfrac9{16},$$

and by symmetry $\ell_1 = \tfrac9{16}$ and $\ell_2 = -\tfrac1{16}$. For $w = \tfrac1{16}$ these are the weights of line L4. So the new point is the value at $i + \tfrac12$ of the cubic through the four old points, and for data from a cubic $g$ it is $g$ at that parameter. By the scaling $t \mapsto 2t$, the same holds in each round, which with Lemma 1 gives the claim. For $g(t) = t^2$ and the nodes $-1, 0, 1, 2$, the rule gives $\big(\tfrac12 + w\big)(0 + 1) - w(1 + 4) = \tfrac12 - 4w$, and this equals $g(\tfrac12) = \tfrac14$ only when $w = \tfrac1{16}$. $\square$

**Lemma 4 (differences).** Let $d^{(k)}_i = P^{(k)}_{i+1} - P^{(k)}_i$ and $\delta_k = \max_i |d^{(k)}_i|$. Then

$$d^{(k+1)}_{2i} = \tfrac12 d^{(k)}_i + w \big(d^{(k)}_{i-1} - d^{(k)}_{i+1}\big), \qquad d^{(k+1)}_{2i+1} = \tfrac12 d^{(k)}_i - w \big(d^{(k)}_{i-1} - d^{(k)}_{i+1}\big),$$

so $\delta_{k+1} \le \mu\, \delta_k$ with $\mu = \tfrac12 + 2|w|$.

*Proof.* Drop the index $(k)$. The first difference is the new point minus $P_i$:

$$\big(\tfrac12 + w\big)(P_i + P_{i+1}) - w(P_{i-1} + P_{i+2}) - P_i = \tfrac12 (P_{i+1} - P_i) + w (P_i - P_{i-1}) - w (P_{i+2} - P_{i+1}),$$

which is the formula. The second is $P_{i+1}$ minus the new point, and the two sum to $d_i$. The bound follows from the triangle inequality. $\square$

**Theorem.** If $|w| < \tfrac14$, the polygons $f_k$ converge uniformly to a continuous closed curve $f$, and $f(i / 2^k) = P^{(k)}_i$ for all $k$ and $i$. In particular $f$ passes through every input point. The error after $k$ rounds is $|f - f_k| \le \frac{2 |w|\, \delta_0\, \mu^k}{1 - \mu}$.

*Proof.* Here $\mu < 1$. On the parameter interval of the edge from $P^{(k)}_i$ to $P^{(k)}_{i+1}$, the polygon $f_{k+1}$ differs from $f_k$ by a piecewise linear function that is 0 at the ends and equal at the midpoint to

$$P^{(k+1)}_{2i+1} - \tfrac12 \big(P^{(k)}_i + P^{(k)}_{i+1}\big) = w \big(d^{(k)}_{i-1} - d^{(k)}_{i+1}\big).$$

So $|f_{k+1} - f_k| \le 2 |w| \delta_k \le 2|w| \mu^k \delta_0$ everywhere. The sum of these bounds over $k$ is finite, so $(f_k)$ is a Cauchy sequence in the uniform norm. Its limit $f$ is continuous, as a uniform limit of continuous functions, and the sum of the remaining terms gives the error bound. By Lemma 1, $f_j(i / 2^k) = P^{(k)}_i$ for all $j \ge k$, so $f(i / 2^k) = P^{(k)}_i$. $\blacksquare$

**Smoothness.** The theorem shows continuity only. That the limit is $C^1$ for $0 < w < \tfrac18$ was proved by Dyn, Levin and Gregory in 1987, the range was extended to $0 < w < (\sqrt5 - 1)/8$ by Dyn, Gregory and Levin in 1991, and Hechler, Mößner and Reif showed in 2009 that the exact range is $0 < w < \omega^*$, where $\omega^* \approx 0.19273$ is the real root of $32 \omega^3 + 4 \omega - 1 = 0$. These proofs study the scheme for the divided differences $2^k d^{(k)}_i$, which by Lemma 4 is $e_{2i} = e_i + 2w(e_{i-1} - e_{i+1})$, $e_{2i+1} = e_i - 2w(e_{i-1} - e_{i+1})$, and need more than one round to show that its differences contract. We do not repeat them here.
