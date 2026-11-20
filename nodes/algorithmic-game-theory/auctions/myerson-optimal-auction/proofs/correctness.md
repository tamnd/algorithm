---
title: Correctness and optimality of Myerson's auction
proves: [correctness]
status: full
---

There are $n$ bidders with independent private values. Bidder $i$ has a discrete distribution on the values $s_1 < s_2 < \cdots < s_K$ (the support and $K$ depend on $i$, and we drop the index $i$ when only one bidder is in question) with probabilities $f_1, \ldots, f_K > 0$. Write $q_k = \sum_{j \ge k} f_j = \Pr[v \ge s_k]$, so $q_1 = 1$, and put $q_{K+1} = 0$ and $s_{K+1} q_{K+1} = 0$. The revenue curve of the bidder is the list of points $P_0 = (0, 0)$ and $(q_k, s_k q_k)$ for $k = K, K-1, \ldots, 1$, in increasing order of $q$. The segment from $(q_{k+1}, s_{k+1} q_{k+1})$ to $(q_k, s_k q_k)$ has length $f_k$ in $q$ and slope

$$\varphi_k = \frac{s_k q_k - s_{k+1} q_{k+1}}{f_k},$$

which is the discrete virtual value of $s_k$. Let $\bar R$ be the least concave function on $[0, 1]$ that lies on or above all the points, and let $\bar\varphi_k$ be the slope of $\bar R$ on the segment of $s_k$. This is the ironed virtual value. Utilities are quasilinear: a bidder with value $v$ who wins with probability $x$ and pays $p$ has utility $v x - p$.

## Claim 1: line L1 computes the ironed virtual values, and they are nondecreasing in the value

The function `upper_hull` scans the points in increasing order of $q$ and keeps a stack. It removes the top of the stack while that point lies on or below the chord from the point under it to the new point. This is the monotone chain method for the upper hull, and at the end the stack holds the vertices of $\bar R$, from $P_0$ to $(1, s_1)$. Between two consecutive vertices $\bar R$ is linear, so each segment of a support value inside that range gets the slope of the chord. The slopes of a concave function do not increase as $q$ grows. Since $q_k$ decreases as $k$ grows, $\bar\varphi_1 \le \bar\varphi_2 \le \cdots \le \bar\varphi_K$. The slope of $\bar R$ changes only at a vertex, so if $\bar\varphi_{k-1} \ne \bar\varphi_k$, then the point $(q_k, s_k q_k)$ is a vertex of $\bar R$. The point $(q_1, s_1 q_1) = (1, s_1)$ is always a vertex, since it is the last point.

## Claim 2: the allocation rule is monotone

