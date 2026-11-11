---
title: RSA-FDH is EUF-CMA in the random oracle model with a loss of about e times q_s (Coron 2000)
proves: [security]
status: full
---

We use the notation of the page. The model is the random oracle model: $H$ is a uniformly random function from $\{0,1\}^*$ to $\mathbb{Z}_N^*$, and every party gets it only through oracle queries. The forger $F$ gets the public key $(N, e)$, the hash oracle and a signing oracle that returns $H(m)^d \bmod N$. $F$ runs in time $t$, makes $q_h$ hash queries and $q_s$ signing queries, and wins if it outputs $(m^*, \sigma^*)$ with $\sigma^{*e} \equiv H(m^*) \pmod N$ and $m^*$ never submitted to the signing oracle. Its success probability is $\varepsilon$. The RSA problem is: given $(N, e)$ and a uniform $y \in \mathbb{Z}_N^*$, find $x$ with $x^e \equiv y \pmod N$.

**Convention.** We assume that $F$ never repeats a query, that it asks $H(m)$ before it asks for a signature on $m$, and that it asks $H(m^*)$ before it outputs. A forger that does not do this can be changed into one that does, with at most $q_s + 1$ more hash queries; we count $q_h$ after this change, so $q_h \ge q_s + 1$.

**Theorem (Coron 2000).** If $F$ is as above with $q_s \ge 1$, then there is an inverter $I$ for the RSA problem that runs in time $t' = t + (q_h + q_s + 1) \cdot O(k^3)$ and succeeds with probability

$$\varepsilon' \ge \frac{\varepsilon}{q_s (1 + 1/q_s)^{q_s + 1}} \ge \frac{\varepsilon}{4 q_s}.$$

As $q_s$ grows, $(1 + 1/q_s)^{q_s + 1}$ decreases to $\mathrm{e} = 2.718\ldots$, so the loss is about $\mathrm{e} \cdot q_s$.

*Proof.* Fix a number $p_0 \in [0, 1]$, to be chosen at the end.

**Step 1 (the inverter).** $I$ gets $(N, e, y)$. It runs $F$ on the public key $(N, e)$ and answers its queries as follows.

- *Hash query $m$.* $I$ picks $r$ uniformly in $\mathbb{Z}_N^*$ and a bit $c$ that is 0 with probability $p_0$ and 1 otherwise, independently of everything else. It answers $H(m) = r^e \bmod N$ if $c = 0$ and $H(m) = y \cdot r^e \bmod N$ if $c = 1$, and stores $(m, r, c)$.
- *Signing query $m$.* By the convention, $(m, r, c)$ is stored. If $c = 0$, $I$ answers $r$. If $c = 1$, $I$ stops and fails.
- *Output $(m^*, \sigma^*)$.* By the convention, $(m^*, r^*, c^*)$ is stored. If $c^* = 1$ and $\sigma^{*e} \equiv H(m^*) \pmod N$, $I$ outputs $x = \sigma^* \cdot r^{*-1} \bmod N$. Otherwise it fails.

**Step 2 (the answers have the right distribution).** The map $r \mapsto r^e \bmod N$ is a permutation of $\mathbb{Z}_N^*$, by Lemma 1 of the correctness proof restricted to units. So $r^e$ is uniform on $\mathbb{Z}_N^*$ when $r$ is. Multiplication by the unit $y$ is also a permutation of $\mathbb{Z}_N^*$, so $y r^e$ is uniform as well. Hence each hash answer is uniform on $\mathbb{Z}_N^*$ and independent of the earlier answers, whatever its bit $c$, which is the distribution of a random oracle. A signing answer $r$ for $c = 0$ satisfies $r^e \equiv H(m)$, and since RSA is a permutation it is the unique valid signature $H(m)^d \bmod N$, which is what the real signing oracle returns.

