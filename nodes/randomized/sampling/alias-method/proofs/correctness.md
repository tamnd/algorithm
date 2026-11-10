---
title: The alias table exists, Vose's construction builds it in linear time, and a sample has the right law
proves: [correctness, termination, time.build]
status: full
---

The input is a list of $n \ge 1$ non-negative integers $w_0, \ldots, w_{n-1}$ with $W = \sum_i w_i > 0$. Rational weights are first scaled to integers by their common denominator, which does not change the ratios. Line L1 sets $q_i = n w_i$, so $\sum_i q_i = nW$. A column $i$ is *finished* when lines L5 or L8 have set $\mathit{prob}[i]$ and $\mathit{alias}[i]$. A finished column $i$ sends the mass $\mathit{prob}[i]$ to item $i$ and the mass $W - \mathit{prob}[i]$ to item $\mathit{alias}[i]$, out of a total of $W$ for the column.

**Definition.** A table $(\mathit{prob}, \mathit{alias})$ with $0 \le \mathit{prob}[i] \le W$ is *correct* when, for each item $j$,

$$\mathit{prob}[j] + \sum_{i \,:\, \mathit{alias}[i] = j,\ i \ne j} \bigl(W - \mathit{prob}[i]\bigr) + [\mathit{alias}[j] = j]\bigl(W - \mathit{prob}[j]\bigr) = n w_j .$$

The left side is the total mass that the columns send to $j$.

**Lemma 1 (the sampler).** If the table is correct, ALIAS-SAMPLE returns $j$ with probability exactly $w_j / W$.

*Proof.* Line L10 picks the column $i$ with probability $1/n$, and line L11 picks $t$ with probability $1/W$, independently. So each of the $nW$ pairs $(i, t)$ has probability $1/(nW)$. Line L12 returns $i$ for the $\mathit{prob}[i]$ pairs with $t < \mathit{prob}[i]$ and returns $\mathit{alias}[i]$ for the other $W - \mathit{prob}[i]$ pairs. So the number of pairs that return $j$ is the left side of the definition, which is $n w_j$. The probability is $n w_j / (nW) = w_j / W$. $\square$

**Lemma 2 (the invariant).** Let $A$ be the set of columns that are not finished, that is, the columns in *small* or *large*. Before each test of line L3, these statements hold:

1. $\sum_{i \in A} q_i = |A| \cdot W$.
2. Each $i \in A$ is in *small* if $q_i < W$ and in *large* if $q_i \ge W$, and in no other place. Each $q_i \ge 0$.
3. For each item $j$, the mass that the finished columns send to $j$, plus $q_j$ if $j \in A$, equals $n w_j$.

*Proof.* Initialization. No column is finished, $A$ is all of $\{0, \ldots, n-1\}$, and $\sum_i q_i = nW$, so statement 1 holds. Line L2 gives statement 2. Statement 3 says $q_j = n w_j$, which is line L1.

Maintenance. Assume the statements before an iteration. Line L4 removes $l$ with $q_l < W$ and $g$ with $q_g \ge W$. Line L5 finishes column $l$: it sends $q_l$ to $l$ and $W - q_l$ to $g$. Line L6 lowers $q_g$ by the same $W - q_l$. For item $l$, the finished mass gains $q_l$ and $l$ leaves $A$, so statement 3 holds for $l$. For item $g$, the finished mass gains $W - q_l$ and $q_g$ loses $W - q_l$, so statement 3 holds for $g$. No other item changes. For statement 1, $A$ loses $l$, and the sum loses $q_l + (W - q_l) = W$, so the sum is still $|A| \cdot W$. For statement 2, the new $q_g$ is $q_g - W + q_l \ge q_l \ge 0$ because the old $q_g \ge W$, and line L7 puts $g$ in the right list. Also $0 \le \mathit{prob}[l] = q_l < W$. $\square$

**Lemma 3 (termination and the end state).** The loop of line L3 runs at most $n - 1$ times. When it stops, each column $i$ that is not finished has $q_i = W$.

*Proof.* Each iteration finishes column $l$ and finishes no other column, so $|A|$ drops by exactly 1. Column $g$ goes back into a list, so $|A| \ge 1$ after each iteration, and there are at most $n - 1$ iterations.

The loop stops when *small* or *large* is empty. If *large* is empty and *small* is not, then each $i \in A$ has $q_i < W$, so $\sum_{i \in A} q_i < |A| W$. This contradicts statement 1. So *small* is empty, and each $i \in A$ has $q_i \ge W$. By statement 1 the sum is exactly $|A| W$, so each $q_i = W$. $\square$

**Theorem.** ALIAS-BUILD returns a correct table in $O(n)$ time, and ALIAS-SAMPLE then returns $j$ with probability $w_j / W$ for each $j$.

*Proof.* By Lemma 3, at the end each unfinished column has $q_i = W$. Line L8 sets $\mathit{prob}[i] = W$ and $\mathit{alias}[i] = i$, so the column sends $W = q_i$ to $i$. Then statement 3 of Lemma 2 says that the mass that all columns send to $j$ is $n w_j$, for each $j$. Each column is finished exactly once, with $0 \le \mathit{prob}[i] \le W$. So the table is correct, and Lemma 1 gives the law of a sample.

For the time, lines L1 and L2 take $O(n)$. Each iteration of the loop takes $O(1)$ list operations and arithmetic operations, and there are at most $n - 1$ iterations by Lemma 3. Line L8 takes $O(n)$. The total is $O(n)$ operations on integers of at most $\lceil \lg (nW) \rceil + 1$ bits. $\blacksquare$

**Existence.** The theorem also proves that a correct table exists for every list of non-negative rational weights with a positive sum: Vose's construction builds one. In each table, each column holds at most two items.

**Floating point.** The proof uses exact integer arithmetic. If $q_i$ is a float, the update of line L6 rounds, so statement 1 of Lemma 2 holds only up to rounding. Then the loop can stop with a column in *small* whose $q_i$ is slightly below 1 (in units of $W$), which Lemma 3 rules out in exact arithmetic. Setting that column to $\mathit{prob}[i] = 1$, as Vose does, keeps the table valid, but the law of the sample is then off by the accumulated rounding error.
