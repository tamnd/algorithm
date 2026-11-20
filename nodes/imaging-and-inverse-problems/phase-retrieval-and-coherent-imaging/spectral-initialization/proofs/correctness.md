---
title: The expected spectral matrix, an eigenvector perturbation bound, and power iteration
proves: [correctness]
status: full
---

Vectors are in $\mathbb{C}^n$ with $\langle u, v \rangle = u^* v$. The data are $y_r = |a_r^* x|^2$ for $r = 1, \dots, m$, and

$$Y = \frac{1}{m} \sum_{r=1}^m y_r\, a_r a_r^*, \qquad \lambda^2 = n \frac{\sum_r y_r}{\sum_r \|a_r\|^2}.$$

The algorithm returns $\lambda v$, where $v$ is the unit vector that power iteration gives for $Y$ (lines L3 to L6). The claim of correctness has three parts: $Y$ has the structure that makes the method work (Lemmas 1 and 2), its top eigenvector is close to the direction of $x$ when $Y$ is close to its mean (Lemma 3), and power iteration finds that eigenvector (Lemma 4). How large $m$ must be for $Y$ to be close to its mean is a result of Candès, Li and Soltanolkotabi (2015), which is cited and not proved here.

**Lemma 1.** $Y$ is Hermitian and positive semidefinite, and the data do not change when $x$ is replaced by $e^{i\varphi} x$.

*Proof.* Each term $y_r a_r a_r^*$ is Hermitian, and $v^* (y_r a_r a_r^*) v = y_r |a_r^* v|^2 \ge 0$ because $y_r \ge 0$. A sum of such terms has the same two properties. Also $|a_r^* e^{i\varphi} x|^2 = |a_r^* x|^2$. $\square$

So the method can only find $x$ up to a global phase, and the error is measured by $\operatorname{dist}(z, x) = \min_\varphi \|z - e^{i\varphi} x\|$, which equals $\sqrt{\|z\|^2 + \|x\|^2 - 2|x^* z|}$ (the minimum is at the phase of $x^* z$).

**Lemma 2 (the mean of $Y$).** If the $a_r$ are independent with entries $\mathcal{N}(0, 1/2) + i\,\mathcal{N}(0, 1/2)$, then $\mathbb{E}[Y] = \|x\|^2 I + x x^*$. If the $a_r$ are real with entries $\mathcal{N}(0, 1)$ and $x$ is real, then $\mathbb{E}[Y] = \|x\|^2 I + 2 x x^T$. In both cases $\mathbb{E}[y_r] = \|x\|^2$ and $\mathbb{E}\|a_r\|^2 = n$.

*Proof.* Take the complex case and $x \neq 0$. Let $U$ be unitary with $U^* x = \|x\| e_1$, and put $b = U^* a$ for one sampling vector $a$. The distribution of $a$ does not change under a unitary map, so $b$ has the same distribution as $a$. Now $y = |a^* x|^2 = |b^* U^* x|^2 = \|x\|^2 |b_1|^2$ and $a a^* = U b b^* U^*$, so

$$\mathbb{E}[y\, a a^*] = \|x\|^2\, U\, \mathbb{E}\bigl[|b_1|^2 b b^*\bigr] U^* .$$

The $(i, j)$ entry of $\mathbb{E}[|b_1|^2 b b^*]$ is $\mathbb{E}[|b_1|^2 b_i \overline{b_j}]$. For $i \neq j$, at least one of the indices $i$ and $j$ is not $1$, so at least one of the factors $b_i$ and $\overline{b_j}$ is independent of the other factors and has mean $0$, and the entry is $0$. For $i = j \neq 1$ it is $\mathbb{E}|b_1|^2\, \mathbb{E}|b_i|^2 = 1$. For $i = j = 1$ it is $\mathbb{E}|b_1|^4 = 2$, because $|b_1|^2$ has the exponential distribution with mean $1$. So $\mathbb{E}[|b_1|^2 b b^*] = I + e_1 e_1^*$, and

$$\mathbb{E}[y\, a a^*] = \|x\|^2 U (I + e_1 e_1^*) U^* = \|x\|^2 I + x x^* .$$

The mean of $Y$ is the mean of one term. In the real case the same steps with an orthogonal $U$ give $\mathbb{E}[b_1^4] = 3$ in place of $2$, so the result is $\|x\|^2 I + 2 x x^T$. Finally $\mathbb{E}[y] = \|x\|^2 \mathbb{E}|b_1|^2 = \|x\|^2$ and $\mathbb{E}\|a\|^2 = n$. $\square$

