---
title: Distinct random keys give a uniform order
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page with any range $M \ge n$; the page uses $M = n^3$. The calls of RANDOM are independent and uniform on $\{0, \ldots, M-1\}$. For a key vector $P = (P_0, \ldots, P_{n-1})$ with distinct entries, let $\operatorname{ord}(P)$ be the permutation $\sigma$ with $P_{\sigma(0)} < P_{\sigma(1)} < \cdots < P_{\sigma(n-1)}$. Line L5 puts $A[\sigma(p)]$ at position $p$. Because the keys are distinct, $\sigma$ does not depend on the sort that line L5 uses.

Let $D$ be the set of key vectors in $\{0, \ldots, M-1\}^n$ with distinct entries. Then $|D| = M(M-1) \cdots (M-n+1)$, and $|D| \ge 1$ because $M \ge n$.

## Lemma 1: one round

**Lemma 1.** Let $P$ be uniform on $\{0, \ldots, M-1\}^n$. For each permutation $\tau$, $\Pr[\operatorname{ord}(P) = \tau \mid P \in D] = 1/n!$.

*Proof.* Define a map from $D$ to pairs $(S, \tau)$, where $S = \{P_0, \ldots, P_{n-1}\}$ is a set of $n$ values and $\tau = \operatorname{ord}(P)$. The map is one to one: from $(S, \tau)$, write $S = \{s_0 < s_1 < \cdots < s_{n-1}\}$; then $P_{\tau(p)} = s_p$ for each $p$, which fixes $P$. The map is onto: for each $n$-set $S$ and each permutation $\tau$, the vector with $P_{\tau(p)} = s_p$ is in $D$ and maps to $(S, \tau)$. So $D$ is in bijection with the $\binom{M}{n} \cdot n!$ pairs, and for a fixed $\tau$,
$$|\{P \in D : \operatorname{ord}(P) = \tau\}| = \binom{M}{n}.$$
Every vector in $\{0, \ldots, M-1\}^n$ has probability $M^{-n}$. So
$$\Pr[\operatorname{ord}(P) = \tau \mid P \in D] = \frac{\binom{M}{n} M^{-n}}{|D| \, M^{-n}} = \frac{\binom{M}{n}}{n! \binom{M}{n}} = \frac{1}{n!}. \qquad \square$$

## Lemma 2: the loop of lines L2 to L4

Let $q = \Pr[P \in D] = |D| / M^n > 0$. Let $P^{(1)}, P^{(2)}, \ldots$ be the key vectors of the rounds; they are independent and uniform, because each round makes fresh calls of RANDOM.

**Termination.** The loop stops after round $R = \min\{r : P^{(r)} \in D\}$. Then $\Pr[R > r] = (1-q)^r \to 0$, so the loop stops with probability 1, and $E[R] = 1/q$.

**Lemma 2.** The accepted vector $P^{(R)}$ is uniform on $D$.

*Proof.* For each $x \in D$,
$$\Pr[P^{(R)} = x] = \sum_{r \ge 1} \Pr[P^{(1)} \notin D, \ldots, P^{(r-1)} \notin D, P^{(r)} = x] = \sum_{r \ge 1} (1-q)^{r-1} M^{-n} = \frac{M^{-n}}{q} = \frac{1}{|D|}.$$
This does not depend on $x$. $\square$

## The theorem

**Theorem.** PERMUTE-BY-SORTING stops with probability 1, and its output is $A[\sigma(0)], \ldots, A[\sigma(n-1)]$ with $\Pr[\sigma = \tau] = 1/n!$ for each permutation $\tau$.

*Proof.* By Lemma 2, the accepted key vector is uniform on $D$, which is the conditional distribution of $P$ given $P \in D$. By Lemma 1, $\operatorname{ord}$ of such a vector is uniform on the $n!$ permutations. Line L5 outputs the items in the order $\operatorname{ord}(P^{(R)})$. $\blacksquare$

## The bound on ties for M = n³

Let $T_{ab}$ be the event $P_a = P_b$, for $a < b$. Then $\Pr[T_{ab}] = 1/M$, and by the [union bound](/union-bound/),
$$1 - q = \Pr\Big[\bigcup_{a < b} T_{ab}\Big] \le \binom{n}{2} \frac{1}{M} = \frac{n - 1}{2n^2} < \frac{1}{2n}.$$
So $q > 1 - 1/(2n)$ and $E[R] = 1/q < 2n/(2n-1)$. The weaker bound $q \ge 1 - 1/n$ of the textbook exercise follows.

## Why a stable sort without line L4 is biased

If ties are kept and the sort is stable, a tied group keeps the input order. Then the output $\tau$ has probability $N_\tau / M^n$, where $N_\tau$ counts the vectors whose stable order is $\tau$. The identity order gets all vectors with $P_0 \le P_1 \le \cdots \le P_{n-1}$, which are $\binom{M+n-1}{n}$, while the reversed order gets only the vectors with $P_0 > \cdots > P_{n-1}$, which are $\binom{M}{n}$. For $n \ge 2$ these differ, so the output is not uniform for any finite $M$. For $n = 3$ and $M = 2$ they are $4$ and $0$. The bias goes to 0 as $M \to \infty$, since $\binom{M+n-1}{n} / \binom{M}{n} \to 1$.
