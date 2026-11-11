---
title: WOOT integration stops, keeps every character between its neighbours, and orders a shared gap by id
proves: [invariant, correctness, termination]
status: full
---

**Scope.** This file proves termination of INTEGRATE, the neighbour invariant, local intent, and the order of characters typed concurrently into one gap. Convergence in general is the main result of Oster et al. (2006), proved in Isabelle/HOL by Karayel and Gonzàlez (2020); it is not repeated here.

**Setting.** A replica holds a sequence that starts with $c_b$ and ends with $c_e$. A W-character $c$ has an id, $\mathit{prev}(c)$ and $\mathit{next}(c)$. An insert of $c$ runs at a replica only when $\mathit{prev}(c)$ and $\mathit{next}(c)$ are present, and at most once; it calls INTEGRATE$(c, \mathit{prev}(c), \mathit{next}(c))$. Deletes only hide characters. Write $\mathrm{pos}(x)$ for the position of $x$ in the sequence and $t(x)$ for the time at which $x$ was put into the sequence at this replica; $t(c_b) = t(c_e) = 0$.

**Claim 1 (the filter keeps a character).** Let $\mathit{cp}$ be before $\mathit{cn}$, and suppose every character $d$ in the sequence has $\mathrm{pos}(\mathit{prev}(d)) < \mathrm{pos}(d) < \mathrm{pos}(\mathit{next}(d))$ and $t(\mathit{prev}(d)), t(\mathit{next}(d)) < t(d)$. If the set $S'$ of characters strictly between $\mathit{cp}$ and $\mathit{cn}$ is not empty, then some $d \in S'$ has $\mathit{prev}(d)$ at or before $\mathit{cp}$ and $\mathit{next}(d)$ at or after $\mathit{cn}$.

*Proof.* Start with any $d_0 \in S'$. Given $d_k \in S'$: if $\mathit{prev}(d_k)$ is in $S'$, let $d_{k+1} = \mathit{prev}(d_k)$; else if $\mathit{next}(d_k)$ is in $S'$, let $d_{k+1} = \mathit{next}(d_k)$; else stop. Each step lowers $t$, so the chain is finite. At the last $d_k$, neither neighbour is in $S'$. $\mathit{prev}(d_k)$ is before $d_k$, which is after $\mathit{cp}$, and it is not strictly between $\mathit{cp}$ and $\mathit{cn}$, so it is at or before $\mathit{cp}$. In the same way $\mathit{next}(d_k)$ is at or after $\mathit{cn}$. $\square$

**Claim 2 (termination and placement).** Under the hypotheses of Claim 1, INTEGRATE$(c, \mathit{cp}, \mathit{cn})$ stops and puts $c$ strictly between $\mathit{cp}$ and $\mathit{cn}$.

*Proof.* By induction on the number $m$ of characters strictly between $\mathit{cp}$ and $\mathit{cn}$. If $m = 0$, lines L2 and L3 put $c$ right before $\mathit{cn}$, which is right after $\mathit{cp}$. If $m > 0$, the list $L$ built by lines L4 and L5 starts with $\mathit{cp}$, ends with $\mathit{cn}$, and by Claim 1 has at least one character in between, in sequence order. Line L7 stops at an index $i$ with $1 \le i \le |L| - 1$, so $L[i - 1]$ and $L[i]$ are consecutive in $L$, with $L[i - 1]$ before $L[i]$, both in the closed range from $\mathit{cp}$ to $\mathit{cn}$, and at least one of them strictly inside it. So the gap between them holds fewer than $m$ characters, and the induction hypothesis places $c$ inside it, hence strictly between $\mathit{cp}$ and $\mathit{cn}$. $\square$

**Claim 3 (neighbour invariant).** At every replica and every time, every character $d$ in the sequence has $\mathrm{pos}(\mathit{prev}(d)) < \mathrm{pos}(d) < \mathrm{pos}(\mathit{next}(d))$ and $t(\mathit{prev}(d)), t(\mathit{next}(d)) < t(d)$, provided that $\mathit{prev}(c)$ is before $\mathit{next}(c)$ whenever an insert of $c$ runs.

*Proof.* By induction on inserts. The pool rule makes both neighbours present before $c$ is integrated, which gives the condition on $t$. Claim 2 gives the condition on positions for $c$. Inserting one character keeps the relative order of all others. $\square$

The proviso of Claim 3 holds at the source, where $\mathit{prev}(c)$ and $\mathit{next}(c)$ are the visible characters $i - 1$ and $i$. At other replicas it says that two characters are in the same relative order there, which is part of the convergence theorem of Oster et al. and of Karayel and Gonzàlez.

**Claim 4 (local intent).** A local INSERT$(i, x)$ makes $x$ the $i$-th visible character at its source.

*Proof.* At the source $\mathit{cp}$ is the visible character $i - 1$ (or $c_b$) and $\mathit{cn}$ the visible character $i$ (or $c_e$), so only hidden characters lie between them. By Claim 2, $x$ goes strictly between them, so exactly $i - 1$ visible characters are before it. $\square$

**Claim 5 (a shared gap is in id order).** Let $P$ be before $N$, and let $x_1, \ldots, x_m$ have $\mathit{prev} = P$ and $\mathit{next} = N$ and distinct ids. Suppose that no other character is ever put between $P$ and $N$ at any replica. Then at every replica, the characters between $P$ and $N$ are the integrated $x_j$ in increasing id order.

*Proof.* By induction on the number of integrated $x_j$. With none, the gap is empty. Assume that it holds $x_{j_1}, \ldots, x_{j_s}$ in increasing id order and integrate $c = x_j$. Every character in the gap has its neighbours at $P$ and $N$, so line L5 keeps all of them, and $L = (P, x_{j_1}, \ldots, x_{j_s}, N)$. Line L7 stops at the first $L[i]$ with an id above $c$'s, or at $N$. Then $L[i - 1]$ and $L[i]$ are adjacent in the sequence, so the recursive call puts $c$ between them, and the gap is again sorted. The result does not depend on the order of integration. $\square$

**Theorem.** Claims 2 to 5 hold in the stated model: integration stops, every character stays between its neighbours, local inserts keep their intent, and concurrent inserts into one gap converge to id order.

*Proof.* Claims 2 to 5. $\square$

**Termination.** By Claim 2 every call to INTEGRATE stops. The pool loop stops because every round either runs and removes an operation or ends. $\blacksquare$
