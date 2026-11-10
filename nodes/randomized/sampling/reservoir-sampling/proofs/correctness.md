---
title: Algorithm R returns a uniform k-subset
proves: [correctness]
status: full
---

**Statement.** Let $k \ge 0$ and let the stream have $n$ items. Assume that each draw of line L5 is an exact uniform integer in $\{1, \ldots, t\}$, independent of all other draws. If $n \ge k$, RESERVOIR-SAMPLE returns the items of a $k$-subset $S \subseteq \{1, \ldots, n\}$ of positions, and each $k$-subset is returned with probability $1/\binom{n}{k}$. If $n < k$, it returns all $n$ items.

**Setup.** Write $\mathrm{Res}_t$ for the set of positions whose items are in $R$ after the loop has processed item $t$. We use the identity
$$\binom{t+1}{k} = \binom{t}{k} \cdot \frac{t+1}{t+1-k} \qquad (t \ge k \ge 0),$$
which follows from $\binom{t+1}{k} = \frac{(t+1)!}{k!\,(t+1-k)!}$ and $\binom{t}{k} = \frac{t!}{k!\,(t-k)!}$ by dividing the two.

**Case $n < k$.** For each $t \le n < k$, line L4 writes item $t$ to the empty slot $t$, and line L5 never runs. So $R$ holds all $n$ items and the algorithm returns them.

**Invariant.** For each $t$ with $k \le t \le n$: $\mathrm{Res}_t$ is a $k$-subset of $\{1, \ldots, t\}$, and $\Pr[\mathrm{Res}_t = S] = 1/\binom{t}{k}$ for each $k$-subset $S$ of $\{1, \ldots, t\}$.

**Initialization ($t = k$).** Line L4 has written items $1, \ldots, k$ to slots $1, \ldots, k$, with no random draw. So $\mathrm{Res}_k = \{1, \ldots, k\}$ with probability $1 = 1/\binom{k}{k}$, and this is the only $k$-subset of $\{1, \ldots, k\}$.

**Maintenance.** Assume the invariant for some $t$ with $k \le t < n$, and consider item $t+1$. If $k = 0$, line L6 never writes, $\mathrm{Res}_{t+1} = \emptyset$, and the claim holds since $\binom{t+1}{0} = 1$. So let $k \ge 1$. Line L5 draws $j$ uniform in $\{1, \ldots, t+1\}$, independent of $\mathrm{Res}_t$. Item $t+1$ enters if and only if $j \le k$, which has probability $k/(t+1)$. Given that it enters, $j$ is uniform over the $k$ slots, so it overwrites each of the $k$ positions of $\mathrm{Res}_t$ with probability $1/k$. In every case $\mathrm{Res}_{t+1}$ has exactly $k$ elements, all at most $t+1$. Fix a $k$-subset $S$ of $\{1, \ldots, t+1\}$.

1. *Case $t+1 \notin S$.* Then $\mathrm{Res}_{t+1} = S$ if and only if $\mathrm{Res}_t = S$ and $j > k$. These two events are independent, so
$$\Pr[\mathrm{Res}_{t+1} = S] = \frac{1}{\binom{t}{k}} \cdot \frac{t+1-k}{t+1} = \frac{1}{\binom{t+1}{k}}$$
by the identity of the setup.
2. *Case $t+1 \in S$.* Let $S' = S \setminus \{t+1\}$, a $(k-1)$-subset of $\{1, \ldots, t\}$. Then $\mathrm{Res}_{t+1} = S$ if and only if, for some position $y \in \{1, \ldots, t\} \setminus S'$, we have $\mathrm{Res}_t = S' \cup \{y\}$ and $j$ is the slot that holds item $y$. There are $t - (k-1)$ choices of $y$, and these events are disjoint. For each $y$, the probability is $\frac{1}{\binom{t}{k}} \cdot \frac{1}{t+1}$, since a fixed slot is drawn with probability $1/(t+1)$. So
$$\Pr[\mathrm{Res}_{t+1} = S] = \frac{t-k+1}{\binom{t}{k}\,(t+1)} = \frac{1}{\binom{t+1}{k}},$$
again by the identity.

So the invariant holds for $t + 1$.

**Termination.** The loop runs once for each item, so it stops after $n$ steps. At the end $t = n$, and the invariant for $t = n$ is the statement. Line L7 returns $R[1 \ldots k]$, which holds the items at the positions $\mathrm{Res}_n$. $\blacksquare$

**Corollary.** Each position $i \in \{1, \ldots, n\}$ is in $\mathrm{Res}_n$ with probability $\binom{n-1}{k-1}/\binom{n}{k} = k/n$, since exactly $\binom{n-1}{k-1}$ of the equally likely $k$-subsets contain $i$.
