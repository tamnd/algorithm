---
title: Objective perturbation of regularized ERM is epsilon-DP
proves: [correctness]
status: full
---

The data is $D = ((x_1, y_1), \ldots, (x_n, y_n))$ with $x_i \in \mathbb R^d$, $\|x_i\| \le 1$ and $y_i \in \{-1, +1\}$. The neighbor relation is replace: $D'$ differs from $D$ in one example, and $n$ is public. The loss $\ell : \mathbb R \to \mathbb R$ is convex and twice continuously differentiable with $|\ell'(z)| \le 1$ and $0 \le \ell''(z) \le c$ for all $z$. The logistic loss $\ell(z) = \ln(1 + e^{-z})$ has $\ell'(z) = -\sigma(-z)$ and $\ell''(z) = \sigma(z)\sigma(-z) \le 1/4$, where $\sigma(z) = 1/(1 + e^{-z})$, so $c = 1/4$. Let $\Lambda > 0$ and

$$J_D(f) = \frac1n \sum_{i=1}^n \ell(y_i f^{\mathsf T} x_i) + \frac{\Lambda}{2}\|f\|^2.$$

Lines L1 to L3 compute $\varepsilon'$ and $\Delta \ge 0$, line L4 draws $b$ with the density $\nu(b) = e^{-\beta\|b\|}/Z$ for $\beta = \varepsilon'/2$, and line L5 returns the minimizer of

$$J^{\mathrm{priv}}_D(f; b) = J_D(f) + \frac1n b^{\mathsf T} f + \frac{\Delta}{2}\|f\|^2.$$

**Lemma 1 (the noise determines the output, and back).** For every $b$, $J^{\mathrm{priv}}_D(\cdot\,; b)$ has a unique minimizer $f_D(b)$. Define

$$b_D(f) = -n\big(\nabla J_D(f) + \Delta f\big) = -\sum_{i=1}^n y_i\,\ell'(y_i f^{\mathsf T} x_i)\,x_i - n(\Lambda + \Delta) f.$$

Then $f = f_D(b)$ if and only if $b = b_D(f)$. So $b_D$ is a bijection of $\mathbb R^d$ with the inverse $f_D$.

*Proof.* $J^{\mathrm{priv}}_D(\cdot\,; b)$ is $(\Lambda + \Delta)$-strongly convex and differentiable, so it has exactly one minimizer, and it is the only point where the gradient $\nabla J_D(f) + b/n + \Delta f$ is zero. That gradient is zero exactly when $b = b_D(f)$. Every $b$ has the minimizer $f_D(b)$ with $b_D(f_D(b)) = b$, so $b_D$ is onto. If $b_D(f_1) = b_D(f_2) = b$, both points minimize the same function, so $f_1 = f_2$. $\square$

**Lemma 2 (the density of the output).** Let $A_D(f) = \sum_{i=1}^n \ell''(y_i f^{\mathsf T} x_i)\,x_i x_i^{\mathsf T} + n(\Lambda + \Delta) I$. The output $f_D(b)$ has the density

$$p_D(f) = \nu(b_D(f))\,\det A_D(f).$$

*Proof.* $b_D$ is continuously differentiable with the Jacobian matrix $-A_D(f)$, since $y_i^2 = 1$. $A_D(f)$ is symmetric and $A_D(f) \succeq n(\Lambda + \Delta) I \succ 0$, so the Jacobian is invertible everywhere. By Lemma 1 and the inverse function theorem, $b_D$ is a $C^1$ bijection with a $C^1$ inverse. The change of variables formula gives, for every event $S$,

$$\Pr[f_D(b) \in S] = \Pr[b \in b_D(S)] = \int_{b_D(S)} \nu(b)\,db = \int_S \nu(b_D(f))\,|\det(-A_D(f))|\,df,$$

and $|\det(-A_D(f))| = \det A_D(f)$ because $A_D(f)$ is positive definite. $\square$

