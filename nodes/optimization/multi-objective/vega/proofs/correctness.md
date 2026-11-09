---
title: VEGA keeps its population size, returns mutually non-dominated points, and its expected selection is a weighted sum
proves: [correctness]
status: full
---

All objectives are minimized. The population has $N$ members and there are $p$ objectives. Line numbers refer to the `pseudo id=main` block of the VEGA page. VEGA is a heuristic, so "correctness" here means the invariants that the code keeps and the exact statement about its selection. Nothing below says that VEGA reaches the Pareto front.

## Population size

**Lemma 1.** If $\lvert P \rvert = N$ before line L3, then $\lvert P \rvert = N$ after line L8.

*Proof.* Line L5 adds $\lceil N/p \rceil$ members for the first $N \bmod p$ objectives and $\lfloor N/p \rfloor$ for the rest. These sizes sum to $p \lfloor N/p \rfloor + (N \bmod p) = N$, so $\lvert M \rvert = N$ after line L4. Line L6 permutes $M$ and keeps its size. Line L7 takes the members of $M$ in consecutive pairs and makes two offspring per pair; when $N$ is odd, the last member is paired with the first and makes one offspring. So $\lvert Q \rvert = 2 \lfloor N/2 \rfloor + (N \bmod 2) = N$, and line L8 sets $P \leftarrow Q$. Line L1 makes $N$ members, so the claim holds in each generation by induction. $\square$

## The output

**Lemma 2.** Line L9 returns a nonempty set of members of the final population, no two of which dominate each other, and each member of the final population is dominated by a returned member or is returned.

*Proof.* Line L9 keeps a member $x$ exactly when no member $z$ of $P$ has $f(z) \prec f(x)$. Two returned members do not dominate each other by this rule. Dominance is a strict partial order on the finite set of images, so each member that is not returned is dominated by a minimal element, and a minimal element is returned. The set of minimal elements of a nonempty finite set is nonempty. $\square$

The returned set is the first front of the last population only. Points of earlier populations are not kept, because VEGA has no elitism.

## Expected selection (Richardson, Palmer, Liepins and Hilliard, 1989)

In Schaffer's VEGA, part $i$ of the pool is filled by proportional selection. Let $g_i(x) > 0$ be a fitness for objective $i$ to be maximized, for example $g_i = c_i - f_i$ with a constant $c_i$ larger than each $f_i$ in $P$. Let $S_i = \sum_{x \in P} g_i(x)$. Each of the $N/p$ slots of part $i$ picks member $x$ with probability $g_i(x)/S_i$, independently.

**Theorem 3.** Assume that $p$ divides $N$. The expected number of copies of $x$ in the pool $M$ is

$$E[c(x)] = \frac{N}{p} \sum_{i=1}^{p} \frac{g_i(x)}{S_i}.$$

This is equal to the expected number of copies of $x$ under proportional selection of $N$ parents with the scalar fitness $h(x) = \sum_{i} w_i\, g_i(x)$, $w_i = 1/S_i$.

*Proof.* Part $i$ has $N/p$ slots, and each slot picks $x$ with probability $g_i(x)/S_i$. By linearity of expectation, part $i$ contributes $(N/p)\, g_i(x)/S_i$, and the sum over $i$ gives the formula. Under proportional selection on $h$, each of $N$ slots picks $x$ with probability $h(x)/H$, where

$$H = \sum_{x \in P} h(x) = \sum_{i=1}^{p} \frac{1}{S_i} \sum_{x \in P} g_i(x) = \sum_{i=1}^{p} 1 = p.$$

So the expected number of copies is $N h(x)/p$, the same value. $\square$

The equality holds for the expectations only. Under VEGA the count $c(x)$ is a sum of $p$ independent binomial variables with different success probabilities; under the weighted sum it is one binomial variable. The weights $w_i = 1/S_i$ depend on the population, so they change from one generation to the next.

**Corollary 4.** If $g(x') \ge g(x)$ in each coordinate with one strict inequality, then $E[c(x')] > E[c(x)]$. A member with the largest expected count maximizes a weighted sum with positive weights over the population.

*Proof.* The weights $w_i = 1/S_i$ are positive, so $h(x') > h(x)$, and $E[c] = N h / p$. The second claim is the definition of $h$. $\square$

So a non-dominated member that does not maximize any positively weighted sum over the population, a member in a non-convex part of the front, never gets the largest expected share. The example on the VEGA page has one such member.
