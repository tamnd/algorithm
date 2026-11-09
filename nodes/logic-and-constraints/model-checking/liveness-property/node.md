---
tag: 9TH7DJ
kind: definition
slug: liveness-property
name: Liveness property
aliases:
- Liveness
- Progress property
area: logic-and-constraints/model-checking
level: intro
summary: A property stating that something good eventually happens. No finite prefix can violate it, the liveness properties are the dense sets, and every property is safety intersected with liveness.
prereqs: [safety-property, temporal-logic]
see_also: [safety-property, fairness, linear-temporal-logic, ltl-model-checking, nested-depth-first-search, buchi-automaton, liveness-to-safety, ctl-model-checking]
sources:
  - paper: doi:10.1016/0020-0190(85)90056-0
    title: Bowen Alpern and Fred B. Schneider, Defining liveness, Information Processing Letters 21(4), 1985, pages 181 to 185
    locator: the definition of liveness (each finite prefix extends to a word in the property), the topological characterization as dense sets, and the theorem that every property is the intersection of a safety property and a liveness property
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 3, Section 3.4 (liveness properties and the decomposition theorem) and Section 3.5 (fairness); Chapter 4 (checking omega-regular properties with nested depth-first search)
  - paper: doi:10.1109/TSE.1977.229904
    title: Leslie Lamport, Proving the correctness of multiprocess programs, IEEE Transactions on Software Engineering SE-3(2), 1977, pages 125 to 143
    locator: the informal notion of liveness ("something good eventually happens")
  - paper: "Bowen Alpern and Fred B. Schneider, Recognizing safety and liveness, Distributed Computing 2(3), 1987, pages 117 to 126"
    locator: the decomposition of a property given by a Buchi automaton into a safety automaton and a liveness automaton
---

A liveness property says that something good eventually happens: each request is eventually answered, a waiting process eventually enters its critical section, the program eventually terminates. Its defining feature is the opposite of a [safety property](/safety-property/): no finite prefix of an execution can violate it, because the good thing can still happen later. So a counterexample to a liveness property is an infinite path, and in a finite system a lasso: a finite path to a cycle that repeats forever. Alpern and Schneider (1985) gave the formal definition and proved that every property is the intersection of a safety property and a liveness property.

## Definition

Fix $\Sigma = 2^{AP}$ and a linear-time property $P \subseteq \Sigma^\omega$, as on the [safety property](/safety-property/) page. Write $\mathit{pref}(P)$ for the set of finite prefixes of the words in $P$.

**Liveness property.** $P$ is a **liveness property** if each finite word can be extended to a word in $P$:

$$\text{for each } u \in \Sigma^* \text{ there is a } \sigma \in \Sigma^\omega \text{ with } u\sigma \in P, \quad \text{that is,} \quad \mathit{pref}(P) = \Sigma^*.$$

So $P$ has no bad prefix. A Kripke structure that violates $P$ does so on an infinite path, never on a finite one.

**Topology.** With the prefix metric on $\Sigma^\omega$ (two words are close when they share a long prefix), the open balls are the sets $u\Sigma^\omega$ for $u \in \Sigma^*$. $P$ is a liveness property exactly when it meets each such ball, that is, when $P$ is **dense**. The [safety properties](/safety-property/) are the closed sets. A set that is closed and dense is the whole space, so $\Sigma^\omega$ is the only property that is both safety and liveness.

**Decomposition theorem (Alpern and Schneider 1985).** For each property $P \subseteq \Sigma^\omega$, the sets

$$\mathit{Safe} = \mathit{cl}(P) \qquad \text{and} \qquad \mathit{Live} = P \cup (\Sigma^\omega \setminus \mathit{cl}(P))$$

are a safety property and a liveness property, and $P = \mathit{Safe} \cap \mathit{Live}$.

*Proof.* We prove it in any topological space $X$, with $\mathit{cl}$ the topological closure.

1. $\mathit{Safe} = \mathit{cl}(P)$ is closed, so it is a safety property.
2. $\mathit{Live}$ is dense. Its closure contains $\mathit{cl}(P)$, because $P \subseteq \mathit{Live}$, and it contains $X \setminus \mathit{cl}(P)$, because that set is a subset of $\mathit{Live}$. The union of the two is $X$.
3. $\mathit{Safe} \cap \mathit{Live} = (\mathit{cl}(P) \cap P) \cup (\mathit{cl}(P) \setminus \mathit{cl}(P)) = P$, because $P \subseteq \mathit{cl}(P)$. $\blacksquare$