**Step 3 (the bits are hidden).** Consider a thought experiment $E$ in which $I$ never stops on a signing query with $c = 1$, but answers it with the true value $H(m)^d \bmod N$. By Step 2, the view of $F$ in $E$ (its coins and all answers) has exactly the distribution of the real EUF-CMA game in the random oracle model, so $F$ wins in $E$ with probability $\varepsilon$. In $E$ the value $H(m)$ is uniform on $\mathbb{Z}_N^*$ for both values of $c$, and the signing answer is a function of $H(m)$. So the view of $F$ is independent of the vector of bits $c$, and conditioned on the view the bits are still independent, each 0 with probability $p_0$.

**Step 4 (when $I$ succeeds).** Let $S$ be the set of messages that $F$ submits to the signing oracle in $E$, so $|S| \le q_s$, and let $m^*$ be its output. Both are functions of the view. Suppose that $F$ wins in $E$, that $c = 0$ for every $m \in S$, and that $c^* = 1$ for $m^*$. Then $I$ and $E$ behave the same on every query, because $I$ differs from $E$ only on signing queries with $c = 1$, and there are none. So $I$ reaches the output step with the winning pair, and $\sigma^{*e} \equiv H(m^*) = y \cdot r^{*e} \pmod N$. Then $x = \sigma^* r^{*-1}$ satisfies $x^e \equiv \sigma^{*e} r^{*-e} \equiv y \pmod N$, so $I$ solves the instance.

**Step 5 (the probability).** A winning $m^*$ is not in $S$. By Step 3, conditioned on any view in which $F$ wins, the bits of the at most $q_s + 1$ distinct messages in $S \cup \{m^*\}$ are independent, so the event of Step 4 has conditional probability $p_0^{|S|}(1 - p_0) \ge p_0^{q_s}(1 - p_0)$. Hence

$$\varepsilon' \ge \varepsilon \cdot p_0^{q_s}(1 - p_0).$$

**Step 6 (the best $p_0$).** The function $f(p_0) = p_0^{q_s}(1 - p_0)$ on $[0, 1]$ has derivative $p_0^{q_s - 1}(q_s - (q_s + 1)p_0)$, which is positive for $p_0 < q_s/(q_s + 1)$ and negative after it. So the maximum is at $p_0 = q_s/(q_s + 1)$, where

$$f = \Bigl(\frac{q_s}{q_s + 1}\Bigr)^{q_s} \frac{1}{q_s + 1} = \frac{q_s^{q_s}}{(q_s + 1)^{q_s + 1}} = \frac{1}{q_s} \Bigl(\frac{q_s}{q_s + 1}\Bigr)^{q_s + 1} = \frac{1}{q_s (1 + 1/q_s)^{q_s + 1}}.$$

The sequence $(1 + 1/n)^{n+1}$ is decreasing in $n \ge 1$ with limit $\mathrm{e}$, and it equals 4 at $n = 1$, so $f \ge 1/(4 q_s)$.

**Step 7 (the time).** $I$ runs $F$ and, for each of the $q_h$ hash queries, computes one exponentiation $r^e \bmod N$ and at most one multiplication. Each signing answer is a table lookup, and the output step costs one inversion and one exponentiation. With $O(k^3)$ per exponentiation, $t' = t + (q_h + q_s + 1) \cdot O(k^3)$. $\blacksquare$

**The loss of Bellare and Rogaway.** The proof of Bellare and Rogaway (1996, Theorem 3.1) guesses which hash query will be the forged message: it plants $y$ in one query chosen uniformly among $q_h + q_s + 1$ and answers all others with $r^e$. It fails when the guess is wrong, so $\varepsilon' \ge \varepsilon / (q_s + q_h + 1)$. Coron's random choice of the bit $c$ replaces $q_h$ by $q_s$ in the loss, and $q_s$ is usually much smaller, because signatures need the signer while hash queries are offline work.

**A real hash into $\mathbb{Z}_N$.** The theorem uses a random oracle into $\mathbb{Z}_N^*$. A random oracle into $\mathbb{Z}_N$ differs from it only when an answer is a non-unit, which has probability $(p + q - 1)/N$ per query; over all queries this adds at most $(q_h + q_s + 1)(p + q - 1)/N$ to the bound, and such an answer would reveal a factor of $N$.
