---
title: Hopscotch hashing keeps its neighbourhood invariant and implements a dictionary
proves: [correctness, termination]
status: full
---

Write $\mathrm{home}(k) = h(k) \bmod m$ and $\delta(s, i) = (s - i) \bmod m$ for the distance of slot $s$ from slot $i$. Assume $1 \le H \le m$. Then for each slot $i$, the slots $(i + d) \bmod m$ for $d = 0, \ldots, H - 1$ are $H$ distinct slots, so bit $d$ of $\mathrm{hop}[i]$ names one slot. The invariant (P1), (P2), (P3) is the one on the page, and $D$ is the set of pairs in full slots.

**Lemma 1 (one neighbourhood suffices).** Assume (P1) and (P2). A key $k$ is in the table if and only if, with $i = \mathrm{home}(k)$, there is a $d < H$ such that bit $d$ of $\mathrm{hop}[i]$ is 1 and slot $(i + d) \bmod m$ holds $k$.

*Proof.* If $k$ is in slot $s$, let $d = \delta(s, i)$. By (P1), $d < H$, and $s = (i + d) \bmod m$. Slot $s$ holds a key with home $i$, so bit $d$ of $\mathrm{hop}[i]$ is 1 by (P2). The converse is clear. $\square$

So the loops of lines L2 and L3, L18 and L19, and L22 and L23 find $k$ if and only if $k$ is in the table, and they find its only slot, by (P3).

**Lemma 2 (one displacement).** Assume (P1) and (P2), let slot $j$ be empty, and let $t$, $d$, $b$ and $s$ be as in lines L11 and L13, so $1 \le t \le H - 1$, $0 \le d < t$, $b = (j - t) \bmod m$, bit $d$ of $\mathrm{hop}[b]$ is 1 and $s = (b + d) \bmod m$. After line L14, (P1) and (P2) hold, slot $s$ is empty, and $D$ is the same.

*Proof.* By (P2), slot $s$ holds a key $x$ with home $b$. Line L14 moves the pair of $x$ to slot $j$, which was empty, and empties slot $s$; so $D$ does not change. Now $\delta(j, b) = t < H$, so (P1) holds for $x$, and it holds for every other key, which did not move.

For (P2), only the bits that refer to slots $s$ and $j$ can change their truth. Slot $s$ is $(b + d) \bmod m$ and slot $j$ is $(b + t) \bmod m$. For bucket $b$: slot $s$ no longer holds a key with home $b$, and line L14 clears bit $d$; slot $j$ now holds $x$, with home $b$, and line L14 sets bit $t$. For a bucket $c \ne b$: before the move, slot $s$ held $x$, whose home is not $c$, and slot $j$ was empty, so all the bits of $c$ that name $s$ or $j$ were 0. After the move, slot $s$ is empty and slot $j$ holds $x$, whose home is not $c$, so these bits must still be 0, and they are, since line L14 changes only $\mathrm{hop}[b]$. $\square$

**Lemma 3 (HOP-PLACE).** Assume (P1), (P2) and (P3), and that $k$ is not in the table. Then HOP-PLACE$(T, k, v)$ ends after at most $m$ passes of each of its loops. If it returns OK, (P1) and (P2) hold, and the full slots hold the old pairs and $(k, v)$, each once. If it returns FAIL, (P1), (P2) and (P3) hold and $D$ is the same as before the call.

*Proof.* The loop of line L7 raises $e$ at each pass and stops at $e = m$, so it ends after at most $m$ passes. If it stops with $e = m$, all slots are full, and line L8 returns FAIL with nothing changed. Otherwise slot $(i + e) \bmod m$ is empty, with $e < m$.

For the loop of lines L9 to L15, use the loop invariant: (P1) and (P2) hold, $D$ is the set of the old pairs, $0 \le e < m$, and slot $(i + e) \bmod m$ is empty. It holds at the first test of line L9 by the paragraph above. In a pass, $e \ge H$, and line L10 sets $j = (i + e) \bmod m$, which is empty. If line L12 returns FAIL, nothing has changed in this pass, and the claim of the lemma for FAIL follows from the loop invariant; (P3) holds since $D$ and the set of full slots did not change. Otherwise Lemma 2 applies, so after line L14, (P1) and (P2) hold, $D$ is the same, and slot $s$ is empty, where

