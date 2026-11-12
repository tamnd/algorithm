---
title: The counter algorithm returns exactly the closure X+
proves: [correctness]
status: full
---

Let $F = W_1 \to Z_1, \ldots, W_k \to Z_k$ and $X \subseteq U$. Recall that $X^+$ is the least set $C$ with $X \subseteq C$ and with $W_i \subseteq C \Rightarrow Z_i \subseteq C$ for each $i$. By [Armstrong's axioms](/armstrongs-axioms/), this is the set of $A$ with $F \models X \to A$. Each FD $W_i \to Z_i$ of $F$ satisfies $W_i \subseteq X^+ \Rightarrow Z_i \subseteq X^+$, so a set obtained from $X$ by firing FDs whose left side is already inside it stays inside $X^+$.

Let $P$ be the set of attributes that line L6 has removed from the queue so far.

**Invariant.** At each test of line L5:

- (a) $\mathit{closure} \subseteq X^+$.
- (b) $P \cap \mathit{queue} = \emptyset$ and $P \cup \mathit{queue} = \mathit{closure}$, and each attribute occurs in the queue at most once.
- (c) $\mathit{count}[i] = |W_i - P|$ for each $i$.
- (d) If $\mathit{count}[i] = 0$, then $Z_i \subseteq \mathit{closure}$.

**Initialization.** After lines L1 to L3, $P = \emptyset$, $\mathit{closure} = X = \mathit{queue}$ as a set, and $\mathit{count}[i] = |W_i| = |W_i - \emptyset|$. Line L4 calls ADD$(Z_i)$ for each $i$ with $W_i = \emptyset$. ADD appends a new attribute $B$ to both the closure and the queue, so (b) still holds, and it never appends an attribute that is already in the closure. Each fired FD has $W_i = \emptyset \subseteq X^+$, so $Z_i \subseteq X^+$ and (a) holds. The counters with value 0 are those with $W_i = \emptyset$, and line L4 added their $Z_i$, so (d) holds. Part (c) holds because no counter changed.

**Maintenance.** Assume the invariant before an iteration, and let line L6 remove $A$. By (b), $A \notin P$, and $A \in \mathit{closure}$. After the iteration, $P' = P \cup \{A\}$.

- For (c): line L8 lowers $\mathit{count}[i]$ by one for each $i$ in $\mathit{list}[A]$, that is, for each $i$ with $A \in W_i$. For those $i$, $|W_i - P'| = |W_i - P| - 1$, since $A \in W_i - P$. For other $i$, $|W_i - P'| = |W_i - P|$. Each $i$ occurs once in $\mathit{list}[A]$. So (c) holds for $P'$.
- For (a): line L9 calls ADD$(Z_i)$ only when $\mathit{count}[i] = 0$, which by (c) means $W_i \subseteq P' \subseteq \mathit{closure} \subseteq X^+$. Then $Z_i \subseteq X^+$, so the closure stays inside $X^+$.
- For (b): $A$ moved from the queue to $P'$. ADD appends to the queue only attributes new to the closure, so the queue holds each attribute at most once, and $P' \cup \mathit{queue} = \mathit{closure}$ still holds.
- For (d): a counter that was 0 before stays 0, and its $Z_i$ is still in the closure, since the closure only grows. A counter that becomes 0 in this iteration becomes 0 in line L8, and line L9 then calls ADD$(Z_i)$. So each zero counter has its right side in the closure.

**Termination.** Each iteration removes one attribute from the queue and adds it to $P$. By (b), no attribute enters the queue twice, because an attribute enters the queue only when it enters the closure, and it never leaves the closure. So the loop runs at most $|U|$ times.

**Conclusion.** When the loop stops, the queue is empty, so $P = \mathit{closure}$ by (b). Let $W_i \subseteq \mathit{closure}$. Then $W_i - P = \emptyset$, so $\mathit{count}[i] = 0$ by (c), and $Z_i \subseteq \mathit{closure}$ by (d). Also $X \subseteq \mathit{closure}$, because line L3 put $X$ in and nothing removes attributes. So the returned set holds $X$ and is closed under $F$, and therefore it contains the least such set: $X^+ \subseteq \mathit{closure}$. With (a), $\mathit{closure} = X^+$. $\square$

**Cost.** The termination argument gives at most $|U|$ iterations of line L5. Over the whole run, line L8 runs once for each pair $(A, i)$ with $A \in W_i$ and $A$ removed from the queue, so at most $\sum_i |W_i|$ times. A counter reaches 0 at most once, because it only decreases, so each FD fires at most once and ADD reads each $Z_i$ at most once. With the setup in lines L1 and L2, the total time is $O(|U| + \sum_i (|W_i| + |Z_i|))$.
