---
tag: YJ25C7
kind: theorem
slug: channel-routing-np-completeness
name: NP-completeness of channel routing
aliases:
- Szymanski theorem
area: eda/routing
level: advanced
summary: Deciding whether a channel routes in k tracks is NP-complete without doglegs (LaPaugh 1980) and with doglegs (Szymanski 1985), though left-edge is optimal without vertical constraints.
prereqs: [channel-routing-problem, np-complete]
see_also: [vertical-constraint-graph, channel-density, left-edge-algorithm, dogleg-channel-routing, greedy-channel-router, yoshimura-kuh-algorithm, polynomial-time-reduction, switchbox-routing]
sources:
  - paper: "A. S. LaPaugh, Algorithms for Integrated Circuit Layout, An Analytic Approach, PhD thesis, MIT, report MIT/LCS/TR-248, 1980"
    locator: the NP-completeness of channel routing in a given number of tracks when each net has one trunk (general locator)
  - paper: doi:10.1109/TCAD.1985.1270096
    title: Thomas G. Szymanski, Dogleg channel routing is NP-complete, IEEE Transactions on Computer-Aided Design 4(1), 31 to 41, 1985
    locator: the NP-completeness of channel routing in a given number of tracks in the two-layer Manhattan model where wires may dogleg in any column (general locator)
  - paper: "M. Middendorf, Manhattan channel routing is NP-complete under truly restricted settings, Chicago Journal of Theoretical Computer Science, article 6, 1996"
    locator: hardness for channels with strong limits on the nets (general locator; the title is not checked against the journal)
  - paper: "M. Sarrafzadeh, Channel-routing problem in the knock-knee mode is NP-complete, IEEE Transactions on Computer-Aided Design 6(4), 1987"
    locator: hardness of channel routing in the knock-knee model for nets with more than two pins (general locator)
  - book: isbn:9780792383932
    title: Naveed A. Sherwani, Algorithms for VLSI Physical Design Automation, third edition, Kluwer, 1999
    locator: the chapter on detailed routing, the part on channel routing (the complexity of channel routing; general locator)
---

Channel routing asks for the fewest tracks in which the nets of a [channel](/channel-routing-problem/) can be routed. Two results show that this is hard in the usual two-layer model. A. S. LaPaugh proved in her 1980 MIT thesis that the decision version is NP-complete when each net must use one trunk on one track, the model without doglegs. T. G. Szymanski proved in 1985 that it stays NP-complete when wires may change track in any column. So, unless P = NP, no router finds the fewest tracks on every channel in polynomial time, which is why practical channel routers are heuristics. The hardness comes from the vertical constraints: when the [vertical constraint graph](/vertical-constraint-graph/) has no edges, the [left-edge algorithm](/left-edge-algorithm/) uses $d$ tracks, the [channel density](/channel-density/), and that is optimal.

## Statement

A channel has columns $1, \ldots, n$, a top pin and a bottom pin in each column, each a net label or 0, and the routing grid of the reserved two-layer model with $k$ tracks: trunks on layer H, branches on layer V, vias at grid points, and no point of a layer shared by two nets.

**Channel routing without doglegs (CR-ND).** Given a channel and an integer $k$, is there a map $t$ from nets to $\{1, \ldots, k\}$ such that nets with intersecting intervals get different tracks, and $t(a) < t(b)$ for every edge $a \to b$ of the vertical constraint graph?

**Channel routing with doglegs (CR-D).** Given a channel and an integer $k$, is there a routing of all nets on the grid with $k$ tracks and no columns outside the channel, where each net may use layer H and layer V in any column?

**Theorem.**

1. CR-ND is NP-complete (LaPaugh 1980).
2. CR-D is NP-complete (Szymanski 1985).
3. If the vertical constraint graph has no edges, CR-ND is solvable in polynomial time, and the answer is yes exactly when $k \ge d$.

The page on the [channel routing problem](/channel-routing-problem/) shows that CR-ND has the stated form: a routing with one trunk per net exists with $k$ tracks if and only if such a map exists.

## In plain words

It is easy to check a proposed routing: look at every column and every track. It is hard to find the narrowest one. For a large channel, no known method does much better than trying very many arrangements, in the worst case.

The trouble comes from the rules that one net must be above another. Without those rules, the simple method of filling lanes from the left is always best. Allowing nets to change lanes does not remove the trouble.

## Proof

**Membership of CR-ND in NP.** A certificate is the map $t$. It has $N$ entries, one per net, each at most $k$, and $k$ can be taken at most $N$ without loss, because with an acyclic constraint graph $N$ tracks always suffice. To check it, compute the intervals of the nets and the edges of the constraint graph in one pass over the columns, then check the at most $n$ edges, and check that the nets on each track are pairwise disjoint by sorting them by left end. This takes polynomial time.

