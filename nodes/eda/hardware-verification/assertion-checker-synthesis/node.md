---
tag: SYM1QA
kind: technique
slug: assertion-checker-synthesis
name: Assertion checker synthesis
aliases:
- monitor synthesis from assertions
- assertion compilation to hardware
area: eda/hardware-verification
level: advanced
summary: Compiles temporal assertions into automata and then into synthesizable monitor circuits that run in simulation, emulation or silicon, as in Boule and Zilic's work.
prereqs: [assertion-based-verification, safety-property, nondeterministic-finite-automaton, subset-construction]
see_also: [deterministic-finite-automaton, dfa-minimization, regular-expression, thompson-construction, buchi-automaton, ltl-to-buchi-translation, invariant-checking, product-machine]
sources:
  - book: isbn:9781402085857
    title: Marc Boulé and Zeljko Zilic, Generating Hardware Assertion Checkers, For Hardware Verification, Emulation, Post-Fabrication Debugging and On-Line Monitoring, Springer, 2008
    locator: the automata for Booleans, sequences and properties, the encoding of automata as circuits, and the checkers for PSL and SVA (general locator)
  - paper: doi:10.1145/1297666.1297670
    title: Marc Boulé and Zeljko Zilic, Automata-based assertion-checker synthesis of PSL properties, ACM Transactions on Design Automation of Electronic Systems 13(1), article 4, 1 to 21, 2008
    locator: the automaton for each PSL operator, the treatment of weak and strong operators, and the circuit form of the automata
  - paper: doi:10.1023/A:1011254632723
    title: Orna Kupferman and Moshe Y. Vardi, Model checking of safety properties, Formal Methods in System Design 19(3), 291 to 314, 2001
    locator: bad prefixes, informative prefixes, and the size of automata that recognize them
  - paper: "IEEE Std 1800-2017, IEEE Standard for SystemVerilog, Unified Hardware Design, Specification, and Verification Language, IEEE, 2018"
    title: IEEE Standard for SystemVerilog, Unified Hardware Design, Specification, and Verification Language, IEEE Std 1800-2017
    locator: Clause 16 (sequences, the implication operators, weak and strong sequence properties, and the semantics of attempts)
---

Assertion checker synthesis turns a temporal assertion into a finite automaton and then into a small synchronous circuit, a *checker*, whose output `fail` goes to 1 in the clock cycle where the run of the design refutes the assertion. The checker reads the same signals as the assertion and needs no simulator, so it runs inside a simulator, in an emulator, on an FPGA prototype or on the chip itself. For the fragment `always (r |-> s)` with sequences `r` and `s`, this page builds the checker from an NFA for `r` and a DFA for `s`, and proves that it reports exactly the finite prefixes that refute some attempt. Every such prefix is a [bad prefix](/safety-property/), and under a condition on `s` every bad prefix is one.

## In plain words

An assertion such as "every request is granted within three cycles" is a rule over time. A checker is a small circuit that watches the signals and raises an alarm in the cycle where the rule breaks.

The rule has a trigger (a request) and an obligation (a grant soon after). A trigger can come in any cycle while older obligations still wait, so many attempts are open at once. The checker keeps flags for where the trigger pattern may be and flags for where the open obligations stand, and updates them each cycle with a few gates.

The trick is to track obligations with a machine that never guesses. Then two attempts in the same position have the same future, and one flag stands for both. With a machine that guesses, merging attempts can hide the death of one of them.

## When it applies

- The assertion is a [safety property](/safety-property/), or the part of it that a finite run can refute. A [liveness property](/liveness-property/) has no bad prefix, so no checker can flag its failure in finite time.
- The target is hardware or a cycle-based model: emulation, an FPGA prototype, post-silicon debug or on-line monitoring, where no simulator is present. A checker also gives a formal tool the property as a circuit: the assertion holds if and only if `fail` is never 1 on the [product](/product-machine/) of the design and the checker, an [invariant](/invariant-checking/).
- The operators are those that a finite automaton can express: Booleans, concatenation, union, repetition, and implications between sequences. This page treats the fragment below. Intersection adds a product of automata. Local variables of SVA carry data and need more than a finite automaton over the signal values.

## The template

**The fragment.** Let $AP$ be the signals and $\Sigma = 2^{AP}$ the letters, so a trace is $w = w_0 w_1 \ldots \in \Sigma^\omega$, and $w[i..j] = w_i \cdots w_j$. A Boolean $b$ matches the letter $a$ when $a \models b$. Sequences are built from Booleans by concatenation (`r ##1 r'`), union (`r or r'`) and repetition (`r[*m:n]`, `r[*1:$]`). A sequence $r$ denotes a regular language $L(r) \subseteq \Sigma^+$; the fragment requires $\varepsilon \notin L(r)$ and $L(s) \ne \emptyset$. The assertion is

