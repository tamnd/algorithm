---
title: The Wirtinger gradient, the stationary points, and linear convergence under a regularity condition
proves: [correctness]
status: full
---

Vectors are in $\mathbb{C}^n$ with $\langle u, v \rangle = u^* v$. The data are $y_r = |a_r^* x|^2$ for $r = 1, \dots, m$. Write $p_r(z) = a_r^* z$ and $e_r(z) = |p_r(z)|^2 - y_r$. The loss and the step direction are

$$f(z) = \frac{1}{2m} \sum_{r=1}^m e_r(z)^2, \qquad g(z) = \frac1m \sum_{r=1}^m e_r(z)\, a_r\, p_r(z).$$

The algorithm takes $z_\tau = z_{\tau-1} - (\mu_\tau / \|z_0\|^2)\, g(z_{\tau-1})$ (line L6). The claim of correctness has four parts. The step direction is the steepest descent direction of $f$ (Lemma 1). The solutions are exactly the zeros of $f$, and they are stationary points (Lemma 2). A small step decreases $f$ (Lemma 3). Near the solutions, a regularity condition gives linear convergence to the set of solutions (Lemma 4). That the regularity condition holds with high probability for Gaussian vectors is the work of Candès, Li and Soltanolkotabi (2015), which is cited and not proved here.

The error is $\operatorname{dist}(z, x) = \min_\varphi \|z - e^{i\varphi} x\|$. The minimum is at $e^{i\varphi(z)} = c / |c|$ with $c = x^* z$ (or any $\varphi$ if $c = 0$), because $\|z - e^{i\varphi} x\|^2 = \|z\|^2 + \|x\|^2 - 2 \operatorname{Re}(e^{-i\varphi} c)$.

**Lemma 1 (the gradient).** For every $z$, every $d \in \mathbb{C}^n$ and real $t$,

$$\frac{d}{dt} f(z + t d) \Big|_{t = 0} = 2 \operatorname{Re} \langle g(z), d \rangle .$$

*Proof.* With $p = p_r(z)$ and $b = a_r^* d$, we have $|p + t b|^2 = |p|^2 + 2t \operatorname{Re}(\bar p b) + t^2 |b|^2$. So the derivative of $e_r(z + td)$ at $t = 0$ is $2 \operatorname{Re}(\bar p b)$, and the derivative of $f$ is

$$\frac{1}{2m} \sum_r 2 e_r \cdot 2 \operatorname{Re}(\overline{p_r}\, a_r^* d) = \frac{2}{m} \sum_r e_r \operatorname{Re}(\overline{p_r}\, a_r^* d).$$

On the other side, $g^* = \frac1m \sum_r e_r \overline{p_r}\, a_r^*$ because $e_r$ is real, so $\langle g, d \rangle = \frac1m \sum_r e_r \overline{p_r}\, a_r^* d$. Twice its real part is the same sum. $\square$

So if $\mathbb{C}^n$ is read as $\mathbb{R}^{2n}$ with the inner product $\operatorname{Re} \langle u, v \rangle$, the ordinary gradient of $f$ is $2g$. This $g$ is the Wirtinger derivative $\partial f / \partial \bar z$ (Candès, Li and Soltanolkotabi 2015, Section 6). Among the directions $d$ with $\|d\| = 1$, the derivative $2 \operatorname{Re}\langle g, d \rangle$ is smallest at $d = -g / \|g\|$ by the Cauchy-Schwarz inequality. So line L6 is gradient descent on $\mathbb{R}^{2n}$ with the step $\mu_\tau / (2\|z_0\|^2)$.

**Lemma 2 (solutions and stationary points).** $f(z) \ge 0$ for all $z$, and $f(z) = 0$ exactly when $|a_r^* z|^2 = y_r$ for all $r$. In particular $f(e^{i\varphi} x) = 0$ and $g(e^{i\varphi} x) = 0$ for all real $\varphi$. Also $f(e^{i\varphi} z) = f(z)$ and $g(e^{i\varphi} z) = e^{i\varphi} g(z)$. Finally $g(0) = 0$.

*Proof.* $f$ is a sum of squares, so $f \ge 0$ with equality exactly when every $e_r = 0$. For $z = e^{i\varphi} x$ each $e_r = |e^{i\varphi} a_r^* x|^2 - y_r = 0$, so $f = 0$ and every term of $g$ is $0$. Replacing $z$ by $e^{i\varphi} z$ does not change $e_r$ and multiplies $p_r$ by $e^{i\varphi}$, which gives the two identities. At $z = 0$ every $p_r = 0$. $\square$

So the method can only find $x$ up to a global phase, and the error must be measured by $\operatorname{dist}$. The point $z = 0$ is a stationary point with $f(0) = \frac{1}{2m} \sum_r y_r^2 > 0$ when $x \neq 0$, so a stationary point need not be a solution. This is one reason why the start matters.

**Lemma 3 (a small step decreases $f$).** If $g(z) \neq 0$, there is $t^* > 0$ such that $f(z - t g(z)) < f(z)$ for $0 < t < t^*$. If the second derivative of $\phi(t) = f(z - t g(z))$ is at most $L$ on $[0, s]$, then $f(z - s g(z)) \le f(z) - 2 s \|g(z)\|^2 + \frac12 L s^2$.

