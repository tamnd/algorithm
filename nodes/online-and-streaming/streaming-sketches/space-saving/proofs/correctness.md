---
title: Space-Saving overestimates each count by at most m/k and is isomorphic to Misra-Gries
proves: [correctness]
status: full
---

Let $T$ be the table after $m$ updates, with counters $T[x]$ and errors $\epsilon[x]$ for $x \in T$. Write $\mu = \min_{y \in T} T[y]$ when $|T| = k$ and $\mu = 0$ when $|T| < k$. Write $\hat f_x = T[x]$ for $x \in T$ and $\hat f_x = \mu$ otherwise. Let $f_x$ be the true count of $x$.

**Lemma 1.** $\sum_{y \in T} T[y] = m$. Once $|T| = k$, the table stays full, and $\mu$ never falls.

*Proof.* Line L3 adds 1 to one counter. Line L5 adds a counter 1. Lines L6 to L8 remove a counter of value $\mu$ and add one of value $\mu + 1$. So each update adds exactly 1 to the sum, and the sum starts at 0. Only lines L6 to L8 remove an item, and they add one at the same time, so a full table stays full. Counters never fall, and the counter that is removed has the smallest value $\mu$ and is replaced by $\mu + 1$, so the smallest counter does not fall. The change from $\mu = 0$ to a full table also does not lower $\mu$. $\square$

**Lemma 2.** At all times:

1. while $|T| < k$, every item that has arrived is in $T$, with $T[x] = f_x$ and $\epsilon[x] = 0$;
2. for each $x \in T$: $T[x] - \epsilon[x] \le f_x \le T[x]$ and $\epsilon[x] \le \mu$;
3. for each $x \notin T$: $f_x \le \mu$.

*Proof.* By induction on $m$. All parts hold for the empty table. Assume them before SS-UPDATE$(T, x)$, which adds 1 to $f_x$, and write $\mu'$ for the new value of $\mu$. By Lemma 1, $\mu' \ge \mu$, so parts 2 and 3 for the items that the update does not touch stay true.

- *Line L3.* $T[x]$ and $f_x$ both grow by 1, and $\epsilon[x]$ does not change. So part 2 holds for $x$. Part 1 holds because nothing else changes.
- *Line L5.* Here $x \notin T$ and $|T| < k$, so by part 1, $x$ had not arrived, and now $f_x = 1 = T[x]$ and $\epsilon[x] = 0$. If the table is still not full, part 1 holds. If it is now full, parts 2 and 3 follow from part 1: every counter is exact, $\epsilon = 0 \le \mu'$, and every item that is not in $T$ has not arrived.
- *Lines L6 to L8.* Here $x \notin T$ and the table is full, so by part 3, $f_x \le \mu$ before the update, and $f_x \le \mu + 1 = T[x]$ after it. Also $T[x] - \epsilon[x] = 1 \le f_x$, and $\epsilon[x] = \mu \le \mu'$. So part 2 holds for $x$. The removed item $y$ had $f_y \le T[y] = \mu \le \mu'$ by part 2, so part 3 holds for $y$. $\square$

**Theorem.** After $m$ updates, for every item $x$,
$$ f_x \;\le\; \hat f_x \;\le\; f_x + \mu \;\le\; f_x + \frac{m}{k}, $$
and each item with $f_x > m/k$ is in $T$.

*Proof.* For $x \in T$, part 2 of Lemma 2 gives $f_x \le T[x] \le f_x + \epsilon[x] \le f_x + \mu$. For $x \notin T$, part 3 gives $f_x \le \mu = \hat f_x$, and $\hat f_x - f_x \le \mu$ because $f_x \ge 0$. If $|T| < k$, then $\mu = 0 \le m/k$. If $|T| = k$, the $k$ counters are each at least $\mu$ and add up to $m$ by Lemma 1, so $k\mu \le m$. Finally, an item $x \notin T$ has $f_x \le \mu \le m/k$, so an item with $f_x > m/k$ is in $T$. $\square$

**Theorem (isomorphism, Agarwal et al. 2012).** Run Space-Saving with $k$ counters and the Misra-Gries summary with $k - 1$ counters on the same stream. Write $s_x = T[x]$ for $x \in T$ and $s_x = 0$ otherwise, and let $C$ be the Misra-Gries counters, with $c_x = C[x]$ for $x \in C$ and $c_x = 0$ otherwise. Then after each item:

- (a) $c_x = \max(s_x - \mu, 0)$ for every $x$, and
- (b) the number of Misra-Gries decrement steps so far is $\mu$.

*Proof.* By induction on $m$. Both summaries start empty with $\mu = 0$. Assume (a) and (b) before the arrival of $x$. By (a), $C$ is the set of items with $s_y > \mu$. We show that after the update, (a) holds, and that a decrement step happens exactly when $\mu$ grows by 1, while $\mu$ does not change otherwise. This gives (b).

