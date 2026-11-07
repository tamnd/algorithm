---
title: Pairwise summation satisfies the gamma of ceil(log2 n) error bound
proves: [correctness]
status: full
---

**Setting.** A floating-point system with unit roundoff $u$ in which every addition satisfies the standard model $\mathrm{fl}(a + b) = (a + b)(1 + \delta)$, $|\delta| \le u$. This holds for round to nearest with $u = \tfrac12\beta^{1-p}$ and for directed rounding with $u = \beta^{1-p}$, as long as the result does not overflow; an addition that underflows is exact, so it satisfies the model with $\delta = 0$. Write $\gamma_h = hu/(1 - hu)$ for $hu < 1$.

**Lemma 1** (Higham, Lemma 3.1). If $|\delta_j| \le u$ and $\rho_j = \pm 1$ for $j = 1, \ldots, h$, and $hu < 1$, then $\prod_{j=1}^h (1 + \delta_j)^{\rho_j} = 1 + \theta_h$ with $|\theta_h| \le \gamma_h$. Only the case $\rho_j = 1$ is needed here, and for it the proof is short: $|\prod(1 + \delta_j) - 1| \le (1 + u)^h - 1$, and $(1 + u)^h \le 1/(1 - u)^h \le 1/(1 - hu)$, the last step by Bernoulli's inequality $(1 - u)^h \ge 1 - hu$. So $(1 + u)^h - 1 \le hu/(1 - hu) = \gamma_h$.

**The tree.** A run of PAIRWISE-SUM on $x_1, \ldots, x_n$, $n \ge 1$, defines a binary tree: a call with $n \le b$ terms is a chain in which the terms are added one by one, and a call with $n > b$ terms is a node whose two children are the calls on the two halves. Every addition (line L4 or line L9) is an internal node with two inputs. For a term $x_i$, let $h_i$ be the number of additions on the path from $x_i$ to the root, and let $h = \max_i h_i$.

**Lemma 2 (the computed value).** If no addition overflows and $hu < 1$, the value returned by any call on a range $R$ is $\sum_{i \in R} x_i \prod_{j \in P_i} (1 + \delta_j)$, where $P_i$ is the set of additions on the path from $x_i$ to the root of that call, and $|\delta_j| \le u$.

*Proof.* By induction on the size of the call. A single term is returned unchanged, and the product over the empty path is $1$. For a chain in lines L3 and L4, after the step that adds $x_k$ the value is $\mathrm{fl}(s + x_k) = (s + x_k)(1 + \delta)$; by induction $s$ has the stated form for the earlier terms, and multiplying by $1 + \delta$ adds the new addition to the path of every earlier term and of $x_k$. For line L9, $\mathrm{fl}(s_1 + s_2) = (s_1 + s_2)(1 + \delta)$, and $s_1$ and $s_2$ have the stated form by induction on the two halves; the addition of line L9 is on the path of every term of the range. $\square$

**Theorem.** Under the same assumptions, $\hat s = \sum_{i=1}^n x_i (1 + \theta_i)$ with $|\theta_i| \le \gamma_{h_i} \le \gamma_h$, hence

$$|\hat s - s| \le \gamma_h \sum_{i=1}^n |x_i|.$$

*Proof.* Apply Lemma 2 to the top-level call and Lemma 1 to each product, which has $h_i \le h$ factors; $\gamma$ is increasing in $h$. Then $|\hat s - s| = |\sum x_i \theta_i| \le \sum |x_i| |\theta_i| \le \gamma_h \sum|x_i|$. $\square$

**Lemma 3 (the depth for $b = 1$).** With $b = 1$, $h = d(n)$ where $d(1) = 0$ and $d(n) = 1 + d(\lceil n/2 \rceil)$ for $n \ge 2$, and $d(n) = \lceil \log_2 n \rceil$.

*Proof.* A call on $n \ge 2$ terms makes one addition and two calls on $\lfloor n/2 \rfloor$ and $\lceil n/2 \rceil$ terms. The largest path goes through the larger half, because $d$ is nondecreasing (by induction: if $m \le n$ then $\lceil m/2 \rceil \le \lceil n/2 \rceil$). So $h = 1 + d(\lceil n/2 \rceil)$. For the closed form, let $k = \lceil \log_2 n \rceil \ge 1$ for $n \ge 2$, so $2^{k-1} < n \le 2^k$. Then $2^{k-2} < n/2 \le 2^{k-1}$, and since $2^{k-1}$ is an integer, $\lceil n/2 \rceil \le 2^{k-1}$; also $\lceil n/2 \rceil \ge n/2 > 2^{k-2}$. Hence $\lceil \log_2 \lceil n/2 \rceil \rceil = k - 1$, and by induction $d(n) = 1 + (k - 1) = k$. $\square$

**Lemma 4 (the depth with blocks).** With block size $b \ge 1$, $h \le (b - 1) + \lceil \log_2 \lceil n/b \rceil \rceil$ for $n \ge 1$.

*Proof.* After $k$ halvings the largest range has $\lceil n/2^k \rceil$ terms (the ceiling of a ceiling of halves is the ceiling of $n/2^k$). Recursion stops on a path once the range has at most $b$ terms, which happens after at most $K$ halvings, the least $k$ with $\lceil n/2^k \rceil \le b$, that is $2^k \ge n/b$, that is $2^k \ge \lceil n/b \rceil$; so $K = \lceil \log_2 \lceil n/b \rceil \rceil$. Each halving contributes one addition (line L9) to the path, and the leaf chain contributes at most $b - 1$ additions. $\square$

**Bottom-up variant.** Level $\ell$ of the bottom-up method has $\lceil n/2^\ell \rceil$ values, each the sum of a contiguous group of at most $2^\ell$ terms, and each level adds at most one addition to the path of every term. After $\lceil \log_2 n \rceil$ levels one value is left, so the same theorem holds with $h = \lceil \log_2 n \rceil$.

**Cost.** Every addition merges two values into one, and the algorithm starts with $n$ values and ends with one, so it makes exactly $n - 1$ additions.