Fix the reports of all bidders except $i$, and let $c_j$ be their ironed virtual values (line L2). By lines L3 and L4, bidder $i$ with ironed virtual value $c$ wins exactly when $c \ge 0$, $c > c_j$ for every $j < i$ with $c_j \ge 0$, and $c \ge c_j$ for every $j > i$ with $c_j \ge 0$. Each condition stays true when $c$ grows. By Claim 1, a higher report gives a value of $c$ at least as high. So if bidder $i$ wins with report $s_k$, it wins with every report $s_{k'} > s_k$. The method `wins` tests exactly these conditions.

## Claim 3: truth telling is a dominant strategy and the auction is individually rational

Fix bidder $i$, its true value $v$ in its support, and the reports of the others. Let $t$ be the smallest support value of bidder $i$ with which it wins, if there is one. By Claim 2, bidder $i$ wins with a report $b$ exactly when $b \ge t$. Line L5 is reached only for the winner $w$, which wins with its own report, so the scan finds a value, and it is the smallest winning report, so the winner pays $t$. The value $t$ depends only on the reports of the others.

If bidder $i$ reports $v$, it gets $v - t \ge 0$ when $v \ge t$ and $0$ when $v < t$, that is, $\max(v - t, 0) \ge 0$. This is individual rationality. With any other report it either wins and pays the same $t$, for utility $v - t$, or loses, for utility $0$. Both are at most $\max(v - t, 0)$. If no report wins, bidder $i$ always gets $0$.

## Claim 4: the expected revenue equals the expected ironed virtual surplus

Fix bidder $i$ and the reports of the others. Let $x_k \in \{0, 1\}$ say whether bidder $i$ wins with report $s_k$, and put $x_0 = 0$. By Claim 2, $x$ is nondecreasing, and by Claim 3 the payment with report $s_k$ is

$$p_k = \sum_{j \le k} s_j (x_j - x_{j-1}),$$

because the sum is $s_t$ when $k \ge t$ and $0$ otherwise. Exchange the order of summation:

$$\sum_k f_k p_k = \sum_j s_j (x_j - x_{j-1}) q_j = \sum_j x_j \bigl(s_j q_j - s_{j+1} q_{j+1}\bigr) = \sum_j f_j x_j \varphi_j. \tag{1}$$

Now compare with $\bar\varphi$. Put $G_k = \sum_{j \ge k} f_j \varphi_j$ and $\bar G_k = \sum_{j \ge k} f_j \bar\varphi_j$. The first sum telescopes to $G_k = s_k q_k$, the height of the revenue curve at $q_k$. The second is the integral of the slope of $\bar R$ from $0$ to $q_k$, so $\bar G_k = \bar R(q_k)$, since $\bar R(0) = 0$. Summation by parts gives, with $G_{K+1} = \bar G_{K+1} = 0$,

$$\sum_k f_k x_k (\bar\varphi_k - \varphi_k) = \sum_k x_k \bigl((\bar G_k - \bar G_{k+1}) - (G_k - G_{k+1})\bigr) = \sum_{k \ge 1} (x_k - x_{k-1}) (\bar G_k - G_k). \tag{2}$$

In (2), the term $k = 1$ vanishes because $(1, s_1)$ is a vertex of $\bar R$. For $k \ge 2$, the auction decides through $\bar\varphi$ only, so $x_k \ne x_{k-1}$ implies $\bar\varphi_k \ne \bar\varphi_{k-1}$, and then $(q_k, s_k q_k)$ is a vertex by Claim 1, so $\bar G_k = G_k$. Hence (2) is zero, and $\sum_k f_k p_k = \sum_k f_k x_k \bar\varphi_k$.

Take the expectation over the independent reports of the others and sum over the bidders. The expected revenue is $\mathbb{E}[\sum_i X_i(v) \bar\varphi_i(v_i)]$, where $X_i(v) = 1$ if bidder $i$ wins at the profile $v$. At each profile the winner has the largest ironed virtual value, which is nonnegative, and no one wins only when all of them are negative. So the expected revenue is $\mathbb{E}[\max(0, \max_i \bar\varphi_i(v_i))]$.

## Claim 5: no Bayesian incentive compatible and individually rational mechanism earns more

Take any mechanism, perhaps randomized, in which truth telling is a Bayes-Nash equilibrium (BIC) and every type has nonnegative expected utility (interim IR). For bidder $i$, let $x_k$ be its probability to win and $p_k$ its expected payment with report $s_k$, both averaged over the values of the others, and put $x_0 = p_0 = 0$.

*Monotone.* Type $s_k$ does not gain by reporting $s_{k-1}$, and type $s_{k-1}$ does not gain by reporting $s_k$. Adding the two inequalities gives $(s_k - s_{k-1})(x_k - x_{k-1}) \ge 0$, so $x$ is nondecreasing.

*Payment bound.* IR for type $s_1$ gives $p_1 \le s_1 x_1$. The first of the two inequalities above is $s_k x_k - p_k \ge s_k x_{k-1} - p_{k-1}$, that is, $p_k \le p_{k-1} + s_k (x_k - x_{k-1})$. By induction, $p_k \le \sum_{j \le k} s_j (x_j - x_{j-1})$ for every $k$.

So, by the computation (1), $\sum_k f_k p_k \le \sum_k f_k x_k \varphi_k$. In (2), every term is now nonnegative: $x_k - x_{k-1} \ge 0$ and $\bar G_k \ge G_k$ because $\bar R$ lies above the curve, and the term $k = 1$ is zero. Hence $\sum_k f_k p_k \le \sum_k f_k x_k \bar\varphi_k$. Let $X_i(v)$ be the probability that bidder $i$ gets the item at the profile $v$. By independence, $\sum_k f_k x_k \bar\varphi_k = \mathbb{E}[X_i(v) \bar\varphi_i(v_i)]$. Summing over the bidders, and using $X_i \ge 0$ and $\sum_i X_i \le 1$, the expected revenue is at most

$$\mathbb{E}\Bigl[\sum_i X_i(v)\, \bar\varphi_i(v_i)\Bigr] \le \mathbb{E}\Bigl[\max\bigl(0, \max_i \bar\varphi_i(v_i)\bigr)\Bigr].$$

By Claim 4, Myerson's auction attains this bound. A DSIC and ex post IR mechanism is also BIC and interim IR, so the auction is optimal in both classes.

## The continuous regular case

For a distribution with density $f$ and a strictly increasing virtual valuation $\varphi(v) = v - (1 - F(v))/f(v)$, the function `myerson_regular` gives the item to the bidder with the largest nonnegative virtual value and charges $\varphi_w^{-1}(\max(0, \max_{j \ne w} \varphi_j(b_j)))$. This is the smallest bid with which $w$ still wins, up to a tie, which has probability $0$. The proofs of Claims 3 to 5 carry over with sums replaced by integrals: the payment identity is $p(v) = v x(v) - \int_0^v x(z)\, dz$ (Myerson's lemma), and integration by parts gives $\mathbb{E}[p_i] = \mathbb{E}[\varphi_i(v_i) x_i(v_i)]$. No ironing is needed because $\varphi$ is already monotone. For $U[0, 1]$, $\varphi(v) = 2v - 1$, and with two bidders the revenue is $\mathbb{E}[\max(0, 2\max(v_1, v_2) - 1)] = \int_{1/2}^1 (2z - 1)\, 2z\, dz = 5/12$.

## Running time

Line L1 builds one hull per bidder in time linear in its support size, since the points come sorted by $q$ and each point enters and leaves the stack at most once. One run of the auction does $O(n)$ work in lines L2 to L4, and line L5 checks at most $K_w$ support values with an $O(n)$ test each. The implementation keeps that test simple. Computing the two maxima of the others once makes each test $O(1)$, for $O(n + K_w)$ per run.
