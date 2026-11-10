---
title: P-MERGE has work Θ(N) and span Θ(log^2 N), and P-MERGE-SORT has span Θ(log^3 n)
proves: [time.worst, depth.worst]
status: full
---

We use the lines of P-MERGE on the page and the names of the correctness proof: a call of size $N = n_1 + n_2 \ge 1$ has the longer range $X$ with $n_1$ items and the shorter range $Y$ with $n_2 \le N/2$ items, and its two calls have sizes $N_1$ and $N_2$ with $N_1 + N_2 = N - 1$. The cost model is the one of the implementation. A call of size 0 costs 1. A call of size $N \ge 1$ has its own cost $c = 2 + b$, where $b$ is the number of probes of the binary search of line L7. The work is $W(N) = c + W(N_1) + W(N_2)$, and since the calls of lines L10 and L11 run in parallel, the span is $S(N) = c + \max\{S(N_1), S(N_2)\}$. $\lg$ is $\log_2$.

**Lemma 1 (binary search).** A lower bound search over a range of $m$ items does at least $\lfloor \lg(m + 1) \rfloor$ and at most $\lceil \lg(m + 1) \rceil$ probes.

*Proof.* Each probe of a range of $m \ge 1$ items leaves a range of either $\lfloor m/2 \rfloor$ or $\lceil m/2 \rceil - 1$ items, and the search stops at $m = 0$. Let $k(m)$ be the number of probes; $k(0) = 0$. Upper bound by induction: both new sizes are at most $\lfloor m/2 \rfloor$, so $k(m) \le 1 + \lfloor \lg \lfloor m/2 \rfloor \rfloor + 1 = \lfloor \lg m \rfloor + 1 = \lceil \lg(m + 1) \rceil$, where the inner bound is read as $0$ when $\lfloor m/2 \rfloor = 0$. Lower bound by induction: both new sizes are at least $\lfloor (m - 1)/2 \rfloor$, and $\lfloor (m-1)/2 \rfloor + 1 = \lfloor (m + 1)/2 \rfloor$, so $k(m) \ge 1 + \lfloor \lg \lfloor (m + 1)/2 \rfloor \rfloor = \lfloor \lg (m + 1) \rfloor$, because $\lfloor \lg \lfloor y/2 \rfloor \rfloor = \lfloor \lg y \rfloor - 1$ for each integer $y \ge 2$. $\blacksquare$

**Lemma 2 (the split is balanced).** For a call of size $N \ge 1$, $\max\{N_1, N_2\} \le 3N/4$ and $\min\{N_1, N_2\} \ge N/4 - 1$. Its own cost is $c \le \lceil \lg(N + 1) \rceil + 2 \le \lg(N + 1) + 3$.

*Proof.* The left call gets the $\lfloor n_1/2 \rfloor$ items of $X$ before $x$, and the right call gets the $\lceil n_1/2 \rceil - 1$ items of $X$ after $x$. So each call gets at least $\lceil n_1/2 \rceil - 1 \ge n_1/2 - 1 \ge N/4 - 1$ items, since $n_1 \ge N/2$. The other call then gets at most $N - 1 - (\lceil n_1/2 \rceil - 1) \le N - N/4 = 3N/4$ items. By Lemma 1, $b \le \lceil \lg(n_2 + 1) \rceil \le \lceil \lg(N + 1) \rceil$. $\blacksquare$

**Theorem 3 (work).** For each $N \ge 0$, $N \le W(N) \le 10N + 1 - \lg(N + 1)$. So $W(N) = \Theta(N)$.

*Proof.* Each call of size at least 1 writes one item at line L9 and costs at least 1, and each item is written once, so $W(N) \ge N$. The upper bound is by strong induction on $N$, with the [substitution method](/substitution-method/). For $N = 0$, $W(0) = 1 = 10 \cdot 0 + 1 - \lg 1$. Let $N \ge 1$. By the hypothesis for the two calls and Lemma 2,

$$W(N) \le \lg(N+1) + 3 + 10(N_1 + N_2) + 2 - \lg(N_1 + 1) - \lg(N_2 + 1) = 10N - 5 + \lg(N + 1) - \lg\big((N_1 + 1)(N_2 + 1)\big).$$

Let $s = \min\{N_1, N_2\} + 1$. The two factors add up to $N + 1$, so the larger factor is at least $(N + 1)/2$, and $(N_1 + 1)(N_2 + 1) \ge s(N + 1)/2$. By Lemma 2, $s \ge N/4$, and $N/4 \ge (N + 1)/32$ for $N \ge 1$. So $(N_1 + 1)(N_2 + 1) \ge (N + 1)^2/64$, which gives $\lg\big((N_1+1)(N_2+1)\big) \ge 2\lg(N + 1) - 6$, and then $W(N) \le 10N + 1 - \lg(N + 1)$. $\blacksquare$

**Theorem 4 (span, upper bound).** For each $N \ge 0$,

