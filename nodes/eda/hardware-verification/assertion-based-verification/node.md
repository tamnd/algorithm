---
tag: 3R99EC
kind: concept
slug: assertion-based-verification
name: Assertion-based verification
aliases:
- ABV
- assertion-based design
area: eda/hardware-verification
level: core
summary: Writes design intent as temporal assertions in a language such as PSL or SVA and checks them in simulation, emulation and formal tools.
prereqs: [linear-temporal-logic, safety-property]
see_also: [assertion-checker-synthesis, functional-coverage, constrained-random-stimulus-generation, liveness-property, invariant-checking, bounded-model-checking, ltl-model-checking, sequential-equivalence-checking]
sources:
  - paper: "IEEE Std 1850-2010, IEEE Standard for Property Specification Language (PSL), IEEE, 2010"
    title: IEEE Standard for Property Specification Language (PSL), IEEE Std 1850-2010 (first edition IEEE Std 1850-2005)
    locator: the Boolean, temporal, verification and modeling layers; the directives assert, assume and cover; weak and strong operators and the semantics on finite and truncated paths
  - paper: "IEEE Std 1800-2017, IEEE Standard for SystemVerilog, Unified Hardware Design, Specification, and Verification Language, IEEE, 2018"
    title: IEEE Standard for SystemVerilog, Unified Hardware Design, Specification, and Verification Language, IEEE Std 1800-2017
    locator: Clause 16 (Assertions, with sequences, properties, implication, sampling and the assert, assume and cover statements) and Clause 17 (Checkers)
  - book: isbn:9780387353135
    title: Cindy Eisner and Dana Fisman, A Practical Introduction to PSL, Springer, 2006
    locator: the chapters on the temporal layer, on weak and strong operators, on SEREs and suffix implication, and on the verification layer (general locator)
  - book: isbn:9781402080272
    title: Harry D. Foster, Adam C. Krolnik and David J. Lacey, Assertion-Based Design, second edition, Kluwer, 2004
    locator: the methodology chapters on where to put assertions, assertion density and assertions at block interfaces (general locator)
  - paper: doi:10.1023/A:1011254632723
    title: Orna Kupferman and Moshe Y. Vardi, Model checking of safety properties, Formal Methods in System Design 19(3), 291 to 314, 2001
    locator: bad prefixes and informative prefixes of safety formulas, and automata that recognize them
---

Assertion-based verification (ABV) is a way to check a hardware design against its intended behavior written as *assertions*: formulas of a [linear temporal logic](/linear-temporal-logic/) over the clock cycles of the design, extended with regular expressions over cycles. The two standard languages are PSL (IEEE Std 1850) and SystemVerilog Assertions, or SVA (Clause 16 of IEEE Std 1800). A simulator turns each assertion into a monitor that reports the first cycle at which the run breaks it, an emulator does the same in hardware, and a formal tool tries to prove that no input sequence breaks it. The same languages also state what the environment may do (assumptions) and which scenarios a run must reach (cover goals).

## In plain words

A designer knows rules that the hardware must always follow: a request gets a grant within three clock cycles, two units never own the bus at the same time, a full buffer never takes another item. Assertion-based verification writes such rules down in a special language, next to the design, and lets tools check them. A simulator watches every rule on every clock cycle and stops at the first cycle where a rule breaks, at the place where the bug acts. A formal tool tries to prove that no input sequence at all can break the rule. The same text also says what the inputs are allowed to do, and which interesting cases a run should reach. The method finds bugs earlier and closer to their cause than a check of the outputs alone. It only checks the rules that someone wrote, so a missing rule hides a bug.

## The idea

**Traces.** Fix a clock. Let $AP$ be the set of design signals that the assertions mention. A run of the design gives a *trace* $w = w_0 w_1 w_2 \ldots$, where $w_k \subseteq AP$ is the set of signals that are true at the $k$-th clock edge. A design $M$ (a finite state machine, or a [Kripke structure](/kripke-structure/) after unrolling its inputs) defines the set $\mathit{Tr}(M)$ of its infinite traces from reset. A property $\varphi$ defines a set $L(\varphi)$ of infinite traces.

**The three directives.** PSL and SVA attach one of three directives to a property.

- `assert` $\varphi$: every trace of $M$ that the assumptions allow is in $L(\varphi)$.
- `assume` $\psi$: only the traces in $L(\psi)$ count. A formal tool checks $\mathit{Tr}(M) \cap L(\psi) \subseteq L(\varphi)$. A simulator either checks $\psi$ like an assertion on the inputs, or gives it to the stimulus generator as a constraint (see [constrained random stimulus generation](/constrained-random-stimulus-generation/)).
- `cover` $s$: some allowed trace contains a match of the sequence $s$. Here the tool wants a witness, not a proof of absence. Cover goals are one source of [functional coverage](/functional-coverage/).

**Layers of the language.** Both languages have a Boolean layer (expressions over signals at one clock edge), a sequence layer (regular expressions over cycles, called SEREs in PSL and sequences in SVA, with concatenation `##1`, delay ranges `##[1:3]` and repetition `[*m:n]`), a property layer (implication, `always`, `until`, `eventually` and their strong forms) and the directives. The suffix implication `r |-> p` of SVA (`{r} |-> p` in PSL) says: at every cycle where a match of the sequence `r` ends, the property `p` holds from that cycle. `r |=> p` starts `p` one cycle later. A clock and a reset are part of each assertion: `@(posedge clk) disable iff (rst)` in SVA. SVA samples the signals of a concurrent assertion in the Preponed region of the time step, before the clock edge updates the design, so an assertion sees the values that were stable before the edge.

