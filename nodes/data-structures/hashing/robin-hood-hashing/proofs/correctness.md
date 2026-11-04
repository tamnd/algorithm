---
title: Robin Hood hashing keeps its invariant, finds each key, and minimizes the sum of squared distances
proves: [correctness, termination]
status: full
---

All slot indices are taken modulo $m$. A slot is *full* when it holds a key. For a full slot $j$, write $T[j]$ for its key and $D[j]$ for the stored distance. A table is *valid* when (a) no key occurs twice, (b) for each full slot $j$, $D[j] = (j - h(T[j])) \bmod m$, (c) at least one slot is EMPTY, and (d) the invariant (R) holds:

> **(R)** For each full slot $j$ with $D[j] > 0$, slot $j - 1$ is full and $D[j-1] \ge D[j] - 1$.

**Lemma 1 (paths are full).** In a valid table, let slot $s$ hold $x$ with distance $t$. Then for each $u = 0, \ldots, t$, the slot $h(x) + u = s - (t - u)$ is full and its distance is at least $u$.

*Proof.* By induction on $t - u$. For $u = t$, slot $s$ is full with distance $t$. If slot $s - (t-u)$ is full with distance $e \ge u$ and $u \ge 1$, then $e > 0$, so by (R) slot $s - (t - u) - 1$ is full with distance at least $e - 1 \ge u - 1$. $\square$

Lemma 1 gives $t + 1$ full slots, and at most $m - 1$ slots are full, so each distance in a valid table is at most $m - 2$.

**Lemma 2 (search).** In a valid table, RH-SEARCH$(T, k)$ returns the slot of $k$ if $k$ is in $T$, and NIL otherwise. It makes at most $m$ probes.

*Proof.* In the iteration with distance $d$, the loop looks at slot $j = h(k) + d$ (line L1 and line L5). It returns a slot only at line L4, where $T[j] = k$, so if $k$ is absent the result is NIL. Each iteration increases $d$ by 1. All stored distances are at most $m - 2$, so in the iteration with $d = m - 1$ line L3 returns, if no earlier line did. So the loop makes at most $m$ probes.

Now let $k$ be at slot $s = h(k) + t$, with distance $t$. For $d < t$, Lemma 1 with $u = d$ shows that slot $h(k) + d$ is full with distance at least $d$, so line L3 does not return. That slot does not hold $k$, because $k$ occurs only once, at $s \ne h(k) + d$ (as $0 \le d < t \le m - 1$). So line L4 does not return either. At $d = t$, slot $s$ holds $k$ with $D[s] = t$, so line L3 does not return and line L4 returns $s$. $\square$

**Lemma 3 (insertion).** If the table is valid, $k$ is not in it, and at least two slots are EMPTY, then RH-INSERT$(T, k)$ ends, the new table is valid, and it holds the old keys and $k$. The slot that becomes full is the first EMPTY slot at or after $h(k)$.

*Proof.* Call the pair $(x, d)$ the key in the hand at slot $j$, at the test of line L8. We prove that at each such test these statements hold:

1. The keys in the table, with $x$, are the old keys and $k$, each once.
2. $d = (j - h(x)) \bmod m$, and (b) holds for each full slot.
3. (R) holds for the table.
4. If $d > 0$, slot $j - 1$ is full and $D[j-1] \ge d - 1$.
5. Exactly the slots that were full before the call are full now.

At the first test, $x = k$, $j = h(k)$ and $d = 0$, and the table is the old one, so 1 to 5 hold.

Suppose that 1 to 5 hold at the test, and slot $j$ is full, so line L8 does not return. Two cases follow.

*Case $D[j] \ge d$.* Line L9 does nothing. Line L10 moves to $j + 1$ with distance $d + 1$, which keeps statement 2 for $x$. Statement 4 at the new position needs slot $j$ full with $D[j] \ge d$, which is the case. Statements 1, 3 and 5 do not change.

