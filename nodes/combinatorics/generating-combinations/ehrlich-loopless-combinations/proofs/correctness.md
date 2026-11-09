---
title: The loopless revolving door algorithm visits each k-subset once, with O(1) work for each step
proves: [correctness]
status: full
---

Fix $n > k > 1$. Let $K$ be the set of sequences $c = (c_k, \ldots, c_1)$ with $n > c_k > c_{k-1} > \cdots > c_1 \ge 0$, and put $c_{k+1} = n$. The map from $c$ to the set $\{c_1, \ldots, c_k\}$ is a bijection from $K$ to the $k$-subsets of $\{0, \ldots, n-1\}$.

**Directions.** Position $i$ is *rising* if $k - i$ is even and *falling* if $k - i$ is odd. Let $\sigma_i = +1$ for a rising position and $\sigma_i = -1$ for a falling one. The *revolving door order* on $K$ is the lexicographic order of the keys $(\sigma_k c_k, \sigma_{k-1} c_{k-1}, \ldots, \sigma_1 c_1)$. Knuth shows that this is the order of the weight-$k$ strings in the binary reflected Gray code. We do not need that fact here.

**Ranges.** For $1 \le i \le k$ and fixed $c_{i+1}$, let $R_i = \{i - 1, \ldots, c_{i+1} - 1\}$. Since $c_i > c_{i-1} > \cdots > c_1 \ge 0$, we have $c_i \ge i - 1$, and $c_i < c_{i+1}$, so $c_i \in R_i$. Each value $v \in R_i$ has a completion: $c_i = v$ and $c_m = m - 1$ for $m < i$. The *first* value $\varphi_i$ of $R_i$ is its least element if $i$ is rising and its greatest if $i$ is falling. The *last* value $\lambda_i$ is the other end. Position $i$ is *free* in $c$ if $c_i \ne \lambda_i$, so that $c_i + \sigma_i \in R_i$.

**Lemma 1 (successor).** Let $c \in K$. If no position is free, $c$ is the last element of $K$. Otherwise let $i$ be the least free position. Then the successor $c'$ of $c$ has $c'_m = c_m$ for $m > i$, $c'_i = c_i + \sigma_i$, and $c'_m = \varphi_m$ computed from $c'_{m+1}$, for $m = i - 1, \ldots, 1$.

*Proof.* If no position is free, then $c_k = \lambda_k$ is the largest key value possible at position $k$, and by induction downward each $c_m$ is the largest key value possible after $c_k, \ldots, c_{m+1}$. So no element has a larger key. Otherwise, $c'$ is in $K$: $c'_i \in R_i$, and each $c'_m$ for $m < i$ is in its range. Its key is greater than the key of $c$, since they first differ at position $i$ and $\sigma_i c'_i = \sigma_i c_i + 1$. Let $b \in K$ have a greater key than $c$, and let $p$ be the largest position with $b_p \ne c_p$. Then $\sigma_p b_p > \sigma_p c_p$. If $p < i$, position $p$ is not free in $c$, so $c_p = \lambda_p$ is the largest key value in $R_p$, a contradiction. If $p > i$, then $\sigma_p b_p > \sigma_p c'_p$ and $b$ is after $c'$. If $p = i$, then $\sigma_i b_i \ge \sigma_i c'_i$. If this is strict, $b$ is after $c'$. If it is equal, $b$ and $c'$ agree at positions $i$ and above, and for $m = i - 1, \ldots, 1$ the value $\varphi_m$ has the least key in $R_m$, so the key of $b$ is not less than the key of $c'$. So $c'$ is the least element after $c$. $\square$

The first element of $K$ is $c_m = m - 1$ for all $m$: position $k$ is rising, so $\varphi_k = k - 1$, and for $m < k$ the range $R_m = \{m - 1\}$ has one element.

**Lemma 2 (shape below the free position).** Let $2 \le i \le k$, and let no position below $i$ be free in $c$. Then $c_m = m - 1$ for $m \le i - 2$, and $c_{i-1} = c_i - 1$ if $i - 1$ is rising, $c_{i-1} = i - 2$ if $i - 1$ is falling. Also, after the step of Lemma 1 at position $i$, $c'_m = m - 1$ for $m \le i - 2$, and $c'_{i-1} = i - 2$ if $i - 1$ is rising, $c'_{i-1} = c'_i - 1$ if $i - 1$ is falling.