$$s = (b + d) \bmod m = (j - t + d) \bmod m = (i + e - (t - d)) \bmod m.$$

Line L15 sets $e' = e - (t - d)$. Since $1 \le t - d \le t \le H - 1$ and $e \ge H$, we get $1 \le e' < e < m$, and slot $(i + e') \bmod m = s$ is empty. So the loop invariant holds again. As $e$ falls by at least 1 at each pass and stays at least 1, the loop makes at most $m$ passes.

When the loop ends, $e < H$ and slot $q = (i + e) \bmod m$ is empty. By (P2), every bit that names slot $q$ is 0, in particular bit $e$ of $\mathrm{hop}[i]$. Line L16 puts $(k, v)$ in slot $q$ and sets that bit. Then (P1) holds for $k$, as $\delta(q, i) = e < H$, and (P2) holds: the only bits that name slot $q$ belong to the buckets $c$ with $\delta(q, c) < H$, and of these only bucket $i$ is the home of the key in slot $q$. The full slots hold the old pairs, which are distinct, and $(k, v)$, and $k$ was absent. $\square$

**Theorem.** Start from the empty table, with $1 \le H \le m$, and apply any sequence of HOP-INSERT, HOP-SEARCH and HOP-DELETE in which every call to RESIZE returns. After each call, (P1), (P2) and (P3) hold, $D$ is the map that the same sequence gives on an abstract dictionary, and each search returns the value of its key in $D$, or NIL. HOP-SEARCH, HOP-DELETE and each call to HOP-PLACE end after at most $H$, $H$ and $2m$ passes of their loops.

*Proof.* **Base.** No slot is full and all bits are 0, so the invariant holds and $D$ is empty.

**Search.** By Lemma 1, lines L17 to L20 return the value of $k$ if $k$ is a key and NIL otherwise, after at most $H$ passes, and change nothing.

**Delete.** By Lemma 1, lines L21 to L23 find the slot $q = (i + d) \bmod m$ of $k$ if $k$ is a key. Line L24 empties it, clears bit $d$ of $\mathrm{hop}[i]$ and lowers $n$. (P1) holds for the other keys, which did not move. For (P2), only bits that name slot $q$ change truth; the one that was 1 was bit $d$ of the home $i$ of $k$, which is now 0, and the others were 0 and stay 0. (P3) holds, and $D$ loses exactly the pair of $k$. If $k$ is not a key, nothing changes.

**Insert.** By Lemma 1, lines L1 to L3 find $k$ if it is a key, and then only its value changes. Otherwise $k$ is absent. Each call of HOP-PLACE at line L4 that returns FAIL leaves the invariant and $D$, by Lemma 3. Then RESIZE$(T, 2m)$ saves the list $P$ of the pairs, which are $|D| = n$ pairs with distinct keys. Each attempt of lines L27 and L28 starts from an empty table of $m' \ge m$ slots, in which the invariant holds with $D$ empty, and calls HOP-PLACE on the pairs of $P$, none of which is in the table yet, since the keys of $P$ are distinct. By Lemma 3, after an attempt in which all calls return OK, the table holds exactly the pairs of $P$ and (P1) and (P2) hold; $n$ was not changed and equals $|P|$, so (P3) holds. Since $H \le m \le m'$, the condition $H \le m'$ holds for each new size. So when RESIZE returns, the invariant holds and $D$ is as before. When HOP-PLACE at line L4 returns OK, Lemma 3 shows that the table holds the old pairs and $(k, v)$, and line L5 raises $n$, so (P3) holds and $D$ gains exactly $(k, v)$.

By induction on the number of calls, the claims hold after each call. $\blacksquare$

The theorem assumes that RESIZE returns. It does when, for some size $m'$, all the placements succeed; this fails forever when more than $H$ keys have the same value $h(k)$, as the page explains. The Python version stops with an error in that case and when the table would pass $2^{20}$ slots, which keeps the invariant, since a failed HOP-PLACE does.
