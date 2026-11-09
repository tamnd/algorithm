---
tag: B66K94
kind: technique
slug: restarts
name: Restarts in SAT solving
aliases:
- Luby restarts
- restart policy
- glucose restarts
area: logic-and-constraints/sat-solving
level: advanced
summary: "A CDCL solver at times undoes all decisions and starts the search again, but keeps its learned clauses, scores and saved phases. A restart policy says when."
prereqs: [cdcl, las-vegas-algorithm]
see_also: [phase-saving, literal-block-distance, vsids, clause-database-reduction, geometric-distribution, random-restart-hill-climbing, moving-average, stochastic-local-search]
sources:
  - paper: doi:10.1016/0020-0190(93)90029-9
    title: Michael Luby, Alistair Sinclair and David Zuckerman, Optimal speedup of Las Vegas algorithms, Information Processing Letters 47(4), 1993
    locator: pages 173 to 180 (the optimal strategy for a known distribution is a fixed cutoff, the universal sequence, its upper bound of order ell log ell, and the matching lower bound)
  - paper: "Jinbo Huang, The effect of restarts on the efficiency of clause learning, Proceedings of the 20th International Joint Conference on Artificial Intelligence (IJCAI 2007), 2007"
    locator: pages 2318 to 2323 (seven restart policies compared on 251 instances from 22 benchmark families)
  - paper: doi:10.1007/978-3-642-33558-7_11
    title: Gilles Audemard and Laurent Simon, Refining restarts strategies for SAT and UNSAT, Principles and Practice of Constraint Programming (CP 2012), Lecture Notes in Computer Science 7514, 2012
    locator: pages 118 to 126 (the dynamic restart rule on recent and global LBD averages, and the blocking of restarts by the trail size)
  - paper: "Carla P. Gomes, Bart Selman and Henry Kautz, Boosting combinatorial search through randomization, Proceedings of the Fifteenth National Conference on Artificial Intelligence (AAAI 1998), 1998"
    locator: heavy-tailed run time distributions of randomized backtracking search, and rapid randomized restarts
  - paper: doi:10.1007/978-3-540-24605-3_37
    title: Niklas Eén and Niklas Sörensson, An extensible SAT-solver, SAT 2003, Lecture Notes in Computer Science 2919, 2004
    locator: pages 502 to 518 (the MiniSat search loop with restarts after a growing number of conflicts)
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 4, Conflict-Driven Clause Learning SAT Solvers, by Marques-Silva, Lynce and Malik (search restarts)
---

A restart in a [CDCL](/cdcl/) solver undoes every decision and every assignment above level 0 and starts the search again from the empty trail, while it keeps the learned clauses, the [VSIDS](/vsids/) scores and the [saved phases](/phase-saving/). The restart policy decides when to restart: after a fixed sequence of conflict counts, such as the Luby sequence, or by a dynamic rule, such as the glucose rule on [literal block distance](/literal-block-distance/). Restarts are a heuristic for CDCL, and their measured effect is mixed; the exact result behind them is the theorem of Luby, Sinclair and Zuckerman, proved below, that one fixed sequence of cutoffs is within a logarithmic factor of the best cutoff for every [Las Vegas algorithm](/las-vegas-algorithm/).

## In plain words

A search that makes a bad early choice can spend a very long time below that choice before it finds out. A restart gives up the current path and begins again from the top. The solver does not forget what it learned: the learned facts, the memory of which variables were busy, and the last value of each variable all stay. So the new search starts from the same problem but with better guesses.

The hard question is when to give up. Restart too often and the solver never gets deep enough to finish anything. Restart too rarely and it stays stuck. One answer is a fixed schedule that mixes many short tries with some long ones. Another answer is to watch how good the recent conflicts are and restart when they get worse than usual.

## When it applies

- The search is complete and keeps what it learned, so a restart loses only the current partial assignment. In CDCL, the learned clauses carry the knowledge, and [phase saving](/phase-saving/) brings much of the old assignment back.
- Run times are very uneven: on many instances, randomized backtracking search has a heavy-tailed run time distribution, with most runs short and a few extremely long, as Gomes, Selman and Kautz observed. A cutoff stops the long runs.
- For the exact theorem, the algorithm must be a Las Vegas algorithm whose runs are independent: each run starts from scratch with fresh random bits. CDCL restarts are not independent, because the runs share learned clauses and scores, so for CDCL the theorem is a guide and not a guarantee.

