---
title: A query has a consistent coordination-free distributed implementation exactly when it is monotone
proves: [statement]
status: full
---

This is a full proof of the theorem in the form given on the main page. The model is a simplified form of the relational transducer networks of Ameloot, Neven and Van den Bussche (2013). The two directions follow their proof ideas: flooding for the "if" part, and a run that cannot tell a small input from a larger one for the "only if" part.

## The model, restated

- An *instance* is a finite set of facts. A *query* $Q$ maps each instance $I$ to an instance $Q(I)$. It is *monotone* if $I \subseteq J$ implies $Q(I) \subseteq Q(J)$.
- A *network* is a finite nonempty set $N$ of nodes. Every node can send messages to every other node. A message is a finite set of facts, possibly with a tag.
- A *program* $\Pi$ is a deterministic procedure that each node runs. A node knows its own identity, the set $N$ and its local input. In one *step*, the active node reads some subset (possibly empty) of the messages that are waiting for it, updates its local state, sends finitely many messages, and *outputs* finitely many facts. Output is never retracted.
- A *distribution* of $I$ on $N$ is a map $H$ from nodes to instances with $\bigcup_{x \in N} H(x) = I$. Node $x$ starts with local input $H(x)$.
- A *run* is a sequence of steps. A step that reads no message is a *heartbeat*. A run is *fair* if it is infinite, every node takes infinitely many steps, and every message sent is read in the end. Messages may wait for any finite time and are read in any order.
- $\Pi$ *computes* $Q$ if, for every network $N$, every instance $I$, every distribution $H$ of $I$ on $N$ and every fair run, the set of facts output by all nodes in the run is exactly $Q(I)$.
- $\Pi$ is *coordination-free* if, in addition, for every network $N$ and every instance $I$, there are a distribution $H$ of $I$ on $N$ and a finite run of heartbeats only, after which the facts output so far are exactly $Q(I)$.

Two facts about runs are used below.

**Fact A.** Every finite run can be extended to a fair run. Take the nodes in a fixed cyclic order, and let each step of the active node read all messages waiting for it. Every node then takes infinitely many steps, and every message is read at the next step of its receiver.

**Fact B.** In a run, the sequence of states and outputs of a node $x$ is fixed by $H(x)$, the identity $x$, the set $N$, and the messages that $x$ reads at each of its steps. This is because the program is deterministic and a step of $x$ depends on nothing else. In particular, if $x$ takes only heartbeats, then its states and outputs over its first $k$ steps depend only on $H(x)$, $x$ and $N$.

## Monotone implies a coordination-free implementation

Let $Q$ be monotone and computable. The *flooding program* does this at each node $x$.

1. The node keeps a set $K_x$ of known facts. At the start, $K_x = H(x)$.
2. At its first step, the node sends one message holding $H(x)$ to every other node.
3. At each step, it adds to $K_x$ all facts in the messages it reads. If this adds a new fact, it sends one message holding the new facts to every other node.
4. At the end of each step, it outputs every fact of $Q(K_x)$ that it has not output before.

**Lemma 1 (no wrong output).** In every run on a distribution of $I$, every output fact is in $Q(I)$.

*Proof.* Every message holds facts that some node knew, and every node starts with facts of $I$. By induction on the steps of the run, $K_x \subseteq I$ for every node $x$ at all times. A fact output by $x$ is in $Q(K_x)$ for the value of $K_x$ at that step, and $Q(K_x) \subseteq Q(I)$ by monotonicity. $\square$

**Lemma 2 (all output, in fair runs).** In every fair run on a distribution of $I$, every fact of $Q(I)$ is output.

*Proof.* Let $f \in I$, and let $y$ be a node with $f \in H(y)$. At its first step, $y$ sends $H(y)$ to every other node. In a fair run, $y$ takes a first step, and every other node $x$ reads this message in the end. From then on $f \in K_x$, since $K_x$ only grows. So there is a step after which $K_x = I$ for every node $x$ (there are finitely many facts and nodes). The next step of any node $x$ outputs every fact of $Q(K_x) = Q(I)$ that it has not output before. $\square$