*Proof.* Position $i - 1$ is at its last value: the greatest element $c_i - 1$ of $R_{i-1}$ if it is rising, the least element $i - 2$ if it is falling. In the second case, $R_{i-2} = \{i - 3\}$, and each lower range has one element, so $c_m = m - 1$ for $m \le i - 2$. In the first case, position $i - 2$ is falling, so it is at its least value $i - 3$, and again each lower range has one element. The claim on $c'$ is the same argument with first values in place of last values, which swaps the roles of rising and falling. $\square$

**Lemma 3 (the step).** Let $i$ be the least free position of $c$.

- (A) If $i$ is rising, then $c_i + 1 < c_{i+1}$, and $c'$ is $c$ with $c_i$ replaced by $c_i + 1$ and, if $i \ge 2$, $c_{i-1}$ replaced by the old value $c_i$. Before the step $c_{i-1} = i - 2$.
- (B) If $i$ is falling, then $c_i \ge i$, and $c'$ is $c$ with $c_i$ replaced by $c_{i-1}$ and, if $i \ge 2$, $c_{i-1}$ replaced by $i - 2$. For $i = 1$ the step is $c_1 \leftarrow c_1 - 1$.

In both cases exactly one element leaves the set and one enters.

*Proof.* (A) A rising position is free when $c_i < c_{i+1} - 1$, and $\sigma_i = 1$. For $i \ge 2$, position $i - 1$ is falling, so by Lemma 2, $c_{i-1} = i - 2$ before, $c'_{i-1} = c'_i - 1 = c_i$ after, and the entries below $i - 1$ do not change. The set loses $i - 2$ and gains $c_i + 1$. (B) A falling position is free when $c_i > i - 1$, and $\sigma_i = -1$. For $i \ge 2$, position $i - 1$ is rising, so by Lemma 2, $c_{i-1} = c_i - 1$ before, so $c'_i = c_i - 1 = c_{i-1}$, and $c'_{i-1} = i - 2$. The set loses $c_i$ and gains $i - 2$. For $i = 1$ the step is $c_1 \pm 1$. $\square$

**Lemma 4 (the scan).** Suppose that line L8 starts with $2 \le j \le k$, with $s = $ UP if $j$ is rising and $s = $ DOWN if $j$ is falling, and with no free position below $j$. Then lines L8 to L12 either make the step of Lemma 1 at the least free position $i \ge j$ and stop with $j = i$, or, if no position at or above $j$ is free, return.

*Proof.* By induction on the passes, the invariant holds at each pass: no position below $j$ is free, and $s$ matches the direction of $j$. When $s = $ DOWN, line L9 tests $c_j \ge j$, which says that the falling position $j$ is free, and then makes step (B) of Lemma 3. When $s = $ UP, line L11 tests $c_j + 1 < c_{j+1}$, which says that the rising position $j$ is free, and makes step (A). If the test fails, position $j$ is not free, lines L10 and L12 add $1$ to $j$, and they flip $s$, which matches the direction of $j + 1$. Position $k$ is rising, so line L10 runs only with $j < k$, and the new $j$ is at most $k$. Line L12 returns only when the rising position $k$ is not free, and then no position is free. Each pass adds $1$ to $j$ or stops, so the loop ends. Lines L9 and L11 write $c[j-1]$ with $j \ge 2$, and line L11 reads $c[j+1]$ with $j \le k$, so all indices are in range. $\square$

**Lemma 5 (the start).** At line L4, let $j$ be $k + 1$ at the first step and otherwise the position of the last step. After lines L4 to L7, either the step at position $1$ is done and it is the step of Lemma 1, or the conditions of Lemma 4 hold.

*Proof.* *Lines L5 to L7.* Position $1$ is rising if and only if $k$ is odd. Line L5 tests if a rising position $1$ is free, line L6 tests if a falling position $1$ is free, and each makes the step of Lemma 3 at $i = 1$. If position $1$ is not free, line L7 sets $j = 2$, and $s$ matches the direction of position $2$, which is falling when $k$ is odd. These lines are correct for any value of $j$.

*Line L4.* Let $j \ge 3 + [k \text{ odd}]$ and $j_0 = j - 1 - [j \equiv k]$, so $j_0 = j - 2$ if $j$ is rising and $j_0 = j - 1$ otherwise. In both cases $j_0 \equiv k \pmod 2$, so $j_0$ is rising and $s = $ UP is right. If $k$ is odd, $j \ge 4$ gives $j_0 \ge 3$. If $k$ is even, $j \ge 3$ gives $j_0 \ge 2$. So $2 \le j_0 \le k$. It remains to show that no position below $j_0$ is free.

At the first step, $j = k + 1$, $j_0 = k$, and $c_m = m - 1$ for all $m$, so each range $R_m$ with $m < k$ has one element. No position below $k$ is free.

