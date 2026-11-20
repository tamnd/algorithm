---
title: The English clock auction stops within one increment of the second-highest threshold, and dropping out at one's value is dominant up to one increment
proves: [correctness]
status: full
---

We use the pseudocode of the page, with thresholds $d_1, \ldots, d_n$, increment $\delta > 0$ and start price $p_0$. Write $g_k = p_0 + k\delta$ for the clock prices, and $A_k = \{i : d_i \ge g_k\}$.

**Claim 1 (the outcome).** If $A_0$ is empty, CLOCK returns no winner. If $A_0 = \{j\}$, it returns $j$ at price $p_0$. Otherwise let $a$ be the largest $k$ with $|A_k| \ge 2$. If $A_{a+1}$ is not empty, it has one element $j$, and CLOCK returns $j$ at price $g_{a+1}$. If $A_{a+1}$ is empty, CLOCK returns the smallest index in $A_a$ at price $g_a$.

*Proof.* The sets $A_k$ shrink as $k$ grows, and $A_k$ is empty for large $k$ because the thresholds are finite, so $a$ exists when $|A_0| \ge 2$. Line L1 sets $A = A_0$ and $p = g_0$. We show by induction that before the $k$-th test of line L3 (counting from 0), $A = A_k$ and $p = g_k$, for each $k \le a + 1$ that the loop reaches. This holds for $k = 0$. If $k \le a$, then $|A_k| \ge 2$, so the loop runs, and line L4 computes $\{i \in A_k : d_i \ge g_{k+1}\} = A_{k+1}$. If $k < a$, then $|A_{k+1}| \ge 2$, so line L5 does not return and line L6 sets $A = A_{k+1}$ and $p = g_{k+1}$. If $k = a$, then $|A_{a+1}| \le 1$. If $A_{a+1}$ is empty, line L5 returns the smallest index of $A_a$ at $g_a$. Otherwise line L6 sets $A = A_{a+1}$, a single bidder, and $p = g_{a+1}$, the loop stops, and line L7 returns that bidder at $g_{a+1}$. The cases with $|A_0| \le 1$ are lines L2 and L7 directly. $\square$

**Claim 2 (price and efficiency).** Let $|A_0| \ge 2$, and let $d_{(1)} \ge d_{(2)}$ be the two largest thresholds. Then $g_a$ is the largest clock price at most $d_{(2)}$, the price $p$ is $g_a$ or $g_{a+1}$, $|p - d_{(2)}| < \delta$, $p \le d_w$ for the winner $w$, and $d_w > d_{(1)} - \delta$.

*Proof.* $|A_k| \ge 2$ if and only if $g_k \le d_{(2)}$, which gives the first statement, and $g_a \le d_{(2)} < g_{a+1}$. Both possible prices are within $\delta$ of $d_{(2)}$, strictly. The winner is in $A_a$ or $A_{a+1}$ at the price it pays, so $p \le d_w$. If the winner pays $g_{a+1}$, it is the bidder with $d_{(1)}$. If it pays $g_a$, then $A_{a+1}$ is empty, so $d_{(1)} < g_{a+1} = g_a + \delta \le d_w + \delta$. $\square$

With truthful thresholds $d_i = v_i$, Claim 2 says that the winner never pays more than its value, that the price is within $\delta$ of the second-highest value, and that the winner's value is within $\delta$ of the highest value.

**Claim 3 (truthful dropping is dominant up to $\delta$).** Fix bidder $i$ with value $v_i \ge p_0$, and fix any strategies of the other bidders. A strategy of a bidder may depend on everything it has seen: the price and who has left. Then the utility of $i$ with the threshold $d_i = v_i$ is at least 0, and at least the utility of any other strategy of $i$ minus $\delta$. If $i$ never wins a tie, the loss is less than $\delta$.

*Proof.* Consider the run in which $i$ never leaves. It fixes, for each clock price, which of the others stay. Let $g_a$ be the last clock price at which at least one other bidder is active (if no other bidder is active at $p_0$, then $i$ wins at $p_0$ with any threshold at least $p_0$, which gives $v_i - p_0 \ge 0$ with the truthful threshold, and the claim holds). A strategy of $i$ is the same as the price at which $i$ leaves, because up to that moment the run is the same as the run in which $i$ never leaves: the others see the same history. So bidder $i$ has three possible outcomes.

- It leaves before $g_a$: at the step where it leaves, another bidder is still active at $g_a$, so $i$ loses, with utility 0.
- It accepts $g_a$ but not $g_{a+1}$: then all active bidders leave at once after $g_a$, and the tie rule decides. Bidder $i$ either wins at $g_a$ or loses. The tie outcome depends only on the indices, the same for every threshold in $[g_a, g_{a+1})$.
- It accepts $g_{a+1}$: then $i$ is alone and wins at $g_{a+1}$.

Now compare with the truthful threshold $v_i$.

- If $v_i \ge g_{a+1}$, truthful bidding wins at $g_{a+1}$ with utility $v_i - g_{a+1} \ge 0$. The best other outcome is a won tie at $g_a$, worth $v_i - g_a = (v_i - g_{a+1}) + \delta$. The loss is at most $\delta$, and it is 0 if $i$ never wins a tie.
- If $g_a \le v_i < g_{a+1}$, truthful bidding gets the tie outcome: $v_i - g_a \ge 0$ or $0$. Winning at $g_{a+1}$ gives $v_i - g_{a+1} < 0$. So the loss is at most $v_i - g_a < \delta$.
- If $v_i < g_a$, truthful bidding loses with 0, and every winning outcome has a price at least $g_a > v_i$. The loss is 0.

In each case the truthful utility is at least 0 and the loss is at most $\delta$, strictly less if $i$ loses ties. $\square$

**Cost.** By Claim 1 the loop runs at most $a + 1$ times, where $a = \lfloor (d_{(2)} - p_0)/\delta \rfloor$, and each pass scans the active set in $O(n)$. The time is $O(n k)$ with $k = a + 2$ clock steps, and the extra space is $O(n)$ for the active set.
