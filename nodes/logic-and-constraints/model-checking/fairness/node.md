---
tag: A0PCGG
kind: concept
slug: fairness
name: Fairness
aliases:
- Fairness constraints
- Weak fairness
- Strong fairness
- Justice and compassion
- Fair CTL
area: logic-and-constraints/model-checking
level: advanced
summary: Constraints that keep only executions in which enabled actions are eventually taken. Weak fairness is justice, strong fairness is compassion, and fair CTL is checked with SCCs.
prereqs: [kripke-structure, computation-tree-logic, liveness-property, strongly-connected-components]
see_also: [liveness-property, ctl-labelling-algorithm, ctl-model-checking-linear-time, emerson-lei-algorithm, tarjan-scc, ltl-model-checking, starvation-freedom, buchi-automaton]
sources:
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 3, Section 3.5 (unconditional, strong and weak fairness, fairness assumptions and their realizability) and Chapter 6, Section 6.5 (fair CTL and the algorithm for fair EG by strongly connected components)
  - paper: doi:10.1145/5397.5399
    title: Edmund M. Clarke, E. Allen Emerson and A. Prasad Sistla, Automatic verification of finite-state concurrent systems using temporal logic specifications, ACM Transactions on Programming Languages and Systems 8(2), 1986, pages 244 to 263
    locator: the extension of the labelling algorithm to fairness constraints, using the strongly connected components of the restricted graph
  - paper: doi:10.1016/0167-6423(87)90036-0
    title: E. Allen Emerson and Chin-Laung Lei, Modalities for model checking, branching time logic strikes back, Science of Computer Programming 8(3), 1987, pages 275 to 306
    locator: fair CTL with strong fairness constraints, decided in polynomial time
  - book: "Zohar Manna and Amir Pnueli, The Temporal Logic of Reactive and Concurrent Systems: Specification, Springer, 1992"
    locator: the fair transition system model with justice and compassion requirements
---

Fairness is an assumption about which infinite executions of a system count. A model of a concurrent system has executions in which the scheduler ignores one process forever, although that process could move. Real schedulers do not do this, so a [liveness property](/liveness-property/) checked over all executions often fails for a reason nobody cares about. A fairness constraint removes the unrealistic executions and checks the property only on the fair ones. The two standard forms are weak fairness (justice) and strong fairness (compassion), and for [CTL](/computation-tree-logic/) both are handled with [strongly connected components](/strongly-connected-components/).

## In plain words

Two people share one door. A model checker asks: will each person who waits eventually get through? It answers no, because there is a run in which the other person always goes first. That run is legal in the model, but it is not how a reasonable scheduler behaves.

Fairness tells the checker to ignore such runs. Weak fairness says: an action that stays possible forever is taken at some point. Strong fairness says: an action that becomes possible again and again is taken at some point. Strong fairness removes more runs, so more properties hold under it.

For the branching-time logic CTL, the checker finds the fair runs with a graph search. A fair run ends up circling inside one tightly connected group of states, and that group must touch each place the fairness rules ask for.

## The idea

**Infinity sets.** For an infinite path $\pi$ of a [Kripke structure](/kripke-structure/) $M = (S, I, R, L)$, let $\mathit{inf}(\pi)$ be the set of states that occur infinitely often on $\pi$. Since $S$ is finite, $\mathit{inf}(\pi)$ is non-empty, and $\pi$ stays inside $\mathit{inf}(\pi)$ from some point on.

**Action-based fairness.** For an action (or a process) $a$, let $\mathit{en}_a$ be the set of states in which $a$ is enabled and $\mathit{taken}_a$ the set of states that are entered by a step of $a$. Then a path $\pi$ is

- **unconditionally fair** for $a$ if $\mathsf{G}\mathsf{F}\,\mathit{taken}_a$: $a$ is taken infinitely often;
- **weakly fair** for $a$ if $\mathsf{F}\mathsf{G}\,\mathit{en}_a \to \mathsf{G}\mathsf{F}\,\mathit{taken}_a$: if $a$ is enabled continuously from some point on, then $a$ is taken infinitely often;
- **strongly fair** for $a$ if $\mathsf{G}\mathsf{F}\,\mathit{en}_a \to \mathsf{G}\mathsf{F}\,\mathit{taken}_a$: if $a$ is enabled infinitely often, then $a$ is taken infinitely often.

