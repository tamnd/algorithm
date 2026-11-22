---
tag: M2Q0B6
kind: concept
slug: bgp-prefix-hijacking
name: BGP prefix hijacking
aliases:
- route hijacking
- IP hijacking
area: security-and-privacy/network-and-web-security
level: core
summary: An autonomous system announces a prefix it does not own, or a more specific one, so that traffic for it is routed to the attacker.
history:
  year: 2006
  people: [Sandra Murphy]
  note: RFC 4272 (January 2006) analyzed the lack of origin and path checks in BGP. The RPKI (RFC 6480, 2012), route origin validation (RFC 6811, 2013) and BGPsec (RFC 8205, 2017) followed.
see_also: [route-origin-validation, bgp, longest-prefix-match, dns-cache-poisoning, ingress-filtering, man-in-the-middle-attack, digital-signature]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc4272"
    title: Sandra Murphy, BGP security vulnerabilities analysis, RFC 4272, January 2006
    locator: Section 3.1.5.3 (the originating AS and false originations) and Section 4.1 (the residual risk)
  - paper: "Hitesh Ballani, Paul Francis and Xinyang Zhang, A study of prefix hijacking and interception in the Internet, ACM SIGCOMM 2007, pages 265 to 276, doi:10.1145/1282380.1282411"
    locator: the definitions of hijacking and interception and the analysis of how much of the Internet an AS can capture
  - url: "https://www.ripe.net/about-us/news/youtube-hijacking-a-ripe-ncc-ris-case-study/"
    title: RIPE NCC, YouTube hijacking, a RIPE NCC RIS case study, 2008
    locator: the timeline of the event of 24 February 2008
  - url: "https://www.rfc-editor.org/rfc/rfc9319"
    title: Yossi Gilad, Sharon Goldberg, Kotikalapudi Sriram, Job Snijders and Ben Maddison, The use of maxLength in the Resource Public Key Infrastructure (RPKI), RFC 9319, BCP 185, October 2022
    locator: Section 3 (forged-origin sub-prefix hijacks) and Section 5 (minimal ROAs)
---

BGP prefix hijacking is the announcement, by an autonomous system (AS), of an IP prefix that its holder did not allow that AS to announce. [BGP](/bgp/) speakers believe the announcement unless they filter it, so traffic for the prefix flows toward the wrong AS: from part of the Internet when the announcement competes with the real route for the same prefix, and from almost all of it when the false prefix is more specific, because routers forward by [longest prefix match](/longest-prefix-match/). The traffic can be dropped, read or passed back to the real destination. [Route origin validation](/route-origin-validation/) stops announcements from the wrong origin, and BGPsec signs the whole path.

## In plain words

Post offices learn where to send letters from notes their neighbors pass on: "letters for streets 1 to 100 come through me". Nobody checks these notes. A dishonest office can claim streets 1 to 100 too, and the offices near it believe whichever claim sounds closer.

It can do even better by claiming only streets 1 to 50. Every office prefers the most precise note, so all letters for those streets go to the liar, from everywhere. The fix is a signed list, kept by the true owner of the streets, that says which office may claim them and how small a piece may be claimed.

## The idea

**Why it works.** BGP has no built-in way to check that the AS at the start of an AS path holds the prefix, or that the path is real. RFC 4272 (Section 3.1.5.3) describes false originations as a basic weakness, and Section 4.1 notes that the protocol alone leaves this risk. Each AS picks routes by local policy, often preferring routes from customers and then shorter AS paths, and forwards packets by the longest matching prefix in its table.

**Kinds of hijack.** The adversary controls the BGP speakers of one AS, and its neighbors accept some of its announcements; it does not control other ASes or the RPKI keys of the prefix holder.

