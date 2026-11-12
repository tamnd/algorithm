---
title: The largest share on a consistent hashing ring, with one point and with v points per server
proves: [correctness]
status: full
---

**Model.** The ring is the circle $[0, 1)$ of length 1. There are $n \ge 1$ servers, and server $s$ has $v \ge 1$ points. All $N = nv$ points are independent and uniform on the circle. A key goes to the first point at or after it in the clockwise direction, so each point *owns* the arc from the point before it up to itself. The *share* $A_s$ of server $s$ is the total length of the arcs of its points. The shares add up to 1, and the average share is $1/n$. Let $H_n = \sum_{k=1}^n 1/k$ and $(y)_+ = \max(y, 0)$.

**Statement.**

(a) *One point per server* ($v = 1$, $n \ge 2$). Let $L = \max_s A_s$ be the largest arc. For $x \ge 0$,
$$ \Pr[L > x] = \sum_{k=1}^{n} (-1)^{k+1}\binom nk (1 - kx)_+^{\,n-1}, \qquad \Pr\bigl[\min_s A_s > x\bigr] = (1 - nx)_+^{\,n-1}, $$
so $\mathbb E[L] = H_n/n$ and $\mathbb E[\min_s A_s] = 1/n^2$. For each $c > 0$ and each $0 < \epsilon < 1$,
$$ \Pr\Bigl[L > \frac{(1+c)\ln n}{n-1}\Bigr] \le n^{-c}, \qquad \Pr\Bigl[L \le \frac{(1-\epsilon)\ln n}{n}\Bigr] \le e\,n^{-\epsilon}. $$

(b) *$v$ points per server.* For each $0 < \delta < 1$,
$$ \Pr\Bigl[\text{some } A_s \notin \Bigl[\frac{1-\delta}{(1+\delta)n}, \frac{1+\delta}{(1-\delta)n}\Bigr]\Bigr] \le 2n\,e^{-v\delta^2/4}. $$
In particular, for $c > 0$ and $v \ge 16\ln(2n^{c+1})$, put $\delta = 2\sqrt{\ln(2n^{c+1})/v} \le 1/2$. Then with probability at least $1 - n^{-c}$ every share lies in $[(1 - 2\delta)/n, (1 + 4\delta)/n]$.

(c) *Keys.* Let $m$ keys have independent uniform positions, independent of the points. If all shares are at most $\alpha/n$, then for $0 < \epsilon \le 1$ the probability, over the keys, that some server gets at least $(1+\epsilon)\alpha m/n$ keys is at most $n\,e^{-\epsilon^2 m/(3n)}$. So if $v \ge (4/\delta^2)\ln(2n^{c+1})$ and $m \ge 3(c+1)n\ln n/\epsilon^2$, then every server gets at most $(1+\epsilon)\frac{1+\delta}{1-\delta}\cdot\frac mn$ keys with probability at least $1 - 2n^{-c}$.

## Lemma 1 (labeled gaps are uniform on the simplex)

Let $N \ge 2$ points $P_1, \ldots, P_N$ be independent and uniform on the circle, and let $D_j$ be the length of the arc owned by $P_j$. Then $(D_1, \ldots, D_N)$ is uniform on the simplex $\Delta_N = \{d \in \mathbb R^N : d_j \ge 0, \sum_j d_j = 1\}$: the vector $(D_1, \ldots, D_{N-1})$ has the constant density $(N-1)!$ on $\{d_j > 0, \sum_{j < N} d_j < 1\}$, and $D_N = 1 - \sum_{j<N} D_j$. Moreover the circular order of the labels is independent of $(D_1, \ldots, D_N)$.

*Proof.* The arc lengths do not change when all points turn by the same angle. Turn by $-P_1$. For a fixed $u$, the variables $(P_j - u) \bmod 1$ for $j \ge 2$ are independent and uniform, and they do not depend on $u$ in law, so after the turn $P_1 = 0$ and $Y_j = (P_j - P_1) \bmod 1$, $j = 2, \ldots, N$, are independent and uniform on $[0, 1)$, independent of $P_1$.

Let $Y_{(1)} < \cdots < Y_{(N-1)}$ be the sorted values (ties have probability 0). Their joint density is $(N-1)!$ on $\{0 < y_1 < \cdots < y_{N-1} < 1\}$. Put $S_1 = Y_{(1)}$, $S_j = Y_{(j)} - Y_{(j-1)}$ for $2 \le j \le N-1$, and $S_N = 1 - Y_{(N-1)}$. The map from $(y_1, \ldots, y_{N-1})$ to $(s_1, \ldots, s_{N-1})$ is linear and triangular with ones on the diagonal, so its determinant is 1, and it maps the ordered region onto $\{s_j > 0, \sum_{j<N} s_j < 1\}$. So $(S_1, \ldots, S_{N-1})$ has the constant density $(N-1)!$, that is, $S$ is uniform on $\Delta_N$. This law does not change when the coordinates are permuted, because a permutation of coordinates maps $\Delta_N$ onto itself and preserves volume.