## The template

```pseudo id=main
CDCL-WITH-RESTARTS(F)
L1  loop
L2      confl ← PROPAGATE()
L3      if confl ≠ nil
L4          if the current level is 0 then return UNSAT
L5          learn a clause, backjump and assert it, as in CDCL
L6          UPDATE(confl)                  ▷ hole STATS: conflict count, LBD averages, trail size
L7      else if SHOULD-RESTART()           ▷ hole POLICY: when to restart
L8          BACKTRACK(0)                   ▷ hole KEEP: what survives the restart
L9      else if every variable is assigned then return SAT
L10     else DECIDE()
```

The holes:

- **POLICY.** The usual choices, by the number of conflicts since the last restart:
  - *Fixed interval*: restart after every $u$ conflicts.
  - *Geometric*: the $i$th interval is $u \cdot g^{i-1}$. MiniSat 1.14 used $u = 100$ and $g = 1.5$.
  - *Luby*: the $i$th interval is $u \cdot t_i$, where $t_1, t_2, \ldots$ is the Luby sequence $1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, \ldots$, defined by $t_i = 2^{k-1}$ if $i = 2^k - 1$, and $t_i = t_{i - 2^{k-1} + 1}$ if $2^{k-1} \le i < 2^k - 1$. MiniSat 2.2 uses $u = 100$.
  - *Glucose*: let $\bar{g}_{50}$ be the mean LBD of the last 50 learned clauses, and $\bar{g}$ the mean LBD of all learned clauses so far. Restart when 50 clauses were learned since the last restart and $0.8 \cdot \bar{g}_{50} > \bar{g}$. The test runs after each conflict. To block a restart, Audemard and Simon also keep the mean trail size over the last 5000 conflicts. When the trail at a conflict is more than 1.4 times that mean, the solver may be close to a model, so it clears the window of 50 and the restart waits.
- **STATS.** A count of conflicts for the fixed sequences; the window of recent LBD values, the running total of all LBD values, and the window of trail sizes for glucose.
- **KEEP.** Learned clauses, activities and saved phases survive. Clauses learned at level 0, and units found by the search, remain assigned at level 0.

**Correctness.** A restart only unassigns literals above level 0, the same as a backjump to level 0, so it keeps every invariant of CDCL. The answer SAT still comes with a model and the answer UNSAT still comes from a conflict at level 0, so soundness does not change. Termination needs more care: if a solver restarts after every single conflict and also deletes learned clauses, it can repeat itself for ever. The [CDCL](/cdcl/) page proves termination when the restart intervals grow without bound, as with the Luby and geometric policies, or when no learned clause is deleted. For the glucose rule together with clause deletion, no termination proof is known.

The rest of this section proves the theorem behind the Luby policy, in the model of Luby, Sinclair and Zuckerman. A Las Vegas algorithm $A$ on a fixed input has a run time $T \ge 1$, an integer random variable. A *strategy* is a sequence of cutoffs $s_1, s_2, \ldots$: run $A$ for up to $s_1$ steps; if it has not stopped, start a fresh independent run for up to $s_2$ steps; and so on. Write $q(t) = \Pr[T \le t]$ and $\ell(t) = \mathrm{E}[\min(T, t)] / q(t)$ for $q(t) > 0$.

*Lemma 1 (fixed cutoff).* The strategy $t, t, t, \ldots$ has expected total time $\ell(t)$. *Proof.* Each run stops with an answer with probability $q(t)$, independently, so the number of runs is [geometric](/geometric-distribution/) with mean $1/q(t)$. Every run costs $\min(T, t)$ steps, with mean $\mathrm{E}[\min(T,t)]$, and the number of runs is a stopping time for the sequence of runs, so by Wald's identity the expected total is $\mathrm{E}[\min(T,t)]/q(t)$. $\blacksquare$

Luby, Sinclair and Zuckerman prove that when the distribution of $T$ is known, a fixed cutoff that minimizes $\ell(t)$ is an optimal strategy. Write $\ell^* = \inf_t \ell(t)$. The Luby sequence needs no knowledge of the distribution.

