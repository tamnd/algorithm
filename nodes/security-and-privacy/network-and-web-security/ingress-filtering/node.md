---
tag: 2H2CT0
kind: technique
slug: ingress-filtering
name: Ingress filtering
aliases:
- source address validation
- BCP 38
area: security-and-privacy/network-and-web-security
level: intro
summary: A router at the edge of a network drops packets whose source address could not come from the link they arrived on. It stops forged sources at the network where they start.
history:
  year: 1998
  people: [Paul Ferguson, Daniel Senie, Fred Baker, Pekka Savola]
  note: Ferguson and Senie wrote RFC 2267 in 1998 and RFC 2827 (BCP 38) in 2000. Baker and Savola added the reverse path checks for multihomed networks in RFC 3704 (BCP 84) in 2004.
prereqs: [longest-prefix-match]
see_also: [syn-flooding, ip-traceback-problem, packet-classification, longest-prefix-match, bgp, firewall-policy-anomaly-detection, route-origin-validation]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc2827"
    title: Paul Ferguson and Daniel Senie, Network ingress filtering, defeating denial of service attacks which employ IP source address spoofing, RFC 2827 (BCP 38), May 2000
    locator: Section 3 (restricting forged traffic, with the filter on the link to a customer prefix), Section 4 (further capabilities) and Section 5 (liabilities)
  - url: "https://www.rfc-editor.org/rfc/rfc3704"
    title: Fred Baker and Pekka Savola, Ingress filtering for multihomed networks, RFC 3704 (BCP 84), March 2004
    locator: Sections 2.1 to 2.5 (access lists, strict, feasible path and loose reverse path forwarding, and loose RPF that ignores default routes) and Section 4 (solutions for multihomed networks)
  - url: "https://www.rfc-editor.org/rfc/rfc4987"
    title: Wesley M. Eddy, TCP SYN flooding attacks and common mitigations, RFC 4987, August 2007
    locator: Section 3.1 (filtering as a defense against SYN floods with forged sources)
---

Ingress filtering is the rule that a router drops a packet whose source address cannot belong to the network on the other side of the link it came in on. Applied at the edge of every network, it stops forged source addresses where they start, so attacks such as [SYN flooding](/syn-flooding/) with forged sources and reflection attacks lose their cover. RFC 2827 (BCP 38) gives the rule for a single link, and RFC 3704 (BCP 84) gives the reverse path checks that make it work for networks with more than one provider. Its one weakness is economic: the network that deploys it protects everyone else, not itself.

## In plain words

A post office near a village sees every letter that leaves the village. Each letter has a return address. If the return address is in another city, the letter is lying about where it came from, so the post office keeps it back. The post office in the big city cannot do this check, because letters from everywhere pass through it.

A router at the edge of a network is that village post office. It knows which addresses belong to the customers behind each link. A packet from a customer with a sender address that is not one of the customer's own is forged, and the router drops it. When the customer has two providers, the check must allow addresses that belong to either path, or it drops real traffic.

## When it applies

- A router sits at a point where the set of valid source addresses behind a link is known and small: a customer access link, a data center edge, a campus uplink.
- The traffic to stop carries forged source addresses: floods that hide their origin, reflection and amplification attacks that send replies to a victim, and blind attacks that need a trusted source address.
- The routing table already holds the needed facts. A reverse path check reuses the [longest prefix match](/longest-prefix-match/) lookup of the forwarding path, with the source address in place of the destination.
- It does not apply in the middle of the internet, where any source can arrive on any link, and it cannot stop forgery of an address inside the customer's own prefix.

## The template

A packet $p$ arrives on interface $i$. The holes are the set of valid prefixes for $i$, the choice of check, and what to do with a dropped packet. The cost per packet is one [packet classification](/packet-classification/) or one longest prefix match on the source address, in the [word RAM](/word-ram/) model with addresses as words.

```pseudo id=main
INGRESS-CHECK(p, i)
L1  s ← source address of p
L2  case MODE of
L3      acl:      pass ← s matches a prefix in ALLOWED[i]          ▷ hole: prefixes of the network behind i
L4      strict:   r ← LPM(s); pass ← r exists and i = interface of r
L5      feasible: pass ← i ∈ FEASIBLE(s)                          ▷ hole: every interface with a route to s
L6      loose:    r ← LPM(s); pass ← r exists and r is not a default route
L7  if pass then forward p
L8  else drop p and LOG(p, i)                                     ▷ hole: count, sample or alert
```

Line L3 is the BCP 38 filter: an access list per customer link with the prefixes assigned to that customer (RFC 2827, Section 3). Lines L4 to L6 are the unicast reverse path forwarding (uRPF) checks of RFC 3704, Section 2. Strict mode (line L4) passes a packet only if the router's best route back to the source leaves through the same interface. Feasible path mode (line L5) also accepts the interfaces of alternative routes that the router has learned but not chosen. Loose mode (line L6) asks only that some route to the source exists; RFC 3704, Section 2.5, adds that a default route must not count, or every source passes. The checks go from strong to weak: an address that passes strict passes feasible, and one that passes feasible passes loose, provided that its best route is not a default route. A source covered only by a default route through the arrival interface passes strict mode as written and fails loose mode.

