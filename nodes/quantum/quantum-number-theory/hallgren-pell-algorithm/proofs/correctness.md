---
title: Hallgren's algorithm returns the regulator and the fundamental solution of Pell's equation
proves: [correctness]
status: full
---

We use the pseudocode of the page. $D > 1$ is not a square, $\mathcal{O} = \mathbb{Z}[\sqrt D]$, $\varepsilon = x_1 + y_1 \sqrt D$ is its fundamental unit with $\varepsilon > 1$, and $R = \ln \varepsilon$. The input register has size $q$, the scale is $N > 0$, $S = NR$, the window is $w = 1/N$, and $B \ge R$ is a known bound with $q \ge 3(NB)^2$. We assume $S \ge 1$.

**Facts about the cycle.** We use the following standard facts about the continued fraction of $\sqrt D$, with $a_k$, $P_k$, $Q_k$ and the convergents $p_k/q_k$ as on the page (see the book *Solving the Pell Equation* by Jacobson and Williams). Let $\theta_k = p_{k-1} + q_{k-1}\sqrt D$ with $\theta_0 = 1$, let $I_k$ be the ideal $[Q_k, P_k + \sqrt D]$, and let $\ell$ be the period of the expansion.

1. $\theta_k \bar\theta_k = (-1)^k Q_k$, and $\theta_k$ generates $I_k$ or its conjugate, so the ideal (as a label) is determined by $(Q_k, P_k \bmod Q_k)$.
2. $\theta_{k + \ell} = \varepsilon\,\theta_k$ and $(Q_{k+\ell}, P_{k+\ell} \bmod Q_{k+\ell}) = (Q_k, P_k \bmod Q_k)$. The labels of $I_0, \dots, I_{\ell - 1}$ are distinct, and $Q_k = 1$ if and only if $\ell$ divides $k$.
3. $\theta_0 < \theta_1 < \theta_2 < \cdots$, so the distances $\delta_k = \ln \theta_k$ increase strictly, with $\delta_0 = 0$ and $\delta_{k+\ell} = \delta_k + R$.
4. $x_1 + y_1\sqrt D$ with $x_1, y_1 \ge 1$ gives $R \ge \ln(1 + \sqrt D)$. The positive solutions of $x^2 - Dy^2 = 1$ are the powers $\eta^n$ of $\eta = \varepsilon$ if $\varepsilon\bar\varepsilon = 1$, and of $\eta = \varepsilon^2$ if $\varepsilon\bar\varepsilon = -1$. The fundamental solution is $\eta$.

So the distances at which the ideal $(1) = \mathcal{O}$ occurs are exactly the multiples $uR$, $u \ge 0$, and its generator there is $\varepsilon^u$.

