---
title: Linear scan gives a correct program, and it is optimal for its intervals
proves: [correctness, optimality]
status: full
---

We prove five facts about LINEAR-SCAN-ALLOCATE. Lemma 1 links intervals to liveness. Lemmas 2 to 4 are about the scan on intervals: no two overlapping kept intervals share a register, no spill happens when the overlap is at most $k$, and the number of spills is the smallest possible for the given intervals. Lemma 5 shows that the rewritten program has the same outcome as the input.

## Setup

The program $P$ has `const`, `copy` and `op` instructions only, and it has been prepared: a new entry block copies each live parameter $p$ from its slot `mem.p`. Line L1 numbers the instructions and terminators of $P$ in block order as items $0, 1, \ldots, N-1$. Item $n$ reads at position $2n$ and writes at position $2n+1$. Each instruction is followed in its block by another item, at least by the terminator, so the only successor of an instruction $n$ is item $n+1$. The successors of a terminator are the first items of its successor blocks.

Write $L(n)$ for the set of non-slot names live just before item $n$, as line L2 computes it. The backward fixed point of [live variable analysis](/live-variable-analysis/) gives exactly the names $x$ for which some path of items from $n$ reaches a read of $x$ with no write of $x$ before that read. For an instruction $n$ that writes $y$ and reads $\mathrm{use}(n)$,

$$L(n) = \mathrm{use}(n) \cup (L(n+1) \setminus \{y\}),$$

and for a terminator, $L(n)$ is the name it reads (if any) together with the union of $L(m)$ over its successor items $m$.

Line L3 gives each non-slot name $x$ the interval $I(x) = [s_x, e_x]$, the smallest closed range of integers that contains every write position $2n+1$ of $x$ and every position $2n$ with $x \in L(n)$. Two intervals *overlap* when they share a position. The *overlap* of a set of intervals is the largest number of them that contain one position.

## Intervals contain interference

**Lemma 1.** If $x, y \in L(n)$, then $2n \in I(x) \cap I(y)$. If item $n$ writes $y$ and $x \ne y$ is live just after $n$, then $2n+1 \in I(x) \cap I(y)$.

*Proof.* The first claim is the definition of $I$. For the second, item $n$ is an instruction, so the point just after it is the point just before item $n+1$, and $x \in L(n+1)$. Since $x \ne y$, the equation above gives $x \in L(n)$. So $2n$ and $2n+2$ are both in $I(x)$, and $I(x)$ is a range, so $2n+1 \in I(x)$. The write of $y$ puts $2n+1$ in $I(y)$. $\square$

So the overlap graph of the intervals contains the interference graph. The converse fails: an interval may contain positions where its name is dead, as in the example on the page. That is the only reason why linear scan is a heuristic for the program and not for its intervals.

## The scan on intervals

Let $\sigma$ be the order of line L6: by start, then by end, then by name. Write $X_m$ for the first $m$ intervals of $\sigma$, $G_m$ for the set of intervals of $X_m$ that hold a register after step $m$, and $q$ for the start of the interval $i = \sigma(m+1)$ of the next step. For a set $F$ of intervals and an integer $t$, let $F_{<t}$ be the members of $F$ that end before $t$.

**Invariant (A).** Just after line L7 in the step of $i$, the list *active* is the set of members of $G_m$ that end at or after $q$, the registers of its members are pairwise different, and *free* holds the other registers of $\{0, \ldots, k-1\}$.

*Proof.* By induction on $m$. At $m = 0$ both sides are empty and *free* is full. Suppose (A) holds at the step of $i$. Lines L10 to L12 have just removed the members that end before $q$, and returned their registers. Every member of $G_m$ that ends at or after $q$ ended at or after each earlier start too, so no earlier step removed it, and it is in *active*. Line L9 takes a register from *free*, which no active member holds. Line L14 moves the register of the removed interval $s$ to $i$, and $s$ leaves *active*. Line L15 changes nothing. In each case the registers stay pairwise different, and *active* becomes the set of members of $G_{m+1}$ that end at or after $q$. The next start $q'$ is at least $q$, so after line L7 of the next step, *active* is the set of members of $G_{m+1}$ that end at or after $q'$. $\square$

