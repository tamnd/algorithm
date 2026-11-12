---
title: The hands of CLOCK-Pro stop and keep its invariants
proves: [correctness]
status: full
---

We use the pseudocode of the page with $m \ge 2$ pages and a start value $1 \le m_c \le m - 1$. Let $H$, $C$ and $N$ be the numbers of hot pages, resident cold pages and non-resident cold pages. The invariants are:

- (I1) $H + C \le m$;
- (I2) $N \le m$;
- (I3) $1 \le m_c \le m - 1$;
- (I4) $H \le m - m_c$;
- (I5) every hot page is resident and not in a test period, and every non-resident page is cold and in its test period.

The clock is a circular doubly linked list, and every hand points to an entry of it, or to nothing when it is empty. Removing an entry first moves every hand on it to the next entry, so the hands always point to entries of the list.

**$m_c$ (I3).** Lines L6 and L21 clamp $m_c$ from above at $m - 1$, and line L29 clamps it from below at $1$.

**(I5).** A page turns hot on lines L7 and L21, and both make it resident and end its test. A hot page turns cold on line L32 and stays resident. A page becomes non-resident only on line L16, and only if it is in its test period. A non-resident page leaves its test period only on line L29, and line L30 then removes it at once. So (I5) holds at all times.

**Lemma 1 (RUN-HAND-HOT stops).** It is called only by BALANCE, when $H > m - m_c \ge 1$. Each step on a cold entry ends its test or removes it, and no step makes a page hot or sets a bit. Each step on a hot entry with its bit set clears the bit. So within two turns of the clock the hand reaches a hot entry with bit 0, and line L32 stops. A call turns exactly one hot page cold, so BALANCE stops after at most $H$ calls, with $H \le m - m_c$.

**Lemma 2 (RUN-HAND-TEST stops).** It is called while $N > m \ge 2$. Each call is one step. A step on a non-resident entry removes it and lowers $N$. There are more than $m$ non-resident entries in the clock, so the hand reaches one within one turn, and the loop on line L18 stops.

**Lemma 3 (RUN-HAND-COLD stops and evicts one page).** It is called when $H + C = m$. By (I4) before the call, and because every BALANCE inside the call restores (I4), we have $H \le m - m_c \le m - 1$ at every step, so $C \ge 1$: there is always a resident cold page. Each step on a resident cold page with its bit set clears that bit (lines L21 and L24). No step sets a bit, and a page that BALANCE turns cold has bit $0$. So there are at most $m$ such steps. After them, the next resident cold page that the hand reaches has bit $0$, and line L16 evicts it and the run stops. Between two steps on resident cold pages, the hand skips only hot and non-resident entries, at most one turn of the clock.

**Theorem.** (I1) to (I5) hold after every request.

*Proof.* By induction. They hold for the empty clock. Assume they hold before a request for $x$.

*Hit.* Only a bit changes.

*Miss.* If $H + C = m$, Lemma 3 frees one resident page, so $H + C = m - 1$ after line L4. BALANCE inside it restores (I4) each time it is needed, and RUN-HAND-TEST on line L18 restores (I2). After line L4, $x$ is either still a non-resident entry or not in the clock. In the first case, lines L6 to L8 make it hot and resident: $N$ drops by one, $H + C$ grows by one to at most $m$, and BALANCE restores (I4) after the change of $m_c$ (Lemma 1). In the second case, line L10 adds a resident cold page: $H + C$ grows by one to at most $m$, and $N$ does not change. If $H + C < m$ before the request, no eviction happens, and the same two cases apply. Lines L29 and L30 only lower $N$ and $m_c$, and lowering $m_c$ only weakens (I4). So all invariants hold after the request. $\blacksquare$

**Consequences.**

1. *The cache never holds more than $m$ pages,* by (I1), and once it is full a miss evicts exactly one page, by Lemma 3.
2. *Ghosts never hold data and are bounded.* By (I2) and (I5), at most $m$ entries are non-resident, and each one is a cold page still in its test period. The clock has at most $2m$ entries.
3. *A request is a hit if and only if its page is resident,* because pages are loaded on lines L7 and L10 and evicted only on line L16.
4. *Running time.* Each hand step either clears a bit set by an earlier hit, evicts or removes an entry, ends a test, or turns a hot page cold, or it skips an entry. By Lemmas 1 to 3, the skips between two steps of the other kinds are at most one turn, $2m$ entries. The other kinds of step number $O(n)$ over $n$ requests, so the total work is $O(n m)$.

**The test file.** It checks (I1) to (I5), the counts and the links of the clock after every request on 60 seeded random traces, with and without adaptation, and every listed row of the worked example.
