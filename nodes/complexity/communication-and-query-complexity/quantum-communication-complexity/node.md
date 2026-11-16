---
tag: 5FTAJ2
kind: concept
slug: quantum-communication-complexity
name: Quantum communication complexity
area: complexity/communication-and-query-complexity
level: research
summary: "The communication cost of a function when the two parties send qubits, or share entanglement. Some partial functions need exponentially less; set disjointness needs about the square root of n."
prereqs: [communication-model, randomized-communication-complexity, quantum-state, entanglement]
see_also: [quantum-query-complexity, disjointness-problem, inner-product-problem, equality-problem, simultaneous-message-model, superdense-coding, quantum-teleportation, information-complexity]
sources:
  - paper: doi:10.1109/SFCS.1993.366852
    title: "Andrew Chi-Chih Yao, Quantum circuit complexity, 34th IEEE Symposium on Foundations of Computer Science (FOCS 1993), pages 352-361"
    locator: the definition of quantum communication complexity (qubit messages, no prior entanglement)
  - paper: doi:10.1145/276698.276713
    title: "Harry Buhrman, Richard Cleve and Avi Wigderson, Quantum vs. classical communication and computation, 30th ACM Symposium on Theory of Computing (STOC 1998), pages 63-68"
    locator: the simulation of query algorithms by protocols, and the O(sqrt(n) log n) protocol for disjointness
  - paper: doi:10.4086/toc.2005.v001a004
    title: "Scott Aaronson and Andris Ambainis, Quantum search of spatial regions, Theory of Computing 1(4), 2005, pages 47-79"
    locator: the O(sqrt(n)) protocol for disjointness
  - paper: doi:10.1070/IM2003v067n01ABEH000422
    title: "Alexander A. Razborov, Quantum communication complexity of symmetric predicates, Izvestiya Mathematics 67(1), 2003, pages 145-159"
    locator: the Omega(sqrt(n)) lower bound for disjointness, with and without prior entanglement
  - paper: doi:10.1145/301250.301343
    title: "Ran Raz, Exponential separation of quantum and classical communication complexity, 31st ACM Symposium on Theory of Computing (STOC 1999), pages 358-367"
    locator: a partial function with an O(log n) quantum protocol and a polynomial lower bound for classical randomized protocols
  - paper: doi:10.1103/PhysRevLett.87.167902
    title: "Harry Buhrman, Richard Cleve, John Watrous and Ronald de Wolf, Quantum fingerprinting, Physical Review Letters 87(16), 2001, article 167902"
    locator: equality in the simultaneous message model with O(log n) qubits, against Theta(sqrt(n)) classical bits with private randomness
  - paper: doi:10.1016/S0304-3975(02)00377-8
    title: "Ronald de Wolf, Quantum communication and complexity, Theoretical Computer Science 287(1), 2002, pages 337-353"
    locator: the survey (the models with and without entanglement, the lower bound for inner product, the separations known in 2002)
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 2.3 (superdense coding), Section 1.3.7 (teleportation) and Chapter 12 (the Holevo bound)
---

Quantum communication complexity is the cost of computing a function $f(x, y)$ when Alice holds $x$, Bob holds $y$, and the messages are qubits instead of bits. Yao defined the model in 1993. A second model, due to Cleve and Buhrman, lets the parties share entangled qubits before the protocol starts, and they then send classical bits or qubits. The setting is the two-party [communication model](/communication-model/), and the measures sit next to the deterministic measure $D^{cc}(f)$ and the [randomized communication complexity](/randomized-communication-complexity/) $R^{cc}(f)$. Quantum messages save little for some functions, such as inner product, and a great deal for others: the [disjointness problem](/disjointness-problem/) needs only about $\sqrt n$ qubits, against $\Theta(n)$ classical bits.

## In plain words

Two people each have a long string. They want to know one fact that depends on both strings, and they pay for each piece of information that they send. In the usual setting each piece is a bit. Here each piece is a qubit, a quantum bit. A single qubit cannot carry more than one ordinary bit of information to the receiver. But the two people can use qubits to work on both strings together, in a way that ordinary messages cannot copy. For some tasks this makes the cost much smaller. To find out whether two sets have a common element, ordinary messages must be about as long as the sets, but quantum messages need only about the square root of that length. For other tasks, such as the parity of a bitwise product, quantum messages give almost no saving.

## The idea

**The model.** Alice and Bob each have a private quantum register, and there is a channel register that they pass back and forth. In each round the party with the channel applies a unitary map that depends on its own input to its private register and the channel, and then sends the channel to the other party. The cost of a protocol is the total number of qubits sent. At the end one party measures and outputs a bit. The default is two-way communication with error at most $1/3$ on every input. Write

- $Q^{cc}(f)$ for the bounded-error cost in Yao's model, with no entanglement at the start,
- $Q^{cc,*}(f)$ for the bounded-error cost when the parties share any number of entangled qubit pairs at the start, and
- $Q^{cc}_E(f)$ for the cost when the protocol must be correct with probability 1.

