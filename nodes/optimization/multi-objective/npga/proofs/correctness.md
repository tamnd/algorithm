---
title: The Pareto domination tournament of NPGA, its exact detection probability, and the invariants of the loop
proves: [correctness]
status: full
---

All objectives are minimized, $N$ is the population size, $t$ is the size of the comparison set, and line numbers refer to the `pseudo id=main` block of the NPGA page. NPGA is a heuristic. The statements below are about one tournament and about the sizes that the loop keeps; none of them says that NPGA reaches the Pareto front.

## One tournament

In line L5 the comparison set $C$ is a uniformly random subset of $t$ members of $P$, drawn without replacement. Let $k(x)$ be the number of members of $P$ whose image dominates $f(x)$.

**Lemma 1.** The probability that some member of $C$ dominates $x$ is

$$\pi(k, t) = 1 - \binom{N - k}{t} \Big/ \binom{N}{t}, \qquad k = k(x).$$

It is $0$ when $k = 0$, it grows with $k$ and with $t$, and it is $1$ when $t > N - k$.

*Proof.* No member of $C$ dominates $x$ exactly when $C$ is a subset of the $N - k$ members that do not dominate $x$. There are $\binom{N-k}{t}$ such subsets out of $\binom{N}{t}$, all equally likely. If $k = 0$ the ratio is $1$. If $t > N - k$ there is no such subset, so the ratio is $0$. For the growth, $\binom{N-k}{t} / \binom{N}{t} = \prod_{j=0}^{t-1} \frac{N - k - j}{N - j}$, and each factor is non-increasing in $k$, while a larger $t$ adds factors that are at most $1$. $\square$

**Lemma 2.** (a) A member that no member of $P$ dominates is never found dominated. (b) If exactly one candidate is found dominated, the other one wins. (c) If $t = N$, a candidate that is dominated in $P$ never wins against a candidate that is not.

*Proof.* (a) $C \subseteq P$. (b) is lines L7 and L8. (c) With $t = N$, $C = P$, so "found dominated" is the same as "dominated in $P$", and (b) applies. $\square$

For $t < N$ a dominated candidate can win against a non-dominated one: when $C$ misses all its dominators, both candidates pass the test of line L6, and the niche counts of line L9 decide. Lemma 1 gives the probability of that event.

## Niche counts

In line L9 the niche count of a candidate $x$ is $m(x) = \sum_{z \in M} \mathrm{sh}(d(f(x), f(z)))$, where $M$ is the part of the mating pool filled so far and $\mathrm{sh}(d) = 1 - d/\sigma$ for $d < \sigma$ and $0$ otherwise. This is the continuously updated sharing of Oei, Goldberg and Chang.

**Lemma 3.** $m(x) \ge 0$, and $m(x) = 0$ when no image in $M$ is closer than $\sigma$ to $f(x)$. Each copy of $f(x)$ already in $M$ adds $1$.

*Proof.* Each term lies in $[0, 1]$, it is $0$ for $d \ge \sigma$, and it is $1$ for $d = 0$. $\square$

So the first winner of each generation is picked at random between the candidates whenever the dominance test is a tie, and each later winner in a tie is the candidate whose image is less represented among the parents chosen so far.

## The loop

**Lemma 4.** Each generation keeps $\lvert P \rvert = N$, and line L11 returns a nonempty set of mutually non-dominated members of the last population.

*Proof.* The loop of lines L4 to L9 adds one member to $M$ per tournament and stops at $\lvert M \rvert = N$. Line L10 makes one offspring per pool member. The output is the set of minimal elements of the last population under dominance, which is nonempty because a nonempty finite set with a strict partial order has a minimal element; two minimal elements do not dominate each other. $\square$
