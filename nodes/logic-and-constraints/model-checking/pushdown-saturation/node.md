---
tag: KE52MW
kind: algorithm
slug: pushdown-saturation
name: Pre-star and post-star saturation
aliases:
- Pre* and post* algorithms
- Saturation for pushdown systems
- Bouajjani-Esparza-Maler saturation
area: logic-and-constraints/model-checking
level: research
summary: Compute the predecessors or successors of a regular set of pushdown configurations by adding transitions to a finite automaton until nothing changes. Pre* takes O(q^2 r) time.
solves: [pushdown-reachability]
model: word-ram
complexity:
  vars: {q: the number of states of the automaton, r: the number of rules, t: the number of transitions of the input automaton}
  time: {worst: O(q^2 r + t)}
  space: {extra: O(q r + t)}
properties: {deterministic: true, recursive: false}
history:
  year: 1997
  people: [Ahmed Bouajjani, Javier Esparza, Oded Maler]
  note: Bouajjani, Esparza and Maler gave the saturation procedures at CONCUR 1997, and Finkel, Willems and Wolper gave a similar one the same year. Esparza, Hansel, Rossmanith and Schwoon made them efficient in 2000.
prereqs: [pushdown-system, nondeterministic-finite-automaton]
see_also: [pushdown-reachability, cfl-reachability, regular-language, ltl-model-checking, fixed-point, symbolic-reachability]
sources:
  - paper: "Ahmed Bouajjani, Javier Esparza and Oded Maler, Reachability analysis of pushdown automata: application to model-checking, CONCUR 1997, Lecture Notes in Computer Science 1243, Springer, pages 135 to 150"
    title: "Reachability analysis of pushdown automata: application to model-checking"
    locator: P-automata, the saturation rules for pre* and post*, and their correctness proofs
  - paper: "Javier Esparza, David Hansel, Peter Rossmanith and Stefan Schwoon, Efficient algorithms for model checking pushdown systems, CAV 2000, Lecture Notes in Computer Science 1855, Springer, pages 232 to 247"
    title: Efficient algorithms for model checking pushdown systems
    locator: the worklist algorithms for pre* and post*, the derived rules, and their time and space bounds
  - paper: "Stefan Schwoon, Model-checking pushdown systems, PhD thesis, Technische Universität München, 2002"
    title: Model-checking pushdown systems
    locator: the chapter on the reachability algorithms, with full proofs, and the witness generation
  - paper: "Alain Finkel, Bernard Willems and Pierre Wolper, A direct symbolic approach to model checking pushdown systems, INFINITY 1997, Electronic Notes in Theoretical Computer Science 9"
    title: A direct symbolic approach to model checking pushdown systems
    locator: the independent saturation procedure for post*
  - paper: "J. Richard Büchi, Regular canonical systems, Archiv für mathematische Logik und Grundlagenforschung 6, 1964, pages 91 to 111"
    title: Regular canonical systems
    locator: the regularity of the sets of words derivable in prefix rewriting systems
  - paper: "Thomas Reps, Stefan Schwoon, Somesh Jha and David Melski, Weighted pushdown systems and their application to interprocedural dataflow analysis, Science of Computer Programming 58(1-2), 2005"
    title: Weighted pushdown systems and their application to interprocedural dataflow analysis
    locator: the extension of pre* and post* saturation to weights from a bounded idempotent semiring
---

*Saturation* computes, for a [pushdown system](/pushdown-system/) and a regular set $C$ of configurations given by a finite automaton, an automaton for $\mathrm{pre}^*(C)$, the configurations that can reach $C$, or for $\mathrm{post}^*(C)$, the configurations that can be reached from $C$. It never builds the infinite configuration graph. Instead it adds transitions to the automaton, one at a time, by a local rule that reads each pushdown rule backwards (for pre*) or forwards (for post*), until no rule adds anything. Bouajjani, Esparza and Maler gave the method in 1997; the worklist version of Esparza, Hansel, Rossmanith and Schwoon (2000) computes pre* in time $O(q^2 r)$ for an automaton with $q$ states and a system with $r$ rules. The algorithm is the standard solution of the [pushdown reachability problem](/pushdown-reachability/) and the core of model checkers for recursive programs.

