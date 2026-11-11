---
tag: A3BXW7
kind: abstract-type
slug: peer-sampling-service
name: Peer sampling service
aliases:
- random peer sampling service
area: distributed/gossip
level: advanced
summary: A service at every node whose getPeer operation returns a peer that should look like a uniform random live node, the building block of gossip protocols.
prereqs: [gossip-protocol, random-peer-sampling, churn]
see_also: [random-peer-sampling, newscast, cyclon, scamp, hyparview, lpbcast, membership-management, gossip-protocol]
sources:
  - paper: doi:10.1145/1275517.1275520
    title: Márk Jelasity, Spyros Voulgaris, Rachid Guerraoui, Anne-Marie Kermarrec and Maarten van Steen, Gossip-based peer sampling, ACM Transactions on Computer Systems 25(3), article 8, 2007
    locator: the service interface init and getPeer, the generic protocol with peer selection, view selection with the parameters H and S, and view propagation, and the experimental findings on randomness, self-healing and in-degree
  - paper: "Márk Jelasity, Rachid Guerraoui, Anne-Marie Kermarrec and Maarten van Steen, The peer sampling service: experimental evaluation of unstructured gossip-based implementations, Middleware 2004"
    locator: the first statement of the service and of the generic framework
---

A peer sampling service is a service at every node of a large network whose main operation, getPeer, returns the address of another node, and the returned nodes should look like independent uniform samples of the live nodes. Jelasity, Voulgaris, Guerraoui, Kermarrec and van Steen (2007) named it as the common building block under [gossip protocols](/gossip-protocol/), which all assume that a node can contact a random peer. A real implementation keeps a small partial view of $c$ node descriptors at each node and refreshes it by gossip, so the samples are only close to uniform. [Newscast](/newscast/) and [Cyclon](/cyclon/) are instances of the generic gossip framework from the same paper.

## In plain words

Many gossip methods start each step with the same instruction: pick a random member of the group and talk to it. In a group of millions of computers, no computer knows the full member list, and the list changes all the time.

A peer sampling service fills this gap. Each computer asks the service for "someone at random", and the service answers with a name. Inside, the service keeps a short list of names, a few dozen at most. Now and then two computers swap parts of their lists, so the lists stay fresh and mixed.

The answers are not perfectly random. Names that a computer got recently tend to be similar, and the lists of neighbours overlap. In practice they are random enough for gossip, and the service removes crashed computers and adds new ones without any central list.

## Operations

| operation | what it does |
|---|---|
| `init()` | starts the service at a joining node. The node needs the address of at least one node that is already in the overlay. |
| `getPeer()` | returns the address of a node other than the caller. |

The service is a local object: both operations run at the calling node without a round trip. All network work happens in the background, in the gossip protocol that maintains the view.

**The generic implementation.** The state of node $p$ is a view, a list of at most $c$ node descriptors. A descriptor is a pair of an address and an age, the number of cycles since the descriptor was created by its node. getPeer returns the address of a descriptor of the view. Once per cycle, the active thread of $p$ runs:

1. select a peer $q$ from the view, by the *peer selection* policy: `rand` (a uniform descriptor) or `tail` (the descriptor with the highest age);
2. if the view propagation is `push` or `pushpull`: build a buffer with the fresh descriptor $(p, 0)$, then permute the view, move the $H$ oldest descriptors to its end, and add the first $c/2 - 1$ descriptors of the view to the buffer; send the buffer to $q$. If the propagation is `pull`, send an empty request;
3. if the propagation is `pull` or `pushpull`: receive the buffer of $q$ and apply *view selection* to it;
4. increase the age of every descriptor in the view.

The passive thread of $q$ receives a buffer, answers with a buffer of its own if the propagation includes pull, applies view selection, and increases the ages.

**View selection** with parameters $H$ (healing) and $S$ (swap) merges a received buffer into a view of target size $c$:

1. append the buffer to the view;
2. remove duplicate addresses, and keep the youngest descriptor of each;
3. remove the $\min(H, |view| - c)$ oldest descriptors;
4. remove the $\min(S, |view| - c)$ descriptors from the head of the view, which are the ones that were just sent to the peer;
5. remove random descriptors until $|view| = c$.

