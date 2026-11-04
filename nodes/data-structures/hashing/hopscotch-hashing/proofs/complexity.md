---
title: Worst-case and expected cost of hopscotch hashing
proves: [time.worst, time.expected]
status: sketch
---

**Worst case of search and delete.** The loops of lines L18 and L22 run $H$ times, and each pass tests one bit and makes at most one key comparison. So each operation takes $O(H)$ time, when a hash value and a key comparison cost $O(1)$. The bound is reached: put $H$ keys with the same home $i$ in a table with $H \le m$; a search for another key with home $i$ compares it with all $H$ keys.

**Worst case of HOP-PLACE.** By Lemma 3 of [the correctness proof](correctness.md), the loop of line L7 makes at most $m$ passes, and the loop of lines L9 to L15 makes at most $e - H + 1 \le m$ passes, since $e$ falls by at least 1 at each pass and the loop stops when $e < H$. A pass looks at the $H - 1$ bitmaps $\mathrm{hop}[(j - t) \bmod m]$ for $t = H - 1, \ldots, 1$. On the [word RAM](/word-ram/) with $H \le w$, the test of line L11 for one bitmap is $x \wedge (2^t - 1) \ne 0$, and the smallest such $d$ is the index of the lowest set bit of that word, both $O(1)$ word operations. So a pass takes $O(H)$ time, and HOP-PLACE takes $O(m + mH) = O(mH)$ time. One attempt of RESIZE to $m'$ slots makes $n \le m'$ calls of HOP-PLACE, each in $O(m'H)$; a sharper count follows from the expected case below.

**Lemma 4 (the same full slots as linear probing).** Consider a sequence of inserts of distinct keys into an empty hopscotch table with $m$ slots, with no delete and no failed HOP-PLACE, and the same sequence in a linear-probing table with $m$ slots and the same homes. After each insert, the two tables have the same set of full slots.

*Proof.* By induction on the number of inserts. Before an insert of $k$, the two sets of full slots are equal, so line L7 stops at the slot $j$ where linear probing puts $k$: the first empty slot at or after $\mathrm{home}(k)$. Each pass of the loop L9 to L15 fills the empty slot $j$ and empties a slot $s$ that was full; and line L16 fills the last empty slot of the chain. So the net change of the set of full slots is that slot $j$ becomes full, as in linear probing. $\square$

**Expected cost of HOP-PLACE.** Assume the homes of the keys are independent and uniform on the $m$ slots, and that $n = \alpha m$ keys are in the table, inserted as in Lemma 4. Then the distance $e$ found by line L7 is the number of probes of an unsuccessful search of linear probing in a table with $n$ keys, minus 1. Knuth (Volume 3, Section 6.4, the analysis of Algorithm L) shows that the expected number of such probes is about $\frac{1}{2}\big(1 + 1/(1 - \alpha)^2\big)$ for large $m$ and fixed $\alpha < 1$; see the [analysis of linear probing](/linear-probing-analysis/). We quote this result and do not prove it here. The loop L9 to L15 makes at most $e$ passes of $O(H)$ time each, so the expected time of HOP-PLACE is

$$O\big(1 + E[e] \cdot H\big) = O\Big(1 + \frac{H}{(1 - \alpha)^2}\Big).$$

This bounds an insert that does not trigger a resize. The probability that HOP-PLACE fails depends on $H$ and $\alpha$; Herlihy, Shavit and Tzafrir study it by experiment, and this proof does not bound it. With deletes, Lemma 4 no longer holds as stated, because hopscotch hashing empties the slot of a deleted key while linear probing must keep a tombstone or move keys back. $\blacksquare$
