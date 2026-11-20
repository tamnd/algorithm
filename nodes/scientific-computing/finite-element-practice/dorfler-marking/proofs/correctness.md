---
title: Both marking procedures return a bulk set of minimal size
proves: [correctness]
status: full
---

**Setting.** The input is a list of numbers $\eta^2_1, \ldots, \eta^2_n \ge 0$ with $n \ge 1$, and $\theta \in (0, 1]$. Write $\Sigma = \sum_i \eta^2_i$ and $g = \theta\Sigma$. A set $S \subseteq \{1, \ldots, n\}$ is a bulk set if $\sum_{i \in S}\eta^2_i \ge g$. Let $L^*$ be the smallest size of a nonempty bulk set. It exists, because the full set is a bulk set ($\Sigma \ge \theta\Sigma$). Fix a descending order $\pi$ of the indices, $\eta^2_{\pi(1)} \ge \eta^2_{\pi(2)} \ge \cdots \ge \eta^2_{\pi(n)}$, and write $P_L = \{\pi(1), \ldots, \pi(L)\}$ for its prefixes. Arithmetic is exact (real-RAM, or Fraction in the code).

**Lemma 1 (prefixes are best).** For every $L$, the prefix $P_L$ has the largest sum among all sets of size $L$. So $L^*$ is the smallest $L \ge 1$ such that $P_L$ is a bulk set, and every prefix of a descending order of length $L^*$ is a minimal bulk set.

*Proof.* Let $|S| = L$. List the values of $S$ in descending order as $s_1 \ge \cdots \ge s_L$. The $j$-th largest value of $S$ is at most the $j$-th largest value of all indicators, $s_j \le \eta^2_{\pi(j)}$, because at least $j$ values of the whole list are at least $s_j$. Sum over $j$. If some $S$ of size $L$ is a bulk set, so is $P_L$, and the converse is trivial. $\square$

**Claim A (DORFLER-SORT, lines L1 to L6).** The output has size $L^*$ and is a bulk set.

*Proof.* Line L2 gives a descending order. The loop at line L4 adds $\pi(1), \pi(2), \ldots$ and stops before adding $\pi(L+1)$ exactly when the sum of $P_L$ is at least $g$ and $L \ge 1$. So it returns $P_L$ for the smallest $L \ge 1$ with $P_L$ a bulk set, which is $L^*$ by Lemma 1. $\square$

**Claim B (DORFLER-SELECT, lines L7 to L16).** The procedure stops, and its output has size $L^*$ and is a bulk set.

*Proof.* We prove the following invariant at the start of each pass of line L9. Write $a = |\text{marked}|$ and $c = |\text{cand}|$. There is a descending order $\pi$ of all indices with

1. marked $= \{\pi(1), \ldots, \pi(a)\}$ and cand $= \{\pi(a+1), \ldots, \pi(a+c)\}$;
2. goal $= g - \sum_{i \in \text{marked}}\eta^2_i$;
3. $a < L^* \le a + c$.

At the start $a = 0$, cand is everything, and $1 \le L^* \le n$, so the invariant holds.

In one pass, line L10 picks a value $p$ of cand, and line L11 splits cand into high ($> p$), equal ($= p$) and low ($< p$), which are not empty in the case of equal. Choose $\pi$ so that it lists marked, then high, then equal, then low, each in descending order. It is still a descending order, and it keeps property 1 of the invariant. Let $s_h$ and $s_e$ be the sums of high and equal. By property 2, the prefix $P_{a + j}$ is a bulk set exactly when the sum of its first $j$ elements after marked is at least goal.

*Case L13: high is not empty and $s_h \ge$ goal.* Then $P_{a + |\text{high}|}$ is a bulk set, so $L^* \le a + |\text{high}|$. The new cand is high, which is $\{\pi(a+1), \ldots, \pi(a + |\text{high}|)\}$. Properties 1 and 2 still hold, and property 3 holds with the new $c = |\text{high}|$. The new cand is smaller, because the pivot index is not in high.

*Case L14: not case L13, and $s_h + s_e \ge$ goal.* If high is not empty, then $s_h <$ goal, so $P_{a + |\text{high}|}$ is not a bulk set and $L^* > a + |\text{high}|$. If high is empty, then $L^* > a = a + |\text{high}|$ by property 3. Also $P_{a + |\text{high}| + |\text{equal}|}$ is a bulk set, so $L^*$ lies in the equal block. The code takes high and then the elements of equal one at a time, until the sum reaches goal and at least one element is marked. All elements of equal have the same value, so any order of them is a descending order, and the code returns the prefix $P_{L}$ of the smallest $L > a + |\text{high}|$ that is a bulk set (with $L \ge 1$). This is $L^*$ by Lemma 1.

*Case L15: $s_h + s_e <$ goal.* Then $P_{a + |\text{high}| + |\text{equal}|}$ is not a bulk set, so $L^* > a + |\text{high}| + |\text{equal}|$. Line L15 moves high and equal into marked, lowers goal by $s_h + s_e$ and sets cand to low. All three properties hold for the new values. The new cand is smaller, because equal contains the pivot.

Each pass either returns or makes cand strictly smaller, so the loop ends after at most $n$ passes. It cannot end with cand empty: then $c = 0$, and property 3 would give $a < L^* \le a$. So it ends at line L14 with a bulk set of size $L^*$. $\square$

**Claim C (expected cost).** With the pivot chosen uniformly at random from cand, the expected number of operations on indicators is at most $16n$, in the real-RAM model.

*Proof.* One pass costs at most $4c$ operations (three filters and one sum over cand, plus a sum over equal). Let $c_0 = n, c_1, c_2, \ldots$ be the sizes of cand. If the pivot has rank $r$ in cand (in descending order, ties counted once), the next cand is high or low, of size at most $\max(r - 1, c - r)$. For $r$ uniform in $\{1, \ldots, c\}$, the mean of $\max(r - 1, c - r)$ is at most $3c/4$, and ties only make the parts smaller. So $\mathbb{E}[c_{i+1} \mid c_i] \le \tfrac34 c_i$, and $\mathbb{E}[c_i] \le (\tfrac34)^i n$. The expected total cost is at most $4\sum_i \mathbb{E}[c_i] \le 4n\sum_i(\tfrac34)^i = 16n$. $\square$
