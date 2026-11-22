---
tag: YC5F7Y
kind: concept
slug: dns-cache-poisoning
name: DNS cache poisoning
aliases:
- Kaminsky attack
- DNS spoofing
area: security-and-privacy/network-and-web-security
level: core
summary: An attacker races the real server with forged replies so that a resolver caches a false record, helped by guessing the query id and port.
history:
  year: 2009
  people: [Bert Hubert, Remco van Mook]
  note: RFC 5452 (January 2009) made random query IDs and source ports a requirement and gave the model of forgery used here. DNSSEC (RFC 4033 to 4035, 2005) adds signatures that remove the race.
see_also: [ingress-filtering, nonce, birthday-paradox, digital-signature, man-in-the-middle-attack, bgp-prefix-hijacking, syn-flooding]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc5452"
    title: Bert Hubert and Remco van Mook, Measures for making DNS more resilient against forged answers, RFC 5452, January 2009
    locator: Section 7.1 (the symbols), Section 7.2 (the probability of a successful forgery), Section 9.1 (the rules for accepting an answer) and Section 9.2 (random source ports and IDs)
  - paper: "David Dagon, Manos Antonakakis, Paul Vixie, Tatuya Jinmei and Wenke Lee, Increased DNS forgery resistance through 0x20-bit encoding: security via leet queries, ACM CCS 2008, pages 211 to 222, doi:10.1145/1455770.1455798"
    locator: the description of the encoding and its analysis of the extra entropy per query name
  - url: "https://www.rfc-editor.org/rfc/rfc4033"
    title: Roy Arends, Rob Austein, Matt Larson, Dan Massey and Scott Rose, DNS security introduction and requirements, RFC 4033, March 2005
    locator: the overview of the services DNSSEC gives (origin authentication and data integrity) and of what it does not give; the records and the protocol changes are in RFC 4034 and RFC 4035
---

DNS cache poisoning puts a false record into the cache of a DNS resolver, so that the resolver gives the wrong answer to every client that asks while the record lives. The classic form is an off-path race: the attacker sends forged replies that claim to come from the real name server, and the resolver accepts the first reply that matches its query. A reply must match a 16-bit query ID and the resolver's source port, so making both random is the main defense, and DNSSEC signatures remove the race. The attack needs forged source addresses, which links it to [ingress filtering](/ingress-filtering/).

## In plain words

A receptionist phones a company to ask for a staff member's number, then waits for a callback. Whoever calls back first with an answer that sounds right gets written in the address book, and the receptionist gives that number to everyone for a week.

A trickster who cannot hear the call can still phone in many fake callbacks, hoping one comes first and passes the check. If the receptionist checks only the name asked about, this is easy. If each request carries a random ticket number and a random extension to call back, the trickster must guess both, and the chance becomes tiny. A signed answer stops the trick completely, because the trickster cannot sign.

## The idea

**The cache.** A recursive resolver answers clients by asking authoritative servers and keeps each answer for its time to live (TTL). One false record therefore reaches many clients, for as long as its TTL, which is why a cache is a better target than one client.

**The race.** The resolver sends a query over UDP and waits for a reply. RFC 5452 (Section 9.1) lists what an answer must match before a resolver accepts it: the question, the query ID, the source and destination addresses, and the ports. An attacker who is not on the path cannot see the query, so it must guess the fields it does not know and send forged replies with the address of the real server as source, during the short time before the real reply arrives. A forged source address passes only where [ingress filtering](/ingress-filtering/) is missing.

**The probability.** RFC 5452, Section 7, models one attempt. Let $I$ be the number of possible IDs (at most 65536), $P$ the number of source ports the resolver uses, $N$ the number of authoritative servers it may ask, $D$ the number of identical queries it has outstanding at once, $R$ the rate of forged replies per second, and $W$ the time window in seconds before the real answer arrives. The chance of success in one window is

$$
P_s = \frac{D \cdot R \cdot W}{N \cdot P \cdot I} .
$$

After a failed window the real answer is cached for its TTL, so in $T$ seconds there are about $A = T / \text{TTL}$ windows, and the chance that some window succeeds is $P_{cs} = 1 - (1 - P_s)^A$ (theorem, under the model's assumption that the attacker has no information about the ID and port beyond their ranges).

**Defenses**, each with the adversary it stops:

| defense | what it adds | stops | does not stop |
|---|---|---|---|
| Random query ID over all 65536 values (RFC 5452, Section 9.2) | the factor $I$ | off-path guessing with a known ID | an attacker who sees the query |
| Random source port from a large range (Section 9.2) | the factor $P$ | off-path guessing with a known port | an attacker who sees the query |
| One outstanding query per question | $D = 1$ | the gain from many identical queries, a [birthday](/birthday-paradox/) effect | single-query guessing |
| Random case in the query name, 0x20 (Dagon et al.) | about one bit per letter, when the server copies the case | off-path guessing | names with few letters, servers that do not copy the case |
| Accepting records only for the zone asked about | limits what a reply may add | out-of-zone extra records (heuristic) | false records inside the zone |
| DNSSEC (RFC 4033 to 4035) | a [digital signature](/digital-signature/) over the records | any forged data, on path or off path, for signed zones checked by a validating resolver | unsigned zones, and denial of service |

The ID, the port and the case bits act together as a [nonce](/nonce/) that an off-path attacker must guess. None of them helps against an on-path attacker, who sees the query, as in a [man-in-the-middle attack](/man-in-the-middle-attack/); only signatures do.

## Examples

**A cache before and after.** A resolver's cache drawn as a table, with documentation names and addresses. The forged entry is shown only as the state that defenses must prevent.

| name | type | value | TTL left | source |
|---|---|---|---|---|
| www.example.com | A | 192.0.2.10 | 3600 | the authoritative server for example.com |
| mail.example.net | A | 198.51.100.25 | 1200 | the authoritative server for example.net |
| www.example.org | A | 203.0.113.99 | 86400 | a forged reply that won a race |

Every client that asks for www.example.org in the next day gets 203.0.113.99, an address the zone owner never published. A validating resolver would have rejected the reply if example.org were signed, because the record would carry no valid signature.

**The effect of the port.** Take one authoritative server ($N = 1$), $D = 1$, $I = 65536$, and an attacker that sends $R = 10{,}000$ forged replies per second into a window of $W = 0.1$ s, so 1000 replies per window.

| resolver | $P$ | $P_s$ per window | windows for a 50% chance |
|---|---|---|---|
| fixed source port | 1 | $1000/65536 \approx 0.0153$ | about 45 |
| random port from 16,384 | 16384 | about $9.3 \times 10^{-7}$ | about 745,000 |

With a TTL of one hour, 745,000 windows take about 85 years (computed from the model). A fixed port leaves only the ID, which falls within a few dozen windows; random ports multiply the work by $P$.

## Where it is used

- **Resolver design.** The rules of RFC 5452 are part of every current resolver: random IDs, random ports, strict matching of replies, and one outstanding query per question.
- **DNSSEC.** Validating resolvers check signatures from the root down, which is the only defense against attackers on the path.
- **Network defense.** [Ingress filtering](/ingress-filtering/) removes the forged source addresses the race needs. Routing attacks such as [BGP prefix hijacking](/bgp-prefix-hijacking/) can put an attacker on the path, which turns an off-path guess into an on-path attack and leaves DNSSEC as the defense.
- **Threat models.** Any protocol that trusts DNS answers without its own authentication, such as plain mail delivery, inherits the risk of a poisoned resolver.

## References