- **Case A: $x \in T$ and $s_x > \mu$.** Space-Saving adds 1 to $s_x$. The counter of $x$ was not the smallest, so $\mu$ does not change. By (a), $x \in C$ with $c_x = s_x - \mu$, so Misra-Gries adds 1 to $c_x$, with no decrement step. Then (a) holds.
- **Case B: $x \in T$ and $s_x = \mu$.** Then $\mu > 0$, because counters in $T$ are positive, so the table is full. By (a), $x \notin C$.
  - *B1: $x$ is the only item with counter $\mu$.* After the update, every counter is at least $\mu + 1$, so $\mu' = \mu + 1$. Before it, the other $k - 1$ items had $s_y > \mu$, so $|C| = k - 1$, and Misra-Gries does a decrement step: each $c_y$ falls by 1 to $s_y - \mu - 1 = s_y - \mu'$, and $x$ stays out with $c_x = 0 = s_x + 1 - \mu'$.
  - *B2: another item also has counter $\mu$.* Then $\mu' = \mu$, and at most $k - 2$ items have $s_y > \mu$, so $|C| \le k - 2$. Misra-Gries inserts $x$ with $c_x = 1 = (s_x + 1) - \mu'$, with no decrement step.
- **Case C: $x \notin T$ and $|T| < k$.** Then $\mu = 0$, and by (a), $C$ is exactly $T$ with the same counters. Space-Saving inserts $x$ with counter 1.
  - *C1: $|T| < k - 1$ before.* The table is still not full, so $\mu' = 0$. Here $|C| < k - 1$, so Misra-Gries also inserts $x$ with counter 1, with no decrement step.
  - *C2: $|T| = k - 1$ before.* Now the table is full and the new counter 1 is the smallest, so $\mu' = 1$. Here $|C| = k - 1$ and $x \notin C$, so Misra-Gries does a decrement step: each $c_y = s_y$ falls to $s_y - 1 = s_y - \mu'$, and $c_x = 0 = 1 - \mu'$.
- **Case D: $x \notin T$ and $|T| = k$.** Then $s_x = 0$ and $c_x = 0$. Space-Saving removes an item $y$ with $s_y = \mu$ and gives $x$ the counter $\mu + 1$.
  - *D1: $y$ was the only item with counter $\mu$.* After the update, every counter is at least $\mu + 1$, so $\mu' = \mu + 1$. Before it, $C$ held the other $k - 1$ items, so $|C| = k - 1$, and Misra-Gries does a decrement step: each $c_z$ falls to $s_z - \mu'$, $c_x = 0 = (\mu + 1) - \mu'$, and $c_y = 0$ with $s_y$ now 0.
  - *D2: another item also has counter $\mu$.* Then $\mu' = \mu$, $|C| \le k - 2$, and Misra-Gries inserts $x$ with $c_x = 1 = (\mu + 1) - \mu'$, with no decrement step. The item $y$ had $c_y = 0$, and now $s_y = 0$, so $c_y = \max(0 - \mu', 0)$ still holds.

In each case the items that the update does not touch keep their $s$, their $c$ changes by $-1$ exactly in a decrement step, and $\mu$ grows by 1 exactly in a decrement step. So (a) holds for them as well, and (b) follows. $\square$

**Corollary.** For every $x$, the Space-Saving estimate $\hat f_x$ equals $c_x + \mu$, the Misra-Gries estimate plus its number of decrement steps.

*Proof.* If $s_x \ge \mu$, then $s_x = \max(s_x - \mu, 0) + \mu = c_x + \mu$, and if $x \in T$ this is $\hat f_x$. If $x \notin T$, then $c_x = 0$ and $\hat f_x = \mu$. Every $x \in T$ has $s_x \ge \mu$ when the table is full, and $\mu = 0$ when it is not. $\square$

**Theorem (merge).** Let two summaries with the same $k$, of streams $\sigma_1$ and $\sigma_2$, each be built by updates or by earlier merges. The merge maps each summary to Misra-Gries counters, merges them with MG-MERGE into $C$, and returns the estimates $\hat f_x = c_x + D$ with $D = \lfloor (m - \sum_y C[y]) / k \rfloor$ and $m = m_1 + m_2$. Then $f_x \le \hat f_x \le f_x + D$ and $D \le m/k$ for the concatenation.

*Proof.* For a summary built by updates, the corollary and the isomorphism show that the map gives the Misra-Gries summary of the same stream with $k - 1$ counters. For a merged summary, the map returns its stored Misra-Gries counters $C$. By the correctness theorem of the [Misra-Gries summary](/misra-gries-summary/), with its parameter equal to $k$, MG-MERGE gives counters with $0 \le f_x - c_x \le (m - \sum_y C[y])/k$ for every $x$. As $f_x - c_x$ is an integer, $f_x - c_x \le D$, so $f_x \le c_x + D = \hat f_x$. Also $\hat f_x - f_x = D - (f_x - c_x) \le D$, and $D \le m/k$ because the counters are not negative. The counters $C$ again satisfy the Misra-Gries invariant, so the argument applies to further merges. $\blacksquare$
