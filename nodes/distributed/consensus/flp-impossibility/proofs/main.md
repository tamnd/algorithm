---
title: No deterministic consensus protocol is totally correct in spite of one crash
proves: [statement]
status: full
---

This is the proof of Fischer, Lynch and Paterson (1985), with the same three lemmas, written out step by step.

**The model.** There are $n \ge 2$ processes. Process $p$ has a one-bit input register $x_p$, an output register $y_p$ with values in $\{b, 0, 1\}$, and other internal storage. The output starts as $b$ and is *write-once*: once $y_p \in \{0, 1\}$, the transition function does not change it. Then $p$ has *decided* $y_p$. The transition function of each process is deterministic.

The *message buffer* is a multiset of messages $(p, m)$, which means "$m$ is sent to $p$". The operation $\mathrm{send}(p, m)$ puts $(p, m)$ in the buffer. The operation $\mathrm{receive}(p)$ either removes some $(p, m)$ from the buffer and returns $m$, or returns the null value $\varnothing$ and leaves the buffer as it is. The choice is free, subject only to the fairness rule of admissible runs below.

A *configuration* is the internal state of each process plus the buffer. An *initial configuration* has each process in an initial state, which holds its input, and an empty buffer. A *step* of $p$ is one $\mathrm{receive}(p)$ that returns some $m$, then a deterministic change of state of $p$ that depends on its state and $m$, then a finite set of sends. A step is fixed by the configuration and the *event* $e = (p, m)$, and its result is written $e(C)$. The event $(p, m)$ with $m \ne \varnothing$ is *applicable* to $C$ if $(p, m)$ is in the buffer of $C$; the event $(p, \varnothing)$ is always applicable. A *schedule* $\sigma$ is a finite or infinite sequence of events, and $\sigma(C)$ is the result of applying them in order, when each is applicable in turn. $C'$ is *reachable* from $C$ if $C' = \sigma(C)$ for a finite schedule $\sigma$. A configuration is *accessible* if it is reachable from some initial configuration.

A configuration $C$ *has decision value* $v$ if $y_p = v$ for some process $p$ in $C$.

**Correctness.** A protocol is *partially correct* if (1) no accessible configuration has more than one decision value, and (2) for each $v \in \{0, 1\}$, some accessible configuration has decision value $v$. In a run, a process is *nonfaulty* if it takes infinitely many steps, and *faulty* otherwise. A run is *admissible* if at most one process is faulty and each message sent to a nonfaulty process is received in the end. A run is *deciding* if some process decides in it. A protocol is *totally correct in spite of one fault* if it is partially correct and each admissible run is deciding.

Clause (2) is the validity condition: it rules out the protocol that always decides 0. Termination asks only that *some* process decide, so the theorem is stronger than one in which all correct processes must decide.

**Theorem.** No consensus protocol is totally correct in spite of one fault.

Assume, for a contradiction, that $P$ is totally correct in spite of one fault.

**Valence.** For a configuration $C$, let $V(C)$ be the set of decision values of the configurations reachable from $C$. Admissible runs from $C$ exist (for example, run the processes in turn, each receiving its oldest message), and each one decides, so $V(C) \ne \emptyset$. $C$ is *bivalent* if $V(C) = \{0, 1\}$, and *univalent* otherwise: *0-valent* if $V(C) = \{0\}$ and *1-valent* if $V(C) = \{1\}$. If $C'$ is reachable from $C$, then $V(C') \subseteq V(C)$, because reachability is transitive.

**Fact.** If $C$ has decision value $v$, then $C$ is $v$-valent. Each configuration reachable from $C$ keeps the decided output registers, because they are write-once, so it has decision value $v$. By partial correctness, part (1), it has no other decision value. So $V(C) = \{v\}$. In particular, a bivalent configuration has no decision value: no process has decided in it.

**Lemma 1 (commutativity).** Let $C$ be a configuration, and let $\sigma_1$ and $\sigma_2$ be finite schedules from $C$ such that the set of processes that take steps in $\sigma_1$ and the set that take steps in $\sigma_2$ are disjoint. Then $\sigma_2$ is applicable to $\sigma_1(C)$, $\sigma_1$ is applicable to $\sigma_2(C)$, and $\sigma_2(\sigma_1(C)) = \sigma_1(\sigma_2(C))$.

