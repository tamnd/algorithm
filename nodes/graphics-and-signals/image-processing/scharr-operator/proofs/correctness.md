---
title: The Scharr passes compute the Scharr masks, and the direction error formula
proves: [correctness]
status: full
---

We write $c_W(x) = \min(\max(x, 0), W - 1)$ and $c_H(y) = \min(\max(y, 0), H - 1)$ for the clamp rule. Let $w = (w_{-1}, w_0, w_1) = (3, 10, 3)$ and $e = (-1, 0, 1)$. Then $S_x[v][u] = w_v e_u$ and $S_y[v][u] = e_v w_u$.

**Lemma 1 (separable form).** For every pixel $(x, y)$, line L3 gives $g_x(x, y) = \sum_{u, v} S_x[v][u]\, I(c_W(x + u), c_H(y + v))$, and line L4 gives the same sum with $S_y$.

*Proof.* Line L1 gives $s(x', y) = \sum_v w_v I(x', c_H(y + v))$ for each column $x'$. Line L3 reads $s$ at the columns $c_W(x \pm 1)$, which are inside the image, so $g_x(x, y) = \sum_{u = \pm 1} e_u \sum_v w_v I(c_W(x + u), c_H(y + v))$. The term $u = 0$ would be 0 because $e_0 = 0$. The clamp rule acts on each coordinate on its own, so this is the direct sum. The proof for $g_y$ changes the axes. $\square$

**Theorem 2 (exact on affine images).** If $I(x, y) = a x + b y + k$ and $1 \le x \le W - 2$, $1 \le y \le H - 2$, then $g_x(x, y) = 32a$ and $g_y(x, y) = 32b$.

*Proof.* No read is clamped. With $\sum_u e_u = 0$, $\sum_u u\, e_u = 2$ and $\sum_v w_v = 16$, Lemma 1 gives $g_x = a \cdot 2 \cdot 16 = 32a$, because every other term holds the factor $\sum_u e_u = 0$. The same sums give $g_y = 32b$. $\square$

For the direction error we take any smoothing weights $w = (\alpha, \beta, \alpha)$ with $\alpha \ge 0$ and $\beta > 2\alpha$, and we set $\gamma = \alpha / (\beta + 2\alpha)$. Prewitt has $\gamma = \tfrac{1}{3}$, Sobel has $\gamma = \tfrac{1}{4}$ and Scharr has $\gamma = \tfrac{3}{16}$. (Prewitt and Sobel have $\beta \le 2\alpha$, but the proof below uses $\beta > 2\alpha$ only to keep a factor positive for all frequencies, and for small $|\omega|$ that factor is positive for them too.)

**Lemma 3 (plane wave response).** Let $I(x, y) = \cos(\omega_x x + \omega_y y + \varphi_0)$ on the whole grid, and write $\varphi = \omega_x x + \omega_y y + \varphi_0$. Then

$$g_x = -2 \sin \omega_x\, (\beta + 2\alpha \cos \omega_y) \sin \varphi, \qquad g_y = -2 \sin \omega_y\, (\beta + 2\alpha \cos \omega_x) \sin \varphi.$$

*Proof.* The correlation with $w_v e_u$ factors. Along $x$, $\cos(\varphi + \omega_x) - \cos(\varphi - \omega_x) = -2 \sin \omega_x \sin \varphi$. Along $y$, a function $f(\varphi)$ of the phase becomes $\alpha f(\varphi - \omega_y) + \beta f(\varphi) + \alpha f(\varphi + \omega_y)$, and for $f = \sin$ this is $(\beta + 2 \alpha \cos \omega_y) \sin \varphi$. Apply the two steps one after the other. The formula for $g_y$ follows by the change of axes. $\square$

