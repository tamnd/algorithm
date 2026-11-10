---
title: P-MERGE writes the sorted merge of its two inputs, and its parallel calls write disjoint cells
proves: [correctness, termination]
status: full
---

We use the lines of P-MERGE on the page. A call gets two sorted ranges $T[p_1 \ldots r_1 - 1]$ and $T[p_2 \ldots r_2 - 1]$ of a source array $T$ and an output start $p_3$ in an array $A$. The ranges are disjoint, and the output range $A[p_3 \ldots p_3 + n_1 + n_2 - 1]$ shares no cell with $T$. We write $N = n_1 + n_2$ for the size of the call, and we call the two ranges $X$ (the longer one after lines L2 to L4) and $Y$.

**Lemma 1 (the split).** Let $N \ge 1$, let $x = T[q_1]$ be the item of line L6, and let $k = q_1 - p_1$ and $j = q_2 - p_2$ after line L7. Then:

1. every item of $X[0 \ldots k - 1]$ and of $Y[0 \ldots j - 1]$ is at most $x$;
2. every item of $X[k + 1 \ldots]$ and of $Y[j \ldots]$ is at least $x$;
3. $k = \lfloor n_1 / 2 \rfloor$, and the two calls of lines L10 and L11 have sizes $N_1 = k + j$ and $N_2 = N - 1 - N_1$.

*Proof.* Lines L2 to L4 only swap the names of the two ranges, so after them $n_1 \ge n_2$ and $n_1 \ge 1$ because $N \ge 1$. Line L6 picks $q_1 = \lfloor (p_1 + r_1)/2 \rfloor$, so $k = \lfloor n_1/2 \rfloor$ and $p_1 \le q_1 < r_1$, and $x$ is an item of $X$. Since $X$ is sorted, the items before $x$ are at most $x$ and the items after it are at least $x$. Line L7 returns the least index $q_2$ in $[p_2, r_2]$ with $q_2 = r_2$ or $x \le T[q_2]$. So all items of $Y$ before $q_2$ are less than $x$, and since $Y$ is sorted, all items from $q_2$ on are at least $x$. The left call of line L10 gets $X[0 \ldots k - 1]$ and $Y[0 \ldots j - 1]$, which is $k + j$ items. The right call gets the rest except $x$, which is $N - 1 - N_1$ items. $\blacksquare$

**Lemma 2 (the output places).** Line L8 sets $q_3 = p_3 + N_1$. The left call writes $A[p_3 \ldots q_3 - 1]$, line L9 writes $A[q_3]$, and the right call writes $A[q_3 + 1 \ldots p_3 + N - 1]$. These three ranges are disjoint, and they cover the output range of the call.

*Proof.* By Lemma 1, $q_3 = p_3 + k + j = p_3 + N_1$. A call with output start $s$ and size $M$ writes only inside $A[s \ldots s + M - 1]$: this holds for $M = 0$, where line L5 writes nothing, and it follows for $M \ge 1$ from the three ranges of this lemma by induction on $M$. The left call has start $p_3$ and size $N_1$, and the right call has start $q_3 + 1$ and size $N_2 = N - 1 - N_1$, so it ends at $p_3 + N - 1$. $\blacksquare$

**Lemma 3 (no races).** The two calls of lines L10 and L11 run in parallel with no [determinacy race](/determinacy-race/).

*Proof.* Both calls only read $T$, and no call writes $T$, because the output ranges share no cell with $T$. By Lemma 2 they write disjoint ranges of $A$. So no cell is written by one call and read or written by the other. $\blacksquare$

**Theorem (correctness and termination).** Each call of P-MERGE ends, and when it ends, $A[p_3 \ldots p_3 + N - 1]$ holds the items of the two input ranges, each as many times as it occurs in them, in sorted order.

*Proof.* By strong induction on $N$. If $N = 0$, line L5 returns at once and the output range is empty. Let $N \ge 1$. By Lemma 1 both calls have size at most $N - 1$, so they end by the induction hypothesis, and with them the call ends. By the hypothesis the left call writes the sorted merge of $X[0 \ldots k-1]$ and $Y[0 \ldots j - 1]$ into $A[p_3 \ldots q_3 - 1]$, and the right call writes the sorted merge of the remaining items except $x$ into $A[q_3 + 1 \ldots]$. Line L9 puts $x$ at $q_3$. The three parts together hold each input item once, and by Lemma 1 every item of the left part is at most $x$ and every item of the right part is at least $x$. Each part is sorted, so the whole range is sorted. Lemma 3 makes the parallel run give the same result as a run of the two calls one after the other. $\blacksquare$

**Remark (stability).** The theorem says nothing about the order of equal items, and P-MERGE is not stable. Take $X$ as the second input with items $1_b, 1_c$ and $Y$ as the first input with item $1_a$. Line L6 picks $x = 1_c$, line L7 returns $q_2 = p_2$ because $1_a \le x$, and $1_a$ goes after $x$ in the output, so it ends up after items of the second input. To make it stable, use the lower bound search of line L7 when $X$ is the first input and the upper bound search (the least index with $x < T[q_2]$) when $X$ is the second input. Lemma 1 then holds with "less than" and "at most" exchanged on the side of $Y$, and the proof is the same.
