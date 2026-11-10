---
tag: 6S7ZTH
kind: theorem
slug: ring-election-lower-bound
name: Ring election message lower bound
aliases:
- Omega(n log n) lower bound for ring election
- Burns lower bound
- Frederickson-Lynch bound
area: distributed/leader-election
level: advanced
summary: Leader election on a ring needs Omega(n log n) messages, for uniform asynchronous algorithms (Burns) and for synchronous comparison-based ones (Frederickson and Lynch).
prereqs: [ring-leader-election, ring-network, asynchronous-model, synchronous-model, message-complexity]
see_also: [hirschberg-sinclair, peterson-leader-election, dolev-klawe-rodeh, franklin, chang-roberts, anonymous-ring-impossibility, complete-network-leader-election, round-complexity]
sources:
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 3, Section 3.3.3 (Burns's lower bound by open schedules) and Section 3.4.2 (lower bounds for comparison-based and time-bounded synchronous algorithms)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Section 3.5 (TimeSlice and VariableSpeeds), Section 3.6 (comparison-based lower bound), Section 3.7 (non-comparison lower bound), Section 15.1.4 (asynchronous lower bound)
  - paper: doi:10.1145/7531.7919
    title: Greg N. Frederickson and Nancy A. Lynch, Electing a leader in a synchronous ring, Journal of the ACM 34(1), 1987
    locator: pages 98 to 115 (Omega(n log n) for comparison-based algorithms, and for time-bounded algorithms with a large identifier set)
  - paper: doi:10.1145/1634.1889
    title: Jan Pachl, Ephraim Korach and Doron Rotem, Lower bounds for distributed maximum-finding algorithms, Journal of the ACM 31(4), 1984
    locator: pages 905 to 918 (lower bounds on the average number of messages on rings)
---

Electing a leader on a [ring](/ring-network/) of $n$ processes with distinct identifiers needs $\Omega(n \log n)$ messages in the worst case, under either of two sets of hypotheses. Burns proved it in 1980 for asynchronous algorithms that do not know $n$. Frederickson and Lynch proved it in 1987 for synchronous algorithms that may know $n$ but use identifiers only by comparing them. So the $O(n \log n)$ algorithms of [Hirschberg and Sinclair](/hirschberg-sinclair/), [Peterson](/peterson-leader-election/) and [Dolev, Klawe and Rodeh](/dolev-klawe-rodeh/) are optimal up to a constant factor. Without both restrictions the bound can fail: a synchronous algorithm that computes with the identifiers can elect a leader with $n$ messages.

## Statement

Processes $p_0, \ldots, p_{n-1}$ form a ring and have distinct identifiers from an infinite ordered set, such as the integers. The algorithm is deterministic. A *run* is a schedule of the [message complexity](/message-complexity/) model: every message sent is counted once.

**Theorem 1 (Burns).** Take the [asynchronous model](/asynchronous-model/) on a bidirectional ring, oriented or not, where the processes do not know $n$ (the algorithm is *uniform*: the same code runs on rings of every size). Let $n = 2^m \ge 2$.

1. If an algorithm makes every process output the largest identifier, then for every set of $n$ identifiers there is a placement of them on the ring and a run with at least $\frac{n}{4}(\log_2 n + 1)$ messages.
2. So every leader election algorithm has a run with at least $\frac{n}{4}(\log_2 n + 1) - 2n$ messages, which is $\Omega(n \log n)$.

**Theorem 2 (Frederickson and Lynch).** Take the [synchronous model](/synchronous-model/) on a bidirectional ring. All processes start in round 1, and $n$ may be known. The algorithm is *comparison based*: a process may store, copy and send identifiers, and may compare two identifiers, but it uses them in no other way. Let $n = 2^m \ge 4$. Then on the bit-reversal ring, in which $p_i$ has the identifier whose $m$-bit binary form is that of $i$ reversed, every comparison-based leader election algorithm sends more than $\frac{n}{4} H_{n/4} \ge \frac{n}{4} \ln \frac{n}{4}$ messages, where $H_k$ is the $k$-th harmonic number.

**Theorem 3 (no comparison hypothesis).** In the synchronous model with $n$ known and positive integer identifiers, the TimeSlice algorithm elects a leader with exactly $n$ messages, in $n \cdot u_{\min}$ rounds, where $u_{\min}$ is the smallest identifier.

Frederickson and Lynch also prove $\Omega(n \log n)$ for all $n$, not only powers of 2, and for algorithms that may compute with identifiers but whose number of rounds is bounded by a function of $n$, provided the identifier set is large enough. Those extensions are stated here without proof.

## In plain words

Picture people in a circle who must pick a leader by passing notes. In one setting the notes travel at unpredictable speeds and nobody knows how big the circle is. In the other setting everyone moves in step, but people may only ask which of two names comes first.

In both settings some arrangements of names force many notes. The reason is that a part of the circle cannot tell what lies beyond it. Two half circles can each be made to waste notes, then joined, and the joined circle must waste even more notes to let the halves learn about each other. Doing this again and again gives the bound.

If people may do arithmetic on names and use waiting time as a signal, the bound goes away, but then the wait can be very long.

## Proof

### Theorem 1: pasting open runs

The proof follows Burns, as presented by Attiya and Welch and by Lynch. Assume that a process sends messages only when it starts and when it receives a message, and that each process writes its output at most once. A finite run is *complete* if no message is in transit at its end; nothing more can then happen, so in a complete run every process has written its output.

**Fact K (no news, no answer).** Let $\rho$ be a complete run on a ring $R$, and let $X$ be an arc of $R$ that does not hold the largest identifier. If no message from outside $X$ is in the causal past of a process $g \in X$, then $\rho$ is not correct.

*Proof.* Build the ring $R^*$ from $R$ by giving the processes outside $X$ new identifiers, all larger than every identifier of $R$. The events of $\rho$ whose causal past lies in $X$ form a valid run prefix of $R^*$, because each of them sees the same messages there. All events of $g$ are among them, so in $R^*$ the process $g$ writes the same output as in $\rho$. In $\rho$ this output must be the largest identifier of $R$, which is smaller than the largest identifier of $R^*$. So the run of $R^*$ is wrong, and the algorithm is not correct. $\square$

A run prefix is *open at a link* $e$ if no message is delivered over $e$ in it; messages may be sent over $e$ and stay in transit. Let $T(2) = 1$ and $T(n) = 2T(n/2) + n/4$.

**Lemma.** For every $n = 2^m \ge 2$ and every set $I$ of $n$ identifiers there is a ring with the identifiers $I$ and a run prefix that is open at some link and delivers at least $T(n)$ messages.

*Proof.* Induction on $m$.

*Base, $n = 2$.* The ring has processes $p$ and $q$ and two links. If no message is ever delivered, the run is complete and the process with the smaller identifier has heard nothing from the other one, which contradicts Fact K. So some message is delivered. Stop right after the first delivery. The prefix is open at the other link and delivers 1 message.

*Step.* Split $I$ into two sets of $n/2$ identifiers. By induction there are rings $R_1$ and $R_2$ with run prefixes $\sigma_1$ and $\sigma_2$, open at links $e_1 = \{p_1, q_1\}$ and $e_2 = \{p_2, q_2\}$, each with at least $T(n/2)$ deliveries. Remove $e_1$ and $e_2$ and add the links $e_p = \{p_1, p_2\}$ and $e_q = \{q_1, q_2\}$, so that each process keeps its ports. This gives a ring $R$ of size $n$. Since the algorithm is uniform, the same code runs on $R$, and $\sigma_1 \sigma_2$ is a run prefix of $R$ in which each process sees exactly what it saw before: no message crossed $e_1$ or $e_2$. So $\sigma_1 \sigma_2$ is open at $e_p$ and $e_q$ and delivers at least $2T(n/2)$ messages. This is the only place where uniformity is used. Call the two halves $H$ and $\bar H$, where $H$ does not hold the largest identifier.

1. Extend $\sigma_1 \sigma_2$ by starting every process that has not started and delivering messages, but never over $e_p$ or $e_q$, as long as possible. If this never stops, there are open prefixes with any number of deliveries and we are done. Otherwise call the result $\alpha$. After $\alpha$ the only messages in transit cross $e_p$ or $e_q$.
2. Let $\beta_p$ deliver, after $\alpha$, all messages except those over $e_q$, until none is left; let $\beta_q$ do the same with the roles of $e_p$ and $e_q$ exchanged. If either is infinite we are done. Let $A_p$ and $A_q$ be the sets of processes that receive a message in $\beta_p$ and in $\beta_q$.
3. Inside each half, $A_p$ is an arc that starts at the end of $e_p$ in that half, or is empty. Indeed after $\alpha$ a process can receive a message in $\beta_p$ only over $e_p$ or from a neighbour that received one earlier in $\beta_p$, since processes send only when they receive. The same holds for $A_q$ and $e_q$.

*Case 1: in some half $X$, every process lies in $A_p \cup A_q$.* The arcs $A_p \cap X$ and $A_q \cap X$ start at the two ends of $X$ and cover it, so $|A_p| + |A_q| \ge n/2$. Say $|A_p| \ge n/4$. Every process of $A_p$ receives at least one message in $\beta_p$, so the prefix $\alpha \beta_p$ is open at $e_q$ and delivers at least $2T(n/2) + n/4 = T(n)$ messages.

*Case 2: each half has a process outside $A_p \cup A_q$.* Let $g$ be such a process in $H$. Then $A_p$ and $A_q$ lie in the two arcs that remain when the two gap processes are removed, so they are disjoint, no process of $A_p$ is next to one of $A_q$, and $A_p$ holds no end of $e_q$ and $A_q$ no end of $e_p$. In $\beta_p$ every message sent goes to a neighbour, which then receives it, so it goes inside $A_p$; the processes outside $A_p$ are left as they were after $\alpha$. So $\beta_q$ can run after $\beta_p$, and $\rho = \alpha \beta_p \beta_q$ is a run. At its end no message is in transit, so $\rho$ is complete. The process $g$ takes no step after $\alpha$, and in $\alpha$ no message crossed $e_p$ or $e_q$, so its causal past lies in $H$. Fact K says that $\rho$ is not correct, a contradiction. So Case 2 cannot happen. $\square$

The recurrence gives $T(n)/n = T(n/2)/(n/2) + 1/4$, so $T(n)/n = 1/2 + (m - 1)/4$ and $T(n) = \frac{n}{4}(\log_2 n + 1)$. Every message delivered was sent, which proves part 1.

For part 2, let $E$ be a uniform leader election algorithm. Add two trips round the ring: the leader sends a token in one direction that collects the largest identifier and comes back to it, which it recognises by its own identifier, and then the leader sends the largest identifier round the ring once more; each process outputs it. The new algorithm makes every process output the largest identifier and sends at most $2n$ more messages than $E$. A run of it with at least $T(n)$ messages contains a run of $E$ with at least $T(n) - 2n$ messages, because the messages of $E$ do not depend on the added ones. $\blacksquare$

The same proof works for unidirectional rings: join the links so that each process keeps its incoming and its outgoing link.

### Theorem 2: order-equivalent neighbourhoods

Two segments of the ring of the same length are *order-equivalent* if the map that sends the $t$-th identifier of one to the $t$-th identifier of the other preserves order. For $k \le (n - 1)/2$, the *$k$-neighbourhood* of $p_i$ is the segment $p_{i-k}, \ldots, p_{i+k}$. Two states, or two messages, are *equivalent under a map* $f$ of identifiers if applying $f$ to every identifier in one gives the other. A round is *active* if at least one message is sent in it. Let $a(t)$ be the number of active rounds among rounds $1, \ldots, t$ of the run.

**Lemma A (bit-reversal ring).** Let $1 \le l \le n$ and let $2^j$ be the least power of 2 with $2^j \ge l$. On the bit-reversal ring, every segment of length $l$ is order-equivalent to at least $n / 2^j > n/(2l)$ segments, itself included.

*Proof.* Write a position as $i = b \cdot 2^j + t$ with $0 \le t < 2^j$. Reversing $m$ bits gives $\mathrm{rev}_m(i) = \mathrm{rev}_j(t) \cdot 2^{m-j} + \mathrm{rev}_{m-j}(b)$. So two identifiers whose positions have different offsets $t \ne t'$ compare as $\mathrm{rev}_j(t)$ and $\mathrm{rev}_j(t')$ do, whatever their blocks are. A segment of length $l \le 2^j$ that starts at offset $t_0$ covers the offsets $t_0, t_0 + 1, \ldots$ of one block and maybe the offsets $0, 1, \ldots$ of the next block, cyclically, and all these offsets are different. So the order type of the segment depends only on $t_0$, and the $n/2^j$ segments whose start positions are equal modulo $2^j$ are order-equivalent. Since $2^{j-1} < l$, we have $n/2^j > n/(2l)$. $\square$