$$ \varphi = \texttt{always } (r \mid\!\!\to s), $$

read with SVA semantics: the implication is overlapping and the consequent sequence is weak, which is the default in an `assert` statement. An **attempt** is a pair $(j, k)$ with $w[j..k] \in L(r)$; the consequent starts at cycle $k$. For a word $u \in \Sigma^*$, call $u$ **dead** when no prefix of $u$ is in $L(s)$ and $u$ is not a prefix of any word of $L(s)$. A suffix $v \in \Sigma^\omega$ **weakly satisfies** $s$ when some prefix of $v$ is in $L(s)$, or every finite prefix of $v$ is a prefix of a word of $L(s)$. Then $w \models \varphi$ when $w[k..]$ weakly satisfies $s$ for every attempt $(j, k)$.

**Step 1: an NFA for the antecedent.** Build an NFA $A_r = (Q, q_0, \Delta, F)$ without $\varepsilon$-moves whose transitions carry Booleans, for example by the [Thompson construction](/thompson-construction/) followed by $\varepsilon$-removal, or by the position automaton. For $X \subseteq Q$ let $\mathrm{Post}(X, a) = \{q' : (q, b, q') \in \Delta,\ q \in X,\ a \models b\}$.

**Step 2: a DFA for the consequent.** Build an $\varepsilon$-free NFA $A_s = (P, p_0, \Delta_s, F_s)$ for $s$. Remove the transitions whose Boolean is unsatisfiable, then remove the states from which no state of $F_s$ is reachable. Apply the [subset construction](/subset-construction/) to the trimmed NFA, with letters of $\Sigma$, and change it in two ways: a subset that meets $F_s$ becomes the sink $\top$ (the attempt succeeded), and the empty subset becomes the sink $\bot$ (the attempt is dead). Call the result $D_s$, with start state $d_0 = \{p_0\}$ and transition function $\delta$. [DFA minimization](/dfa-minimization/) may shrink it.

**Step 3: the checker.** The checker has a register $R \subseteq Q$ (one flip-flop per NFA state) and a register $S$ that holds a set of states of $D_s$ other than $\top$ and $\bot$ (one flip-flop per DFA state). Both start empty. In cycle $k$, with letter $a_k = w_k$:

```
R  := Post(R ∪ {q0}, a_k)                     -- antecedent matches in progress
m  := (R ∩ F ≠ ∅)                             -- a match of r ends at cycle k
S' := { δ(d, a_k) : d ∈ S ∪ ({d0} if m) }     -- step every open attempt
fail_k := (⊥ ∈ S')
S  := S' \ {⊤, ⊥}
```

In hardware, each flip-flop of $R$ and $S$ has a next-state function that is an OR of ANDs of flip-flops and Booleans, one term per transition. A reset clears both registers, which is what `disable iff` asks for.

**Why the consequent needs a DFA.** Two attempts in the same state of $D_s$ have the same future: whether and when each dies depends only on that state and on the letters to come. So one flip-flop can stand for both, and $S$ loses nothing that `fail` needs. Two attempts that share an NFA state do not have this property, because the NFA state of an attempt is not one state but a set. The antecedent can stay an NFA because $m$ asks only whether some match ends, and the union of the NFA sets answers exactly that.

### Why the checker is exact

**Lemma 1 (deadness is closed under extension).** If $u$ is dead, then $ux$ is dead for each letter $x$.

*Proof.* A prefix of $ux$ is a prefix of $u$ or $ux$ itself. No prefix of $u$ is in $L(s)$. If $ux \in L(s)$, then $u$ is a prefix of a word of $L(s)$, which is false. If $ux$ is a prefix of a word of $L(s)$, then so is $u$, which is false. $\square$

**Lemma 2.** $v$ weakly satisfies $s$ if and only if no finite prefix of $v$ is dead.

*Proof.* Suppose $v[0..i] \in L(s)$. A prefix longer than $i + 1$ letters has a prefix in $L(s)$, and a shorter one is a prefix of $v[0..i] \in L(s)$, so neither is dead. If every prefix of $v$ is a prefix of a word of $L(s)$, none is dead. Conversely, if no prefix is dead, then either some prefix has a prefix in $L(s)$, or every prefix is a prefix of a word of $L(s)$, and in both cases $v$ weakly satisfies $s$. $\square$

