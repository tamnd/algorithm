---
tag: 7ZW1HX
kind: technique
slug: cube-and-conquer
name: Cube-and-conquer
aliases:
- cube and conquer
- CnC
area: logic-and-constraints/sat-solving
level: research
summary: Split the formula into many cubes with a lookahead solver that cuts its tree by a dynamic threshold, then solve each cube with incremental CDCL under assumptions.
prereqs: [lookahead-sat, cdcl, incremental-sat]
see_also: [parallel-portfolio-sat, drat-proof, failed-literal-probing, work-stealing, pigeonhole-principle]
sources:
  - paper: doi:10.1007/978-3-642-34188-5_8
    title: Marijn J. H. Heule, Oliver Kullmann, Siert Wieringa and Armin Biere, Cube and conquer, guiding CDCL SAT solvers by lookaheads, HVC 2011, LNCS 7261, 2012, 50-65
    locator: Section 4 (the basic method on van der Waerden instances), Section 5 (CreateCubes and the cutoff rule with theta, Figures 2 and 3), Section 6 (solving the cubes, Figure 4), Section 7 and Table 1 (experiments)
  - paper: doi:10.1007/978-3-319-40970-2_15
    title: Marijn J. H. Heule, Oliver Kullmann and Victor W. Marek, Solving and verifying the Boolean Pythagorean triples problem via cube-and-conquer, SAT 2016, LNCS 9710, 228-245
    locator: the encoding, the split into cubes, the run on 800 cores and the DRAT proof
  - paper: "Peter van der Tak, Marijn J. H. Heule and Armin Biere, Concurrent cube-and-conquer, Pragmatics of SAT (POS) 2012"
    title: Concurrent cube-and-conquer
    locator: running the cube phase and the conquer phase at the same time
  - book: isbn:9781643681603
    title: Biere, Heule, van Maaren and Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 5 (Heule and van Maaren, Look-Ahead Based SAT Solvers), the lookahead heuristics that the cube phase uses
---

Cube-and-conquer solves a hard CNF formula in two phases. In the *cube phase*, a [lookahead solver](/lookahead-sat/) builds the top of a search tree and cuts it off at a dynamic depth. Each cut branch gives a *cube*, the conjunction of the decision literals on its path, and each branch that the lookahead refutes gives a learned clause. In the *conquer phase*, a [CDCL](/cdcl/) solver solves the formula under each cube, usually as [assumptions](/incremental-sat/) in one incremental solver. The formula is satisfiable exactly when some cube is. The method combines the strengths of both kinds of solver: lookahead makes good global decisions near the root, and CDCL is fast on the easy subproblems near the leaves. Heule, Kullmann, Wieringa and Biere introduced it in 2011. The cubes are independent, so the conquer phase runs in parallel with no communication, and the method has solved the Boolean Pythagorean triples problem and other hard combinatorial problems.

## In plain words

A hard puzzle can be too big for one fast but short-sighted solver. So first let a careful planner make the first few big choices, in every possible way. Each list of choices is one smaller puzzle, and the planner stops when the smaller puzzle looks easy enough. Some lists of choices already lead to a clash, and the planner throws them away.

Then hand each small puzzle to the fast solver. If any small puzzle has a solution, the big one has too. If every small puzzle fails, the big one has no solution. The small puzzles do not depend on each other, so many computers can share them.

## When it applies

- Hard combinatorial formulas, often unsatisfiable, where plain CDCL takes days or more and lookahead alone also takes too long.
- Problems where splitting on a few variables makes the rest much easier, so that the cubes are of similar difficulty.
- Parallel or distributed solving: cubes are independent jobs, and thousands of cores can work with no clause sharing.
- Cases that need a proof: each cube gives its own [DRAT](/drat-proof/) proof, and the proofs and the tree combine into one.

It is a poor fit for large industrial formulas that CDCL solves quickly anyway: there the cube phase costs more than it saves.

## The template

Notation: $F$ is a CNF formula with $n$ variables, $m$ clauses and size $|F|$, the total number of literal occurrences. $|\mathrm{vars}(F)|$ counts the variables that occur in $F$. At a node of the cube tree, $\varphi_{dec}$ is the set of decision literals on the path from the root, and $\varphi_{imp}$ is the set of literals implied by the lookahead (unit propagation and failed literals). The threshold $\theta$ is a global number that changes during the search.

The cube phase is CreateCubes* of the 2011 paper (Figure 3), and the conquer phase is its Figure 4.

