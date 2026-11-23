---
title: Propose-test-release for the median computes the distance to instability and is (2 epsilon, delta)-DP
proves: [correctness]
status: full
---

We use the pseudocode of the page. A dataset is a list $x$ of $n$ values in $[0, \Lambda]$, with $n$ odd and $m = (n+1)/2$. We sort it and set $x_i = 0$ for $i \le 0$ and $x_i = \Lambda$ for $i > n$. Two datasets are neighbors if one value is replaced by another, and $d(x, y)$ is the number of replacements from $x$ to $y$. The median is $f(x) = x_m$, and $LS(y) = \max_{d(y,y')=1} |f(y) - f(y')|$ is its local sensitivity. The proposed bound is $b > 0$, the threshold is $T = \ln(1/\delta)/\varepsilon$, and the output $\bot$ means "no answer".

**Claim 1 (line L1).** Let $\gamma(x) = \min\{d(x, y) : LS(y) > b\}$, with $\gamma(x) = \infty$ if no $y$ has $LS(y) > b$. Then $\gamma(x) = \min\{k \ge 0 : A(k, x) > b\}$, with $A(k, x) = \max_{0 \le t \le k+1}(x_{m+t} - x_{m+t-k-1})$.

*Proof.* By Nissim, Raskhodnikova and Smith (2007, Proposition 3.4), $A(k, x) = \max_{d(x,y) \le k} LS(y)$. The proof is on the [smooth sensitivity](/smooth-sensitivity/) page. So $A(k, x) > b$ exactly when some $y$ with $d(x, y) \le k$ has $LS(y) > b$, and the least such $k$ is $\gamma(x)$. For $k \ge n$ every dataset is within $k$ replacements and $A(k, x) = \Lambda$, so $\gamma(x) = \infty$ exactly when $b \ge \Lambda$, and the loop can stop at $k = n$. The test file checks line L1 against a breadth-first search over the grid $\{0, \dots, \Lambda\}^n$ for $n \le 5$ and $\Lambda \le 4$. $\square$

**Claim 2 (sensitivity of $\gamma$).** For neighbors $x, x'$, $|\gamma(x) - \gamma(x')| \le 1$, and $\gamma(x) = \infty$ exactly when $\gamma(x') = \infty$.

*Proof.* $d$ is a metric, so $d(x, y) \le 1 + d(x', y)$ for every $y$. Take the minimum over the $y$ with $LS(y) > b$: $\gamma(x) \le 1 + \gamma(x')$, and the same with $x$ and $x'$ swapped. The set $\{y : LS(y) > b\}$ does not depend on $x$, so it is empty for both or for neither. $\square$

**Claim 3 (privacy; Vadhan Proposition 3.2).** The output is $(2\varepsilon, \delta/2)$-DP, so it is $(2\varepsilon, \delta)$-DP.

*Proof.* Fix neighbors $x, x'$ and a set $S$ of outputs. Write $P_x(\bot) = P(\gamma(x) + Z \le T)$ with $Z \sim \mathrm{Lap}(1/\varepsilon)$, and $p_x = 1 - P_x(\bot)$. Lines L2 and L3 are the [Laplace mechanism](/laplace-mechanism/) on $\gamma$, which has sensitivity 1 by Claim 2, followed by a test. So by post-processing, $P_x(\bot) \le e^{\varepsilon} P_{x'}(\bot)$ and $p_x \le e^{\varepsilon} p_{x'}$. If both $\gamma$ are infinite, the test passes for both, and the case below with $\gamma(x) \ge 1$ applies.

Case $\gamma(x) \ge 1$. Then $LS(x) \le b$, so $|f(x) - f(x')| \le b$. Let $S_0 = S \setminus \{\bot\}$ and let $L_c$ be the law of $c + \mathrm{Lap}(b/\varepsilon)$. Then $L_{f(x)}(S_0) \le e^{\varepsilon} L_{f(x')}(S_0)$, and

$$P_x(S) = [\bot \in S] P_x(\bot) + p_x L_{f(x)}(S_0) \le e^{\varepsilon}[\bot \in S] P_{x'}(\bot) + e^{2\varepsilon} p_{x'} L_{f(x')}(S_0) \le e^{2\varepsilon} P_{x'}(S).$$

Case $\gamma(x) = 0$. Then $p_x = P(Z > T) = \frac{1}{2} e^{-\varepsilon T} = \delta/2$, and

$$P_x(S) \le [\bot \in S] P_x(\bot) + p_x \le e^{\varepsilon} P_{x'}(S) + \delta/2.$$

In both cases $P_x(S) \le e^{2\varepsilon} P_{x'}(S) + \delta/2$. $\square$

Vadhan states the result with $\delta$. The proof gives $\delta/2$ because $P(Z > T) = \delta/2$ for the Laplace law. The test file computes the exact output law for every pair of neighbors with $n = 3$ and $\Lambda = 4$, and checks the hockey-stick divergence at $e^{2\varepsilon}$ against $\delta/2$ by a fine numerical integration.

**Claim 4 (utility).** If $\gamma(x) \ge T + t/\varepsilon$ with $t \ge 0$, the test passes with probability at least $1 - \frac{1}{2} e^{-t}$, and then the output is $f(x) + \mathrm{Lap}(b/\varepsilon)$, whose error is above $s$ with probability $e^{-s\varepsilon/b}$.

*Proof.* The test fails when $Z \le T - \gamma(x) \le -t/\varepsilon$, which has probability $\frac{1}{2} e^{-t}$. The second part is the tail of the Laplace law. $\square$

**Cost.** Sorting takes $O(n \log n)$. Line L1 tries $k = 0, 1, \dots, \gamma(x)$ and each try takes $O(k)$, so it takes $O(\min(\gamma(x), n)^2)$ after the sort. Lines L2 to L4 take $O(1)$. The total is $O(n^2)$ time in the worst case and $O(n)$ extra space.
