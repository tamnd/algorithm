---
title: The binomial test returns the exact tail probabilities, and each p-value is valid
proves: [correctness]
status: full
---

We use the pseudocode of the page. Let $X \sim \text{Binomial}(n, p_0)$ and write $b(k) = \binom{n}{k} p_0^k (1 - p_0)^{n-k}$ for $k = 0, \ldots, n$. All arithmetic is exact in this proof; the last part says what changes in floating point.

**Claim 1 (the returned values).** Line L1 sets $w[k] = b(k)$. Lines L2 and L3 give $P_{hi}(x) = \sum_{k \ge x} b(k) = P_{p_0}(X \ge x)$ and $P_{lo}(x) = \sum_{k \le x} b(k) = P_{p_0}(X \le x)$. Lines L4 and L5 return these for the one-sided alternatives. Lines L6 to L8 return, for $\delta = 0$,

$$p_{ml}(x) = \sum_{k : b(k) \le b(x)} b(k) = P_{p_0}\big(b(X) \le b(x)\big),$$

which is at most $1$, so the minimum in line L8 has no effect in exact arithmetic. The doubling rule of the code returns $p_{d}(x) = \min\{1, 2 \min(P_{lo}(x), P_{hi}(x))\}$. These are the definitions on the page. $\square$

**Lemma (a tail p-value is valid).** Let $X$ take finitely many values, let $T$ be any real function of $X$, and let $p(x) = P(T(X) \ge T(x))$. Then $P(p(X) \le u) \le u$ for every $u \in [0, 1]$.

*Proof.* Let $A = \{x : p(x) \le u\}$ be the set of values in the support with a p-value at most $u$. If $A$ is empty, the probability is $0$. Otherwise $A$ is finite, so it has an element $x^*$ with the smallest value of $T$. Each $x \in A$ has $T(x) \ge T(x^*)$, so $A \subseteq \{x : T(x) \ge T(x^*)\}$. Hence $P(X \in A) \le P(T(X) \ge T(x^*)) = p(x^*) \le u$. $\square$

**Claim 2 (validity).** Under $H_0$, for every $\alpha \in [0, 1]$, each of the four p-values satisfies $P_{p_0}(p(X) \le \alpha) \le \alpha$. So the test that rejects when $p(x) \le \alpha$ has size at most $\alpha$.

*Proof.* Apply the lemma with these choices of $T$.

- $P_{hi}$: take $T(x) = x$.
- $P_{lo}$: take $T(x) = -x$.
- $p_{ml}$: take $T(x) = -b(x)$. Then $T(X) \ge T(x)$ if and only if $b(X) \le b(x)$.
- $p_d$: if $p_d(x) \le \alpha$ then $P_{lo}(x) \le \alpha/2$ or $P_{hi}(x) \le \alpha/2$. By the lemma each of these events has probability at most $\alpha/2$, so their union has probability at most $\alpha$. $\square$

**Claim 3 (the tolerance keeps validity).** With $\delta > 0$ in line L6, the code returns $p_\delta(x) = P_{p_0}(b(X) \le (1 + \delta) b(x)) \ge p_{ml}(x)$. So $\{x : p_\delta(x) \le \alpha\} \subseteq \{x : p_{ml}(x) \le \alpha\}$, and Claim 2 gives $P(p_\delta(X) \le \alpha) \le \alpha$. A larger $\delta$ can only make the test more conservative. Its purpose is to count two exactly equal probabilities, such as $b(k)$ and $b(n - k)$ when $p_0 = 1/2$, as equal after rounding. $\square$

**Floating point.** The code forms each $b(k)$ as $\exp$ of a sum of $\operatorname{lgamma}$ values and logarithms, so each term has a small relative error that grows with the size of the logarithms, and `math.fsum` adds the terms with one rounding. The upper and lower tails are summed directly, so a small tail is not computed as $1$ minus a number close to $1$. The tests compare the result with exact `Fraction` sums to $10^{-12}$ for $n \le 25$, and to a relative $10^{-9}$ for a tail near $10^{-37}$ at $n = 1000$.

**Cost.** Line L1 does $n + 1$ evaluations of three $\operatorname{lgamma}$ values, one $\exp$ and $O(1)$ other operations. Lines L2, L3 and L7 each scan the list once. So the time is $\Theta(n)$ in the real-RAM model with $\operatorname{lgamma}$ and $\exp$ as unit operations, and the list uses $\Theta(n)$ space. $\square$
