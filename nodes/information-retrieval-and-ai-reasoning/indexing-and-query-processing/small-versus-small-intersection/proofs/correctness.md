---
title: Small-versus-small returns the intersection with at most 2 m log2(1 + n/m) + 3 m tests for each list
proves: [correctness]
status: full
---

All lists are strictly increasing. A test is one two-way comparison of ids, either $<$ or $=$. For a list $L$ of length $n$ we write GALLOP$(L, x, lo)$ for the search of line L6, which is NEXT-GEQ of the [posting list](/posting-list/) page: it returns the least index $p \ge lo$ with $L[p] \ge x$, or $n$ if there is none.

**Lemma 1 (galloping).** GALLOP$(L, x, lo)$ with $lo < n$ returns the index above. With $g = p - lo$, it makes 1 test when $g = 0$ and at most $2 \lfloor \log_2 g \rfloor + 2$ tests when $g \ge 1$. In both cases this is at most $2 \log_2(g + 1) + 2$. With $lo \ge n$ it makes no test and returns $lo$.

*Proof.* The correctness and the first two counts are the theorem of the proof file of the [posting list](/posting-list/) page, for the same procedure. In short: the probes at offsets $0, 1, 3, 7, \ldots, 2^t - 1$ all give $<$, so $g \ge 2^t$; one more probe may stop the doubling; the binary search runs on at most $2^t - 1$ indices and makes at most $t$ tests. The total is $1 + t + 1 + t$ with $t \le \lfloor \log_2 g \rfloor$. For $g \ge 1$, $\lfloor \log_2 g \rfloor \le \log_2(g+1)$; for $g = 0$, $1 \le 2$. $\square$

**Lemma 2 (one step).** Let $C$ be a strictly increasing list of $r$ candidates and $L$ a strictly increasing list of length $n$. The loop of lines L4 to L8 sets the output list to $C \cap L$ in increasing order, and makes at most $2r \log_2(1 + n/r) + 3r$ tests when $r \ge 1$.

*Proof.* We use this invariant, before the search for a candidate $x$:

> **(S)** Each id in $L[0 \ldots p-1]$ is less than $x$, and the output holds the candidates before $x$ that are in $L$, in order.

Line L4 sets $p = 0$ and the output is empty, so (S) holds for the first candidate. Line L6 returns the least $p' \ge p$ with $L[p'] \ge x$. By (S), no index below $p$ holds an id $\ge x$, so $p'$ is the least index of $L$ with $L[p'] \ge x$. Hence $x \in L$ exactly when $p' < n$ and $L[p'] = x$, which is the test of lines L7 and L8. If $p' = n$, each id of $L$ is less than $x$, so no later candidate, which is larger than $x$, is in $L$, and the break of line L7 is right. Otherwise let $x'$ be the next candidate, with $x' > x$. If $L[p'] = x$, line L8 adds $x$ and sets $p = p' + 1$; each id of $L[0 \ldots p']$ is at most $x < x'$. If $L[p'] > x$, then $p = p'$, and each id of $L[0 \ldots p'-1]$ is less than $x < x'$. So (S) holds for $x'$. When the loop ends, the output is $C \cap L$ in order.

For the count, let the loop search for $r' \le r$ candidates, and let $g_1, \ldots, g_{r'}$ be the values of $g$ in Lemma 1 for these searches. The start of each search is at least the answer of the search before it, so the ranges $[p, p')$ do not overlap and $\sum_i g_i \le n$. Each candidate costs at most $2 \log_2(g_i + 1) + 2$ tests in line L6 and one test in line L8. The function $y \mapsto \log_2(1 + y)$ is concave, so by Jensen's inequality

$$\sum_{i=1}^{r'} \log_2(1 + g_i) \le r' \log_2\left(1 + \frac{1}{r'} \sum_i g_i\right) \le r' \log_2\left(1 + \frac{n}{r'}\right).$$

So the step makes at most $2r' \log_2(1 + n/r') + 3r'$ tests. The function $h(s) = s \log_2(1 + n/s)$ is nondecreasing for $s > 0$: its derivative is $\log_2(1 + y) - \frac{y}{(1+y) \ln 2}$ with $y = n/s$, and $\ln(1 + y) \ge \frac{y}{1+y}$ for $y \ge 0$. With $r' \le r$ this gives the bound. If $r' = 0$, the step makes no test. $\square$

**Theorem.** For lists $L_1, \ldots, L_k$ with lengths $n_1 \le \cdots \le n_k$ after line L1, SVS returns $L_1 \cap \cdots \cap L_k$ in increasing order. If $n_1 \ge 1$, it makes at most

$$\sum_{t=2}^{k} \left( 2 n_1 \log_2\left(1 + \frac{n_t}{n_1}\right) + 3 n_1 \right)$$

tests. For $k = 2$, $m = n_1$ and $n = n_2$, this is $2m \log_2(1 + n/m) + 3m$, which is at most $5 \log_2 \binom{m+n}{m}$.

*Proof.* By induction on $t$, the candidate list after step $t$ is $L_1 \cap \cdots \cap L_t$ in increasing order: it holds for $t = 1$ by line L2, and Lemma 2 gives the step from $t - 1$ to $t$. If it becomes empty, the full intersection is empty, so the early stop of line L3 is right. Each candidate list is a subset of $L_1$, so its size $r$ is at most $n_1$. By Lemma 2 and because $h$ is nondecreasing, step $t$ makes at most $2 n_1 \log_2(1 + n_t/n_1) + 3 n_1$ tests.

For the last claim, $\binom{m+n}{m} = \prod_{i=1}^{m} \frac{n+i}{i} \ge \left(\frac{m+n}{m}\right)^m$, because $\frac{n+i}{i} \ge \frac{n+m}{m}$ for $1 \le i \le m$. So $\log_2 \binom{m+n}{m} \ge m \log_2(1 + n/m)$. Since $n \ge m$, also $m \log_2(1 + n/m) \ge m$. Hence $2m \log_2(1 + n/m) + 3m \le 2 \log_2 \binom{m+n}{m} + 3 \log_2 \binom{m+n}{m}$. $\blacksquare$

The lower bound $\lceil \log_2 \binom{m+n}{m} \rceil$ for each algorithm in the comparison model is proved in the proof file of [adaptive set intersection](/adaptive-set-intersection/). So SVS with galloping is optimal for two lists up to a factor of 5 in the worst case.