By Lemmas 1 and 2, the facts output in every fair run are exactly $Q(I)$, so the flooding program computes $Q$.

**Lemma 3 (coordination-free).** For every network $N$ and instance $I$, take $H(x) = I$ for every node $x$. Pick any node $x$ and let it take one heartbeat. At the end of that step, $K_x = I$, so $x$ outputs all of $Q(I)$. The run has one heartbeat and no message is read. $\square$

So the flooding program is a coordination-free program that computes $Q$.

## A coordination-free implementation implies monotone

Let $\Pi$ be a coordination-free program that computes $Q$. Let $I \subseteq J$ be instances and let $f \in Q(I)$. We show $f \in Q(J)$.

**Step 1: a network with two nodes.** Coordination-freeness holds for every network, so take a network $N$ with at least two nodes.

**Step 2: the ideal run for $I$.** By coordination-freeness there are a distribution $H$ of $I$ on $N$ and a finite run $\rho$ of heartbeats only, after which the facts output are exactly $Q(I)$. So some node $x$ outputs $f$ in $\rho$, at its $k$-th step for some $k \ge 1$.

**Step 3: a distribution of $J$ that $x$ cannot tell apart.** Choose a node $y \ne x$. Define $H'$ by $H'(y) = H(y) \cup J$ and $H'(z) = H(z)$ for every node $z \ne y$. Then
$$\bigcup_{z \in N} H'(z) = I \cup J = J,$$
because $I \subseteq J$. So $H'$ is a distribution of $J$ on $N$, and $H'(x) = H(x)$.

**Step 4: the same steps of $x$.** Let $\rho'$ be the run on $H'$ in which only $x$ is active, for $k$ steps, and each step is a heartbeat. This is a valid finite run: a node may always take a step that reads no message. By Fact B, the states and outputs of $x$ in its first $k$ steps depend only on $H'(x) = H(x)$, on $x$ and on $N$. These are the same as in $\rho$, where $x$ also took only heartbeats. So $x$ outputs $f$ at its $k$-th step in $\rho'$.

**Step 5: correctness on $J$.** By Fact A, extend $\rho'$ to a fair run $\rho''$ on $H'$. Since $\Pi$ computes $Q$, the set of facts output in $\rho''$ is exactly $Q(J)$. Output is never retracted, and $f$ is output in $\rho''$. So $f \in Q(J)$.

Since $f \in Q(I)$ was arbitrary, $Q(I) \subseteq Q(J)$, and $Q$ is monotone. $\square$

## What each assumption does

- *Output is never retracted.* Step 5 needs it: a fact output early must belong to the final answer. If outputs could be retracted, a node could guess and correct later, which is the rollback that strong eventual consistency also rules out.
- *Correctness on every distribution and every fair run.* Step 5 uses a run on a distribution $H'$ that nobody chose for being convenient. A program that is correct only on some distributions or some schedules does not give the conclusion.
- *Coordination-freeness.* Step 2 needs a run in which $x$ outputs $f$ before reading anything. Without it, Step 4 fails: $x$ could wait for a message from $y$, and $y$'s extra input $J$ would change what $x$ reads. The program in the Tightness section of the main page does exactly this and computes non-monotone queries.
- *At least two nodes.* Step 3 puts the extra facts on a node other than $x$. In a network with one node, the only distribution of $J$ gives $x$ all of $J$, and $x$ can tell $I$ from $J$.
- *Knowledge of $N$ and of its own identity.* The proof allows both and does not use them, because $N$ and $x$ are the same in $\rho$ and $\rho'$. So the theorem holds whether or not nodes know the network.
- *Monotonicity and computability.* Lemma 1 uses monotonicity; the flooding program also needs to compute $Q(K_x)$, so $Q$ must be computable. $\blacksquare$
