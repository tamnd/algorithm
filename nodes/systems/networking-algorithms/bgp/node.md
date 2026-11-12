---
tag: BXJ1W1
kind: algorithm
slug: bgp
name: Border Gateway Protocol (BGP)
aliases:
- BGP
- border gateway protocol
- BGP-4
- BGP decision process
area: systems/networking-algorithms
level: advanced
summary: "The path-vector protocol between the autonomous systems of the Internet. Each router picks one route per prefix by a fixed list of tie-breaks, from local preference down to peer address."
solves: [routing-problem]
model: asynchronous-model
complexity:
  vars: {k: the number of candidate routes to one prefix, n: the number of autonomous systems, m: the number of links between them}
  time: {worst: O(k)}
  space: {extra: O(k)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 1989
  people: [Kirk Lougheed, Yakov Rekhter]
  note: The first BGP was RFC 1105 (1989). BGP-4, in use since the mid 1990s, is now RFC 4271 (Rekhter, Li and Hares, 2006).
prereqs: [path-vector-routing, routing-problem]
see_also: [hot-potato-routing, link-state-routing, distance-vector-routing, longest-prefix-match, ecmp-hashing, nash-equilibrium, split-horizon-poison-reverse, multicast-routing]
sources:
  - url: https://www.rfc-editor.org/rfc/rfc4271
    title: Y. Rekhter, T. Li and S. Hares (editors), A Border Gateway Protocol 4 (BGP-4), RFC 4271, January 2006
    locator: Section 4 (message formats), Section 5.1 (path attributes, with MULTI_EXIT_DISC in 5.1.4 and LOCAL_PREF in 5.1.5), Section 9.1 (the decision process, with 9.1.1 the degree of preference and 9.1.2.2 the tie-breaking rules), Section 10 (timers)
  - paper: "Lixin Gao and Jennifer Rexford, Stable Internet routing without global coordination, IEEE/ACM Transactions on Networking 9(6), 2001, pages 681 to 692"
    locator: the preference and export rules for customers, peers and providers, and the proof that they guarantee convergence
  - paper: "Timothy G. Griffin, F. Bruce Shepherd and Gordon Wilfong, The stable paths problem and interdomain routing, IEEE/ACM Transactions on Networking 10(2), 2002, pages 232 to 243"
    locator: BGP policies as the stable paths problem, and the gadgets that do not converge
  - paper: "Lixin Gao, On inferring autonomous system relationships in the Internet, IEEE/ACM Transactions on Networking 9(6), 2001"
    locator: customer, peer and provider relationships, and valley-free AS paths (page numbers not checked)
  - url: https://www.rfc-editor.org/rfc/rfc3345
    title: D. McPherson, V. Gill, D. Walton and A. Retana, Border Gateway Protocol (BGP) Persistent Route Oscillation Condition, RFC 3345, August 2002
    locator: the oscillation caused by MED comparison together with route reflection
  - book: isbn:9780136681557
    title: James F. Kurose and Keith W. Ross, Computer Networking, A Top-Down Approach, eighth edition, Pearson, 2021
    locator: Chapter 5, Section 5.4 (routing among the ISPs, BGP, hot-potato routing, the route-selection algorithm, routing policy)
---

The Border Gateway Protocol (BGP) is the routing protocol between the autonomous systems (ASes) of the Internet, the separately run networks of ISPs, companies and universities. It is [path-vector routing](/path-vector-routing/): for each address prefix, a BGP router advertises the list of ASes that its route crosses (the AS_PATH), and it refuses any route that already contains its own AS. Each router chooses one route per prefix with the **decision process** of RFC 4271. The process first applies the operator's policy, as a local preference, and then a fixed list of tie-breaks: shortest AS path, origin type, MED, eBGP over iBGP, nearest exit, router identifier and peer address. Policy is what makes BGP useful between competing businesses. It is also what can keep it from converging; the customer, peer and provider rules of Gao and Rexford are the standard way to make it converge.

## In plain words

The Internet is made of tens of thousands of networks, each run by a different company or school. They do not share maps, and they do not trust each other. Each network tells its neighbours which addresses it can reach, and by which chain of networks.

A router that hears several ways to the same addresses must choose one. First it asks what its owner prefers: a way through a paying customer is better than a way through a network that it must pay. If that does not decide, it takes the shortest chain of networks. If that still does not decide, it goes through a list of smaller rules, down to "the neighbour with the lowest number". So every router picks exactly one way, and picks it the same way every time.

## The problem

Each AS owns some address prefixes and wants every other AS to be able to reach them. Links join ASes in business relationships: a customer pays its provider for transit, and two peers exchange their customers' traffic for free. Each AS wants routes that suit its own business, and it does not want to reveal its internal topology or policy. The goal is, for each prefix, a route at every AS that is loop-free, consistent with the next AS's route, and allowed by everyone's policy, and the protocol must settle on such routes after each change.

## The algorithm

**Sessions and messages.** Two BGP routers form a session over TCP and exchange OPEN, UPDATE, NOTIFICATION and KEEPALIVE messages (RFC 4271, Section 4). An UPDATE announces routes, each a prefix with path attributes, or withdraws them. A session between routers in different ASes is eBGP; one between routers of the same AS is iBGP. Each router keeps the routes it has received in its Adj-RIB-In, its chosen routes in its Loc-RIB, and the routes it sends in its Adj-RIB-Out.

**The attributes used by the decision.** AS_PATH is the list of ASes. LOCAL_PREF is the degree of preference that the AS gives the route, set by import policy and carried only inside the AS (Section 5.1.5). ORIGIN says how the route entered BGP: IGP, EGP or INCOMPLETE. MULTI_EXIT_DISC (MED) is a hint from a neighbouring AS about which of several links into it to use (Section 5.1.4). NEXT_HOP is the address to forward to.

**The decision process.** For each prefix, the router applies these steps to the routes in its Adj-RIB-In (Section 9.1.2).

```pseudo id=main
BGP-DECISION(R, me)                   ▷ R: the candidate routes to one prefix
L1  R ← the routes in R whose NEXT_HOP is reachable and whose AS_PATH does not contain me
L2  if R is empty then return none
L3  keep the routes with the highest degree of preference (LOCAL_PREF)
L4  keep the routes with the shortest AS_PATH
L5  keep the routes with the lowest ORIGIN (IGP < EGP < INCOMPLETE)
L6  in each group of routes from one neighbouring AS, keep the routes with the lowest MED
L7  if some route was learned by eBGP then keep only the eBGP routes
L8  keep the routes with the lowest interior cost to their NEXT_HOP
L9  keep the routes from the router with the lowest BGP Identifier
L10 return the route from the lowest peer address

BGP-SPEAKER(a)                        ▷ AS-level model with the Gao-Rexford policy
L11 on UPDATE from neighbour b: store the route with LOCAL_PREF by relation (customer > peer > provider);  best ← BGP-DECISION
L12 if best changed: send it to every neighbour if it is a customer route or a's own; otherwise send it to customers only
```

Lines L4 to L10 are the tie-breaking rules (a) to (g) of Section 9.1.2.2. MED is compared only between routes from the same neighbouring AS, because each AS sets its MED values in its own way. Line L8 is [hot-potato routing](/hot-potato-routing/): among equally good routes, take the exit that is nearest inside the AS. Lines L11 and L12 are the policy most ASes follow, which is analysed below.

**Policy.** Operators set LOCAL_PREF and filter what they send. Gao and Rexford described the common practice: an AS prefers routes from customers (they pay), then from peers (free), then from providers (it pays), and it carries traffic for others only when someone pays for it. So it sends routes learned from peers and providers to its customers only. A path that results is **valley-free**: it goes up through providers, crosses at most one peer link, and goes down through customers.

## Example

Router R in AS 1 has six routes to the prefix 203.0.113.0/24. The tie-break columns are used only when the earlier ones are equal.

| route | AS_PATH | LOCAL_PREF | ORIGIN | MED | session | interior cost | BGP id |
|---|---|---|---|---|---|---|---|
| r1 | 7 9 | 100 | IGP | | eBGP | 0 | 7 |
| r2 | 4 8 9 | 200 | IGP | | eBGP | 0 | 4 |
| r3 | 2 9 | 200 | IGP | 10 | iBGP | 5 | 21 |
| r4 | 2 9 | 200 | IGP | 20 | iBGP | 1 | 22 |
| r5 | 3 9 | 200 | IGP | 0 | iBGP | 3 | 31 |
| r6 | 6 9 | 200 | EGP | | eBGP | 0 | 6 |

1. LOCAL_PREF removes r1, although its AS path is short: AS 1 has set 100 on routes from its provider AS 7.
2. AS_PATH length removes r2, of length 3.
3. ORIGIN removes r6.
4. MED: r3 and r4 both come from AS 2, and r3 has the lower MED, so r4 goes. r5 comes from AS 3, so its MED is not compared with theirs.
5. No eBGP route is left among r3 and r5, so both stay.
6. Interior cost: r5 costs 3 and r3 costs 5, so R picks r5.

Note that r4 had the least interior cost of all, but it lost at the MED step before costs were compared. If r5 were withdrawn, R would pick r3. A router that compared MEDs pair by pair in the order the routes arrived could pick differently, which is one source of the MED oscillations of RFC 3345.

## Correctness

The full proof is in [the correctness proof](#proof-correctness).

**The decision process.** Each step keeps the routes that are best by one attribute, so it never empties a nonempty set, and the last step leaves one route because peer addresses differ. Each step depends on the set of routes and not on their order, so the choice is well defined. Line L1 removes routes that contain the router's own AS, so no AS-level loop is ever chosen.

**Convergence under the Gao-Rexford rules.** Assume that no AS is, through a chain of providers, its own provider, that customer routes get a higher LOCAL_PREF than peer and provider routes, and that export follows line L12. Then for each prefix, the ASes settle in three waves. First come the ASes above the origin in the customer-provider hierarchy, bottom up: their customer routes come only from customers below them, and a customer route beats any other. Next come the ASes that take a route from such a peer. Last come the rest, top down, from their providers. Then nothing changes, and the paths are loop-free, consistent and valley-free. Without these rules, BGP policies can encode the BAD GADGET of [path-vector routing](/path-vector-routing/) and oscillate for ever.

## Complexity

- **The decision process.** One pass per step over the $k$ candidates, with a table of the least MED of each neighbouring AS, so $O(k)$ time and $O(k)$ space per prefix. A router of the Internet's core holds on the order of a million prefixes, each with a few candidates, and reruns the process only for prefixes that an UPDATE changes.
- **Convergence.** Under the Gao-Rexford rules, the number of waves is bounded by the depth of the provider hierarchy. Without them, there is no bound: some configurations never converge, and deciding whether a configuration has a stable state is NP-complete (Griffin, Shepherd and Wilfong). After a withdrawal, path exploration can make BGP try many longer paths, and the MRAI timer (30 seconds by default on eBGP sessions) multiplies each step.

| measure | bound | case |
|---|---|---|
| decision time per prefix | $O(k)$ | $k$ candidate routes |
| space per prefix | $O(k)$ | Adj-RIB-In |
| convergence | bounded | Gao-Rexford rules |
| convergence | may never happen | general policies |

## Properties

- **AS-level loop freedom** at every instant, from the AS_PATH check.
- **Policy first.** Path length is only the second criterion. BGP paths are often not shortest, by AS count or by distance.
- **Deterministic choice.** Every router chooses one route per prefix, and the same set of routes always gives the same choice, if MEDs are compared by groups.
- **Information hiding.** An AS reveals only the routes it chooses to export, not its topology or its preferences.
- **Incremental.** After the initial table exchange, only changes are sent.

## Variants and improvements

- **iBGP inside one AS.** The border routers of one AS share their external routes over iBGP. To avoid loops without a path change, a router does not pass a route learned over iBGP to another iBGP peer, which requires a full mesh of iBGP sessions. Route reflectors (RFC 4456) and confederations (RFC 5065) remove the full mesh, at the risk of new oscillations.
- **Multipath.** Many routers can install several routes that tie down to line L8 and spread flows among them; see [ECMP hashing](/ecmp-hashing/).
- **Route flap damping.** Suppress a prefix that changes too often.
- **Security.** BGP believes what its neighbours say, so an AS can announce prefixes it does not own (a hijack) or a more specific prefix that wins by [longest prefix match](/longest-prefix-match/). The RPKI lets routers check that an AS may originate a prefix (RFC 6811), and BGPsec signs whole AS paths (RFC 8205).
- **Inside data centres.** Some large data centres run eBGP between every layer of switches as their only routing protocol, because it is simple and its policies are easy to control.

## When to use it

BGP is the only protocol used between ASes on the Internet, and every network with more than one provider runs it. Inside an AS, an IGP such as OSPF or IS-IS ([link-state routing](/link-state-routing/)) computes paths to the border routers, and iBGP carries the external routes over them. BGP is also used where its policy control matters more than fast convergence, as in large data centres and VPN services.

## Pitfalls

- **Comparing MED across ASes.** MED values from different neighbours have no common meaning. The default is to compare them only within one neighbouring AS. Comparing them in arrival order can make the choice depend on timing and, with route reflectors, oscillate.
- **Policies that break Gao-Rexford.** A backup arrangement in which an AS prefers a route through a provider to a route through a customer can create a dispute wheel. Networks have oscillated for this reason.
- **Leaks.** An AS that sends routes from one provider to another provider breaks the valley-free rule and can attract and drop large amounts of traffic. Export filters must follow line L12.
- **Slow withdrawal.** After a prefix disappears, BGP can take minutes to remove it everywhere, because of path exploration and the MRAI timer.
- **Hot-potato shifts.** A change of interior cost can change the exit chosen at line L8 for many prefixes at once, and shift traffic between neighbouring ASes; see [hot-potato routing](/hot-potato-routing/).

## Implementations

The Python code implements the decision process of RFC 4271 Section 9.1.2, and an AS-level simulation of BGP with customer, peer and provider links, the Gao-Rexford preferences, valley-free export, FIFO links with seeded random delays and batched updates. The tests check each tie-break in order, the MED rule within one neighbouring AS, and the independence of the result from the order of the candidates. On seeded random AS hierarchies, they check that the simulation converges, that every AS reaches every prefix by a loop-free, valley-free path whose suffix is the next AS's path, that customer routes win wherever they exist, and that the result does not depend on the timing.

## History

The Exterior Gateway Protocol of the early Internet assumed a tree of networks. BGP, first specified by Lougheed and Rekhter in RFC 1105 (1989), sent the AS path with each route so that the networks could form any graph without loops. BGP-4 added classless prefixes (CIDR) in the mid 1990s, and its current specification is RFC 4271 (2006). The theory of BGP convergence came later. Varadhan, Govindan and Estrin noted in the 1990s that policies can oscillate. Gao and Rexford (2001) showed that the economic rules most ASes follow guarantee convergence. Griffin, Shepherd and Wilfong (2002) defined the stable paths problem and showed that deciding whether a stable state exists is NP-complete.

## References
