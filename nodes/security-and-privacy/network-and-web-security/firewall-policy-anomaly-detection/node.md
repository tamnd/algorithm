---
tag: MRZ666
kind: algorithm
slug: firewall-policy-anomaly-detection
name: Firewall policy anomaly detection
aliases:
- Al-Shaer firewall analysis
- rule shadowing detection
area: security-and-privacy/network-and-web-security
level: advanced
summary: "Finds shadowed, redundant, generalized and correlated rules in an ordered firewall rule list by comparing the packet sets of rule pairs."
model: word-ram
complexity:
  vars: {m: the number of rules, d: the number of header fields}
  time: {worst: Θ(m^2 d), average: Θ(m^2 d), best: Θ(m^2 d)}
  space: {extra: O(1)}
properties: {deterministic: true}
history:
  year: 2004
  people: [Ehab Al-Shaer, Hazem Hamed]
  note: "Al-Shaer and Hamed defined the shadowing, correlation, generalization and redundancy anomalies of a single firewall and their detection in 2004, and extended them to distributed firewalls in the same year."
prereqs: [packet-classification, access-control-list]
see_also: [interval-tree, segment-tree, range-tree, binary-decision-diagram, base-rate-fallacy-intrusion-detection]
sources:
  - paper: "Ehab S. Al-Shaer and Hazem H. Hamed, Modeling and management of firewall policies, IEEE Transactions on Network and Service Management 1(1), 2004, pages 2 to 10, doi:10.1109/TNSM.2004.4623689"
    locator: "the relations between rules, the definitions of shadowing, correlation, generalization and redundancy, and the policy tree used to detect them"
  - paper: "Ehab S. Al-Shaer and Hazem H. Hamed, Discovery of policy anomalies in distributed firewalls, IEEE INFOCOM 2004, pages 2605 to 2616, doi:10.1109/INFCOM.2004.1354680"
    locator: the intra-firewall anomaly classes and their extension to rules on different firewalls of a path
---

Firewall policy anomaly detection checks an ordered list of firewall rules for pairs of rules that conflict or repeat each other. Each rule matches a set of packets, given by one interval for each header field, such as the protocol, the source and destination addresses and the ports, and the first rule that matches a packet decides it. For an earlier rule $R_x$ and a later rule $R_y$, Al-Shaer and Hamed (2004) named four classes: shadowing, where $R_y$ never acts because $R_x$ catches all its packets with another action; redundancy, where a rule can be removed without a change; generalization, where $R_y$ covers $R_x$ with another action; and correlation, where the two overlap partly with different actions. The check compares each pair of rules in $\Theta(m^2 d)$ time for $m$ rules of $d$ fields. It is exact for each pair, but it is not a full check of the policy: a rule can be covered by several earlier rules together, and no single pair shows that. The analysis only reads the rule list and needs no access to a network.

## In plain words

A firewall reads its rules from the top and uses the first rule that fits a packet. Rules are easy to add and hard to keep in order, so a long list often has mistakes.

The check looks at each pair of rules, an earlier one and a later one, and asks how the packets they match relate. If the earlier rule already catches every packet of the later rule with another answer, the later rule can never act, which is shadowing. If a rule could be deleted and every packet would get the same answer, it is redundant. If a later rule is wider and gives the other answer, it is a generalization, which is often on purpose but worth a look. If the two rules overlap only in part and give different answers, the order decides the overlap, which is a correlation.

## The problem

A rule $R_i$ has a box $B_i = I_{i,1} \times \cdots \times I_{i,d}$, a product of $d$ non-empty integer intervals, and an action such as allow or deny. An address prefix such as 192.0.2.0/24 is the interval of its addresses, and "any" is the full range. The decision on a packet $p$ is the action of the first $R_i$ with $p \in B_i$, or a default action. The input is the list $R_1, \ldots, R_m$. The output is the list of pairs $x < y$ in each class:

- **shadowing:** $B_y \subseteq B_x$ and the actions differ;
- **redundancy (later):** $B_y \subseteq B_x$ and the actions are the same, so $R_y$ can be removed;
- **generalization:** $B_x \subsetneq B_y$ and the actions differ;
- **redundancy (earlier):** $B_x \subsetneq B_y$, the actions are the same, and no rule between them meets $B_x$ with another action, so $R_x$ can be removed;
- **correlation:** $B_x$ and $B_y$ meet, neither contains the other, and the actions differ.