*Proof.* By Lemma 1 with $d = -g$, $\phi'(0) = -2\|g\|^2 < 0$. The function $\phi$ is a polynomial of degree at most $4$ in $t$, so it is smooth, and $\phi(t) < \phi(0)$ for all small $t > 0$. The second claim is Taylor's theorem with the remainder $\frac12 \phi''(\xi) s^2$ for some $\xi \in [0, s]$. $\square$

So with $L$ a bound for $\phi''$, every step $s < 4\|g\|^2 / L$ decreases $f$. The function $f$ is a quartic, so $L$ grows with $\|z\|$; a step that is too large can increase $f$, and a fixed step is safe only on a bounded region. This is why the schedule starts small.

**Lemma 4 (linear convergence under a regularity condition).** Let $\nabla f(z) = g(z)$, let $E = \{z : \operatorname{dist}(z, x) \le \varepsilon\}$, and let $\alpha, \beta > 0$ be such that for all $z \in E$

$$\operatorname{Re} \langle g(z), z - e^{i\varphi(z)} x \rangle \ge \frac1\alpha \operatorname{dist}^2(z, x) + \frac1\beta \|g(z)\|^2 . \tag{RC}$$

If $z \in E$ and $0 < \mu \le 2/\beta$, then $z^+ = z - \mu g(z)$ has $\operatorname{dist}^2(z^+, x) \le (1 - 2\mu/\alpha)\operatorname{dist}^2(z, x)$. So from any $z_0 \in E$ the iterates stay in $E$ and $\operatorname{dist}^2(z_\tau, x) \le (1 - 2\mu/\alpha)^\tau \operatorname{dist}^2(z_0, x)$.

*Proof.* Put $h = z - e^{i\varphi(z)} x$, so $\|h\| = \operatorname{dist}(z, x)$. Then

$$\|z^+ - e^{i\varphi(z)} x\|^2 = \|h - \mu g\|^2 = \|h\|^2 - 2\mu \operatorname{Re}\langle g, h \rangle + \mu^2 \|g\|^2 .$$

By (RC) this is at most $\|h\|^2 - \frac{2\mu}{\alpha}\|h\|^2 - \frac{2\mu}{\beta}\|g\|^2 + \mu^2\|g\|^2$. The last two terms add to $\mu (\mu - 2/\beta) \|g\|^2 \le 0$. The distance of $z^+$ is a minimum over all phases, so it is at most the norm on the left side. So $\operatorname{dist}^2(z^+, x) \le (1 - 2\mu/\alpha) \operatorname{dist}^2(z, x) \le \varepsilon^2$, and $z^+ \in E$. Induction on $\tau$ gives the rest. $\square$

The factor $1 - 2\mu/\alpha$ is not negative: (RC) and the Cauchy-Schwarz inequality give $\frac1\alpha \|h\|^2 + \frac1\beta \|g\|^2 \le \|g\| \|h\|$, and the inequality of arithmetic and geometric means gives $\frac1\alpha \|h\|^2 + \frac1\beta \|g\|^2 \ge \frac{2}{\sqrt{\alpha\beta}} \|g\| \|h\|$. So $\alpha \beta \ge 4$ when (RC) holds with $g \neq 0$, and $2\mu/\alpha \le 4/(\alpha\beta) \le 1$. Lemma 4 is Lemma 7.10 of Candès, Li and Soltanolkotabi (2015), and (RC) is their Condition 7.9.

**The cited theorem.** Candès, Li and Soltanolkotabi (2015, Theorem 3.3) take $a_r$ with independent entries $\mathcal{N}(0, 1/2) + i\,\mathcal{N}(0, 1/2)$ and $m \ge c_0\, n \log n$. With probability at least $1 - 10 e^{-\gamma n} - 8/n^2$ the spectral start has $\operatorname{dist}(z_0, x) \le \frac18 \|x\|$. For a constant $\mu_\tau = \mu \le c_1 / n$ there is an event of probability at least $1 - 13 e^{-\gamma n} - m e^{-1.5 m} - 8/n^2$ on which every $z_0$ with that bound gives

$$\operatorname{dist}(z_\tau, x) \le \frac18 \Bigl(1 - \frac\mu4\Bigr)^{\tau/2} \|x\| .$$

Here $c_0$, $c_1$ and $\gamma$ are numerical constants. Their proof shows that (RC) holds on $E$ with $\varepsilon = \frac18 \|x\|$ and suitable $\alpha$ and $\beta$, and then applies Lemma 4. The spectral start itself is treated on the page on [spectral initialization](/spectral-initialization/).

**What is not claimed.** The proof that (RC) holds with high probability for Gaussian vectors, and so the theorem above, is cited and not proved here. The theorem is for a constant step $\mu \le c_1 / n$. The schedule $\mu_\tau = \min(1 - e^{-\tau/\tau_0}, \mu_{\max})$ that the implementation uses is a tuned choice, and it has no proof. With $\mu_{\max} = 0.4$ and $n = 8$ the iterates can leave the solution again (see the example on the main page). The tests measure the recovery on fixed seeds with $\mu_{\max} = 0.3$ and do not check a theorem there.
