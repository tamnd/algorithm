---
tag: BJPZH5
kind: definition
slug: explicit-leader-election
name: Explicit leader election
aliases:
- Implicit vs explicit election
area: distributed/leader-election
level: intro
summary: The form of leader election in which every process learns the identifier of the leader. On a ring it costs at most n messages more than the implicit form.
prereqs: [ring-leader-election, ring-network, message-complexity]
see_also: [chang-roberts, dolev-klawe-rodeh, floodmax, peterson-leader-election, omega-failure-detector, flooding, convergecast, distributed-spanning-tree]
sources:
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 3, Section 3.1 (the leader election problem and its variants, in which the non-leaders also output) and Chapter 4, Section 4.1 (election in a general synchronous network, where all processes learn the leader)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 3, Section 3.1 (the leader election problem with elected and not-elected states)
  - book: isbn:9780521794831
    title: Gerard Tel, Introduction to Distributed Algorithms, second edition, Cambridge University Press, 2000
    locator: Chapter 7 (the election problem, and the remark that the elected process can inform the others)
---

Explicit leader election is the form of leader election in which, at the end, every process knows the identifier of the leader. In the weaker, *implicit* form, exactly one process knows that it is the leader, and the other processes need only know that they are not, or need not know anything. The two forms differ by one broadcast: on a [ring](/ring-network/) of $n$ processes the leader sends its identifier once round, which costs $n$ messages, so all the bounds of [ring election](/ring-leader-election/) hold for both forms.

## Definition

Consider a network of $n$ processes with distinct identifiers $\mathrm{id}_1, \ldots, \mathrm{id}_n$. Each process $p$ has an output variable $\mathit{status}_p \in \{\text{unknown}, \text{leader}, \text{non-leader}\}$, and in the explicit form also a variable $\mathit{lid}_p$, with no value at the start. Each variable is written at most once. An algorithm solves:

- **Implicit leader election** if in each admissible run there is exactly one process $\ell$ that eventually has $\mathit{status}_\ell = \text{leader}$, and no other process ever has status *leader*. Some authors also require that every $p \ne \ell$ eventually has $\mathit{status}_p = \text{non-leader}$; this is the form of Attiya and Welch.
- **Explicit leader election** if in addition every process $p$ eventually has $\mathit{lid}_p = \mathrm{id}_\ell$.

A process that knows $\mathrm{id}_\ell$ and its own identifier knows its status, so the explicit form implies the stronger implicit form. **Maximum finding**, or extrema finding, is the explicit form with $\ell$ the process of the largest identifier: every process learns $\max_p \mathrm{id}_p$.

**From implicit to explicit.** Given an algorithm for the implicit form, the leader sends $\langle \text{leader}, \mathrm{id}_\ell \rangle$ to all processes when it knows its status. On a unidirectional ring each process stores the value and forwards it, and the leader drops it when it returns: exactly $n$ messages. Without the return to the leader, $n - 1$ messages are enough, but then the leader does not learn that every process knows. On a network with a [spanning tree](/distributed-spanning-tree/) rooted at the leader, $n - 1$ messages are enough; by [flooding](/flooding/) on a graph with $m$ edges, at most $2m$.

## Examples and non-examples

- **Chang-Roberts without its announcement.** The process with the largest identifier receives its own identifier back and knows that it is the leader. The others never learn the result, and they cannot tell when the run is over. This is implicit election in the weak form. The [Chang-Roberts](/chang-roberts/) page adds the announcement, which makes it explicit for $n$ more messages.
- **Le Lann's algorithm.** Each identifier goes all the way round, so each process sees every identifier and computes the largest. This is explicit without an extra announcement, but it costs $n^2$ messages.
- **FloodMax.** In [FloodMax](/floodmax/) every process floods the largest identifier it has seen for a number of rounds equal to the diameter. At the end every process knows the largest identifier, so it solves explicit election.
- **Dolev-Klawe-Rodeh.** The [algorithm](/dolev-klawe-rodeh/) ends with a message that tells every process the maximum. It is explicit, and the process with the largest identifier is the leader.
- **Non-example: knowing the largest value is not knowing the leader.** In Lynch's form of [Peterson's algorithm](/peterson-leader-election/), the leader holds the largest identifier as its temporary value, but its own identifier can be different. On the ring $3, 7, 1, 5, 2$ the leader is the process with identifier 2. A process that learns "the maximum is 7" learns who would win under maximum finding, not who the leader is.
- **Non-example: eventual leaders.** The [Omega failure detector](/omega-failure-detector/) gives each process a leader that may change for some time and is the same correct process at all processes only from some unknown time on. Its output is never final, so it is not explicit election in the sense above.

## Related definitions

- **Leader election on a ring.** The [ring election problem](/ring-leader-election/) states the uniqueness and election conditions and the variants of the model.
- **Termination.** Many authors also ask that each process halts. In the explicit form a process can halt as soon as it has $\mathit{lid}_p$, but the last messages may still be in transit.
- **Broadcast and convergecast.** The step from implicit to explicit is one broadcast from the leader. If the leader must learn that all processes know, the broadcast is followed by a [convergecast](/convergecast/), or on a ring by the return of the message.
- **Message bounds.** On a ring the extra cost is $n$ messages, which is $O(n)$ next to the $\Theta(n \log n)$ messages of the election itself. So the [ring election lower bound](/ring-election-lower-bound/) holds for both forms. Proofs of this bound often work with the explicit form and transfer the result to the implicit form by this argument.

## References
