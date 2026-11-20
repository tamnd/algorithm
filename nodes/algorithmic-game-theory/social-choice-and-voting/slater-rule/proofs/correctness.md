---
title: Correctness and properties of the subset program for Slater's rule
proves: [correctness]
status: full
---

Let $A = \{0, \ldots, m - 1\}$, let $P$ be a profile of $n$ rankings, and let $g(x, y)$ be the margins. Write $x \to y$ when $g(x, y) > 0$, and $\mathrm{lose}(v) = \{u : u \to v\}$. For a ranking $r$ of a set $S \subseteq A$, its cost $\kappa(r)$ is the number of pairs $\{x, y\} \subseteq S$ with $x \to y$ and $y$ above $x$ in $r$. Let $\mathrm{opt}(S)$ be the least cost of a ranking of $S$, with $\mathrm{opt}(\emptyset) = 0$.

**Claim 1 (recursion).** For nonempty $S$, $\mathrm{opt}(S) = \min_{v \in S} \left( |\mathrm{lose}(v) \cap (S \setminus \{v\})| + \mathrm{opt}(S \setminus \{v\}) \right)$. More precisely, the least cost of a ranking of $S$ with first element $v$ is the term for $v$.

*Proof.* Let $r$ be a ranking of $S$ with first element $v$, and let $r'$ be the rest of $r$, a ranking of $S \setminus \{v\}$. The pairs that contain $v$ have $v$ on top, so exactly those with $u \to v$, $u \in S \setminus \{v\}$, are reversed. The other pairs are the pairs of $r'$. So $\kappa(r) = |\mathrm{lose}(v) \cap (S \setminus \{v\})| + \kappa(r')$. The least value over $r'$ is the term for $v$, and the least value over $v$ is the right side.

**Claim 2 (correctness).** After lines L2 to L4, $\mathrm{cost}[S] = \mathrm{opt}(S)$ for every $S$. Lines L5 to L8 return the Slater ranking that is first in lexicographic order. A candidate is a Slater winner exactly when it passes the test of line L7 for $S = A$.

*Proof.* The first part follows from Claim 1 by induction on the bit mask of $S$, because the mask of $S \setminus \{v\}$ is smaller than that of $S$. For the second part, consider the loop with the invariant that the list $r$ built so far is a prefix of the lexicographically first ranking of $A$ with cost $\mathrm{opt}(A)$, and that $S$ is the set of the candidates not in $r$. A ranking that begins with $r$ and continues with $v$ can reach cost $\mathrm{opt}(A)$ exactly when $v$ passes the test of line L7, by Claim 1 applied to $S$ and because the pairs between $r$ and $S$ are the same for all such rankings. The lexicographically first optimal ranking continues with the smallest such $v$, and line L7 picks it. The third part is Claim 1 for $S = A$.

**Claim 3 (Smith set on top).** Let $T$ be the Smith set, the smallest nonempty set of candidates each of whom has a positive margin over every candidate outside it. Every Slater ranking puts every member of $T$ above every candidate outside $T$.

*Proof.* Let $r$ be a ranking that puts some $y \notin T$ above some $x \in T$. Let $r'$ list the members of $T$ in their order in $r$, then the others in their order in $r$. Pairs inside $T$ and pairs outside $T$ keep their order. A pair $\{x, y\}$ with $x \in T$ and $y \notin T$ has $x \to y$, so it costs nothing in $r'$, and at least one such pair costs 1 in $r$. So $\kappa(r') < \kappa(r)$, and $r$ is not optimal. A Condorcet winner $c$ has $T = \{c\}$, so it is on top of every Slater ranking.

**Claim 4 (Pareto).** If $n \ge 1$ and every voter ranks $a$ above $b$, then every Slater ranking puts $a$ above $b$.

*Proof.* For every $x \ne a, b$, a voter who ranks $b$ above $x$ also ranks $a$ above $x$, and a voter who ranks $x$ above $a$ also ranks $x$ above $b$. So $b \to x$ implies $a \to x$, and $x \to a$ implies $x \to b$. Let $r$ put $b$ above $a$, and let $r'$ be $r$ with $a$ and $b$ exchanged. For $x$ above both or below both, the two pairs with $x$ cost the same in total in $r$ and $r'$. For $x$ between them, $r$ has $b$ above $x$ above $a$ and pays $[x \to b] + [a \to x]$, and $r'$ pays $[x \to a] + [b \to x]$, which is not more by the two implications. The pair $\{a, b\}$ has $a \to b$, since $g(a, b) = n \ge 1$, and costs 1 in $r$ and 0 in $r'$. So $\kappa(r') < \kappa(r)$.

**Claim 5 (monotonicity).** Let $w$ be a Slater winner of $P$, and let $Q$ be $P$ with $w$ moved up one place on one ballot, passing $x$. Then $w$ is a Slater winner of $Q$.

*Proof.* Only the margin between $w$ and $x$ changes, by 2 in favour of $w$. So the only arc that can change is between $w$ and $x$: the arc $x \to w$ may disappear, and the arc $w \to x$ may appear. For a ranking $r$, the cost changes only on the pair $\{w, x\}$. If $r$ puts $w$ above $x$, the cost goes down by $\Delta = [x \to w \text{ in } P] - [x \to w \text{ in } Q] \ge 0$, and if $r$ puts $x$ above $w$, it does not go down. So every cost goes down by at most $\Delta$, and a Slater ranking $r^*$ of $P$ with $w$ on top goes down by exactly $\Delta$. So $r^*$ is optimal for $Q$, and $w$ is a winner.

**Claim 6 (anonymity and neutrality).** Reordering the voters does not change the result. Renaming the candidates by $\pi$ renames the Slater rankings and the winners by $\pi$.

*Proof.* The cost of a ranking depends only on the arcs, which do not depend on the order of the voters, and renaming the candidates renames the arcs.

**Claim 7 (time).** SLATER runs in $O(n m^2 + 2^m m)$ time and $O(2^m)$ space on a word RAM with words of at least $m$ bits.

*Proof.* The margins take $O(n m^2)$ time, and line L1 takes $O(m^2)$. Line L4 runs for $2^m - 1$ sets and tries at most $m$ candidates, each with one AND, one population count, one lookup and one addition. Lines L5 to L8 run $m$ times with at most $m$ tries each. The table has $2^m$ entries of $O(\log m)$ bits. $\blacksquare$