```pseudo id=main
CUBE-AND-CONQUER(F)
L1  θ ← 1000; A ← ∅ (cubes); C ← ∅ (learned clauses); CREATE-CUBES(∅), with:
L2      CREATE-CUBES(φ_dec): θ ← 1.05·θ; φ_imp ← LOOKAHEAD-SIMPLIFY(F, φ_dec)
L3      if φ_dec ∪ φ_imp falsifies a clause of F or |φ_dec| > 20 then θ ← 0.7·θ
L4      if φ_dec ∪ φ_imp falsifies a clause of F then C ← C ∪ {¬φ_dec}; return
L5      if |φ_dec| · |φ_dec ∪ φ_imp| > θ · |vars(F)| then A ← A ∪ {φ_dec}; return
L6      l ← LOOKAHEAD-DECIDE(F, φ_dec ∪ φ_imp)
L7      CREATE-CUBES(φ_dec ∪ {l}); CREATE-CUBES(φ_dec ∪ {¬l})
L8  load F ∪ C into an incremental CDCL solver S
L9  for each cube c in A
L10     if S is SAT under the assumptions c then return SAT with its model
L11     optionally add the clause ¬c′, where c′ ⊆ c are the failed assumptions
L12 return UNSAT
```

**The exact rules.**

- **Cutoff (L5).** A node becomes a cube when the product of the number of decisions and the number of assigned variables is larger than $\theta$ times the number of variables. The product mixes two older rules: cut after a fixed number of decisions (method A), or after a fixed number of assigned variables (method B).
- **Increment (L2).** $\theta$ grows by 5% at every node, with no condition, so that it can recover when it got too small.
- **Decrement (L3).** $\theta$ shrinks by 30% at every refuted node and at every node deeper than 20 decisions. The idea of the authors is that a conflict found by the lookahead would have been found faster by CDCL, so the neighbouring branches should be cut earlier. The depth rule stops the tree from growing too deep; for a fast cube phase they suggest the condition $|\varphi_{dec}| + \log_2 |F| > 30$ instead.
- **Start value (L1).** $\theta = 1000$. They report that a value 10 times larger or smaller hardly changes the partition. With this start, $\theta$ first decreases before any branch is cut.
- **Cubes.** A cube holds only the decisions $\varphi_{dec}$, in the order they were made. The authors found that adding the implied literals did not help.
- **Refuted leaves (L4).** The clause $\neg\varphi_{dec}$ goes into $C$. After the cube phase, $C$ is shortened by self-subsuming resolution, and the shorter clauses remove literals from the cubes.
- **Conquer (L8 to L12).** One incremental solver takes the cubes one by one as assumptions. After a refuted cube, the clause of the failed assumptions may be added, and the authors also reset the clause deletion policy, because learned clauses of one cube rarely help with the next.

### Why it is correct

**Lemma 1.** Every clause added to $C$ is implied by $F$.

*Proof.* The lookahead simplification adds only literals implied by $F \wedge \varphi_{dec}$ (unit propagation and failed literals, see [failed-literal probing](/failed-literal-probing/)). If they falsify a clause, then $F \wedge \varphi_{dec}$ is unsatisfiable, so $F$ implies $\neg\varphi_{dec}$. $\square$

**Lemma 2.** The cubes are pairwise contradictory, and every model of $F$ satisfies exactly one cube.

*Proof.* Two leaves of the binary tree split at some node, where one took $l$ and the other $\neg l$, so their cubes clash. Take a model $\sigma$ of $F$ and follow from the root the branch whose decision $\sigma$ satisfies. At each node on this path, the implied literals are implied by $F$ and the decisions, so $\sigma$ satisfies them, and no clause is falsified. So the path cannot end at a refuted leaf, and it ends at a cube that $\sigma$ satisfies. $\square$

**Theorem.** CUBE-AND-CONQUER returns SAT with a model of $F$ if and only if $F$ is satisfiable.

*Proof.* By Lemma 1, $F \wedge C$ has the same models as $F$, and the clauses $\neg c'$ of L11 are implied by $F \wedge C$ (see [incremental SAT](/incremental-sat/)). If $F$ is satisfiable, a model satisfies some cube by Lemma 2, so the solver finds a model at L10 at the latest for that cube. A model found at L10 satisfies $F$. $\blacksquare$

## Classic examples

**A traced run.** For the [pigeonhole formula](/pigeonhole-principle/) with 5 pigeons and 4 holes (20 variables, $x_{4i+j+1}$ for pigeon $i$ in hole $j$), the implementation with the start value $\theta = 0.5$ instead of 1000 builds this tree:

| node $\varphi_{dec}$ | $\vert\varphi_{dec} \cup \varphi_{imp}\vert$ | $\theta$ after L2, L3 | result |
|---|---|---|---|
| $\emptyset$ | 0 | 0.525 | decide $\neg x_1$ |
| $\neg x_1$ | 1 | 0.551 | $1 \le 11.0$, decide $\neg x_2$ |
| $\neg x_1, \neg x_2$ | 2 | 0.579 | $4 \le 11.6$, decide $x_3$ |
| $\neg x_1, \neg x_2, x_3$ | 7 | 0.608 | $21 > 12.2$: cube |
| $\neg x_1, \neg x_2, \neg x_3$ | 8 | 0.638 | $24 > 12.8$: cube |
| $\neg x_1, x_2$ | 6 | 0.670 | $12 \le 13.4$, decide $x_5$ |
| $\neg x_1, x_2, x_5$ | conflict | 0.492 | learn $(x_1 \vee \neg x_2 \vee \neg x_5)$ |
| $\neg x_1, x_2, \neg x_5$ | conflict | 0.362 | learn $(x_1 \vee \neg x_2 \vee x_5)$ |
| $x_1$ | 5 | 0.380 | $5 \le 7.6$, decide $x_6$ |
| $x_1, x_6$ | conflict | 0.279 | learn $(\neg x_1 \vee \neg x_6)$ |
| $x_1, \neg x_6$ | conflict | 0.205 | learn $(\neg x_1 \vee x_6)$ |

So there are 2 cubes and 4 refuted leaves. In the conquer phase, the first cube fails with the core $\{x_3\}$, and the unit $(\neg x_3)$ is added. Then the second cube fails with the empty core: $F \wedge C$ with the added clause is already unsatisfiable. The tests check this trace, check Lemmas 1 and 2 by brute force on random formulas with up to 10 variables, and check the answer against brute force for up to 12 variables.

**Van der Waerden numbers.** The method came out of work on van der Waerden numbers. In Section 4 of the 2011 paper, the OKsolver made the cubes by cutting at a fixed number $D$ of assigned variables, and MiniSat 2.2.0 solved them, on one core. The authors report, for example, that for $vdw(3, 15) = 218$ the lookahead solver satz needed about 20 hours, while cube-and-conquer with $D = 35$ (32331 cubes) took about 4 hours. For $vdw(4, 8) = 146$, picosat needed 8 hours and cube-and-conquer with $D = 20$ (65270 cubes) 4 hours. They state a total speed-up of at least a factor of two over the best single solver on these instances.

**Hard application instances.** In Section 7 of the same paper, march_cc made the cubes and iLingeling solved them on 12 cores, on instances of the SAT 2009 application track that no solver had solved in the competition. The authors report that cube-and-conquer solved several more of these instances than the portfolio solvers Plingeling and ManySAT, while the portfolio solvers were stronger on three very large instances.

**Boolean Pythagorean triples.** Heule, Kullmann and Marek (2016) showed with cube-and-conquer that $\{1, \ldots, 7825\}$ cannot be split into two parts with no Pythagorean triple $a^2 + b^2 = c^2$ inside one part. They report a run of about 2 days on a cluster with 800 cores, a DRAT proof of almost 200 terabytes, and a compressed certificate of 68 gigabytes.

## Variations

- **The basic method.** Cut each branch after exactly $D$ decisions, or once at least $D$ variables are assigned, and solve each cube as an independent file. This is Section 4 of the 2011 paper.
- **Order of the cubes.** The authors observed that cubes with more right branches (discrepancies) tend to be easier. For satisfiable formulas, they solve cubes with few right branches first, as in limited discrepancy search. In parallel runs, hard cubes should start first.
- **Parallel conquer.** Idle threads take the next unsolved cube. This needs no communication beyond the job queue; see also [work stealing](/work-stealing/). Clause sharing between the threads is optional.
- **Concurrent cube-and-conquer.** Run the two phases at the same time and let CDCL take over branches that the lookahead finds hard (van der Tak, Heule and Biere).
- **Cubes in the proof.** For verified results, each cube gets a DRAT proof under its assumptions, and a proof that the cubes cover the space ties them together, as in the Pythagorean triples proof.

## Pitfalls

- **Cutting too early.** Few, hard cubes waste the parallelism, and one hard cube can dominate the run time. Lowering $\theta$ at refuted nodes (L3) and the depth rule counter this.
- **Cutting too late.** Millions of trivial cubes make the cube phase the bottleneck, and the incremental solver spends its time on assumptions.
- **Implied literals in the cubes.** Putting $\varphi_{imp}$ into the cubes adds literals that CDCL may not derive by unit propagation, such as failed literals. The paper found decision-only cubes better.
- **Learned clauses across cubes.** Keeping all learned clauses of earlier cubes slows the solver down; reset the clause database after each cube (Figure 4, line 6).
- **Satisfiable formulas.** The order of the cubes matters only for satisfiable formulas, and a bad order can hide the solution in the last cube.

## Exercises

1. Show that the clauses $\neg c'$ added at L11 never remove a model of $F$.
2. Prove that the cubes of a cube tree together with the refuted leaves cover all $2^n$ assignments exactly once.
3. With $\theta$ fixed, compare the number of cubes produced by the product rule with method A (a fixed number of decisions) on a formula where one branch of each decision assigns many more variables than the other.
4. Describe how to build a single DRAT proof of unsatisfiability from one DRAT proof per cube and the clauses of $C$.
5. Why is it reasonable to decrease $\theta$ after the lookahead refutes a node? Give an example where it makes the next cube easier for CDCL.

## References