The arc $S_j$ for $j \le N-1$ ends at the point of rank $j$ among $P_2, \ldots, P_N$, and $S_N$ ends at $P_1 = 0$. The ranks of the independent and identically distributed $Y_2, \ldots, Y_N$ form a uniform random permutation $\pi$ that is independent of the sorted values, so $\pi$ is independent of $S$. The labeled vector $D$ is $S$ with its coordinates permuted by $\pi$. Given $\pi$, it is a fixed permutation of a uniform vector on $\Delta_N$, so it is uniform on $\Delta_N$ whatever $\pi$ is. Hence $D$ is uniform on $\Delta_N$ and independent of $\pi$, and $\pi$ fixes the circular order. $\square$

## Lemma 2 (several long arcs at once)

In the setting of Lemma 1, let $K$ be a set of $k$ labels and $x \ge 0$. Then $\Pr[D_j > x \text{ for all } j \in K] = (1 - kx)_+^{\,N-1}$.

*Proof.* If $kx \ge 1$, the event needs $\sum_{j \in K} D_j > 1$, which is impossible, so the probability is 0. Let $kx < 1$ and write $\mathbf 1_K$ for the indicator vector of $K$. The map $d \mapsto d' = (d - x\mathbf 1_K)/(1 - kx)$ sends the event set $\{d \in \Delta_N : d_j > x \text{ for } j \in K\}$ one to one onto $\{d' \in \Delta_N : d'_j > 0 \text{ for } j \in K\}$, because $\sum_j d'_j = (1 - kx)/(1 - kx) = 1$. The image differs from $\Delta_N$ only by a set of volume 0. In the coordinates $d_1, \ldots, d_{N-1}$ the map is a translation followed by a scaling by $1/(1 - kx)$, so it multiplies $(N-1)$-dimensional volume by $(1 - kx)^{-(N-1)}$. Under the uniform law the event therefore has probability $(1 - kx)^{N-1}$. $\square$

## Proof of (a)

With $v = 1$ the shares are the $n$ arcs $D_1, \ldots, D_n$ of Lemma 1 with $N = n$.

*Exact law.* $\{L > x\} = \bigcup_j \{D_j > x\}$. By inclusion and exclusion, and by Lemma 2 for each of the $\binom nk$ sets of size $k$,
$$ \Pr[L > x] = \sum_{k=1}^n (-1)^{k+1} \sum_{|K| = k} \Pr\Bigl[\bigcap_{j \in K}\{D_j > x\}\Bigr] = \sum_{k=1}^n (-1)^{k+1}\binom nk (1 - kx)_+^{\,n-1}. $$
The smallest arc exceeds $x$ exactly when all $n$ arcs do, so Lemma 2 with $K$ the full set gives $(1 - nx)_+^{\,n-1}$.

*Means.* $L$ takes values in $[0, 1]$, so $\mathbb E[L] = \int_0^1 \Pr[L > x]\,dx$. Since $\int_0^{1/k}(1 - kx)^{n-1}dx = 1/(kn)$,
$$ \mathbb E[L] = \frac 1n \sum_{k=1}^n (-1)^{k+1}\binom nk \frac 1k. $$
This sum is $H_n$. Indeed $1 - (1-t)^n = \sum_{k=1}^n (-1)^{k+1}\binom nk t^k$ by the binomial theorem, and also $1 - (1-t)^n = t\sum_{j=0}^{n-1}(1-t)^j$ by the geometric sum with ratio $1 - t$. Divide both by $t$ and integrate over $[0, 1]$: the first form gives $\sum_k (-1)^{k+1}\binom nk/k$ and the second gives $\sum_{j=0}^{n-1} 1/(j+1) = H_n$. So $\mathbb E[L] = H_n/n$. In the same way $\mathbb E[\min_s A_s] = \int_0^{1/n}(1 - nx)^{n-1}dx = 1/n^2$.

*Upper bound.* By the [union bound](/union-bound/) and Lemma 2 with $k = 1$, $\Pr[L > x] \le n(1-x)_+^{\,n-1} \le n\,e^{-x(n-1)}$, since $1 - x \le e^{-x}$. With $x = (1+c)\ln n/(n-1)$ the right side is $n \cdot n^{-(1+c)} = n^{-c}$.

