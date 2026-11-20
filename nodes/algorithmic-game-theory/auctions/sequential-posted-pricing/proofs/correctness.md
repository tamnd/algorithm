---
title: Correctness and the revenue guarantee of sequential posted pricing
proves: [correctness]
status: full
---

There are $n$ bidders with independent values, and bidder $i$ has a discrete distribution $F_i$. For a price $s$ in the support of $F_i$ write $q_i(s) = \Pr[v_i \ge s]$. The revenue curve of bidder $i$ is the set of points $(0, 0)$ and $(q_i(s), s\, q_i(s))$, and $\bar R_i$ is the least concave function on $[0, 1]$ above these points. The ex ante relaxation is

$$\mathrm{EAR} = \max \Bigl\{ \sum_i \bar R_i(q_i) : \sum_i q_i \le 1,\ 0 \le q_i \le 1 \Bigr\}.$$

## Claim 1: lines L1 to L4 solve the ex ante relaxation

Line L1 computes the vertices of each $\bar R_i$ by the monotone chain method, as in [ironing](/ironing/). The function $\bar R_i$ is piecewise linear with nonincreasing slopes, and $\bar R_i(0) = 0$. So $\bar R_i(q_i)$ is the largest total of $\sum_k m_{ik} t_{ik}$ over amounts $0 \le t_{ik} \le \ell_{ik}$ with $\sum_k t_{ik} = q_i$, where segment $k$ of bidder $i$ has slope $m_{ik}$ and length $\ell_{ik}$: filling the segments in order of decreasing slope is best, and this order is the order along the hull. Hence EAR is a fractional knapsack problem with capacity 1, items of size $\ell_{ik}$ and value density $m_{ik}$. Segments with $m_{ik} \le 0$ never help. The greedy rule of lines L2 to L4, which takes the segments in order of decreasing density and cuts the last one, is optimal for the fractional knapsack by the usual exchange argument. Because the slopes of one bidder decrease along its hull, the greedy rule takes the segments of each bidder in their hull order, so the amounts it takes for bidder $i$ form an initial part of its hull, of total length $q_i$, and their value is $\bar R_i(q_i)$. So line L4 ends with $\sum_i \bar R_i(q_i) = \mathrm{EAR}$ and $\sum_i q_i \le 1$.

## Claim 2: line L5 gives each bidder a lottery that matches its share

If $q_i$ is a vertex $(q, R, s)$ of $\bar R_i$, the price $s$ sells with probability $q_i(s) = q$ and earns $s q = \bar R_i(q_i)$. For the vertex $(0, 0)$ the bidder gets no offer, with sale probability and revenue $0$. Otherwise $q_i$ lies strictly between two consecutive vertices $(q_a, R_a, s_a)$ and $(q_b, R_b, s_b)$ with $q_a < q_i < q_b$. Line L5 offers $s_a$ with probability $\lambda = (q_b - q_i)/(q_b - q_a)$ and $s_b$ with probability $1 - \lambda$. Then the sale probability is $\lambda q_a + (1 - \lambda) q_b = q_i$, and the expected revenue is $\lambda R_a + (1 - \lambda) R_b = \bar R_i(q_i)$, since $\bar R_i$ is linear between the two vertices. In both cases, with $P_i$ the random price of bidder $i$,

$$\Pr[v_i \ge P_i] = q_i, \qquad \mathbb{E}\bigl[P_i \cdot \mathbf{1}\{v_i \ge P_i\}\bigr] = \bar R_i(q_i). \tag{1}$$

## Claim 3: the mechanism is truthful and individually rational

Each bidder sees one take-it-or-leave-it price that does not depend on its own value. Accepting gives $v_i - P_i$ and declining gives $0$, so accepting exactly when $v_i \ge P_i$ is optimal for every value, and no bidder pays more than its value. If the prices were revealed only when offered, the same holds, since the offer to a bidder does not depend on its own behavior. Lines L7 to L9 sell to the first bidder in the order who accepts, so at most one bidder buys.