So the top eigenvector of $\mathbb{E}[Y]$ is $x / \|x\|$, with eigenvalue $2\|x\|^2$ (complex case) against $\|x\|^2$ for all other directions. By the law of large numbers, $\lambda^2 = (\frac1m \sum_r y_r) / (\frac{1}{mn} \sum_r \|a_r\|^2) \to \|x\|^2$ as $m \to \infty$.

**Lemma 3 (perturbation).** Let $H = \|x\|^2 I + x x^*$ with $x \neq 0$, let $Y$ be Hermitian with $\|Y - H\| \le \varepsilon$ (spectral norm), and let $v$ be a unit eigenvector of $Y$ for its largest eigenvalue. Then $|u^* v|^2 \ge 1 - 2\varepsilon / \|x\|^2$, where $u = x / \|x\|$.

*Proof.* The largest eigenvalue is the maximum of $w^* Y w$ over unit $w$, so $v^* Y v \ge u^* Y u \ge u^* H u - \varepsilon = 2\|x\|^2 - \varepsilon$. On the other hand $v^* Y v \le v^* H v + \varepsilon = \|x\|^2 + \|x\|^2 |u^* v|^2 + \varepsilon$. Together, $\|x\|^2 |u^* v|^2 \ge \|x\|^2 - 2\varepsilon$. $\square$

So if $Y$ is within $\varepsilon = \delta \|x\|^2$ of its mean, the angle $\theta$ between $v$ and $x$ has $\sin^2 \theta \le 2\delta$. Candès, Li and Soltanolkotabi (2015, Theorem 3.3) show that for $m \ge c_0\, n \log n$, with $c_0$ a large enough constant, the estimate scaled to the norm $\sqrt{\frac1m \sum_r y_r}$ has $\operatorname{dist}(z_0, x) \le \frac18 \|x\|$ with probability at least $1 - 10 e^{-\gamma n} - 8/n^2$, and they note that the same holds with $\lambda$. The $\log n$ is needed for this plain version because the terms $y_r a_r a_r^*$ have heavy tails; Chen and Candès (2017) remove the large $y_r$ and work with $m$ of order $n$.

**Lemma 4 (power iteration).** Let $Y$ be Hermitian and positive semidefinite with eigenvalues $\mu_1 > \mu_2 \ge \dots \ge \mu_n \ge 0$ and unit eigenvectors $u_1, \dots, u_n$. Let $v_0$ be a unit vector with $c_1 = u_1^* v_0 \neq 0$, and let $v_k = Y v_{k-1} / \|Y v_{k-1}\|$. Then, with $\theta_k$ the angle between $v_k$ and $u_1$,

$$\tan \theta_k \le \left(\frac{\mu_2}{\mu_1}\right)^k \tan \theta_0 .$$

*Proof.* Write $v_0 = \sum_j c_j u_j$. Then $v_k$ is a positive multiple of $Y^k v_0 = \sum_j \mu_j^k c_j u_j$. So

$$\tan^2 \theta_k = \frac{\sum_{j \ge 2} \mu_j^{2k} |c_j|^2}{\mu_1^{2k} |c_1|^2} \le \left(\frac{\mu_2}{\mu_1}\right)^{2k} \frac{\sum_{j \ge 2} |c_j|^2}{|c_1|^2} = \left(\frac{\mu_2}{\mu_1}\right)^{2k} \tan^2 \theta_0 . \qquad \square$$

Because $Y$ is positive semidefinite, its largest eigenvalue is also the largest in absolute value, so the iteration finds the top eigenvector and not an eigenvector of a large negative eigenvalue. A random start has $c_1 \neq 0$ with probability one. If $\mu_1 = \mu_2$, the top eigenvector is not unique and the method gives some unit vector in the top eigenspace. For $\mathbb{E}[Y]$ the ratio $\mu_2 / \mu_1$ is $1/2$ in the complex case and $1/3$ in the real case.

**What is not claimed.** The concentration of $Y$ about its mean, and so the bound $\operatorname{dist}(z_0, x) \le \frac18 \|x\|$, is cited, not proved. For small $m$ the estimate can be far from $x$; the tests measure the error on fixed seeds and do not check a theorem there.
