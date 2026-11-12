---
title: CoDel drops only after a full interval above target and follows the square-root control law
proves: [correctness]
status: full
---

We use the pseudocode of the page, with TARGET, INTERVAL and MAXPACKET as given, and write $I$ for INTERVAL. The link calls DEQUEUE whenever it is free and the queue is not empty. Times are real numbers.

**Lemma 1 (only an ok packet is dropped).** Every packet that CoDel drops was returned by a call of DODEQUEUE with $ok = $ true.

*Proof.* Drops happen only at lines L11 and L14. Line L14 runs only when line L13 found $ok$ true for the packet $p$ of line L6, and it drops that $p$. Line L11 runs only when $dropping$ is true. On the first pass of the loop, $dropping$ is still true only if line L9 did not run, that is, only if the call of line L6 gave $ok$ true, and line L11 drops that packet. On a later pass, $dropping$ is still true only if line L12 found $ok$ true for the packet that line L11 popped on the pass before, and that is the packet the pass drops. $\square$

**Lemma 2 (no drop without a standing queue).** Suppose that CoDel drops a packet at time $now$. Then there is a time $t_0 \le now - I$ such that every call of DODEQUEUE in the time interval $[t_0, now]$ popped a packet, every such packet had sojourn time at least TARGET, and every such pop left more than MAXPACKET bytes in the queue.

*Proof.* By Lemma 1, the dropped packet came from a call of DODEQUEUE at time $now$ that returned $ok$ true. That call reached line L5, so $first\_above \ne$ none and $now \ge first\_above$. Let $t_0$ be the time of the call that last set $first\_above$ at line L4. Then $first\_above = t_0 + I$, so $t_0 \le now - I$. Lines L1 and L3 set $first\_above$ to none. Line L4 sets it only when it is none. So no call between the call at $t_0$ and the call at $now$, and neither of these two calls, ran line L1 or took the branch of line L3. A call that does not run line L1 pops a packet. A call that does not take the branch of line L3 popped a packet with sojourn time at least TARGET and left more than MAXPACKET bytes. $\square$

In particular, when the last packet leaves a queue, the pop leaves 0 bytes, so line L3 resets $first\_above$. Hence an empty queue, or a single packet of at most MAXPACKET bytes, always starts the test again. A burst whose packets leave with sojourn time at least TARGET for a stretch of time shorter than $I$, and with some packet below TARGET (or the end of the queue) before and after the stretch, causes no drop.

**Lemma 3 (the control law).** Consider a dropping state that line L14 starts at time $e$, and let $c_0$ be the count that lines L15 and L16 set. While the state lasts, after the $j$-th drop of lines L10 to L12 we have $count = c_0 + j$ and

$$drop\_next = D_{j+1}, \qquad \text{where } D_j = e + I \sum_{i=0}^{j-1} \frac{1}{\sqrt{c_0 + i}}.$$

The $j$-th drop of the loop happens at the first call of DEQUEUE at a time $now \ge D_j$, for each $j \ge 1$ that the state reaches.

*Proof.* Line L17 sets $drop\_next = e + I/\sqrt{c_0} = D_1$ and $count = c_0$. Induction on $j$: before the $j$-th drop, $count = c_0 + j - 1$ and $drop\_next = D_j$. Line L11 adds 1 to $count$, which gives $c_0 + j$. If the state goes on, line L12 adds $I/\sqrt{c_0 + j}$ to $drop\_next$, which gives $D_j + I/\sqrt{c_0+j} = D_{j+1}$. Line L12 adds to $drop\_next$, not to $now$, so the planned times do not depend on the times of the calls. The loop of line L10 drops exactly when $now \ge drop\_next$, so the $j$-th drop happens at the first call at or after $D_j$. If several planned times are already past, one call drops several packets. $\square$

**Lemma 4 (the growth of the drop rate).** For $c_0 = 1$ and $j \ge 1$,

$$2\left(\sqrt{j+1} - 1\right) \le \frac{D_j - e}{I} \le 2\sqrt{j}.$$

*Proof.* For $c_0 = 1$, $(D_j - e)/I = \sum_{i=1}^{j} i^{-1/2}$. The function $x^{-1/2}$ decreases on $x > 0$. So $i^{-1/2} \ge \int_i^{i+1} x^{-1/2} dx$, and the sum is at least $\int_1^{j+1} x^{-1/2} dx = 2\sqrt{j+1} - 2$. Also $i^{-1/2} \le \int_{i-1}^{i} x^{-1/2} dx$ for $i \ge 2$, so the sum is at most $1 + \int_1^j x^{-1/2} dx = 2\sqrt j - 1 \le 2\sqrt{j}$. $\square$

So if a dropping state with $c_0 = 1$ lasts for time $\tau$ and the link serves the queue in that time, the number of planned drops in it is at least $\lfloor (\tau / 2I)^2 \rfloor$ and less than $(\tau/2I + 1)^2$. The number of drops grows like the square of the time, and the drop rate grows linearly. A start with $c_0 > 1$ by line L16 only makes the gaps smaller.

**Lemma 5 (each packet is handled once).** Each call of DODEQUEUE that does not run line L1 pops exactly one packet at line L2. Each popped packet is either dropped at line L11 or L14, or held in $p$ and returned at line L18. Every assignment to $p$ in lines L11 and L14 comes right after the old $p$ was dropped. So no packet is lost without a drop and none is sent twice.

*Proof.* The only assignments to $p$ are at lines L6, L11 and L14. At lines L11 and L14 the old value of $p$ was dropped just before. So the packet in $p$ at line L18 is the last packet popped, and every earlier pop in the same call was dropped. $\square$

**Theorem.** Each packet that enters a CoDel queue is either sent or dropped, exactly once (Lemma 5). CoDel drops a packet only when the sojourn time of every packet that left in the past INTERVAL was at least TARGET (Lemma 2). In a dropping state, the drops follow the planned times $D_j$ of the control law (Lemma 3), whose gaps shrink like $I/\sqrt{count}$ (Lemma 4). $\blacksquare$

Nothing here bounds the sojourn time. That bound would need a model of how the senders respond to drops, and CoDel makes no such assumption. Against traffic that does not respond, as in the overload example of the page, the drop rate settles near the excess of the arrival rate over the link rate, while the delay stays well above TARGET.
