---
title: Active constellation extension keeps every decision and every distance margin, keeps the symbol band-limited, and never increases the clipped energy for step sizes up to 2
proves: [correctness]
status: full
---

Let $\mathcal{C}$ be a square QAM constellation with unit mean energy: its points are $u + jw$ with $u$ and $w$ in a PAM set $\{\pm a_1, \ldots, \pm a_{S/2}\}$, where $0 < a_1 < \cdots < a_{S/2}$ are equally spaced with step $2a_1$. Write $a_{\max} = a_{S/2}$ for the outer level. Let $X \in \mathcal{C}^N$ be the data, $L$ the oversampling factor, $A > 0$ the clipping magnitude and $\mu > 0$ the step size. Write $T$ for the map of lines L2 and L8 from $N$ subcarrier values to the oversampled symbol, $T(Y) = \sqrt L\, F_{LN}^H Z(Y)$, where $Z(Y)$ puts $(L - 1)N$ zeros in the middle of $Y$. Let $B$ be the map of line L6 that keeps the $N$ in-band values of $F_{LN}\, e$ and divides them by $\sqrt L$. We work in exact arithmetic.

**Lemma 1 (the transforms).** $B(T(Y)) = Y$ for every $Y$, and $T^H = L\, B$, so $\lVert T(Y) \rVert^2 = L \lVert Y \rVert^2$.

*Proof.* $F_{LN}$ is unitary, so $F_{LN}\, T(Y) = \sqrt L\, Z(Y)$, whose in-band values are $\sqrt L\, Y$; dividing by $\sqrt L$ gives $Y$. The adjoint of $T$ is $\sqrt L\, Z^H F_{LN}$, and $Z^H$ keeps the in-band values, so $T^H = \sqrt L \cdot \sqrt L\, B = L B$. Then $\lVert T(Y) \rVert^2 = \langle Y, T^H T Y \rangle = L \langle Y, B T Y \rangle = L \lVert Y \rVert^2$. $\square$

**The extension region.** For one coordinate $u_0 \in \{\pm a_i\}$ of a constellation point, let $I(u_0) = \{u_0\}$ if $|u_0| < a_{\max}$, $I(u_0) = [a_{\max}, \infty)$ if $u_0 = a_{\max}$, and $I(u_0) = (-\infty, -a_{\max}]$ if $u_0 = -a_{\max}$. For a point $x_0 = u_0 + j w_0$, the extension region is $E(x_0) = \{u + jw : u \in I(u_0),\ w \in I(w_0)\}$.

**Lemma 2 (the projection).** $E(x_0)$ is a closed [convex set](/convex-set/), and the function `project` of line L7 returns its nearest point to any $z$.

*Proof.* Each $I(u_0)$ is a point or a closed half-line, so it is closed and convex, and so is the product $E(x_0)$. The squared distance $|z - (u + jw)|^2 = (\mathrm{Re}\, z - u)^2 + (\mathrm{Im}\, z - w)^2$ is a sum of a term in $u$ and a term in $w$, so the nearest point minimizes each term over its own set. The nearest point of $\{u_0\}$ is $u_0$, and the nearest point of $[a_{\max}, \infty)$ to $t$ is $\max(t, a_{\max})$, and similarly for the negative half-line. These are the three cases of `project`. $\square$

**Lemma 3 (margins grow).** Let $y \in E(x_0)$. Then for every point $q \in \mathcal{C}$, $|\mathrm{Re}(y - q)| \ge |\mathrm{Re}(x_0 - q)|$ and $|\mathrm{Im}(y - q)| \ge |\mathrm{Im}(x_0 - q)|$, so $|y - q| \ge |x_0 - q|$. Also, for every $q \ne x_0$, $|y - x_0| < |y - q|$, so a minimum-distance detector maps the noiseless $y$ to $x_0$, and the distance from $y$ to each boundary of the decision region of $x_0$ is at least that of $x_0$.

*Proof.* Take the real parts; the imaginary parts are the same. If $|u_0| < a_{\max}$, then $\mathrm{Re}\, y = u_0$ and nothing changes. If $u_0 = a_{\max}$, then $\mathrm{Re}\, y \ge a_{\max} \ge \mathrm{Re}\, q$ for every $q$, so $|\mathrm{Re}(y - q)| = \mathrm{Re}\, y - \mathrm{Re}\, q \ge a_{\max} - \mathrm{Re}\, q = |\mathrm{Re}(x_0 - q)|$. The case $u_0 = -a_{\max}$ is the mirror image. Adding the squares of the two parts gives $|y - q| \ge |x_0 - q|$.

