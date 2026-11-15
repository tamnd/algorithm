---
title: Balanced interleaving builds a list with balanced prefixes and computes the credit of equations (1) to (3)
proves: [correctness]
status: full
---

Let $A = (A[1], \ldots, A[p])$ and $B = (B[1], \ldots, B[q])$ be rankings, each with no repeated document. Write $\mathrm{top}_j(A) = \{A[1], \ldots, A[j]\}$ for $0 \le j \le p$, and the same for $B$. Lines refer to the pseudocode on the page.

**Invariant.** Before each test of line L2, with $s = ka - 1$ and $t = kb - 1$:

> **(J1)** $I$ has no repeated document, and the set of documents of $I$ is $\mathrm{top}_s(A) \cup \mathrm{top}_t(B)$.
>
> **(J2)** $s - t \in \{0, 1\}$ if $a\_first$ is true, and $s - t \in \{0, -1\}$ if it is false.

*Initialization.* Line L1 sets $I$ empty and $s = t = 0$. Both tops are empty, so (J1) holds, and $s - t = 0$, so (J2) holds.

*Maintenance.* Assume (J1) and (J2) and that the loop body runs, so $ka \le p$ and $kb \le q$. Suppose $a\_first$ is true; the other case is symmetric. By (J2), either $s = t$ or $s = t + 1$.

- If $s = t$, then $ka = kb$ and $a\_first$ is true, so line L3 takes the first branch. Line L4 appends $A[ka]$ if it is not in $I$, and line L5 sets $s$ to $s + 1$. The new set of $I$ is the old set together with $A[ka]$, which is $\mathrm{top}_{s+1}(A) \cup \mathrm{top}_t(B)$. No document is appended twice, because of the test in line L4. The new difference is 1.
- If $s = t + 1$, then $ka > kb$, so line L3 takes the second branch. In the same way, lines L7 and L8 add $B[kb]$ and set $t$ to $t + 1$. The new difference is 0.

So (J1) and (J2) hold again.

*Termination.* Each step increases $s + t$ by 1, and the body runs only while $s < p$ and $t < q$. So the loop stops after at most $p + q - 1$ steps.

**Claim 1 (balanced prefixes).** For every $m$ with $0 \le m \le |I|$, there are $s', t'$ with $|s' - t'| \le 1$ and $\{I[1], \ldots, I[m]\} = \mathrm{top}_{s'}(A) \cup \mathrm{top}_{t'}(B)$.

*Proof.* The list $I$ only grows, by one document at a time, and only in lines L4 and L7. So each prefix of the final $I$ is the value of $I$ at some test of line L2: the prefix of length 0 at the start, and the prefix of length $m \ge 1$ at the test just after the step that appended $I[m]$. At that test (J1) and (J2) hold, with $|s - t| \le 1$. $\square$

**Claim 2 (credit).** If $C$ is a nonempty set of documents of $I$, CREDIT returns the sign of $h_a - h_b$, where $c$ is the clicked document lowest in $I$, $k = \min\{j : A[j] = c \text{ or } B[j] = c\}$, $h_a = |C \cap \mathrm{top}_k(A)|$ and $h_b = |C \cap \mathrm{top}_k(B)|$.

*Proof.* By (J1) at the end of the loop, $c$ is in $\mathrm{top}_s(A)$ or in $\mathrm{top}_t(B)$, so at least one of its ranks is finite. The smallest $j$ with $A[j] = c$ or $B[j] = c$ is the smaller of the rank of $c$ in $A$ and its rank in $B$, which is the value of line L12. Lines L13 and L14 count the two sets and return the sign. $\square$

**Claim 3 (the method is not fair under random clicks).** There are rankings for which a user who clicks one shown document chosen uniformly at random, independently of the documents, makes CREDIT prefer B with probability more than 1/2.

*Proof.* Take $A = (a, b, c, d)$ and $B = (b, c, d, a)$. By the invariant and a direct run of the loop, the coin gives $I = (a, b, c, d)$ or $I = (b, a, c, d)$. In both lists, a click on a gives $k = 1$, $h_a = 1$, $h_b = 0$. A click on b gives $k = 1$ and $h_b = 1 > h_a = 0$. A click on c gives $k = 2$, since c is $B[2]$, and $c \notin \mathrm{top}_2(A)$, so B wins. A click on d gives $k = 3$, since d is $B[3]$, and $d \notin \mathrm{top}_3(A)$, so B wins. So for each value of the coin, B wins with probability $3/4$, and A with probability $1/4$. $\square$

**Cost.** Each step of the loop runs once per increase of $s + t$, so there are at most $p + q$ steps. With the documents of $I$ also kept in a hash set, each step costs $O(1)$ expected time, and CREDIT reads each list once. Together this is $O(p + q)$ time and $O(p + q)$ extra space. $\blacksquare$
