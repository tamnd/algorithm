---
title: The rounded dynamic programming brackets the p-value and is exact when its middle table is empty
proves: [correctness]
status: full
---

Let $M$ have columns $j = 1, \ldots, L$ with real entries $M_j(a)$, let $p$ be the background and let $\Sigma^+ = \{a : p(a) > 0\}$. Only words over $\Sigma^+$ have positive probability, so all statements below are about these words. Write $S(w) = \sum_j M_j(w_j)$ and $P(\alpha) = \Pr[S(w) \ge \alpha]$. Fix a round with step $\varepsilon > 0$ and let $N$, $E$, $A$ and $B$ be the values of lines L3 to L6, with the maximum of line L4 over $\Sigma^+$. Write $T(w) = \sum_j N_j(w_j)$, an integer, and $S_\varepsilon(w) = \varepsilon T(w)$.

**Lemma 1 (the rounding error).** For every word $w$ over $\Sigma^+$, $S_\varepsilon(w) \le S(w) \le S_\varepsilon(w) + E$, and $0 \le E < L\varepsilon$.

*Proof.* By the definition of the floor, $0 \le M_j(a) - \varepsilon N_j(a) < \varepsilon$. Summing over the columns of $w$ gives the first inequality, and each term is at most the maximum of its column, which gives the second. $E$ is a sum of $L$ numbers in $[0, \varepsilon)$. $\square$

**Lemma 2 (the integer thresholds).** For an integer $s$, $\varepsilon s \ge \alpha$ if and only if $s \ge A$, and $\varepsilon s \ge \alpha - E$ if and only if $s \ge B$. Also $B \le A$.

*Proof.* $\varepsilon s \ge \alpha$ means $s \ge \alpha/\varepsilon$, and for an integer $s$ this means $s \ge \lceil \alpha/\varepsilon \rceil = A$. The same argument gives the second claim. $B \le A$ since $E \ge 0$. $\square$

**Lemma 3 (ROUND).** ROUND returns $\mathrm{sure} = \Pr[T(w) \ge A]$ and a table with $\mathrm{middle}[s] = \Pr[T(w) = s]$ for every $s$ with $B \le s < A$ and $\Pr[T(w) = s] > 0$, and no other keys.

*Proof.* For a word $w$ let $t_j(w) = \sum_{i \le j} N_i(w_i)$ and let $\mathrm{best}_j$, $\mathrm{worst}_j$ be the largest and the smallest sums of $N$ over the columns after $j$, over $\Sigma^+$, with $\mathrm{best}_L = \mathrm{worst}_L = 0$. Say that $w$ is *lumped at $j$* if $j$ is the first column with $t_j(w) + \mathrm{worst}_j \ge A$ or $t_j(w) + \mathrm{best}_j < B$, and the first of the two tests holds; *dropped at $j$* if the second holds at that first column; and *kept* if neither test holds at any column.

The tests at column $j$ depend only on the prefix $w_1 \cdots w_j$. By induction on $j$, the table after column $j$ maps each $t$ to the total probability of the prefixes of length $j$ with $t_j = t$ that are neither lumped nor dropped at a column up to $j$, and `sure` holds the total probability of the prefixes lumped at a column up to $j$. The step from $j - 1$ to $j$ takes each kept prefix of length $j - 1$ with its probability $q$, extends it by each letter $a \in \Sigma^+$ with probability $q\,p(a)$, and applies the two tests in order, which is the rule of ROUND. A prefix lumped or dropped earlier is not extended, and its probability is the sum of the probabilities of all its completions, since the letters are independent and $\sum_{a \in \Sigma^+} p(a) = 1$.

If $w$ is lumped at $j$, then $T(w) \ge t_j(w) + \mathrm{worst}_j \ge A$. If $w$ is dropped at $j$, then $T(w) \le t_j(w) + \mathrm{best}_j < B$. If $w$ is kept, then at $j = L$ neither test holds, so $B \le T(w) < A$. These three cases are disjoint and cover every word. A word with $T(w) \ge A$ is not dropped, since dropped words have $T < B \le A$, and is not kept, so it is lumped; a word with $B \le T(w) < A$ is neither lumped nor dropped, so it is kept and lands in the table at $T(w)$. So `sure` is $\Pr[T \ge A]$, and the table is the distribution of $T$ on $[B, A)$. Keys come only from words of positive probability. $\square$

**Theorem 1 (the bracket).** $\mathrm{lo} \le P(\alpha) \le \mathrm{hi}$, where $\mathrm{lo}$ and $\mathrm{hi}$ are the values of lines L8 and L9.

