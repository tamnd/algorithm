---
title: The bound D is a lower bound, and the bounded search finds every string within z differences
proves: [correctness]
status: full
---

Let $X$ have length $n$, let $W$ have length $m$, and write $\mathrm{rows}(u)$ for the interval of suffix array rows of $X\$$ whose suffixes start with $u$. We use the backward-search lemma of the [FM-index](/fm-index/): if $[sp, ep) = \mathrm{rows}(u)$, then $\mathrm{rows}(bu) = [C(b) + O(b, sp),\ C(b) + O(b, ep))$, and $\mathrm{rows}(\varepsilon) = [0, n+1)$. The interval is empty exactly when $bu$ does not occur in $X$. Costs are unit costs: a mismatch, an inserted letter of $W$ and a deleted letter (a letter of $v$ with no partner in $W$) each cost 1. We write $\delta(W', v)$ for the edit distance.

**Lemma 1 (CALCULATE-D).** After line L6 for index $i$, $D(i)$ equals the number of pieces of the greedy split of $W[0 \ldots i]$, and the current piece $W[j \ldots i]$ (empty after L5) occurs in $X$.

*Proof.* The test at L3 uses the FM-index of $\overleftarrow{X}$, $X$ reversed. Backward search for the letters $W[j], W[j+1], \ldots, W[i]$ in that order gives $\mathrm{rows}(\overleftarrow{W[j \ldots i]})$ in $\overleftarrow{X}$, which is empty exactly when $W[j \ldots i]$ does not occur in $X$. So L3 tests the right condition, L4 counts a piece when it closes, and L5 starts the next piece. Induction on $i$. $\square$

**Lemma 2 (lower bound).** For every $i$ and every substring $v$ of $X$, $\delta(W[0 \ldots i], v) \ge D(i)$.

*Proof.* Let the closed pieces be $W[j_1 \ldots i_1], \ldots, W[j_d \ldots i_d]$ with $d = D(i)$, $j_1 = 0$, $j_{t+1} = i_t + 1$ and $i_d \le i$. None of them occurs in $X$. Fix an optimal alignment of $W[0 \ldots i]$ with $v$. Suppose that for some $t$ no column of the alignment that holds a letter of $W[j_t \ldots i_t]$ is a mismatch or an insertion, and that no deletion column lies strictly between two such columns. Then the letters $W[j_t], \ldots, W[i_t]$ are matched, in order, to consecutive letters of $v$, so $W[j_t \ldots i_t]$ is a substring of $v$ and so of $X$, which is false. So each piece has a difference column that holds one of its letters or lies strictly between two of its letters. These sets of columns are disjoint for different pieces, because the pieces are disjoint and consecutive in $W$. So the alignment has at least $d$ differences. $\square$

Since $D(i)$ grows with $i$, and an alignment of $W$ restricts to an alignment of each prefix with at most as many differences, a partial alignment of $W[i+1 \ldots m-1]$ with $z$ differences left can be completed only if $z \ge D(i)$.

**Invariant of the search.** Each state $(i, z, [sp, ep))$ pushed by INEXACT-SEARCH satisfies: there is a string $u$ with $[sp, ep) = \mathrm{rows}(u)$, $u$ occurs in $X$, and $\delta(W[i+1 \ldots m-1], u) \le z_0 - z$, where $z_0$ is the starting budget and $z \ge 0$.

*Proof.* The first state has $u = \varepsilon$ and $i = m-1$. L10 keeps $u$ and consumes $W[i]$ as an insertion, at cost 1. L12 prepends $b$ to $u$ and consumes nothing of $W$: a deleted letter, at cost 1. L13 and L14 prepend $b$ and consume $W[i]$, at cost 0 or 1. Each step that costs 1 needs $z > 0$, so $z$ stays nonnegative. The new interval is $\mathrm{rows}(bu)$ by backward search, and L11 keeps only nonempty ones, so $bu$ occurs. $\square$

**Theorem (soundness).** Every interval reported at L9 is $\mathrm{rows}(v)$ for a string $v$ that occurs in $X$ with $\delta(W, v) \le z_0$.

*Proof.* At L9, $i < 0$, so by the invariant $\delta(W, u) \le z_0$ for the string $u$ of the state. $\square$

**Theorem (completeness).** Let $v$ occur in $X$ and have an alignment $A$ with $W$ of at most $z_0$ differences whose first column is not a deleted letter of $v$. Then the search reports $\mathrm{rows}(v)$, with or without the pruning at L8.

*Proof.* Read the columns of $A$ from right to left. Each column is one of the four steps L10, L12, L13 or L14, and it is allowed: a difference step comes with $z > 0$ because $A$ has at most $z_0$ differences, and the interval after a step is $\mathrm{rows}$ of a suffix of $v$, which occurs, so L11 does not skip it. So the sequence of states along $A$ is pushed, one after another. No state on it is pruned at L8: at the state after the columns for $W[i+1 \ldots m-1]$, the remaining columns align $W[0 \ldots i]$ with a prefix $v'$ of $v$, a substring of $X$, with at most $z$ differences, and $z \ge \delta(W[0 \ldots i], v') \ge D(i)$ by Lemma 2. The last column consumes $W[0]$, so the state after it has $i = -1$ and the string $v$, and L9 reports $\mathrm{rows}(v)$. The set of seen states only removes repeats of a state that was already expanded, so it does not lose any path. $\square$

The condition on the first column is harmless: deleting the first letter of $v$ costs 1 and only moves the start of the occurrence. So the set of end positions $SA[r] + |v|$ of the reported rows equals the set $\{e : \min_s \delta(W, X[s \ldots e-1]) \le z_0\}$ that [Sellers' algorithm](/sellers-algorithm/) computes. For if $\delta(W, X[s \ldots e-1]) \le z_0$, an optimal alignment that starts with deletions of $v$ can drop them, which gives a later start, the same end and fewer differences. The tests check this equality on random inputs, with and without the bound $D$.

**Termination.** Each step either lowers $i$ or lowers $z$, and $z$ never goes below 0, so every path of the search has at most $m + z_0$ steps, and the search ends.