**Lemma 3 (the DFA).** For $u \in \Sigma^+$, the run of $D_s$ on $u$ ends in $\top$ if some prefix of $u$ is in $L(s)$, in $\bot$ if $u$ is dead, and otherwise in the set $X_u$ of trimmed-NFA states reachable from $p_0$ on $u$, which is not empty.

*Proof.* In the trimmed NFA each state reaches $F_s$ by transitions with satisfiable Booleans, so it reaches $F_s$ on some word. If $X_u \ne \emptyset$, pick $q \in X_u$ and a word $y$ that leads from $q$ to $F_s$; then $uy \in L(s)$. Conversely, if $uy \in L(s)$, every state of an accepting run reaches $F_s$ and every transition used has a satisfied Boolean, so the run survives the trimming and $X_u \ne \emptyset$. So $X_u \ne \emptyset$ exactly when $u$ is a prefix of a word of $L(s)$. A subset meets $F_s$ exactly when the word read so far is in $L(s)$. The sinks $\top$ and $\bot$ are entered at the first such event and never left. By induction on the length of $u$, the run ends in $\top$ when some prefix is in $L(s)$, and otherwise in $\bot$ exactly when $X_u = \emptyset$, which by the above is when $u$ is dead. $\square$

**Lemma 4 (the registers).** After cycle $k$: (a) $q \in R$ if and only if some $j \le k$ has a run of $A_r$ on $w[j..k]$ from $q_0$ to $q$, so $m = 1$ exactly when some attempt $(j, k)$ exists; (b) $S'$ is the set of states $\delta(d_0, w[k'..k])$ over the attempts $(j, k')$ with $k' \le k$ that are not dead and not in $\top$ after $w[k'..k-1]$ (all attempts with $k' = k$ count).

*Proof.* Induction on $k$. For (a), $R$ after cycle $k$ is $\mathrm{Post}(R_{k-1} \cup \{q_0\}, w_k)$, and the runs that end at $k$ are those that start at $k$ from $q_0$ or extend a run that ended at $k - 1$. For (b), the attempts that end before $k$ and are still open after $k - 1$ have their states in $S_{k-1}$ by the hypothesis and the line that removes $\top$ and $\bot$; each moves to $\delta(d, w_k)$. The new attempts are added through $d_0$ exactly when $m = 1$. Different attempts in the same state share one entry, which changes the set but not its elements. $\square$

**Theorem 1 (soundness and first detection).** $\mathit{fail}_k = 1$ if and only if some attempt $(j, k')$ with $k' \le k$ has $w[k'..k]$ dead and, when $k' < k$, $w[k'..k-1]$ not dead. Call $w[0..t]$ **refuting** when some attempt $(j, k')$ with $k' \le t$ has $w[k'..t]$ dead. Then the first cycle with $\mathit{fail} = 1$ is the least $t$ such that $w[0..t]$ is refuting; $w \not\models \varphi$ if and only if some prefix is refuting; and every refuting prefix is a bad prefix of $\varphi$.

*Proof.* The first claim is Lemma 4(b) with Lemma 3. A refuting prefix at $t$ comes from an attempt whose word first became dead at some $t' \le t$, and by Lemma 1 the word stays dead, so the least refuting $t$ is the first $t'$ with $\mathit{fail} = 1$. By Lemma 2, $w \not\models \varphi$ if and only if some attempt has a dead prefix $w[k'..t]$, that is, some prefix is refuting. If $w[0..t]$ is refuting through the attempt $(j, k')$, any infinite word $w'$ with prefix $w[0..t]$ has the same attempt and the same dead word $w'[k'..t]$, so $w' \not\models \varphi$. Hence $w[0..t]$ is a bad prefix. $\blacksquare$

**Theorem 2 (completeness for a universal letter).** Suppose some letter $\sigma^\star$ satisfies every Boolean that occurs in $s$. Then every bad prefix of $\varphi$ is refuting, so the checker reports the first bad prefix of each trace in the cycle where it ends.

*Proof.* Let $u = w[0..t]$ be a prefix that is not refuting, and let $w' = u \, (\sigma^\star)^\omega$. Write $s$ as a regular expression over its Boolean occurrences; a letter word is in $L(s)$ when it matches some word $\beta_1 \cdots \beta_n$ of Booleans of that expression letter by letter. Take an attempt $(j, k')$ of $w'$. If $k' > t$, then $w'[k'..] = (\sigma^\star)^\omega$, and $(\sigma^\star)^n$ matches any Boolean word of $s$ of length $n$, which exists since $L(s) \ne \emptyset$; so the suffix has a prefix in $L(s)$. If $k' \le t$, then $w[k'..t]$ is not dead because $u$ is not refuting. Either it has a prefix in $L(s)$, and we are done, or $w[k'..t] y \in L(s)$ for some $y$, matching a Boolean word $\beta_1 \cdots \beta_n$. Replace each letter of $y$ by $\sigma^\star$, which satisfies the same Booleans; then $w[k'..t] (\sigma^\star)^{|y|} \in L(s)$, a prefix of $w'[k'..]$. So $w' \models \varphi$, and $u$ is not a bad prefix. $\blacksquare$

