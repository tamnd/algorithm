---
title: 2Q serves each request, keeps its invariants, and is not competitive when K_in + K_out + 2 is at most c
proves: [correctness]
status: full
---

**Setting.** The cache has $c \ge 1$ slots, and $0 \le K_{in} < c$ and $K_{out} \ge 0$. The resident set is $R = A1_{in} \cup A_m$. The lines are those of the main page.

**Lemma 1 (invariants).** After each request: (a) the three queues are pairwise disjoint and hold no page twice; (b) $|R| \le c$; (c) $|A1_{out}| \le K_{out}$; (d) the requested page is in $R$.

*Proof.* By induction on the requests. At the start all queues are empty. Consider a request to $x$.

- *Line L3 or L4.* No queue changes except the order of $A_m$, so (a), (b) and (c) still hold, and $x \in R$.
- *RECLAIM.* If $|R| < c$, line L8 changes nothing. Else $|R| = c$ by (b). If $|A1_{in}| > K_{in}$, line L9 moves the tail $y$ of $A1_{in}$ to $A1_{out}$. Before this, $y \notin A1_{out}$ by (a), so the queues stay disjoint, and the trim keeps (c). If $|A1_{in}| \le K_{in}$, then $|A_m| = c - |A1_{in}| \ge c - K_{in} \ge 1$, so line L10 can page out the tail of $A_m$. In both cases $|R| \le c - 1$ after RECLAIM.
- *Line L5.* Here $x$ is in $A1_{out}$, so by (a) it is not resident. Line L5 removes $x$ from $A1_{out}$, so after RECLAIM the page $x$ is in no queue. It then enters $A_m$, and $|R| \le c$.
- *Line L6.* Here $x$ is in no queue. After RECLAIM, it enters $A1_{in}$, and $|R| \le c$.

In each case (a) to (d) hold after the request. $\square$

So 2Q is a correct online paging rule: each request is served, at most $c$ pages are resident, and a miss loads only the requested page.

**Lemma 2 (the size of $A1_{in}$).** Let the cache be full, $|R| = c$, and let $|A1_{in}| \le K_{in} + 1$. Then after each later request that takes line L6, the cache is still full and $|A1_{in}| \le K_{in} + 1$.

*Proof.* The cache is full, so RECLAIM frees one slot and line L6 fills it. If $|A1_{in}| > K_{in}$, then $|A1_{in}| = K_{in} + 1$, line L9 removes one page from $A1_{in}$ and line L6 adds one, so the size stays $K_{in} + 1$. Else line L10 runs and $A1_{in}$ grows by one, to at most $K_{in} + 1$. $\square$

**Lemma 3 (a long prefix).** If $K_{out} \ge 1$, there is a request sequence $\pi$ after which the cache is full and $|A1_{in}| \le K_{in} + 1$.

*Proof.* First request $c$ new pages. They all go to $A1_{in}$ by line L6, and the cache is full. Now repeat the following step while $|A_m| < c - K_{in} - 1$, that is, while $|A1_{in}| > K_{in} + 1$. Request a new page $s$; line L6 puts it in $A1_{in}$. Then request new pages until $s$ is in $A1_{out}$. Each of these requests takes line L6 with $|A1_{in}| > K_{in}$, so line L9 pages out the tail of $A1_{in}$, and $|A1_{in}|$ does not change. So $s$ reaches the tail and moves to the head of $A1_{out}$ after at most $c$ requests, and it is there because $K_{out} \ge 1$. Then request $s$ again: line L5 applies, line L9 pages out a page of $A1_{in}$, and $s$ enters $A_m$. The step makes $|A_m|$ larger by one and leaves the cache full. After at most $c$ steps, $|A1_{in}| = K_{in} + 1$. $\square$

**Theorem 4 (not competitive).** Let $K_{out} \ge 1$ and $K_{in} + K_{out} + 2 \le c$. Then there are no constants $\alpha$ and $\beta$ with $\mathrm{2Q}(\sigma) \le \alpha \cdot \mathrm{OPT}(\sigma) + \beta$ for all $\sigma$.

*Proof.* Let $\pi$ be the prefix of Lemma 3. Let $w_1, \ldots, w_c$ be $c$ pages that do not occur in $\pi$, and let $\sigma_r = \pi$ followed by $r$ copies of $w_1, \ldots, w_c$.

Look at the concatenated queue $Q$: the pages of $A1_{in}$ from head to tail, then the identifiers of $A1_{out}$ from head to tail. We show by induction that, after $\pi$, each request of $\sigma_r$ takes line L6 and is a miss.

Assume that this is true for all earlier requests after $\pi$. Then each of them took line L6. Line L6 adds one page at the head of $Q$. Line L9 moves the tail of $A1_{in}$ to the head of $A1_{out}$, which keeps the order of $Q$, and the trim removes the tail of $Q$. Line L10 does not change $Q$. So after $\pi$, $Q$ acts as a FIFO queue: pages enter at the head and leave only at the tail. By Lemma 2, $|A1_{in}| \le K_{in} + 1$, so $|Q| \le K_{in} + 1 + K_{out}$.

Now consider a request to $w_j$. If it is in the first copy, $w_j$ is new and in no queue, so line L6 applies. Else $w_j$ entered the head of $Q$ at its previous request, $c$ requests earlier. Since then, $c - 1$ other pages entered $Q$ at the head, and $c - 1 \ge K_{in} + K_{out} + 1 \ge |Q|$. So $w_j$ has left $Q$ at the tail. It was never in $A_m$, because a page enters $A_m$ only in line L5, and no request after $\pi$ took line L5. So $w_j$ is in no queue, and line L6 applies again. This completes the induction.

So $\mathrm{2Q}(\sigma_r) \ge c \cdot r$. An offline rule can serve $\pi$ as the optimum does, then load $w_1, \ldots, w_c$ with $c$ misses and keep them. So $\mathrm{OPT}(\sigma_r) \le \mathrm{OPT}(\pi) + c$, which does not depend on $r$. Then $c \cdot r \le \alpha (\mathrm{OPT}(\pi) + c) + \beta$ fails for large $r$. $\blacksquare$

**Corollary 5.** With $K_{in} = c/4$ and $K_{out} = c/2$, the condition is $3c/4 + 2 \le c$, that is $c \ge 8$. So 2Q with the parameters of Johnson and Shasha is not competitive for each $c \ge 8$.

**Remark.** If $K_{out} = 0$, the set $A1_{out}$ is always empty, line L5 never applies, and $A_m$ stays empty. A full cache then has $|A1_{in}| = c > K_{in}$, so line L9 always pages out the oldest page: 2Q is FIFO, which is $c$-competitive. The proof above does not cover the case $K_{in} + K_{out} + 2 > c$ with $K_{out} \ge 1$.

The tests check Lemma 1 on random sequences, compare the rule with an independent list model, and check Theorem 4 for $c = 8$, $K_{in} = 2$ and $K_{out} = 4$, where each request of the cycle is a miss while the offline optimum stays below the cost of the prefix plus $c$.
