---
tag: 2V2501
kind: technique
slug: parallel-portfolio-sat
name: Parallel portfolio solving
aliases:
- portfolio solving
- parallel portfolio SAT
- algorithm portfolio
area: logic-and-constraints/sat-solving
level: advanced
summary: Run several differently configured CDCL solvers on the same formula in parallel, share short learned clauses, and return the first answer.
prereqs: [cdcl, restarts, clause-learning]
see_also: [cube-and-conquer, vsids, phase-saving, literal-block-distance, clause-database-reduction, work-stealing]
sources:
  - paper: doi:10.1016/S0004-3702(00)00081-3
    title: Carla P. Gomes and Bart Selman, Algorithm portfolios, Artificial Intelligence 126(1-2), 2001, 43-62
    locator: portfolios of randomized algorithms with heavy-tailed run times, their expected run time and variance, and the efficient set of portfolios
  - paper: "Youssef Hamadi, Saïd Jabbour and Lakhdar Sais, ManySAT: a parallel SAT solver, Journal on Satisfiability, Boolean Modeling and Computation 6, 2009, 245-262"
    title: "ManySAT: a parallel SAT solver"
    locator: Section 3 (the four cores, Table 1), Section 3.5 (clause sharing up to size 8), Section 4 (SAT-Race 2008 results, Tables 2 and 3)
  - paper: "Youssef Hamadi, Saïd Jabbour and Lakhdar Sais, Control-based clause sharing in parallel SAT solving, IJCAI 2009"
    title: Control-based clause sharing in parallel SAT solving
    locator: a control loop that changes the size limit of shared clauses during the run
  - paper: doi:10.1007/978-3-642-34188-5_8
    title: Marijn J. H. Heule, Oliver Kullmann, Siert Wieringa and Armin Biere, Cube and conquer, guiding CDCL SAT solvers by lookaheads, HVC 2011, LNCS 7261, 2012, 50-65
    locator: Section 6.2, the comparison of partitioning and portfolio approaches to parallel SAT
  - book: isbn:9781643681603
    title: Biere, Heule, van Maaren and Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 12 (algorithm configuration and selection) for portfolios, and Chapter 4 for the CDCL parameters that a portfolio varies
---

A parallel portfolio solver runs $k$ different SAT solvers, or $k$ differently configured copies of one [CDCL](/cdcl/) solver, on the same formula at the same time. The first one to find a model or a refutation stops the others. The members differ in their [restart](/restarts/) policy, decision heuristic, [phase](/phase-saving/) policy and random seed, so that their run times on one formula differ widely. In addition, the members usually exchange short learned clauses, which are valid for all of them. The idea of algorithm portfolios comes from Gomes and Selman (2001). ManySAT (Hamadi, Jabbour and Sais, 2009), first shown in the parallel track of the SAT-Race 2008, brought it to CDCL with clause sharing. The alternative is to split the search space, as in [cube-and-conquer](/cube-and-conquer/).

## In plain words

Give the same puzzle to several people who each have their own way of working. Whoever finishes first gives the answer, and the others stop. Since a solver's run time on one puzzle depends a lot on luck and on its settings, the fastest of several different solvers is often much faster than a typical one.

The solvers can also pass each other short notes: facts they have learned, which hold for everyone because everyone works on the same puzzle.

## When it applies

- Formulas where the run time of one solver varies widely with the seed or the settings, which is common for CDCL on application formulas.
- Machines with several cores and shared memory, where clause sharing is cheap.
- Formulas that are hard to split into parts of equal difficulty, so that divide and conquer gives unbalanced work.

If all members behave the same way, the portfolio gains nothing; diversity is the whole point.

## The template

Notation: $F$ is a CNF formula with $n$ variables, $m$ clauses and size $|F|$, the total number of literal occurrences. There are $k$ members $P_1, \ldots, P_k$, and $e$ is the size limit for shared clauses.

```pseudo id=main
PORTFOLIO(F, P_1, …, P_k)
L1  start member P_i on F in thread i, for i = 1, …, k
L2  each P_i runs CDCL with its own restarts, heuristic, phase policy and seed
L3  when P_i learns a clause c with |c| ≤ e, it puts c in its export queue
L4  P_j imports unit clauses at its next restart and other clauses after a decision
L5  when some P_i finds a model or derives the empty clause, it reports the answer
L6  stop all threads and return that answer
```

The holes are the set of configurations (L2), the sharing rule (L3) and the import points (L4).

**ManySAT, as published.** The JSAT paper describes four cores (Table 1). They differ in their restart policies: geometric (100, then factor 1.5), a new dynamic policy, arithmetic (steps of 16000), and Luby with unit 512. The cores use VSIDS with 2% or 3% random decisions, and the phase is chosen by occurrence counts, progress saving, or always false. Two cores use an extended learning scheme. Each core exports learned clauses of size at most $e = 8$, a limit chosen by tests on SAT-Race 2008 and SAT Competition 2007 formulas. Units are imported when a core is at level 0, and other clauses after each decision, through lockless queues.

### Why it is correct

**Lemma 1.** Every clause that any member learns or imports is implied by $F$.

*Proof.* By induction on time. Each member starts from $F$. A learned clause is a resolvent of clauses that the member holds, which are implied by $F$ by the hypothesis. An imported clause was learned or imported by another member, so it is implied by $F$ too. $\square$