*Lower bound.* Fix $0 \le x < 1$ and let $X = \sum_{j=1}^n [D_j > x]$ count the arcs longer than $x$. Then $\{L \le x\} = \{X = 0\}$. By Lemma 2, $\mathbb E[X] = n(1-x)^{n-1}$ and
$$ \mathbb E[X^2] = \mathbb E[X] + \sum_{i \ne j}\Pr[D_i > x, D_j > x] = \mathbb E[X] + n(n-1)(1 - 2x)_+^{\,n-1}. $$
Since $(1-x)^2 - (1 - 2x) = x^2 \ge 0$, we have $0 \le (1-2x)_+ \le (1-x)^2$, so the last term is at most $n^2(1-x)^{2(n-1)} = \mathbb E[X]^2$ and $\mathrm{Var}[X] \le \mathbb E[X]$. By [Chebyshev's inequality](/chebyshev-inequality/),
$$ \Pr[X = 0] \le \Pr\bigl[|X - \mathbb E X| \ge \mathbb E X\bigr] \le \frac{\mathrm{Var}[X]}{(\mathbb E X)^2} \le \frac{1}{n(1-x)^{n-1}}. \tag{1} $$
Now let $x = \ell = (1-\epsilon)\ln n/n$ with $0 < \epsilon < 1$ and $n \ge 2$. Then $\ell \le \ln n/n \le 1/e < 1/2$. For $0 \le \ell \le 1/2$, $-\ln(1 - \ell) = \ell + \sum_{k \ge 2}\ell^k/k \le \ell + \frac{\ell^2}{2}\sum_{j \ge 0}\ell^j = \ell + \frac{\ell^2}{2(1-\ell)} \le \ell + \ell^2$. So $(1-\ell)^{n-1} \ge (1-\ell)^n \ge e^{-n\ell - n\ell^2}$. Here $n\ell = (1-\epsilon)\ln n$ and $n\ell^2 \le (\ln n)^2/n \le 4/e^2 < 1$, because $(\ln y)^2/y$ has its maximum $4/e^2$ at $y = e^2$. Hence $n(1-\ell)^{n-1} \ge n \cdot n^{-(1-\epsilon)}e^{-1} = n^{\epsilon}/e$, and (1) gives $\Pr[L \le \ell] \le e\,n^{-\epsilon}$. $\square$

## Lemma 3 (exponential representation)

Let $E_1, \ldots, E_N$ be independent with the exponential law of mean 1, and $T = \sum_j E_j$. Then $(E_1/T, \ldots, E_N/T)$ is uniform on $\Delta_N$ and independent of $T$.

*Proof.* The density of $(E_1, \ldots, E_N)$ is $e^{-(e_1 + \cdots + e_N)}$ on the positive orthant. Change variables to $t = \sum_j e_j$ and $w_j = e_j/t$ for $j < N$. The inverse is $e_j = t w_j$ for $j < N$ and $e_N = t(1 - \sum_{j<N} w_j)$. In the Jacobian matrix, row $j < N$ has $t$ in column $w_j$ and $w_j$ in column $t$; row $N$ has $-t$ in each column $w_k$ and $1 - \sum w_j$ in column $t$. Adding rows $1, \ldots, N-1$ to row $N$ turns row $N$ into $(0, \ldots, 0, 1)$, so the determinant is $t^{N-1}$. The density of $(w, t)$ is $e^{-t}t^{N-1}$ on $\{t > 0\} \times \{w_j > 0, \sum_{j<N} w_j < 1\}$. It is a product of a function of $t$ and a constant in $w$, so $w$ is uniform on the simplex and independent of $t$. $\square$

## Lemma 4 (tails of a sum of exponentials)

Let $G$ be the sum of $v$ independent exponential variables of mean 1, and $0 < \delta < 1$. Then
$$ \Pr[G \ge (1+\delta)v] \le e^{-v(\delta - \ln(1+\delta))} \le e^{-v\delta^2/4}, \qquad \Pr[G \le (1-\delta)v] \le e^{-v(-\delta - \ln(1-\delta))} \le e^{-v\delta^2/2}. $$

*Proof.* For $\lambda < 1$, $\mathbb E[e^{\lambda E}] = \int_0^\infty e^{(\lambda - 1)y}dy = 1/(1 - \lambda)$, so $\mathbb E[e^{\lambda G}] = (1-\lambda)^{-v}$. By [Markov's inequality](/markov-inequality/) on $e^{\lambda G}$ with $\lambda = \delta/(1+\delta)$, $\Pr[G \ge (1+\delta)v] \le e^{-\lambda(1+\delta)v}(1-\lambda)^{-v} = e^{-\delta v}(1+\delta)^v$. On $e^{-\lambda G}$ with $\lambda = \delta/(1-\delta)$, $\Pr[G \le (1-\delta)v] \le e^{\lambda(1-\delta)v}(1+\lambda)^{-v} = e^{\delta v}(1-\delta)^v$. These are the first inequalities.

For the second ones, let $f(\delta) = \delta - \ln(1+\delta) - \delta^2/(2(1+\delta))$. Then $f(0) = 0$ and $f'(\delta) = \delta/(1+\delta) - (2\delta + \delta^2)/(2(1+\delta)^2) = \delta^2/(2(1+\delta)^2) \ge 0$, so $\delta - \ln(1+\delta) \ge \delta^2/(2(1+\delta)) \ge \delta^2/4$ for $\delta \le 1$. And $-\delta - \ln(1-\delta) = \sum_{k \ge 2}\delta^k/k \ge \delta^2/2$. $\square$

## Proof of (b)

By Lemma 1 (with $N = nv$) and Lemma 3, we may take the arcs owned by the labeled points to be $E_j/T$, with $E_1, \ldots, E_N$ independent exponential variables of mean 1 and $T = \sum_j E_j$. Then $A_s = G_s/T$, where $G_s$ is the sum of the $v$ variables $E_j$ of the points of server $s$. The $G_s$ are sums over disjoint sets of indices, and $T = \sum_s G_s$.

Suppose that $(1-\delta)v \le G_s \le (1+\delta)v$ for every $s$. Adding over the $n$ servers gives $(1-\delta)nv \le T \le (1+\delta)nv$, so
$$ \frac{1-\delta}{(1+\delta)n} \le A_s = \frac{G_s}{T} \le \frac{1+\delta}{(1-\delta)n} \quad\text{for every } s. $$
So a share leaves the window only if some $G_s$ leaves $[(1-\delta)v, (1+\delta)v]$. By Lemma 4 and the union bound over the $n$ servers, this has probability at most $n(e^{-v\delta^2/4} + e^{-v\delta^2/2}) \le 2n\,e^{-v\delta^2/4}$.

For the second sentence, $v \ge 16\ln(2n^{c+1})$ gives $\delta = 2\sqrt{\ln(2n^{c+1})/v} \le 1/2$, and $2n\,e^{-v\delta^2/4} = 2n\,e^{-\ln(2n^{c+1})} = n^{-c}$. For $0 < \delta \le 1/2$, $\frac{1+\delta}{1-\delta} = 1 + \frac{2\delta}{1-\delta} \le 1 + 4\delta$ and $\frac{1-\delta}{1+\delta} = 1 - \frac{2\delta}{1+\delta} \ge 1 - 2\delta$. $\square$

## Proof of (c)

Fix the points, and so the shares. Each key lands in the region of server $s$ with probability $A_s$, independently of the other keys, so the number of keys of server $s$ is binomial with parameters $m$ and $A_s$. If $\alpha/n \ge 1$, the claim holds because no server has more than $m$ keys. Otherwise, write the position test of key $j$ as $[U_j < A_s]$ with $U_j$ independent and uniform; since $A_s \le \alpha/n$, the count is at most $Z = \sum_j [U_j < \alpha/n]$, which is binomial with mean $\alpha m/n$. The [Chernoff bound](/chernoff-bound/) for $0 < \epsilon \le 1$ gives $\Pr[Z \ge (1+\epsilon)\alpha m/n] \le e^{-\epsilon^2\alpha m/(3n)}$. The largest share is at least the average $1/n$, so $\alpha \ge 1$, and the union bound over the $n$ servers gives at most $n\,e^{-\epsilon^2 m/(3n)}$.

With $m \ge 3(c+1)n\ln n/\epsilon^2$ this is at most $n \cdot n^{-(c+1)} = n^{-c}$. With $v \ge (4/\delta^2)\ln(2n^{c+1})$, part (b) gives $\alpha = (1+\delta)/(1-\delta)$ except with probability $2n\,e^{-v\delta^2/4} \le n^{-c}$. The two failure events together have probability at most $2n^{-c}$. $\square$

## Remark: the closest point rule

Karger et al. send an item to the closest point, not to the next point clockwise. On the circle, a point then owns half of the arc before it and half of the arc after it, so $A_s = (G_s + G'_s)/(2T)$, where $G'_s$ is the sum of the variables $E_j$ of the arcs that follow the points of $s$. Each arc follows exactly one point, so $G'_s$ is a sum of $v$ distinct $E_j$. By Lemma 1 the circular order is independent of the arcs, so given the order, $G'_s$ is again a sum of $v$ independent exponential variables. If every $G_s$ and every $G'_s$ lies in $[(1-\delta)v, (1+\delta)v]$, then $T$ and each $A_s$ lie in the same windows as above. The union bound over $2n$ sums gives the failure probability $4n\,e^{-v\delta^2/4}$. The unit interval of Karger et al. has two end pieces without wrap-around; this proof does not treat them.
