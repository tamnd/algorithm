---
tag: BJQN9P
kind: technique
slug: assume-guarantee-reasoning
name: Assume-guarantee reasoning
aliases:
- Assume-guarantee rule
- Assumption-commitment reasoning
- Rely-guarantee reasoning
area: logic-and-constraints/model-checking
level: advanced
summary: Check each component under an assumption about its environment, then discharge the assumption on the other components; non-circular rules are sound, circular ones need extra conditions.
prereqs: [compositional-verification, labelled-transition-system, safety-property, product-construction]
see_also: [compositional-verification, lstar-algorithm, simulation-relation, trace-equivalence, language-containment, cegar, liveness-property, inductive-invariant]
sources:
  - paper: doi:10.1007/3-540-36577-X_24
    title: Jamieson M. Cobleigh, Dimitra Giannakopoulou and Corina S. Păsăreanu, Learning assumptions for compositional verification, TACAS 2003, LNCS 2619
    locator: pages 331 to 346 (the non-circular rule, the weakest assumption, the use of L* with membership and conjecture queries answered by model checking, and the case study)
  - paper: "Amir Pnueli, In transition from global to modular temporal reasoning about programs, in Logics and Models of Concurrent Systems, NATO ASI Series F13, Springer, 1985"
    title: In transition from global to modular temporal reasoning about programs
    locator: the assume-guarantee triple notation and modular temporal reasoning
  - paper: "Martín Abadi and Leslie Lamport, Conjoining specifications, ACM Transactions on Programming Languages and Systems 17(3), 1995"
    title: Conjoining specifications
    locator: the composition theorem for circular assumption-guarantee specifications, with safety assumptions and the condition that a guarantee holds one step longer than its assumption
  - paper: "Kenneth L. McMillan, Circular compositional reasoning about liveness, CHARME 1999, LNCS 1703"
    title: Circular compositional reasoning about liveness
    locator: the unsoundness of naive circular reasoning for liveness, and a sound circular rule based on induction over time
---

Assume-guarantee reasoning proves a property of a composition $M_1 \parallel M_2$ by checking each component in an environment that is described by an *assumption*. The triple $\langle A \rangle\, M\, \langle P \rangle$ says: whenever $M$ runs in an environment that satisfies $A$, the system satisfies $P$. The basic *non-circular* rule is

$$\frac{\langle A \rangle\, M_1\, \langle P \rangle \qquad \langle \mathit{true} \rangle\, M_2\, \langle A \rangle}{\langle \mathit{true} \rangle\, M_1 \parallel M_2\, \langle P \rangle}$$

and each premise is a model checking problem much smaller than the product when $A$ is small. The notation goes back to Pnueli (1985), and for shared-variable programs the same idea is Jones's rely-guarantee method. A *circular* rule uses each component's guarantee as the other's assumption, $\langle A_2 \rangle M_1 \langle A_1 \rangle$ and $\langle A_1 \rangle M_2 \langle A_2 \rangle$. Without extra conditions it is unsound, as the counterexamples below show; it becomes sound for safety properties with a one-step delay in the guarantee (Abadi and Lamport), or with induction over time for liveness (McMillan 1999). Finding a good assumption is the hard part. Cobleigh, Giannakopoulou and Păsăreanu (2003) learn it automatically with the [L\* algorithm](/lstar-algorithm/), with model checking queries as the teacher. Assume-guarantee reasoning is one family of [compositional verification](/compositional-verification/); that page has the general technique, including compositional minimization, which needs no assumptions.

## In plain words

Two parts of a system work together, and we want to know that the whole system is safe. Checking the whole system at once is too expensive. So we guess a simple description $A$ of how the second part behaves, as far as the first part can see it.

Then we do two small checks. First: the first part, together with any partner that behaves like $A$, is safe. Second: the real second part really behaves like $A$. If both checks pass, the whole system is safe.

Using the two parts' promises about each other in a circle ("I behave if you behave, and you behave if I behave") is tempting, but it can prove false things. It needs extra rules, for example that each part keeps its promise one step longer than the other part has kept its own.

## When it applies

- **Two or more components with a narrow interface.** The assumption only mentions the interface actions or variables, so it can be much smaller than the component it stands for.
- **Safety properties of labelled transition systems or circuits.** The premises are checks of the form "the product of $A$, $M$ and an error automaton for $P$ cannot reach the error state".
- **An assumption is known or learnable.** Designers often know the protocol at an interface. Otherwise L\* can learn an assumption, which is regular for safety properties.
- **Liveness and circular dependencies.** Circular rules are needed when each component's correctness depends on the other's, as in handshake protocols. Then the extra soundness conditions must be met.

## The template

Components are labelled transition systems with alphabets $\alpha M_1$, $\alpha M_2$, composed in parallel with synchronization on shared actions. A safety property $P$ is a deterministic automaton with an error state, and $M \models P$ means that no trace of $M$, projected to $\alpha P$, reaches the error state. The triple $\langle A \rangle M \langle P \rangle$ means $A \parallel M \models P$, and $\langle \mathit{true} \rangle M \langle P \rangle$ means $M \models P$. The assumption is over the interface alphabet $\Sigma = (\alpha M_1 \cup \alpha P) \cap \alpha M_2$.

