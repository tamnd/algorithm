---
title: The RTS backward pass gives the exact smoothing marginals of a linear Gaussian model
proves: [correctness]
status: full
---

We use the model and the pseudocode of the page: $x_0 \sim \mathcal N(m_0, P_0)$, $x_t = A x_{t-1} + q_t$ with $q_t \sim \mathcal N(0, Q)$, $y_t = H x_t + r_t$ with $r_t \sim \mathcal N(0, R)$, all noise terms independent. Assume that $Q$ is positive definite, so that each predicted covariance $P_{t+1|t} = A P_{t|t} A^\top + Q$ is positive definite and invertible, and that $R$ is positive definite, so that $S_t$ is invertible.

**Two facts about Gaussians.** (G1) If $(u, v)$ is jointly Gaussian with means $(a, b)$ and covariance blocks $\Sigma_{uu}, \Sigma_{uv}, \Sigma_{vv}$, and $\Sigma_{vv}$ is invertible, then $u \mid v \sim \mathcal N\bigl(a + \Sigma_{uv}\Sigma_{vv}^{-1}(v - b),\ \Sigma_{uu} - \Sigma_{uv}\Sigma_{vv}^{-1}\Sigma_{vu}\bigr)$. (G2) If $v \sim \mathcal N(\mu, \Sigma)$ and $u \mid v \sim \mathcal N(c + G v, \Lambda)$, then $u \sim \mathcal N(c + G\mu, \Lambda + G \Sigma G^\top)$. Both are standard; see Särkkä (2013), Appendix A.1, or Bishop (2006), Section 2.3.

**The forward pass.** Lines L1 to L5 are the Kalman filter. By induction on $t$, $x_t \mid y_{1:t} \sim \mathcal N(m_{t|t}, P_{t|t})$ and $x_{t+1} \mid y_{1:t} \sim \mathcal N(m_{t+1|t}, P_{t+1|t})$. The base case is the prior. The prediction of line L3 is (G2) with $u = x_t$, $v = x_{t-1}$, $G = A$. The update of line L5 is (G1) applied to the joint Gaussian of $(x_t, y_t)$ given $y_{1:t-1}$, whose blocks are $P_{t|t-1}$, $P_{t|t-1} H^\top$ and $S_t = H P_{t|t-1} H^\top + R$; then $K_t = P_{t|t-1} H^\top S_t^{-1}$ and the covariance is $P_{t|t-1} - K_t S_t K_t^\top$. The full treatment is on the [Kalman filter](/kalman-filter/) page.

**A conditional independence.** For $0 \le t < T$, the joint density factors as
$$p(x_{0:T}, y_{1:T}) = \underbrace{p(x_{0:t}, y_{1:t})}_{\text{past}} \; p(x_{t+1} \mid x_t) \; \underbrace{p(y_{t+1} \mid x_{t+1}) \prod_{s = t+2}^{T} p(x_s \mid x_{s-1})\, p(y_s \mid x_s)}_{\text{future, a function of } x_{t+1:T},\, y_{t+1:T}}.$$
Fix $x_{t+1}$ and $y_{1:T}$. As a function of $x_t$, the density is the past factor times $p(x_{t+1} \mid x_t)$, after the other variables are integrated out; the future factor does not depend on $x_t$ and cancels in the normalization. So
$$p(x_t \mid x_{t+1}, y_{1:T}) = p(x_t \mid x_{t+1}, y_{1:t}). \tag{1}$$

**Claim.** For $t = T, T-1, \ldots, 0$, $x_t \mid y_{1:T} \sim \mathcal N(m_{t|T}, P_{t|T})$ with the values of lines L6 to L10.

*Proof by backward induction.* For $t = T$ the smoothing and filtering distributions are the same, which is line L6.

Assume the claim for $t + 1$. Given $y_{1:t}$, the pair $(x_t, x_{t+1})$ is jointly Gaussian, because $x_{t+1} = A x_t + q_{t+1}$ with $q_{t+1}$ independent of $(x_t, y_{1:t})$. Its blocks are
$$\mathbb E = \begin{pmatrix} m_{t|t} \\ A m_{t|t} \end{pmatrix}, \qquad \mathrm{Cov} = \begin{pmatrix} P_{t|t} & P_{t|t} A^\top \\ A P_{t|t} & P_{t+1|t} \end{pmatrix},$$
and $A m_{t|t} = m_{t+1|t}$. By (G1), with $C_t = P_{t|t} A^\top P_{t+1|t}^{-1}$ as in line L8,
$$x_t \mid x_{t+1}, y_{1:t} \sim \mathcal N\bigl(m_{t|t} + C_t (x_{t+1} - m_{t+1|t}),\ P_{t|t} - C_t P_{t+1|t} C_t^\top\bigr).$$
Here $P_{t|t} A^\top P_{t+1|t}^{-1} A P_{t|t} = C_t P_{t+1|t} C_t^\top$ because $C_t P_{t+1|t} = P_{t|t} A^\top$ and $P_{t+1|t}$ is symmetric. By (1) this is also the law of $x_t$ given $x_{t+1}$ and $y_{1:T}$. By the induction hypothesis $x_{t+1} \mid y_{1:T} \sim \mathcal N(m_{t+1|T}, P_{t+1|T})$. Apply (G2) under the conditioning on $y_{1:T}$, with $G = C_t$:
$$m_{t|T} = m_{t|t} + C_t (m_{t+1|T} - m_{t+1|t}), \qquad P_{t|T} = P_{t|t} - C_t P_{t+1|t} C_t^\top + C_t P_{t+1|T} C_t^\top.$$
These are lines L9 and L10. $\square$

**Consequences.** (a) $P_{t|T} \preceq P_{t|t}$ in the order of positive semidefinite matrices, by backward induction from $P_{T|T} \preceq P_{T|T}$: if $P_{t+1|T} \preceq P_{t+1|t+1}$, then $P_{t+1|T} \preceq P_{t+1|t}$, since the filter update gives $P_{t+1|t+1} = P_{t+1|t} - K_{t+1} S_{t+1} K_{t+1}^\top \preceq P_{t+1|t}$; so $C_t (P_{t+1|T} - P_{t+1|t}) C_t^\top \preceq 0$, and line L10 gives $P_{t|T} \preceq P_{t|t}$. (b) The smoothed means and covariances do not depend on the observations through anything but $m_{t|t}$, $P_{t|t}$ and the next smoothed moments, which is why one forward and one backward sweep suffice.

**Cost.** The forward pass does, per step, a constant number of products of $n \times n$, $n \times m$ and $m \times m$ matrices and one $m \times m$ inverse: $O(n^3 + n^2 m + n m^2 + m^3)$. The backward pass does one $n \times n$ inverse and a constant number of $n \times n$ products per step: $O(n^3)$. The total over $T$ steps is $O(T(n^3 + n^2 m + n m^2 + m^3))$, and the stored moments take $O(T n^2)$ memory.
