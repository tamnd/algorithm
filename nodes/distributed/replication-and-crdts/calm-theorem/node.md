---
tag: 6GH3BT
kind: theorem
slug: calm-theorem
name: CALM theorem
aliases:
- consistency as logical monotonicity
- CALM
area: distributed/replication-and-crdts
level: research
summary: A query has a consistent, coordination-free distributed implementation exactly when it is monotone, that is, when more input never retracts an output.
prereqs: [datalog, eventual-consistency]
see_also: [crdt, state-based-crdt, join-semilattice, strong-eventual-consistency, cap-theorem, semi-naive-evaluation, crdt-convergence-theorem, consistency-models]
sources:
  - paper: "Joseph M. Hellerstein, The declarative imperative, experiences and conjectures in distributed logic, SIGMOD Record 39(1), 2010"
    title: Joseph M. Hellerstein, The declarative imperative, experiences and conjectures in distributed logic, SIGMOD Record 39(1), 2010
    locator: the section on conjectures, which states the CALM conjecture that consistent, coordination-free programs are exactly the monotonic ones
  - paper: "Tom J. Ameloot, Frank Neven and Jan Van den Bussche, Relational transducers for declarative networking, Journal of the ACM 60(2), 2013, first in PODS 2011"
    title: Tom J. Ameloot, Frank Neven and Jan Van den Bussche, Relational transducers for declarative networking, Journal of the ACM 60(2), 2013
    locator: the model of transducer networks with horizontal distributions and fair runs, the definitions of consistency, coordination-freeness and obliviousness, and the main theorem that coordination-free computation captures exactly the monotone queries
  - paper: "Tom J. Ameloot, Bas Ketsman, Frank Neven and Daniel Zinn, Weaker forms of monotonicity for declarative networking, a more fine-grained answer to the CALM-conjecture, ACM PODS 2014"
    title: Tom J. Ameloot, Bas Ketsman, Frank Neven and Daniel Zinn, Weaker forms of monotonicity for declarative networking, PODS 2014
    locator: policy-aware transducer networks, in which nodes know the distribution policy, and the weaker forms of monotonicity that they capture
  - paper: "Joseph M. Hellerstein and Peter Alvaro, Keeping CALM, when distributed consistency is easy, Communications of the ACM 63(9), 2020"
    title: Joseph M. Hellerstein and Peter Alvaro, Keeping CALM, when distributed consistency is easy, Communications of the ACM 63(9), 2020
    locator: the informal statement of the theorem, the examples of deadlock detection and garbage collection, and the relation to CRDTs, Bloom and coordination avoidance
  - paper: "Peter Alvaro, Neil Conway, Joseph M. Hellerstein and William R. Marczak, Consistency analysis in Bloom, a CALM and collected approach, CIDR 2011"
    title: Peter Alvaro, Neil Conway, Joseph M. Hellerstein and William R. Marczak, Consistency analysis in Bloom, CIDR 2011
    locator: the Bloom language and its program analysis, which finds the points of order where non-monotone operations follow asynchronous communication
---

The CALM theorem, short for *consistency as logical monotonicity*, says which distributed computations can give a consistent answer without coordination. A computation from inputs to outputs has a coordination-free implementation, in which no node ever waits to hear from others before it answers, exactly when it is *monotone*: adding input facts can only add output facts, never take one away. Hellerstein stated it as a conjecture in 2010, and Ameloot, Neven and Van den Bussche proved it in 2011 for a model of networks of relational transducers. It explains why [CRDTs](/crdt/) and grow-only data need no coordination, and where coordination is unavoidable.

## Statement

**Model** (a simplified form of the model of Ameloot, Neven and Van den Bussche).

- An *instance* is a finite set of facts. A *query* $Q$ maps each instance $I$ to an instance $Q(I)$. $Q$ is *monotone* if $I \subseteq J$ implies $Q(I) \subseteq Q(J)$.
- A *network* is a finite nonempty set $N$ of nodes that can all send messages to each other. The input $I$ is spread over the nodes by a *distribution* $H$, a map from nodes to instances with $\bigcup_{x \in N} H(x) = I$. Facts may be on more than one node.
- Every node runs the same deterministic *program* $\Pi$. A node knows its identity, the set $N$ and its local input. In one step, it reads some of the messages waiting for it, possibly none, changes its state, sends messages and outputs facts. Output is never retracted. A step that reads no message is a *heartbeat*.
- A run is *fair* if every node takes infinitely many steps and every message is read in the end. Messages can wait any finite time and arrive in any order.
- $\Pi$ *computes* $Q$ if, for every network, every input $I$, every distribution of $I$ and every fair run, the facts output by all nodes together are exactly $Q(I)$. This is the *consistency* of CALM: the answer does not depend on where the data is or on how messages are delayed.
- $\Pi$ is *coordination-free* if, in addition, for every network and every input $I$ there are a distribution of $I$ and a finite run of heartbeats only that already outputs all of $Q(I)$. So when the data is placed well, no communication is needed at all; communication that is needed even then is coordination.

**Theorem (CALM).** A computable query $Q$ is computed by some coordination-free program if and only if $Q$ is monotone.

Ameloot, Neven and Van den Bussche also proved that the monotone queries are exactly those computed by *oblivious* programs, in which nodes know neither their identity nor the set of nodes.

## In plain words

Some questions have answers that only grow as you learn more facts. "Is there a path from A to B?" is one: once you find a path, more roads never remove it. Other questions can flip: "Is there no path from A to B?" can be true now and false once one more road is known.