$$S(N) \le \big(\lfloor \log_{4/3} N \rfloor + 1\big)\big(\lceil \lg(N + 1) \rceil + 2\big) + 1 = O(\log^2 N),$$

where the first factor is read as $0$ when $N = 0$.

*Proof.* The span is the largest total own cost along a chain of calls from the top call down to a call of size 0. By Lemma 2 a call at depth $d$ (the top call has depth 0) has size at most $(3/4)^d N$. A call of size at least 1 thus has $(3/4)^d N \ge 1$, so $d \le \lfloor \log_{4/3} N \rfloor$. A chain thus has at most $\lfloor \log_{4/3} N \rfloor + 1$ calls of size at least 1, each with own cost at most $\lceil \lg(N + 1) \rceil + 2$ by Lemma 2 (sizes only go down along the chain), and it ends with one call of size 0, which costs 1. $\blacksquare$

**Theorem 5 (span, lower bound).** Call an input *interleaved* if its items are distinct and the sorted merge takes them from the two inputs in turn. For each interleaved input of size $N$, with $x = \lg(N + 1)$,

$$S(N) \ge \frac{x(x + 1)}{2} = \Omega(\log^2 N).$$

So the span of P-MERGE in the worst case is $\Theta(\log^2 N)$.

*Proof.* In an interleaved input the two sizes differ by at most 1, so $n_2 = \lfloor N/2 \rfloor$. The items are distinct, so by the split lemma of the correctness proof the left call gets exactly the items less than $x = T[q_1]$, which form a prefix of the merged order, and the right call gets the items greater than it, a suffix. A prefix or suffix of a sequence that alternates also alternates, so both calls are interleaved. The larger of the two has $N' \ge (N - 1)/2$ items, so $\lg(N' + 1) \ge x - 1$. By Lemma 1 the own cost is $c \ge 2 + \lfloor \lg(\lfloor N/2 \rfloor + 1) \rfloor > 2 + \lg\big((N + 1)/2\big) - 1 = x$.

Now induct on $N$ with the claim $S(M) \ge f(\lg(M + 1))$ for each interleaved input of size $M$, where $f(y) = y(y + 1)/2$ is increasing for $y \ge 0$. For $M = 0$, $S(0) = 1 \ge f(0) = 0$. For $N \ge 1$, $S(N) \ge c + S(N') \ge x + f(x - 1) = x + (x - 1)x/2 = f(x)$. Theorem 4 gives the matching upper bound. $\blacksquare$

**Theorem 6 (P-MERGE-SORT).** P-MERGE-SORT of the page has span $\Theta(\log^3 n)$ and work $\Theta(n \log n)$.

*Proof.* Its span satisfies $S_{\text{sort}}(n) = 1 + \max\{S_{\text{sort}}(\lfloor n/2 \rfloor), S_{\text{sort}}(\lceil n/2 \rceil)\} + S(n)$ for $n \ge 2$, with $S_{\text{sort}}(0) = S_{\text{sort}}(1) = 1$, where $S(n)$ is the span of the merge of line 7 of P-MERGE-SORT. Let $B(N)$ be the bound of Theorem 4; it does not decrease as $N$ grows. We claim $S_{\text{sort}}(n) \le \lceil \lg n \rceil \big(B(n) + 1\big) + 1$, with $\lceil \lg 0 \rceil$ read as 0. This holds for $n \le 1$. For $n \ge 2$, both halves have at most $\lceil n/2 \rceil$ items and $\lceil \lg \lceil n/2 \rceil \rceil = \lceil \lg n \rceil - 1$, so by induction $S_{\text{sort}}(n) \le 1 + (\lceil \lg n \rceil - 1)\big(B(n) + 1\big) + 1 + B(n)$, which is the claim. This is $O(\log^3 n)$.

For the lower bound let $n = 2^L$ and let the input be the bit reversal permutation: position $i$ holds the number whose $L$ bits are those of $i$ in reverse order. A subarray of size $2^\ell$ at an aligned position holds the numbers with fixed lowest $L - \ell$ bits, and its two halves differ in the next bit. So once the halves are sorted, they interleave, and the merge at that subarray has span at least $f(\lg(2^\ell + 1)) \ge \ell(\ell + 1)/2$ by Theorem 5. The chain of calls that follows the left half at each level meets one such merge for each $\ell = 1, \ldots, L$, so $S_{\text{sort}}(n) \ge \sum_{\ell = 1}^{L} \ell(\ell + 1)/2 = L(L + 1)(L + 2)/6 = \Omega(\log^3 n)$.

For the work, Theorem 3 gives $W(N) \le 10N + 1$ for each merge. The merges of one level of the recursion have sizes that add up to at most $n$, and there are at most $2^{\ell}$ of them at level $\ell$, so one level costs $O(n)$ and the $\lceil \lg n \rceil$ levels cost $O(n \log n)$. Each level with all sizes at least 2 costs at least $n$ by Theorem 3, and there are $\lfloor \lg n \rfloor$ such levels, so the work is also $\Omega(n \log n)$. $\blacksquare$