**Soundness of the non-circular rule.** Let $\sigma$ be a trace of $M_1 \parallel M_2$. Its projection to $\alpha M_2$ is a trace of $M_2$, so by the second premise $\sigma{\restriction}\alpha A$ is accepted by $A$. Its projection to $\alpha M_1$ is a trace of $M_1$. So $\sigma{\restriction}(\alpha M_1 \cup \alpha A)$ is a trace of $A \parallel M_1$, and by the first premise its projection to $\alpha P$ does not reach the error state. As $\alpha P \subseteq \alpha M_1 \cup \Sigma$, this projection is $\sigma{\restriction}\alpha P$. ∎

**The weakest assumption.** Let $A_w$ be the set of traces $t \in \Sigma^*$ such that $M_1$, in an environment that does exactly $t$ on $\Sigma$, cannot violate $P$. Then $\langle A_w \rangle M_1 \langle P \rangle$ holds, every $A$ with $\langle A \rangle M_1 \langle P \rangle$ satisfies $L(A) \subseteq A_w$, and $\langle \mathit{true} \rangle M_1 \parallel M_2 \langle P \rangle$ holds if and only if $M_2 \models A_w$. So the rule is complete when $A = A_w$. The set $A_w$ is regular (Giannakopoulou, Păsăreanu and Barringer, 2002), which is what makes learning possible.

**Learning the assumption.** Cobleigh, Giannakopoulou and Păsăreanu run L\* with $A_w$ as the target language. The teacher answers queries with model checking.

```pseudo id=main
AG-LEARN(M_1, M_2, P)
L1  run L* over Σ = (αM_1 ∪ αP) ∩ αM_2, with target language A_w
L2  membership query for t ∈ Σ*: answer yes iff ⟨t⟩ M_1 ⟨P⟩               ▷ t as a linear transition system
L3  loop
L4      A ← the next conjecture of L*
L5      if ⟨A⟩ M_1 ⟨P⟩ fails with counterexample c then give c↾Σ to L* as a negative example; continue
L6      if ⟨true⟩ M_2 ⟨A⟩ holds then return HOLDS                           ▷ both premises of the rule hold
L7      let c be the counterexample of M_2 against A, and t ← c↾Σ
L8      if ⟨t⟩ M_1 ⟨P⟩ fails then return FAILS                              ▷ t is a real interface trace that breaks P
L9      give t to L* as a positive example                                    ▷ t ∈ A_w but A rejects it
```

**Why it is correct.** HOLDS at line L6 follows from the rule. At line L8, $M_2$ can do $t$ on the interface, and $M_1$ with $t$ violates $P$; the two runs agree on the shared actions, which lie in $\Sigma$, so they combine into a run of $M_1 \parallel M_2$ that violates $P$. Each counterexample given to L\* at line L5 or L9 lies in the symmetric difference of $L(A)$ and $A_w$. By Angluin's theorem, L\* makes at most $k$ conjectures, where $k$ is the number of states of the minimal automaton of $A_w$, and its last conjecture is $A_w$. With $A = A_w$, line L5 cannot fail, and line L6 or line L8 ends the loop. The loop often ends earlier, with an assumption smaller than $A_w$.

**Circular rules.** The naive circular rule

$$\frac{\langle A_2 \rangle\, M_1\, \langle A_1 \rangle \qquad \langle A_1 \rangle\, M_2\, \langle A_2 \rangle}{\langle \mathit{true} \rangle\, M_1 \parallel M_2\, \langle A_1 \wedge A_2 \rangle}$$

is unsound in general. Two counterexamples:

- *Zero-delay safety.* Two synchronous components share Boolean signals $x$ (output of $M_1$) and $y$ (output of $M_2$). $M_1$ requires $x_t = y_t$ at each time $t$, and $M_2$ requires $y_t = x_t$. Let $A_1 = \mathbf{G}\,\neg x$ and $A_2 = \mathbf{G}\,\neg y$. If the environment of $M_1$ keeps $y$ at 0, then $x$ stays 0, so the first premise holds, and the second holds by symmetry. But the composition has the run with $x_t = y_t = 1$ for all $t$, which violates both. Each component assumes that the other's output stays 0 and then guarantees that its own stays 0, yet both outputs can be 1 together. The same happens for labelled transition systems with a shared action $\mathit{bad}$ and $A_1 = A_2 =$ "$\mathit{bad}$ never happens": each premise holds because the assumed environment refuses $\mathit{bad}$, yet $M_1 \parallel M_2$ can do $\mathit{bad}$ if both components can.
- *Liveness.* $M_1$ waits until $y = 1$ and then sets $x := 1$; $M_2$ waits until $x = 1$ and then sets $y := 1$; both start at 0. With $A_1 = \mathbf{F}\,x$ and $A_2 = \mathbf{F}\,y$, both premises hold, but in the composition both wait forever.