The condition of Theorem 2 holds when $s$ uses only Booleans that one valuation can make true together, for example when every Boolean of $s$ is a positive signal. Without it the checker can be late, as the third example below shows. Prefixes that are bad by the letters they contain, not by an argument about all extensions, are what Kupferman and Vardi call *informative*; the refuting prefixes of this page play that role.

**Cost.** The antecedent register has at most $|Q|$ flip-flops, linear in the number of Boolean occurrences of $r$ for the position automaton. The consequent register has one flip-flop per state of $D_s$, at most $2^{|P|} + 2$ states before minimization. That bound comes from the subset construction; some sequences need many fewer, and bounded delays such as `##[1:n] b` give a chain of $n$ states. The logic per cycle is one AND term per transition. For general LTL safety formulas, Kupferman and Vardi give automata for the informative prefixes of size $2^{O(|\varphi|)}$, while their construction for exactly the bad prefixes is doubly exponential.

## Classic examples

**A bounded handshake.** `assert property (@(posedge clk) req |-> ##[1:3] gnt);` Here $r$ is the Boolean `req`, so $A_r$ has two states and $m = \mathit{req}_k$. The consequent read from cycle $k$ is "any letter, then `gnt` within the next 3 letters". $D_s$ has the states $d_0$, $d_1$, $d_2$, $d_3$, $\top$ and $\bot$: $d_0$ goes to $d_1$ on any letter, and $d_i$ goes to $\top$ on `gnt` and to $d_{i+1}$ otherwise, with $d_4 = \bot$. $d_0$ is never stored, so $S$ needs three flip-flops $q_1, q_2, q_3$ (state $d_i$ is open):

$$ q_1^{+} = \mathit{req}, \qquad q_2^{+} = q_1 \wedge \neg \mathit{gnt}, \qquad q_3^{+} = q_2 \wedge \neg \mathit{gnt}, \qquad \mathit{fail} = q_3 \wedge \neg \mathit{gnt}. $$

Run it with `req` at cycles 1, 2 and 5 and `gnt` at cycle 3. The columns $q_1 q_2 q_3$ show the register after the cycle.

| cycle | req | gnt | $q_1 q_2 q_3$ | fail |
|---|---|---|---|---|
| 0 | 0 | 0 | 000 | 0 |
| 1 | 1 | 0 | 100 | 0 |
| 2 | 1 | 0 | 110 | 0 |
| 3 | 0 | 1 | 000 | 0 |
| 4 | 0 | 0 | 000 | 0 |
| 5 | 1 | 0 | 100 | 0 |
| 6 | 0 | 0 | 010 | 0 |
| 7 | 0 | 0 | 001 | 0 |
| 8 | 0 | 0 | 000 | 1 |

At cycle 2, flip-flop $q_1$ holds the attempt of cycle 2 and $q_2$ the attempt of cycle 1. The grant at cycle 3 closes both. The attempt of cycle 5 dies at cycle 8. The letter $\{\mathit{gnt}\}$ satisfies every Boolean of $s$, so by Theorem 2 the prefix $w[0..8]$ is the first bad prefix: after cycle 7, a grant at cycle 8 could still save the run.

**Why an NFA for the consequent is wrong.** Take $r = \texttt{true}$ and $s = $ `a ##1 b`, so every cycle starts an attempt, and the run $\{a\}\{a\}$. The NFA for $s$ is $p_0 \xrightarrow{a} p_1 \xrightarrow{b} p_2$ with $p_2$ final. A checker that keeps one union $U$ of NFA states over all attempts gets $U = \{p_1\}$ after cycle 0, and after cycle 1 gets $\mathrm{Post}(\{p_1\} \cup \{p_0\}, \{a\}) = \{p_1\}$. $U$ is not empty, so it reports nothing. But the attempt of cycle 0 needed $b$ at cycle 1 and is dead. With $D_s$, that attempt is in the state $\{p_1\}$, which goes to $\bot$ on $\{a\}$, and `fail` is 1 at cycle 1.