Since $\mathsf{F}\mathsf{G}\,\mathit{en}_a$ implies $\mathsf{G}\mathsf{F}\,\mathit{en}_a$, unconditional fairness implies strong fairness, which implies weak fairness. Each is a liveness property, and each is used as an assumption: $M$ satisfies $\varphi$ under fairness if each fair path from $I$ satisfies $\varphi$.

**State-based form: justice and compassion.** The model checking algorithms use sets of states. A **justice** requirement is a set $J \subseteq S$, and $\pi$ is just when $\mathit{inf}(\pi) \cap J \ne \emptyset$. A **compassion** requirement is a pair $(p, q)$ of sets, and $\pi$ is compassionate when

$$\mathit{inf}(\pi) \cap p \ne \emptyset \implies \mathit{inf}(\pi) \cap q \ne \emptyset.$$

Weak fairness for $a$ is the justice set $J = (S \setminus \mathit{en}_a) \cup \mathit{taken}_a$, and strong fairness for $a$ is the compassion pair $(\mathit{en}_a, \mathit{taken}_a)$. A justice set $J$ is the compassion pair $(S, J)$. In automata terms, justice sets are a generalized Büchi condition and compassion pairs are a Streett condition. A *fairness constraint* is a finite list of justice and compassion requirements, and a path is **fair** when it meets all of them.

**Fair CTL.** Fair CTL has the syntax of [CTL](/computation-tree-logic/), but its path quantifiers range over fair paths only: $s \models \mathsf{E}_f\,\psi$ if some fair path from $s$ satisfies $\psi$, and $\mathsf{A}_f\,\psi$ dually. Fairness cannot be written inside CTL, because $\mathsf{E}\mathsf{G}\mathsf{F}\,p$ is not a CTL formula, so it is built into the semantics. Let $\mathit{fair} = \mathsf{E}_f\mathsf{G}\,\mathit{true}$, the states with at least one fair path. A path is fair if and only if each of its suffixes is fair, since fairness depends only on $\mathit{inf}(\pi)$. This gives

$$\mathsf{E}_f\mathsf{X}\,\varphi = \mathsf{E}\mathsf{X}(\varphi \wedge \mathit{fair}), \qquad \mathsf{E}_f[\varphi\,\mathsf{U}\,\psi] = \mathsf{E}[\varphi\,\mathsf{U}\,(\psi \wedge \mathit{fair})],$$

and the universal operators by duality. So the only new algorithm needed is one for $\mathsf{E}_f\mathsf{G}\,\varphi$.

**Fair EG with justice only.** Let $S_\varphi$ be the set of states that satisfy $\varphi$, and $M_\varphi$ the subgraph of $M$ on $S_\varphi$. Call a strongly connected component $C$ of $M_\varphi$ *fair* if it is nontrivial (it has an edge inside it) and meets each justice set $J_1, \ldots, J_k$.

*Claim.* $s \models \mathsf{E}_f\mathsf{G}\,\varphi$ if and only if $s \in S_\varphi$ and $s$ can reach a fair component within $M_\varphi$.

*Proof.* Let $\pi$ be a fair path from $s$ in $S_\varphi$. The set $\mathit{inf}(\pi)$ is strongly connected in $M_\varphi$, since between two of its states $\pi$ goes back and forth, and it has an edge, so it lies in one nontrivial component $C$. It meets each $J_i$, so $C$ does too, and $\pi$ reaches $C$. Conversely, if $s$ reaches a fair $C$ in $M_\varphi$, pick $t_i \in C \cap J_i$. Inside $C$ there is a cycle through $t_1, \ldots, t_k$, since $C$ is strongly connected and nontrivial. The path from $s$ to $C$ followed by this cycle forever stays in $S_\varphi$ and visits each $J_i$ infinitely often. $\blacksquare$