## The algorithm

```pseudo id=main
ANOMALIES(R[1..m])
L1  A ← empty list
L2  for x ← 1 to m - 1 do
L3      blocked ← false     ▷ a rule after x meets R[x] with another action
L4      for y ← x + 1 to m do
L5          rel ← RELATION(B[x], B[y]) ; same ← (action[x] = action[y])
L6          if rel ≠ DISJOINT then
L7              if rel ∈ {EQUAL, SUPERSET} then add (same ? REDUNDANT-LATER : SHADOWING, x, y)
L8              else if rel = SUBSET and not same then add (GENERALIZATION, x, y)
L9              else if rel = SUBSET and not blocked then add (REDUNDANT-EARLIER, x, y)
L10             else if rel = CORRELATED and not same then add (CORRELATION, x, y)
L11             if not same then blocked ← true
L12 return A
```

RELATION compares the boxes field by field. Two boxes are disjoint if some pair of intervals is disjoint. Box $B_x$ is inside $B_y$ if each interval of $B_x$ is inside the interval of $B_y$ in the same field. SUBSET means that $B_x$ is strictly inside $B_y$, and SUPERSET means the reverse. The flag of line L3 records, for the fixed $x$, whether some rule after $x$ and before the current $y$ meets $B_x$ with another action. Line L11 updates it after the tests of the current pair, so line L9 sees only the rules strictly between $x$ and $y$.

The code also has IS-DEAD, which decides whether a rule is covered by the union of all earlier rules. It subtracts each earlier box from the pieces of the rule that remain; the difference of two boxes is at most $2d$ disjoint boxes.

## Example

The policy uses documentation addresses only. The fields are protocol, source, source port, destination and destination port, and the default action is deny.

| rule | protocol | source | source port | destination | destination port | action |
| --- | --- | --- | --- | --- | --- | --- |
| $R_1$ | tcp | 198.51.100.0/25 | any | 203.0.113.10 | 80 | allow |
| $R_2$ | tcp | 198.51.100.0/24 | any | 203.0.113.10 | 80 | deny |
| $R_3$ | tcp | 198.51.100.200 | any | 203.0.113.10 | 80 | allow |
| $R_4$ | tcp | 198.51.100.128/26 | any | 203.0.113.0/24 | any | allow |
| $R_5$ | udp | 192.0.2.53 | 53 | 203.0.113.0/24 | any | allow |
| $R_6$ | udp | 192.0.2.0/24 | 53 | 203.0.113.0/24 | any | allow |
| $R_7$ | udp | 192.0.2.10 | 53 | 203.0.113.5 | 53 | allow |

ANOMALIES reports one pair of each class. All other pairs are disjoint, because the protocols, the source blocks or the destinations do not meet.

| pair | relation | line | class | meaning |
| --- | --- | --- | --- | --- |
| $R_1, R_2$ | $B_1 \subsetneq B_2$ | L8 | generalization | $R_2$ denies the rest of 198.51.100.0/24 after $R_1$ allows the first half |
| $R_2, R_3$ | $B_3 \subseteq B_2$ | L7 | shadowing | $R_3$ never acts: $R_2$ denies all its packets |
| $R_2, R_4$ | correlated | L10 | correlation | from 198.51.100.128/26 to 203.0.113.10 port 80, $R_2$ denies what $R_4$ allows |
| $R_5, R_6$ | $B_5 \subsetneq B_6$ | L9 | redundancy (earlier) | $R_5$ can be removed |
| $R_6, R_7$ | $B_7 \subseteq B_6$ | L7 | redundancy (later) | $R_7$ can be removed |

For $x = 5$, no rule between $R_5$ and $R_6$ exists, so blocked is false at line L9. A packet from 198.51.100.150 to 203.0.113.10 port 80 is denied by $R_2$, and the same packet to 203.0.113.11 is allowed by $R_4$. The correlation is a question for the administrator: maybe $R_4$ was meant to come first.

## Correctness

