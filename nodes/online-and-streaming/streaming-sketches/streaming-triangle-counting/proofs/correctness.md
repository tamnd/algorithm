---
title: Correctness of neighborhood sampling for triangle counting
proves: [correctness]
status: full
---

We prove that one estimator of neighborhood sampling (lines L1 to L7 of the page) is unbiased for the number $T$ of triangles, we compute its second moment exactly, and we bound the number of estimators that line L8 needs for an $(\varepsilon, \delta)$ estimate.

**Setting.** The stream is $e_1, \ldots, e_m$, the distinct edges of a simple graph $G$ in some order. For $j \in [m]$ let $N(e_j) = \{e_k : k > j,\ e_k \cap e_j \ne \emptyset\}$ and $c_j = |N(e_j)|$. For a triangle $\tau$ of $G$, let $f_1(\tau), f_2(\tau), f_3(\tau)$ be its three edges in stream order. Let $C = \max_j c_j$. Each call $\mathrm{coin}(p)$ returns true with probability $p$, independently of all other calls. At the end of the stream, $i = m$, and the estimate is $X = m \cdot c$ if found is true, and $X = 0$ otherwise.

## The first reservoir

For $j \in [m]$, let $A_j$ be the event that line L2 resets the state at step $j$ and at no later step. At the end, $r_1 = e_j$ exactly on $A_j$, and the events $A_1, \ldots, A_m$ are disjoint and cover all outcomes, because step 1 always resets.

**Lemma 1.** $\Pr[A_j] = 1/m$ for every $j$.

*Proof.* At step $k$ the reset happens with probability $1/k$, independently of earlier steps, and with probability 1 at $k = 1$. So
$$\Pr[A_j] = \frac{1}{j} \prod_{k=j+1}^{m} \left(1 - \frac{1}{k}\right) = \frac{1}{j} \prod_{k=j+1}^{m} \frac{k-1}{k} = \frac{1}{j} \cdot \frac{j}{m} = \frac{1}{m}. \qquad \square$$

## The second reservoir

**Lemma 2.** Given $A_j$, at the end $c = c_j$, and if $c_j \ge 1$ then $r_2$ is uniform over $N(e_j)$.

*Proof.* On $A_j$, step $j$ sets $r_1 = e_j$, $r_2 = \text{none}$, $c = 0$, and no later step resets. So each later edge $e_k$ reaches line L3 with $r_1 = e_j$, and it passes the test of L3 exactly when $e_k \in N(e_j)$. Let $g_1, \ldots, g_{c_j}$ be the edges of $N(e_j)$ in stream order. Line L5 runs once for each of them, so at the end $c = c_j$, and when $g_t$ arrives, line L6 runs with $c = t$. The coins of line L6 are independent of the coins of line L2, so conditioning on $A_j$ does not change them. Line L6 sets $r_2 = g_t$ with probability $1/t$, and $r_2$ keeps this value exactly when no later coin of line L6 is true. Hence
$$\Pr[r_2 = g_t \mid A_j] = \frac{1}{t} \prod_{u=t+1}^{c_j} \left(1 - \frac{1}{u}\right) = \frac{1}{t} \cdot \frac{t}{c_j} = \frac{1}{c_j}. \qquad \square$$

## When the flag is true

For two edges $a, b$ that share exactly one vertex, write $h(a, b)$ for the third edge of the triangle on $a \cup b$, which may or may not be in $G$.

**Lemma 3.** Given $A_j$ and $r_2 = g_t$ at the end, found is true at the end if and only if $h(e_j, g_t)$ is an edge of the stream that arrives after $g_t$.

*Proof.* Write $h = h(e_j, g_t)$. Say $e_j = \{a, x\}$ and $g_t = \{a, y\}$, so $h = \{x, y\}$. The edges are distinct, so $x \ne y$ and $h$ is a valid pair.

Consider the step at which $g_t$ arrives. Line L6 sets $r_2 = g_t$ and found to false at this step, because $r_2 = g_t$ at the end and $g_t$ arrives only once. After this step, $r_2$ does not change, and no step resets, by $A_j$. So after this step found changes only at line L4, and line L4 sets it to true exactly at a step whose edge is $h(r_1, r_2) = h$.

If $h$ arrives after $g_t$, then $h$ shares the vertex $x$ with $e_j$, so it passes line L3, and line L4 sets found to true. Nothing later sets found to false: line L6 at the step of $h$ or later would change $r_2$, which does not happen, and line L2 does not reset. So found is true at the end.

If $h$ does not arrive after $g_t$, then no step after $g_t$ has the edge $h$, since each edge arrives at most once. So found stays false from the step of $g_t$ to the end. $\square$

**Lemma 4.** For a triangle $\tau$ let $E_\tau$ be the event that at the end $r_1 = f_1(\tau)$ and $r_2 = f_2(\tau)$. Then found is true at the end if and only if $E_\tau$ holds for some triangle $\tau$. The events $E_\tau$ are pairwise disjoint, and $\Pr[E_\tau] = 1/(m\,c(f_1(\tau)))$, where $c(e_j) = c_j$.

