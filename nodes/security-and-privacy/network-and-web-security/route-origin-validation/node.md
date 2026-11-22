---
tag: BC5B6R
kind: algorithm
slug: route-origin-validation
name: Route origin validation
aliases:
- RPKI origin validation
- ROV
area: security-and-privacy/network-and-web-security
level: advanced
summary: Marks each BGP route valid, invalid or not found by matching its prefix and origin AS against signed route origin authorizations.
model: word-ram
complexity:
  vars: {L: the length of the route prefix in bits, c: the number of VRPs that cover the route, N: the number of VRPs, W: the address width}
  time: {worst: O(L + c), average: O(L + c), best: O(1)}
  space: {extra: O(1)}
properties: {deterministic: true, validates_origin_only: true, online: true}
history:
  year: 2013
  people: [Pradosh Mohapatra, John Scudder, David Ward, Randy Bush, Rob Austein]
  note: RFC 6811 (January 2013) defined the procedure on top of the Resource Public Key Infrastructure of RFC 6480 (February 2012).
prereqs: [bgp, trie]
see_also: [bgp-prefix-hijacking, longest-prefix-match, radix-tree, digital-signature, ingress-filtering, packet-classification]
sources:
  - paper: "P. Mohapatra, J. Scudder, D. Ward, R. Bush and R. Austein, BGP Prefix Origin Validation, RFC 6811, January 2013"
    url: https://www.rfc-editor.org/rfc/rfc6811
    locator: Section 2 (Covered, Matched, the three states, the route origin ASN and AS 0), Section 2.1 (pseudocode, with the prose authoritative) and Section 6 (forged origins are not prevented)
  - paper: "M. Lepinski and S. Kent, An Infrastructure to Support Secure Internet Routing, RFC 6480, February 2012"
    url: https://www.rfc-editor.org/rfc/rfc6480
    locator: Section 3 (route origin authorizations)
  - paper: "Y. Gilad, S. Goldberg, K. Sriram, J. Snijders and B. Maddison, The Use of maxLength in the Resource Public Key Infrastructure (RPKI), RFC 9319, BCP 185, October 2022"
    url: https://www.rfc-editor.org/rfc/rfc9319
    locator: Section 3 (forged-origin sub-prefix hijacks) and Section 5 (minimal ROAs)
  - paper: "M. Lepinski and K. Sriram (editors), BGPsec Protocol Specification, RFC 8205, September 2017"
    url: https://www.rfc-editor.org/rfc/rfc8205
    locator: the abstract and the introduction (signatures over the AS path)
---

Route origin validation (ROV) checks whether the autonomous system (AS) that originates a [BGP](/bgp/) route is allowed to originate that prefix. The allowed pairs come from route origin authorizations (ROAs): objects signed in the Resource Public Key Infrastructure (RPKI) by the holder of the address space, each naming one AS, some prefixes and a maximum length. A router reduces the validated ROAs to triples called VRPs and gives each route one of three states: Valid, Invalid or NotFound. The check catches announcements from the wrong AS, a common form of [BGP prefix hijacking](/bgp-prefix-hijacking/), but it does not check the rest of the AS path.

## In plain words

The owner of a block of addresses signs a short statement: "only network 64496 may announce my block, and no piece smaller than this size". Routers collect these statements, check the signatures once, and keep a list.

When a route arrives, the router looks for statements about blocks that contain the announced block. If none exist, it knows nothing, and the route is "not found". If one of them names the network that announced the route and allows that size, the route is "valid". If statements exist but none fits, the route is "invalid", and the router can choose to drop it. The router only checks who started the route, not who passed it along.

## The problem

**Input.** A set of VRPs, each a triple (prefix $q$, maximum length $\ell_{\max}$, ASN $a$), and a route with prefix $P$ of length $|P|$ and an AS_PATH. The route origin ASN is the rightmost AS in the final segment of the AS_PATH if that segment is an AS_SEQUENCE; the speaker's own AS if the AS_PATH is empty or the final segment is a confederation segment; and the value NONE otherwise, for example for an AS_SET (RFC 6811, Section 2).