*Lemma 2 (counting in the Luby sequence).* Among the first $2^m - 1$ terms, for each $i < m$ there are exactly $2^{m-1-i}$ terms equal to $2^i$, and there are no others. So the first $2^m - 1$ terms sum to $m \cdot 2^{m-1}$, and for $j < m$ exactly $2^{m-j} - 1$ of them are at least $2^j$. *Proof.* By induction on $m$: the first $2^m - 1$ terms are two copies of the first $2^{m-1} - 1$ terms followed by $2^{m-1}$. Summing $2^{m-1-i} \cdot 2^i$ over $i < m$ gives $m 2^{m-1}$, and summing $2^{m-1-i}$ over $j \le i < m$ gives $2^{m-j} - 1$. $\blacksquare$

*Lemma 3 (a cheap cutoff).* For every cutoff $t$ with $q(t) > 0$, there is a cutoff $c \ge 1$ with $c / q(c) \le 2\ell(t)$. *Proof.* Write $L = \ell(t)$ and $M = \mathrm{E}[\min(T,t)] = \sum_{s=0}^{t-1} (1 - q(s))$, so $L = M/q(t) \ge M$. Suppose that $q(c) < c/(2L)$ for every $c$ with $1 \le c \le t$. If $t \le 2L$, then $q(t) < t/(2L)$ gives $M = L q(t) < t/2$, but every term $1 - q(s) > 1 - s/(2L) \ge 0$, so $M \ge t - t(t-1)/(4L) > t/2$, which is a contradiction. If $t > 2L$, let $u = \lceil 2L \rceil \le t$; then $M \ge \sum_{s=0}^{u-1} (1 - s/(2L)) = u - u(u-1)/(4L)$, and for $2L \le u < 2L + 1$ this is at least $L + 1/2 > L \ge M$, again a contradiction. $\blacksquare$

*Theorem (Luby, Sinclair and Zuckerman).* For every distribution of $T$ and every cutoff $t$ with $L = \ell(t)$, the Luby strategy has expected total time less than $32 L (\lg L + 5)$. In particular it is $O(\ell^* \log \ell^*)$.

*Proof.* Take $c$ from Lemma 3, let $p = q(c) \ge c/(2L)$, and let $j = \lceil \lg c \rceil$, so $c \le 2^j < 2c$. Call a run *long* if its cutoff is at least $2^j$. A long run stops with probability at least $q(2^j) \ge p$, independently of the others. Let $N$ be the index of the first long run that stops; then $\Pr[N \ge n] \le (1-p)^{n-1}$, and the strategy stops no later than the end of long run number $N$. By Lemma 2 with $m = r + j$, the first $2^r - 1$ long runs lie within the first $2^{r+j} - 1$ runs, whose total length is $(r+j) 2^{r+j-1}$. So

$$\mathrm{E}[\text{time}] \le \sum_{r \ge 1} \Pr[N \ge 2^{r-1}] \cdot (r+j) 2^{r+j-1}.$$

Let $R$ be the least $r \ge 1$ with $2^{r-1} p \ge 1$; then $2^R \le 4/p$. The terms with $r \le R$ sum to less than $(R+j) 2^{R+j}$. For $r = R + s$ with $s \ge 1$, $\Pr[N \ge 2^{r-1}] \le (1-p)^{2^{r-1}-1} \le e^{p} e^{-p 2^{R-1} 2^s} \le e \cdot e^{-2^s}$, and since $\sum_{s \ge 1} 2^{s-1} e^{-2^s} < 0.18$ and $\sum_{s \ge 1} s 2^{s-1} e^{-2^s} < 0.22$, these terms sum to less than $2^{R+j} (0.49 (R+j) + 0.6)$. The total is less than $2 (R + j + 1) 2^{R+j}$. Finally $2^{R+j} < (4/p)(2c) = 8c/p \le 16L$, so $R + j + 1 < \lg L + 5$, and the time is less than $32 L (\lg L + 5)$. $\blacksquare$

Luby, Sinclair and Zuckerman also prove the matching lower bound: for every strategy that does not know the distribution, there are distributions on which its expected time is at least a constant times $\ell^* \log \ell^*$. So no universal strategy beats the Luby sequence by more than a constant factor. Their own constants differ from the ones above.

