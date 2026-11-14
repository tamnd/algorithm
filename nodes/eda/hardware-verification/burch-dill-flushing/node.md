---
tag: W76CN0
kind: technique
slug: burch-dill-flushing
name: Burch-Dill flushing
aliases:
- pipeline flushing abstraction
- Burch-Dill commutative diagram
area: eda/hardware-verification
level: advanced
summary: Burch and Dill's check of a pipelined processor against its ISA that flushes the pipeline to get an abstraction function and proves a commuting diagram in EUF logic.
prereqs: [euf-satisfiability, simulation-relation]
see_also: [positive-equality, euf-satisfiability, congruence-closure, ackermannization, simulation-relation, inductive-invariant, symbolic-simulation, product-machine]
sources:
  - paper: doi:10.1007/3-540-58179-0_44
    title: J. R. Burch and D. L. Dill, Automatic verification of pipelined microprocessor control, Computer Aided Verification (CAV 1994), LNCS 818, 68 to 80, 1994
    locator: the abstraction function obtained by flushing the pipeline with stall inputs, the commuting diagram between one implementation step and zero or one specification steps, and its check by a validity checker for uninterpreted functions with equality
  - paper: doi:10.1145/371282.371364
    title: R. E. Bryant, S. German and M. N. Velev, Processor verification using efficient reductions of the logic of uninterpreted functions to propositional logic, ACM Transactions on Computational Logic 2(1), 93 to 134, 2001
    locator: positive equality and the reduction of the Burch-Dill formulas of pipelined processors to propositional logic
  - paper: doi:10.1007/bfb0028739
    title: R. Hosabettu, M. Srivas and G. Gopalakrishnan, Decomposing the proof of correctness of pipelined microprocessors, Computer Aided Verification (CAV 1998), LNCS 1427, 122 to 134, 1998
    locator: completion functions, one per unfinished instruction, which split the flushing abstraction into smaller proof steps
---

Burch-Dill flushing proves that a pipelined processor behaves like its instruction set architecture (ISA), which runs one instruction at a time. The hard part of such a proof is to say which ISA state an implementation state stands for, when several instructions are partly done. Burch and Dill (1994) take the answer from the implementation itself. Feed it stall cycles that fetch nothing until the pipeline is empty, then read the register file and the other programmer-visible state. This *flushing* gives an abstraction function $\alpha$ from implementation states to ISA states. The check is a commuting diagram: one implementation step followed by $\alpha$ must give the same result as $\alpha$ followed by the ISA step of the instruction that was fetched, or by no step if none was. Burch and Dill write the two sides as terms in which the data values, the ALU and the memories are uninterpreted, and they prove the equation in the logic of equality with [uninterpreted functions](/euf-satisfiability/). The check covers control logic such as bypasses, stalls and squashes, and it does not depend on the width of the data or on what the ALU computes.

## In plain words

A pipeline works on several instructions at once. One is fetched, one reads its registers, one computes, one writes back. To compare it with the simple one-at-a-time machine of the manual, you need to say what "the current state" of the pipeline means.

Flushing gives the answer. Stop fetching and let the pipeline run until every started instruction has finished. The register file then holds the state that the simple machine would have.

Now compare two routes from any pipeline state. Route one: run the pipeline for one cycle, then flush. Route two: flush, then run the simple machine on the instruction the pipeline took in that cycle. If the two routes always end in the same state, the pipeline is correct. The values in the registers stay symbols, so the proof covers every value at once.

## When it applies

- There are two deterministic machines. The implementation has a state $q \in Q$ and a step $\delta_I(q, i)$ per clock cycle, where an input $i$ offers an instruction or is a stall. The specification has a state $s$ and a step $\delta_S(s, j)$ that runs one instruction $j$.
- In every cycle the implementation either takes the offered instruction or does not, and $\mathrm{fetched}(q, i)$ says which. A stall input never fetches.
- The pipeline drains: from every reachable state, $d$ stall cycles complete all instructions in flight. Let $\mathrm{FLUSH}(q) = \delta_I^d(q, \mathrm{stall})$, and let $\mathrm{proj}$ keep the programmer-visible part. Then $\alpha(q) = \mathrm{proj}(\mathrm{FLUSH}(q))$.
- Each initial state $q_0$ has an empty pipeline, and $\alpha(q_0)$ is the matching initial ISA state $s_0$.
- For the check in EUF, the design must be correct for every interpretation of the uninterpreted parts. A design that relies on an algebraic property of the ALU, such as commutativity of addition, needs that property as an extra axiom.

The criterion of correctness is the flushed one. For every run from an initial state, flushing at the end gives the ISA state after the fetched instructions, in the order fetched.

## The template

