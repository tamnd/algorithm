---
title: The records are unbiased, the grid finds exactly the valid records, and the interpolation error is O(a) under the split sphere model
proves: [correctness]
status: full
---

Let $x$ be a point with the unit normal $n$, and let $E(x) = \int_{H^2(n)} L_i(x, \omega) \cos\theta\, d\omega$ be its irradiance. Assume that $0 \le L_i \le L_{\max}$. A record is $(x_i, n_i, E_i, R_i)$ with $R_i > 0$, and its weight at $(x, n)$ is

$$w_i(x) = \frac{1}{|x - x_i|/R_i + \sqrt{1 - n \cdot n_i}},$$

with $w_i = \infty$ when the denominator is 0. The set of valid records at $(x, n)$ is $S = \{ i : w_i(x) > 1/a \}$.

**Lemma 1 (a record is unbiased).** Line L4 with $m \times m$ strata takes $u_1$ uniform in $[i/m, (i + 1)/m)$ and $u_2$ uniform in $[j/m, (j + 1)/m)$ for each stratum $(i, j)$, and maps them to the direction $\omega$ with $\sin\theta = \sqrt{u_1}$ and $\phi = 2\pi u_2$. Then $\hat E = \frac{\pi}{m^2}\sum_{i, j} L_i(x, \omega_{ij})$ has $E[\hat E] = E(x)$ and $\operatorname{Var}[\hat E] \le \pi^2 L_{\max}^2 / (4m^2)$.

*Proof.* The map $(u_1, u_2) \mapsto \omega$ has $u_1 = \sin^2\theta$, so $du_1\, du_2 = 2\sin\theta\cos\theta\, d\theta \cdot d\phi/(2\pi) = \frac{\cos\theta}{\pi}\, d\omega$, since $d\omega = \sin\theta\, d\theta\, d\phi$. So a point uniform in the unit square gives $\omega$ with the density $\cos\theta/\pi$. Each stratum has the area $1/m^2$, so

$$E[\hat E] = \pi \sum_{i, j} \frac{1}{m^2}\, m^2 \int_{\text{stratum}} L_i(x, \omega(u))\, du = \pi \int_{[0,1]^2} L_i(x, \omega(u))\, du = \pi \int_{H^2} L_i \frac{\cos\theta}{\pi}\, d\omega = E(x).$$

The $m^2$ samples are independent. Each one lies in $[0, L_{\max}]$, so its variance is at most $L_{\max}^2/4$. So $\operatorname{Var}[\hat E] \le \frac{\pi^2}{m^4} \cdot m^2 \cdot \frac{L_{\max}^2}{4}$. $\square$

**Lemma 2 (the grid lookup).** Line L6 puts record $i$ into every grid cell whose key lies between the key of $x_i - aR_i(1, 1, 1)$ and the key of $x_i + aR_i(1, 1, 1)$, coordinate by coordinate. Line L1 looks at the records of the cell of $x$ and keeps those with $w_i(x) > 1/a$. Then line L1 returns exactly $S$.

*Proof.* Every record that line L1 returns passes the weight test, so it is in $S$. Conversely, let $i \in S$. Then $|x - x_i|/R_i \le 1/w_i(x) < a$, so $|x - x_i| < aR_i$, and each coordinate of $x$ lies within $aR_i$ of the same coordinate of $x_i$. The key of a coordinate is $\lfloor c/h \rfloor$ for the cell size $h$, which is a nondecreasing function of $c$. So each coordinate of the key of $x$ lies between the two bounds of line L6, record $i$ is in the cell of $x$, and line L1 finds it. $\square$

The test compares line L1 with a scan of all the records, which is Lemma 2.

**Lemma 3 (convex combination).** If $S$ is not empty, the value of line L3 lies between $\min_{i \in S} E_i$ and $\max_{i \in S} E_i$. If $(x, n)$ is the position and normal of a record, the value is the value of that record.

*Proof.* The weights in $S$ are positive, so line L3 is a convex combination of the $E_i$. If $x = x_i$ and $n = n_i$, then $w_i = \infty$, and the implementation returns $E_i$, which is the limit of line L3 as $w_i \to \infty$. $\square$

**Theorem 1 (interpolation error).** Assume the split sphere bound: for every record $i$ and every $(x, n)$,

$$|E(x) - E(x_i)| \le C\, E(x_i) \left( \frac{|x - x_i|}{R_i} + \sqrt{1 - n \cdot n_i} \right) = \frac{C\, E(x_i)}{w_i(x)}, \tag{H}$$

with a constant $C$. If each record has the exact value $E_i = E(x_i)$, then the value $\tilde E(x)$ of line L3 has

$$|\tilde E(x) - E(x)| < C\, a\, \max_{i \in S} E_i.$$

*Proof.* Let $W = \sum_{i \in S} w_i(x)$. Then

$$|\tilde E(x) - E(x)| = \Big| \sum_{i \in S} \frac{w_i}{W} \big(E_i - E(x)\big) \Big| \le \sum_{i \in S} \frac{w_i}{W} \cdot \frac{C E_i}{w_i} = \frac{C}{W} \sum_{i \in S} E_i.$$

Each $w_i > 1/a$, so $W > |S|/a$, and $\sum_{i \in S} E_i \le |S| \max_{i \in S} E_i$. Combine the two. $\square$

Ward obtained (H) for the worst case of a point at the center of a sphere of radius $R_i$ with one bright half and one dark half. A movement $\delta$ changes $E$ by about $\frac{4}{\pi}\frac{\delta}{R_i}E$, and a rotation by the angle $\theta$ changes it by about $\sqrt{2 - 2\cos\theta}\,E = \sqrt 2 \sqrt{1 - \cos\theta}\, E$, so (H) holds to first order with $C = \max(4/\pi, \sqrt 2) = \sqrt 2$. (H) is a model and not a theorem about every scene. The harmonic mean of line L5 estimates the distance $R_i$ to the surfaces that matter most, and a small nearby object that no ray hits makes the estimate too large. The test measures the error with exact records, as in Theorem 1, and checks that it falls as $a$ falls.

**Theorem 2 (noisy records).** If the records have the values $E_i = E(x_i) + \eta_i$, the value of line L3 is $\tilde E(x) + \sum_{i \in S} \frac{w_i}{W}\eta_i$, with $\tilde E$ as in Theorem 1. The second term has the absolute value at most $\max_{i \in S} |\eta_i|$.

*Proof.* Line L3 is linear in the $E_i$, and the weights $w_i/W$ are nonnegative and sum to 1. $\square$

So a smaller $a$ does not reduce the error below the noise of one record, which is what the second test of the example shows.

**Theorem 3 (convergence in the double limit).** Let the queries be a finite set $P$ of distinct points with their normals, in a closed scene where every ray hits a surface within the distance $D$. If no two points of $P$ share a position and $a\, D < \min |x - x'|$ over the distinct points $x, x'$ of $P$, then each point of $P$ makes its own record, and its value is the estimate of Lemma 1. So it is unbiased and its variance is $O(1/m^2)$, which goes to 0 as $m \to \infty$.

*Proof.* The harmonic mean of line L5 is at most the largest hit distance, so $R_i \le D$. For a record at $x_i \ne x$ in $P$, $|x - x_i|/R_i \ge |x - x_i|/D > a$, so $w_i(x) < 1/a$ and record $i$ is not valid at $x$. So the first query at $x$ finds no valid record and makes one by lines L4 to L7, and a later query at the same $(x, n)$ returns it by Lemma 3. Apply Lemma 1. $\square$

For a fixed $a$ and $m$ the method is biased, by Theorem 1 and by the interpolation of noisy values.
