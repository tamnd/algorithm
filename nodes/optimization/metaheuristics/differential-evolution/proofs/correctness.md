---
title: Differential evolution stays in the box, keeps the best point of each slot, is invariant under monotone changes of f and, with CR = 1, under linear maps
proves: [correctness]
status: full
---

We use the pseudocode of the page. Write $x_i^{(t)}$ for member $i$ after generation $t$, with $x_i^{(0)}$ the start population, and $t_i^{(t)}$ for the trial made for target $i$ in generation $t$.

**Claim 1 (bounds).** If every $x_i^{(0)}$ is in the box $[\ell, u]$, then every repaired mutant, every trial and every $x_i^{(t)}$ is in the box.

*Proof.* By induction on $t$. Assume that the population of generation $t - 1$ is in the box. Take a coordinate $j$ of a mutant $v$ after line L6. If $v_j$ was in $[\ell_j, u_j]$, it is unchanged. If $v_j < \ell_j$, line L6 sets $v_j = (\ell_j + x_{r_1, j})/2$, and since $\ell_j \le x_{r_1, j} \le u_j$, the midpoint is in $[\ell_j, u_j]$. The case $v_j > u_j$ is the same. The trial takes each coordinate from $v$ or from $x_i$, both in the box, so it is in the box. Each new member is a trial or an old member, so the new population is in the box. $\square$

**Claim 2 (elitism per member).** For every $i$ and $t$, $f(x_i^{(t)}) \le f(x_i^{(t-1)})$. The minimum $m_t = \min_i f(x_i^{(t)})$ does not increase, and $m_t$ is the smallest value of $f$ among the start population and all trials of generations $1, \dots, t$.

*Proof.* Line L8 sets $x_i^{(t)}$ to the trial only if $f(t_i^{(t)}) \le f(x_i^{(t-1)})$, and otherwise keeps $x_i^{(t-1)}$, which gives the first statement, and so $m_t \le m_{t-1}$. For the last statement, use induction on $t$, with $t = 0$ clear. A trial of generation $t$ that is accepted is a member of the new population, so its value is at least $m_t$. A trial that is rejected has $f(t_i^{(t)}) > f(x_i^{(t-1)}) = f(x_i^{(t)}) \ge m_t$. So every value seen in generation $t$ is at least $m_t$. By the induction hypothesis, every value seen before generation $t$ is at least $m_{t-1} \ge m_t$. Since $m_t$ is itself the value of a member, which is a point seen, it is the minimum of all values seen. $\square$

**Claim 3 (increasing transformations).** Let $g$ be strictly increasing. With the same random numbers, the runs on $f$ and on $g \circ f$ give the same populations.

*Proof.* By induction on $t$. If the populations are the same before generation $t$, lines L4 to L7 use only the population and the random numbers, so they give the same trials. Line L8 compares $g(f(t)) \le g(f(x_i))$, which holds if and only if $f(t) \le f(x_i)$. So the same trials are accepted. The returned member is chosen by comparisons, so it is the same too. $\square$

**Claim 4 (maps of the space).** Let $\phi(x) = A x + b$ with $A$ invertible, and $f_\phi = f \circ \phi^{-1}$. With the same random numbers:

1. without bounds and with $CR = 1$, the run on $f_\phi$ from the population $\phi(x_i^{(0)})$ has the populations $\phi(x_i^{(t)})$;
2. with any $CR$, if $A$ is diagonal with positive entries and the box is replaced by $\phi([\ell, u]) = [\phi(\ell), \phi(u)]$, the same holds with bounds.

*Proof.* By induction on $t$. Assume that the population of the second run is $\phi(x_i)$, where $x_i$ is the population of the first. Lines L4 and L7 draw the same indices and random numbers in both runs, because they do not depend on the points. The mutant of the second run is
$$\phi(x_{r_1}) + F\bigl(\phi(x_{r_2}) - \phi(x_{r_3})\bigr) = A x_{r_1} + b + F A (x_{r_2} - x_{r_3}) = \phi(v),$$
since $b$ cancels in the difference. In part 1, with $CR = 1$ the trial is the mutant, so the second trial is $\phi(t)$. In part 2, $\phi$ acts on each coordinate by $y_j = a_j x_j + b_j$ with $a_j > 0$. This map keeps the order, so $\phi(v)_j < \phi(\ell)_j$ if and only if $v_j < \ell_j$, and it keeps midpoints, so the repair of line L6 gives $\phi$ of the repaired mutant. The crossover picks coordinate $j$ from the mutant or from the target, and both are mapped coordinate by coordinate, so the second trial is $\phi(t)$. In both parts, $f_\phi(\phi(t)) = f(t)$ and $f_\phi(\phi(x_i)) = f(x_i)$, so line L8 makes the same choice, and the new population of the second run is $\phi$ of the new population of the first. $\square$

For a rotation $A$ and $CR < 1$, the second step fails: the crossover of $\phi(v)$ and $\phi(x_i)$ coordinate by coordinate is in general not $\phi$ of the crossover of $v$ and $x_i$, because a rotation mixes the coordinates.

**Claim 5 (stagnation).** Fix a population $x_1, \dots, x_p$. For each target $i$, the set $T_i$ of trials that lines L4 to L7 can make is finite. If $f(t) > f(x_i)$ for every $t \in T_i$ and every $i$, then the population never changes again.

*Proof.* There are at most $(p - 1)(p - 2)(p - 3)$ choices of $(r_1, r_2, r_3)$, each gives one mutant, the repair is a function of the mutant and $x_{r_1}$, and the trial is determined by the set of coordinates taken from the mutant, which has at most $2^n$ choices. So $|T_i| \le (p - 1)(p - 2)(p - 3) 2^n$. Under the assumption, line L8 rejects every trial, so the population after the generation is the same, and the assumption holds again for the next generation. By induction, the population stays the same forever. $\square$

Claim 5 does not need the population to be near a minimum: the condition is only about the finitely many trials, which is why there is no general guarantee that DE converges to a minimum.