Every member of *active* starts at or before $q$ and ends at or after $q$. So in the step of $i$, *active* $\cup \{i\}$ is a set of intervals that all contain the position $q$.

**Lemma 2 (registers).** Two kept intervals that overlap get different registers. Each $G_m$ has overlap at most $k$.

*Proof.* Let $a$ and $b$ be kept at the end with $a$ before $b$ in $\sigma$. If they overlap, then $s_a \le s_b \le e_a$. A kept interval never loses its register, so $a$ is in $G_m$ for every step $m$ after its own, and in the step of $b$, it ends at or after $s_b$. By (A), $a$ is in *active* there. Interval $b$ gets its register at line L9 from *free*, or at line L14 from the removed interval $s \ne a$. In both cases (A) says the register differs from that of $a$, and $a$ keeps its register to the end.

For the overlap, take a position $p$ and let $i$ be the last interval of $\sigma$ that contains $p$ and is in $G_m$. Every member of $G_m$ that contains $p$ starts at or before $s_i \le p$ and ends at or after $p$, so it contains $s_i$ and was in *active* or was $i$ at the end of the step of $i$. That set has at most $k$ members, since line L9 only adds an interval when fewer than $k$ are active, and line L14 swaps one for one. $\square$

**Lemma 3 (no spill and the number of registers).** Let $\omega$ be the overlap of all intervals. The scan spills nothing if and only if $\omega \le k$, and then it uses exactly $\omega$ registers.

*Proof.* A spill happens at line L8 only when $|\textit{active}| = k$, and then *active* $\cup \{i\}$ is $k+1$ intervals that contain $s_i$, so $\omega > k$. Conversely, if nothing is spilled, every interval is kept, and Lemma 2 gives $\omega \le k$.

Now let nothing be spilled. When interval $i$ arrives with $a$ active intervals, those $a$ intervals and $i$ contain $s_i$, so $a + 1 \le \omega$. The $a$ active intervals hold $a$ registers, so the lowest free register is at most $a \le \omega - 1$. So only the registers $0, \ldots, \omega - 1$ are used. Some position lies in $\omega$ intervals, and by Lemma 2 they hold $\omega$ different registers. $\square$

**Lemma 4 (fewest spills).** Let $F \subseteq X_m$ be any set with overlap at most $k$. Then for every integer $t$, including $t = \infty$, $|F_{<t}| \le |(G_m)_{<t}|$. In particular $|F| \le |G_m|$, so for $m = n$ the scan spills as few intervals as possible.

*Proof.* By induction on $m$. For $m = 0$ both sides are $0$. Assume the claim for $m$ and take $F \subseteq X_{m+1}$ with overlap at most $k$. Let $A$ be *active* after line L7 in the step of $i = \sigma(m+1)$, so $|A| \le k$. Write $[\phi] = 1$ when the statement $\phi$ is true and $0$ otherwise.

*Case 1: $i \notin F$.* Then $F \subseteq X_m$ and $|F_{<t}| \le |(G_m)_{<t}|$. Line L9 adds $i$, line L15 adds nothing, and line L14 replaces $s$ by $i$ with $e_i \le e_s$, so $[e_i < t] \ge [e_s < t]$. In all three cases $|(G_{m+1})_{<t}| \ge |(G_m)_{<t}|$.

*Case 2: $i \in F$ and $|A| < k$.* Line L9 runs, so $G_{m+1} = G_m \cup \{i\}$. With $F' = F \setminus \{i\} \subseteq X_m$,

$$|F_{<t}| = |F'_{<t}| + [e_i < t] \le |(G_m)_{<t}| + [e_i < t] = |(G_{m+1})_{<t}|.$$

*Case 3: $i \in F$ and $|A| = k$.* Lines L13 to L15 drop the interval $r$ of $A \cup \{i\}$ with the largest end: $r = s$ at line L14, or $r = i$ at line L15. So $G_{m+1} = (G_m \cup \{i\}) \setminus \{r\}$, and we must show

$$|F'_{<t}| + [e_r < t] \le |(G_m)_{<t}|. \qquad (*)$$

