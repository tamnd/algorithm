---
tag: W0AS60
kind: model
slug: take-grant-model
name: Take-Grant protection model
aliases:
- take-grant model
area: security-and-privacy/access-control-and-information-flow
level: advanced
summary: A graph model of protection in which subjects take and grant rights along edges, built so that the safety question is decidable in linear time.
model: word-ram
prereqs: [access-control-matrix, harrison-ruzzo-ullman-model]
see_also: [harrison-ruzzo-ullman-model, hru-safety-undecidability, access-control-matrix, capability-list, connected-components, reachability, confinement-problem, breadth-first-search]
sources:
  - paper: doi:10.1109/SFCS.1976.1
    title: "Anita K. Jones, Richard J. Lipton and Lawrence Snyder, A linear time algorithm for deciding security, 17th Annual Symposium on Foundations of Computer Science (FOCS), 1976, pages 33 to 41"
    locator: the take, grant, create and remove rules and the linear time decision procedure
  - paper: doi:10.1145/322017.322025
    title: "Richard J. Lipton and Lawrence Snyder, A linear time algorithm for deciding subject security, Journal of the ACM 24(3), 1977, pages 455 to 464"
    locator: the characterization of can-share and the linear time algorithm
  - book: isbn:9780321712332
    title: "Matt Bishop, Computer Security: Art and Science, second edition, Addison-Wesley, 2018"
    locator: "Chapter 3, Foundational Results (the Take-Grant protection model: sharing of rights, islands, bridges and spans, theft and conspiracy, interpretation of the model)"
---

The Take-Grant protection model is a model of protection in which the state is a directed graph and four fixed rules change it. Vertices are subjects and objects, and an edge from $x$ to $y$ carries the rights that $x$ has over $y$. Two special rights, *take* ($t$) and *grant* ($g$), move other rights along the edges. Jones, Lipton and Snyder gave the model in 1976 as an answer to the [HRU result](/hru-safety-undecidability/) that safety is undecidable for general protection systems. In Take-Grant the rules are fixed, and the question "can $x$ come to hold right $\alpha$ over $y$?" has an exact graph characterization and a linear time algorithm.

## The machine

**Protection graph.** A state is a finite directed graph $G = (V, E)$ with a label $\lambda(x, y) \subseteq R$ on each edge, where $R$ is a finite set of rights that contains $t$ and $g$. The vertices are split into subjects (active) and objects (passive). The graph is the [access control matrix](/access-control-matrix/) written as a graph: $\lambda(x, y) = A[x, y]$, and a missing edge is an empty cell.

**Rules.** Let $x$, $y$, $z$ be distinct vertices and let $x$ be a subject. Write $G \vdash G'$ if one rule takes $G$ to $G'$.

| rule | precondition | effect |
|---|---|---|
| $x$ takes ($\alpha$ to $z$) from $y$ | $t \in \lambda(x, y)$, $\alpha \subseteq \lambda(y, z)$ | add $\alpha$ to $\lambda(x, z)$ |
| $x$ grants ($\alpha$ to $z$) to $y$ | $g \in \lambda(x, y)$, $\alpha \subseteq \lambda(x, z)$ | add $\alpha$ to $\lambda(y, z)$ |
| $x$ creates ($\alpha$ to new vertex) $y$ | $y$ is a new subject or object | add $y$ and the edge $x \to y$ with label $\alpha$ |
| $x$ removes ($\alpha$ to) $y$ | $\lambda(x, y)$ exists | remove $\alpha$ from $\lambda(x, y)$ |

These four are the *de jure* rules: they change rights. Take says that a subject who may take from $y$ gets any right that $y$ holds. Grant says that a subject who may grant to $y$ can give $y$ any right it holds. In HRU terms each rule is a command with at most two tests and one or two primitive operations, so Take-Grant is one fixed protection system.

**The question.** For a right $\alpha$ and vertices $x$, $y$ of $G_0$, define

$$\mathit{can\_share}(\alpha, x, y, G_0) \iff \exists G:\ G_0 \vdash^* G \text{ and } \alpha \in \lambda_G(x, y).$$

**Cost.** In the word RAM model, store the graph as adjacency lists with $n$ vertices and $m$ labeled edges. One rule costs $O(1)$ expected time with a hash map of edges. The decision procedures below run in $O(n + m)$ time.

## What it counts

The model counts which rights can reach which vertices. The adversary in $\mathit{can\_share}$ is a set of subjects that all cooperate: every subject applies any rule that helps the transfer, and no one refuses. So $\mathit{can\_share}$ is false only if no coalition of all the subjects can move the right. A false answer is a proof of safety against any such coalition. A true answer only says that a transfer is possible if the subjects on the path agree.