Otherwise the last step was at position $j = i \ge 3$, and by Lemma 2 the entries are now $c_m = m - 1$ for $m \le i - 2$. For $m \le i - 3$ this gives $R_m = \{m - 1\}$, so position $m$ is not free. If $i$ is rising, $j_0 = i - 2$ and we are done. If $i$ is falling, $j_0 = i - 1$, and position $i - 1$ is rising, so Lemma 2 gives $c_{i-1} = i - 2$ after the step. Then $R_{i-2} = \{i - 3\}$ and position $i - 2$ is not free either. $\square$

**Theorem 1 (correctness).** For $n > k > 1$, REVOLVING-DOOR-LOOPLESS$(n, k)$ visits each element of $K$ exactly once, in the revolving door order, and then stops. Each step takes out one element of the subset and puts in one.

*Proof.* Line L1 makes the first element of $K$ and sets $j = k + 1$. By Lemma 5 and Lemma 4, each pass through lines L4 to L12 changes $c$ to its successor of Lemma 1 and leaves $j$ equal to the position of the change, or returns when no position is free, which by Lemma 1 happens only after the last element. Line L5 and line L6 set $j = 1$, the position of their change. By induction on the number of visits, the $r$-th visit sees the $r$-th element of $K$. The keys strictly increase, so no element is visited twice, and no element is skipped. Lemma 3 gives the revolving door property. $\blacksquare$

**Lemma 6 (the next free position).** Let a step at position $i$ change $c$ to $c'$, and let $i'$ be the least free position of $c'$, if one exists.

- (A) If $i$ is rising and $i \ge 3$, then $i' = i - 2$. If $i = 2$ is rising, $i' = 1$. If $i = 1$ is rising, $i' \le 2$.
- (B) If $i$ is falling, then $i' \in \{\max(i - 1, 1), i + 1, i + 2\}$, or $c'$ is the last element.

*Proof.* (A) For $i \ge 3$, positions below $i - 2$ have one possible value. Position $i - 2$ is rising with $c'_{i-2} = i - 3$, and its range goes up to $c'_{i-1} - 1 = c_i - 1 \ge i - 2$, since $c_i \ge i - 1$. So it is free. For $i = 2$, position $1$ is falling with $c'_1 = c_2 \ge 1$, so it is free. For $i = 1$, if position $1$ is not free then $c'_1 = c_2 - 1$, and $c'_1 \ge 1$ gives $c_2 \ge 2$, so the falling position $2$ is free.

(B) The positions below $i - 1$ have one possible value, as in Lemma 5. If $c'_i \ge i$ and $i \ge 2$, the rising position $i - 1$, with $c'_{i-1} = i - 2$ and range up to $c'_i - 1 \ge i - 1$, is free. If $c'_1 \ge 1$ and $i = 1$, position $1$ is free. Otherwise $c'_i = i - 1$, so positions $i - 1$ and $i$ are at their least values and are not free. Before the step $c_i = i$, so $c_{i+1} \ge i + 1$, and $c_{i+1}$ does not change. Position $i + 1$ exists since $i$ is falling and $k$ is rising. If it is not free, then $c_{i+1} = c_{i+2} - 1$, so $c_{i+2} \ge i + 2$. If $i + 2 \le k$, the falling position $i + 2$ is then free. If $i + 2 = k + 1$, no position is free and $c'$ is the last element. $\square$

**Theorem 2 (loopless).** Each step makes at most $4$ passes of the loop of line L8, so the time between two visits is $O(1)$.

*Proof.* At the first step, line L4 jumps to $j_0 = k$, since $k + 1 \ge 3 + [k \text{ odd}]$ for $k \ge 2$. Position $k$ is free because $c_k = k - 1 < n - 1$, so the loop makes one pass. Otherwise let the last step be at position $i$. If line L4 jumps and $i$ is rising, then by Lemma 6 (A) the first test, at $i - 2$, succeeds: one pass. If line L4 jumps and $i$ is falling, the loop tests positions $i - 1, i, i + 1, i + 2$ at most, by Lemma 6 (B): at most $4$ passes. If line L4 does not jump, then $i \le 3$ and the loop starts at position $2$. By Lemma 6, $i' \le 5$, so the loop tests positions $2, \ldots, 5$ at most: at most $4$ passes. Each pass and each of lines L3 to L7 take $O(1)$ time. $\blacksquare$

The total time is $\Theta(k)$ for line L1 plus $O(1)$ for each of the $N = C(n, k)$ visits, which is $\Theta(N)$ since $N \ge n > k$ for $1 < k < n$.
