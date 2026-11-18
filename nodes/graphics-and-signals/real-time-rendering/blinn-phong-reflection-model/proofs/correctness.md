---
title: Properties of the Blinn-Phong model
proves: [correctness]
status: full
---

**Setting.** For unit vectors $n$, $l$ and $v$ with $n \cdot l > 0$ and $n \cdot v > 0$, the code computes $h = (l + v) / \lVert l + v \rVert$, the lobe $\max(0, n \cdot h)^s$, the normalized BRDF $f = k_d / \pi + k_s \frac{s + 8}{8\pi} (n \cdot h)^s$, the distribution $D = \frac{s + 2}{2\pi} (n \cdot h)^s$ and the Phong lobe $\max(0, r \cdot v)^p$ with $r = 2 (n \cdot l) n - l$. The claims are about these formulas in exact arithmetic. That the model looks plausible is a heuristic and is not claimed.

**Claim 1 (the half vector).** $h \cdot l = h \cdot v$, and $n \cdot h = 1$ exactly when $v = r$.

*Proof.* $h \cdot l = (1 + l \cdot v) / \lVert l + v \rVert = h \cdot v$. If $v = r$, then $l + v = 2 (n \cdot l) n$, a positive multiple of $n$, so $h = n$. Conversely, if $h = n$, then $l + v = c\, n$ for some $c > 0$, and $c = 2 (n \cdot l)$ because $n \cdot v = c - n \cdot l$ and $h \cdot l = h \cdot v$ give $n \cdot l = n \cdot v$; so $v = 2 (n \cdot l) n - l = r$. $\square$

**Claim 2 (reciprocity).** $f(l, v) = f(v, l)$ and $r(l) \cdot v = r(v) \cdot l$.

*Proof.* $h$ is symmetric in $l$ and $v$, and so is $f$. $r(l) \cdot v = 2 (n \cdot l)(n \cdot v) - l \cdot v$, which is symmetric. $\square$

**Claim 3 (normalization of $D$).** $\int_{H^2} D(h)\, (n \cdot h)\, d\omega_h = 1$ for every $s \ge 0$.

*Proof.* With $\mu = n \cdot h$ and $d\omega_h = d\mu\, d\phi$ after the change of variables, the integral is $2\pi \cdot \frac{s + 2}{2\pi} \int_0^1 \mu^{s + 1}\, d\mu = 1$. $\square$

**Claim 4 (the albedo at normal view).** For $v = n$, the specular albedo $A(s) = \int k\, (n \cdot h)^s (n \cdot l)\, d\omega_l$ with $k = (s + 8) / (8\pi)$ equals $(s + 8)\big(2 (1 - c_0^{s + 4}) / (s + 4) - (1 - c_0^{s + 2}) / (s + 2)\big)$ with $c_0 = 1 / \sqrt 2$. It is 1 at $s = 0$ and tends to 1 as $s \to \infty$.

*Proof.* Change variables from $l$ to $h$: $l = 2 (v \cdot h) h - v$ and $d\omega_l = 4 (v \cdot h)\, d\omega_h$. With $v = n$ and $\theta_h$ the angle of $h$, $v \cdot h = \cos\theta_h = c$ and $n \cdot l = 2c^2 - 1$, which is positive for $c > c_0$. So $A = 2\pi k \int_{c_0}^1 c^s (2c^2 - 1)\, 4c\, dc = (s + 8) \int_{c_0}^1 (2 c^{s + 3} - c^{s + 1})\, dc$, which is the closed form. At $s = 0$ it is $8 (2 \cdot \frac34 / 4 - \frac12 / 2) = 1$. As $s \to \infty$, the powers of $c_0$ vanish and $A \to \lim (s + 8)\, s / ((s + 4)(s + 2)) = 1$. $\square$

The largest value, $1.0752$ near $s = 8.76$, is found on a grid by the tests. The albedo at other view angles is computed by quadrature in $h$ and checked against the closed form at $v = n$.

**Claim 5 (the Phong match at normal view).** For $v = n$, $r \cdot v = \cos 2\theta_h$, and $\log \cos^p 2\theta - \log \cos^{4p} \theta = O(p \theta^4)$ as $\theta \to 0$.

*Proof.* For $v = n$, $r \cdot v = n \cdot l = 2 \cos^2\theta_h - 1 = \cos 2\theta_h$. With $\log \cos x = -x^2 / 2 - x^4 / 12 + O(x^6)$, $p \log\cos 2\theta = -2 p \theta^2 - \frac{4}{3} p \theta^4 + O(p \theta^6)$ and $4 p \log\cos\theta = -2 p \theta^2 - \frac13 p \theta^4 + O(p \theta^6)$. The $\theta^2$ terms are equal. $\square$

**What the tests check.** Claim 1 and Claim 2 at random directions, Claim 3 by the midpoint rule for $s$ up to 1000, Claim 4 against quadrature, Claim 5 at small angles, the lobe shape at 75°, and the classic form at a mirror configuration.