## In plain words

A program with recursion has a call stack that can grow forever, so it has infinitely many states. But you can describe big sets of stacks with a small automaton that reads the stack from top to bottom. Saturation starts with an automaton for the target states, and it keeps adding arrows. The rule is simple: if a program step turns "location p with letter a on top" into "location p2 with some letters on top", and the automaton can already read those letters from p2 to some state, then it should also be able to read the letter a from p to that state. When no new arrow can be added, the automaton accepts exactly the states that can reach the target. The automaton never gets new states, so this stops after a number of steps that is polynomial in its size.

## The problem

A pushdown system is $\mathcal{P} = (P, \Gamma, \Delta)$ with control locations $P$, stack alphabet $\Gamma$ and rules $\langle p, \gamma \rangle \hookrightarrow \langle p', w \rangle$ with $|w| \le 2$. It moves by $\langle p, \gamma u \rangle \Rightarrow \langle p', w u \rangle$.

A *$\mathcal{P}$-automaton* is $\mathcal{A} = (Q, \Gamma, \to, P, F)$: a finite set of states $Q \supseteq P$, transitions $\to \subseteq Q \times \Gamma \times Q$, and final states $F \subseteq Q$. We write $s \xrightarrow{w} s'$ for a path labelled $w$. It accepts $\langle p, w \rangle$ when $p \xrightarrow{w} f$ for some $f \in F$; $L(\mathcal{A})$ is the set of accepted configurations. We assume that the input automaton has no transition into a state of $P$; any automaton can be changed to have this property by copying the states of $P$.

Input: $\mathcal{P}$ and $\mathcal{A}$. Output: an automaton for $\mathrm{pre}^*(L(\mathcal{A}))$, or for $\mathrm{post}^*(L(\mathcal{A}))$.

## The algorithm

**Pre\*.** The automaton for $\mathrm{pre}^*$ has the same states as $\mathcal{A}$. It is the least set of transitions that contains $\to$ and satisfies the *saturation rule*:

$$\text{if } \langle p, \gamma \rangle \hookrightarrow \langle p', w \rangle \in \Delta \text{ and } p' \xrightarrow{w} s \text{ in the current automaton, then add } p \xrightarrow{\gamma} s.$$

Applying the rule in any order until nothing changes gives the right result. The efficient version below is a worklist algorithm. For a push rule $\langle p_1, \gamma_1 \rangle \hookrightarrow \langle q, \gamma \gamma_2 \rangle$, once a transition $q \xrightarrow{\gamma} q'$ is known, it stores a *derived* rule $\langle p_1, \gamma_1 \rangle \hookrightarrow \langle q', \gamma_2 \rangle$, which acts like an internal rule from then on. This avoids searching for paths of length two again and again.

```pseudo id=main
PRE-STAR(Δ, A)                         ▷ A = (Q, Γ, →_0, P, F) with no transition into P
L1  rel ← ∅, trans ← →_0
L2  for each pop rule ⟨p, γ⟩ ↪ ⟨p', ε⟩ in Δ do trans ← trans ∪ {(p, γ, p')}
L3  Δ' ← ∅                                ▷ the derived rules
L4  while trans ≠ ∅ do
L5      remove a transition t = (q, γ, q') from trans
L6      if t ∈ rel then continue
L7      rel ← rel ∪ {t}
L8      for each rule ⟨p_1, γ_1⟩ ↪ ⟨q, γ⟩ in Δ ∪ Δ' do trans ← trans ∪ {(p_1, γ_1, q')}
L9      for each rule ⟨p_1, γ_1⟩ ↪ ⟨q, γ γ_2⟩ in Δ do
            Δ' ← Δ' ∪ {⟨p_1, γ_1⟩ ↪ ⟨q', γ_2⟩}
L10         for each (q', γ_2, q'') ∈ rel do trans ← trans ∪ {(p_1, γ_1, q'')}
L11 return (Q, Γ, rel, P, F)
```

