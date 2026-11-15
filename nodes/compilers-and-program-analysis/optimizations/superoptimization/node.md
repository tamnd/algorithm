---
tag: QZVYCR
kind: technique
slug: superoptimization
name: Superoptimization
aliases:
- superoptimizer
- Massalin superoptimizer
area: compilers-and-program-analysis/optimizations
level: advanced
summary: Searches all short instruction sequences for the cheapest one that is equivalent to a given sequence, checked by tests and proof.
prereqs: [peephole-optimization, three-address-code]
see_also: [stochastic-superoptimization, equality-saturation, translation-validation, cegis, program-synthesis, bit-blasting, breadth-first-search, uniform-cost-search]
sources:
  - paper: doi:10.1145/36206.36194
    title: Henry Massalin, Superoptimizer, a look at the smallest program, Proceedings of the Second International Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS II), 1987, 122-126
    locator: the exhaustive search over instruction sequences in order of length, the quick test on sample inputs before a full check, the pruning of sequences, and the short branch-free programs found for the 68020
  - paper: doi:10.1145/143095.143146
    title: Torbjörn Granlund and Richard Kenner, Eliminating branches using a superoptimizer and the GNU C compiler, Proceedings of the ACM SIGPLAN 1992 Conference on Programming Language Design and Implementation (PLDI 1992), 341-352
    locator: the GNU superoptimizer, its search over short sequences for several machines, and the branch-free sequences added to GCC
  - paper: doi:10.1145/512529.512566
    title: "Rajeev Joshi, Greg Nelson and Keith Randall, Denali: a goal-directed superoptimizer, Proceedings of the ACM SIGPLAN 2002 Conference on Programming Language Design and Implementation (PLDI 2002), 304-314"
    locator: the goal-directed search that matches axioms into an e-graph and asks a SAT solver for a program within a cycle budget
  - paper: doi:10.1145/1168857.1168906
    title: Sorav Bansal and Alex Aiken, Automatic generation of peephole superoptimizers, Proceedings of the 12th International Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS 2006), 394-403
    locator: superoptimizing the sequences of training programs offline, with canonical register names, test vectors and a solver check, and storing the results as peephole rules
  - paper: doi:10.1145/2451116.2451150
    title: Eric Schkufza, Rahul Sharma and Alex Aiken, Stochastic superoptimization, Proceedings of the 18th International Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS 2013), 305-316
    locator: the replacement of exhaustive search by a Markov chain over programs, with tests and a validator
  - paper: doi:10.1145/2872362.2872387
    title: Phitchaya Mangpo Phothilimthana, Aditya Thakur, Rastislav Bodik and Dinakar Dhurjati, Scaling up superoptimization, Proceedings of the 21st International Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS 2016), 297-310
    locator: the enumerative search that prunes by the state of the machine on tests, and its combination with stochastic and symbolic search
---

A superoptimizer finds the cheapest instruction sequence that computes the same thing as a given sequence. It does not apply rewrite rules. It searches: it tries every sequence of length 0, then every sequence of length 1, then of length 2, and stops at the first one that is equivalent to the target. Henry Massalin built the first one in 1987 for the Motorola 68020 and gave it the name: the result is not just better code, it is the best code for the machine model and the cost. Because the number of sequences grows as the number of instructions to the power of the length, a superoptimizer only reaches sequences of a few instructions. Each candidate first runs on a few test inputs, which rejects almost all of them at low cost, and the survivors get a full equivalence check. The common mistake is to take a sequence that passes the tests as a correct one. Tests can only reject; only the full check, by exhaustive inputs or a solver, can accept.

## In plain words

Suppose a compiler wrote three instructions for a small job. Is there a shorter way? A superoptimizer answers by brute force. It lists every possible sequence of one instruction and asks of each: does it do the same job? Then every sequence of two instructions, and so on. The first one that does the job is the shortest, because all shorter ones were already tried.

Asking "does it do the same job" for every input is slow. So each candidate first runs on a handful of sample inputs. Almost every candidate fails at once and is thrown away. The few that pass all samples get a full check, and only a candidate that passes the full check is kept.

The lists grow very fast, so this works for a few instructions only. It pays for code that runs very often.

## When it applies

- The target is a short straight-line sequence, or a window of a longer one, whose live-in and live-out registers are known. Branches and memory make the model and the check much harder.
- The machine has a precise model: what each instruction does to every register, flag and memory cell that matters.
- The cost of each instruction is known and positive. The usual cost is the number of instructions, or the cycles from a latency table.
- The result is worth a long search: an inner loop, a library routine, or a rule that a [peephole optimizer](/peephole-optimization/) will apply many times.

## The template

**Model.** A machine state is the contents of the registers (and flags and memory, if the model has them). An instruction is a function from states to states. A program $p = i_1; \ldots; i_n$ runs its instructions in order. The inputs are the live-in registers and the output is the set of live-out registers. The instruction set $\mathcal{I}$ is finite: on the toy machine here, `rd = ra op rb` with `op` one of `+ - & | ^ << >>` and a copy `rd = ra`, over four registers of $w$ bits and the constant 1, which gives $|\mathcal{I}| = 716$.

