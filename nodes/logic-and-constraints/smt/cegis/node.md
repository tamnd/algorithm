---
tag: P1YF3Y
kind: algorithm
slug: cegis
name: Counterexample-guided inductive synthesis
aliases:
- CEGIS
- counterexample-guided synthesis
area: logic-and-constraints/smt
level: research
summary: Alternate between synthesizing a candidate from examples and a verifier that returns counterexamples.
solves: [syntax-guided-synthesis]
properties: {deterministic: true, exact: true, incremental: true}
history:
  year: 2006
  people: [Armando Solar-Lezama, Liviu Tancau, Rastislav Bodík, Sanjit A. Seshia, Vijay Saraswat]
  note: Introduced with program sketching at ASPLOS 2006, where a SAT solver fills the holes of a sketch from a growing set of test inputs.
prereqs: [smt-problem, syntax-guided-synthesis]
see_also: [cegar, quantifier-instantiation, incremental-solving, bit-blasting, inductive-invariant, dfa-learning, bounded-model-checking, maxsmt]
sources:
  - paper: doi:10.1145/1168857.1168907
    title: Armando Solar-Lezama, Liviu Tancau, Rastislav Bodík, Sanjit Seshia and Vijay Saraswat, Combinatorial sketching for finite programs, Architectural Support for Programming Languages and Operating Systems (ASPLOS 2006)
    locator: the sketch language, the reduction of hole filling to an exists-forall problem, and the counterexample-driven loop over inputs
  - paper: "Armando Solar-Lezama, Program synthesis by sketching, PhD thesis, University of California, Berkeley, 2008"
    locator: the chapter on CEGIS, with the name, the loop and its use with a SAT solver
  - paper: doi:10.1109/FMCAD.2013.6679385
    title: Rajeev Alur, Rastislav Bodík, Garvit Juniwal, Milo M. K. Martin, Mukund Raghothaman, Sanjit A. Seshia, Rishabh Singh, Armando Solar-Lezama, Emina Torlak and Abhishek Udupa, Syntax-guided synthesis, Formal Methods in Computer-Aided Design (FMCAD 2013)
    locator: CEGIS as the common frame of the enumerative, symbolic and stochastic SyGuS solvers
  - paper: "Susmit Jha, Sumit Gulwani, Sanjit A. Seshia and Ashish Tiwari, Oracle-guided component-based program synthesis, International Conference on Software Engineering (ICSE 2010)"
    locator: synthesis from components with an input-output oracle and distinguishing inputs (to be checked)
  - paper: "Susmit Jha and Sanjit A. Seshia, A theory of formal synthesis via inductive learning, Acta Informatica 54(7) (2017)"
    locator: the conditions under which CEGIS stops over infinite domains, and variants with different counterexamples (to be checked)
  - paper: "Alessandro Abate, Cristina David, Pascal Kesseli, Daniel Kroening and Elizabeth Polgreen, Counterexample guided inductive synthesis modulo theories, Computer Aided Verification (CAV 2018)"
    locator: CEGIS(T), where the synthesizer leaves constants symbolic and a theory solver finds them (to be checked)
---

Counterexample-guided inductive synthesis (CEGIS) finds a program $c$ in a space of candidates that satisfies a specification for every input, $\exists c\, \forall x\, \varphi(x, c)$, by a loop between two solvers. The *synthesizer* finds a candidate that is correct on a finite set of example inputs; the *verifier* checks the candidate on all inputs and, if it is wrong, returns one input where it fails, which becomes a new example. Each solver call has only one quantifier, so a SAT or [SMT](/smt-problem/) solver can answer it. CEGIS is the usual algorithm for [syntax-guided synthesis](/syntax-guided-synthesis/): the SyGuS page states the problem (a grammar and a logical specification) and its undecidability, and this page is the loop, its proof and its cost. It stops whenever the candidate space or the input space is finite, and it may run forever otherwise.

## In plain words

We want a small program that gives the right answer for every input. Checking all inputs at once is hard, so we work with a short list of test inputs.

First, a solver finds a program that is right on the tests in the list. Then a second solver tries to break this program: it looks for any input where the answer is wrong. If it finds none, we are done. If it finds one, we add that input to the list and ask for a new program.

Each new test removes the last program and maybe many others. If there are only finitely many programs, or finitely many inputs, the loop must end. The list usually stays short, because a few well-chosen tests rule out most wrong programs.

## The problem

The input is a set $C$ of candidates (for example the ways to fill the holes of a program sketch, or the terms of a grammar up to a size), a set $X$ of inputs, and a specification $\varphi(x, c)$, read as "candidate $c$ is correct on input $x$". In the implementation, $\varphi(x, c)$ is $\mathrm{spec}(x, \mathrm{run}(c, x))$, which allows relational specifications with more than one correct output. The output is a $c \in C$ with $\varphi(x, c)$ for all $x \in X$, or the answer that no such candidate exists. This is the semantic core of [syntax-guided synthesis](/syntax-guided-synthesis/), with $C$ the language of the grammar.

