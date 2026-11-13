---
title: Richardson-Lucy iterates stay nonnegative, keep the total flux and never lower the Poisson likelihood
proves: [correctness]
status: full
---

Number the pixels, and write the circular blur as a matrix: $A_{xy} = p(x - y)$, with the difference taken modulo the image size. Then $A_{xy} \ge 0$, and every column sums to 1, because $\sum_x A_{xy} = \sum_t p(t) = 1$. For $u \ge 0$ put $b = Au$. One step of lines L3 to L6 is

$$u^{+}_y = u_y \sum_x A_{xy}\, r_x, \qquad r_x = \begin{cases} d_x / b_x & d_x > 0, \\ 0 & d_x = 0. \end{cases}$$

The column-sum property is used only in Claim 4. Call $u$ admissible if $u \ge 0$ and $b_x > 0$ for every $x$ with $d_x > 0$.

**Claim 1 (well defined).** If $u_0 > 0$ at every pixel, then $u_0$ is admissible, and if $u$ is admissible then so is $u^{+}$. So line L4 never divides by zero.

*Proof.* For $u_0 > 0$, $b_x = \sum_y A_{xy} u_y > 0$ because row $x$ of $A$ sums to $\sum_t p(t) = 1$ under the periodic border, so it has a positive entry. Now let $u$ be admissible and $d_x > 0$. Since $b_x > 0$, there is a $y$ with $A_{xy} > 0$ and $u_y > 0$. For that $y$, $u^{+}_y \ge u_y A_{xy} d_x / b_x > 0$, and so $b^{+}_x \ge A_{xy} u^{+}_y > 0$. $u^{+} \ge 0$ is Claim 2. $\square$

**Claim 2 (nonnegativity).** If $u$ is admissible, then $u^{+} \ge 0$.

*Proof.* $u_y \ge 0$, $A_{xy} \ge 0$ and $r_x \ge 0$, because $d_x \ge 0$ and $b_x > 0$ where $d_x > 0$. $\square$

**Claim 3 (flux).** If $u$ is admissible, then $\sum_y u^{+}_y = \sum_x d_x$, for any nonnegative $A$.

*Proof.* Exchange the sums:

$$\sum_y u^{+}_y = \sum_x r_x \sum_y A_{xy} u_y = \sum_x r_x b_x = \sum_{x : d_x > 0} \frac{d_x}{b_x} b_x = \sum_x d_x. \qquad \square$$

The identity is exact, so it holds in rational arithmetic with no rounding. For a matrix whose column sums $s_y$ are not all 1, such as a blur with a zero border, the EM update is $u^{+}_y = (u_y / s_y)\sum_x A_{xy} r_x$, and the same computation gives $\sum_y s_y u^{+}_y = \sum_x (Au^{+})_x = \sum_x d_x$ instead: the predicted image keeps the flux, not the estimate.

**Claim 4 (the likelihood does not decrease).** Let $L(v) = \sum_x (d_x \log (Av)_x - (Av)_x)$ for $v \ge 0$, with $0 \log 0 = 0$ and $\log 0 = -\infty$. If $u$ is admissible, then $L(u^{+}) \ge L(u)$.

*Proof.* Since every column of $A$ sums to 1, $\sum_x (Av)_x = \sum_y v_y$. Let $X = \{x : d_x > 0\}$, so $b_x > 0$ for $x \in X$. For $x \in X$ define the weights $w_{xy} = A_{xy} u_y / b_x$ on the set $S_x = \{y : A_{xy} u_y > 0\}$. They are positive and sum to 1 over $S_x$.

Lower bound. Fix $v \ge 0$ and $x \in X$. Since $(Av)_x \ge \sum_{y \in S_x} A_{xy} v_y$ and the logarithm is increasing and concave, [Jensen's inequality](/jensens-inequality/) gives

$$\log (Av)_x \ge \log \sum_{y \in S_x} w_{xy} \frac{A_{xy} v_y}{w_{xy}} \ge \sum_{y \in S_x} w_{xy} \log \frac{A_{xy} v_y}{w_{xy}},$$

where a term with $v_y = 0$ is $-\infty$. Multiply by $d_x > 0$ and sum over $x \in X$. With

$$Q(v) = \sum_{x \in X} d_x \sum_{y \in S_x} w_{xy} \log \frac{A_{xy} v_y}{w_{xy}} - \sum_y v_y,$$

this gives $L(v) \ge Q(v)$ for every $v \ge 0$.

Touching at $u$. For $v = u$ and $y \in S_x$, $A_{xy} u_y / w_{xy} = b_x$, so the inner sum is $\log b_x$, and $Q(u) = \sum_{x \in X} d_x \log b_x - \sum_y u_y = L(u)$.

Maximizing $Q$. Collect the terms of each $v_y$. With $c_y = \sum_{x \in X,\, y \in S_x} d_x w_{xy}$,

$$Q(v) = \sum_y \big(c_y \log v_y - v_y\big) + \text{const},$$

where the constant does not depend on $v$, and a term with $c_y = 0$ is just $-v_y$. If $c_y > 0$, then $t \mapsto c_y \log t - t$ is strictly concave on $t > 0$ with its maximum at $t = c_y$; if $c_y = 0$, the maximum over $t \ge 0$ is at $t = 0 = c_y$. So $Q$ is largest at $v_y = c_y$. Now

$$c_y = \sum_{x \in X,\, A_{xy} u_y > 0} d_x \frac{A_{xy} u_y}{b_x} = u_y \sum_x A_{xy} r_x = u^{+}_y,$$

because the terms with $A_{xy} u_y = 0$ and those with $d_x = 0$ add zero. So $u^{+}$ maximizes $Q$, and

$$L(u^{+}) \ge Q(u^{+}) \ge Q(u) = L(u). \qquad \square$$

This is the EM algorithm: the complete data are the counts $z_{xy}$ of photons that leave source pixel $y$ and reach detector pixel $x$, independent Poisson with mean $A_{xy} u_y$, so that $d_x = \sum_y z_{xy}$. The E step computes $\mathbb{E}[z_{xy} \mid d] = d_x w_{xy}$, and the M step sets $u_y$ to the expected number of photons from $y$, divided by the probability $s_y = 1$ that a photon from $y$ is detected.

**Claim 5 (fixed points).** If $d = Au^\ast$ for some $u^\ast \ge 0$, then $u^\ast$ is a fixed point.

*Proof.* Take $y$ with $u^\ast_y > 0$. Every $x$ with $A_{xy} > 0$ has $d_x \ge A_{xy} u^\ast_y > 0$, so $r_x = d_x / b_x = 1$, and $u^{+}_y = u^\ast_y \sum_x A_{xy} = u^\ast_y$. If $u^\ast_y = 0$, then $u^{+}_y = 0$. $\square$

The same computation shows that a pixel with $u_y = 0$ has $u^{+}_y = 0$, so zeros of the start stay zeros.

**What is not claimed.** Claim 4 gives a monotone sequence $L(u_k)$, bounded above by $\sum_x (d_x \log d_x - d_x)$, so the values converge. The convergence of the iterates themselves to a maximizer of the concave function $L$ needs a further argument, given for this model by Vardi, Shepp and Kaufman (1985). No bound on the number of steps follows, and the maximizer for noisy data is a poor image, which is why the method is stopped early.

**Cost.** Lines L3 and L5 each sum $K$ products per pixel, and lines L4 and L6 do one operation per pixel, so one iteration is $\Theta(WHK)$ and uses $\Theta(WH)$ extra space for $b$, $r$ and $c$.