**Lemma 1 (weak periodicity).** For integers $0 \le k < k' < q$, $f_N(k) = f_N(k')$ implies $|k' - k - uS| < 1$ for some integer $u \ge 1$. For each $k$ and $u$ at most one $k'$ has this property with $f_N(k') = f_N(k)$.

*Proof.* Let $f_N(k) = (I_j, o)$ with $o = \lfloor k - N\delta_j \rfloor$ and $f_N(k') = (I_{j'}, o')$. Equal labels give equal ideals, so $j' = j + u\ell$ for an integer $u$ by Fact 2, and $\delta_{j'} = \delta_j + uR$ by Fact 3. Then $o = o'$ means that $k - N\delta_j$ and $k' - N\delta_j - uS$ lie in the same interval $[o, o + 1)$, so they differ by less than 1. For fixed $u$, $k'$ lies in $[N\delta_j + uS + o,\ N\delta_j + uS + o + 1)$, which holds at most one integer. Since $k' > k$ and the distances increase, $u \ge 1$. $\square$

**Lemma 2 (the output distribution).** One run of lines L3 to L6 gives $c \in \{0, \dots, q - 1\}$ with probability

$$P(c) = \frac{1}{q^2} \sum_{v} \Big| \sum_{k < q,\ f_N(k) = v} e^{2\pi i kc/q} \Big|^2,$$

where $v$ runs over the values of $f_N$.

*Proof.* Line L3 gives $q^{-1/2} \sum_k |k\rangle|0\rangle$ and line L4 gives $q^{-1/2}\sum_k |k\rangle|f_N(k)\rangle$, where the target holds an injective code of the value. After line L5 the amplitude of $|c\rangle|v\rangle$ is $q^{-1} \sum_{f_N(k) = v} e^{2\pi i kc/q}$. The states $|v\rangle$ are orthogonal, so the probability of $c$ is the sum over $v$ of the squared moduli. $\square$

By Lemma 1, each level set $\{k : f_N(k) = v\}$ is a set of points within distance 1 of an arithmetic progression with the irrational step $S$. Call a pair of samples *good* if it satisfies the hypotheses of Lemma 3 below. Hallgren's analysis of Fourier sampling for such functions shows that a pair is good with probability at least inverse polynomial in $\log D$, for suitable $N$ and $q$. The theorem below does not depend on this bound, which only controls the number of rounds.

**Lemma 3 (the convergent step).** Let $|c_i - j_i q/S| \le 1$ for $i = 1, 2$, with integers $1 \le j_1, j_2 \le J$, $\gcd(j_1, j_2) = 1$, and $q > (4J + 1)S$. Then $j_1/j_2$ is a convergent of $c_1/c_2$, and $t = j_1 q/(N c_1)$ satisfies $|t - R| \le w$ and $t \le B + w$.

*Proof.* Write $c_i = j_i q/S + \beta_i$ with $|\beta_i| \le 1$. Then $c_1 j_2 - c_2 j_1 = \beta_1 j_2 - \beta_2 j_1$, which has modulus at most $2J$, and $c_2 \ge j_2(q/S - 1) > 4J j_2$. So

$$\Big| \frac{c_1}{c_2} - \frac{j_1}{j_2} \Big| \le \frac{2J}{c_2 j_2} < \frac{1}{2 j_2^2},$$

and by Legendre's theorem on continued fractions, the reduced fraction $j_1/j_2$ is a convergent of $c_1/c_2$. Next, $t = R/(1 + \beta_1 S/(j_1 q))$, so $|t - R| \le R \cdot \frac{S/q}{1 - S/q} = \frac{NR^2}{q - S}$. From $q \ge 3(NB)^2 \ge 3S^2$ and $S \ge 1$ we get $q - S \ge 3S^2 - S \ge S^2 = N^2R^2$, so $|t - R| \le NR^2/(N^2R^2) = 1/N = w$. Finally $t \le R + w \le B + w$. $\square$

**Lemma 4 (the window test).** Line L8 records only positive multiples $uR$ of $R$ with $uR \le B + 2w$. Line L11 always finds $R$, and every distance it finds is a positive multiple of $R$.

*Proof.* Line L8 records a distance $\delta > 0$ of the ideal $(1)$, so $\delta = uR$ with $u \ge 1$ by the facts above, and $\delta \le t + w \le B + 2w$. Let $\delta^\star = uR$ be the smallest recorded distance. By Fact 4, $u \le (B + 2w)/R \le (B + 2w)/\ln(1 + \sqrt D) \le K$. For $k = u$, the center $\delta^\star/k$ is exactly $R$, and $(1)$ has distance $R$ there, so line L11 finds $R$. Everything that line L11 finds is again a distance of $(1)$ above 0, so a positive multiple of $R$. $\square$

**Theorem.** If the algorithm returns, it returns the regulator $R$ exactly as the distance $\ln \varepsilon$ of the cycle, and the fundamental solution $(x, y)$ of $x^2 - Dy^2 = 1$. Each round with a good pair of samples returns, so the number of rounds is at most geometric with the success rate of a good pair.

*Proof.* By Lemma 4, line L11 finds $R$ and nothing smaller, so line L12 takes the distance $R$ and its generator $\theta_\ell = \varepsilon = x + y\sqrt D$. If $x^2 - Dy^2 = 1$, then $\varepsilon$ is the fundamental solution by Fact 4. Otherwise $x^2 - Dy^2 = -1$, and line L13 replaces $\varepsilon$ by $\varepsilon^2 = (x^2 + Dy^2) + 2xy\sqrt D$, which has norm $(-1)^2 = 1$ and is the fundamental solution by Fact 4. For a good pair, Lemma 3 shows that $t = j_1 q/(N c_1)$ is one of the estimates of line L7 and lies within $w$ of $R$, where $(1)$ has the distance $R$, so line L8 records it and the round returns. $\square$

The exact output does not depend on floating-point accuracy beyond the window test: $R$ and $\varepsilon$ come from the cycle, and the identities $x^2 - Dy^2 = \pm 1$ are checked in integers.