So $H$ sets how fast old descriptors, which may belong to crashed nodes, are dropped, and $S$ sets how many of the sent descriptors are given away instead of kept. The paper names three settings: *blind* ($H = 0$, $S = 0$), *healer* ($H = c/2$) and *swapper* ($H = 0$, $S = c/2$). Newscast is close to (rand, pushpull, healer), and Cyclon is close to (tail, pushpull, swapper).

## Laws

These laws describe the ideal service. Each implementation meets them only approximately, and its page says how far it is from each one.

1. **Uniformity.** Each call of getPeer returns a node chosen uniformly from the live nodes other than the caller.
2. **Independence.** Calls of getPeer are independent, at one node over time and across nodes.
3. **Membership.** A node that has joined and has not crashed is returned with positive probability by some node within bounded time. A crashed node stops being returned within bounded time.
4. **Connectivity.** The directed graph in which $p$ points to $q$ when $q$ is in the view of $p$ is connected, so the service never splits the network into parts that cannot see each other.
5. **Local cost.** Each node stores $O(c)$ descriptors and sends $O(1)$ messages of size $O(c)$ per cycle, independent of $n$.

Laws 1 and 2 cannot hold exactly with partial views (see Lower bounds). The service is judged by how close the overlay graph is to a random graph with the same out-degree $c$: its in-degree distribution, its clustering coefficient, its path lengths, and how fast it removes dead descriptors.

**The findings of the paper.** Jelasity et al. simulated the combinations of peer selection, view selection and propagation from several starting topologies, and with churn and large failures. Their main findings, as they state them:

- None of the variants gives a truly random overlay. The overlays have a higher [clustering coefficient](/clustering-coefficient/) than a random graph, and their in-degree distribution differs from a random graph, so the samples of nearby nodes and of one node over time are correlated.
- Push-only view propagation is weak: it can lead to partitioned or badly connected overlays in some starting scenarios. They recommend push-pull.
- A larger $H$ removes the descriptors of crashed nodes faster and makes the overlay heal quickly after failures. A larger $S$ makes the in-degree more even. The two goals conflict, and a small positive $H$ with a large $S$ is a good trade off.
- The overlays stay connected after the removal of a large fraction of the nodes, and their properties converge to the same state whatever the starting topology.

## Implementations

| implementation | view | exchange | dead descriptors | notes |
|---|---|---|---|---|
| [Newscast](/newscast/) | $c$ descriptors with timestamps | push-pull with a uniform peer, keep the $c$ freshest | removed fast, by age | uneven in-degree |
| [Cyclon](/cyclon/) | $c$ descriptors with ages | swap $\ell$ descriptors with the oldest neighbour | removed within about $c$ cycles | in-degree close to $c$ with small variance |
| framework, blind / healer / swapper | $c$ descriptors | as above with $(H, S)$ | depends on $H$ | covers both of the rows above |
| [SCAMP](/scamp/) | about $(c + 1) \ln n$ addresses, no ages | subscription forwarding, not periodic | by lease and resubscription | the view size adapts to $n$ |
| [lpbcast](/lpbcast/) | $l$ addresses | membership piggybacked on broadcast messages | by unsubscriptions | view size fixed |
| [HyParView](/hyparview/) | small active view and larger passive view | shuffles in the passive view | detected by TCP on the active view | built for broadcast reliability |

For the problem that these services solve, with the uniform ideal and the random walk methods, see [random peer sampling](/random-peer-sampling/).

## Lower bounds

- **Repeats.** Between two changes of the view, getPeer returns nodes from a set of at most $c$ nodes, so any $c + 1$ such calls contain a repeat. For independent uniform samples, $c + 1$ calls repeat only with probability about $(c + 1)^2 / (2n)$, by the [birthday paradox](/birthday-paradox/). So for $c$ much smaller than $n$ law 2 fails, and a node that needs many samples in one cycle sees the same peers again.
- **Overlap.** If $q$ is in the view of $p$ and they have just exchanged with push-pull, their views share descriptors. So the samples of neighbours are correlated, and the clustering coefficient of the overlay is higher than the $c / n$ of a random graph with out-degree $c$, unless the exchange gives descriptors away instead of copying them, as the swapper does.

## References
