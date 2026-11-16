---
title: Correctness of semi-global matching
proves: [correctness]
status: full
---

Semi-global matching does not claim to minimize the two-dimensional energy. What we prove is that it computes what it is defined to compute: for each direction $r$ and pixel $p$, the path cost $L_r(p, \cdot)$ equals, up to a constant that does not depend on $d$, the least energy of a disparity sequence along the ray that ends at $p$ with disparity $d$; and its values stay in $[C(p, d), C(p, d) + P_2]$. Then $S$ and the winner-takes-all step are plain sums and minima.

## Setup

The cost volume gives $C(p, d) \ge 0$ for $d \in \{0, \dots, D - 1\}$. Fix a direction $r$ and a pixel $p$. Walking back from $p$ by $-r$ until the next step would leave the image gives the ray $p_0, p_1, \dots, p_t = p$ with $p_{s} = p_{s-1} + r$. Define the jump cost $V(a, b) = 0$ if $a = b$, $\min(P_1, P_2)$ if $|a - b| = 1$, and $P_2$ otherwise, with $P_1, P_2 \ge 0$. (With the usual choice $P_2 \ge P_1$ this is $P_1$ for a jump of one.) The chain energy of a sequence $d_0, \dots, d_t$ is

$$E_t(d_0, \dots, d_t) = \sum_{s=0}^{t} C(p_s, d_s) + \sum_{s=1}^{t} V(d_{s-1}, d_s),$$

and $\tilde L(p, d)$ is its least value over all sequences with $d_t = d$.

## Lemma 1 (the recursion without subtraction)

$\tilde L(p_0, d) = C(p_0, d)$, and for $s \ge 1$

$$\tilde L(p_s, d) = C(p_s, d) + \min_{k} \big(\tilde L(p_{s-1}, k) + V(k, d)\big).$$

*Proof.* A sequence ending with $d$ at $p_s$ is a sequence ending with some $k$ at $p_{s-1}$, followed by the jump from $k$ to $d$ and the cost $C(p_s, d)$. The best choice of the earlier part, for a fixed $k$, has energy $\tilde L(p_{s-1}, k)$. Take the least value over $k$. $\square$

## Lemma 2 (the four candidates)

For any vector $x$ over the disparities with $m = \min_k x_k$,

$$\min_k \big(x_k + V(k, d)\big) = \min\big(x_d,\ x_{d-1} + P_1,\ x_{d+1} + P_1,\ m + P_2\big),$$

where the terms $x_{d \pm 1}$ are left out if the index is outside the range.

*Proof.* Call the two sides $A$ and $B$. The terms of $A$ are $x_d$ for $k = d$, $x_{d \pm 1} + \min(P_1, P_2)$ for $k = d \pm 1$, and $x_k + P_2$ for the other $k$.

$B \le A$: each term of $A$ is at least some term of $B$. $x_d$ is a term of $B$. If $P_1 \le P_2$, then $x_{d \pm 1} + \min(P_1, P_2) = x_{d \pm 1} + P_1$; otherwise it is $x_{d \pm 1} + P_2 \ge m + P_2$. And $x_k + P_2 \ge m + P_2$.

$A \le B$: each term of $B$ is at least some term of $A$. $x_d$ is a term of $A$. $x_{d \pm 1} + P_1 \ge x_{d \pm 1} + \min(P_1, P_2)$. Finally, let $k^*$ attain $m$; since $V(k^*, d) \le P_2$, the term $x_{k^*} + V(k^*, d)$ of $A$ is at most $m + P_2$. $\square$

## Lemma 3 (the subtraction only shifts)

Let $L_r$ be computed by the algorithm, with $m_s = \min_k L_r(p_s, k)$. Then for all $s$ and $d$,

$$L_r(p_s, d) = \tilde L(p_s, d) - \sum_{s' < s} m_{s'}.$$

*Proof.* By induction on $s$. For $s = 0$ both sides are $C(p_0, d)$ (line L4). For $s \ge 1$, line L6 computes $C(p_s, d) + \min(\dots) - m_{s-1}$, where by Lemma 2 the minimum equals $\min_k (L_r(p_{s-1}, k) + V(k, d))$. By the induction hypothesis $L_r(p_{s-1}, \cdot)$ is $\tilde L(p_{s-1}, \cdot)$ minus a constant $c_{s-1} = \sum_{s' < s-1} m_{s'}$, and a constant shift passes through the minimum. With Lemma 1,

$$L_r(p_s, d) = C(p_s, d) + \min_k\big(\tilde L(p_{s-1}, k) + V(k, d)\big) - c_{s-1} - m_{s-1} = \tilde L(p_s, d) - \sum_{s' < s} m_{s'}. \qquad \square$$

So for each pixel and direction, $L_r(p, \cdot)$ and the exact chain minimum $\tilde L(p, \cdot)$ differ by a constant, and they have the same order over $d$. The code visits rows in the order of the sign of the row step of $r$ and columns in the order of the sign of its column step; then $p - r$ is visited before $p$, so line L6 reads a final value. The test file checks Lemma 3 against brute force over all sequences on small rays, for all 16 directions.

## Lemma 4 (bounds)

For all $p$ and $d$, $C(p, d) \le L_r(p, d) \le C(p, d) + P_2$. In particular $0 \le L_r(p, d) \le C_{\max} + P_2$, where $C_{\max}$ is the largest cost.

*Proof.* At the first pixel of a ray, $L_r = C$. Otherwise, with $x = L_r(p - r, \cdot)$ and $m = \min x$, the value added to $C(p, d)$ is $\min(x_d, x_{d \pm 1} + P_1, m + P_2) - m$. Every candidate is at least $m$, because $P_1, P_2 \ge 0$, so the value is at least 0. The last candidate is $m + P_2$, so the value is at most $P_2$. $\square$

This is the bound $L \le C_{\max} + P_2$ that Hirschmüller (2008) gives. It means that the path costs fit in a fixed number of bits, however long the path is.

## The output

Line L7 adds $L_r(p, d)$ over the directions, and line L8 takes the least $d$ with the least sum. Both are exact. By Lemmas 3 and 4, $S(p, d) = \sum_r \tilde L_r(p, d) - K(p)$ with $K(p)$ independent of $d$, so the winner-takes-all choice is the $d$ that minimizes the sum over the directions of the exact chain minima ending at $p$ with disparity $d$. Since each $C(p, d)$ appears once in every $\tilde L_r(p, d)$, this sum counts the data cost of $p$ itself $|R|$ times; this is part of the definition of the method and does not change with the subtraction.

## Cost

For each direction, each of the $W H$ pixels takes one minimum over $D$ values and $D$ updates with four candidates, which is $O(D)$. So the path costs of $|R|$ directions take $\Theta(W H D |R|)$ time, and the sum $S$ needs $\Theta(W H D)$ memory. $\square$