**Fair EG with compassion.** A component $C$ can contain a compassion pair $(p, q)$ with $C \cap p \ne \emptyset$ and $C \cap q = \emptyset$. A fair path inside $C$ must then avoid $p$ from some point on, so remove the states of $p$ from $C$, split the rest into strongly connected components again, and recurse. A component is fair when it is nontrivial, meets each justice set, and each pair $(p, q)$ with $C \cap p \ne \emptyset$ has $C \cap q \ne \emptyset$; then a cycle through all of $C$ is fair. Each level of the recursion removes at least one pair for good (after it, the pair's $p$ no longer meets the component), so the depth is at most $k + 1$ for $k$ pairs. Each level works on disjoint subgraphs, so it costs $O(|M| + k|S|)$ with [Tarjan's algorithm](/tarjan-scc/), and the total is $O((k + 1)(|M| + k|S|))$ per $\mathsf{E}_f\mathsf{G}$ subformula. This is the algorithm of Clarke, Emerson and Sistla (1986) and of Emerson and Lei (1987), and it is the fairness part of the [linear-time bound for CTL](/ctl-model-checking-linear-time/).

The [Emerson-Lei algorithm](/emerson-lei-algorithm/) page gives the same set as a fixed point for justice: $\mathsf{E}_f\mathsf{G}\,\varphi = \nu Z.\, \varphi \wedge \bigwedge_i \mathsf{E}\mathsf{X}\, \mathsf{E}[\varphi\,\mathsf{U}\,(Z \wedge J_i)]$, which symbolic model checkers use.

## Examples

**Mutual exclusion with a starving process.** In the two-process structure of the [Kripke structure](/kripke-structure/) page, process 1 can enter when $\mathit{en} = w_1 \wedge y = 1$ holds, and it has entered when $c_1$ holds. The property "a waiting process 1 eventually enters", $\mathsf{AG}(w_1 \to \mathsf{AF}\,c_1)$, fails without fairness. The witness is the cycle $(w,n,1) \to (w,w,1) \to (w,c,0) \to (w,n,1)$, on which process 2 enters and leaves forever while process 1 waits.

- *Weak fairness does not help.* On the cycle, $\mathit{en}$ is false at $(w,c,0)$, so $\mathit{en}$ is not continuously true. The justice set $\neg\mathit{en} \vee c_1$ is visited infinitely often, so the cycle is weakly fair, and the property still fails.
- *Strong fairness does.* On the cycle, $\mathit{en}$ holds infinitely often and $c_1$ never does, so the compassion pair $(\mathit{en}, c_1)$ removes it. Under this pair, $\mathsf{AG}(w_1 \to \mathsf{AF}\,c_1)$ holds in the structure.

The example shows why the two notions differ: an action that is enabled only now and then can be ignored forever under weak fairness, but not under strong fairness.

**A small check of the definitions.** Take states $0, 1, 2$ with edges $0 \to 1$, $1 \to 0$, $0 \to 2$, $2 \to 2$, and let $t$ hold at $2$ only. Then $\mathsf{AF}\,t$ holds only at $2$, because the cycle $0\,1\,0\,1 \ldots$ avoids $t$. The justice set $\{1, 2\}$ does not exclude this cycle, so $\mathsf{A}_f\mathsf{F}\,t$ still holds only at $2$. The compassion pair $(\{0\}, \{2\})$ excludes it, since the cycle visits $0$ infinitely often and never $2$, and then $\mathsf{A}_f\mathsf{F}\,t$ holds at all three states. The tests of the [CTL labelling algorithm](/ctl-labelling-algorithm/) check exactly these sets.

## Where it is used

- **CTL model checking.** The [CTL labelling algorithm](/ctl-labelling-algorithm/) handles fairness with the component analysis above, and symbolic model checkers such as SMV compute fair $\mathsf{EG}$ with the fixed point of [Emerson and Lei](/emerson-lei-algorithm/).
- **LTL model checking.** In [LTL model checking](/ltl-model-checking/) fairness is a premise: check $\mathit{fair} \to \varphi$, or search the product with a [Büchi automaton](/buchi-automaton/) for an accepting cycle that also meets the justice sets. Strong fairness turns the search into a Streett emptiness test, which is again an SCC refinement.
- **Concurrency.** Weak fairness of each process is the usual assumption for [starvation freedom](/starvation-freedom/) of locks. Strong fairness is needed when a process waits on a resource that is free only now and then, as with semaphores. TLA+ writes the two as $\mathrm{WF}$ and $\mathrm{SF}$ in its specifications.
- **Probabilistic systems.** In a finite Markov chain, almost every path is strongly fair with respect to each transition, which is why [PCTL model checking](/pctl-model-checking/) of qualitative properties resembles fair CTL.

## References
