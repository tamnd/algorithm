---
title: Validity of the MUSTANG codes
proves: [correctness]
status: full
---

We use the notation of the page. The machine has $n \ge 1$ states, and $k \ge 1$ is the code length, with $2^k \ge n$; the default $k = \lceil \log_2 n \rceil$ (at least 1) has this property. The weights $w(s, t)$ of lines L2 and L3 are finite numbers, and nothing below depends on their values.

## Theorem (valid codes)

The loop of lines L5 to L7 stops after exactly $n$ rounds, and line L8 returns an injective map from the states to $\{0, 1\}^k$.

*Proof.* We show by induction on the number $r$ of rounds done that the placed states are exactly $r$ distinct states, each with its own code, and that no two placed states share a code.

At the start, $r = 0$ and nothing is placed. Suppose the claim holds after $r < n$ rounds. Then some state is unplaced, so line L6 has a candidate and picks an unplaced state $s$. The placed states use $r$ distinct corners, and $r < n \le 2^k$, so at least one corner is free, and line L7 picks a free corner $c$. After the round, $s$ is placed with code $c$, $s$ was not placed before, and no placed state has code $c$. So the claim holds after $r + 1$ rounds.

Each round places one new state, so after $n$ rounds every state is placed and the loop stops. By the claim, the $n$ codes are distinct, so the map is injective. $\square$

The choices of lines L6 and L7 are well defined, since the tie rules (the total weight, then the order of the states; the smallest corner) give a single answer. So the result is a function of the machine and the mode.

## What is not proved

Nothing here says that the codes minimize the embedding cost $\sum w(s, t)\, d_H(\mathrm{enc}(s), \mathrm{enc}(t))$. The greedy places each state once and never moves it, and the tests find weight graphs on which it misses the least cost. Nothing here says that a small embedding cost gives small logic: on the example of the page, the fanout code has the least embedding cost and the worst minimum two-level cover of all two-bit codes, found by exhaustive search. Every statement on the page about the quality of the codes is a measurement on small random machines, and it uses the two-level cube count as a proxy for the multilevel cost that MUSTANG aims at.