The randomness in $R^{cc}(f)$ must be stated. Quantum parties can make private random bits, so $Q^{cc}(f) \le R^{cc,\mathrm{priv}}(f)$. Shared [entanglement](/entanglement/) gives shared random bits when both parties measure their halves of [Bell pairs](/bell-states/), so $Q^{cc,*}(f) \le R^{cc,\mathrm{pub}}(f)$.

**Qubits against bits.** With shared entanglement, the difference between qubit messages and bit messages is at most a factor of 2. [Quantum teleportation](/quantum-teleportation/) sends one qubit with two classical bits and one Bell pair, and [superdense coding](/superdense-coding/) sends two classical bits with one qubit and one Bell pair. The Holevo bound limits the other direction: $k$ qubits cannot give the receiver more than $k$ bits of information about the sender's input, or $2k$ bits with entanglement. So quantum protocols cannot win by sending more information. They win because the messages can be in superposition over many parts of the input, which lets the parties run a quantum algorithm on both inputs together. Entanglement alone, with no messages, transmits nothing; this is the [no-communication theorem](/no-communication-theorem/).

**From queries to communication.** Buhrman, Cleve and Wigderson showed how to run a [quantum query](/quantum-query-complexity/) algorithm as a protocol. Suppose the algorithm computes $g$ on the string $z$ with $z_i = x_i \wedge y_i$. Alice keeps the state. For a query, she computes $x_i$ into a qubit and sends the index register and that qubit to Bob. Bob applies the phase $(-1)^{x_i y_i}$ and sends both back, and Alice clears the qubit. One query costs $2(\lceil \log_2 n \rceil + 1)$ qubits. So a query algorithm with $T$ queries gives a protocol with $O(T \log n)$ qubits.

**Lower bounds.** Many classical methods carry over, with changes. The discrepancy method holds for quantum protocols, and gives $\Omega(n)$ qubits for the [inner product problem](/inner-product-problem/), with or without entanglement. Razborov proved $\Omega(\sqrt n)$ for disjointness with a matrix method that uses the symmetry of the function.

## Examples

**Disjointness.** Alice holds $x$ and Bob holds $y$, both in $\{0,1\}^n$, and they ask whether some $i$ has $x_i = y_i = 1$. Classical randomized protocols need $\Theta(n)$ bits. Grover search for such an $i$, run through the simulation above, gives $O(\sqrt n \log n)$ qubits. Take $n = 1024$ and the case with at most one common element. Grover search needs $\lfloor (\pi/4)\sqrt{1024} \rfloor = 25$ queries, each query costs $2(10 + 1) = 22$ qubits, and the total is $550$ qubits. Then Alice sends the index that the search found (10 bits) and Bob replies with $y_i$ (1 bit), so the total is 561 against $n + 1 = 1025$ for the trivial protocol. For $n = 2^{20}$ the counts are $804$ queries and $33768$ qubits, against $1048577$ bits. Aaronson and Ambainis removed the $\log n$ factor and gave $O(\sqrt n)$ qubits, and Razborov proved that $\Omega(\sqrt n)$ qubits are needed, with or without entanglement. So disjointness has a quadratic gap between quantum and classical cost.

**Equality with no shared randomness.** In the [simultaneous message model](/simultaneous-message-model/), Alice and Bob each send one message to a referee and share no randomness. For the [equality problem](/equality-problem/), classical protocols need $\Theta(\sqrt n)$ bits. Buhrman, Cleve, Watrous and de Wolf gave quantum fingerprints: each party sends a state of $O(\log n)$ qubits, and the referee compares the two states with a swap test. Equal strings give equal states, and different strings give states that are almost orthogonal.

**A partial function with an exponential gap.** Raz gave a partial function, defined by a promise on the inputs, with a quantum protocol of $O(\log n)$ qubits and a classical randomized lower bound that is a power of $n$. For total functions no gap larger than polynomial is known between $Q^{cc}$ and $R^{cc}$, and whether one exists is open.

**Inner product.** For $\mathrm{IP}(x, y) = \sum_i x_i y_i \bmod 2$, quantum protocols need $\Omega(n)$ qubits, so the saving is at most a constant factor.

## Where it is used

- **Limits of distributed quantum computing.** Lower bounds in this model show which tasks gain nothing from quantum networks, such as inner product, and which gain a polynomial or exponential factor.
- **Lower bounds for other quantum models.** As in the classical case, a protocol can simulate a quantum streaming algorithm or a quantum data structure, so communication lower bounds become space or time lower bounds there. With the simulation above, a query algorithm also gives a protocol, so a communication lower bound gives a query lower bound.
- **Entanglement and nonlocality.** The model with shared entanglement measures how much entanglement can replace communication. The [CHSH game](/chsh-inequality/) is the smallest case: with no messages at all, entanglement wins a game more often than any classical strategy.

## References
