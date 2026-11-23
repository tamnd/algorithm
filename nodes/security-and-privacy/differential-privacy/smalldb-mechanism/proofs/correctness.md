---
title: SmallDB is epsilon-DP, a small database with error alpha exists, and the output is accurate
proves: [correctness]
status: full
---

We use the pseudocode of the page. The universe $X$ has $U$ elements, the data is a histogram $x$ over $X$ with $n \ge 1$ records, and $n$ is public. For a query $f \in \{0,1\}^X$ and a histogram $h$ with $\|h\|_1 > 0$, $f(h) = \sum_j f_j h_j / \|h\|_1$ is the fraction of records that $f$ counts. Two datasets are neighbors if one record is replaced by another, so $n$ stays the same. $R$ is the set of histograms with exactly $m$ records, and $u(x, y) = -\max_{f \in Q} |f(x) - f(y)|$.

**Claim 1 (privacy).** The output of line L4 is $\varepsilon$-DP.

*Proof.* For neighbors $x, x'$ and each $f$, the count $\sum_j f_j x_j$ moves by at most 1 and $n$ is fixed, so $|f(x) - f(x')| \le 1/n$. Then for each $y$, $|f(x) - f(y)|$ moves by at most $1/n$, and so does the maximum over $f$: $|u(x, y) - u(x', y)| \le 1/n$. Line L4 picks $y$ with probability $P_x(y) = e^{\varepsilon n u(x,y)/2} / Z(x)$, with $Z(x) = \sum_{r \in R} e^{\varepsilon n u(x,r)/2}$. So $e^{\varepsilon n u(x,y)/2} \le e^{\varepsilon/2} e^{\varepsilon n u(x',y)/2}$ and $Z(x') \le e^{\varepsilon/2} Z(x)$, which give $P_x(y) \le e^{\varepsilon} P_{x'}(y)$. $R$ does not depend on $x$, so this covers every output. $\square$

**Claim 2 (a small database exists; Dwork-Roth Proposition 4.1).** Let $|Q| \ge 3$, $\alpha > 0$ and $m \ge \ln|Q|/\alpha^2$. Then some $y \in R$ has $\max_{f \in Q} |f(x) - f(y)| \le \alpha$.

*Proof.* Draw $m$ records independently from the empirical distribution $x/n$, and let $y$ be their histogram. For a fixed $f$, $f(y)$ is the mean of $m$ independent 0-1 variables with mean $f(x)$. By the Hoeffding inequality, $P(|f(y) - f(x)| > \alpha) \le 2 e^{-2m\alpha^2} \le 2|Q|^{-2}$. By the union bound over $Q$, the probability that some query has error above $\alpha$ is at most $2|Q|^{-1} < 1$. So some outcome $y$ has all errors at most $\alpha$, and it lies in $R$. $\square$

**Claim 3 (accuracy).** Let $\mathrm{OPT} = \max_{y \in R} u(x, y)$ and $\beta \in (0, 1)$. With probability at least $1 - \beta$ the output has

$$\max_{f \in Q} |f(x) - f(y)| \le -\mathrm{OPT} + \frac{2(\ln|R| + \ln(1/\beta))}{\varepsilon n}.$$

With $m = \lceil \ln|Q|/\alpha^2 \rceil$ and $|Q| \ge 3$, Claim 2 gives $-\mathrm{OPT} \le \alpha$.

*Proof.* Let $t = \ln|R| + \ln(1/\beta)$, and call $y$ bad if $u(x, y) < \mathrm{OPT} - 2t/(\varepsilon n)$. Let $y^*$ reach $\mathrm{OPT}$. For a bad $y$, $P(y)/P(y^*) = e^{\varepsilon n (u(x,y) - \mathrm{OPT})/2} < e^{-t} = \beta/|R|$. There are at most $|R|$ bad $y$, and $P(y^*) \le 1$, so the total probability of a bad output is less than $\beta$. $\square$

**Size of $R$.** $|R| = \binom{m + U - 1}{U - 1} \le U^m$, so $\ln|R| \le m \ln U$. With $m = \lceil \ln|Q|/\alpha^2 \rceil$ the error bound of Claim 3 is at most

$$\alpha + \frac{2\big((\ln|Q|/\alpha^2 + 1)\ln U + \ln(1/\beta)\big)}{\varepsilon n}.$$

The first term falls with $\alpha$ and the second grows as $1/\alpha^2$. Choosing $\alpha$ of order $(\ln U \ln|Q|/(\varepsilon n))^{1/3}$ makes the error of that order. Dwork and Roth state the result as Theorem 4.5 with explicit constants: error at most $\big((16 \log|X| \log|Q| + 4\log(1/\beta))/(\varepsilon \|x\|_1)\big)^{1/3}$ with probability at least $1 - \beta$.

**Cost.** Line L2 lists $|R| = \binom{m + U - 1}{U - 1}$ histograms. Line L3 computes the $|Q|$ answers of each in $O(|Q| U)$, after the answers on $x$ are computed one time. Line L4 normalizes and samples in $O(|R|)$. The total is $O(|R|\,|Q|\,U)$ time and $O(|R|)$ space, exponential in $m$ when $U \ge 2$.