## The algorithm

```pseudo id=main
CEGIS(C, X, φ)                    ▷ C: candidates, X: inputs, φ(x, c): c is correct on x
L1  E ← E₀                         ▷ initial examples, often ∅
L2  loop
L3      c ← SYNTH(E): some c ∈ C with φ(x, c) for all x ∈ E
L4      if there is no such c then return NONE
L5      x ← VERIFY(c): some x ∈ X with ¬φ(x, c)
L6      if there is no such x then return c
L7      E ← E ∪ {x}
```

**The synthesizer (line L3).** It solves $\exists c \bigwedge_{x \in E} \varphi(x, c)$, a formula with one copy of $\varphi$ for each example and no universal quantifier. With a sketch whose holes are bit-vectors, this is a [bit-vector](/bit-vector-satisfiability/) formula that a SAT solver handles after [bit-blasting](/bit-blasting/). The solver can be [incremental](/incremental-solving/): line L7 only adds a conjunct.

**The verifier (line L5).** It solves $\exists x\, \neg \varphi(x, c)$ for the fixed candidate $c$, which is a plain SMT query. A model is a counterexample; unsatisfiability proves that $c$ is correct for all inputs.

**The implementation** uses simple scans for the two oracles: the synthesizer returns the first candidate in a fixed list that is correct on all examples, and the verifier returns the first failing input. Both can be replaced by solver calls. The tests check every returned program against brute force over the whole input space.

## Example

Fill the holes $h_1, h_2$ of the 4-bit sketch $(x + h_1) \mathbin{\&} h_2$ so that it rounds $x$ up to a multiple of 4, modulo 16: the specification is $y = 4 \lceil x/4 \rceil \bmod 16$. The candidates are the 256 pairs $(h_1, h_2)$, scanned with $h_1$ first; the inputs are $0, \ldots, 15$.

| round | examples $E$ | candidate (line L3) | counterexample (line L5) | why it fails |
|---|---|---|---|---|
| 1 | none | $(0, 0)$: $x \mathbin{\&} 0$ | $x = 1$ | gives 0, needs 4 |
| 2 | $\{1\}$ | $(3, 4)$: $(x + 3) \mathbin{\&} 4$ | $x = 5$ | gives $8 \mathbin{\&} 4 = 0$, needs 8 |
| 3 | $\{1, 5\}$ | $(3, 12)$: $(x + 3) \mathbin{\&} 12$ | none | correct on all 16 inputs |

In round 2, no $h_1 \le 2$ works for $x = 1$: $(1 + h_1) \le 3$, and a number at most 3 has no bit 2, so it cannot give 4 after the mask. In round 3, the example $x = 5$ needs bit 3 in $h_2$, and $x = 1$ needs bit 2; $h_2 = 12$ is the first such mask. Two examples out of 16 inputs fixed the program. A brute-force check confirms that $(3, 12)$ is the only correct pair.

If the specification is $y = x + 1$ and the sketch is $x \mathbin{\&} h$, the loop returns NONE after two rounds: the first candidate fails on $x = 0$, and no mask gives $0 \mathbin{\&} h = 1$.

## Correctness

The two oracles have contracts: line L3 returns a candidate consistent with $E$, or nothing only if none exists; line L5 returns a failing input, or nothing only if $c$ is correct.

- **Soundness.** A candidate returned at line L6 passed the verifier, so it is correct. NONE at line L4 means that no candidate is consistent with the examples, and a correct candidate is consistent with all examples, so none exists.
- **Progress.** The candidate $c$ of line L3 is correct on all of $E$, and the counterexample $x$ is an input where it fails. So $x$ is a new example, and $c$ is not consistent with $E \cup \{x\}$: each round removes at least one candidate and adds one new input.
- **Termination.** If $C$ is finite, at most $|C|$ rounds can remove a candidate; if $X$ is finite, at most $|X|$ rounds can add an input. So the loop stops within $\min(|C|, |X|) + 1$ rounds.

The full proof, and an example where the loop runs forever when both spaces are infinite, are in the proof file.

## Complexity

- **Rounds.** At most $\min(|C|, |X|) + 1$, and this is tight in the worst case. Take the specification "output 0", inputs $X$, and candidates $c_a$ for $a \in X$ that output 1 on $a$ only, listed before the constant 0 program. Each round removes one $c_a$, so the loop takes $|X| + 1$ rounds. In practice the number of rounds is small, often below ten, because each counterexample removes many candidates at once.
- **Cost per round.** The synthesizer query has $|E|$ copies of $\varphi$, so it grows linearly with the round number; the verifier query has one copy. Each query is NP-hard for bit-vector or Boolean $\varphi$.
- **Overall.** For Boolean candidates and inputs, $\exists c\, \forall x\, \varphi$ is the 2QBF problem, complete for the second level $\Sigma_2^p$ of the polynomial hierarchy, so a polynomial bound on the rounds is not expected. CEGIS trades one hard quantified query for a sequence of quantifier-free ones.
- **Space.** The example set and one solver instance for each oracle.

