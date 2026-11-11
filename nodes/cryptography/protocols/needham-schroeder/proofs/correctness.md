---
title: Soundness and completeness of the bounded Dolev-Yao search
proves: [correctness, termination]
status: full
---

We use the notation and the line numbers of the page. A *scenario* is a finite list of sessions, each an initiator run of an honest agent with a fixed partner or a responder run of an honest agent. A *state* is a pair $(S, K)$: the local state of each session, and the set $K$ of terms that the intruder knows, closed under analysis. Terms are atoms, tuples and encryptions $\{m\}_{pk(X)}$. The intruder starts with all agent names, its nonce $N_i$, all public keys, and its own private key.

**The model.** An *execution* is a sequence of events. A send event of a session adds the sent message to the intruder's knowledge. A receive event of a session is allowed when the received message matches the session's expected pattern with typed values (nonces for nonce variables, agent names for agent variables) and the intruder can deduce it from what it knows. The deduction relation $K_0 \vdash t$ is the least relation with: $t \in K_0$ gives $K_0 \vdash t$; from $K_0 \vdash (t_1, \ldots, t_n)$ follows $K_0 \vdash t_j$; from $K_0 \vdash \{m\}_{pk(I)}$ follows $K_0 \vdash m$; from $K_0 \vdash t_1, \ldots, K_0 \vdash t_n$ follows $K_0 \vdash (t_1, \ldots, t_n)$; and from $K_0 \vdash m$ follows $K_0 \vdash \{m\}_{pk(X)}$ for every agent $X$. An *attack* is an execution that reaches a state where a goal fails.

**Lemma 1 (deduction is analysis then synthesis).** For a finite set $K_0$, $K_0 \vdash t$ holds if and only if $\mathrm{derive}(\mathrm{close}(K_0), t)$ returns true.

*Proof.* If direction. Each term that close adds in line L12 is a part of a tuple or the body of an encryption under $pk(I)$, both deducible by the rules. Each step of derive in line L13 is a composition rule. So derive true implies $K_0 \vdash t$.

Only if direction. Take a deduction tree of $K_0 \vdash t$ of least size. Suppose some decomposition step (a projection or a decryption) has as its premise a term that was made by a composition step. A projection of a tuple made from $t_1, \ldots, t_n$ gives a $t_j$ that already has a smaller tree, and a decryption of $\{m\}_{pk(I)}$ made from $m$ gives $m$, which already has a smaller tree. In both cases the tree can be made smaller, against the choice. So in a least tree, every decomposition step acts on a term that is in $K_0$ or that was itself made by decomposition. Hence all decompositions are at the top of the tree, near the leaves, and they produce terms that close adds. The steps below them are compositions, which derive follows. So derive returns true. $\square$

**Lemma 2 (one intruder nonce suffices).** If an attack exists in which the intruder uses fresh atoms of its own, an attack exists in which it uses only the atom $N_i$.

*Proof.* Map each atom that the intruder made to $N_i$ and keep all other atoms. Deduction is preserved: the map sends each rule instance to a rule instance. The honest agents only test whether a received atom is equal to one of their own nonces or names, and the map does not change their own atoms and does not make an intruder atom equal to an honest one. So each receive event stays allowed, and each goal that failed still fails, because the goals only speak of honest nonces and names. $\square$

**Theorem 3 (soundness).** If the search returns a trace in line L5, the trace is an attack.

*Proof.* Each pushed state comes from a predecessor by one send (line L7) or by one receive followed by the reply (line L10). A receive is pushed only when derive is true on the closed knowledge, which by Lemma 1 means the intruder can deduce the message, and the message has the pattern's form with typed values. So the trace is an execution. The search returns it only when a goal fails in its last state (line L5). $\square$

**Theorem 4 (completeness within the bound).** If an attack exists for the scenario in the typed model, the search returns some attack.

*Proof.* By Lemma 2 we may take an attack in which all intruder atoms are $N_i$. Then each received value is a nonce of the scenario or $N_i$, or an agent name, which are exactly the values that line L9 tries. By Lemma 1 each receive of the attack passes the test of line L10 in the state reached so far. So each step of the attack is one of the transitions that lines L6 to L10 push, and the states of the attack are reachable in the graph that the search explores. The search is a depth-first search with an explicit stack, which visits every state reachable from the start, except that it skips a state already visited in line L4. Skipping is safe because the set of transitions and the goal test depend only on the state $(S, K)$, not on the path that reached it. So the search reaches the first state on the attack where a goal fails, or an earlier failing state, and returns there. $\square$

**Theorem 5 (termination).** The search stops.

*Proof.* Each session takes at most two steps and binds at most two values from finite sets, so it has finitely many local states. The intruder knowledge is a function of the session states, because it is the closure of the initial knowledge and of the messages that the sessions have sent, and each sent message is fixed by the session's state. So there are finitely many states, each is expanded at most once, and each expansion pushes finitely many successors. $\square$

Theorems 3 and 4 hold for one scenario. A result of no attack says nothing about scenarios with more sessions or about an untyped model, in which an agent could accept a nonce in place of a name. $\blacksquare$