**Finite runs.** A simulation run is a finite trace $u = w_0 \cdots w_t$. It can show that an assertion fails, but never that it holds on all traces. For a [safety property](/safety-property/), every failing infinite trace has a finite bad prefix, so a failure always shows in finite time. A checker built from the formula reports some bad prefixes at once and others one or more cycles later (the details and the proof are on [assertion checker synthesis](/assertion-checker-synthesis/)). A [liveness property](/liveness-property/) such as "every request is granted some time" has no bad prefix, so no finite run refutes it. PSL marks strong operators with `!` (`eventually!`, `until!`, `next!`) and SVA writes `s_eventually`, `s_until` and so on: at the end of a run, an obligation of a strong operator that is still open counts as a failure, while a weak operator lets it pass. This is a convention for truncated runs, not a proof.

**Formal checking.** A formal tool decides $M \models \varphi$ under the assumptions. For a safety assertion, it builds a checker automaton for the bad prefixes, forms the product with the design, and checks the invariant "the checker never fails" by [invariant checking](/invariant-checking/), [bounded model checking](/bounded-model-checking/), [k-induction](/k-induction/) or [IC3](/ic3-pdr/). For a liveness assertion it uses a [Büchi automaton](/buchi-automaton/) and [LTL model checking](/ltl-model-checking/). Formal tools usually work on one block, with assumptions on its inputs. An assumption of one block is then an assertion of the block that drives it, which closes the argument in an assume-guarantee style.

**Vacuity.** An implication `r |-> p` holds at every cycle where `r` does not match. If `r` never matches in a run, or in any trace of the design, the assertion passes for no useful reason. This is *vacuous* success. Tools report it, and a common rule is to add `cover property (r)` for each antecedent.

**What an assertion buys and what it does not.** An assertion inside a block fires at the cycle and the place where a bug first breaks a rule, while an output check sees the effect only when it reaches an output, maybe much later or never. This is an observability argument, not a theorem: the gain is measured on designs, and depends on where the assertions are and on how many there are. An assertion checks only what it says. A design with no failing assertion can still be wrong, and the set of assertions is itself a model of the specification that can have holes, in the same way as a coverage model.

## Examples

**A bounded handshake.** "Each request gets a grant within 1 to 3 cycles":

```
assert property (@(posedge clk) disable iff (rst) req |-> ##[1:3] gnt);   // SVA
assert always (req -> next_e[1..3] (gnt)) @(rising_edge(clk));          -- PSL
```

Take a run with `req` true at cycles 1, 2 and 5, and `gnt` true only at cycle 3. The requests of cycles 1 and 2 are both granted at cycle 3. The request of cycle 5 needs a grant at cycle 6, 7 or 8. There is none, so the checker reports a failure at cycle 8, and the prefix $w_0 \cdots w_8$ is a bad prefix. The three-register checker that does this is worked out on [assertion checker synthesis](/assertion-checker-synthesis/).

**Mutual exclusion.** `assert property (@(posedge clk) $onehot0(gnt_vec));` says that at most one bit of the grant vector is 1 at each edge. It is an invariant $\mathsf{G}\,p$ with $p$ a Boolean expression, the simplest safety property.

**Assert, assume and cover on one FIFO.** For a FIFO with depth 4:

- `assume property (@(posedge clk) !(push && full));` says that the producer never pushes into a full FIFO. It restricts the inputs.
- `assert property (@(posedge clk) count <= 4);` and `assert property (@(posedge clk) full == (count == 4));` state what the FIFO guarantees.
- `cover property (@(posedge clk) full ##1 pop ##1 push);` asks for a run that fills the FIFO, removes one item and adds one again.

A formal tool proves the two assertions for every input sequence that obeys the assumption. In simulation the assumption is checked on the producer, so a producer that breaks the protocol is caught at its source.

**Vacuous success.** If a test never raises `req`, the handshake assertion passes in every cycle. The cover goal `cover property (@(posedge clk) req)` stays unhit and shows that the pass means nothing.

**A liveness assertion.** `assert property (@(posedge clk) req |-> s_eventually gnt);` cannot fail at any finite cycle. A simulation that ends with an open request reports that obligation as failed only because `s_eventually` is strong. A formal tool proves or refutes the property with a Büchi automaton and fairness on the environment.

**Non-example.** A scoreboard that compares the outputs of the design with a reference model checks the same design, but it is not an assertion: it is a test bench component that sees only the outputs, and a formal tool cannot use it as a property without a model of the reference. [Sequential equivalence checking](/sequential-equivalence-checking/) compares two designs on all inputs, and ABV compares one design with a set of properties.

## Where it is used

- **Simulation.** Simulators compile assertions into monitors that run in every cycle. A failure gives the assertion, the cycle and the trace, which shortens debugging. Assertions on block interfaces also check the test bench.
- **Formal property checking.** The same assertions are the input of model checkers: safety assertions by invariant checking on the product of the design and the checker, liveness assertions by LTL model checking. Assumptions bound the inputs.
- **Emulation, prototypes and silicon.** Assertions compiled into hardware checkers run in an emulator, on an FPGA prototype or on a chip for debug and on-line monitoring. The construction and its exactness are on [assertion checker synthesis](/assertion-checker-synthesis/).
- **Stimulus and coverage.** Assumptions give the constraints of a [constrained random](/constrained-random-stimulus-generation/) generator, and cover goals give items of [functional coverage](/functional-coverage/). Both measure and steer a simulation, and neither proves anything about the traces that were not run.
- **Protocol checkers.** A set of assertions for a bus protocol is written once and reused in each design that uses the bus, on both sides of the interface.

## References