*Proof.* Suppose found is true at the end, with $r_1 = e_j$ and $r_2 = g_t$. Then $r_2$ is not none, so $g_t \in N(e_j)$ exists. By Lemma 3, $h = h(e_j, g_t)$ is in the stream and arrives after $g_t$, which arrives after $e_j$. So $\tau = \{e_j, g_t, h\}$ is a triangle with $f_1(\tau) = e_j$ and $f_2(\tau) = g_t$, and $E_\tau$ holds.

Conversely, let $\tau$ be a triangle and suppose $E_\tau$ holds. Then $f_2(\tau)$ and $f_3(\tau)$ arrive after $f_1(\tau)$ and touch it, so $f_2(\tau) \in N(f_1(\tau))$, and $h(f_1(\tau), f_2(\tau)) = f_3(\tau)$ arrives after $f_2(\tau)$. By Lemma 3, found is true at the end.

Two edges that share a vertex span three vertices, so the pair $(f_1(\tau), f_2(\tau))$ determines $\tau$. So different triangles give different pairs, and the events $E_\tau$ are disjoint. Finally, if $f_1(\tau) = e_j$, then $c_j \ge 1$ and, by Lemmas 1 and 2, $\Pr[E_\tau] = \Pr[A_j] \cdot \Pr[r_2 = f_2(\tau) \mid A_j] = \frac{1}{m} \cdot \frac{1}{c_j}$. $\square$

## Expectation and variance

**Theorem 1 (unbiased).** $\mathbb{E}[X] = T$.

*Proof.* By Lemma 4, $X = 0$ outside the disjoint union of the events $E_\tau$, and on $E_\tau$, by Lemma 2, $X = m \cdot c(f_1(\tau))$. Hence
$$\mathbb{E}[X] = \sum_{\tau} \Pr[E_\tau] \cdot m\,c(f_1(\tau)) = \sum_{\tau} \frac{m\,c(f_1(\tau))}{m\,c(f_1(\tau))} = T. \qquad \square$$

**Theorem 2 (variance).** $\mathbb{E}[X^2] = \sum_\tau m\,c(f_1(\tau))$, and $\mathrm{Var}[X] \le mCT - T^2 \le mCT$. Moreover $C \le 2(\Delta - 1)$, where $\Delta$ is the largest degree of $G$.

*Proof.* In the same way,
$$\mathbb{E}[X^2] = \sum_\tau \frac{(m\,c(f_1(\tau)))^2}{m\,c(f_1(\tau))} = \sum_\tau m\,c(f_1(\tau)) \le mCT,$$
and $\mathrm{Var}[X] = \mathbb{E}[X^2] - T^2$. An edge $\{u, v\}$ of a simple graph shares a vertex with at most $(\deg u - 1) + (\deg v - 1) \le 2(\Delta - 1)$ other edges, so $C \le 2(\Delta - 1)$. $\square$

On the worked example of the page, the two triangles have $c(f_1) = 3$, so $\mathbb{E}[X^2] = 6 \cdot 3 + 6 \cdot 3 = 36$ and $\mathrm{Var}[X] = 32$, which the tests confirm by exact enumeration of all coin flips.

## The number of estimators

**Theorem 3.** Let $\hat T$ be the mean of $s$ independent estimators (line L8), and let $0 < \varepsilon, \delta < 1$. If $T = 0$, then $\hat T = 0$ always. If $T \ge 1$ and $s \ge mC/(\varepsilon^2 \delta T)$, then $\Pr[|\hat T - T| > \varepsilon T] \le \delta$.

*Proof.* If $T = 0$, there is no triangle, so by Lemma 4 found is false at the end of every estimator and $\hat T = 0$. If $T \ge 1$, then by Theorem 1 $\mathbb{E}[\hat T] = T$, and by independence and Theorem 2 $\mathrm{Var}[\hat T] = \mathrm{Var}[X]/s \le mCT/s$. By Chebyshev's inequality,
$$\Pr[|\hat T - T| > \varepsilon T] \le \frac{mCT}{s\,\varepsilon^2 T^2} = \frac{mC}{s\,\varepsilon^2 T} \le \delta. \qquad \square$$

**Corollary (median of means).** Let $s_0 = \lceil 4mC/(\varepsilon^2 T) \rceil$ and $k = \lceil 8 \ln(1/\delta) \rceil$. Run $k$ independent groups of $s_0$ estimators and output the median of the $k$ group means. Then the output is within $\varepsilon T$ of $T$ with probability at least $1 - \delta$, with $k s_0 = O((mC/(\varepsilon^2 T)) \log(1/\delta))$ estimators.

*Proof.* By Theorem 3 with $\delta = 1/4$, each group mean is outside $[(1 - \varepsilon)T, (1 + \varepsilon)T]$ with probability at most $1/4$, independently of the other groups. If the median is outside this interval, then at least $k/2$ group means are outside it. The number $B$ of such groups is a sum of $k$ independent indicators with mean at most $k/4$, so by Hoeffding's inequality $\Pr[B \ge k/2] \le \exp(-2k(1/4)^2) = \exp(-k/8) \le \delta$. $\square$

**Space.** Each estimator stores $i$, $r_1$, $r_2$, $c$ and one bit, which is $O(1)$ words, so the algorithm uses $O(s)$ words, and $O((mC/(\varepsilon^2 T)) \log(1/\delta))$ words with the corollary. $\blacksquare$
