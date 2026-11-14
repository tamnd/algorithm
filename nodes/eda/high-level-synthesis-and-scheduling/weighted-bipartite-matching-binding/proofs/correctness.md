---
title: The matching binder uses the fewest registers and is optimal step by step
proves: [correctness]
status: full
---

We use the notation of the page. Each value $x$ is held in the consecutive steps $b(x), \ldots, e(x)$, and two values conflict when these sets meet. Let $L = \max_t |\{x : b(x) \le t \le e(x)\}|$ be the largest number of values live in one step. The steps $t$ of line L2 are processed in increasing order.

**Lemma 1 (each step places every new value).** At line L7, $|F| \ge |A|$, so a matching that covers $A$ exists, and after L8 every value of $A$ has a register.

*Proof.* Line L5 adds $\max(0, |A| - |F|)$ registers to $F$, so afterwards $|F| \ge |A|$. Matching the values of $A$ to distinct registers of $F$ in any order covers $A$, so the largest-weight matching that covers $A$ exists, and L8 gives every $x \in A$ a register. Each value has exactly one first step $b(x)$, so it is placed exactly once. $\square$

**Lemma 2 (validity).** After the loop, no two values of one register share a step.

*Proof.* Values enter a register in increasing order of their first step, and at most one per step, since $M$ is a matching. When $x$ enters $r$ at step $t = b(x)$, line L4 put $r$ in $F$ only if $\mathrm{end}(r) < t$, where $\mathrm{end}(r)$ is the last step of the latest value in $r$. All earlier values of $r$ end at or before the latest one, since each entered only after the previous one had ended. So every earlier value $y$ of $r$ has $e(y) < b(x)$, and $x$ and $y$ share no step. $\square$

**Lemma 3 (busy registers).** After line L8 at step $t$, if L5 added a register at step $t$, then every register holds a value live in step $t$.

*Proof.* If L5 added registers, then after L5 $|F| = |A|$, and since $M$ covers $A$ with distinct registers of $F$, every register of $F$ gets a value $x$ with $b(x) = t$, live in step $t$. A register $r \notin F$ has $\mathrm{end}(r) \ge t$. Its latest value $y$ entered at a step $b(y) < t$, since the steps are processed in increasing order, and $e(y) = \mathrm{end}(r) \ge t$, so $y$ is live in step $t$. $\square$

**Theorem 1 (fewest registers).** The binder uses exactly $L$ registers, and no valid binding uses fewer.

*Proof.* The $L$ values live in one step pairwise conflict, so every valid binding uses at least $L$ registers. For the binder, consider the last step $t$ at which L5 added a register. Registers are never removed, so the final number of registers equals the number after step $t$. By Lemma 3, each of them holds a value live in step $t$, and by Lemma 2 these values are distinct, so there are at most $L$ of them. If L5 never adds a register, there are none and $X$ is empty. $\square$

**Theorem 2 (each step is optimal for its step).** Fix the bindings of the steps before $t$, which fix $\mathrm{Src}(r)$ and $\mathrm{Dst}(r)$ before step $t$. Among all ways to place the values of $A$ in distinct registers of $F$, the matching of L7 adds the fewest connections to the cost.

*Proof.* Placing $x$ in $r$ adds the source $\mathrm{src}(x)$ to $\mathrm{Src}(r)$ if it is not already there, and the ports of $\mathrm{Dst}(x) \setminus \mathrm{Dst}(r)$ to $\mathrm{Dst}(r)$. The number of new connections is
$$\bigl(1 - [\mathrm{src}(x) \in \mathrm{Src}(r)]\bigr) + \bigl(|\mathrm{Dst}(x)| - |\mathrm{Dst}(x) \cap \mathrm{Dst}(r)|\bigr) = 1 + |\mathrm{Dst}(x)| - w(x, r).$$
In a matching, each register of $F$ receives at most one value of $A$, so the new connections of different pairs fall in different registers and add up. A placement $P$ of $A$ adds
$$\sum_{(x, r) \in P} \bigl(1 + |\mathrm{Dst}(x)| - w(x, r)\bigr) = \sum_{x \in A} \bigl(1 + |\mathrm{Dst}(x)|\bigr) - w(P)$$
connections. The first sum does not depend on $P$, so the fewest added connections come from the largest $w(P)$, which is the matching of line L7. $\square$

**What is not claimed.** Theorem 2 fixes the earlier steps. A choice that is best at step $t$ can force a worse choice later, and the page gives an instance with four values where the binder costs 9 while 8 is possible. So the binder is exact for the register count and optimal step by step for the interconnect, and it is a heuristic for the total interconnect. $\blacksquare$