**Definitions** (RFC 6811, Section 2). A VRP covers $P$ if $|q| \le |P|$ and $q$ and $P$ agree on the first $|q|$ bits. A VRP matches the route if it covers $P$, $|P| \le \ell_{\max}$, and the origin ASN equals $a$. No route matches a VRP whose ASN is 0, and NONE matches no VRP.

**Output.** Valid if at least one VRP matches; Invalid if at least one VRP covers $P$ but none matches; NotFound if no VRP covers $P$.

The VRPs are stored in a [trie](/trie/) keyed by the bits of their prefixes, one trie per address family. The covering VRPs of $P$ are exactly the VRPs stored at the nodes on the path from the root to $P$.

## The algorithm

```pseudo id=main
VALIDATE(T, P, origin)           ▷ T: the trie of VRPs for the family of P
L1  state ← NotFound
L2  node ← the root of T
L3  for i ← 0 to |P| do           ▷ node holds the prefix of the first i bits of P
L4      for each VRP (ℓmax, a) stored at node do
L5          state ← Invalid       ▷ a VRP covers P
L6          if |P| ≤ ℓmax and origin ≠ NONE and a ≠ 0 and a = origin then return Valid
L7      if i = |P| or node has no child for bit i of P then stop the loop, else node ← that child
L8  return state
```

Line L5 records that $P$ is covered; line L6 tests the three conditions of a match and returns at the first one. The loop goes down the trie only along the bits of $P$, so it visits the covering VRPs and nothing else. RFC 6811 gives similar pseudocode in Section 2.1 and states that the prose definitions are authoritative.

## Example

All prefixes and AS numbers here are documentation values. The VRPs are:

| VRP prefix | max length | ASN |
|---|---|---|
| 192.0.2.0/24 | 24 | 64496 |
| 198.51.100.0/24 | 25 | 64497 |
| 203.0.113.0/24 | 24 | 0 |
| 2001:db8:1000::/36 | 48 | 64498 |

Routes received by a router in AS 64510:

| route prefix | AS_PATH | origin | covering VRPs | state | reason |
|---|---|---|---|---|---|
| 192.0.2.0/24 | 64500 64496 | 64496 | 192.0.2.0/24 | Valid | covered, length 24 ≤ 24, ASN equal |
| 192.0.2.0/25 | 64500 64496 | 64496 | 192.0.2.0/24 | Invalid | length 25 > 24 |
| 192.0.2.0/24 | 64500 64511 | 64511 | 192.0.2.0/24 | Invalid | ASN differs |
| 198.51.100.128/25 | 64497 | 64497 | 198.51.100.0/24 | Valid | length 25 ≤ 25 |
| 203.0.113.0/24 | 64501 | 64501 | 203.0.113.0/24 | Invalid | a VRP with ASN 0 matches nothing |
| 2001:db8:1000::/48 | 64500 64498 | 64498 | 2001:db8:1000::/36 | Valid | length 48 ≤ 48 |
| 2001:db8:1000::/48 | 64500 {64498 64499} | NONE | 2001:db8:1000::/36 | Invalid | the final segment is an AS_SET |
| 2001:db8::/32 | 64499 | 64499 | none | NotFound | the /36 VRP is longer, so it does not cover |

The second and third rows are the two shapes of a hijack that ROV stops: a more specific prefix, and the wrong origin. The ASN 0 row shows how a holder says "this space must not be routed".

## Correctness

**Theorem.** VALIDATE returns the state defined in RFC 6811, Section 2, for every set of VRPs and every route. This is a statement about the computation; the security guarantee is the next paragraph.

The proof shows that the nodes visited by lines L3 and L7 hold exactly the VRPs that cover $P$: a VRP with prefix $q$ is stored at the node reached by the bits of $q$, and that node lies on the path of $P$ if and only if $|q| \le |P|$ and $q$ is a prefix of the bits of $P$. Line L6 then applies the definition of a match to each covering VRP. The full proof is in [proofs/correctness.md](proofs/correctness.md).