**Lemma B (local view).** Suppose the $a(t)$-neighbourhoods of $p_i$ and $p_j$ are order-equivalent under the map $f$. Then after round $t$ the state of $p_i$ holds only identifiers of its $a(t)$-neighbourhood, and the states of $p_i$ and $p_j$ are equivalent under $f$.

*Proof.* Induction on $t$. Before round 1 each state holds only the process's own identifier, and all processes run the same code from the same start, with the same round number since all start together. If round $t + 1$ is not active, no process receives anything, and a comparison-based transition maps equivalent states to equivalent states. If it is active, let $k = a(t + 1) = a(t) + 1$. The new state of $p_i$ depends on its own state and on the messages of $p_{i-1}$ and $p_{i+1}$, which depend on their states after round $t$. The $(k - 1)$-neighbourhoods of $p_{i-1}, p_i, p_{i+1}$ lie in the $k$-neighbourhood of $p_i$, and $f$ maps them, preserving order, onto those of $p_{j-1}, p_j, p_{j+1}$. By induction the three states are equivalent under $f$, so the messages are, and so are the new states. $\square$

*Proof of Theorem 2.* Take a comparison-based algorithm and its run on the bit-reversal ring with $n = 2^m \ge 4$.

- **At least $n/4$ active rounds.** Let $p_i$ become the leader in round $t$. By Lemma B every $p_j$ whose $a(t)$-neighbourhood is order-equivalent to that of $p_i$ becomes the leader in round $t$ too. If $2a(t) + 1 \le n/2$, Lemma A gives at least $n / 2^j \ge 2$ such processes, and there are two leaders. So $2a(t) + 1 > n/2$, that is $a(t) \ge n/4$.
- **Many senders in each active round.** Let round $t_k$ be the $k$-th active round, $1 \le k \le n/4$, so $a(t_k - 1) = k - 1$. Some $p_i$ sends in round $t_k$, and what it sends is a function of its state after round $t_k - 1$. By Lemma B every $p_j$ whose $(k - 1)$-neighbourhood is order-equivalent to that of $p_i$ also sends a message in round $t_k$. By Lemma A with $l = 2k - 1$ there are more than $n/(2(2k - 1)) \ge n/(4k)$ of them.

