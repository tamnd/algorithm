---
title: Best-response dynamics returns a pure Nash equilibrium or a true cycle, and never cycles in a potential game
proves: [correctness, termination]
status: full
---

Let $G$ be a finite game with players $1, \ldots, n$, pure strategy sets $S_i = \{0, \ldots, |S_i| - 1\}$ and utilities $u_i$ on $S = S_1 \times \cdots \times S_n$. For a profile $s$ let $U(s)$ be the set computed in line L3, the players $i$ with $s_i \notin BR_i(s_{-i})$. When $U(s)$ is not empty, let $f(s)$ be the profile that lines L7 and L8 produce: the smallest $i \in U(s)$ switches to the smallest element of $BR_i(s_{-i})$. Let $s^0$ be the start profile and $s^{t+1} = f(s^t)$ as long as $U(s^t)$ is not empty.

**Claim 1 (an equilibrium return is correct).** If the algorithm returns $(s, \text{"equilibrium"})$, then $s$ is a pure Nash equilibrium.

*Proof.* The return happens at line L4, so $U(s)$ is empty, that is, $s_i \in BR_i(s_{-i})$ for every player $i$. Then $u_i(s) = \max_{b} u_i(b, s_{-i}) \ge u_i(b, s_{-i})$ for every $i$ and every $b \in S_i$, which is the definition of a pure Nash equilibrium. $\square$

**Claim 2 (the invariant).** At the start of each pass of the loop, `seen` is the set $\{s^0, \ldots, s^{t-1}\}$ and the current profile is $s^t$, where $t$ is the number of earlier passes. Also $s^0, \ldots, s^{t-1}$ are pairwise distinct.

*Proof.* By induction on $t$. Initialization: before the first pass, `seen` is empty (line L1) and the profile is $s^0$. Maintenance: suppose the pass with profile $s^t$ does not return. Then $U(s^t)$ is not empty (line L4) and $s^t \notin \{s^0, \ldots, s^{t-1}\}$ (line L5), so after line L6 `seen` is $\{s^0, \ldots, s^t\}$, a set of $t + 1$ distinct profiles, and lines L7 and L8 set the profile to $f(s^t) = s^{t+1}$. $\square$

**Claim 3 (a cycle return is correct).** If the algorithm returns $(s, \text{"cycle"})$ in the pass with profile $s^t$, then no $s^r$ with $r \ge 0$ is a pure Nash equilibrium, so the dynamics from $s^0$ never stop.

*Proof.* The return is at line L5, so $U(s^t)$ is not empty and, by Claim 2, $s^t = s^j$ for some $j < t$. For $j \le r < t$ the pass with profile $s^r$ did not return at line L4, so $U(s^r)$ is not empty. Since $s^{r+1} = f(s^r)$ depends only on $s^r$, induction on $r$ gives $s^{r + (t - j)} = s^r$ for all $r \ge j$. So the sequence from index $j$ on runs through the profiles $s^j, \ldots, s^{t-1}$ for ever, and each has a player who can gain. For $r < j$ the profile $s^r$ also had $U(s^r)$ not empty, because the pass with $s^r$ did not return. So no profile of the sequence is a pure Nash equilibrium. $\square$

**Claim 4 (termination).** The algorithm returns after at most $|S|$ passes that do not return, so after at most $|S| + 1$ passes.

*Proof.* By Claim 2, after $t$ passes that do not return, `seen` holds $t$ distinct profiles of $S$, so $t \le |S|$. The loop has no other exit than the two returns, so it returns in pass $|S| + 1$ at the latest. $\square$

**Claim 5 (potential games).** Suppose $G$ has a generalized ordinal potential, a function $P : S \to \mathbb{R}$ such that $u_i(b, s_{-i}) > u_i(s)$ implies $P(b, s_{-i}) > P(s)$ for every $i$, $s$ and $b$. Then the algorithm never returns "cycle", so it returns a pure Nash equilibrium. Every exact potential (with $u_i(b, s_{-i}) - u_i(s) = P(b, s_{-i}) - P(s)$), and so Rosenthal's potential of a congestion game written with $u_i = -c_i$, is a generalized ordinal potential.

*Proof.* In a pass that does not return, the mover $i$ of line L7 has $s_i \notin BR_i(s_{-i})$, so its new strategy $b$ of line L8 has $u_i(b, s_{-i}) = \max_{b'} u_i(b', s_{-i}) > u_i(s)$. Hence $P(s^{t+1}) > P(s^t)$ for every $t$ for which $s^{t+1}$ is defined, and $P(s^0) < P(s^1) < \cdots$. So the profiles $s^0, s^1, \ldots$ are pairwise distinct, and line L5 never finds the current profile in `seen`. By Claim 4 the algorithm returns, so it returns at line L4, and Claim 1 applies. For an exact potential, a positive gain $u_i(b, s_{-i}) - u_i(s)$ equals the rise of $P$, so $P$ is also a generalized ordinal potential. $\blacksquare$