**Guarantee and its adversary.** Assume that the RPKI data is correct and fresh, that the router validated the signatures, and that the attacker controls a BGP speaker but no RPKI key of the address holder. Then a route that the attacker originates from its own AS for a prefix covered by VRPs that do not name that AS is Invalid. The guarantee does not hold against an attacker who puts the authorized AS at the right end of a forged AS_PATH: RFC 6811, Section 6, states that such a forged origin defeats the check, since it validates the origin, not the path.

## Complexity

In the [word RAM](/word-ram/) model with addresses of $W$ bits:

- **Time.** VALIDATE visits at most $|P| + 1 \le W + 1$ nodes and looks at each of the $c$ covering VRPs once, so it takes $O(L + c)$ time with $L = |P|$. The best case is $O(1)$: the root has no child for the first bit, or a VRP at the root matches.
- **Space.** The trie has $O(N W)$ nodes for $N$ VRPs; a path-compressed [radix tree](/radix-tree/) cuts this to $O(N)$. VALIDATE itself needs $O(1)$ extra space.
- **The oracle.** A linear scan over all VRPs takes $O(N)$ per route. The tests use it to check the trie.

## Properties

- **Three states.** NotFound keeps routes for space without ROAs usable during partial deployment.
- **Origin only.** The AS path beyond the origin is not checked.
- **Monotone in VRPs.** Adding a VRP can turn NotFound into Invalid or Valid, and Invalid into Valid, but never Valid into anything else.
- **Policy is local.** RFC 6811 gives a state; each operator decides whether to drop Invalid routes or only prefer Valid ones.

## Variants and improvements

- **Minimal ROAs.** RFC 9319 (BCP 185) recommends ROAs that list only the prefixes actually announced and avoid a maxLength longer than needed. A loose maxLength lets an attacker announce an unused more specific prefix with a forged origin and win by [longest prefix match](/longest-prefix-match/) while the route still validates (Section 3).
- **Path validation.** BGPsec (RFC 8205) has each AS sign the path as it forwards the route, which closes the forged-origin gap at the cost of a [digital signature](/digital-signature/) per hop.
- **Data structures.** Routers store VRPs in compressed tries or radix trees, the same structures used for forwarding tables.

## When to use it

Use ROV on every BGP router that accepts routes from neighbors, together with ROAs for your own space, to reject wrong-origin and too-specific announcements. Use it with prefix filters for customers, which work without the RPKI, and consider BGPsec or other path checks where forged paths are a concern.

## Pitfalls

- **Matching ASN 0.** If line L6 omits $a \ne 0$, a route originated from AS 0, or a careless implementation that treats a missing origin as 0, can become Valid for space whose holder said it must not be routed. Keep the test $a \ne 0$ in line L6.
- **Checking only the longest covering VRP.** If line L4 looks only at the VRP with the longest prefix, as in a forwarding lookup, a route covered by a /23 VRP for its origin and a /24 VRP for another AS becomes Invalid. Loop over every node from the root in line L3 and every VRP in line L4.
- **Forgetting the maximum length.** If line L6 omits $|P| \le \ell_{\max}$, every more specific announcement by the authorized AS, and every forged-origin sub-prefix, validates. Keep the length test.
- **Taking the origin from an AS_SET.** If the origin is read from an AS_SET as its last member, an attacker can list any AS in the set. Use NONE for an AS_SET, as RFC 6811 requires, so that line L6 never matches.
- **A loose maxLength in the ROA.** The algorithm is correct, but a ROA with maxLength /32 for a /24 allows a forged-origin hijack of any unused /25 to /32. Publish minimal ROAs.

## Implementations

The code is a synthetic model: it uses documentation prefixes and AS numbers, reads no RPKI data and speaks no BGP. It stores VRPs in a binary trie per family and checks it against a linear scan of the RFC 6811 definitions on 1500 random routes, together with the rules for the origin ASN.

## History

The RPKI architecture appeared as RFC 6480 in February 2012, with ROAs binding an AS to prefixes. Mohapatra, Scudder, Ward, Bush and Austein specified the validation procedure in RFC 6811 in January 2013. BGPsec followed in RFC 8205 in 2017 to protect the whole path, and RFC 9319 in 2022 gave advice on maxLength, because loose ROAs leave space open to forged-origin sub-prefix hijacks.

## References
