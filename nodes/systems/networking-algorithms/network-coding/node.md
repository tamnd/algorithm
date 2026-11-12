---
tag: S62752
kind: technique
slug: network-coding
name: Network coding
aliases:
- linear network coding
- random linear network coding
- RLNC
area: systems/networking-algorithms
level: research
summary: "Intermediate nodes send linear combinations of the packets they receive. For multicast this reaches the min-cut bound, which routing alone cannot always reach."
prereqs: [max-flow-min-cut-theorem, multicast-routing, gaussian-elimination]
see_also: [steiner-tree-problem, menger-theorem, schwartz-zippel-lemma, fountain-codes, regenerating-codes, erasure-codes, integrality-gap, maximum-throughput-routing]
sources:
  - paper: doi:10.1109/18.850663
    title: "Rudolf Ahlswede, Ning Cai, Shuo-Yen Robert Li and Raymond W. Yeung, Network information flow, IEEE Transactions on Information Theory 46(4), 2000"
    locator: pages 1204 to 1216 (the butterfly network and the multicast capacity theorem)
  - paper: doi:10.1109/TIT.2002.807285
    title: "Shuo-Yen Robert Li, Raymond W. Yeung and Ning Cai, Linear network coding, IEEE Transactions on Information Theory 49(2), 2003"
    locator: pages 371 to 381 (linear codes reach the multicast capacity)
  - paper: doi:10.1109/TNET.2003.818197
    title: "Ralf Koetter and Muriel Médard, An algebraic approach to network coding, IEEE/ACM Transactions on Networking 11(5), 2003"
    locator: pages 782 to 795 (transfer matrices, decodability as a nonzero determinant)
  - paper: doi:10.1109/TIT.2005.847712
    title: "Sidharth Jaggi, Peter Sanders, Philip A. Chou, Michelle Effros, Sebastian Egner, Kamal Jain and Ludo M. G. M. Tolhuizen, Polynomial time algorithms for multicast network code construction, IEEE Transactions on Information Theory 51(6), 2005"
    locator: pages 1973 to 1982 (deterministic construction over a field with at least as many elements as sinks)
  - paper: doi:10.1109/TIT.2006.881746
    title: "Tracey Ho, Muriel Médard, Ralf Koetter, David R. Karger, Michelle Effros, Jun Shi and Ben Leong, A random linear network coding approach to multicast, IEEE Transactions on Information Theory 52(10), 2006"
    locator: pages 4413 to 4430 (the success probability bound (1 - d/q)^η)
  - paper: "Philip A. Chou, Yunnan Wu and Kamal Jain, Practical network coding, Proceedings of the 41st Allerton Conference on Communication, Control and Computing, 2003"
    locator: coding vectors in packet headers, generations, buffering
  - paper: doi:10.1145/1159913.1159942
    title: "Sachin Katti, Hariharan Rahul, Wenjun Hu, Dina Katabi, Muriel Médard and Jon Crowcroft, XORs in the air: practical wireless network coding, ACM SIGCOMM 2006"
    locator: the COPE design (opportunistic coding at wireless relays, learning what neighbors have overheard)
---

Network coding lets the routers of a network do more than store and forward: a node that has received several packets may send a combination of them, usually a linear combination over a finite field $\mathbb{F}_q$, and the receivers decode by solving a linear system. For multicast from one source to several sinks, the best rate with routing alone is a fractional packing of [Steiner trees](/steiner-tree-problem/), which can be strictly smaller than the [min-cut](/max-flow-min-cut-theorem/) to each sink. Coding reaches the min-cut to every sink at the same time, and random coefficients reach it with high probability, so the code can be built without knowing the network.

## In plain words

Two friends each want to hear two messages, A and B, from a single sender. Some of the paths are shared. With plain forwarding, a shared link can carry only A or only B, so one friend misses a message. If the shared link carries A and B mixed together, each friend can use the message it already has to take the mixture apart and get the other one. Network coding does this in general: routers send mixtures, every packet says how it was mixed, and each receiver untangles enough mixtures to recover all the messages.

## When it applies

- **Multicast.** One source sends the same data to several sinks. This is where coding is guaranteed to help: the rate equals the smallest min-cut from the source to a sink, and linear codes reach it. For a single sink coding gains nothing, since [edge-disjoint paths](/edge-disjoint-paths/) already reach the min-cut.
- **Shared bottlenecks.** Coding helps when flows to different sinks compete for the same links, as in the butterfly below. On a tree there is nothing to gain.
- **Broadcast media and relays.** In wireless networks, one transmission reaches several neighbors, so a relay that sends the XOR of two packets serves two receivers that each already have one of them.
- **Lossy links and unknown topology.** Random coefficients need no knowledge of the network, and any $h$ independent combinations decode, so it does not matter which packets are lost. This is the same property that [fountain codes](/fountain-codes/) give on a single path.
- **Not for multiple unicast in general.** When different sinks want different data, linear codes are not always enough, and the capacity is not known in general.