**Cost.** A fixed policy costs $O(1)$ per conflict: a counter and the next term of the sequence, which a loop computes in $O(\log i)$ time. The glucose rule keeps a queue of 50 values, a running sum and a window of 5000 trail sizes, so $O(1)$ per conflict. The restart itself costs one backtrack to level 0, linear in the trail length; the loss is the work needed to rebuild the assignment, which phase saving reduces.

**Example.** Take a Las Vegas algorithm with $T = 1$ with probability $0.1$ and $T = 1000$ otherwise. Without restarts the expected time is $900.1$. The best fixed cutoff is $t = 1$, with $\ell^* = 1/0.1 = 10$. The Luby strategy, which does not know the distribution, has expected time about $17.4$. With $T = 10$ with probability $0.05$ and $T = 10^6$ otherwise, no restarts cost about $950000$, the best cutoff $t = 10$ gives $\ell^* = 200$, and Luby gives about $1398$.

| $i$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $t_i$ | 1 | 1 | 2 | 1 | 1 | 2 | 4 | 1 | 1 | 2 | 1 | 1 | 2 | 4 | 8 |

The first 7 terms sum to $3 \cdot 4 = 12$ and the first 15 to $4 \cdot 8 = 32$, as Lemma 2 says. Over 400 random distributions with up to four values between 1 and $10^5$, the Luby strategy never used more than $2.06\,\ell^* (\lg \ell^* + 1)$ steps, so the constant 32 of the proof is far from tight.

## Classic examples

- **Huang's comparison.** Huang ran a CDCL solver with seven restart policies on 251 instances from 22 benchmark families of Velev, with a limit of two hours each. Every policy did better than no restarts. The Luby policy was best overall, though only by a small margin in some cases, and was about 1.2 times faster in total time than the geometric policy of MiniSat. No policy was best on every family.
- **MiniSat 2.2.** It uses Luby restarts with a unit of 100 conflicts, together with phase saving.
- **Glucose.** The first glucose solver used Luby restarts with a unit of 32; Audemard and Simon later replaced them by the dynamic LBD rule with blocking.

## Variations

- **Partial restarts.** On a restart, keep the bottom decision levels whose decision variables have a higher score than the variable that the solver would decide next, since it would make these decisions again anyway.
- **Mode switching.** Some recent solvers switch between a focused mode, with frequent glucose-style restarts, and a stable mode, with rare Luby-style restarts.
- **Exponential moving averages.** Later solvers replace the windows of the glucose rule by [exponential moving averages](/exponential-moving-average/), which cost less memory.
- **Restarts in local search.** [Stochastic local search](/stochastic-local-search/) and [random-restart hill climbing](/random-restart-hill-climbing/) restart from a new random assignment and keep nothing. There, the runs are close to independent, and the Las Vegas model applies more directly.

## Pitfalls

- **Expecting the theorem to hold for CDCL.** The theorem needs independent runs. CDCL runs share learned clauses, scores and phases, so the bound is not proved for CDCL, and the measured gains come from experiments only.
- **Short intervals with deletion.** A policy whose intervals stay bounded, combined with aggressive [clause database reduction](/clause-database-reduction/), loses the termination proof.
- **Restarts without phase saving.** Frequent restarts with a fixed polarity throw away the assignment each time; the glucose policy relies on saved phases to rebuild it.
- **Off-by-one in the Luby sequence.** The recursive definition is 1-based. Using 0-based indices with the same formula gives a different sequence.
- **Counting the wrong unit.** The theorem counts steps of the algorithm. Solvers count conflicts, which have very different costs, so the unit $u$ needs tuning.

## Exercises

1. Prove that the subsequence of Luby terms that are at least $2^j$, each divided by $2^j$, is again the Luby sequence.
2. Give a distribution on which the geometric strategy $u g^{i-1}$, for any fixed $u$ and $g > 1$, has expected time much larger than $\ell^*$.
3. Let $T = 1$ with probability $p$ and $T = K$ otherwise. Find the best fixed cutoff and $\ell^*$ as functions of $p$ and $K$.
4. Write the Luby sequence as a loop without recursion that uses $O(1)$ memory and $O(\log i)$ time for term $i$.

## References