## Properties

- **Sound always.** Each answer is correct, even when the spaces are infinite and the loop is stopped by a time limit.
- **Complete for finite spaces.** Finite candidate spaces include sketches with bit-vector holes and grammars bounded by size.
- **Order of results.** With the scanning synthesizer of the implementation, the result is the first correct candidate in the list, which gives a way to prefer small programs.
- **Black-box oracles.** The loop uses the solvers only through their contracts, so any SMT solver, enumerator or test harness can play either role.
- **Incremental.** Examples only grow, so the synthesizer can keep its learned clauses between rounds.

## Variants and improvements

- **Enumerative CEGIS.** The synthesizer enumerates the terms of a grammar by size and keeps only one term for each behaviour on the current examples (observational equivalence); this is the strongest method in many SyGuS competitions.
- **CEGIS(T)** (Abate et al. 2018). The synthesizer keeps constants symbolic and asks a theory solver for their values, which helps when the program needs large constants.
- **Oracle-guided synthesis** (Jha et al. 2010). When no full specification exists, an oracle gives the correct output for each distinguishing input, an input where two consistent candidates differ.
- **ICE learning.** For [inductive invariants](/inductive-invariant/), counterexamples are positive examples, negative examples and implications between states.
- **Comparison with [CEGAR](/cegar/).** CEGAR checks a property of one system and refines an abstraction after a spurious counterexample; CEGIS searches for a program and refines a set of examples. Both are loops between a cheap approximate check and an exact check.
- **Exists-forall solving.** SMT solvers solve $\exists \forall$ formulas with a similar loop of model-based [quantifier instantiation](/quantifier-instantiation/), and 2QBF solvers use the same idea.
- **Learning with equivalence queries.** Angluin's algorithm for [DFA learning](/dfa-learning/) has the same shape: a hypothesis, an equivalence query, and a counterexample that refines the hypothesis.

## When to use it

Use CEGIS when a candidate is easy to check on one input, the specification is a formula that a solver can refute, and the candidate space is finite or ordered by size. Typical cases are filling holes in a program sketch, finding constants of a controller, superoptimization of short instruction sequences, and synthesis of invariants. When the specification only gives input-output examples, the verifier is a test against those examples, and plain programming by example is enough. When candidates and inputs are both infinite, bound one of them (for example the size of the program), or use a method with a stronger termination argument.

## Pitfalls

- **Storing only the last counterexample.** Wrong: line L7 as $E \leftarrow \{x\}$. Two wrong candidates can then return in turn forever. Right: $E \leftarrow E \cup \{x\}$, which makes Lemma 2 of the proof work.
- **A verifier that checks only the examples.** Wrong: line L5 searches $E$ for a failure. It never finds one, since line L3 chose $c$ to fit $E$. Right: line L5 searches the whole input space $X$.
- **Storing the expected output with the counterexample.** Wrong: for a relational specification, add the pair $(x, y)$ with one correct output $y$ and ask line L3 for $\mathrm{run}(c, x) = y$. This removes correct programs that give another correct output. Right: store only $x$ and check $\varphi(x, c)$ again in line L3.
- **Treating "unknown" as "unsatisfiable".** Wrong: a time-out of the verifier at line L6 taken as "no counterexample". The returned program may be wrong. Right: return only after a real proof of unsatisfiability, and report "unknown" otherwise.
- **Reading NONE as "no program exists".** Wrong: line L4 taken as unrealizability of the full problem. It only says that no candidate of $C$ works, for example none up to the chosen size. Right: grow $C$, for example the size bound, and run again.

## Implementations

## History

Solar-Lezama, Tancau, Bodík, Seshia and Saraswat introduced the loop in 2006 for the SKETCH system, where a programmer writes a program with holes and a SAT solver fills them; the name CEGIS comes from Solar-Lezama's thesis of 2008. Jha, Gulwani, Seshia and Tiwari used a similar loop with an input-output oracle in 2010. Alur and others defined syntax-guided synthesis in 2013 with CEGIS as the common frame of its solvers, and the yearly SyGuS competition followed. Jha and Seshia (2017) studied when the loop stops on infinite domains, and Abate and others (2018) combined it with theory solvers for constants.

## Exercises

1. Run the example with the candidates scanned with $h_2$ first. Which counterexamples appear?
2. In the worst-case family above, the verifier returns the only failing input in each round. Show that no verifier can do better on that family, and that a different order of candidates needs only one round.
3. Give a finite candidate space and an infinite input space where CEGIS needs $|C|$ rounds.
4. Write the synthesizer query of round 3 of the example as a bit-vector formula.

## References