Adding over $k = 1, \ldots, n/4$, the run sends more than $\sum_{k=1}^{n/4} \frac{n}{4k} = \frac{n}{4} H_{n/4}$ messages. $\blacksquare$

### Theorem 3: TimeSlice

Run on a unidirectional synchronous ring with $n$ known. Rounds are grouped into phases of $n$ rounds; phase $v$ is rounds $(v - 1)n + 1, \ldots, vn$. At the start of phase $v$, the process with identifier $v$ sends $v$, unless it has already received a message. Every process that receives a message forwards it, and the process that gets its own identifier back is the leader. In phases $1, \ldots, u_{\min} - 1$ nothing is sent. In phase $u_{\min}$ the identifier $u_{\min}$ goes round the ring in $n$ rounds; every other process receives it before its own phase starts, so it never sends its identifier. So exactly $n$ messages are sent, and the leader knows after $n \cdot u_{\min}$ rounds. $\blacksquare$

The algorithm is not comparison based: it uses the value $v$ as a time. Its number of rounds is not bounded by any function of $n$.

## Consequences

- **Optimal ring algorithms.** [Hirschberg-Sinclair](/hirschberg-sinclair/), [Franklin](/franklin/), [Peterson](/peterson-leader-election/) and [Dolev-Klawe-Rodeh](/dolev-klawe-rodeh/) use $O(n \log n)$ messages, so they are optimal up to a constant factor. [Chang-Roberts](/chang-roberts/) uses $\Theta(n^2)$ messages in the worst case and is not.
- **Knowing $n$ does not help comparison-based algorithms.** An asynchronous comparison-based algorithm run in lock step, with every message delayed one round, is a synchronous comparison-based algorithm with at most as many messages, so Theorem 2 also applies to it, even when $n$ is known.
- **Asynchrony costs no more messages than synchrony for these algorithms.** Both models give $\Theta(n \log n)$ for comparison-based algorithms.
- **Other networks.** On complete networks the same order of messages is needed; see [leader election in complete networks](/complete-network-leader-election/). On trees, $O(n)$ messages are enough, because there is no cycle to go round.