For the first kind, a computer can answer as soon as it knows enough, even if more news is still on its way. It never has to take an answer back, so it never waits for others.

For the second kind, a computer can only say "yes" after it is sure that no more news can arrive. Being sure means asking every other computer, and that waiting is coordination.

The CALM theorem says this split is exact: a question can be answered without coordination if and only if it is of the first kind.

## Proof

The full proof is in the proof file. Here is its plan.

*If $Q$ is monotone.* Use *flooding*. Each node keeps the set $K$ of facts it knows, starting with its local input. It sends every fact it learns to every other node, and after each step it outputs $Q(K)$. Since $K \subseteq I$ at all times, monotonicity gives $Q(K) \subseteq Q(I)$, so no output is ever wrong. In a fair run, every node learns all of $I$ in the end, so all of $Q(I)$ is output. If every node gets all of $I$ as local input, one heartbeat outputs $Q(I)$, so the program is coordination-free.

*If a coordination-free program computes $Q$.* Let $I \subseteq J$ and $f \in Q(I)$. Take a network with two or more nodes and a distribution $H$ of $I$ with a run of heartbeats only in which some node $x$ outputs $f$. Give the extra facts of $J$ to a node $y \ne x$ and leave the input of $x$ unchanged. Node $x$ takes the same heartbeats and, since it reads no message, it cannot tell $I$ from $J$, so it outputs $f$ again. The program is correct on $J$ in every fair run and never retracts output, so $f \in Q(J)$. Hence $Q(I) \subseteq Q(J)$.

## Consequences

- **Monotone programs need no coordination.** [Datalog](/datalog/) without negation is monotone, so recursive queries such as reachability and transitive closure can be evaluated by nodes that exchange facts in any order, for example by distributed [semi-naive evaluation](/semi-naive-evaluation/), and output answers as soon as they are derived.
- **Non-monotone steps are where coordination goes.** Negation, set difference, "for all", and aggregates such as an exact count or a minimum over all data are not monotone. Hellerstein and Alvaro contrast distributed deadlock detection, which is monotone because a cycle of waiting stays a cycle, with distributed garbage collection, which is not, because "no reference to this object exists" can be broken by a reference that has not arrived yet.
- **Program analysis.** The Bloom language checks programs for *points of order*, places where a non-monotone operator reads data that came through asynchronous communication. Only those places need coordination, such as a barrier, a consensus round or sealing a set of inputs.
- **Lattices and CRDTs.** Bloom^L generalizes from sets of facts to user-defined join-semilattices. A [state-based CRDT](/state-based-crdt/) is monotone in this sense: its state only goes up in a [join-semilattice](/join-semilattice/), which is why it converges without coordination, as the [CRDT convergence theorem](/crdt-convergence-theorem/) shows. A read is safe without coordination when it is itself a monotone function of the state, such as "the counter is at least 10"; a read of the exact current value is not.
- **Availability.** A coordination-free program answers during a network partition, so by the [CAP theorem](/cap-theorem/) its outputs cannot be linearizable reads of changing data. CALM says what such programs can still compute deterministically: exactly the monotone queries.

## Tightness

- **Non-monotone queries need coordination, but are computable with it.** If nodes know the set of nodes, every computable query has a consistent program. Each node sends its whole local input in one message to every other node. A node that has read one such message from every other node knows all of $I$ and outputs $Q(I)$. Any run that outputs $Q(I)$ for a nonempty answer then reads messages, unless the network has one node; for a non-monotone query no distribution avoids this, by the theorem. This is the coordination that CALM counts.
- **Two nodes are needed.** In a network of one node, every query is computed without messages. The theorem quantifies over all networks, and the proof uses one with two or more nodes.
- **Output must be final.** If a program may retract output, it can output guesses and correct them, which makes every query look coordination-free until the answer settles. The theorem is about programs whose outputs are never withdrawn, which matches the no-rollback idea of [strong eventual consistency](/strong-eventual-consistency/).
- **Knowing more about the data placement helps.** Ameloot, Ketsman, Neven and Zinn (2014) let nodes know the *distribution policy*, the rule that says which node holds which facts. Then a node can know that it has all facts about some value, and some non-monotone queries become coordination-free. They capture these larger classes with weaker forms of monotonicity, in which $Q(I) \subseteq Q(J)$ is required only when $J$ adds facts of particular kinds to $I$.
- **Consistency of outputs, not of memory.** The consistency in CALM is that the result is a deterministic function of the whole input. It is not a read/write [consistency model](/consistency-models/), and it says nothing about a service whose clients keep reading and writing, unless the service is described as a query over the log of all requests.

## History

Hellerstein stated the CALM conjecture in his PODS 2010 keynote, published in SIGMOD Record in 2010, together with related conjectures about time and coordination in declarative distributed programs. Alvaro, Conway, Hellerstein and Marczak built the Bloom language and its monotonicity analysis on it in 2011. Ameloot, Neven and Van den Bussche formalized the conjecture with relational transducer networks and proved it at PODS 2011, with the journal version in 2013. Ameloot, Ketsman, Neven and Zinn refined it for nodes that know the distribution policy in 2014. Conway et al. extended the programming model from sets to lattices in Bloom^L in 2012, which links CALM to CRDTs. Hellerstein and Alvaro gave an overview for a general audience in Communications of the ACM in 2020.

## References
