---
title: The permutation test and its Monte Carlo version have exact level
proves: [correctness]
status: full
---

We use the pseudocode of the page. $G$ is a finite group of transformations of the sample space, with $\lvert G \rvert = K$. The **randomization hypothesis** is that under $H_0$ the data $Z$ and $gZ$ have the same distribution for every $g \in G$. For two samples, $G$ is the group of permutations of the $n$ coordinates and the hypothesis is exchangeability. For paired data, $G$ is the group of sign changes and the hypothesis is that the $D_i$ are independent and symmetric about 0. The statistic is a fixed function $T$.

For a point $z$ define the exact p-value

$$p(z) = \frac{1}{K} \#\{g \in G : T(gz) \ge T(z)\}.$$

**Lemma (ranks).** Let $v_1, \ldots, v_N$ be real numbers and $R_i = \#\{j : v_j \ge v_i\}$, which counts $i$ itself. Then $\#\{i : R_i \le k\} \le k$ for every $k \ge 0$.

*Proof.* Let $A = \{i : R_i \le k\}$. If $A$ is empty there is nothing to prove. Otherwise pick $i_0 \in A$ with the smallest value $v_{i_0}$. Every $i \in A$ has $v_i \ge v_{i_0}$, so $A \subseteq \{j : v_j \ge v_{i_0}\}$ and $\lvert A \rvert \le R_{i_0} \le k$. $\square$

**Claim 1 (the algorithm computes $p$).** In the two-sample case $T(gz)$ depends on $g$ only through the set of the $m$ indices that $g$ moves into the first group. Each such set arises from exactly $m!(n - m)!$ permutations, so the fraction of permutations with $T(gz) \ge T(z)$ equals the fraction of the $\binom{n}{m}$ sets, which lines L8 to L11 count. In the paired case the code lists the $2^n$ sign vectors directly. $\square$

**Claim 2 (exact level).** Under the randomization hypothesis, $P(p(Z) \le \alpha) \le \alpha$ for every $\alpha \in [0, 1]$.

*Proof.* Let $\Gamma$ be uniform on $G$ and independent of $Z$. For each fixed $g$, $gZ \overset{d}{=} Z$, so also $\Gamma Z \overset{d}{=} Z$, and it suffices to bound $P(p(\Gamma Z) \le \alpha)$.

Fix $z$. Because $G$ is a group, $\{g h z : g \in G\}$ is the same multiset as $\{g z : g \in G\}$ for each $h \in G$. So $p(hz) = R_h / K$, where $R_h = \#\{g : T(gz) \ge T(hz)\}$ is the rank count of the value $v_h = T(hz)$ among the $K$ values $(v_g)_{g \in G}$. By the lemma with $k = \lfloor \alpha K \rfloor$,

$$P(p(\Gamma z) \le \alpha) = \frac{\#\{h : R_h \le \alpha K\}}{K} \le \frac{\lfloor \alpha K \rfloor}{K} \le \alpha.$$

This holds for every $z$. Since $\Gamma$ is independent of $Z$, averaging over $Z$ gives $P(p(\Gamma Z) \le \alpha) \le \alpha$. $\square$

If the values $T(gz)$, $g \in G$, are distinct and $\alpha K$ is an integer, the set in the lemma has exactly $\alpha K$ elements, and the size is exactly $\alpha$. In general, a test that also rejects with a suitable probability when $T(Z)$ equals the boundary value has size exactly $\alpha$; this is the randomized permutation test.

**Claim 3 (the Monte Carlo p-value is valid).** Let $g_1, \ldots, g_b$ be independent and uniform on $G$ and independent of $Z$, and let $c = \#\{j : T(g_j Z) \ge T(Z)\}$. Under the randomization hypothesis, $P((1 + c)/(1 + b) \le \alpha) \le \alpha$ for every $\alpha \in [0, 1]$ and every $b \ge 1$.

*Proof.* Let $\Gamma$ be uniform on $G$, independent of $Z$ and of the $g_j$, and put $Y = \Gamma Z$. Since $Y \overset{d}{=} Z$ and the $g_j$ are independent of both, the tuple $(Y, g_1, \ldots, g_b)$ has the same law as $(Z, g_1, \ldots, g_b)$. So the p-value has the same law when it is computed from $Y$, that is, from the values $V_0 = T(\Gamma Z)$ and $V_j = T(g_j \Gamma Z)$ for $j = 1, \ldots, b$.

Condition on $Z = z$. The elements $\Gamma, g_1 \Gamma, \ldots, g_b \Gamma$ are independent and uniform on $G$: given $\Gamma$, each $g_j \Gamma$ is uniform because $g \mapsto g \Gamma$ is a bijection of $G$, and the $g_j$ are independent of each other and of $\Gamma$. So $V_0, V_1, \ldots, V_b$ are independent and identically distributed given $Z = z$, and in particular exchangeable.

Let $R_i = \#\{j \in \{0, \ldots, b\} : V_j \ge V_i\}$. The p-value is $(1 + c)/(1 + b) = R_0/(b + 1)$. By exchangeability $P(R_0 \le k) = P(R_i \le k)$ for each $i$, so with $k = \lfloor \alpha (b + 1) \rfloor$ and the lemma,

$$P\Big(\frac{R_0}{b + 1} \le \alpha\Big) = P(R_0 \le k) = \frac{1}{b + 1} E\big[\#\{i : R_i \le k\}\big] \le \frac{\lfloor \alpha (b + 1) \rfloor}{b + 1} \le \alpha.$$

This holds given $Z = z$ for every $z$, so it holds without conditioning. $\square$

The proof also shows why $c/b$ is not a valid p-value. For a continuous statistic, $c = 0$ has probability $1/(b + 1)$ under $H_0$, so the rule "reject when $c/b \le \alpha$" has size at least $1/(b + 1)$ for every $\alpha \ge 0$.

**Claim 4 (cost).** The Monte Carlo loop does $b$ shuffles of $\Theta(n)$ swaps each and $b$ evaluations of $T$. The exact loop evaluates $T$ on $\binom{n}{m}$ splits. With $T$ the difference of the means, each evaluation costs $\Theta(n)$, which gives $\Theta(b n)$ and $\Theta(n \binom{n}{m})$. Both keep one copy of the data, so the extra space is $\Theta(n)$. $\square$