## The template

**Setting.** The network is a directed acyclic graph; each edge carries one symbol of $\mathbb{F}_q^L$ per use, for a prime $q$ (or a power of a prime). The source $s$ has $h$ messages $x_1, \ldots, x_h \in \mathbb{F}_q^L$, and $h$ is at most the min-cut from $s$ to each sink. Every edge $e$ carries a *global coding vector* $g(e) \in \mathbb{F}_q^h$ and the payload $y(e) = \sum_k g(e)_k x_k$. The coding vector travels in the packet header, so the sinks need not know the network or the coefficients.

```pseudo id=main
LINEAR-NETWORK-CODE(G, s, T, x_1, ..., x_h)     ▷ hole: COEF(e', e), the local coefficient from edge e' to edge e
L1  give h virtual edges into s the unit vectors u_1, ..., u_h as coding vectors and x_1, ..., x_h as payloads
L2  for each edge e = (v, w) of G, in a topological order of the tails, do
L3      for each edge e' into v: β(e', e) ← COEF(e', e)    ▷ hole: uniform in F_q, or chosen by a deterministic construction
L4      g(e) ← Σ_{e' into v} β(e', e) g(e')               ▷ the global coding vector, in the header
L5      y(e) ← Σ_{e' into v} β(e', e) y(e')               ▷ the payload, the same combination
L6  for each sink t in T do
L7      A ← the rows g(e), Y ← the rows y(e), for the edges e into t
L8      if rank A = h then solve A x = Y by Gaussian elimination over F_q, which gives x_1, ..., x_h
L9      else t cannot decode
```

**The hole.** In *random linear network coding* each node draws its coefficients uniformly from $\mathbb{F}_q$, independently. In a *deterministic* code, they are computed centrally, for example by the algorithm of Jaggi et al.

