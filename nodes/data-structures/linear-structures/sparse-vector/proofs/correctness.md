---
title: The sparse vector operations return the vector values and keep the invariant
proves: [correctness]
status: full
---

**Statement.** Let each sparse vector satisfy (I1) to (I3) of the page, and let $v_i$ denote the entry that (I3) assigns. Assume the table $T$ behaves as a map: after T-PUT$(T, i, x)$ the key $i$ maps to $x$, after DELETE$(T, i)$ the key $i$ is absent, the other keys keep their values, and iteration visits each pair of $T$ once. Then, for indices $0 \le i < d$ and vectors of equal dimension:

1. after PUT$(v, i, x)$, the vector satisfies (I1) to (I3) with $v_i = x$ and every other entry unchanged;
2. GET$(v, i)$ returns $v_i$;
3. DOT$(u, w)$ returns $\sum_{i=0}^{d-1} u_i w_i$, and DOT-DENSE$(u, a)$ returns $\sum_{i=0}^{d-1} u_i a[i]$;
4. PLUS$(u, w)$ returns a vector $r$ that satisfies (I1) to (I3) with $r_i = u_i + w_i$ for every $i$, and leaves $u$ and $w$ unchanged.

**Proof.**

*Part 1.* If $x = 0$, line L1 deletes $i$, so $i$ is not a key and (I3) gives $v_i = 0 = x$. If $x \ne 0$, line L2 maps $i$ to $x$, so (I3) gives $v_i = x$, and the new value is nonzero. In both cases the other keys and their values are unchanged, so the other entries are unchanged and still satisfy (I2) and (I3). The only key that may be added is $i$, and $0 \le i < d$, so (I1) holds.

*Part 2.* Line L3 returns $T[i]$ if $i$ is a key and 0 otherwise, which is $v_i$ by (I3).

*Part 3.* Exchanging $u$ and $w$ on line L4 does not change the sum, since $u_i w_i = w_i u_i$. Let $K$ be the set of keys of $u.T$ after line L4. We show the loop invariant: after the loop has visited a set $S \subseteq K$ of pairs, $s = \sum_{i \in S} u_i w_i$. It holds with $S = \emptyset$ and $s = 0$ by line L5. A round visits a new pair $(i, x)$ with $x = u_i$ by (I3), and adds $x \cdot \mathrm{GET}(w, i) = u_i w_i$ by part 2, so the invariant holds for $S \cup \{i\}$. The loop visits each pair once, so at line L8 $S = K$ and $s = \sum_{i \in K} u_i w_i$. For an index $i \notin K$, (I3) gives $u_i = 0$, so $u_i w_i = 0$, and $\sum_{i \in K} u_i w_i = \sum_{i=0}^{d-1} u_i w_i$. The proof for DOT-DENSE is the same with $a[i]$ in place of GET$(w, i)$.

*Part 4.* Line A1 makes $r$ a copy of $u$, so $r$ satisfies (I1) to (I3) with $r = u$, and later changes to $r$ do not touch $u$. The loop reads $w$ and never writes it. Let $S$ be the set of keys of $w.T$ visited so far. The loop invariant is: $r$ satisfies (I1) to (I3), and $r_i = u_i + w_i$ for $i \in S$, and $r_i = u_i$ for $i \notin S$. It holds at the start with $S = \emptyset$. A round visits a new pair $(i, x)$ with $x = w_i$. Before the round, $r_i = u_i$ since $i \notin S$, and GET$(r, i)$ returns it by part 2. Line A3 calls PUT$(r, i, u_i + w_i)$, which by part 1 keeps (I1) to (I3), sets $r_i = u_i + w_i$, and changes no other entry. So the invariant holds for $S \cup \{i\}$. At line A4 every key of $w.T$ is in $S$. For $i \notin S$, (I3) for $w$ gives $w_i = 0$, so $r_i = u_i = u_i + w_i$. Hence $r_i = u_i + w_i$ for every $i$. When $u_i + w_i = 0$, part 1 shows that index $i$ is not stored, so (I2) holds for $r$.

Each loop visits a finite table once and each round takes finitely many steps, so every operation stops. $\blacksquare$