**The guarantee.** Suppose every packet that leaves a network $N$ for the rest of the internet passes line L3, with $\text{ALLOWED}$ equal to the prefixes of $N$. Then no packet from $N$ reaches the rest of the internet with a source address outside $N$. The adversary here is any host inside $N$, with full control of the packets it sends. The guarantee says nothing about forgery of other addresses inside $N$, about packets from networks without the filter, or about traffic that uses real source addresses.

## Classic examples

- **SYN floods with forged sources.** [SYN flooding](/syn-flooding/) depends on sources that do not answer. A filter at the attacker's edge removes them, and RFC 4987, Section 3.1, lists filtering as the first defense.
- **Help for traceback.** If filters were everywhere, the source address would identify the network of origin, and the [IP traceback problem](/ip-traceback-problem/) would shrink to finding a host inside one network. [Probabilistic packet marking](/probabilistic-packet-marking/) and [hash-based IP traceback](/hash-based-ip-traceback/) exist because the filters are not everywhere.
- **Access lists as classification.** An ingress access list is a one-field instance of [packet classification](/packet-classification/), and its rules can conflict with the rest of the policy in the ways that [firewall policy anomaly detection](/firewall-policy-anomaly-detection/) finds.
- **Reverse path checks on routing data.** uRPF reads the table that [BGP](/bgp/) and the interior protocols fill. Its sibling on the control plane is [route origin validation](/route-origin-validation/), which checks that the origin of a route announcement is authorized, not the source of a packet.

## Variations

**A worked table.** An edge router of a provider has a customer link $i_1$ for the customer prefix 203.0.113.0/24 and an upstream link $i_0$ with a default route. A second customer, multihomed, owns 198.51.100.0/24 and reaches the router on link $i_2$, and also through another provider. The router's best route to 198.51.100.0/24 goes through the other provider over $i_0$ because of a shorter path, but it also has a route through $i_2$ that it did not choose. The table gives the decision for packets that arrive on the customer links.

| arrives on | source | acl (line L3) | strict (L4) | feasible (L5) | loose (L6) |
|---|---|---|---|---|---|
| $i_1$ | 203.0.113.9 | pass | pass | pass | pass |
| $i_1$ | 198.51.100.4 | drop | drop | drop | pass |
| $i_1$ | 192.0.2.1 (an address with no specific route) | drop | drop | drop | drop |
| $i_2$ | 198.51.100.4 | pass | drop | pass | pass |

Row 2 shows why loose mode is weak: it accepts a forged address that has any route. Row 4 shows why strict mode is wrong on multihomed links: routing is asymmetric, so the best route back to the source leaves on $i_0$, and a real packet is dropped. Feasible path mode accepts it because it uses all learned routes.

**Where to filter.** RFC 3704, Section 3, describes filters at several levels: on the host's first router, on the customer edge, on the provider edge and on peering links. A filter closer to the hosts knows a smaller set of valid addresses and is more exact.

**Egress filtering.** The same check, run by the customer on its own outgoing link, is often called egress filtering. It needs no help from the provider.

**Filtering on peering links.** On a link to another provider, the valid set is the customer cone of the peer, which changes with routing. Loose mode, or feasible path mode with the routes the peer announces, is the practical choice there (RFC 3704, Section 3.3).

## Pitfalls

- **Strict mode on asymmetric routes.** Using line L4 on a link to a multihomed customer drops real traffic whenever the best route back leaves on another interface. Use line L5, or an access list (line L3) with the customer's prefixes from both providers (RFC 3704, Section 4.2).
- **Loose mode with a default route.** If line L6 counts a default route as a route, every source passes and the check does nothing. RFC 3704, Section 2.5, describes loose mode that ignores default routes for this reason.
- **Stale access lists.** An access list that is not updated when a customer gets a new prefix drops the customer's real traffic. Generate line L3's list from the same records that assign prefixes.
- **The incentive gap.** The network that deploys a filter spends effort and protects other networks. A page or a report that says "the internet is protected by BCP 38" overstates it: the protection holds only for traffic from networks that filter (RFC 2827, Section 5, discusses liabilities).
- **Forgery inside the prefix.** A filter on a /24 cannot tell one host of the /24 from another. Hosts on a shared segment need a check at the first router or switch port.

## Exercises

1. Give the decision of each of the four modes for a packet with source 203.0.113.200 that arrives on $i_2$ in the worked table. Explain the strict and feasible results from the routes.
2. Prove that strict mode never drops a real packet on a link where the router's best route to each source in the customer's prefix leaves through that link.
3. Prove the order of the checks: for any routing table, the set of (source, interface) pairs that pass strict mode is contained in the set that passes feasible mode, and, among sources whose best route is not a default route, in the set that passes loose mode. Give a table and a packet that pass strict mode through a default route and fail loose mode.
4. A provider filters with line L3 on every customer link but not on peering links. Describe which forged sources can still enter the internet from the provider's network, and from where.

## References