**Why it works.** Every coding vector is a linear function of the coefficients, so each entry of the matrix $A_t$ at sink $t$ is a polynomial in the coefficients, of degree at most the length of the longest path. Sink $t$ decodes exactly when $\det A_t \neq 0$ for an $h \times h$ submatrix. If the min-cut to $t$ is at least $h$, there are $h$ edge-disjoint paths from $s$ to $t$ ([Menger's theorem](/menger-theorem/)), and the coefficients that route $x_k$ along the $k$-th path and send zero elsewhere make $A_t$ a permutation matrix, so $\det A_t$ is a nonzero polynomial. The product $\prod_t \det A_t$ is then a nonzero polynomial too. Over a field with more elements than the degree of each variable in it, some choice of coefficients makes it nonzero, which is a deterministic linear code for all sinks at once. A random choice makes it nonzero with high probability by the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/); the sharper analysis of Ho et al. gives success probability at least $(1 - d/q)^\eta$, where $d$ is the number of sinks and $\eta$ the number of edges with random coefficients.

**Cost.** A coded packet costs $O(hL)$ field operations at a node with $h$ inputs, plus a header of $h$ field elements. A sink decodes $h$ packets of length $L$ with $O(h^3 + h^2 L)$ operations. In practice the data is cut into *generations* of $h$ packets, and only packets of the same generation are combined.

## Classic examples

- **The butterfly network.** The source $s$ sends $x_1$ to $a$ and $x_2$ to $b$. Node $a$ sends $x_1$ to sink $t_1$ and to $c$; node $b$ sends $x_2$ to sink $t_2$ and to $c$. The edge from $c$ to $d$ is the bottleneck, and $d$ forwards to both sinks. Each sink has min-cut 2. If $c$ sends $x_1 \oplus x_2$, then $t_1$ computes $x_2 = x_1 \oplus (x_1 \oplus x_2)$, $t_2$ computes $x_1$, and both receive 2 messages per use. A brute force over all forwarding choices shows that routing gives some sink at most 1 message per use, and the best fractional packing of Steiner trees gives 3/2 per use: three trees of weight 1/2 reach it, and edge weights of 1/2 on the two source edges and the bottleneck prove that no packing does better, by [LP duality](/lp-duality/).
- **Two-way relay (COPE).** Alice and Bob exchange packets through a relay $r$. With routing, $r$ needs two transmissions; it can instead broadcast $p_A \oplus p_B$ once, and each end removes its own packet. Katti et al. built this into the COPE protocol for wireless mesh networks, where relays code opportunistically from what they know their neighbors have overheard.
- **Random coding on random networks.** In the test code, 25 random acyclic networks on 8 nodes (each forward edge present with probability 1/2, seeds 0 to 24) were drawn, with node 0 as source and the last two nodes as sinks; 21 of them had a positive min-cut $h$ to both sinks, between 1 and 4, and from 10 to 19 edges. Random linear coding over $\mathbb{F}_{101}$ with 150 trials per network let both sinks decode in 97.8 percent of the trials, and always recovered the right data. The bound $(1 - 2/101)^\eta$ averages 75.4 percent on these networks.
- **Field size matters.** On the butterfly with random coefficients, both sinks decode with probability exactly $6/4096$ over $\mathbb{F}_2$ (every one of the 12 coefficients must be right), and in 20000 trials each, with about 2.2 percent over $\mathbb{F}_3$, 42 percent over $\mathbb{F}_{11}$ and 92 percent over $\mathbb{F}_{101}$.
- **Distributed storage.** [Regenerating codes](/regenerating-codes/) view the repair of a lost storage node as a multicast problem and use network coding to cut the repair traffic.
- **Content distribution.** Peer-to-peer systems such as Avalanche let peers send random combinations of the blocks they hold, so that a downloader never waits for one rare block.

## Variations

- **Deterministic construction.** Jaggi et al. give a polynomial-time algorithm that picks coefficients edge by edge along $h$ edge-disjoint paths to each sink, keeping the coding vectors on each sink's current cut independent. A field with at least as many elements as sinks suffices.
- **Random linear network coding.** Ho et al.: coefficients chosen at random, coding vectors in headers, the bound $(1 - d/q)^\eta$. With $q = 2^8$ or $2^{16}$ the failure rate is small in practice, and a failing sink only needs a few more packets.
- **Algebraic framework.** Koetter and Médard describe a code by transfer matrices and reduce decodability to a polynomial being nonzero; this also covers delays and cycles, with coefficients in rational functions of a delay variable.
- **Coding against errors and eavesdroppers.** Network error correcting codes extend classical bounds to networks, and secure network coding hides the messages from an eavesdropper on a limited number of edges. Subspace codes (Koetter and Kschischang) treat the received data as a vector space, which fits random coding.
- **Coding gain.** The ratio of coded to routed multicast rate is 4/3 on the butterfly. In undirected networks it is at most 2 (Li and Li), and it equals the [integrality gap](/integrality-gap/) of a cut relaxation for the Steiner tree problem (Agarwal and Charikar). In directed networks it can grow with the size of the network.
- **Beyond multicast.** For several unicast sessions, Dougherty, Freiling and Zeger gave networks where linear codes over any field cannot reach the rate that nonlinear codes reach.

## Pitfalls

- **Coefficients over too small a field.** Over $\mathbb{F}_2$, random coding fails often, as the butterfly numbers show. Use a field of $2^8$ elements or more, or deterministic coefficients.
- **Rate above the min-cut.** No code decodes $h$ messages at a sink whose min-cut is below $h$: the rank of its matrix is at most the min-cut.
- **Mixing packets of different generations.** Combining packets from different generations makes the system larger than the header can describe. Keep a generation number in each packet.
- **Header overhead.** The coding vector costs $h$ field elements per packet. With $h = 32$ and $\mathbb{F}_{2^8}$ that is 32 bytes, which matters for small packets.
- **Decoding delay.** A sink usually needs all $h$ packets of a generation before it can decode any of them. Real-time traffic needs small generations or systematic codes that send the original packets first.
- **Pollution.** One malicious node that sends a bad combination corrupts every packet that mixes it in. Defenses include homomorphic signatures and hashes that survive linear combination.
- **Cycles.** In a network with cycles, a combination can arrive back at its sender. Generations and a delay variable, or coding only on an acyclic subnetwork, avoid this.

## Exercises

1. In the butterfly, list the forwarding choices on the 9 edges and show that no choice gives both sinks 2 distinct messages. Then find a fractional packing of Steiner trees of value 3/2.
2. Show that if the min-cut from $s$ to a sink $t$ is $k$, every sink matrix $A_t$ has rank at most $k$, so no linear code multicasts more than $\min_t$ min-cut messages.
3. Prove that a uniformly random $h \times h$ matrix over $\mathbb{F}_q$ is invertible with probability $\prod_{i=1}^{h} (1 - q^{-i})$, and evaluate it for $q = 2$ and large $h$. *Answer:* about 0.289.
4. Over $\mathbb{F}_2$, find the probability that random coefficients let both sinks of the butterfly decode. *Answer:* $6/4096$; the source edges must carry two independent vectors (6 of the 16 choices), and the 8 other coefficients must all be 1.
5. For the two-way relay, count the transmissions with and without coding, and find the throughput gain.

## References