```pseudo id=main
BURCH-DILL-CHECK(δ_I, δ_S, FLUSH, proj, Q, inputs)
L1  for each implementation state q in Q do
L2      s ← proj(FLUSH(q))
L3      for each input i do q′ ← δ_I(q, i)
L4          left ← proj(FLUSH(q′))
L5          right ← δ_S(s, instr(i)) if fetched(q, i), else s
L6          if left ≠ right then return the counterexample (q, i)
L7  return the diagram commutes on Q
```

Burch and Dill run lines L1 to L6 once, symbolically. $Q$ is all states, each latch holds a fresh symbol, and the control values are Boolean variables. Lines L2 to L5 are [symbolic simulation](/symbolic-simulation/) of $d + 1$ implementation cycles and one ISA step on terms. Line L6 asks whether the formula $\mathit{left} = \mathit{right}$ is valid in EUF. The holes of the template are the stall input and the depth $d$ of the flush, the function $\mathrm{fetched}$, and the decision procedure for line L6.

**The commuting diagram is exact on reachable states.** Let $R$ be the set of implementation states reachable from initial states. For a run $q_0 \xrightarrow{i_1} q_1 \cdots \xrightarrow{i_n} q_n$, let $w$ be the sequence of fetched instructions, and let $\delta_S^*(s_0, w)$ be the ISA state after running $w$. The theorem: the diagram commutes at every $q \in R$ and every input $i$ if and only if $\alpha(q_n) = \delta_S^*(s_0, w)$ for every run.