## Tightness

- **Order.** The bounds are tight up to constants: there are $O(n \log n)$ algorithms in all the models of the theorems.
- **Constants.** The constants here are $1/4$ (Theorem 1, with $\log_2$) and $1/4$ (Theorem 2, with $\ln$), while the best known unidirectional algorithms use about $1.36\, n \log_2 n$ messages. The exact constant for the worst case is not settled by these proofs.
- **The comparison hypothesis is needed** in the synchronous case: Theorem 3 uses $n$ messages. For $n$ unknown, Lynch's VariableSpeeds algorithm uses $O(n)$ messages and a number of rounds exponential in $u_{\min}$.
- **Time bound instead of comparisons.** Frederickson and Lynch show that if the number of rounds is bounded by a function of $n$ alone and the identifier set is large enough, any algorithm behaves like a comparison-based one on some subset of identifiers, by a Ramsey argument, so $\Omega(n \log n)$ holds again.
- **The average case.** Pachl, Korach and Rotem gave lower bounds on the average number of messages over all orders of the identifiers. On unidirectional rings their bound is met by Chang-Roberts.
- **Checks.** The tests in the implementation folder check Lemma A for every segment length on bit-reversal rings with up to 128 processes, the closed form of $T(n)$, that synchronous Chang-Roberts sends at least the bound of Theorem 2 on the bit-reversal ring, and that TimeSlice sends exactly $n$ messages.

## History

Hirschberg and Sinclair asked in 1980 whether $O(n \log n)$ messages are enough, and gave such an algorithm for bidirectional rings. In the same year Burns, in a technical report at Indiana University, proved the matching $\Omega(n \log n)$ lower bound for uniform asynchronous algorithms. Pachl, Korach and Rotem studied average-case bounds in 1984. Frederickson and Lynch published the synchronous bounds in the Journal of the ACM in 1987: for comparison-based algorithms, and, with Ramsey theory, for time-bounded ones. They also showed that the bound fails without these restrictions, by algorithms like TimeSlice that use the identifiers as times.

## References