*Case $D[j] = e < d$.* Line L9 writes $(x, d)$ into slot $j$ and takes $(T[j], e)$ in the hand. Statement 1 is kept, and (b) holds at slot $j$ by statement 2. (R) at slot $j$: as $d > e \ge 0$, statement 4 gives slot $j-1$ full with $D[j-1] \ge d - 1$. (R) at slot $j + 1$: if it is full with $D[j+1] = f > 0$, then the old (R) gave $e \ge f - 1$, so $d > e \ge f - 1$. (R) at other slots is unchanged. Line L10 moves to $j + 1$ with distance $e + 1$, which is the distance of the new key in the hand at $j + 1$, and statement 4 holds because slot $j$ is full with $D[j] = d > e$. Statement 5 is kept because the same slots are full.

Now suppose the test of line L8 finds slot $j$ EMPTY. Line L8 writes $(x, d)$ there and returns. Statement 1 gives the key set. (b) holds at $j$ by statement 2. (R) at slot $j$ holds by statement 4. (R) at slot $j + 1$: before the write, slot $j$ was EMPTY, so by (R) a full slot $j + 1$ had distance 0, and (R) asks nothing for it. So the table is valid, except possibly (c). By statement 5 only the slot $j$ became full, and two slots were EMPTY, so one is still EMPTY.

Termination: between two tests, $j$ moves one slot to the right and statement 5 says the full slots do not change. There is an EMPTY slot, so after at most $m - 1$ moves the test meets it. Because $j$ moves one slot at a time from $h(k)$, the slot that becomes full is the first EMPTY slot at or after $h(k)$. $\square$

**Lemma 4 (deletion).** If the table is valid, RH-DELETE$(T, k)$ removes $k$ if it is present, keeps all other keys, and leaves a valid table.

*Proof.* By Lemma 2, line L11 finds the slot $j_0$ of $k$ or NIL. If NIL, nothing changes. Otherwise let $j_0 + 1, \ldots, j_0 + r$ be the longest block of full slots after $j_0$ in which each distance is positive, with $r \ge 0$. As one slot is EMPTY, $r \le m - 2$. Slot $j_0 + r + 1$ is EMPTY or holds a key with distance 0. The loop of lines L14 to L16 copies the entry of slot $j_0 + q$ to slot $j_0 + q - 1$ with distance one less, for $q = 1, \ldots, r$, and line L17 makes slot $j_0 + r$ EMPTY. The key $k$ is overwritten (or, if $r = 0$, its slot is emptied), and each other key moves at most once, so the key set is the old one without $k$.

(b): a key moved one slot left gets its distance lowered by 1, which is right, and the old distance was at least 1, so the new one is at least 0.

(R): let $y_q$ be the key that was at $j_0 + q$, with old distance $e_q > 0$, for $1 \le q \le r$. Inside the block, for $2 \le q \le r$, the old (R) gave $e_{q-1} \ge e_q - 1$, and both values drop by 1, so (R) holds between the new slots $j_0 + q - 2$ and $j_0 + q - 1$. At the new slot $j_0$ (key $y_1$, distance $e_1 - 1$): if $e_1 - 1 > 0$, the old (R) at $j_0 + 1$ gave $D[j_0] \ge e_1 - 1 > 0$ for the old key $k$; then the old (R) at $j_0$ gave slot $j_0 - 1$ full with distance at least $D[j_0] - 1 \ge e_1 - 2$, which is what (R) asks. Slot $j_0 - 1$ is not changed by the shift, because $r \le m - 2$. Slot $j_0 + r$ is now EMPTY, and slot $j_0 + r + 1$ is EMPTY or has distance 0, so (R) asks nothing there. Other slots do not change. (c) holds because the number of EMPTY slots grows by one. $\square$

**Theorem 1 (correctness).** Start from an EMPTY table with $m \ge 2$ slots, and apply RH-INSERT (for a key that is not present, with at least two EMPTY slots), RH-DELETE and RH-SEARCH in any order. Then each table is valid, the set of keys is the one given by the operations, and each search answers correctly. Each operation ends after $O(m)$ steps.

*Proof.* The EMPTY table is valid. Lemmas 3 and 4 keep validity and give the key set, by induction on the number of operations, and Lemma 2 gives the answer and the bound for search. The loop of RH-DELETE moves over at most $r \le m - 2$ slots. $\blacksquare$

