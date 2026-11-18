---
title: TruthFinder computes well-defined trust and confidence values, stops, and starts as a vote
proves: [correctness, termination, complexity]
status: full
---

We use the pseudocode of the page. $W$ is the set of sources, each fact $f$ is a pair (object, value), $W(f)$ is the set of sources that claim $f$, and $F(w)$ is the set of facts that $w$ claims, which is not empty. The implication $\mathrm{imp}(f' \to f)$ is a number in $[-1, 1]$, and $0 < t_0 < 1$, $\rho \ge 0$, $\gamma > 0$, $\delta \ge 0$, and the cap $T \ge 1$.

TruthFinder is a heuristic: nothing here says that the facts with the highest confidence are true, and nothing says that the iteration converges. The claims below are about what the method computes.

**Lemma 1 (the values are defined).** At the start of each iteration, $0 < t(w) < 1$ for every source. In each iteration every $\tau(w)$, $\sigma(f)$, $\sigma^*(f)$ is a finite real number, and $0 < s(f) < 1$.

*Proof.* By induction on the iterations. Line L1 sets $t(w) = t_0 \in (0, 1)$. If $0 < t(w) < 1$, then $1 - t(w) \in (0, 1)$, so $\tau(w) = -\ln(1 - t(w))$ in line L3 is a finite positive number. Line L4 sums finitely many of them, and line L5 adds a finite sum of finite terms. Line L6 applies the logistic function $x \mapsto 1/(1 + e^{-\gamma x})$, whose values lie strictly between 0 and 1 for every real $x$. Line L7 sets $t(w)$ to a mean of values in $(0, 1)$ over the non-empty set $F(w)$, which again lies in $(0, 1)$. $\square$

In floating point, $s(f)$ can round to 1 when $\gamma \sigma^*(f)$ is very large; the implementation keeps $1 - t(w)$ away from 0 before it takes the logarithm.

**Lemma 2 (the meaning of $\sigma$).** For each fact, $1 - e^{-\sigma(f)} = 1 - \prod_{w \in W(f)} (1 - t(w))$.

*Proof.* $e^{-\sigma(f)} = \prod_{w \in W(f)} e^{-\tau(w)} = \prod_{w \in W(f)} (1 - t(w))$. $\square$

So, if each source is right with probability $t(w)$, independently of the others, $1 - e^{-\sigma(f)}$ is the probability that at least one source of $f$ is right. This is the basic model of Yin, Han and Yu; lines L5 and L6 then change it, and the independence is an assumption, not a fact about the data. The logistic function with $\gamma < 1$ is their correction for sources that copy each other, and it is a heuristic.

**Lemma 3 (the first iteration is a vote).** Suppose $\mathrm{imp} = 0$, or $\mathrm{imp}(f' \to f) = -c$ with a constant $c \ge 0$ for any two different facts on one object. Then after the first iteration, for any two facts $f, g$ on the same object, $s(f) > s(g)$ if and only if $|W(f)| > |W(g)|$.

*Proof.* In the first iteration every source has $t = t_0$, so $\tau(w) = \tau_0 = -\ln(1 - t_0) > 0$ and $\sigma(f) = \tau_0 k_f$ with $k_f = |W(f)|$. Let $K$ be the sum of $k_{f'}$ over the facts $f'$ on the object of $f$. Then
$$\sigma^*(f) = \tau_0 k_f - \rho c \tau_0 (K - k_f) = \tau_0 \big( (1 + \rho c) k_f - \rho c K \big),$$
which grows strictly with $k_f$, since $K$ is the same for $f$ and $g$. The logistic function is strictly increasing. $\square$

So the answers after one iteration are those of a vote, up to ties, and the later iterations change the answers only through the trust values. The tests check this on generated data.

**Termination.** Each pass of lines L3 to L8 counts one iteration, and line L8 stops the loop when the iteration count reaches $T$, whatever the values. So the loop stops after at most $T$ iterations. It can stop earlier, when $1 - \cos(t_{\text{old}}, t) < \delta$. With only one source, both vectors have one positive entry, so the cosine is 1 and the loop stops after the first iteration.

**Cost of one iteration.** Let $C$ be the number of claims and $d_o$ the number of different facts on object $o$. Lines L3 and L7 take $O(|W| + C)$, line L4 takes $O(C)$, line L5 takes $O(\sum_o d_o^2)$ calls of imp, and line L6 takes one step per fact. With imp in constant time an iteration takes $O(|W| + C + \sum_o d_o^2)$, and the whole run at most $T$ times that. Line L9 takes one pass over the facts. $\blacksquare$

**What is not proved.** The map from the trust vector to the next trust vector is continuous and maps $(0, 1)^{|W|}$ into itself, but the method has no proof that the iteration converges, that its limit is unique, or that it ranks true facts first. Yin, Han and Yu report that the trust values settle after a few iterations on their data; that is a measurement.
