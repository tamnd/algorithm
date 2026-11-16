---
title: The MOSSE filter is the exact minimizer of the regularized output error, the running update minimizes an exponentially weighted error, and a circular shift of the input shifts the peak
proves: [correctness]
status: full
---

Notation as on the page. Patches are $n \times n$ real arrays indexed by $x \in \mathbb{Z}_n^2$ (indices modulo $n$). The DFT is $\hat f(k) = \sum_x f(x) e^{-2\pi i \langle k, x \rangle / n}$ with no factor, so its inverse has the factor $1/n^2$. Products and quotients of transforms are taken entry by entry, and $\bar z$ is the complex conjugate.

## Claim 1: correlation is a product with the conjugate

For real $f$ and $h$ let $g(y) = \sum_x f(x + y)\, h(x)$, the circular correlation. Then $\hat g = \hat f\, \overline{\hat h}$.

*Proof.* $\hat g(k) = \sum_y \sum_x f(x + y) h(x) e^{-2\pi i \langle k, y \rangle / n}$. Put $z = x + y$; as $y$ runs over $\mathbb{Z}_n^2$ so does $z$, and $e^{-2\pi i \langle k, y \rangle / n} = e^{-2\pi i \langle k, z \rangle / n} e^{2\pi i \langle k, x \rangle / n}$. The double sum splits into $\hat f(k) \sum_x h(x) e^{2\pi i \langle k, x \rangle / n} = \hat f(k) \overline{\hat h(k)}$, since $h$ is real. $\square$

So the filter can be stored as $H^* = \overline{\hat h}$, and the response to a patch $f$ is the inverse DFT of $\hat f H^*$.

## Claim 2: the closed form is the exact minimizer

Given training patches $f_1, \ldots, f_N$ with desired outputs $g_1, \ldots, g_N$ and $\varepsilon \ge 0$, consider

$$
E(H^*) = \sum_{i=1}^N \sum_k \big| \hat f_i(k) H^*(k) - \hat g_i(k) \big|^2 + \varepsilon \sum_k |H^*(k)|^2 .
$$

If $\varepsilon > 0$, or if $\sum_i |\hat f_i(k)|^2 > 0$ for every $k$, the unique minimizer is

$$
H^*(k) = \frac{\sum_i \hat g_i(k)\, \overline{\hat f_i(k)}}{\sum_i \hat f_i(k)\, \overline{\hat f_i(k)} + \varepsilon} = \frac{A(k)}{B(k) + \varepsilon} .
$$

*Proof.* $E$ is a sum of terms that each depend on one $H^*(k)$, so we minimize each term separately. Fix $k$, write $z = H^*(k)$, $a_i = \hat f_i(k)$, $b_i = \hat g_i(k)$ and $\beta = \sum_i |a_i|^2 + \varepsilon > 0$. Then

$$
\sum_i |a_i z - b_i|^2 + \varepsilon |z|^2 = \beta |z|^2 - 2 \operatorname{Re}\Big( z \sum_i a_i \bar b_i \Big) + \sum_i |b_i|^2 = \beta \Big| z - \frac{\sum_i \bar a_i b_i}{\beta} \Big|^2 + \text{const},
$$

which is minimized exactly at $z = \sum_i \bar a_i b_i / \beta$. $\square$

By Parseval's identity $\sum_k |\hat e(k)|^2 = n^2 \sum_x |e(x)|^2$, and by Claim 1, the data term is $n^2$ times $\sum_i \sum_x ((f_i \star h)(x) - g_i(x))^2$, the sum of squared errors of the correlation outputs in the image domain. So the filter minimizes the output sum of squared error, which gives the method its name, plus the penalty $\varepsilon n^2 \sum_x h(x)^2$.

**One training image.** With $N = 1$, the response to $f_1$ itself is $\hat f_1 H^* = \frac{|\hat f_1|^2}{|\hat f_1|^2 + \varepsilon} \hat g_1$. It equals $\hat g_1$ at every frequency where $\hat f_1 \ne 0$ as $\varepsilon \to 0$, and it is 0 where $\hat f_1 = 0$. So a single image is fit exactly up to its missing frequencies, which is why one image overfits and why several perturbed copies are used.

## Claim 3: the running update minimizes an exponentially weighted error

Let $A_0, B_0$ be the sums of Claim 2 over the initial training set, and for $t \ge 1$ let

$$
A_t = \eta\, \hat g\, \overline{\hat f_t} + (1 - \eta) A_{t-1}, \qquad B_t = \eta\, \hat f_t \overline{\hat f_t} + (1 - \eta) B_{t-1},
$$

with $0 < \eta \le 1$. Then $A_t / (B_t + \varepsilon)$ is the minimizer of

$$
E_t(H^*) = (1 - \eta)^t E_0(H^*) + \sum_{s=1}^t \eta (1 - \eta)^{t - s} \sum_k |\hat f_s H^* - \hat g|^2 + \varepsilon \sum_k |H^*|^2 ,
$$

where $E_0$ is the data term over the initial set.

*Proof.* By induction, $A_t = (1 - \eta)^t A_0 + \sum_{s=1}^t \eta (1 - \eta)^{t-s} \hat g \overline{\hat f_s}$, and the same for $B_t$. The proof of Claim 2 works with positive weights on the terms: with weights $c_i > 0$ the minimizer is $\sum_i c_i \bar a_i b_i / (\sum_i c_i |a_i|^2 + \varepsilon)$. The weights here are $(1 - \eta)^t$ for the initial terms and $\eta (1 - \eta)^{t-s}$ for frame $s$, which give exactly $A_t$ and $B_t$. $\square$

## Claim 4: a circular shift of the input moves the peak by the same amount

If $f'(x) = f(x - d)$ for all $x$ (indices modulo $n$), then the response to $f'$ is $g'(y) = g(y - d)$, where $g$ is the response to $f$.

*Proof.* $g'(y) = \sum_x f(x + y - d) h(x) = g(y - d)$. $\square$

So if the filter gives its peak at the patch center $c$ for the target, a target that moved by $d$ gives the peak at $c + d$, and line L7 recovers $d$. For a real frame the new patch is not a circular shift of the old one: new content enters at one side. The cosine window lowers the weight of the border, but the claim then holds only approximately. This is a heuristic step, and the example on the page measures how well it works.

## What is not claimed

The peak to sidelobe ratio and its threshold are heuristics; nothing here says that a low ratio means failure or a high ratio means success. The filter is optimal only for the training patches and the stated objective. Whether it finds the target in a new frame depends on how much the appearance changed.
