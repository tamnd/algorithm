---
title: A PRF applied to an almost universal function is a PRF, which gives the outer step of the NMAC proof
proves: [correctness]
status: full
---

**Setting.** Let $\mathcal{M}$ be a set of messages and $Y = \{0,1\}^c$. Let $F : \mathcal{K}_2 \times \mathcal{M} \to Y$ be a keyed function that is $\varepsilon$-almost universal: for all $m \neq m'$ in $\mathcal{M}$,
$$\Pr_{k_2}[F_{k_2}(m) = F_{k_2}(m')] \le \varepsilon,$$
with $k_2$ uniform in $\mathcal{K}_2$. Let $g : \mathcal{K}_1 \times Y \to \{0,1\}^n$ be a keyed function. The composition is $h_{k_1, k_2}(m) = g_{k_1}(F_{k_2}(m))$. For NMAC, $F$ is the keyed iterated hash and $g_{k_1}(y) = f(k_1, y \| \mathrm{pad}(c))$.

The PRF advantage of an adversary $A$ against a keyed function $h$ is $\mathrm{Adv}^{\mathrm{prf}}_h(A) = |\Pr[A^{h_k} = 1] - \Pr[A^{\rho} = 1]|$, where $k$ is a uniform key and $\rho$ is a uniform random function with the same domain and range. We assume that $A$ never repeats a query; repeats give no information.

**Theorem.** For every adversary $A$ that makes $q$ queries to $h$, there is an adversary $B$ that makes $q$ queries to $g$ and runs in the time of $A$ plus $q$ evaluations of $F$, such that
$$\mathrm{Adv}^{\mathrm{prf}}_h(A) \le \mathrm{Adv}^{\mathrm{prf}}_g(B) + \binom{q}{2}\varepsilon.$$

*Proof.* We use three games. In each game $A$ asks the oracle on distinct messages $m_1, \ldots, m_q$, each chosen after it has seen the answers to the earlier ones, and then outputs a bit.

- $G_0$: the oracle answers $g_{k_1}(F_{k_2}(m_i))$ for uniform $k_1, k_2$.
- $G_1$: the oracle answers $R(F_{k_2}(m_i))$, where $R : Y \to \{0,1\}^n$ is a uniform random function and $k_2$ is uniform.
- $G_2$: the oracle answers $\rho(m_i)$, where $\rho$ is a uniform random function on $\mathcal{M}$.

Write $p_j = \Pr[A \text{ outputs } 1 \text{ in } G_j]$. Then $\mathrm{Adv}^{\mathrm{prf}}_h(A) = |p_0 - p_2| \le |p_0 - p_1| + |p_1 - p_2|$.

*Step 1: $|p_0 - p_1| = \mathrm{Adv}^{\mathrm{prf}}_g(B)$.* The adversary $B$ has an oracle $O$, which is either $g_{k_1}$ for a uniform $k_1$ or a uniform random function $R$ on $Y$. $B$ picks $k_2$ uniformly, runs $A$, and answers each query $m_i$ with $O(F_{k_2}(m_i))$. When $O = g_{k_1}$, the view of $A$ is exactly its view in $G_0$; when $O = R$, it is exactly its view in $G_1$. $B$ outputs what $A$ outputs. So $B$ makes $q$ queries, and its advantage is $|p_0 - p_1|$.

*Step 2: $|p_1 - p_2| \le \binom{q}{2}\varepsilon$.* Let $\mathrm{BAD}$ be the event that $F_{k_2}(m_i) = F_{k_2}(m_j)$ for some $i < j$. We run $G_1$ and $G_2$ on the same random choices: the coins of $A$, the key $k_2$, and a list $r_1, r_2, \ldots, r_q$ of independent uniform values in $\{0,1\}^n$. In $G_2$, the answer to the $i$-th query is $r_i$; because the queries are distinct and $\rho$ is uniform, this has the correct distribution. In $G_1$, the answer to the $i$-th query is $r_i$ if $F_{k_2}(m_i)$ differs from all earlier $F_{k_2}(m_j)$, and it is the earlier answer $r_j$ if $F_{k_2}(m_i) = F_{k_2}(m_j)$; this has the distribution of $R(F_{k_2}(m_i))$ for a uniform random function $R$, because $R$ gives a fresh uniform value on each new point and the old value on a repeated point.

As long as $\mathrm{BAD}$ has not happened, both games give the same answers, so $A$ asks the same next query in both. Hence the two games differ only if $\mathrm{BAD}$ happens, and $|p_1 - p_2| \le \Pr[\mathrm{BAD}]$, where we may compute $\Pr[\mathrm{BAD}]$ in $G_2$ (the event is the same in both coupled runs up to its first occurrence).

In $G_2$ the answers $r_i$ do not depend on $k_2$, so the messages $m_1, \ldots, m_q$ are a function of the coins of $A$ and of $r_1, \ldots, r_q$ only, and they are independent of $k_2$. Fix the coins of $A$ and the $r_i$; this fixes $q$ distinct messages. For each pair $i < j$, almost universality gives $\Pr_{k_2}[F_{k_2}(m_i) = F_{k_2}(m_j)] \le \varepsilon$. By the union bound over the $\binom{q}{2}$ pairs, $\Pr[\mathrm{BAD}] \le \binom{q}{2}\varepsilon$ for every fixed choice, so also on average.

*Conclusion.* $\mathrm{Adv}^{\mathrm{prf}}_h(A) \le \mathrm{Adv}^{\mathrm{prf}}_g(B) + \binom{q}{2}\varepsilon$. $\blacksquare$

**How NMAC uses it.** In NMAC, $g_{k_1}(y) = f(k_1, y \| \mathrm{pad}(c))$. The map $y \mapsto y \| \mathrm{pad}(c)$ is injective, so if $f$ is a PRF keyed through its chaining input, then $g$ is a PRF with the same advantage. Bellare (CRYPTO 2006) shows that the iterated $F$ is computationally almost universal when $f$ is a PRF, with $\varepsilon$ replaced by a term of order $\ell \cdot \mathrm{Adv}^{\mathrm{prf}}_f + 2^{-c}$ for messages of at most $\ell$ blocks; a computational variant of Step 2 then gives the NMAC theorem with the loss of order $q^2 \ell$. That part is cited, not proved here.

**Why $F$ alone is not a PRF.** For any $m$ of $|m|$ bits and any suffix $s$, let $m^{+} = m \| \mathrm{pad}(|m|) \| s$. Then $F_k(m^{+}) = f^{*}(F_k(m), s \| \mathrm{pad}(|m^{+}|))$, because the blocks of $m \| \mathrm{pad}(|m|)$ are processed first and give the chaining value $F_k(m)$. An adversary who asks $F_k(m)$ computes $F_k(m^{+})$ with no key and checks it with a second query. A random function passes this check with probability $2^{-c}$, so $F$ has PRF advantage close to 1. The outer layer of NMAC hides $F_{k_2}(m)$, which blocks this attack.