So where $\sin \varphi \ne 0$, the vector $(g_x, g_y)$ is parallel to $(\sin \omega_x (\beta + 2\alpha \cos \omega_y),\ \sin \omega_y (\beta + 2\alpha \cos \omega_x))$, which does not depend on the pixel. The true gradient of $I$ is parallel to $(\omega_x, \omega_y)$. Write $\omega_x = r \cos \theta$ and $\omega_y = r \sin \theta$ with $0 < r < \pi$ and $0 \le \theta \le \pi/2$, and let $\hat\theta$ be the angle of the estimate.

**Theorem 4 (direction error).** Uniformly in $\theta$,

$$\hat\theta = \theta + \left( \frac{1}{6} - \gamma \right) \frac{r^2}{4} \sin 4\theta + O(r^4).$$

*Proof.* If $\theta = 0$ then $\omega_y = 0$, so $g_y = 0$ and $\hat\theta = 0$. If $\theta = \pi/2$, then $\hat\theta = \pi/2$ in the same way. Both agree with the formula. For $0 < \theta < \pi/2$, both components of the estimate are positive for small $r$, and

$$\tan \hat\theta = \frac{\sin \omega_y}{\sin \omega_x} \cdot \frac{\beta + 2\alpha \cos \omega_x}{\beta + 2\alpha \cos \omega_y}.$$

We have $\sin \omega = \omega (1 - \omega^2 / 6 + O(\omega^4))$ and $\beta + 2\alpha \cos \omega = (\beta + 2\alpha)(1 - \gamma \omega^2 + O(\omega^4))$. So

$$\tan \hat\theta = \frac{\omega_y}{\omega_x} \cdot \frac{(1 - \omega_y^2 / 6)(1 - \gamma \omega_x^2)}{(1 - \omega_x^2 / 6)(1 - \gamma \omega_y^2)} (1 + O(r^4)) = \tan \theta \left( 1 + \left( \frac{1}{6} - \gamma \right)(\omega_x^2 - \omega_y^2) + O(r^4) \right).$$

Here $\omega_x^2 - \omega_y^2 = r^2 \cos 2\theta$. Let $\delta = \hat\theta - \theta$. The function $\arctan$ has a bounded derivative, so $\delta = O(r^2)$. Now write $\hat\theta = \arctan(\tan \theta\, (1 + \epsilon))$ with $\epsilon = (\tfrac{1}{6} - \gamma) r^2 \cos 2\theta + O(r^4)$. The derivative of $\arctan(\tan \theta\, (1 + \epsilon))$ with respect to $\epsilon$ at $\epsilon = 0$ is $\tan \theta / (1 + \tan^2 \theta) = \sin \theta \cos \theta$, and the second derivative is bounded for all $\theta$. So

$$\delta = \sin \theta \cos \theta \cdot \left( \frac{1}{6} - \gamma \right) r^2 \cos 2\theta + O(r^4) = \left( \frac{1}{6} - \gamma \right) \frac{r^2}{4} \sin 4\theta + O(r^4),$$

because $\sin \theta \cos \theta \cos 2\theta = \tfrac{1}{2} \sin 2\theta \cos 2\theta = \tfrac{1}{4} \sin 4\theta$. $\blacksquare$

**Consequences.** The largest leading error over all $\theta$ is $|\tfrac{1}{6} - \gamma|\, r^2 / 4$. The factor $|\tfrac{1}{6} - \gamma|$ is $\tfrac{1}{6}$ for Prewitt, $\tfrac{1}{12}$ for Sobel and $\tfrac{1}{48}$ for Scharr, so at small $r$ the Scharr error is 4 times smaller than the Sobel error. At $r = \pi/8$ the leading term gives 0.37, 0.18 and 0.046 degrees, which match the exact maxima 0.373, 0.185 and 0.045 degrees found from the formula of Lemma 3. The weights $(1, 4, 1)$ give $\gamma = \tfrac{1}{6}$, so the leading term is 0 and their error is $O(r^4)$. Scharr's weights do not cancel the leading term, but they keep the error small over a wider band of frequencies, which is the aim of an optimization over a band.
