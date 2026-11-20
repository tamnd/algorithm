---
title: The search over unilateral deviations finds an exact potential exactly when one exists
proves: [correctness]
status: full
---

Let a finite cost game have players $1, \ldots, n$, strategy sets $S_1, \ldots, S_n$ and costs $c_i : S \to \mathbb{Q}$, where $S = S_1 \times \cdots \times S_n$. Call two profiles neighbours if they differ in the strategy of exactly one player $i$; for neighbours $s$ and $t$ that differ in player $i$, write $\delta(s, t) = c_i(t) - c_i(s)$. Then $\delta(t, s) = -\delta(s, t)$. A function $\Phi$ on $S$ is an exact potential if and only if $\Phi(t) - \Phi(s) = \delta(s, t)$ for all neighbours $s, t$.

**Every profile gets a value.** From the start profile $s^0$, any profile $s$ is reached by changing the coordinates one at a time, so the neighbour graph is connected. Line L4 gives a value to each new neighbour of a profile taken from the queue and puts it in the queue, so, unless line L5 stops the search, every profile of the connected graph gets a value and is taken from the queue once.

**If the code returns $\Phi$, it is an exact potential.** Let $s$ and $t$ be neighbours. Both are taken from the queue at some time. When $s$ is taken, line L3 looks at $t$. Either $t$ has no value yet and line L4 sets $\Phi(t) = \Phi(s) + \delta(s, t)$, or it has one and line L5 checks the same equation. So $\Phi(t) - \Phi(s) = \delta(s, t)$ holds for every pair of neighbours.

**If the code returns None, no exact potential exists.** Suppose $\Psi$ is an exact potential. By induction on the order in which line L4 sets values, $\Phi(s) = \Psi(s) - \Psi(s^0)$ for every profile with a value: it holds at $s^0$, and line L4 sets $\Phi(t) = \Phi(s) + \delta(s, t) = \Psi(s) - \Psi(s^0) + \Psi(t) - \Psi(s)$. So every check of line L5 compares $\Psi(t) - \Psi(s^0)$ with $\Psi(s) - \Psi(s^0) + \delta(s, t)$, which are equal, and line L5 never returns None.

**Uniqueness.** The same induction shows that any two exact potentials differ by a constant, because both are fixed by their value at $s^0$ along the search tree.

**Cost.** Each profile is taken from the queue once and has $\sum_i (|S_i| - 1)$ neighbours, so the search does $O(|S| \sum_i |S_i|)$ steps. $\blacksquare$
