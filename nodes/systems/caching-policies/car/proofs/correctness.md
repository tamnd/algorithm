---
title: CAR terminates and keeps the invariants I1 to I7
proves: [correctness]
status: full
---

We use the pseudocode of the page with cache size $c \ge 1$. All four lists start empty and $p = 0$. Let $D = |T_1| + |T_2| + |B_1| + |B_2|$ be the size of the directory. The invariants of the paper are:

- I1: $0 \le |T_1| + |T_2| \le c$.
- I2: $0 \le |T_1| + |B_1| \le c$.
- I3: $0 \le |T_2| + |B_2| \le 2c$.
- I4: $0 \le D \le 2c$.
- I5: if $|T_1| + |T_2| < c$, then $B_1$ and $B_2$ are empty.
- I6: if $D \ge c$, then $|T_1| + |T_2| = c$.
- I7: once the cache is full, it stays full.

We also show that $0 \le p \le c$ and that the four lists are disjoint.

**Lemma 1 (REPLACE stops).** Call REPLACE when $|T_1| + |T_2| = c$ and $0 \le p \le c$. Then every step picks a clock that is not empty, and REPLACE stops after at most $c + 1$ steps. It evicts exactly one page, puts its key in $B_1$ or $B_2$, and changes nothing else except bits and the positions of pages inside $T_1 \cup T_2$.

*Proof.* A step that does not stop moves one page within $T_1 \cup T_2$, so $|T_1| + |T_2| = c$ holds at every step. If line L18 picks $T_1$, then $|T_1| \ge 1$. If it picks $T_2$ and $T_2$ were empty, then $|T_1| = c \ge \max(1, p)$, so line L18 would have picked $T_1$. So the picked clock has a head page. A step that does not stop clears the bit of that page (lines L21 and L25). No step sets a bit. There are at most $c$ set bits, so after at most $c$ steps that do not stop, the next step finds a page with bit $0$ and stops. $\blacksquare$

**Lemma 2 (invariants).** I1 to I7 hold after every request, as do $0 \le p \le c$ and disjointness.

*Proof.* By induction on the requests. All hold at the start. Assume they hold before a request for $x$.

*Hit, $x \in T_1 \cup T_2$.* Only a bit changes.

*Miss with $|T_1| + |T_2| < c$.* By I5, $B_1$ and $B_2$ are empty, so lines L3 to L8 do nothing and line L10 puts $x$ in $T_1$. Then $|T_1| + |T_2| \le c$, which is I1. Since the ghost lists are empty, $|T_1| + |B_1| = |T_1| \le c$ and $D = |T_1| + |T_2| \le c$, which give I2, I3 and I4. If the cache is still not full, the ghost lists are still empty, which is I5. And $D = |T_1| + |T_2|$, so I6 holds.

*Miss with $|T_1| + |T_2| = c$.* By Lemma 1, REPLACE moves one key from $T_1 \cup T_2$ to $B_1 \cup B_2$. Then $|T_1| + |T_2| = c - 1$ and $D$ does not change. The value $|T_1| + |B_1|$ does not grow: an eviction from $T_1$ moves a key from $T_1$ to $B_1$, a move from $T_1$ to $T_2$ makes it smaller, and an eviction from $T_2$ does not touch it. So after REPLACE, $|T_1| + |B_1| \le c$ and $|T_1| \le c - 1$. Now there are four cases.

- $x \notin B_1 \cup B_2$ and $|T_1| + |B_1| = c$. Then $|B_1| \ge 1$, line L6 deletes a key of $B_1$, and line L10 adds $x$ to $T_1$. So $|T_1| + |B_1| = c$ and $D$ is unchanged.
- $x \notin B_1 \cup B_2$, $|T_1| + |B_1| < c$ and $D = 2c$. Then $|T_2| + |B_2| = D - (|T_1| + |B_1|) \ge c + 1$ and $|T_2| \le c - 1$, so $|B_2| \ge 2$ and line L8 can delete a key of $B_2$. Line L10 adds $x$ to $T_1$. So $|T_1| + |B_1| \le c$ and $D = 2c$.
- $x \notin B_1 \cup B_2$, $|T_1| + |B_1| < c$ and $D < 2c$. Nothing is deleted, and line L10 adds $x$. So $|T_1| + |B_1| \le c$ and $D \le 2c$.
- $x \in B_1$ or $x \in B_2$. No key is deleted. Line L13 or L16 moves $x$ from its ghost list to $T_2$. So $|T_1| + |B_1|$ does not grow and $D$ is unchanged.

In every case the cache ends with $c$ pages, so I1, I6 and I7 hold, and I5 holds because its condition is false. I2 and I4 were shown case by case. I3 follows from I4. Lines L12 and L15 clamp $p$ to $[0, c]$. A key enters a list only after it leaves another one or after a check that it is in no list, so the lists stay disjoint. $\blacksquare$

**Consequences.**

- A request is a hit if and only if its page is in $T_1 \cup T_2$, and these are the cached pages. Pages are loaded on lines L10, L13 and L16, and evicted only on lines L20 and L24.
- Once $c$ distinct pages have been requested, the cache holds exactly $c$ pages. Before that, the cache holds every page requested so far, because nothing is evicted while the cache is not full.
- The total number of hand steps in REPLACE over $n$ requests is at most $2n$. Each step either stops REPLACE, at most once for each request, or clears a bit, and each bit was set by one hit.

**The test file.** It checks I1 to I7, the bound on $p$ and disjointness after every request on 60 seeded random traces, the hit flags against a second CAR written with plain lists, and every row of the worked example.