RELATION is exact because a box is a product of intervals: two boxes meet if and only if every pair of intervals meets, and one box is inside another if and only if each of its intervals is. Lines L7 to L10 then test the five definitions directly, and the flag of line L3 is true at line L9 exactly when some rule strictly between $x$ and $y$ meets $B_x$ with another action. A shadowed or later-redundant rule never decides a packet, because each of its packets is caught by $R_x$ first. Removing an earlier-redundant $R_x$ changes no decision: a packet that $R_x$ decided now reaches either a rule between the two, which has the same action, or $R_y$, which has the same action. The full proofs are in [proofs/correctness.md](proofs/correctness.md).

## Complexity

- **Time.** Line L5 compares $d$ pairs of intervals, and lines L6 to L11 add constant work, for each of the $m(m-1)/2$ pairs. So the time is $\Theta(m^2 d)$ on the word-RAM in every case.
- **Space.** $O(1)$ extra besides the output list, which can hold up to $m(m-1)/2$ pairs.
- **Union coverage.** IS-DEAD is exact but can produce a number of pieces that grows exponentially with the number of rules. It is for small policies or for one suspect rule.

## Properties

- **Pairwise.** Each class is about one pair. The output lists conflicts to review; it does not say which rule is wrong.
- **Exact for each pair.** Integer intervals make the relations exact, with no sampling of packets.
- **Not complete for the policy.** A rule covered by a union of earlier rules is dead but can show only generalization or correlation pairs.
- **Read only.** The check works on the text of the rules and never sends a packet.

## Variants and improvements

- **Policy tree.** Al-Shaer and Hamed store the rules in a tree with one level for each field, so that rules that share field values share a path. This finds the same anomalies and avoids comparing rules that differ in an early field.
- **Distributed firewalls.** Their INFOCOM 2004 paper also checks rules on different firewalls of a path, for example a packet that one firewall allows and a later one blocks.
- **Decision diagrams.** A [binary decision diagram](/binary-decision-diagram/) or a firewall decision diagram represents the whole decision function, so it can find dead rules that are covered by a union and compare two policies exactly.
- **Faster pair search.** For large rule sets, [interval trees](/interval-tree/) or [range trees](/range-tree/) on one or two fields find the pairs that meet without comparing all pairs. The same structures appear in [packet classification](/packet-classification/).

## When to use it

Use the pairwise check before loading a changed rule list, or as part of a review of an [access control list](/access-control-list/) on a router or a host firewall. It is quick, its classes are easy to explain, and each finding names two rules. Generalization is often intended, for example a final rule that denies all traffic after specific allow rules, so a tool should report it with a lower weight. When the question is whether a rule can ever act, or whether two policies decide every packet the same way, use the union check or a decision diagram, since pairs alone can miss it.

## Pitfalls

- **Only equal boxes in line L7.** If line L7 tests only rel = EQUAL, a later rule strictly inside a wider earlier rule is not reported as shadowed, which is the most common case. Line L7 must test EQUAL and SUPERSET, which together mean $B_y \subseteq B_x$.
- **A weak test in line L9.** If line L9 reports redundancy without the blocked flag, or with a flag that only counts rules in a generalization or correlation with $R_x$, then a rule between them that lies inside $B_x$ with another action is missed. Removing $R_x$ would then change the decision on that rule's packets. Line L11 must set the flag for every rule that meets $B_x$ with another action.
- **Updating the flag too early.** If line L11 runs before line L9 for the same $y$, a rule $R_y$ with another action blocks itself. That is harmless only because line L9 needs the same action; if the classes change, keep the update after the tests.
- **Trusting the pairs.** A rule covered by two earlier rules together never acts, but each pair shows only a correlation or a generalization. Use IS-DEAD or a decision diagram for that question.
- **Mixed address families.** An IPv4 prefix and an IPv6 prefix such as 2001:db8::/32 must not be compared as integers in one field. Use a separate field or a separate policy for each family.

## Implementations

## History

Al-Shaer and Hamed (IEEE Transactions on Network and Service Management, 2004) defined the relations between filtering rules and the shadowing, correlation, generalization and redundancy anomalies, and built a policy tree to find them. In the same year, their INFOCOM paper extended the classes to rules on different firewalls of a network path. Later work added decision diagrams that represent the whole policy, which also find rules that are covered by several earlier rules together.

## References
