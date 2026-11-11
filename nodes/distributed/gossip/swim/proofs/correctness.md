---
title: SWIM first detects a crash in e/(e - 1) expected periods, round-robin probing bounds the detection time, crashes are always confirmed, and refutations override suspicions
proves: [correctness]
status: full
---

**Setting.** Members run lines L1 to L9 in protocol periods. A crashed member takes no steps and answers no message. Incarnation numbers about a member $M$ are created only by $M$ itself (line L5); every other member only copies them. A member $M$ is *probed* by $M_i$ when $M_i$ runs lines L1 to L4 with target $M$; a probe of a crashed member always fails.

**Claim.**

1. *First detection.* Let a member $M$ crash at the start of a period, with no message loss and all other $n - 1$ members live and holding $M$ in their lists. If each live member picks its target uniformly among its $n - 1$ others, the number of periods until the first failed probe of $M$ is geometric with success probability $p_n = 1 - (1 - 1/(n - 1))^{n - 1}$, so its mean is $1/p_n$, and $1/p_n \to e/(e - 1)$ as $n \to \infty$.
2. *Round-robin bound.* With the probe order of line L9, a live member that keeps $M$ in its list probes $M$ within $2n - 1$ periods after any time.
3. *Completeness.* With the round-robin order, every live member eventually marks a crashed member $M$ as Faulty.
4. *Refutation.* If a live member $M_i$ receives Suspect($M_i$, $b$), the Alive update it creates overrides, at every member that receives it, every entry Suspect($M_i$, $b'$) and Alive($M_i$, $b'$) with $b' \le b$.

**Proof of 1.** In a period with no failed probe of $M$ yet, no member suspects $M$, so all $n - 1$ live members still hold $M$ and each picks $M$ with probability $1/(n - 1)$, independently of the others and of earlier periods. With no loss, a probe of $M$ fails and a probe of a live member succeeds. So a period contains a failed probe of $M$ with probability $p_n = 1 - (1 - 1/(n - 1))^{n - 1}$, independently for each period. The first such period is geometric with mean $1/p_n$. Since $(1 - 1/m)^m \to e^{-1}$, $1/p_n \to 1/(1 - e^{-1}) = e/(e - 1)$. $\square$

**Proof of 2.** The probe list of a member has at most $n - 1$ entries, and one entry is probed per period; entries marked Faulty are skipped without using a period. Fix a time $t$. If $M$ is still ahead in the current pass, it is probed within $n - 1$ periods. Otherwise the current pass ends within $n - 2$ periods, the list is shuffled, and the new pass contains $M$ because $M$ is kept, so $M$ is probed within $n - 1$ more periods. In both cases the wait is at most $2n - 3 \le 2n - 1$ periods. A member that joins during a pass is put at a random place and only lengthens the pass by one, which the bound $2n - 1$ covers. $\square$

**Proof of 3.** Let $a$ be the highest incarnation number that $M$ created before it crashed; it is finite, and no larger one is ever created. Consider a live member $M_i$ that does not mark $M$ Faulty. By claim 2, $M_i$ probes $M$ within $2n - 1$ periods, the probe fails, and line L4 marks $M$ Suspect with the incarnation $M_i$ knows. Only an Alive update with a larger incarnation can remove the suspicion (line L6), and each such removal raises the incarnation that $M_i$ knows for $M$. This can happen at most $a + 1$ times. After the last time, the next suspicion lasts until the timeout, and line L7 marks $M$ Faulty. A Faulty entry is never changed again, because Confirm overrides all updates. $\square$

**Proof of 4.** Line L5 sets $\mathrm{inc}_i = b + 1$ (or more, if $M_i$ had a larger one) and creates Alive($M_i$, $\mathrm{inc}_i$) with $\mathrm{inc}_i > b \ge b'$. By the rule of line L6, Alive($j$, $a$) overrides Suspect($j$, $b'$) and Alive($j$, $b'$) whenever $a > b'$. $\square$

**What is not proved.** Accuracy is probabilistic. A live member is confirmed faulty if, before the suspicion timeout of some member, the Suspect update does not reach it or its Alive answer does not come back, and under message loss this has a small but positive probability. Claim 4 does not help against a Confirm that is already made, because Confirm overrides all updates. The dissemination time of $O(\log n)$ periods is the epidemic behaviour of piggybacking, measured on the page.
