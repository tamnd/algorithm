---
title: E2LSH answers the (c, r)-near neighbor query with constant probability
proves: [correctness]
status: full
---

Let $P \subseteq \mathbb{R}^d$ with $|P| = n \ge 1$, $r > 0$, $c > 1$ and $w > 0$. A function of the family is $h(v) = \lfloor (a \cdot v + b)/w \rfloor$ with $a$ a vector of $d$ independent $N(0,1)$ entries and $b$ uniform in $[0, w)$, independent of $a$.

**Lemma 1.** For $\|x - y\| = u > 0$, $\Pr[h(x) = h(y)] = p(u) := \mathbb{E}\big[\max(0, 1 - u|Z|/w)\big]$ with $Z \sim N(0,1)$.

*Proof.* The random variable $a \cdot (x - y) = \sum_i a_i (x_i - y_i)$ is a sum of independent normal variables, so it is normal with mean 0 and variance $\sum_i (x_i - y_i)^2 = u^2$; it has the law of $uZ$. Fix $a$ and let $\alpha = a \cdot x$, $\beta = a \cdot y$, $s = |\alpha - \beta|$. Then $h(x) = h(y)$ if and only if the half-open interval between $\alpha + b$ and $\beta + b$ (of length $s$) contains no multiple of $w$. Since $b$ is uniform on $[0, w)$, the set $\{\alpha + b\}$ modulo $w$ is uniform on $[0, w)$. If $s \ge w$, the interval always contains a multiple of $w$. If $s < w$, it contains one exactly when $(\min(\alpha, \beta) + b) \bmod w$ lies in a set of length $s$, which has probability $s/w$. So $\Pr[h(x) = h(y) \mid a] = \max(0, 1 - s/w)$, and taking the expectation over $a$ gives the lemma. $\square$

**Lemma 2.** $p$ is strictly decreasing on $(0, \infty)$, and with $t = w/u$,
$$p(u) = 1 - 2\Phi(-t) - \frac{2}{\sqrt{2\pi}\,t}\big(1 - e^{-t^2/2}\big).$$

*Proof.* For each value of $Z$, $\max(0, 1 - u|Z|/w)$ is nonincreasing in $u$, and strictly decreasing when $|Z| < w/u$, an event of positive probability. So the expectation is strictly decreasing. For the closed form, $|Z|$ has density $2\varphi(z)$ on $z \ge 0$, with $\varphi(z) = e^{-z^2/2}/\sqrt{2\pi}$, and the integrand is 0 for $z \ge t$. So
$$p(u) = \int_0^t 2\varphi(z)\Big(1 - \frac{z}{t}\Big) dz = \big(2\Phi(t) - 1\big) - \frac{2}{t}\int_0^t z\varphi(z)\,dz = 1 - 2\Phi(-t) - \frac{2}{t}\big(\varphi(0) - \varphi(t)\big),$$
using $\int_0^t z\varphi(z)dz = \varphi(0) - \varphi(t)$ and $2\Phi(t) - 1 = 1 - 2\Phi(-t)$. $\square$

So the family is $(r, cr, p_1, p_2)$-sensitive with $p_1 = p(r) > p_2 = p(cr)$: points within $r$ collide with probability at least $p(r)$, and points beyond $cr$ with probability less than $p(cr)$.

**Theorem.** Let $\rho = \ln(1/p_1)/\ln(1/p_2)$, $k = \lceil \ln n/\ln(1/p_2) \rceil$ and $L = \lceil n^\rho / p_1 \rceil$, and fix $q$ with some $p^* \in P$, $\|q - p^*\| \le r$. Then E2LSH-QUERY$(q, c, r)$ returns a point within $cr$ with probability at least $2/3 - 1/e$, and it never returns a point beyond $cr$.

*Proof.* Only line L6 returns a point, after the test $\|q - x\| \le cr$, so no far point is returned. The $kL$ functions are independent, so for one table $\Pr[g_j(p^*) = g_j(q)] \ge p_1^k$ and $\Pr[g_j(x) = g_j(q)] \le p_2^k \le 1/n$ for each $x$ with $\|q - x\| > cr$.

*Event $E_1$: $p^*$ collides with $q$ in some table.* Since $k < \ln n/\ln(1/p_2) + 1$, $p_1^k \ge p_1 \cdot e^{-\ln n \cdot \ln(1/p_1)/\ln(1/p_2)} = p_1 n^{-\rho}$, so $L p_1^k \ge 1$ and $\Pr[\text{not } E_1] \le (1 - p_1^k)^L \le e^{-L p_1^k} \le 1/e$.

*Event $E_2$: fewer than $3L$ pairs $(j, x)$ with $x$ beyond $cr$ and $g_j(x) = g_j(q)$.* Their expected number is at most $L \cdot n \cdot (1/n) = L$, so by Markov's inequality $\Pr[\text{not } E_2] \le 1/3$.

*Both events give an answer.* If the query returned none, every counted pair failed line L6, so every counted pair is far, and the count stays below $3L$ by $E_2$. Then line L7 never fires, the loop visits all buckets of $q$, and by $E_1$ it meets $p^*$, which passes line L6, a contradiction.

By the union bound, $\Pr[E_1 \cap E_2] \ge 1 - 1/e - 1/3 = 2/3 - 1/e$. $\blacksquare$