Line L2 handles pop rules: from $\langle p, \gamma u \rangle$ the system goes to $\langle p', u \rangle$ in one step, so reading $\gamma$ from $p$ may lead to $p'$. Line L8 handles internal rules and derived rules: if $q \xrightarrow{\gamma} q'$ and $\langle p_1, \gamma_1 \rangle$ goes to $\langle q, \gamma \rangle$, then $p_1 \xrightarrow{\gamma_1} q'$. Lines L9 and L10 handle push rules in two halves. When the first transition $q \xrightarrow{\gamma} q'$ appears, line L9 records the derived rule; line L10 handles the second transitions $q' \xrightarrow{\gamma_2} q''$ that are already present, and line L8 will handle those that come later.

**Post\*.** For post*, the rules are read forwards, and push rules need new states. For each pair $(p', \gamma_1)$ that is the target of a push rule $\langle p, \gamma \rangle \hookrightarrow \langle p', \gamma_1 \gamma_2 \rangle$, add a state $m_{p', \gamma_1}$. The automaton may use empty moves $\varepsilon$.

```pseudo id=post
POST-STAR(Δ, A)                        ▷ A has no transition into P and no ε moves
P1  rel ← the transitions of A that leave states not in P
P2  trans ← the transitions of A that leave states in P
P3  while trans ≠ ∅ do
P4      remove t = (p, a, q) from trans; if t ∈ rel then continue
P5      rel ← rel ∪ {t}
P6      if a ≠ ε then
P7          for each ⟨p, a⟩ ↪ ⟨p', ε⟩: trans ← trans ∪ {(p', ε, q)}
P8          for each ⟨p, a⟩ ↪ ⟨p', γ_1⟩: trans ← trans ∪ {(p', γ_1, q)}
P9          for each ⟨p, a⟩ ↪ ⟨p', γ_1 γ_2⟩:
                trans ← trans ∪ {(p', γ_1, m_{p',γ_1})}, rel ← rel ∪ {(m_{p',γ_1}, γ_2, q)}
P10             for each (p'', ε, m_{p',γ_1}) ∈ rel: trans ← trans ∪ {(p'', γ_2, q)}
P11     else for each (q, γ', q') ∈ rel: trans ← trans ∪ {(p, γ', q')}
P12 return (Q ∪ {m_{p',γ_1}}, Γ, rel, P, F)
```

A pop rule gives an empty move (line P7): after the pop, the stack below is read from where $a$ led. A push rule writes $\gamma_1$ into the new state $m_{p', \gamma_1}$ and $\gamma_2$ from there to $q$ (line P9). Line P11 replaces each empty move followed by a letter with one transition, so that empty moves never need to be chained.

## Example

The [pushdown system](/pushdown-system/) of the recursive program has one control location $g$ and the rules

$$\langle g, m_0 \rangle \hookrightarrow \langle g, p_0 m_1 \rangle,\ \langle g, p_0 \rangle \hookrightarrow \langle g, p_1 \rangle,\ \langle g, p_0 \rangle \hookrightarrow \langle g, p_2 \rangle,\ \langle g, p_1 \rangle \hookrightarrow \langle g, p_0 p_2 \rangle,\ \langle g, p_2 \rangle \hookrightarrow \langle g, \varepsilon \rangle,\ \langle g, m_1 \rangle \hookrightarrow \langle g, m_1 \rangle.$$

**Pre\*.** Which configurations can reach $\langle g, m_1 \rangle$, the point where the call returns to $\mathit{main}$? The input automaton has one transition $g \xrightarrow{m_1} f$, with $F = \{f\}$.

| Step | Transition added | Reason |
|---|---|---|
| L2 | $(g, p_2, g)$ | pop rule $\langle g, p_2 \rangle \hookrightarrow \langle g, \varepsilon \rangle$ |
| L8 | $(g, p_0, g)$ | rule $\langle g, p_0 \rangle \hookrightarrow \langle g, p_2 \rangle$ and $(g, p_2, g)$ |
| L9 | derived $\langle g, m_0 \rangle \hookrightarrow \langle g, m_1 \rangle$ and $\langle g, p_1 \rangle \hookrightarrow \langle g, p_2 \rangle$ | push rules with $p_0$ on top, and $(g, p_0, g)$ |
| L10 | $(g, m_0, f)$ | derived rule and $(g, m_1, f)$ |
| L10 | $(g, p_1, g)$ | derived rule and $(g, p_2, g)$ |

Nothing else can be added. The final automaton has a loop on $g$ for $p_0$, $p_1$ and $p_2$, and the transitions $g \xrightarrow{m_0} f$ and $g \xrightarrow{m_1} f$. So

$$\mathrm{pre}^*(\{\langle g, m_1 \rangle\}) = \{ \langle g, u\, m \rangle : u \in \{p_0, p_1, p_2\}^*,\ m \in \{m_0, m_1\} \}.$$

For instance $\langle g, p_1 p_0 m_1 \rangle$ is in it: $p_1$ calls $p$ again, every call can return, and so the stack unwinds to $m_1$. But $\langle g, m_0 m_1 \rangle$ is not: it can only reach $\langle g, m_1 m_1 \rangle$, with two letters.

**Post\*.** Start from $\langle g, m_0 \rangle$, with the automaton $g \xrightarrow{m_0} f$. Both push rules put $p_0$ on top, so there is one new state $m = m_{g, p_0}$. The algorithm adds $(g, p_0, m)$ and $(m, m_1, f)$ from the first push rule; then $(g, p_1, m)$ and $(g, p_2, m)$ from the two rules for $p_0$; then $(m, p_2, m)$ from the push rule for $p_1$; then $(g, \varepsilon, m)$ from the pop rule for $p_2$; and line P11 turns this empty move into $(g, m_1, f)$ and $(g, p_2, m)$. The result accepts

$$\mathrm{post}^*(\{\langle g, m_0 \rangle\}) = \{\langle g, m_0 \rangle, \langle g, m_1 \rangle\} \cup \{\langle g, x\, p_2^k\, m_1 \rangle : x \in \{p_0, p_1, p_2\},\ k \ge 0\}.$$

The loop $(m, p_2, m)$ records the return points of the recursive calls that can pile up on the stack.

## Correctness

**Theorem.** PRE-STAR terminates, and its result accepts exactly $\mathrm{pre}^*(L(\mathcal{A}))$. POST-STAR terminates, and its result accepts exactly $\mathrm{post}^*(L(\mathcal{A}))$.

For pre*, all transitions have their source and target among the $q$ states of $\mathcal{A}$, so there are finitely many, and each enters rel once. *Soundness:* each new transition $p \xrightarrow{\gamma} s$ comes with a reason, one step $\langle p, \gamma \rangle \Rightarrow \langle p', w \rangle$ and a path $p' \xrightarrow{w} s$ of transitions added earlier; an induction on the insertion times of the transitions on a path shows that if the result accepts $\langle p, w \rangle$, then $\langle p, w \rangle$ reaches a configuration accepted by $\mathcal{A}$. *Completeness:* the result satisfies the saturation rule, because every way of making its hypothesis true is handled by line L2, L8 or L10 at the moment the last needed transition appears; an induction on the length of a run then shows that every configuration that reaches $L(\mathcal{A})$ is accepted. The proof for post* has the same two halves, with an invariant that says what each transition into a new state $m_{p', \gamma_1}$ means. The full proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

Let $q = |Q|$, $r = |\Delta|$ and $t = |{\to_0}|$, and store rel in a table indexed by state and letter, so that lookups take $O(1)$ time.

- **Number of transitions.** Each transition added by the algorithm starts in a control location $p$ with a letter $\gamma$ such that some rule has the left side $\langle p, \gamma \rangle$, so there are at most $r q$ new transitions, and $|rel| \le t + r q$.
- **Line L8.** A rule $\langle p_1, \gamma_1 \rangle \hookrightarrow \langle q, \gamma \rangle$ of $\Delta$ is scanned once for each transition $(q, \gamma, q')$, so at most $q$ times; this costs $O(r q)$. A push rule gives at most $q$ derived rules, one per $q'$, and each is scanned at most $q$ times; this costs $O(r q^2)$.
- **Lines L9 and L10.** A push rule is visited once per transition $(q, \gamma, q')$, so at most $q$ times, and each visit scans at most $q$ transitions $(q', \gamma_2, q'')$. This costs $O(r q^2)$.

So PRE-STAR runs in $O(q^2 r + t)$ time and $O(q r + t)$ space; this is the bound of Esparza, Hansel, Rossmanith and Schwoon (2000). For [pushdown reachability](/pushdown-reachability/) of one configuration, $q$ is the size of the target automaton, so the time is cubic in the input. POST-STAR is also polynomial. The new states $m_{p', \gamma_1}$ add at most $r$ states, every transition it adds starts in a control location or in a new state, and Esparza et al. bound its time by $O(|P|\, r\, (q + r) + |P|\, t)$.

## Properties

- **No new states for pre\*.** The pre* automaton has the states of the input. This gives a direct proof of Büchi's theorem that pre* of a regular set is regular.
- **Order independence.** The result is the least fixed point of the saturation rule, so the order in which the worklist is processed does not change it, only the running time. This is an instance of a least [fixed point](/fixed-point/) computed by chaotic iteration.
- **Incremental.** New rules or new initial transitions can be added later, and the worklist continues from where it stopped.
- **Witnesses.** If each transition records its reason, a path through the reasons gives a run of the pushdown system from an accepted configuration to the target, which is a counterexample trace for model checkers.

## Variants and improvements

- **Symbolic saturation.** When the control locations are valuations of global variables, the rules and transitions are stored as binary decision diagrams, as in the Moped tool of Schwoon.
- **Weighted pushdown systems.** Attaching weights from a bounded idempotent semiring to the rules and computing the combined weight of all paths gives interprocedural dataflow analysis (Reps, Schwoon, Jha and Melski 2005).
- **Model checking.** [LTL model checking](/ltl-model-checking/) of a pushdown system builds the product with a Büchi automaton and uses pre* to find configurations from which an accepting state can be visited again with the stack only growing; Bouajjani, Esparza and Maler (1997) reduce this to pre* computations. CTL and the [modal mu-calculus](/mu-calculus-model-checking/) use alternating automata, with a saturation of the same kind.
- **Summaries and CFL-reachability.** The pop summaries that pre* computes, the transitions $p \xrightarrow{\gamma} p'$ into control locations, are the same as the procedure summaries of [CFL-reachability](/cfl-reachability/) and of the Reps-Horwitz-Sagiv algorithm.

## When to use it

Use saturation to decide reachability or safety for programs with recursion and finite-domain data, to compute all stacks with which a program point can be reached, or as the inner step of LTL model checking for pushdown systems. Use pre* when the target set is small and the initial set large, and post* in the other case; both give exact answers. When the system has two or more stacks, as in concurrent programs with recursion, reachability is undecidable, and saturation applies only to under-approximations such as context-bounded runs.

## Pitfalls

- **Transitions into control locations.** The proofs need an input automaton with no transition into a state of $P$. If the target automaton has one, for example a loop on $p$, copy the states of $P$ first; otherwise the pre* rule can confuse "the stack is read from $p$" with "the run reached $p$ in the middle of the stack".
- **Rules with long right sides.** The pseudocode assumes $|w| \le 2$. A rule that pushes three letters must be split with a new control location first, or line L9 must search paths of any length.
- **Empty moves in post\*.** Forgetting line P11, or chaining empty moves, gives a wrong automaton. In the algorithm above, empty moves start only in control locations and end outside them, so they never chain.
- **The empty stack.** A configuration $\langle p, \varepsilon \rangle$ is accepted only when $p$ itself is final. A pop rule can lead to such a configuration, so tests must include it.

## Implementations

## History

Büchi proved in 1964 that the words derivable in a prefix rewriting system from a regular set form a regular set, which is the regularity of pre* and post* in other terms. Bouajjani, Esparza and Maler used $\mathcal{P}$-automata and the saturation rule in 1997 to model check pushdown systems against LTL and CTL, and Finkel, Willems and Wolper gave a similar post* procedure in the same year. Esparza, Hansel, Rossmanith and Schwoon gave the worklist algorithms with their bounds in 2000, and Schwoon's thesis and his Moped tool made the method practical for programs. Reps, Schwoon, Jha and Melski generalized it to weighted pushdown systems in 2005.

## References