**Paths and words.** A *tg-path* is a path in the graph, with edges taken in either direction, on which each edge has $t$ or $g$ in its label. Its *word* lists the edges in order: $\overrightarrow{t}$ for a $t$ edge in the direction of travel, $\overleftarrow{t}$ for one against it, and the same for $g$. Two vertices are *tg-connected* if a tg-path joins them.

**Islands, bridges and spans.**

- An *island* is a maximal tg-connected set of subjects, using only edges between subjects. Inside an island any right held by one subject can reach any other.
- A *bridge* is a tg-path between two subjects whose word is in $\overrightarrow{t}^*$, $\overleftarrow{t}^*$, $\overrightarrow{t}^*\,\overrightarrow{g}\,\overleftarrow{t}^*$ or $\overrightarrow{t}^*\,\overleftarrow{g}\,\overleftarrow{t}^*$. Rights cross a bridge from one island to the next.
- A subject $x'$ *initially spans* to $x$ if a tg-path from $x'$ to $x$ has a word in $\overrightarrow{t}^*\,\overrightarrow{g}$ or is empty: $x'$ can take a grant right over $x$ and then give $x$ what it holds.
- A subject $s'$ *terminally spans* to $s$ if a tg-path from $s'$ to $s$ has a word in $\overrightarrow{t}^*$ or is empty: $s'$ can take what $s$ holds.

**Example.** Take subjects $p$, $q$, $s$, $z$ and an object $f$, with the edges $p \xrightarrow{t} s$, $s \xrightarrow{r} f$ and $s \xrightarrow{g} q$. Then $p$ takes ($r$ to $f$) from $s$, and $s$ grants ($r$ to $f$) to $q$, so $\mathit{can\_share}(r, p, f, G_0)$ and $\mathit{can\_share}(r, q, f, G_0)$ are true. The subject $z$ has no edges, so no rule involves it, and $\mathit{can\_share}(r, z, f, G_0)$ is false.

## Relation to other models

- **HRU.** The [HRU model](/harrison-ruzzo-ullman-model/) lets the designer choose the commands, and that freedom is what makes safety [undecidable](/hru-safety-undecidability/). Take-Grant fixes the commands. It shows that a protection system can create vertices without bound and still have a decidable safety question.
- **Capabilities.** A $t$ edge works like a [capability](/capability-list/) to read another subject's capability list, and a $g$ edge like a capability to write into it. The model is a common way to reason about capability systems.
- **Graph search.** The characterizations reduce $\mathit{can\_share}$ to [connected components](/connected-components/) and to [reachability](/reachability/) in a graph whose edges are the bridges, both found by [breadth-first search](/breadth-first-search/).
- **Information flow.** The de jure rules move rights, not data. Rights are not the same as information, which is the subject of the [confinement problem](/confinement-problem/).

## Known results in the model

Each item is a theorem.

- **Subject-only graphs** (Jones, Lipton and Snyder 1976). If every vertex of $G_0$ is a subject, $\mathit{can\_share}(\alpha, x, y, G_0)$ holds if and only if $\alpha \in \lambda(x, y)$ already, or some vertex $s$ has $\alpha \in \lambda(s, y)$ and $x$ and $s$ are tg-connected.
- **General graphs** (Lipton and Snyder 1977). $\mathit{can\_share}(\alpha, x, y, G_0)$ holds if and only if $\alpha \in \lambda(x, y)$ already, or all four of these hold: some vertex $s$ has $\alpha \in \lambda(s, y)$; some subject $x'$ is equal to $x$ or initially spans to $x$; some subject $s'$ is equal to $s$ or terminally spans to $s$; and there are islands $I_1, \ldots, I_k$ with $x' \in I_1$, $s' \in I_k$ and a bridge from $I_j$ to $I_{j+1}$ for each $j$.
- **Linear time** (Lipton and Snyder 1977). The condition can be checked in $O(n + m)$ time: find the islands with one pass, find the bridges by a search whose state is a vertex and a position in the word patterns, and test reachability between islands. The proofs use the create rule, but the conditions mention only the vertices and edges of $G_0$, so the unbounded state space does not enter the test.
- **Removal does not help.** The remove rule only deletes rights and no rule tests that a right is absent, so a shortest sequence that shares a right never uses remove.
- **Theft and conspiracy** (Snyder 1981, as presented in Bishop, Chapter 3). The predicate $\mathit{can\_steal}(\alpha, x, y, G_0)$ asks whether $x$ can get $\alpha$ over $y$ when the subjects that already hold $\alpha$ over $y$ never grant it. This changes the adversary: the owners are honest and the others cooperate. It also has a graph characterization. Bishop also treats conspiracy: the smallest number of subjects that must act together for a transfer.
- **De facto rules** (Bishop, Chapter 3). The rules post, pass, spy and find model the flow of information along read and write edges, and the predicate $\mathit{can\_know}(x, y, G_0)$ asks whether information can flow from $y$ to $x$. It also has a path characterization.

## References