So each member works on a formula with the same models as $F$, plus implied clauses. A model found by any member is a model of $F$, and an empty clause derived by any member shows that $F$ is unsatisfiable. The answer at L5 is correct, and it does not depend on which member finishes first.

### Expected run time of the fastest member

Let $T_1, \ldots, T_k$ be the run times of the members without clause sharing, as random variables over the seeds. The portfolio takes $\min_i T_i$ (plus overhead), and for non-negative run times
$$\mathbb{E}\Big[\min_i T_i\Big] = \int_0^\infty \Pr[T_1 > t, \ldots, T_k > t]\, dt.$$

For $k$ independent copies with the same distribution, the integrand is $\Pr[T > t]^k$. Three cases show what to expect.

- **Identical behaviour.** If the members are copies of one deterministic solver, all $T_i$ are equal and the portfolio gains nothing.
- **Exponential run times.** If $\Pr[T > t] = e^{-\lambda t}$, then $\mathbb{E}[\min] = 1/(k\lambda) = \mathbb{E}[T]/k$. The speedup is exactly $k$.
- **Heavy tails.** If $T = 1$ with probability $1/2$ and $T = L$ otherwise, then $\mathbb{E}[T] = (1 + L)/2$ and $\mathbb{E}[\min] = (1 - 2^{-k}) + 2^{-k} L$. For $L = 1000$ and $k = 4$ this is $500.5$ against $63.4375$, a speedup of about 7.9 on 4 cores.

So a portfolio can give a speedup larger than the number of cores when run times have heavy tails. Gomes and Selman studied this effect, and the same effect explains why [restarts](/restarts/) help a single solver. Note that this compares with a typical run of one member; against the best member for each formula, a portfolio without sharing can never be faster.

## Classic examples

- **ManySAT on SAT-Race 2008.** On the 100 formulas of the SAT-Race 2008, with a 900 second limit on a machine with 4 cores, the authors report that ManySAT solved 45 satisfiable and 45 unsatisfiable formulas, against 44 and 41 for pMinisat and 43 and 30 for MiraXT (Table 2). Against the best sequential solver of that race, Minisat 2.1, they report an average speedup of 6.02 for ManySAT on 4 cores, with a minimum of 0.25 and a maximum of 250.17 (Table 3). This is the superlinear effect of the section above, together with clause sharing.
- **Diversity by restarts and phases.** The members of a portfolio vary exactly the parameters on which CDCL is most sensitive: [restart](/restarts/) schedules, the noise in [VSIDS](/vsids/), and the [phase](/phase-saving/) policy.
- **Clause filters.** Instead of a fixed length limit, later portfolios share clauses by quality measures such as the [literal block distance](/literal-block-distance/), and decide what to keep by the same rules as [clause database reduction](/clause-database-reduction/).
- **Cube-and-conquer compared.** Heule et al. report that on hard SAT 2009 application formulas their cube-and-conquer solver solved several more formulas than the portfolio solvers Plingeling and ManySAT, while the portfolios were stronger on three very large formulas. See [cube-and-conquer](/cube-and-conquer/).

## Variations

- **Algorithm selection.** Instead of running all members, predict the best one from features of the formula and run only it. SATzilla is the best-known SAT example; the Handbook chapter on configuration and selection covers it.
- **Sequential portfolios.** Run members one after another with time slices on a single core.
- **Dynamic sharing.** ManySAT 1.1 changes the size limit of shared clauses with a control loop, to keep the flow of clauses between each pair of cores near a target.
- **Unit-only sharing.** Some portfolios exchange only units and equivalences, which are cheap and always useful.
- **Massive portfolios.** On clusters with hundreds or thousands of cores, members are grouped, and clauses are shared in batches over the network.
- **Hybrids.** Combine a portfolio with divide and conquer: split the search space with guiding paths or cubes, and give each part to a small portfolio, with [work stealing](/work-stealing/) when a part ends early.

## Pitfalls

- **No diversity.** $k$ copies of one solver with the same seed do the same search $k$ times. Vary seeds at least, and better the restart and phase policies.
- **Sharing too much.** Every imported clause costs memory and propagation time in every member. Long clauses are rarely useful elsewhere; the ManySAT tests found a limit of 8 best on their benchmarks.
- **Preprocessing that differs between members.** If a member eliminates a variable, clauses imported over that variable are wrong for it. Share only over variables that all members keep, or run the preprocessing once before the portfolio starts.
- **Non-deterministic answers.** With sharing and timing effects, the run time and the model returned change from run to run. Some solvers offer a deterministic mode that synchronizes the members at fixed points.
- **Proofs.** A proof of unsatisfiability must include the imported clauses, which come from other members' proofs. Merging DRAT proofs from several threads needs care with the order of additions and deletions.

## Exercises

1. Prove the formula $\mathbb{E}[\min_i T_i] = \int_0^\infty \Pr[\min_i T_i > t]\,dt$ for non-negative random variables, and derive the exponential case.
2. In the two-point example, find the number of cores $k$ that gives the largest speedup per core for $L = 1000$.
3. Show that a portfolio without clause sharing is never faster on a formula than its fastest member alone on that formula, and give an example where clause sharing makes it faster.
4. Design a scheme that lets a member with variable elimination still import clauses safely.
5. Explain why a portfolio and restarts in one solver use the same property of heavy-tailed run times.

## References