If $e_r \ge t$, this is the claim for $m$ applied to $F'$. Let $e_r < t$. Every member of $A$ and $i$ end before $t$, and every member of $G_m$ outside $A$ ends before $q \le e_i < t$. So $|(G_m)_{<t}| = |G_m|$, and we must show $|F'| \le |G_m| - 1$. Every member of $F'$ starts at or before $q$, so those that end at or after $q$ contain $q$. Together with $i$, which contains $q$, there are at most $k$ of them, so $|F'| - |F'_{<q}| \le k - 1$. By the claim for $m$ with $t = q$, $|F'_{<q}| \le |(G_m)_{<q}| = |G_m| - k$, because exactly the $k$ members of $A$ end at or after $q$. Adding the two bounds gives $|F'| \le |G_m| - 1$. $\square$

The proof uses only that the dropped interval has the largest end in $A \cup \{i\}$, so the way ties are broken does not matter. The kept set $G_n$ is a largest subfamily with overlap at most $k$, which is the unit weight case of the [maximum $k$-colorable interval subgraph](/k-colorable-interval-subgraph/).

## The rewritten program has the same outcome

**Lemma 5.** Assume that no run of $P$ reads a name before it writes it. Let $P'$ be the result of line L16: each kept name $x$ becomes the register $r_{\mathrm{reg}(x)}$, each spilled name $x$ becomes the slot `mem.x`, an operand in a slot is first loaded into the scratch register $s_0$ or $s_1$, a result that goes to a slot is computed into $s_0$ and then stored, and a copy whose two sides become the same location is deleted. Then for every input, $P$ and $P'$ have the same outcome.

*Proof.* Run $P$ and $P'$ on the same input, with stores $\sigma$ and $\sigma'$. Let $\mathrm{loc}(x)$ be the location of $x$ in $P'$. We show that the runs visit the same blocks and that this holds just before each item $n$ of $P$ and the code of $P'$ for it:

> **(R)** Each name $x \in L(n)$ that has been written has $\sigma'(\mathrm{loc}(x)) = \sigma(x)$, and each slot `mem.p` of a parameter that the first block has not yet read holds the argument.

At the start, (R) holds, because both programs get the same arguments in the same slots and no non-slot name has been written.

Take an instruction $n$ that writes $y$. Its operands are in $L(n)$ and have been written, so by (R) their locations hold the right values, and loading them into $s_0$ or $s_1$ changes no location of a name. So $P'$ computes the same value $w$ as $P$, or traps in the same way. Then $P'$ writes $w$ to $\mathrm{loc}(y)$, directly or through $s_0$. A deleted copy `y = a` has $\mathrm{loc}(y) = \mathrm{loc}(a)$, which already holds $\sigma(a) = w$. So the claim holds for $y$ after the step.

Let $x \ne y$ be a name in $L(n+1)$ that has been written. It is in $L(n)$, so its location was right before the step. The step writes only $\mathrm{loc}(y)$ and the scratch registers. No name lives in a scratch register. If $x$ is spilled, its slot `mem.x` differs from $\mathrm{loc}(y)$. If $x$ and $y$ are both kept, Lemma 1 says that $I(x)$ and $I(y)$ overlap, and Lemma 2 gives them different registers. So $\mathrm{loc}(x)$ still holds $\sigma(x)$. The parameter slots are read only in the first block, which has no predecessor and runs once, and the slot of a parameter $p$ is written only when $p$ is spilled and $p$ itself is defined. So (R) holds before item $n+1$.

A terminator reads a name in $L(n)$, so both programs take the same branch or return the same value. Each name live at the start of the next block is in $L(n)$, and the terminator writes nothing, so (R) holds there. By induction over the run, both programs end in the same way: with the same value, with the same trap, or not at all. $\square$

## Summary

The scan is optimal for the interval graph that it builds: it uses the fewest registers when no spill is needed (Lemma 3) and spills the fewest intervals otherwise (Lemma 4). The result is always correct (Lemma 5). The interval graph contains the interference graph (Lemma 1), and it may be larger, so the scan may spill a program that a graph coloring allocator colors with $k$ registers.
