---
title: The PTP offset is exact on symmetric links and within the mean path delay otherwise
proves: [correctness]
status: full
---

We use the pseudocode of the page. Over one exchange the clocks do not drift, and the slave clock reads $o$ more than the master clock at every moment. The Sync spends $a \ge 0$ on links and $r_a \ge 0$ in transparent clocks; the Delay_Req spends $b \ge 0$ on links and $r_b \ge 0$ in transparent clocks. Each transparent clock adds its own residence time to the correctionField of the message, so the fields arrive with values $c_{\mathrm{Sync}} = r_a$ and $c_{\mathrm{Req}} = r_b$. Without transparent clocks, take $r_a = r_b = 0$ and treat queues as part of $a$ and $b$.

**Lemma 1 (the timestamps).** $t_2 - t_1 = a + r_a + o$ and $t_4 - t_3 = b + r_b - o$.

*Proof.* The Sync leaves when the master clock reads $t_1$, so the slave clock reads $t_1 + o$ at that moment. It arrives $a + r_a$ later, so $t_2 = t_1 + o + a + r_a$. The Delay_Req leaves when the slave clock reads $t_3$, when the master clock reads $t_3 - o$. It arrives $b + r_b$ later, so $t_4 = t_3 - o + b + r_b$. $\square$

**Theorem 1.** Lines L1 to L3 give offsetFromMaster $= o + (a - b)/2$ and meanPathDelay $= (a + b)/2$. So the offset is exact when $a = b$, and $|\text{offsetFromMaster} - o| \le \text{meanPathDelay}$ in every case.

*Proof.* By Lemma 1 and the correctionFields, $ms = t_2 - t_1 - r_a = a + o$ and $sm = t_4 - t_3 - r_b = b - o$. Then $(ms - sm)/2 = (a + o - b + o)/2 = o + (a - b)/2$ and $(ms + sm)/2 = (a + b)/2$. Since $a, b \ge 0$, $|a - b|/2 \le (a + b)/2$. $\square$

The residence times $r_a$ and $r_b$ do not appear in the result. So transparent clocks remove the effect of queues, however long and however different in the two directions, and only the asymmetry of the links is left. The gap $t_3 - t_2$ between the two messages also does not appear.

**Theorem 2 (no rule on the same data does better).** If a rule computes an estimate from $t_1, t_2, t_3, t_4$ and the correctionFields only, and is correct within $e$ for all $o$ and all $a, b \ge 0$, then $e \ge (a+b)/2$.

*Proof.* Replace $o$ by $o + s$, $a$ by $a - s$ and $b$ by $b + s$ for any $s$ with $-a \le -s$ and $-b \le s$, that is $-b \le s \le a$. By Lemma 1, $t_2 - t_1$ and $t_4 - t_3$ do not change, so with the same $t_1$ and $t_3$ and the same residence times, all inputs of the rule are the same. The offsets $o + a$ (at $s = a$) and $o - b$ (at $s = -b$) differ by $a + b$, and one estimate is within $e$ of both, so $e \ge (a + b)/2$. $\square$

**Lemma 2 (boundary clocks).** Let clocks $0, 1, \dots, k$ form a chain in which clock $i+1$ is a slave of clock $i$ and moves by its measured offset. Let hop $i$ have link delays $a_i$ and $b_i$. After one pass, clock $k$ differs from clock 0 by $\sum_{i<k} (a_i - b_i)/2$.

*Proof.* By induction on $k$. For $k = 0$ the difference is 0. Let clock $k$ differ from clock 0 by $E_k$, and let clock $k+1$ differ from clock 0 by $x$ before its correction. Its offset from clock $k$ is $x - E_k$. By Theorem 1 it measures $(x - E_k) + (a_k - b_k)/2$ and subtracts it, so its new difference from clock 0 is $x - (x - E_k) - (a_k - b_k)/2 = E_k - (a_k - b_k)/2$. Hence the hop errors add, with the sign convention that the slave subtracts the measured offset; in absolute value the error is at most $\sum_i |a_i - b_i|/2$. $\square$

**The BMCA picks one grandmaster.** The comparison maps each data set to the tuple (priority1, clockClass, clockAccuracy, offsetScaledLogVariance, priority2, clockIdentity) and takes the least tuple in lexicographic order. The clockIdentity is unique, so two different clocks never give equal tuples, and the order is total. If all nodes receive the Announce data of the same set of clocks, they all choose the least tuple, which is the same clock. $\square$
