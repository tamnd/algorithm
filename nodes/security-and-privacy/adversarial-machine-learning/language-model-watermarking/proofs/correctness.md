---
title: The green list detector has a bounded false-positive rate, the bonus never lowers the green mass, and edits lower the count by at most two each
proves: [correctness]
status: full
---

Let $V$ be the vocabulary, $g = \lfloor \gamma |V| \rfloor$ with $1 \le g \le |V| - 1$, and $\gamma' = g / |V|$. For a previous token $u$, let $G(u)$ be the green list of lines L7 and L8. We model the keyed hash $H$ as a random function: the sets $G(u)$ for different $u$ are independent, and each is uniformly random among the subsets of $V$ of size $g$. A text $s = (s_0, \dots, s_T)$ does not depend on the key if it is fixed before the key is drawn, or drawn independently of it.

For a text $s$, let $P(s)$ be the set of distinct pairs $(s_{t-1}, s_t)$ with $1 \le t \le T$. Lines L9 to L13 set $\mathrm{scored} = |P(s)|$ and $\mathrm{count} = |\{(u, v) \in P(s) : v \in G(u)\}|$, because line L11 skips a pair exactly when it is already in the set $\mathrm{seen}$, and line L12 adds each new pair once.

**Lemma 1 (Hoeffding).** Let $X_1, \dots, X_m$ be a sample without replacement from a finite list of numbers in $[0, 1]$ with mean $\mu$, and let $Y_1, \dots, Y_m$ be independent draws with replacement from the same list. Then $E[e^{\lambda \sum X_i}] \le E[e^{\lambda \sum Y_i}]$ for every real $\lambda$.

Hoeffding (1963) proved this comparison for every continuous convex function in place of $e^{\lambda x}$. We use it without proof.

**Lemma 2 (Hoeffding's lemma).** If $Y$ takes values in $[0, 1]$ with mean $\mu$, then $E[e^{\lambda (Y - \mu)}] \le e^{\lambda^2 / 8}$ for every real $\lambda$.

This is the standard lemma behind [Hoeffding's inequality](/hoeffding-inequality/). We use it without proof.

**Theorem 1 (false positives).** Let $s$ not depend on the key, let $N = |P(s)| \ge 1$, and let $z^* > 0$. Then $P(z > z^*) \le e^{-2 z^{*2} \gamma'(1 - \gamma')}$, where $z$ is the value of line L14. If $N = 0$, then $z = 0$ and DETECT returns false.

*Proof.* The set $P(s)$ is fixed, because $s$ does not depend on the key. Group its pairs by the first token: for each $u$, let $v_1, \dots, v_{m_u}$ be the distinct tokens with $(u, v_i) \in P(s)$, so $\sum_u m_u = N$. Let $C_u = \sum_i 1\{v_i \in G(u)\}$, so $\mathrm{count} = \sum_u C_u$.

Fix $u$. Since $G(u)$ is a uniform subset of size $g$, the green status of the distinct tokens $v_1, \dots, v_{m_u}$ has the same distribution as $m_u$ draws without replacement from a list of $|V|$ numbers, $g$ of them equal to 1 and the rest equal to 0: label the tokens of $V$ by $1\{v \in G(u)\}$; by symmetry this labeling is a uniform random arrangement of the list, and reading it at $m_u$ fixed distinct places is a sample without replacement. The list has mean $\gamma'$. By Lemma 1 and then Lemma 2, for every $\lambda > 0$,

$E[e^{\lambda (C_u - \gamma' m_u)}] \le \prod_{i=1}^{m_u} E[e^{\lambda (Y_i - \gamma')}] \le e^{m_u \lambda^2 / 8}$,

where the $Y_i$ are independent Bernoulli variables with mean $\gamma'$.

The variables $C_u$ for different $u$ are functions of different, independent sets $G(u)$, so they are independent, and

$E[e^{\lambda (\mathrm{count} - \gamma' N)}] = \prod_u E[e^{\lambda (C_u - \gamma' m_u)}] \le e^{N \lambda^2 / 8}$.

By Markov's inequality, for $a > 0$, $P(\mathrm{count} - \gamma' N \ge a) \le e^{-\lambda a + N \lambda^2 / 8}$, and the choice $\lambda = 4a / N$ gives $P(\mathrm{count} - \gamma' N \ge a) \le e^{-2a^2 / N}$.

Line L14 gives $z > z^*$ exactly when $\mathrm{count} - \gamma' N > z^* \sqrt{N \gamma'(1 - \gamma')}$. Take $a = z^* \sqrt{N \gamma'(1 - \gamma')} > 0$. Then $P(z > z^*) \le P(\mathrm{count} - \gamma' N \ge a) \le e^{-2 z^{*2} N \gamma'(1 - \gamma') / N} = e^{-2 z^{*2}\gamma'(1 - \gamma')}$. If $N = 0$, the code returns $z = 0$, and $0 > z^*$ is false. $\square$

**Lemma 3 (the bonus helps).** Let a step have the distribution $p = \mathrm{softmax}(z)$ and let $q = \sum_{v \in G} p_v$. After line L4 the green mass is $q' = e^\delta q / (e^\delta q + 1 - q)$. If $\delta \ge 0$, then $q' \ge q$, and if $\delta > 0$ the equality holds only for $q \in \{0, 1\}$.

*Proof.* Adding $\delta$ to the logit of a token multiplies its unnormalized weight $e^{z_v}$ by $e^\delta$. With $Z = \sum_v e^{z_v}$, the green weight becomes $e^\delta q Z$ and the red weight stays $(1 - q) Z$, so $q' = e^\delta q / (e^\delta q + 1 - q)$. Let $a = e^\delta \ge 1$. Then $q' - q = q (a - (a q + 1 - q)) / (a q + 1 - q) = q (1 - q)(a - 1) / (a q + 1 - q) \ge 0$, since the denominator is at least $1 - q + q = 1 > 0$. For $a > 1$ the numerator is zero exactly when $q = 0$ or $q = 1$. $\square$

**Theorem 2 (edits).** Let $s'$ be the text $s$ with the tokens at $m$ positions $p_1, \dots, p_m \in \{1, \dots, T\}$ changed, with the same key. Then $\mathrm{count}(s') \ge \mathrm{count}(s) - 2m$.

*Proof.* The pair at position $t$ is $(s_{t-1}, s_t)$, so it changes only if $t$ or $t - 1$ is an edited position. Let $A = \{p_i\} \cup \{p_i + 1\}$, a set of at most $2m$ positions. For $t \notin A$, the pair of $s'$ at position $t$ is the same as the pair of $s$ at position $t$. So every pair of $P(s)$ that occurs in $s$ at some position outside $A$ is also in $P(s')$, and $P(s) \setminus P(s')$ holds only pairs that occur in $s$ only at positions in $A$; there are at most $|A| \le 2m$ such pairs. The green status of a pair $(u, v)$ depends only on $G(u)$, which is the same for both texts, so the green pairs of $P(s)$ that are lost number at most $2m$, and new pairs can only add to the count. Hence $\mathrm{count}(s') \ge \mathrm{count}(s) - 2m$. $\blacksquare$
