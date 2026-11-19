---
title: The mel conversions are inverse to each other and have the stated shape
proves: [correctness]
status: full
---

We prove the facts that the page and the implementation rely on. Let $m(f) = 2595 \log_{10}(1 + f/700)$ for $f \ge 0$ and $g(u) = 700(10^{u/2595} - 1)$ for $u \ge 0$.

**Lemma 1 (inverse).** $g(m(f)) = f$ for $f \ge 0$ and $m(g(u)) = u$ for $u \ge 0$.

*Proof.* $10^{m(f)/2595} = 1 + f/700$, so $g(m(f)) = 700 \cdot f/700 = f$. Also $1 + g(u)/700 = 10^{u/2595}$, whose $\log_{10}$ is $u / 2595$. $\square$

**Lemma 2 (shape).** $m$ is strictly increasing and strictly concave on $[0, \infty)$, with $m'(f) = 2595 / ((700 + f)\ln 10)$. As $f \to 0$, $m(f) / f \to 2595 / (700 \ln 10) = 1.6100$. For $f \ge 0$, $m(2f) - m(f) = 2595 \log_{10}\bigl((700 + 2f) / (700 + f)\bigr)$, which increases with $f$ and tends to $2595 \log_{10} 2 = 781.17$.

*Proof.* Differentiate: $m'(f) > 0$ and $m''(f) = -2595 / ((700 + f)^2 \ln 10) < 0$. The limit of $m(f)/f$ is $m'(0)$. The ratio $(700 + 2f)/(700 + f) = 2 - 700/(700 + f)$ increases with $f$ and tends to 2. $\square$

So an octave adds fewer mels at low frequencies than at high ones, never more than 781.17, which is the sense in which the scale is logarithmic at high frequencies.

**Lemma 3 (the natural log form).** $1127 \ln(1 + f/700) = (1127 / c)\, m(f)$ with $c = 2595 / \ln 10 = 1126.9942$, so the two forms differ by the factor $1.0000052$, a relative difference below $10^{-5}$ at every frequency.

*Proof.* $2595 \log_{10} x = (2595 / \ln 10) \ln x$. $\square$

**Lemma 4 (the Slaney scale).** $m_S$ is continuous and strictly increasing, and its inverse is $f = f_{sp}\, u$ for $u < 15$ and $f = 1000\, e^{s(u - 15)}$ for $u \ge 15$.

*Proof.* Both pieces are strictly increasing, the linear piece tends to $1000 / f_{sp} = 15$ at $f = 1000$, and the log piece is $15$ there, so $m_S$ is continuous and strictly increasing. Each branch of the inverse solves its piece for $f$, and the branch is chosen by $u < 15$ exactly when $f < 1000$. $\square$

The tests check the values of the table on the page, Lemma 1 and Lemma 4 on a grid of frequencies, Lemma 3 to 4 significant digits, and the monotone shape of both scales.