## Claim 4: the revenue is at least $(1 - (1 - 1/n)^n)\,\mathrm{EAR} \ge (1 - 1/e)\,\mathrm{EAR}$

Let $Z$ be the sale price, with $Z = 0$ if no one buys. Then $\mathbb{E}[Z] = \int_0^\infty \Pr[Z \ge t]\, dt$. Fix $t > 0$. Line L7 offers the prices in decreasing order, so all bidders with $P_i \ge t$ get their offers before any bidder with $P_i < t$. Hence $Z \ge t$ exactly when some bidder $i$ has $P_i \ge t$ and $v_i \ge P_i$. These events are independent across bidders, since the prices are drawn independently and the values are independent. With $a_i(t) = \Pr[P_i \ge t,\ v_i \ge P_i]$,

$$\Pr[Z \ge t] = 1 - \prod_i \bigl(1 - a_i(t)\bigr).$$

By (1), $a_i(t) \le q_i$, so $A(t) = \sum_i a_i(t) \le 1$. By the inequality of arithmetic and geometric means, $\prod_i (1 - a_i) \le (1 - A/n)^n$. The function $g(A) = 1 - (1 - A/n)^n$ is concave with $g(0) = 0$, so $g(A) \ge A\, g(1)$ for $0 \le A \le 1$. Therefore

$$\mathbb{E}[Z] \ge g(1) \int_0^\infty \sum_i a_i(t)\, dt = g(1) \sum_i \mathbb{E}\bigl[P_i \cdot \mathbf{1}\{v_i \ge P_i\}\bigr] = \Bigl(1 - \bigl(1 - \tfrac1n\bigr)^n\Bigr)\, \mathrm{EAR},$$

using (1) and Claim 1 in the last step. Finally $(1 - 1/n)^n \le e^{-1}$ for every $n \ge 1$.

## Claim 5: no BIC and interim IR mechanism earns more than EAR

Take any single-item mechanism that is BIC and interim IR. Let $Q_i$ be the ex ante probability that bidder $i$ gets the item. Since at most one bidder gets it at each profile, $\sum_i Q_i \le 1$. Fix bidder $i$ and let $x_k$ and $p_k$ be its interim allocation and payment at its value $s_k$, as in the proof for [Myerson's optimal auction](/myerson-optimal-auction/). That proof shows that $x$ is nondecreasing, that $p_k \le \sum_{j \le k} s_j (x_j - x_{j-1})$ with $x_0 = 0$, and hence that

$$\mathbb{E}[p_i] \le \sum_j s_j (x_j - x_{j-1})\, q_i(s_j).$$

The weights $w_j = x_j - x_{j-1}$ are nonnegative and sum to $x_K \le 1$. The right side is $\sum_j w_j \cdot s_j q_i(s_j)$, and the sale probability is $Q_i = \sum_k f_k x_k = \sum_j w_j\, q_i(s_j)$. So the pair $(Q_i, \mathbb{E}[p_i])$ lies on or below a combination, with total weight at most 1, of the points of the revenue curve, together with $(0, 0)$ for the remaining weight. Every such combination lies on or below $\bar R_i$, so $\mathbb{E}[p_i] \le \bar R_i(Q_i)$. Summing over $i$, the revenue is at most $\sum_i \bar R_i(Q_i) \le \mathrm{EAR}$.

Together, Claims 4 and 5 show that the mechanism earns at least $1 - (1 - 1/n)^n$, and so at least $1 - 1/e$, of the optimal revenue.

## Running time

Line L1 takes time linear in the support sizes, $O(N)$ in total for sorted supports, and gives at most $N$ segments. Line L2 sorts them in $O(N \log N)$ and lines L3 and L4 scan them once. Line L5 finds each bidder's position on its hull in $O(N)$ total. Running the mechanism sorts the $n$ prices in $O(n \log n)$ and makes at most $n$ offers. Only one bidder can end inside a segment, so at most one lottery has two prices, and the exact expected revenue needs at most two orderings, each in $O(n \log n + N)$.
