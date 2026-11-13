---
title: Each level of the pi/3 recursion cubes the failure probability
proves: [correctness]
status: full
---

We use the pseudocode of the page. The search space is $\{0, 1, \ldots, N-1\}$, $S$ is the set of marked items with $|S| = M$, $P$ is the projector onto the span of $\{|x\rangle : x \in S\}$, and $\bar P = I - P$. Let $\omega = e^{i\pi/3}$ and

$$R_t(\omega) = I - (1 - \omega)P, \qquad R_s(\omega) = I - (1 - \omega)|s\rangle\langle s|,$$

where $|s\rangle$ is the uniform superposition. $R_t(\omega)$ is one query: it multiplies each marked item by $\omega$. Both operators are unitary, with $R_t(\omega)^\dagger = R_t(\bar\omega)$ and $R_s(\omega)^\dagger = R_s(\bar\omega)$. The procedure APPLY-U defines $U_0 = I$ and

$$U_k = U_{k-1}\, R_s(\omega)\, U_{k-1}^\dagger\, R_t(\omega)\, U_{k-1} \quad (k \ge 1),$$

and its branch for the adjoint applies $U_k^\dagger = U_{k-1}^\dagger R_s(\bar\omega) U_{k-1} R_t(\bar\omega) U_{k-1}^\dagger$, the factors of $U_k$ in reverse order and each one inverted. Let $\varepsilon_k = \|\bar P\, U_k|s\rangle\|^2$ be the probability that a measurement of $U_k|s\rangle$ gives an unmarked item.

**Claim.** $\varepsilon_k = \varepsilon_{k-1}^3$ for each $k \ge 1$. So $\varepsilon_n = (1 - M/N)^{3^n}$, the success probability $1 - (1 - M/N)^{3^n}$ never decreases with $n$, and $U_n$ makes $q_n = (3^n - 1)/2$ queries. FIXED-POINT-SEARCH never returns an unmarked item, and if $M/N \ge w$, the depth $n$ of line L1 makes it fail with probability at most $\varepsilon$.

*Proof.* **One level.** Fix $k \ge 1$ and let $|u\rangle = U_{k-1}|s\rangle$, a unit vector. Then $\langle u|P|u\rangle = \|P|u\rangle\|^2 = 1 - \varepsilon_{k-1}$. Write $c = 1 - \omega$. Since $U_{k-1}$ is unitary,

$$U_{k-1} R_s(\omega) U_{k-1}^\dagger = I - c\, U_{k-1}|s\rangle\langle s|U_{k-1}^\dagger = I - c\,|u\rangle\langle u|.$$

So

$$U_k|s\rangle = (I - c|u\rangle\langle u|)(I - cP)|u\rangle = (I - c|u\rangle\langle u|)(|u\rangle - cP|u\rangle).$$

Expand, with $\langle u|u\rangle = 1$ and $\langle u|P|u\rangle = 1 - \varepsilon_{k-1}$:

$$U_k|s\rangle = |u\rangle - cP|u\rangle - c|u\rangle + c^2(1 - \varepsilon_{k-1})|u\rangle = \big(1 - c + c^2(1 - \varepsilon_{k-1})\big)|u\rangle - cP|u\rangle.$$

Apply $\bar P$. Since $\bar P P = 0$,

$$\bar P\, U_k|s\rangle = \big(1 - c + c^2 - c^2\varepsilon_{k-1}\big)\,\bar P|u\rangle.$$

**The choice of $\pi/3$.** $c = 1 - e^{i\pi/3} = \frac{1}{2} - \frac{\sqrt{3}}{2}i = e^{-i\pi/3}$, so $c^2 = e^{-2i\pi/3} = -\frac{1}{2} - \frac{\sqrt{3}}{2}i$. Then

$$1 - c + c^2 = 1 - \tfrac{1}{2} + \tfrac{\sqrt{3}}{2}i - \tfrac{1}{2} - \tfrac{\sqrt{3}}{2}i = 0.$$

So $\bar P\,U_k|s\rangle = -c^2\varepsilon_{k-1}\,\bar P|u\rangle$, and since $|c| = 1$ and $\|\bar P|u\rangle\|^2 = \varepsilon_{k-1}$,

$$\varepsilon_k = \varepsilon_{k-1}^2 \cdot \varepsilon_{k-1} = \varepsilon_{k-1}^3.$$

**All levels.** $U_0 = I$, so $\varepsilon_0 = \|\bar P|s\rangle\|^2 = (N - M)/N = 1 - M/N$. By induction, $\varepsilon_n = (1 - M/N)^{3^n}$. Since $0 \le 1 - M/N \le 1$, the sequence $\varepsilon_n$ does not increase, so the success probability $1 - \varepsilon_n$ does not decrease.

**Queries.** $U_0$ makes no query. $U_k$ calls $U_{k-1}$ three times (once as $U_{k-1}^\dagger$, which makes the same number of queries) and $R_t$ once. So $q_0 = 0$ and $q_k = 3q_{k-1} + 1$, which gives $q_n = (3^n - 1)/2$. The adjoint branch has the same count.

**The run.** Line L4 measures $U_n|s\rangle$, so it gives an unmarked item with probability $\varepsilon_n$. Line L5 checks the item, so FIXED-POINT-SEARCH never returns an unmarked item, and it returns FAIL with probability $\varepsilon_n$. Line L1 picks the smallest $n$ with $(1 - w)^{3^n} \le \varepsilon$. If $M/N \ge w$, then $\varepsilon_n = (1 - M/N)^{3^n} \le (1 - w)^{3^n} \le \varepsilon$. $\blacksquare$

**Remark.** The proof uses nothing about $|s\rangle$ and $P$ except that $|s\rangle$ is a unit vector and $P$ a projector. So the same recursion works for each start state $A|0\rangle$ and each set of good states, as in [amplitude amplification](/amplitude-amplification/), with $R_s$ the phase $\omega$ on $A|0\rangle$.