**Membership of CR-D in NP, for $k$ written in unary.** A certificate is the set of grid edges, vias and points used by each net. The grid has $n(k + 2)$ points per layer, so the certificate has polynomial size, and connectivity and disjointness are checked by a search on each net. Szymanski's paper states the result for the decision problem with $k$ as given; this page only gives the certificate for the case where $k$ is written in unary.

**NP-hardness of CR-ND (sketch).** LaPaugh gives a polynomial-time reduction from a known NP-complete problem to CR-ND. By part 3, such a construction must use vertical constraints: the order they force between nets, together with the rule that nets which meet need different tracks, is what makes the choices hard. The full construction is in the thesis.

**NP-hardness of CR-D (sketch).** Szymanski gives a polynomial-time reduction from a known NP-complete problem to CR-D. The difficulty, compared with CR-ND, is that a router may change the track of a net in any free column, so the construction must work for every placement of doglegs and not only for maps from nets to tracks. The full construction and its proof are in the paper.

**Part 3.** If the constraint graph has no edges, every routing needs at least $d$ tracks by the density bound, and the left-edge algorithm gives one with $d$ tracks. So the answer is yes if and only if $k \ge d$, and $d$ is computed by one sweep over the columns. $\square$

The proofs of parts 1 and 2 on this page are sketches. The page gives no gadget in detail, since the constructions are long and rest on the cited works.

**A small instance to check.** Take the channel

| column | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| top | 5 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |
| bottom | 2 | 2 | 4 | 5 | 3 | 3 | 1 | 4 |

and $k = 3$. The map $t(1) = 1$, $t(3) = t(5) = 2$, $t(2) = t(4) = 3$ is a certificate: the intervals $[4, 7]$ on track 1, $[5, 6]$ and $[1, 4]$ on track 2, and $[1, 2]$ and $[3, 8]$ on track 3 are disjoint on each track, and the edges $1 \to 5$ and $5 \to 2$ go down. For $k = 2$ the answer is no, because column 5 is crossed by nets 1, 3 and 4, so $d = 3$. The left-edge algorithm uses 4 tracks on this channel, so a fast heuristic can miss a yes answer.

## Consequences

- **Heuristics are the practical choice.** The [left-edge algorithm](/left-edge-algorithm/), [dogleg channel routing](/dogleg-channel-routing/), the [Yoshimura-Kuh algorithm](/yoshimura-kuh-algorithm/) and the [greedy channel router](/greedy-channel-router/) all run in polynomial time, so none of them can find the fewest tracks on every channel unless P = NP.
- **Switchboxes.** A channel with $k$ tracks is a [switchbox](/switchbox-routing/) with no pins on the left and right sides, so deciding whether a switchbox can be routed is NP-hard as well.
- **Exact methods are exponential.** Exact routers use branch and bound or integer programming, and their worst-case time grows exponentially.
- **The lower bounds are not tight.** Since $d$ and the longest path of the constraint graph are computed in polynomial time, neither can always equal the optimum unless P = NP.

## Tightness

- **Without vertical constraints the problem is easy.** Part 3 shows that the hardness of CR-ND needs vertical constraints. Channels with all pins on one side, or with one pin per column, have no constraints, and left-edge solves them.
- **Feasibility alone is easy without doglegs.** Whether some $k$ works at all is the question whether the constraint graph is acyclic, which a [cycle detection](/cycle-detection/) answers in linear time. The hard part is the number of tracks.
- **One layer is easy.** With one layer and no crossings, the problem is [river routing](/river-routing/), and the least width is found in polynomial time.
- **Other models.** In the knock-knee model, where two nets may bend at the same grid point, channels with two-pin nets can be routed in $d$ tracks, but Sarrafzadeh showed in 1987 that the problem is NP-complete when nets have more pins. Middendorf showed in 1996 that the Manhattan problem stays NP-complete under strong limits on the instances.

## History

Hashimoto and Stevens gave the left-edge algorithm in 1971, and it was soon clear that vertical constraints make the problem harder. A. S. LaPaugh, in her 1980 PhD thesis at MIT, proved that routing without doglegs in a given number of tracks is NP-complete. Deutsch had shown in 1976 that doglegs often save tracks, and it remained open whether they also make the problem easy. T. G. Szymanski settled this in 1985 in the IEEE Transactions on Computer-Aided Design, with a proof that the problem stays NP-complete when wires may dogleg in any column. Later work extended the hardness to other routing models and to restricted instances.

## References