The decision region of $x_0$ for the minimum-distance rule on a square constellation is a product of two intervals: for the coordinate $u_0$ it is $[u_0 - a_1, u_0 + a_1]$ for an inner level, and $[a_{\max} - a_1, \infty)$ or $(-\infty, -a_{\max} + a_1]$ for an outer level. In the first case $\mathrm{Re}\, y = u_0$ is at the centre, as before. In the second case $\mathrm{Re}\, y \ge a_{\max}$, so its distance to the only boundary $a_{\max} - a_1$ is at least $a_1$, the distance of $u_0$. So $y$ lies inside the region of $x_0$, at least as far from each boundary as $x_0$, and the detector decides $x_0$. $\square$

**Lemma 4 (invariant).** At the start of each pass through line L3, $Y[k] \in E(X[k])$ for every $k$ and $x = T(Y)$. In particular $B(x) = Y$, and $x$ has no energy outside the band of the $N$ subcarriers.

*Proof.* Lines L1 and L2 set $Y = X$, and $X[k] \in E(X[k])$, and $x = T(Y)$. Each pass sets every $Y[k]$ to a projection onto $E(X[k])$ in line L7, and line L8 sets $x = T(Y)$. Lemma 1 gives $B(x) = Y$, and $F_{LN}\, x = \sqrt L\, Z(Y)$ is zero outside the band. $\square$

**Lemma 5 (a projected gradient step).** Let $g(x) = \frac12 \sum_t \big(|x[t]| - A\big)_+^2$ be the clipped energy, where $(s)_+ = \max(s, 0)$, and let $f(Y) = g(T(Y))$. Then $f$ is convex, its gradient is $L$-Lipschitz, and line L7 is

$$Y \leftarrow P_E\Big(Y - \frac{\mu}{L}\, \nabla f(Y)\Big),$$

where $P_E$ projects each subcarrier onto its region.

*Proof.* For one sample, $g_t(x) = \frac12 (|x| - A)_+^2 = \frac12 \mathrm{dist}(x, D)^2$, where $D$ is the closed disc of radius $A$. The squared distance to a closed convex set is convex and differentiable with gradient $x - P_D(x)$, and $x - P_D(x)$ is 1-Lipschitz because $I - P_D$ is firmly nonexpansive. Here $x - P_D(x) = (1 - A/|x|)\, x$ for $|x| > A$ and $0$ otherwise, which is $-e$ for the clipping noise $e$ of line L4. So $\nabla g(x) = -e$, and $\nabla g$ is 1-Lipschitz. By the chain rule and Lemma 1, $\nabla f(Y) = T^H \nabla g(T Y) = -L\, B(e)$, which is $-L\, E$ for the vector $E$ of line L6. So $Y + \mu E = Y - (\mu/L) \nabla f(Y)$, and line L7 projects it. $f$ is convex as a convex function of a linear map. Finally $\lVert \nabla f(Y) - \nabla f(Y') \rVert \le \lVert T^H \rVert\, \lVert T Y - T Y' \rVert \le L \lVert Y - Y' \rVert$, because $\lVert T \rVert = \lVert T^H \rVert = \sqrt L$. $\square$

**Theorem.** For any number of passes, the output $(x, Y)$ of line L9 satisfies:

1. $Y[k] \in E(X[k])$ for every $k$, so the receiver decides every $X[k]$ correctly without noise, and every distance margin is at least as large as for $X$ (Lemma 3);
2. $x = T(Y)$ is the exact band-limited OFDM symbol of $Y$ (Lemma 4);
3. if $0 < \mu \le 2$, the clipped energy $g(x)$ does not increase from one pass to the next, and if the loop stops at line L5, every sample has $|x[t]| \le A$.

*Proof.* Items 1 and 2 are Lemmas 3 and 4. For item 3, let $t = \mu/L$ and $Y^+ = P_E(Y - t \nabla f(Y))$. The projection onto the closed convex set $E$ satisfies $\langle Y - t\nabla f(Y) - Y^+, Y - Y^+ \rangle \le 0$, because $Y \in E$ by Lemma 4. This gives $\langle \nabla f(Y), Y^+ - Y \rangle \le -\frac1t \lVert Y^+ - Y \rVert^2$. The gradient of $f$ is $L$-Lipschitz, so the descent lemma gives

$$f(Y^+) \le f(Y) + \langle \nabla f(Y), Y^+ - Y \rangle + \frac L2 \lVert Y^+ - Y \rVert^2 \le f(Y) - \Big(\frac{L}{\mu} - \frac L2\Big) \lVert Y^+ - Y \rVert^2.$$

The coefficient is at least 0 when $\mu \le 2$, so $f(Y^+) \le f(Y)$, and $g(x) = f(Y)$ by Lemma 4. Line L5 stops only when the clipping noise is zero, that is, when no sample exceeds $A$. $\square$

**What is not claimed.** The clipped energy is a smooth stand-in for the peak. A smaller $g(x)$ does not always mean a smaller $\max_t |x[t]|$, and the PAPR also changes because the extension adds power. The theorem says nothing about how fast $g$ falls, and for $\mu > 2$ the step can overshoot.