**A sound circular rule for safety.** Write $M \models A \rhd G$ if, in every run of $M$ and for every $n \ge 0$, when $A$ holds at times $0, \ldots, n - 1$, then $G$ holds at times $0, \ldots, n$. For state predicates $A_1$ and $A_2$ and the synchronous composition,

$$\frac{M_1 \models A_2 \rhd A_1 \qquad M_2 \models A_1 \rhd A_2}{M_1 \parallel M_2 \models \mathbf{G}\,(A_1 \wedge A_2)}$$

is sound. *Proof.* A run of the composition is a run of each component. By induction on $n$, $A_1$ and $A_2$ hold at times $0, \ldots, n$. For $n = 0$ the hypotheses of both premises are empty, so both guarantees hold at time 0. If both hold at times $0, \ldots, n$, the premises give both at times $0, \ldots, n + 1$. ∎ In the zero-delay counterexample the premise $M_1 \models A_2 \rhd A_1$ fails already for $n = 0$, because $x_0$ can be 1. If $M_1$ is a Moore machine with $x_0 = 0$ and $x_{t+1} = y_t$, the premise holds, and so does the conclusion. Abadi and Lamport proved a general form of this rule for safety assumptions, and McMillan (1999) gave a circular rule for liveness with induction over time.

## Classic examples

**Input and output.** In a small example in the style of Cobleigh et al., $M_1$ (Output) repeats $\mathit{send}, \mathit{out}, \mathit{ack}$, and $M_2$ (Input) repeats $\mathit{in}, \mathit{send}, \mathit{ack}$. The property $P$ says that $\mathit{in}$ and $\mathit{out}$ alternate, starting with $\mathit{in}$. Here $\Sigma = \{\mathit{in}, \mathit{send}, \mathit{ack}\}$. The assumption $A$ that repeats $\mathit{in}, \mathit{send}, \mathit{ack}$ has 3 states. $A \parallel M_1$ has only the run $\mathit{in}, \mathit{send}, \mathit{out}, \mathit{ack}, \ldots$, which satisfies $P$, and $M_2$ satisfies $A$. So both premises hold. The weakest assumption $A_w$ is larger: it also contains traces that $M_1$ refuses, such as $\mathit{ack}$ at the start, because the composition then stops and cannot violate $P$.

**Other uses.**

- **NASA software.** Cobleigh et al. applied the learning method to a model of the executive of the K9 Mars rover in the LTSA tool. Their learned assumptions were small compared with the components; this is a measured result on that case study.
- **Hardware.** McMillan's compositional method in Cadence SMV uses circular assume-guarantee rules with time induction to verify processors and cache protocols by splitting properties over time and data.
- **Rely-guarantee for programs.** For shared-variable concurrency, Jones's rely-guarantee method checks each thread under a rely condition on the other threads' steps; it is the deductive form of the same idea.

## Variations

- **Symmetric rules.** Rules with assumptions for both components, such as $\langle A_1 \rangle M_1 \langle P \rangle$, $\langle A_2 \rangle M_2 \langle P \rangle$ and a check that $\overline{A_1} \parallel \overline{A_2}$ satisfies $P$, where $\overline{A}$ is the complement; they can need smaller assumptions.
- **Many components.** Apply the rule recursively: $M_2$ is itself a composition, and the second premise is checked compositionally.
- **Learning with SAT or with CEGAR.** Other works learn assumptions with SAT-based automata learning, or abstract the interface and refine it with counterexamples, as in [CEGAR](/cegar/).
- **Interface theories.** Interface automata (de Alfaro and Henzinger) build the assumption into the component as the inputs that it accepts.

## Pitfalls

- **Unsound circularity.** Do not use the naive circular rule. Check that the guarantees are delayed by one step, that there are no zero-delay cycles, or that a rule for liveness with induction over time is used.
- **Alphabet mistakes.** The assumption alphabet must contain every action of $M_2$ that $M_1$ or $P$ can observe. If $\Sigma$ is too small, the weakest assumption no longer makes the rule complete, and learning can give wrong FAILS answers unless counterexamples are checked against the full system.
- **Large assumptions.** If $A_w$ is as large as $M_2$, nothing is saved. The method pays off only when the interface behaviour is simpler than the component.
- **Deadlock and liveness.** The trace-based rule is for safety properties. A component that refuses everything satisfies every safety assumption.

## Exercises

1. Prove that $\langle A \rangle M_1 \langle P \rangle$ implies $\langle A' \rangle M_1 \langle P \rangle$ when $L(A') \subseteq L(A)$.
2. Write down the minimal automaton of $A_w$ for the input and output example. *Hint:* besides the three states of the cycle, it has a state that accepts every continuation, reached when $M_1$ refuses the next action.
3. Show that in the zero-delay counterexample the premise $M_1 \models A_2 \rhd A_1$ of the sound circular rule fails, and that it holds for the Moore machine with $x_0 = 0$ and $x_{t+1} = y_t$.
4. Show that the naive circular rule would prove $\langle \mathit{true} \rangle M \langle P \rangle$ for every safety property $P$ over the alphabet of $M$, by taking $M_1 = M_2 = M$ and $A_1 = A_2 = P$.

## References