## The sum of the distances and the sum of their squares

Fix a set $K$ of $n < m$ keys. Call an assignment of the keys to distinct slots a *linear probing layout* when, for each key $x$ at slot $s$, every slot from $h(x)$ to $s$ (going right) is full. Its distance is $d(x) = (s - h(x)) \bmod m$. By Lemma 1, each valid Robin Hood table is a linear probing layout.

**Theorem 2.** Let $L$ and $L'$ be two linear probing layouts of $K$ with the same set $F$ of full slots. Then $\sum_{x} d_L(x) = \sum_x d_{L'}(x)$. If $L$ is a valid Robin Hood table, then $\sum_x d_L(x)^2 \le \sum_x d_{L'}(x)^2$.

*Proof.* For a slot $s$, let $a(s)$ be the number of keys with $h(x) = s$, let $o(s) = 1$ if $s \in F$ and 0 otherwise, and let $c(s)$ be the number of keys whose path from $h(x)$ to its slot contains both $s$ and $s + 1$. A key at distance $d$ crosses exactly $d$ such boundaries, so $\sum_x d(x) = \sum_s c(s)$.

The keys whose path contains $s$ are the keys with home $s$ and the keys that cross the boundary from $s - 1$ to $s$; these are disjoint, because a path is shorter than $m$. Of these keys, exactly $o(s)$ sit at $s$, and the others cross to $s + 1$. So $c(s) = c(s-1) + a(s) - o(s)$. If $s \notin F$, no path contains $s$, so $c(s) = 0$. Pick $s_0 \notin F$, which exists because $n < m$. Then $c(s_0) = 0$, and the recursion gives $c(s_0 + 1), c(s_0 + 2), \ldots$ from $a$ and $o$ only. So $c$, and with it the sum of distances, is the same for $L$ and $L'$.

For the squares, cut the circle at $s_0$ and number the slots $s_0 + 1, \ldots, s_0 + m - 1$ as $1, \ldots, m - 1$. No path contains $s_0$, so each path lies in this range and is an interval $[h(x), s]$ of integers, with $d(x) = s - h(x)$. Suppose a layout $L'$ has keys $x$ at slot $p$ and $y$ at slot $q$ with $p < q$ and $h(x) > h(y)$. Swap them. Then $y$ is at $p$ with $h(y) < h(x) \le p$, and $x$ is at $q > p \ge h(x)$, and the set of full slots is the same, so the result is again a linear probing layout with full set $F$. The change in the sum of squares is

$$(p - h(y))^2 + (q - h(x))^2 - (p - h(x))^2 - (q - h(y))^2 = -2(q - p)(h(x) - h(y)) < 0.$$

The number of layouts is finite, so a layout with the least sum of squares exists, and by the swap it has no such pair: its homes do not decrease from left to right. Call such a layout *sorted*. In a sorted layout, the slots in $F$ are filled from left to right by the keys in order of home, so the multiset of distances is the same for every sorted layout (keys with equal homes can trade places without a change of distances). So every sorted layout has the least sum of squares.

A valid Robin Hood table is sorted. Take two full slots $s < s'$ in the range. If all slots from $s$ to $s'$ are full, it is enough to look at $s' = s + 1$. If $D[s+1] > 0$, (R) gives $h(T[s+1]) = s + 1 - D[s+1] \ge s + 1 - (D[s] + 1) = h(T[s])$. If $D[s+1] = 0$, then $h(T[s+1]) = s + 1 > s \ge h(T[s])$. If an EMPTY slot $e$ lies between $s$ and $s'$, the path of $T[s']$ does not contain $e$, so $h(T[s']) > e > s \ge h(T[s])$. $\blacksquare$

**Consequence.** Lemma 3 shows that RH-INSERT fills the first EMPTY slot at or after the home slot, as plain linear probing does. So the two methods, run on the same sequence of insertions, have the same set of full slots after each step. By Theorem 2 they have the same mean distance, and Robin Hood has the least variance of the distance among all linear probing layouts with these full slots.
