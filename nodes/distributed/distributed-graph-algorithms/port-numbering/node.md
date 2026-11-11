---
tag: 26FYBZ
kind: definition
slug: port-numbering
name: Port numbering
aliases:
- port numbers
- local port labels
- port-numbering model
- PN model
area: distributed/distributed-graph-algorithms
level: intro
summary: Each node numbers its incident edges 1 to deg(v), so it can tell its neighbours apart without names. In the port-numbering model nodes have no identifiers, and symmetry can make problems unsolvable.
prereqs: [synchronous-model]
see_also: [local-model, anonymous-network, anonymous-leader-election, anonymous-ring-impossibility, congest-model, broadcast-problem, distributed-maximal-matching, distributed-minimum-vertex-cover]
sources:
  - paper: doi:10.1145/800141.804655
    title: Dana Angluin, Local and global properties in networks of processors, STOC 1980, 82-93
    locator: networks of identical processors that address neighbours by port, coverings of networks, and the impossibility results that follow from them
  - paper: doi:10.1007/s00446-013-0202-3
    title: Lauri Hella, Matti Järvisalo, Antti Kuusisto, Juhana Laurinharju, Tuomo Lempiäinen, Kerkko Luosto, Jukka Suomela and Jonni Virtema, Weak models of distributed computing, with connections to modal logic, Distributed Computing 28(1), 31-53, 2015
    locator: the seven weak models SB, MB, VB, SV, MV, VV and VVc, the hierarchy SB below MB = VB below SV = MV = VV below VVc, and the logical characterizations
  - url: https://jukkasuomela.fi/da2020/da2020.pdf
    title: Juho Hirvonen and Jukka Suomela, Distributed Algorithms 2020, online textbook
    locator: Chapter 3 (the port-numbering model) and Chapter 7 (covering maps and what they make impossible)
  - paper: "Jukka Suomela, Survey of local algorithms, ACM Computing Surveys 45(2), article 24, 2013"
    locator: Section 3 (models with port numbers, with unique identifiers and with orientations) and the problems solvable in each
---

A *port numbering* labels the edges at each node of a network with the numbers $1, 2, \dots, \deg(v)$, so that a node can say "send this on port 2" or "this message came in on port 3" without knowing who its neighbours are. Each node numbers its own edges, and the two ends of one edge can have different numbers. The *port-numbering model* (PN) is the synchronous model in which nodes have port numbers but no identifiers: all nodes run the same deterministic program, start in the same state if they have the same degree and input, and can tell neighbours apart only by port. Angluin (1980) studied such anonymous networks and showed that symmetry makes many tasks impossible. The [LOCAL](/local-model/) and [CONGEST](/congest-model/) models start from port numbering too, and add unique identifiers, which are a strict addition: they make symmetry breaking possible.

## Definition

**Port numbering.** Let $G = (V, E)$ be a simple undirected graph. A port numbering of $G$ is a family of bijections $p_v : \{\text{edges at } v\} \to \{1, \dots, \deg(v)\}$, one for each node $v$. If $e = \{u, v\}$ has $p_u(e) = i$ and $p_v(e) = j$, write $(u, i) \leftrightarrow (v, j)$: port $i$ of $u$ is joined to port $j$ of $v$. The map $(u, i) \mapsto (v, j)$ is an involution on the set of all ports with no fixed points.

**The port-numbering model.** A distributed algorithm in the PN model is one deterministic state machine, the same for all nodes. A node starts with its degree and its local input only. In each synchronous round it sends one message on each port, receives one message on each port, knowing on which port each one arrived, and changes state. Messages can have any size, and there are no failures. The output of the algorithm may depend on the port numbering, and an algorithm *solves* a problem if its outputs are correct for every graph in the class and every port numbering.

**Notation.** $n$ nodes, $m$ edges, largest degree $\Delta$, diameter $D$.

**Coverings.** A *covering map* from a port-numbered graph $H$ to a port-numbered graph $G$ is a surjection $\varphi : V(H) \to V(G)$ that keeps degrees and inputs and maps port $i$ of $u$, joined to port $j$ of $w$, to port $i$ of $\varphi(u)$, joined to port $j$ of $\varphi(w)$.

**Lemma (proved here).** If $\varphi$ is a covering map from $H$ to $G$, then in every PN algorithm, every node $u$ of $H$ is in the same state as $\varphi(u)$ in $G$ after every round.

