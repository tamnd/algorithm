---
title: Why the weights stay a probability vector, why a heavy component is background, and how long a stationary object takes to become background
proves: [correctness]
status: full
---

Notation as on the page. One pixel has components $(w_k, \mu_k, \sigma_k^2)$, $k = 1, \ldots, K$, with $0 < \alpha < 1$, $0 < T < 1$ and $0 < w_0 < 1$. The claims are about the update rules of lines L1 to L6. They say nothing about whether the background components describe the true background.

## Claim 1: the weights are a probability vector

If $w_k \ge 0$ and $\sum_k w_k = 1$ before an update, the same holds after it.

*Proof.* With a match $m$ (line L3), each new weight $(1 - \alpha) w_k + \alpha [k = m]$ is nonnegative, and their sum is $(1 - \alpha) \sum_k w_k + \alpha = 1$. Without a match (line L2), let $\ell$ be the replaced component and $S = \sum_{k \ne \ell} w_k$. If $S > 0$, each other weight becomes $w_k (1 - w_0) / S \ge 0$, and these sum to $1 - w_0$; with $w_\ell = w_0$ the total is 1. If $S = 0$, the implementation sets each other weight to $(1 - w_0)/(K - 1)$, with the same total. The start state has one weight 1 and the others 0. $\square$

## Claim 2: the means stay in the range of the data

Let $a$ and $b$ be the smallest and the largest value the pixel has shown. Every component with positive weight has $a \le \mu_k \le b$.

*Proof.* A component gets positive weight only when it is created with mean $x$, a shown value, or in the start state with the first value. The mean changes only in line L4, to $(1 - \rho)\mu + \rho x$ with $0 \le \rho \le 1$ (the implementation clamps $\rho$ to 1). A convex combination of two numbers in $[a, b]$ is in $[a, b]$. A component of weight 0 never matches, by line L1, so it never gets weight back except by line L2. $\square$

## Claim 3: a heavy component is background

Let $B$ be defined as in line L5 and let $\pi$ be the order by $w_k / \sigma_k$. If $w_j \ge 1 - T$, then $j$ is one of the first $B$ components.

*Proof.* Let $j$ be at position $p$ of the order. The components before it have total weight at most $1 - w_j \le T$ by Claim 1. So for every $b < p$, the sum $w_{(1)} + \cdots + w_{(b)} \le T$, which is not above $T$. The smallest $b$ with a sum above $T$ is therefore at least $p$, so $B \ge p$ and $j$ is among the first $B$. $\square$

The converse is false. With $T = 0.5$, a narrow component of weight $0.25$ that comes first in the order is background, although $0.25 < 1 - T$. The tests compare the background set with its definition on 500 random mixtures and check Claim 3 on each.

## Claim 4: the weight under repeated matches

If component $j$ has weight $w$ and is the match in $t$ frames in a row, its weight after them is $1 - (1 - w)(1 - \alpha)^t$.

*Proof.* Line L3 gives $w' = (1 - \alpha) w + \alpha$, so $1 - w' = (1 - \alpha)(1 - w)$. By induction on $t$, $1 - w_t = (1 - \alpha)^t (1 - w)$. $\square$

In general, the weight of component $k$ after the frames $1, \ldots, t$ with match indicators $M_1, \ldots, M_t$ is $(1 - \alpha)^t w + \alpha \sum_{s=1}^{t} (1 - \alpha)^{t - s} M_s$, an [exponential moving average](/exponential-moving-average/) of the indicators, as long as no replacement happens.

## Claim 5: the absorption time

Suppose the pixel shows a value $x$ that matches no component, so line L2 creates a component $j$ with weight $w_0$, and then $x$ matches $j$ in every frame (this holds, for example, if the pixel keeps the value $x$ and $x$ is farther than $2.5 \sigma_k$ from every other component). Let

$$t^* = \left\lceil \frac{\ln\big(T / (1 - w_0)\big)}{\ln(1 - \alpha)} \right\rceil.$$

Then the pixel is background in frame $t^*$ after the creation and in every later frame of the run. If, in addition, the components before $j$ in the order have total weight $1 - w_j$, then $t^*$ is the first such frame.

*Proof.* Assume $1 - w_0 > T$; otherwise $t^* \le 0$ and Claim 3 applies at once. By Claim 4 with $w = w_0$, after $t$ matches $1 - w_j = (1 - w_0)(1 - \alpha)^t$. This is at most $T$ if and only if $(1 - \alpha)^t \le T / (1 - w_0)$. Taking logarithms, and dividing by $\ln(1 - \alpha) < 0$, which turns the inequality around, gives $t \ge \ln(T / (1 - w_0)) / \ln(1 - \alpha)$, so the condition holds from $t = t^*$ on, since $1 - w_j$ decreases in $t$. Then $w_j \ge 1 - T$, and by Claim 3 the match $j$ is among the first $B$, so line L6 says background.

For the second sentence: if the components before $j$ have total weight $1 - w_j$, then for $t < t^*$ that total is above $T$, so $B$ ends before $j$ and the pixel is foreground. $\square$

With $\alpha = 0.01$, $T = 0.7$ and $w_0 = 0.05$, $\ln(0.7 / 0.95) / \ln(0.99) = 30.39$, so $t^* = 31$. In the example of the page the old background component has weight $0.95 \cdot 0.99^t$ and comes first, because its $\sigma$ is small, and the third component has weight 0. So the second sentence applies, and the pixel turns to background at exactly $t = 31$. The tests check this.

## Claim 6: cost of one update

Line L1 sorts $K$ numbers and scans them, line L3 changes $K$ weights, line L4 is constant work, and line L5 sorts again and scans. So one update costs $O(K \log K)$ operations, with the exponential and the square root at unit cost. $\square$