**Lemma 3 (the noise moves little).** For replace neighbors and every $f$, $\|b_D(f) - b_{D'}(f)\| \le 2$.

*Proof.* Say $D'$ replaces $(x_n, y_n)$ by $(x', y')$. The sums for $D$ and $D'$ share all terms but one, and the term $n(\Lambda + \Delta) f$ is the same. So $b_D(f) - b_{D'}(f) = y'\ell'(y' f^{\mathsf T} x')\,x' - y_n\ell'(y_n f^{\mathsf T} x_n)\,x_n$. Each of the two vectors has norm at most $|\ell'| \cdot \|x\| \le 1$. $\square$

**Lemma 4 (the determinant moves little).** For replace neighbors and every $f$, $\det A_D(f) / \det A_{D'}(f) \le 1 + c/(n(\Lambda + \Delta))$.

*Proof.* Let $M = \sum_{i<n} \ell''(y_i f^{\mathsf T} x_i)\,x_i x_i^{\mathsf T} + n(\Lambda + \Delta) I$, so $M \succeq n(\Lambda + \Delta) I$. With $u = \sqrt{\ell''(y_n f^{\mathsf T} x_n)}\,x_n$ and $v = \sqrt{\ell''(y' f^{\mathsf T} x')}\,x'$, we have $A_D = M + uu^{\mathsf T}$ and $A_{D'} = M + vv^{\mathsf T}$. The matrix determinant lemma gives $\det(M + uu^{\mathsf T}) = \det M\,(1 + u^{\mathsf T}M^{-1}u)$, and the same for $v$. So

$$\frac{\det A_D(f)}{\det A_{D'}(f)} = \frac{1 + u^{\mathsf T}M^{-1}u}{1 + v^{\mathsf T}M^{-1}v} \le 1 + u^{\mathsf T}M^{-1}u \le 1 + \frac{\|u\|^2}{n(\Lambda + \Delta)} \le 1 + \frac{c}{n(\Lambda + \Delta)},$$

since $v^{\mathsf T}M^{-1}v \ge 0$, the largest eigenvalue of $M^{-1}$ is at most $1/(n(\Lambda + \Delta))$, and $\|u\|^2 = \ell''\,\|x_n\|^2 \le c$. $\square$

Chaudhuri, Monteleoni and Sarwate bound the same ratio by $(1 + c/(n(\Lambda + \Delta)))^2$ in the proof of their Theorem 9, with their Lemma 10 on the eigenvalues of a rank-two update. Lemma 4 is sharper by one factor. Algorithm 2 is set for the weaker bound, so it stays correct, and the proof below shows the slack.

**Theorem (privacy).** Lines L1 to L6 are $\varepsilon$-DP under replace.

*Proof.* By Lemma 2, for every $f$,

$$\frac{p_D(f)}{p_{D'}(f)} = \exp\big(\beta(\|b_{D'}(f)\| - \|b_D(f)\|)\big)\cdot\frac{\det A_D(f)}{\det A_{D'}(f)} \le e^{2\beta}\left(1 + \frac{c}{n(\Lambda + \Delta)}\right) = e^{\varepsilon'}\left(1 + \frac{c}{n(\Lambda + \Delta)}\right),$$

by the triangle inequality, Lemma 3 and Lemma 4. Note that $1 + 2c/(n\Lambda) + c^2/(n^2\Lambda^2) = (1 + c/(n\Lambda))^2$, so line L1 sets $\varepsilon' = \varepsilon - 2\ln(1 + c/(n\Lambda))$. There are two cases.

- *Line L2, $\varepsilon' > 0$ and $\Delta = 0$.* The bound is $\exp(\varepsilon - 2\ln(1 + c/(n\Lambda)) + \ln(1 + c/(n\Lambda))) \le e^{\varepsilon}$.
- *Line L3, $\varepsilon' \le 0$.* Then $(1 + c/(n\Lambda))^2 \ge e^{\varepsilon}$, so $c/(n\Lambda) \ge e^{\varepsilon/2} - 1 > e^{\varepsilon/4} - 1$, and $\Delta = c/(n(e^{\varepsilon/4} - 1)) - \Lambda > 0$. Now $\Lambda + \Delta = c/(n(e^{\varepsilon/4} - 1))$, so $1 + c/(n(\Lambda + \Delta)) = e^{\varepsilon/4}$. The new $\varepsilon' = \varepsilon/2$ gives the bound $e^{\varepsilon/2 + \varepsilon/4} \le e^{\varepsilon}$.

In both cases $p_D(f) \le e^{\varepsilon} p_{D'}(f)$ for every $f$, and integrating over an event $S$ gives $\Pr[\text{output} \in S \mid D] \le e^{\varepsilon}\Pr[\text{output} \in S \mid D']$. $\square$

**What the proof needs.** The proof uses the exact minimizer of line L5: it is a bijection of the noise, and its density has the closed form of Lemma 2. A solver that stops early returns a different random variable, and the theorem does not cover it. The code stops at a gradient norm of $10^{-11}$ and samples with floats, so it follows the analysis only up to these numerical effects. The proof also needs $\ell$ to be twice differentiable with a bounded $\ell''$, which rules out the hinge loss, and $\|x_i\| \le 1$. $\blacksquare$