| kind | what is announced | who is affected | stopped by origin validation |
|---|---|---|---|
| Exact-prefix origin hijack | the same prefix, with the attacker's AS as origin | ASes that prefer the false route by policy or path length | yes, if a ROA exists |
| Sub-prefix hijack | a more specific prefix, attacker as origin | nearly every AS that accepts it, by longest prefix match | yes, if a ROA exists |
| Forged-origin hijack | a path that ends with the true origin AS | as above, minus some path length | no for an exact prefix; yes for a sub-prefix if the ROA's maxLength is minimal |
| Squatting | unused space that nobody announces | everyone, since there is no competing route | only if the holder publishes a ROA, for example one for AS 0 |

**Hijack and interception.** In a hijack the traffic ends at the attacker and the real destination is unreachable for the affected part of the Internet. In an interception the attacker keeps a working route to the real destination and forwards the traffic on after it passes, so the service still works and the hijack is harder to notice. Ballani, Francis and Zhang (SIGCOMM 2007) studied how much traffic an AS can capture in each mode, given the policies ASes follow.

**Defenses.**

- Filtering of customer announcements by the list of prefixes each customer holds.
- [Route origin validation](/route-origin-validation/) with ROAs in the RPKI, and minimal ROAs without loose maxLength (RFC 9319).
- Path validation with BGPsec, which needs a [digital signature](/digital-signature/) from each AS on the path.
- Monitoring of public route collectors to detect unexpected origins and more specific prefixes quickly.

## Examples

All prefixes and AS numbers are documentation values. AS 64496 holds 198.51.100.0/24 and announces it. The ASes form a line 64496 - 64500 - 64501 - 64502 - 64503 - 64511, and, as a simplifying assumption, each prefers the shortest AS path.

**Exact-prefix hijack.** AS 64511 also announces 198.51.100.0/24.

| AS | path to 64496 | path to 64511 | chosen origin for 198.51.100.0/24 |
|---|---|---|---|
| 64500 | 64496 (1 AS) | 64501 64502 64503 64511 (4) | 64496 |
| 64501 | 64500 64496 (2) | 64502 64503 64511 (3) | 64496 |
| 64502 | 64501 64500 64496 (3) | 64503 64511 (2) | 64511 |
| 64503 | 64502 64501 64500 64496 (4) | 64511 (1) | 64511 |

The Internet splits: ASes closer to the attacker send it the traffic.

**Sub-prefix hijack.** AS 64511 announces only 198.51.100.0/25. No AS has a competing /25, so all install it next to the /24. The forwarding table of AS 64500 then reads:

| prefix | next AS | destination 198.51.100.10 | destination 198.51.100.200 |
|---|---|---|---|
| 198.51.100.0/24 | 64496 | matches, 24 bits | matches, 24 bits, chosen |
| 198.51.100.0/25 | 64501, toward 64511 | matches, 25 bits, chosen | does not match |

Even AS 64500, the direct neighbor of the holder, sends the lower half of the block to the attacker.

**With origin validation.** The holder publishes a ROA for (198.51.100.0/24, maxLength 24, AS 64496). Routers that drop Invalid routes then reject both announcements above: the /24 from 64511 has the wrong origin, and the /25 is longer than 24. A forged path that ends in 64496 for the /25 is still Invalid because of the maxLength. If the ROA had maxLength 25, that forged /25 would be Valid, which is the case RFC 9319 warns about.

**A public case.** On 24 February 2008, an AS announced a more specific prefix inside the address space of a well-known video site, and the site was unreachable from much of the Internet for about two hours until the announcement was withdrawn, according to the RIPE NCC case study. The event is a sub-prefix hijack of the kind in the second table.

## Where it is used

- **Routing security.** The threat drives the RPKI, [route origin validation](/route-origin-validation/), RFC 9319 and BGPsec.
- **DNS and other services.** A hijack of the prefix of a name server or of a resolver puts the attacker on the path, which defeats the random IDs and ports that protect against [DNS cache poisoning](/dns-cache-poisoning/) and leaves DNSSEC as the defense.
- **Traffic analysis.** Interception lets an AS observe traffic while keeping the service working, a [man-in-the-middle attack](/man-in-the-middle-attack/) at the routing level that end-to-end encryption limits.
- **Operations.** Monitoring systems compare announcements with ROAs and with history to raise alarms on new origins and more specific prefixes.

## References