*Proof.* By induction on the round $t$. At $t = 0$, $u$ and $\varphi(u)$ have the same degree and input, so the same state. Suppose this holds after round $t - 1$. Port $i$ of $u$ is joined to port $j$ of some $w$, and port $i$ of $\varphi(u)$ is joined to port $j$ of $\varphi(w)$. The message from $w$ on port $j$ depends only on the state of $w$ and on $j$, and $w$ and $\varphi(w)$ are in the same state, so $u$ and $\varphi(u)$ receive the same message on every port, and they move to the same state. ∎

So if two nodes of one graph have the same image under a covering map, or two graphs cover the same graph, a PN algorithm cannot make their outputs differ.

## Examples and non-examples

**A symmetric cycle.** On a cycle $v_0, v_1, \dots, v_{n-1}$, let every node use port 1 for the edge to $v_{i+1}$ and port 2 for the edge to $v_{i-1}$ (indices modulo $n$). The rotation $v_i \mapsto v_{i+1}$ keeps all ports, so it is a covering map from the cycle to itself, and by the lemma $v_i$ and $v_{i+1}$ are in the same state after every round. Hence all nodes are. So no PN algorithm can 3-colour a cycle, find a maximal independent set or a maximal matching on it, or elect a leader: every correct output for these needs two nodes with different outputs. With unique identifiers, the [Cole-Vishkin](/cole-vishkin/) algorithm 3-colours it in $O(\log^* n)$ rounds.

**A single edge.** Two nodes joined by one edge both have degree 1 and port 1. They are in the same state for ever, so no PN algorithm can 2-colour $K_2$ or pick one endpoint. The same holds for any graph with a port-preserving automorphism that moves a node to a neighbour.

**What PN can do.** Problems whose outputs may be equal on symmetric nodes:

- counting the nodes of each degree within distance $r$, and any function of the *view* of radius $r$, the tree of port-numbered walks from a node;
- a maximal matching on bipartite graphs when the nodes know their side;
- a 3-approximation of the minimum vertex cover, by a matching in a bipartite double cover (Polishchuk and Suomela 2009; see [distributed vertex cover](/distributed-minimum-vertex-cover/)).

**Non-example: identifiers.** If each node also gets a unique identifier, the model is [LOCAL](/local-model/) (or CONGEST with small messages), not PN. The two ends of an edge then differ, and the lemma no longer applies, since a covering map that merges two nodes would merge two identifiers.

**Non-example: oriented graphs.** If each edge also has an orientation known to both ends, the model is PO. Orientation alone does not break the symmetry of the cycle above, which can be oriented clockwise.

## Related definitions

- **[Anonymous network](/anonymous-network/).** A network whose nodes have no identifiers; PN is the synchronous anonymous network with port numbers. [Anonymous leader election](/anonymous-leader-election/) and the [anonymous ring impossibility](/anonymous-ring-impossibility/) are the classic consequences of the covering lemma.
- **KT0 and KT1.** In LOCAL and CONGEST, KT0 means that nodes know their ports but not the identifiers behind them, and KT1 that they know the identifiers of their neighbours. KT0 is port numbering plus identifiers. See [broadcast](/broadcast-problem/).
- **Weak models (Hella et al. 2015, cited).** The PN model, written VVc, has two features: a node can send a different message on each port (vector output, V), and it can see on which port each message arrived (vector input, V). Weaker models drop them: a node may only broadcast one message to all ports (B), or may receive only the multiset (M) or set (S) of messages. The classes of solvable problems form the strict hierarchy $\mathsf{SB} \subsetneq \mathsf{MB} = \mathsf{VB} \subsetneq \mathsf{SV} = \mathsf{MV} = \mathsf{VV} \subsetneq \mathsf{VVc}$, where VV drops the consistency between the outgoing and incoming port numbers, and each class has a description in a modal logic.
- **Views and the universal cover.** The *view* of radius $r$ of a node is the tree of all port-numbered walks of length at most $r$ from it. A PN algorithm of $r$ rounds is a function of the view, and two nodes with the same infinite view, the same node of the universal cover, give the same output for ever.
- **Port numbering in [LOCAL](/local-model/).** The ball of a node in LOCAL contains the port numbers at both ends of each edge, so the lemma for PN and the locality theorem for LOCAL have the same proof.

## References