*Proof.*

1. An event $(p, m)$ of $\sigma_2$ reads and changes only the state of $p$, removes only the message $(p, m)$, and adds messages to the buffer.
2. The schedule $\sigma_1$ does not change the state of any process of $\sigma_2$, and it removes only messages addressed to processes of $\sigma_1$. So each message that $\sigma_2$ receives in $C$ is still in the buffer after $\sigma_1$, and each process of $\sigma_2$ is in the same state after $\sigma_1$ as in $C$. By induction on the length of $\sigma_2$, $\sigma_2$ is applicable to $\sigma_1(C)$, and each process of $\sigma_2$ goes through the same states and sends the same messages as it does from $C$.
3. In $\sigma_2(\sigma_1(C))$, each process of $\sigma_1$ has the state it has in $\sigma_1(C)$, each process of $\sigma_2$ has the state it has in $\sigma_2(C)$, and the other processes have their states in $C$. The buffer is the buffer of $C$, minus the messages that $\sigma_1$ and $\sigma_2$ receive, plus the messages that they send. Multiset sums and differences do not depend on the order.
4. By symmetry, the same holds for $\sigma_1(\sigma_2(C))$. So the two configurations are equal. $\square$

**Lemma 2 (a bivalent initial configuration).** $P$ has a bivalent initial configuration.

*Proof.*

1. Assume that each initial configuration is univalent.
2. By partial correctness, part (2), some accessible configuration has decision value 0, so some initial configuration reaches a decision value 0 and is 0-valent. In the same way some initial configuration is 1-valent.
3. Two initial configurations are *adjacent* if they differ only in the input of one process. Any two initial configurations are joined by a chain of adjacent ones, which changes one input at a time. Along a chain from a 0-valent to a 1-valent initial configuration, all configurations are univalent, so there are adjacent $C_0$ and $C_1$ with $C_0$ 0-valent and $C_1$ 1-valent. Let $p$ be the process whose input differs.
4. Take an admissible run from $C_0$ in which $p$ takes no step. It exists, and it is admissible, because only $p$ is faulty and the others can be run fairly. By total correctness it is deciding. Let $\sigma$ be a finite prefix of its schedule after which some process has decided some value $v$.
5. $\sigma$ has no event of $p$. So $\sigma$ is applicable to $C_1$, and $\sigma(C_0)$ and $\sigma(C_1)$ differ only in the state of $p$, by induction on the length of $\sigma$: the other processes start in the same states, get the same messages, and so go through the same states. The process that decides in $\sigma(C_0)$ is not $p$, because $p$ takes no step, so it decides $v$ in $\sigma(C_1)$ too.
6. So $v \in V(C_0) = \{0\}$ and $v \in V(C_1) = \{1\}$. This is a contradiction. $\square$

**Lemma 3 (a step that keeps bivalence).** Let $C$ be a bivalent configuration and let $e = (p, m)$ be an event applicable to $C$. Let $\mathcal{C}$ be the set of configurations reachable from $C$ by schedules in which $e$ does not occur, and let $\mathcal{D} = e(\mathcal{C}) = \{e(E) : E \in \mathcal{C}\}$. Then $\mathcal{D}$ contains a bivalent configuration.

*Proof.*