*Proof.* If the diagram commutes on $R$, use induction on $n$. For $n = 0$, $\alpha(q_0) = s_0$ by assumption. If $\alpha(q_{n-1}) = \delta_S^*(s_0, w')$, then $q_{n-1} \in R$ and the diagram give $\alpha(q_n) = \delta_S(\alpha(q_{n-1}), \mathrm{instr}(i_n))$ when the instruction is fetched, and $\alpha(q_n) = \alpha(q_{n-1})$ when it is not. In both cases this is $\delta_S^*$ of $s_0$ and the fetched sequence $w$. Conversely, let every run satisfy the equation. Take $q \in R$, reached by a run with fetched sequence $w$, and an input $i$. The run extended by $i$ ends in $q' = \delta_I(q, i)$, so $\alpha(q') = \delta_S^*(s_0, w j)$ with $j = \mathrm{instr}(i)$ if it is fetched, or $\delta_S^*(s_0, w)$ if not. Since $\alpha(q) = \delta_S^*(s_0, w)$, this is $\mathit{right}$ at line L5, and the diagram commutes at $(q, i)$. $\square$

The theorem says why flushing is a good choice. The abstraction comes from the stall behavior of the design, so nobody has to write it by hand. A correct design commutes with it on every reachable state, so on those states the check never gives a false alarm. A check over any $Q \supseteq R$ that passes proves the design correct. A failure at a state outside $R$ proves nothing. Burch and Dill check all states. This is stronger than needed, and it fails for designs whose correctness depends on an invariant of the reachable states (see Pitfalls).

**EUF makes it independent of the data.** In the symbolic check, each data value is a term built from symbols by uninterpreted functions, such as $\mathrm{ADD}(\mathrm{ADD}(p_a, p_b), r_0)$. A formula of EUF is valid when it is true for every domain and every interpretation of the symbols and functions. The real ALU on 32-bit words is one interpretation, so a valid diagram holds for it. When the control values are fixed, as in the code of this page, the two sides are plain terms. Then validity is syntactic equality, because the free term algebra, in which every term denotes itself, is one interpretation in which different terms differ. In general the control depends on equalities between register numbers and on data, and line L6 needs an EUF decision procedure, such as [congruence closure](/congruence-closure/) with case splits, [Ackermann's reduction](/ackermannization/) to propositional logic, or [positive equality](/positive-equality/), which made large instances fast.

**Example.** The code models a two-stage pipeline with registers $r_0, r_1, r_2$. Stage 1 reads the operands of an instruction $r_d \leftarrow \mathrm{op}(r_{s1}, r_{s2})$ into the pipeline register $P$. Stage 2 applies the ALU and writes $r_d$ at the clock edge, and a bypass gives the result to a stage 1 instruction that reads $r_d$ in the same cycle. The flush is one stall cycle, so $d = 1$. Take the state with $P$ holding $r_1 \leftarrow \mathrm{ADD}(p_a, p_b)$, the register file $(r_0, r_1, r_2)$ as symbols, and the input $r_2 \leftarrow \mathrm{ADD}(r_1, r_0)$.

| route | register file at the end |
|---|---|
| flush, then ISA step (right) | $r_0$, $\mathrm{ADD}(p_a, p_b)$, $\mathrm{ADD}(\mathrm{ADD}(p_a, p_b), r_0)$ |
| step, then flush, with the bypass (left) | the same terms |
| step, then flush, without the bypass (left) | $r_0$, $\mathrm{ADD}(p_a, p_b)$, $\mathrm{ADD}(r_1, r_0)$ |

Without the bypass, stage 1 reads the old $r_1$, and the third register differs. The terms differ, so the check fails, and an interpretation with $r_1 \ne p_a + p_b$ makes the values differ too. The breadth-first search of the tests then finds a real program that fails: write $r_1$, then read it in the next cycle. A design that bypasses only the first operand fails in the same way on $r_2 \leftarrow \mathrm{ADD}(r_0, r_1)$.

**Cost.** The two sides need $d + 1$ symbolic implementation steps and one ISA step, so the formula has size $O(d \cdot |I|)$ for a design description of size $|I|$, with shared terms. Validity in EUF is coNP-complete, because satisfiability of quantifier-free EUF is [NP-complete](/np-complete/). So the decision at line L6 is where the cost lies. The enumeration in the code is over $2 \cdot 3 \cdot R^2$ control states and $1 + 3 R^3$ inputs for $R$ registers. That is 4,428 diagrams for $R = 3$, each of a few terms.

**Tests.** The term-level check passes for the correct pipeline with 1 to 3 registers and returns a counterexample for each of three bugs. An exhaustive check with 2-bit words and the real ALU agrees, and so does a check with five random ALU tables, as EUF validity predicts. On 1-bit words with 2 registers, a breadth-first search over pairs (implementation state, ISA state) confirms the theorem for all four designs: the diagram commutes on the reachable states exactly when every flushed run matches the ISA. Each failing program that the search returns is replayed. On 600 random programs with stalls, 4-bit words and up to 4 registers, the correct design matches the ISA after a flush, and the design without the bypass fails on more than 50 of them.

## Classic examples

- **In-order pipelines.** Burch and Dill (1994) verified the control of a pipelined processor with bypasses and stalls, with data and memories left uninterpreted, using their own validity checker for EUF.
- **Positive equality.** Bryant, German and Velev (2001) showed that most equations in Burch-Dill formulas occur only positively. With [positive equality](/positive-equality/), the terms can take fixed distinct values, and the formula becomes a much smaller propositional one. This made the check practical for much larger pipelines with SAT and BDD tools.
- **Completion functions.** Hosabettu, Srivas and Gopalakrishnan (1998) split the flush into one function per unfinished instruction, which says how that instruction would complete. The single large diagram becomes a chain of small lemmas.
- **Simulation relations.** The diagram is the condition for $\alpha$ to be a functional [simulation relation](/simulation-relation/) from the implementation to the specification, with the stall steps as stuttering steps.

## Variations

- **Several instructions per cycle.** A superscalar design can fetch $k$ instructions in a cycle. The right side then runs $k$ ISA steps, where $k$ comes from the implementation state.
- **Zero or one step, not known in advance.** If $\mathrm{fetched}$ is hard to state, check that the left side equals either $\alpha(q)$ or $\delta_S(\alpha(q), j)$. This is weaker and needs a separate check of progress.
- **Invariants.** Replace $Q$ by a set that contains the reachable states and is closed under $\delta_I$, an [inductive invariant](/inductive-invariant/). This removes false alarms from unreachable states at the cost of proving the invariant.
- **Bit level.** With small words and a real ALU, the check is a SAT or BDD problem, or a plain enumeration as in the tests. This needs no EUF and handles designs that rely on algebraic facts, but the cost grows with the width.
- **Equivalence of two pipelines.** Flushing both and comparing gives a check of one design against another, related to the [product machine](/product-machine/) used for sequential equivalence.

## Pitfalls

- **A pipeline that never fetches.** A design that stalls for ever makes the diagram commute with zero ISA steps in every cycle. The check proves safety only. Prove separately that the pipeline fetches within a bounded number of cycles.
- **False alarms from unreachable states.** The tests include a design whose bypass compares against a copy of $r_d$ stored in $P$. In every reachable state the copy equals $r_d$, and every program runs correctly. Over all states, a state where the copy differs makes the check fail. Add the invariant "copy equals $r_d$" or check reachable states only.
- **A flush that is itself wrong.** The abstraction uses the stall behavior of the design. If stall cycles drop an instruction in flight, the check compares against the wrong state. The correctness criterion is about flushed runs, so such a bug shows only if stalls also occur in normal runs. Make the stall input of the flush the same input that normal operation uses.
- **Algebraic facts.** A design that swaps the operands of ADD is correct, but $\mathrm{ADD}(a, b) = \mathrm{ADD}(b, a)$ is not valid in EUF, so the check fails. Add the axiom, or leave that operation interpreted.
- **The flush depth.** If $d$ is less than the number of cycles that the longest instruction needs to finish, $\alpha$ reads a register file with some writes missing, and the check fails on correct designs.

## Exercises

1. Add a stage to the example: fetch, read, execute, write. What is $d$, and which bypasses does the check require?
2. Give a design that fails the "zero or one step" check but passes the check with a known $\mathrm{fetched}$, or prove that none exists.
3. Show that a design that always stalls passes the diagram, and write a bounded progress property that rules it out.

## References
