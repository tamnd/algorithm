---
title: The hit probability, the trial count and the EM ascent of PROJECTION
proves: [correctness]
status: full
---

Let $M$ be a motif of length $L$ and let each sequence $s_i$ hold a copy $c_i$ of $M$ that differs from $M$ at exactly the positions of a set $D_i$ with $|D_i| = d$. A trial draws a set $I$ of $k$ positions, uniform among the $\binom{L}{k}$ sets (line L3), and the bucket of a window $x$ is $h_I(x) = (x_j)_{j \in I}$ (line L4).

**Lemma 1 (when a copy hits).** $h_I(c_i) = h_I(M)$ if and only if $I \cap D_i = \emptyset$.

*Proof.* The projections agree when $c_i$ and $M$ have the same letter at every $j \in I$. They have the same letter exactly at the positions outside $D_i$. $\square$

**Theorem 1 (the hit probability).** If $D_i$ is a uniform random $d$-set, independent of $I$, then $\Pr[h_I(c_i) = h_I(M)] = p = \binom{L-d}{k}/\binom{L}{k}$. The same holds for a fixed $D_i$ and a uniform $I$.

*Proof.* For a fixed $D_i$, the sets $I$ that avoid it are the $k$-subsets of the other $L - d$ positions, so by Lemma 1 the probability is $\binom{L-d}{k}/\binom{L}{k}$. This does not depend on $D_i$, so averaging over a random $D_i$ gives the same value. $\square$

When a change may keep the letter (a copy with at most $d$ differences), Lemma 1 gives only "if", and $p$ is a lower bound.

**Theorem 2 (one trial).** If $D_1, \ldots, D_n$ are independent uniform $d$-sets, independent of $I$, the number $H$ of copies in the bucket $h_I(M)$ is $\mathrm{Bin}(n, p)$, and a trial gives $H \ge s$ with probability $P = \Pr[\mathrm{Bin}(n, p) \ge s]$.

*Proof.* Condition on $I$. The events $I \cap D_i = \emptyset$ are independent, since the $D_i$ are, and each has probability $\binom{L-d}{k}/\binom{L}{k}$ for every fixed $I$, by the count of Theorem 1 with the roles of $I$ and $D_i$ exchanged: of the $\binom{L}{d}$ sets $D_i$, $\binom{L-k}{d}$ avoid $I$, and $\binom{L-k}{d}/\binom{L}{d} = \binom{L-d}{k}/\binom{L}{k}$, since both equal $\frac{(L-k)!\,(L-d)!}{L!\,(L-k-d)!}$. So given $I$, $H$ is $\mathrm{Bin}(n, p)$, and the same holds without the condition. $\square$

For a fixed input, the $D_i$ are fixed, and the events $I \cap D_i = \emptyset$ share the one random $I$, so they are not independent in general. Then $\Pr[H \ge s]$ can differ from $P$, while $\mathrm{E}[H] = np$ still holds by Theorem 1 and linearity.

**Theorem 3 (the number of trials).** With $m$ trials that use independent projections, the chance that at least one trial gives $H \ge s$ is $1 - (1 - P)^m$. The least $m$ with $1 - (1 - P)^m \ge q$, for $0 < P < 1$ and $0 < q < 1$, is $\lceil \log(1 - q)/\log(1 - P) \rceil$.

*Proof.* Under the model of Theorem 2, the trials are independent and each fails with probability $1 - P$. The inequality $(1 - P)^m \le 1 - q$ is the same as $m \ge \log(1 - q)/\log(1 - P)$, since $\log(1 - P) < 0$. $\square$

The function `trials_needed` starts from this value and corrects it by one step up or down against the floating-point test of the inequality, so it returns the least $m$ for which the computed inequality holds.

**Lemma 2 (the threshold is checked on sequences).** Line L5 refines a bucket exactly when its windows come from at least $s$ different sequences. If a trial gives $H \ge s$, the motif's bucket is refined in that trial.

*Proof.* The code counts the distinct sequence indices of the members. The $H$ copies lie in $H$ different sequences. $\square$

**Lemma 3 (EM does not lower the score).** Let $\ell(\theta) = \sum_i \log(\frac{1}{W} \sum_q \prod_j \theta_j(x_{iq,j})/\mu(x_{iq,j}))$ and let $\theta'$ be the result of one E step and one M step of line L7 with prior counts $\beta\mu$. Then $\ell(\theta') + \beta \sum_j \sum_a \mu(a) \log \theta'_j(a) \ge \ell(\theta) + \beta \sum_j \sum_a \mu(a) \log \theta_j(a)$.

*Proof.* Up to a constant that does not depend on $\theta$, $\ell$ is the log likelihood of the model in which each sequence has one site at a uniform position, the site letters follow $\theta$ and the other letters follow $\mu$. The E step computes the posterior $z_{iq}$ of the site position. The M step maximizes $\sum_{i,q} z_{iq} \sum_j \log \theta_j(x_{iq,j}) + \beta \sum_j \sum_a \mu(a) \log \theta_j(a)$ over the columns, and for column $j$ the maximum is at $\theta_j(a) \propto \sum_{i,q} z_{iq}[x_{iq,j} = a] + \beta\mu(a)$, the rule of the code, with the sum $n + \beta$ since $\sum_q z_{iq} = 1$. By the ascent property of EM for a posterior with this Dirichlet prior (Dempster, Laird and Rubin 1977), the penalized log likelihood does not decrease. $\square$

The code records $\ell$ without the prior term. The lemma does not promise that this value never falls, so the tests check both: the penalized value of the lemma, step by step from random starts, and the recorded value, which also did not fall on the test inputs. Both checks use a tolerance of $10^{-9}$.

**What is not proved.** A good bucket gives a start near the motif, but EM may move to another fixed point, and line L8 may prefer a model from a random bucket with a higher score. So the overall success rate is measured, not proved.

**Cost.** Line L4 computes $nW$ keys of $k$ letters, $O(nWk)$. Each refined bucket costs $O(|B| L)$ for line L6 and $O(I\,nWL)$ for $I$ EM iterations of line L7. So a trial with $B$ refined buckets costs $O(nWk + B\,I\,nWL)$, and $m$ trials $m$ times that. The buckets take $O(nW)$ space.