1. $e$ is applicable to each $E \in \mathcal{C}$. If $m = \varnothing$ this always holds. If $m \ne \varnothing$, the message $(p, m)$ is in the buffer of $C$ and only the event $e$ can remove it, and $e$ does not occur on the way from $C$ to $E$. So $\mathcal{D}$ is well defined.
2. Assume that $\mathcal{D}$ has no bivalent configuration. Then each $D \in \mathcal{D}$ is univalent.
3. *$\mathcal{D}$ holds a 0-valent and a 1-valent configuration.* Fix $i \in \{0, 1\}$. $C$ is bivalent, so some configuration $E_i$ with decision value $i$ is reachable from $C$, and $E_i$ is $i$-valent by the Fact. If $E_i \in \mathcal{C}$, let $F_i = e(E_i) \in \mathcal{D}$. Then $F_i$ is reachable from $E_i$, so $V(F_i) \subseteq \{i\}$, and $F_i$ is $i$-valent. If $E_i \notin \mathcal{C}$, then $e$ occurs in a schedule from $C$ to $E_i$. Cut that schedule just after its first $e$: the cut point is a configuration $F_i \in \mathcal{D}$ from which $E_i$ is reachable. So $i \in V(F_i)$, and $F_i$ is univalent, so it is $i$-valent.
4. *There are neighbours $C_0, C_1 \in \mathcal{C}$ with $e(C_0)$ 0-valent and $e(C_1)$ 1-valent.* Two configurations are *neighbours* if one is reached from the other by one step. Let $G \in \mathcal{C}$ with $e(G)$ of valence $1 - j$, where $e(C)$ is $j$-valent; such a $G$ exists by step 3. The schedule from $C$ to $G$ has no event $e$, so every configuration on it is in $\mathcal{C}$. Along this path, the valence of $e(\cdot)$ starts at $j$ and ends at $1 - j$, so it changes between two consecutive configurations. Name them so that $e(C_0)$ is 0-valent and $e(C_1)$ is 1-valent. Then $C_1 = e'(C_0)$ or $C_0 = e'(C_1)$ for one event $e' = (p', m')$. By symmetry of the argument below, assume $C_1 = e'(C_0)$. Let $D_0 = e(C_0)$ and $D_1 = e(C_1)$.
5. *Case $p' \ne p$.* By Lemma 1, $D_1 = e(e'(C_0)) = e'(e(C_0)) = e'(D_0)$. So $D_1$ is reachable from $D_0$, and $V(D_1) \subseteq V(D_0) = \{0\}$. But $D_1$ is 1-valent. This is a contradiction.
6. *Case $p' = p$.* Take an admissible run from $C_0$ in which $p$ takes no step. By total correctness it is deciding. Let $\sigma$ be a finite prefix of its schedule that reaches a configuration $A = \sigma(C_0)$ with a decision value. $A$ is univalent by the Fact. The schedule $\sigma$ has no step of $p$, and $e$ and $e'$ are steps of $p$. By Lemma 1, $\sigma(D_0) = \sigma(e(C_0)) = e(\sigma(C_0)) = e(A)$, and $\sigma(D_1) = \sigma(e(e'(C_0))) = e(e'(\sigma(C_0))) = e(e'(A))$. The first is reachable from the 0-valent $D_0$, so it is 0-valent. The second is reachable from the 1-valent $D_1$, so it is 1-valent. Both are reachable from $A$, so $A$ is bivalent. This is a contradiction.
7. Both cases give a contradiction, so $\mathcal{D}$ contains a bivalent configuration. $\square$

**Proof of the theorem.** We build an admissible run in which no process ever decides.

1. Put the processes in a queue, in any order. Order the messages in the buffer by the time they were sent, oldest first.
2. The run goes in stages. In each stage, let $p$ be the process at the head of the queue, and let $m$ be the oldest message to $p$ in the buffer, or $\varnothing$ if there is none. The stage ends with the event $e = (p, m)$, and then $p$ goes to the back of the queue.
3. By Lemma 2, start at a bivalent initial configuration. At the start of a stage the configuration $C$ is bivalent. The event $e$ of the stage is applicable to $C$. By Lemma 3, there is a bivalent configuration $C' = e(E)$ with $E$ reachable from $C$ by a schedule without $e$. The stage applies that schedule and then $e$, and ends at the bivalent $C'$.
4. There are infinitely many stages, and each one ends bivalent. A bivalent configuration has no decision value, by the Fact. So no process decides in this run.
5. The run is admissible, and in fact no process is faulty. Each process reaches the head of the queue infinitely often, so it takes infinitely many steps. A message $(p, m)$ that is sent at some time has finitely many older messages to $p$, and each stage of $p$ removes the oldest one, so $(p, m)$ is received within finitely many stages of $p$.
6. So $P$ has an admissible run that is not deciding, and $P$ is not totally correct in spite of one fault. This contradicts the assumption. $\blacksquare$

**Where the fault is used.** The run of the theorem has no faulty process. The possibility of one crash is used only inside Lemmas 2 and 3, in the step "take an admissible run in which $p$ takes no step". Total correctness promises that such a run decides, and this promise is what the proof turns against the protocol.