**A late report.** Take `always (b ##1 !b)`, that is $r = \texttt{true}$ and $s = $ `b ##1 !b`, and a run that starts with $\{b\}$. The attempt of cycle 0 needs $\neg b$ at cycle 1 and the attempt of cycle 1 needs $b$ at cycle 1, so every extension fails, and $w[0..0]$ is already a bad prefix. No attempt is dead after cycle 0, so the checker reports at cycle 1, one cycle late. No letter satisfies both $b$ and $\neg b$, so Theorem 2 does not apply. The report is still sound, and it arrives as soon as a single attempt is dead.

**A sequence antecedent.** For `start ##1 busy[*1:$] ##1 done |-> ##1 ack`, $A_r$ has the states $q_0$, $q_1$ (after `start`), $q_2$ (after one or more `busy`) and $q_3$ (after `done`, final), with the loop $q_2 \xrightarrow{busy} q_2$. The register $R$ needs three flip-flops for $q_1, q_2, q_3$, however many matches overlap, and $m$ is the new value of $q_3$. The consequent is "any letter, then `ack`". Its state $d_0$ is never stored, so $S$ needs one flip-flop, set when $m = 1$, and `fail` is that flip-flop AND NOT `ack`.

## Variations

- **Non-overlapping implication.** `r |=> s` equals `r ##1 true |-> s`, so it adds one state to $A_r$.
- **Strong consequents and the end of a run.** For a strong sequence, an attempt still open when the run ends is a failure. The checker raises an end-of-test signal when $S \ne \emptyset$ at the last cycle. This reports an obligation, not a bad prefix.
- **Cover goals.** `cover property (s)` needs only the NFA of $s$ with a new start in every cycle, as for the antecedent: the goal is hit when $R \cap F \ne \emptyset$. No subset construction is needed, since cover asks whether some match exists.
- **Per-attempt copies.** When every word of $L(s)$ that matters has at most $n$ letters, at most $n$ attempts are open at once. Keeping $n$ copies of the NFA state set, one per open attempt, costs $n \, |P|$ flip-flops and avoids the subset construction. Which form is smaller depends on $s$.
- **Full PSL and SVA.** Boulé and Zilic give automata for the full set of PSL operators, weak and strong, and for SVA, with rewrite rules that reduce operators to a small core. The checker of this page is a special case of that approach; the details of their construction differ.
- **Formal use.** The product of the design and the checker turns the assertion into the invariant $\mathsf{G}\,\neg\mathit{fail}$, which [bounded model checking](/bounded-model-checking/), [k-induction](/k-induction/) or [IC3](/ic3-pdr/) can check. For LTL in general, the route is [LTL to Büchi translation](/ltl-to-buchi-translation/), and the checker is an automaton for (informative) bad prefixes.

## Pitfalls

- **Merging attempts in an NFA.** One union of NFA states for all attempts of the consequent misses failures, as the second example shows. Determinize the consequent, or keep one copy per attempt.
- **Assuming the report is at the first bad prefix.** It is at the first refuting prefix. Without the condition of Theorem 2, the checker can be one or more cycles late, as in `always (b ##1 !b)`. Soundness is not affected.
- **Vacuous runs.** A checker whose antecedent never matches never fires. Count antecedent matches, or add a cover goal on `r`.
- **Empty matches.** A sequence that can match the empty word, such as `a[*0:2]`, changes the meaning of the implication. The fragment here excludes it. Treat it by the rules of the standard, not by the template above.
- **Sampling and reset.** The checker must read the values that the assertion semantics samples, the values before the clock edge, and must clear its registers on the reset of `disable iff`. A checker that reads values after the edge reports a different property.
- **Size.** The subset construction can blow up. Minimize the DFA, use per-attempt copies, or split a large consequent into several assertions.
- **Liveness.** No finite checker refutes `s_eventually gnt` in finite time. Bounded versions such as `##[1:1000] gnt` are safety properties, but they state a different requirement.

## Exercises

1. Build the checker for `a ##1 b |-> ##1 c`. Give the flip-flops of $R$ and $S$ and their next-state functions, and run it on the letters $\{a\}\{b\}\{a\}\{b\}\{\,\}$.
2. Show that `r |=> s` and `r ##1 true |-> s` have the same attempts, each one cycle later, and the same failures.
3. Prove that the union of NFA states is exact for the antecedent: $R \cap F \ne \emptyset$ after cycle $k$ if and only if some $w[j..k] \in L(r)$.
4. For `always (b ##1 !b)`, give the first bad prefix and the first refuting prefix of the run $\{b\}\{b\}\{\,\}$.
5. For `req |-> ##[1:n] gnt`, show that $D_s$ minimized has $n + 3$ states and that the checker needs $n$ flip-flops, however many requests overlap.

## References