*Proof.* By Lemmas 2 and 3, $\mathrm{lo} = \Pr[T \ge A] = \Pr[S_\varepsilon \ge \alpha]$ and $\mathrm{hi} = \Pr[T \ge B] = \Pr[S_\varepsilon \ge \alpha - E]$. By Lemma 1, $S_\varepsilon(w) \ge \alpha$ implies $S(w) \ge \alpha$, and $S(w) \ge \alpha$ implies $S_\varepsilon(w) \ge S(w) - E \ge \alpha - E$. Take probabilities. $\square$

**Theorem 2 (exact on an empty table).** If the table of line L7 is empty, then $\mathrm{lo} = P(\alpha) = \mathrm{hi}$.

*Proof.* By Lemma 3, an empty table means that no word of positive probability has $B \le T(w) < A$, so $\Pr[T \ge B] = \Pr[T \ge A]$, that is, $\mathrm{hi} = \mathrm{lo}$. Theorem 1 then gives the claim. $\square$

**Lemma 4 (the lower bound does not fall).** Let $\mathrm{lo}$ be computed with step $\varepsilon$ and $\mathrm{lo}'$ with step $\varepsilon/10$. Then $\mathrm{lo}' \ge \mathrm{lo}$.

*Proof.* The number $\varepsilon \lfloor x/\varepsilon \rfloor$ is a point of the grid of step $\varepsilon/10$ that is at most $x$, and $(\varepsilon/10) \lfloor 10x/\varepsilon \rfloor$ is the largest such point. So every entry of the finer rounded matrix is at least the coarser one, $S_{\varepsilon/10}(w) \ge S_\varepsilon(w)$ for every word, and $\Pr[S_{\varepsilon/10} \ge \alpha] \ge \Pr[S_\varepsilon \ge \alpha]$. $\square$

**Theorem 3 (when the loop stops).** Suppose that no word of positive probability has $S(w) = \alpha$, and let $\delta > 0$ be the smallest value of $|S(w) - \alpha|$ over these words. In every round with $L\varepsilon \le \delta$, the table is empty. If some word $w$ of positive probability has $S(w) = \alpha$ and $S_\varepsilon(w) < \alpha$ for every step $\varepsilon$ of the rounds, the table is never empty.

*Proof.* Let $L\varepsilon \le \delta$. A word with $S(w) > \alpha$ has $S(w) \ge \alpha + \delta$ and, by Lemma 1, $S_\varepsilon(w) > S(w) - L\varepsilon \ge \alpha$, so $T(w) \ge A$. A word with $S(w) < \alpha$ has $S_\varepsilon(w) \le S(w) \le \alpha - \delta < \alpha - E$, since $E < L\varepsilon \le \delta$, so $T(w) < B$. So no word has $B \le T(w) < A$, and by Lemma 3 the table is empty. For the second claim, such a $w$ has $\alpha - E \le S(w) - E \le S_\varepsilon(w) < \alpha$, so $B \le T(w) < A$ by Lemma 2, and $w$ is in the table by Lemma 3. $\square$

Since $\varepsilon = \varepsilon_0 10^{-(r-1)}$ in round $r$, the first claim gives at most $1 + \lceil \log_{10}(L\varepsilon_0/\delta) \rceil$ rounds when the cap is not reached. The second claim is why the cap exists. A word with $S(w) = \alpha$ whose entries all lie on the grid has $S_\varepsilon(w) = S(w)$ and does no harm.

**Cost.** After $j$ columns every key $t$ of the table satisfies $\sum_{i \le j} \min_a N_i(a) \le t \le \sum_{i \le j} \max_a N_i(a)$, and $\max_a N_i(a) - \min_a N_i(a) \le R/\varepsilon + 1$, so the table has at most $j(R/\varepsilon + 1) + 1$ keys, and also at most $c^j$, one per prefix. Each key is extended by $c$ letters with $O(1)$ dictionary work, so a round is $O(LcS)$ with $S = O(\min(c^L, LR/\varepsilon))$. The arrays best and worst take $O(Lc)$ to build.

**Hardness.** Touzet and Varré prove that the problem is NP-hard by a reduction from SUBSET SUM. A simple reduction of this kind: given positive integers $x_1, \ldots, x_L$ and a target $t$, let column $j$ have the entry $x_j$ for A and 0 for C, G and T, with the uniform background. The words with $S(w) = t$ are the subsets of the $x_j$ that sum to $t$, so such a subset exists exactly when $P(t) - P(t + 1) > 0$. So an algorithm that computes $P$ in time polynomial in $L$ and in the number of bits of the entries would decide SUBSET SUM in polynomial time. The integer entries give $E = 0$ and $A = B$, so the first round of this page is exact here, but its cost is polynomial in $R/\varepsilon$, not in the number of bits of $R$, so there is no contradiction.