**Legality.** A candidate $q$ may replace the target $p$ if $p \equiv q$: for every input, $p$ and $q$ give the same live-out values. Registers that are not live-out may differ. A test is an input $x$ with the output $p(x)$. *If $q(x) \ne p(x)$ for one test, then $q \not\equiv p$*, so a failed test is a sound reason to reject. A passed test proves nothing about other inputs. The full check is exhaustive on a small model, as here, where there are $2^{2w} = 256$ inputs. On a real machine it is a query to a SAT or SMT solver: [bit-blast](/bit-blasting/) the formula $p(x) \ne q(x)$; if it has no solution, $p \equiv q$, and if it has one, the solution is an input that refutes $q$ and can become a new test.

**Profit.** The cost of a program is $c(p) = \sum_k c(i_k)$ with every $c(i) \ge 1$. With $c(i) = 1$, the cost is the length.

**The search.**

```
for n = 0, 1, ..., N:
    for every q in I^n:
        if q(x) == p(x) for every test x:
            if q is equivalent to p (full check):
                return q
return "none of length <= N"
```

*Theorem 1. If some program of length at most $N$ is equivalent to $p$, the search returns a program equivalent to $p$ of the least length among all such programs.* Proof. The search returns only programs that pass the full check, so the result is equivalent to $p$. Let $n^*$ be the least length of an equivalent program, so $n^* \le N$. For $n < n^*$, no $q \in \mathcal{I}^n$ is equivalent; each either fails a test or fails the full check, so the loop does not return at length $n$. At length $n^*$, the loop visits an equivalent $q^*$. A test cannot reject $q^*$, since $q^*(x) = p(x)$ for every $x$, and the full check accepts it. So the loop returns at length $n^*$, possibly with an earlier program of the same length, which is equivalent too. $\square$

The proof needs two things: the enumeration visits every sequence of each length, and the filter never rejects an equivalent program. Both are what "exhaustive" means here.

**Pruning by state.** The *full state* of a prefix $q$ is the function that maps each input to the whole machine state after $q$, all registers and not only the live-out ones. Two prefixes with the same full state are interchangeable.

*Lemma 2. If prefixes $q$ and $q'$ have the same full state, then for every suffix $s$, $q; s$ and $q'; s$ have the same full state.* Proof. Each instruction is a function of the state. By induction on the length of $s$: the claim holds for the empty suffix, and if $q; s$ and $q'; s$ give the same state on every input, one more instruction $i$ gives the same state again. $\square$

This gives a breadth-first search over full states. Level 0 holds the full state of the empty program. Level $k$ holds every full state that some one-instruction extension of a level $k - 1$ state reaches and that no lower level holds, with one program that reaches it. The search stops at the first level with a state whose live-out part is the output of $p$ on every input.

*Theorem 3. Level $k$ holds exactly the full states whose shortest program has length $k$. So the search returns a shortest program equivalent to $p$.* Proof by induction on $k$. For $k = 0$ it is clear. Let $\sigma$ have a shortest program $q; i$ of length $k \ge 1$. The prefix $q$ has a full state $\sigma'$ whose shortest program has some length $j \le k - 1$, and by induction $\sigma'$ is at level $j$ with a program $r$. By Lemma 2, $r; i$ also reaches $\sigma$, with length $j + 1$. Since $k$ is the least length for $\sigma$, $j + 1 \ge k$, so $j = k - 1$. The search extends $r$ by $i$ at level $k$, and no lower level holds $\sigma$, so $\sigma$ is at level $k$. Conversely, a state at level $k$ has a program of length $k$ and is not at a lower level, so by induction it has no shorter program. The live-out part of a full state decides equivalence, so the first level with an equivalent state is the least length of an equivalent program. $\square$

The same argument with costs in place of lengths, and a priority queue in place of levels, is [uniform-cost search](/uniform-cost-search/) over full states; it returns a program of least cost because every cost is positive. On a real machine there are too many inputs to store a full state, so tools keep the state on the tests only. Then two prefixes can look the same and differ on another input. Merging them can lose the shortest program, but it never makes the search return a wrong one, as long as the result still gets the full check.

## Classic examples

The numbers come from a Python script on the toy machine of the [stochastic superoptimization](/stochastic-superoptimization/) page: $w = 4$, registers `r0` to `r3`, inputs in `r0` and `r1`, output in `r0`, 716 instructions and 256 inputs. The full check runs all 256 inputs.

**XOR in disguise.** The target is

```
r2 = r0 | r1
r3 = r0 & r1
r0 = r2 - r3
```

which computes $x \oplus y$, since $x \mid y$ is $x \oplus y$ plus the bits of $x \wedge y$. With the four tests $(4, 2), (8, 3), (15, 14), (15, 12)$, drawn by a generator with seed 1, the search finds:

| length | candidates | pass the tests | equivalent |
|---|---|---|---|
| 0 | 1 | 0 | 0 |
| 1 | 716 | 2 | 2 |

The two results are `r0 = r0 ^ r1` and `r0 = r1 ^ r0`. Four tests reject 714 of 716 candidates, and the full check runs only twice.

**Tests that are too weak.** The target is `r0 = r0 + r1`, with the tests $(0, 0), (1, 0), (0, 1)$. Of the 716 programs of length 1, six pass: the two orders of `+`, of `|` and of `^`. Only the two orders of `+` are equivalent. The full check refutes `r0 = r0 | r1` with the input $(1, 1)$, where it gives 1 and the target gives 2, and `r0 = r0 ^ r1` with the same input, where it gives 0. A superoptimizer that trusted the tests would turn every addition into an OR.

**Pruning by full state.** The target is

```
r2 = r0 + r0
r3 = r1 + r1
r0 = r2 + r3
```

which computes $2x + 2y$. The search over full states holds 156 new states at level 1 and 20,447 new states at level 2, out of $156 \cdot 716 = 111{,}696$ extensions. At level 2 it finds `r0 = r0 + r1; r0 = r0 + r0`. Plain enumeration of length 2 visits $716^2 = 512{,}656$ programs, of which 16 compute $2x + 2y$. Length 3 would be $716^3 \approx 3.7 \cdot 10^8$ programs, which is why every real superoptimizer prunes.

## Variations

- **Massalin's superoptimizer.** Exhaustive search by length over a real instruction set, with a quick test on sample inputs and pruning of sequences that cannot be optimal. Its results were short branch-free sequences, such as the sign function, that use the carry flag in ways a person does not expect.
- **The GNU superoptimizer.** Granlund and Kenner searched short sequences for several machines and put the branch-free results into GCC.
- **Goal-directed search.** Denali does not enumerate. It applies equality axioms to an e-graph of the target, as in [equality saturation](/equality-saturation/), and asks a SAT solver whether some program within a cycle budget computes the goal from the e-graph.
- **Peephole superoptimizers.** Bansal and Aiken superoptimize the short windows that appear in training programs, offline, and store each result as a rule. A [peephole optimizer](/peephole-optimization/) then applies the rules quickly at compile time.
- **Stochastic search.** [STOKE](/stochastic-superoptimization/) replaces exhaustive search by a Markov chain over programs, which reaches longer programs but gives no guarantee of the least cost.
- **Synthesis with a solver.** The search can also be a [CEGIS](/cegis/) loop: a solver proposes a program that is right on the tests, a second query looks for an input that refutes it, and that input becomes a test. This is [program synthesis](/program-synthesis/) with a cost bound.

## Pitfalls

- **Tests are not a proof.** The weak tests above accept `r0 = r0 | r1` for an addition. Every result must pass a full check. A test can only reject.
- **Pruning on the outputs only.** Lemma 2 needs the whole state. Keep one prefix per value of `r0` alone, and the prefix `r1 = r0 + r1`, which leaves `r0` unchanged, looks like the empty program and is dropped. For the target $(x + y) \oplus x$, the search over full states finds `r1 = r0 + r1; r0 = r0 ^ r1` at length 2. With states keyed on `r0` alone, the script keeps 39, 543 and 7,671 states at levels 1 to 3 and finds no program of length 3 or less.
- **A model that is too small.** A sequence that is right for 4-bit words can be wrong for 64-bit words: $x \gg 4$ is 0 for every 4-bit $x$. The check must use the real word size, flags that are live, and the real rules for memory and undefined cases.
- **The wrong live-out set.** A candidate that writes `r2` is legal only if `r2` is dead after the window. A wrong liveness fact makes a correct search give an incorrect program.
- **The wrong cost.** The least number of instructions is not always the fewest cycles. Latency, throughput and dependences between instructions decide the speed, so the cost model must match the target machine.
- **Explosion.** The search space is $|\mathcal{I}|^n$. Exhaustive search stops at a few instructions, and the full check costs a solver query per survivor. Use it offline, on hot code or to generate rules, not in every compile.

## Exercises

1. On the toy machine, how many programs of length at most 2 are there? How many does Theorem 1 visit, at most, before it returns a program of length 2?
2. Prove that the search with a filter that can reject an equivalent program (a wrong expected output on one test) can return a longer program than the shortest one, or none.
3. Give two prefixes of length 1 with the same value of `r0` on every input and different full states, and a one-instruction suffix that tells them apart.
4. Change the cost so that `<<` costs 1 and `+` costs 2. Which program of least cost computes $2x + 2y$? Show that uniform-cost search over full states finds it.
5. A solver says that $p(x) \ne q(x)$ has the solution $x_0$. Explain how adding $x_0$ to the tests changes the next runs of the search, and why the search still returns a program of least length.

## References