The same proof in terms of words: for step 2, take $u \in \Sigma^*$. If $u \in \mathit{pref}(P)$, then $u$ extends to a word of $P \subseteq \mathit{Live}$. If not, then every extension $u\sigma$ has the prefix $u \notin \mathit{pref}(P)$, so $u\sigma \notin \mathit{cl}(P)$ and $u\sigma \in \mathit{Live}$.

The safety part $\mathit{cl}(P)$ is the strongest safety property implied by $P$. The liveness part is not unique: any liveness property $L$ with $\mathit{cl}(P) \cap L = P$ works. For a property given by a Büchi automaton, both parts are again given by Büchi automata (Alpern and Schneider 1987).

## Examples and non-examples

**Eventually.** $\mathsf{F}\,c_1$ ("process 1 eventually enters its critical section") is a liveness property: each finite word $u$ extends to $u\{c_1\}^\omega$.

**Response.** $\mathsf{G}(\mathit{req} \to \mathsf{F}\,\mathit{ack})$ is a liveness property: append $\{\mathit{ack}\}^\omega$ to any finite word. In the two-process mutual exclusion structure of the [Kripke structure](/kripke-structure/) page, the response property $\mathsf{G}(w_1 \to \mathsf{F}\,c_1)$ fails, and the counterexample is a lasso: the path $(n,n,1)\,(w,n,1)$ followed by the cycle $(w,w,1)\,(w,c,0)\,(w,n,1)$ repeated forever, in which process 1 waits and never enters. Each finite prefix of this path can still be extended to a good path, which is why no finite counterexample exists. A [fairness](/fairness/) assumption removes this path.

**Recurrence and persistence.** $\mathsf{G}\mathsf{F}\,p$ (infinitely often $p$) and $\mathsf{F}\mathsf{G}\,p$ (from some point on, always $p$) are liveness properties. No finite prefix can confirm or refute either of them.

**A decomposition.** $P = p\,\mathsf{U}\,q$ is neither safety nor liveness. Its closure is $p\,\mathsf{W}\,q$ (weak until, which also allows $p$ forever). The theorem gives $\mathit{Live} = (p\,\mathsf{U}\,q) \vee \neg(p\,\mathsf{W}\,q)$, and the simpler liveness property $\mathsf{F}\,q$ also works: $p\,\mathsf{U}\,q = (p\,\mathsf{W}\,q) \wedge \mathsf{F}\,q$.

**Non-example: an invariant.** $\mathsf{G}\,p$ is a safety property, and it is not liveness when $p$ is not valid: a one-letter word whose letter makes $p$ false is a bad prefix.

**Non-example: bounded response.** "Each request is answered within 3 steps" sounds like liveness, but it is a safety property: a violation is visible 3 steps after the request.

**Edge case.** $\Sigma^\omega$ is liveness and safety. $\emptyset$ is safety and not liveness.

## Related definitions

- **Safety property.** A [safety property](/safety-property/) is a closed set; a liveness property is a dense set. Together they generate all properties by the theorem above. The algorithmic split follows the same line: safety reduces to [reachability](/reachability-problem/) of a bad state, and liveness reduces to the reachability of a bad cycle.
- **Checking liveness.** An LTL liveness property is checked by [LTL model checking](/ltl-model-checking/): build a [Büchi automaton](/buchi-automaton/) for the negation, and search the product for a reachable accepting cycle with [nested depth-first search](/nested-depth-first-search/) or [strongly connected components](/strongly-connected-components/). In CTL, liveness is $\mathsf{AF}$ and $\mathsf{AG}\,\mathsf{AF}$, and the [CTL labelling algorithm](/ctl-labelling-algorithm/) computes them with fixed points.
- **Fairness.** [Fairness](/fairness/) constraints such as "infinitely often $F$" are liveness properties used as assumptions. A liveness property usually holds only under fairness, because without it a scheduler can starve a process.
- **Liveness to safety.** The [liveness-to-safety](/liveness-to-safety/) transformation turns the search for a bad cycle into the search for a bad state in a system that saves a copy of one state and later finds it again.
- **Other liveness notions.** Sistla defined *uniform liveness* (one suffix $\sigma$ that works for every prefix) and *absolute liveness* (closed under adding any prefix); $\mathsf{G}\mathsf{F}\,p$ and $\mathsf{F}\,p$ are both, with the suffix $\{p\}^\omega$.
- **Starvation freedom.** In concurrency, [starvation freedom](/starvation-freedom/) is the liveness property that every process that tries to enter its critical section eventually does.

## References
