---
title: Correctness of asymmetric LSH with the simple transformation
proves: [correctness]
status: full
---

Let $X = \{x_1, \dots, x_n\} \subset \mathbb{R}^d$, $M = \max_i \|x_i\| > 0$, $q \ne 0$, and $s(q, x) = q \cdot x/(M\|q\|)$.

**Lemma 1.** $\|P(x)\| = \|Q(q)\| = 1$ and $P(x) \cdot Q(q) = s(q, x)$.

*Proof.* Since $\|x\| \le M$, the number $1 - \|x\|^2/M^2$ is in $[0, 1]$ and its root is real. $\|P(x)\|^2 = \|x\|^2/M^2 + (1 - \|x\|^2/M^2) = 1$, and $\|Q(q)\|^2 = \|q\|^2/\|q\|^2 + 0 = 1$. The last coordinate of $Q(q)$ is 0, so $P(x) \cdot Q(q) = (x/M) \cdot (q/\|q\|) = s(q, x)$. $\square$

So by the Cauchy-Schwarz inequality $s(q, x) \in [-1, 1]$, and the angle $\theta(x) = \arccos s(q, x)$ between $P(x)$ and $Q(q)$ is a decreasing function of $q \cdot x$.

**Lemma 2.** Let $a$ have independent standard normal entries and $u, v$ be unit vectors at angle $\theta \in [0, \pi]$. Then $\Pr[\operatorname{sign}(a \cdot u) = \operatorname{sign}(a \cdot v)] = 1 - \theta/\pi$.

*Proof.* Let $a'$ be the orthogonal projection of $a$ onto the plane spanned by $u$ and $v$ (any plane containing them if $u = \pm v$). Then $a \cdot u = a' \cdot u$ and $a \cdot v = a' \cdot v$. The distribution of $a$ is invariant under rotations, so $a'$ is a standard normal vector in the plane, and its direction is uniform on the circle. With probability 1 it is not orthogonal to $u$ or $v$. The signs differ exactly when the line orthogonal to $a'$ separates $u$ from $v$; this line has a uniform direction, and it separates them for an arc of directions of total measure $2\theta$ out of $2\pi$. So the signs differ with probability $\theta/\pi$. $\square$

With $u = P(x)$ and $v = Q(q)$, one bit agrees with probability $f(s) = 1 - \arccos(s)/\pi$, which is increasing in $s$. So when $s(q, x) \ge S$ a bit agrees with probability at least $p_1 = f(S)$, and when $s(q, x) \le cS$ with probability at most $p_2 = f(cS)$; $p_1 > p_2$ since $S > cS$. The $k$ bits of a key use independent vectors, so a key agrees with probability $f(s)^k$.

**Theorem.** Let $k = \lceil \ln n/\ln(1/p_2) \rceil$ and $L = \lceil n^\rho/p_1 \rceil$ with $\rho = \ln(1/p_1)/\ln(1/p_2)$. If some $x^*$ has $s(q, x^*) \ge S$, then with probability at least $1 - 1/e$ QUERY returns a point $x'$ with $s(q, x') \ge S$. The expected number of candidates $x$ with $s(q, x) \le cS$ is at most $L$.

*Proof.* In one table, $x^*$ shares the bucket of $q$ with probability at least $p_1^k$. Since $k < \ln n/\ln(1/p_2) + 1$,
$$p_1^k \ge p_1 \cdot p_1^{\ln n/\ln(1/p_2)} = p_1 \cdot e^{-\ln n \cdot \ln(1/p_1)/\ln(1/p_2)} = p_1 n^{-\rho}.$$
The $L$ tables are independent, so $x^*$ is missed by all of them with probability at most $(1 - p_1 n^{-\rho})^L \le e^{-L p_1 n^{-\rho}} \le e^{-1}$, since $L p_1 \ge n^\rho$. If $x^*$ is a candidate, line L7 returns the candidate $x'$ with the largest $q \cdot x$, so $q \cdot x' \ge q \cdot x^*$ and $s(q, x') \ge s(q, x^*) \ge S$.

For the second claim, a point with $s(q, x) \le cS$ shares the bucket of $q$ in one table with probability at most $p_2^k \le p_2^{\ln n/\ln(1/p_2)} = 1/n$. By linearity of expectation over at most $n$ such points and $L$ tables, the expected number of such candidates, counted with repetition, is at most $L$. $\blacksquare$
