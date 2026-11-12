---
tag: JDP7S8
kind: problem
slug: packet-classification
name: Packet classification
aliases:
- multi-field classification
- multi-field packet classification
area: systems/networking-algorithms
level: advanced
summary: "Given an ordered list of rules, each a range or prefix on several header fields, find the first rule that matches a packet. Firewalls, QoS and software switches do this per packet."
prereqs: [longest-prefix-match, interval-stabbing-query]
see_also: [hicuts, tuple-space-search, tree-bitmap, orthogonal-point-enclosure, planar-point-location, range-searching-lower-bound, orthogonal-range-searching, bit-set]
sources:
  - paper: doi:10.1109/65.912717
    title: Pankaj Gupta and Nick McKeown, Algorithms for packet classification, IEEE Network 15(2), 2001
    locator: pages 24 to 32 (the problem statement, the geometric view, the bounds for point location and the table of methods)
  - paper: doi:10.1145/1108956.1108958
    title: David E. Taylor, Survey and taxonomy of packet classification techniques, ACM Computing Surveys 37(3), 2005
    locator: pages 238 to 275
  - book: isbn:9780120884773
    title: George Varghese, Network Algorithmics, Morgan Kaufmann, 2005
    locator: Chapter 12, Packet Classification
  - paper: doi:10.1145/285237.285282
    title: V. Srinivasan, George Varghese, Subhash Suri and Marcel Waldvogel, Fast and scalable layer four switching, ACM SIGCOMM 1998
    locator: pages 191 to 202 (grid of tries and crossproducting)
  - paper: doi:10.1145/285237.285283
    title: T. V. Lakshman and D. Stiliadis, High-speed policy-based packet forwarding using efficient multi-dimensional range matching, ACM SIGCOMM 1998
    locator: pages 203 to 214 (the bit vector scheme)
  - paper: doi:10.1145/316188.316217
    title: Pankaj Gupta and Nick McKeown, Packet classification on multiple fields, ACM SIGCOMM 1999
    locator: pages 147 to 160 (recursive flow classification)
  - paper: doi:10.1006/jagm.1996.0063
    title: Mark H. Overmars and A. Frank van der Stappen, Range searching and point location among fat objects, Journal of Algorithms 21(3), 1996
    locator: pages 629 to 656 (cited by Gupta and McKeown for the point location bounds)
---

Packet classification is the per-packet lookup of firewalls, access control lists, quality-of-service markers and software switches. A *classifier* is an ordered list of $n$ rules. Each rule gives a range, a prefix or an exact value for each of $d$ header fields, for example the source and destination addresses, the two port numbers and the protocol. The task is to return the first rule in the list that matches the packet. With $d = 1$ and a destination prefix field, it is [longest prefix match](/longest-prefix-match/). Geometrically, each rule is a box in $d$-dimensional space and a packet is a point, so the task is a point location among boxes that can overlap. For $d \ge 3$ no known method gets both $O(\log n)$ time and close to linear space, so practical methods such as [HiCuts](/hicuts/) and [tuple space search](/tuple-space-search/) are heuristics that use the structure of real rule sets.

## In plain words

A security guard at a building has a list of rules. "People from company A may enter floor 3." "Nobody may enter the server room after 8 pm." "Anybody may enter the lobby." Each rule looks at a few facts about the visitor at the same time. The guard reads the list from the top and uses the first rule that fits.

A router or a firewall does the same for each packet. Each rule looks at several parts of the packet header: where the packet comes from, where it goes, which ports and which protocol. The router must find the first fitting rule among thousands of rules, in the short time before the next packet arrives. Reading the whole list is too slow, and each fast method uses much more memory. The hard part is to find a good balance between the two costs.

## Definition

**Fields.** A packet header gives $d$ fields $x_1, \ldots, x_d$, where field $i$ is a $W_i$-bit integer. The usual five fields are the source and destination IPv4 addresses ($W = 32$), the source and destination ports ($W = 16$) and the protocol ($W = 8$).

**Rules.** A rule $R$ is a product of closed ranges $[\mathit{lo}_1, \mathit{hi}_1] \times \cdots \times [\mathit{lo}_d, \mathit{hi}_d]$, plus an action such as "permit", "deny" or a queue number. In practice the address fields are prefixes (a prefix is the range of all addresses that start with given bits), the port fields are arbitrary ranges, and the protocol is one value or a wildcard. The rule *matches* the packet $x$ if $\mathit{lo}_i \le x_i \le \mathit{hi}_i$ for every field $i$.

**Input.** A classifier $R_1, R_2, \ldots, R_n$ in priority order and a packet $x$.

**Output.** The smallest $i$ such that $R_i$ matches $x$, or "no match". Most classifiers end with a default rule that matches every packet, so the answer always exists.

**Cost.** As for [longest prefix match](/longest-prefix-match/), the main cost is the number of memory accesses per packet, then the memory size, then the update time. The variables are $n$, $d$ and the field widths $W_i$.

**The geometric view.** The header space is a $d$-dimensional grid. Each rule is an axis-parallel box, and a packet is a point. The task is to find the box of highest priority that contains the point. For one field it is an [interval stabbing query](/interval-stabbing-query/) with priorities. For $d$ fields it is the [orthogonal point enclosure](/orthogonal-point-enclosure/) problem with priorities, and if the boxes do not overlap it is point location in a subdivision into boxes, the $d$-dimensional form of [planar point location](/planar-point-location/).

## Variants

- **First match or best match.** Most classifiers use the order of the list. Some give each rule a numeric priority; this is the same after a sort.
- **All matches.** Intrusion detection and accounting want every matching rule, not only the first.
- **Static or dynamic.** A firewall policy changes rarely and can be rebuilt. A software switch such as Open vSwitch gets new rules from a controller all the time, so it needs fast insert and delete.
- **Prefix fields only.** If every field is a prefix (a ternary pattern), the rule fits directly into a TCAM entry, and [tuple space search](/tuple-space-search/) applies without range expansion.
- **One field.** For $d = 1$ with prefixes and priority by length, the problem is [longest prefix match](/longest-prefix-match/).
- **Two fields.** Source and destination prefix pairs, which occur in multicast forwarding and in some VPNs, admit special methods such as the grid of tries.

## Examples

**A small classifier.** The fields are (source address, destination address, source port, destination port, protocol). A star is a wildcard.

| rule | source | destination | source port | destination port | protocol | action |
|---|---|---|---|---|---|---|
| R1 | 10.0.0.0/8 | 192.168.1.0/24 | * | 80 | TCP | permit |
| R2 | * | 192.168.1.0/24 | * | 0 to 1023 | * | deny |
| R3 | 10.1.0.0/16 | * | 1024 to 65535 | * | UDP | permit |
| R4 | * | * | * | * | * | deny |

| packet | matching rules | answer |
|---|---|---|
| 10.2.3.4 to 192.168.1.5, ports 5555 to 80, TCP | R1, R2, R4 | R1 |
| 10.1.2.3 to 192.168.1.5, ports 5555 to 53, UDP | R2, R3, R4 | R2 |
| 10.1.2.3 to 8.8.8.8, ports 5555 to 53, UDP | R3, R4 | R3 |
| 172.16.0.1 to 192.168.1.9, ports 40000 to 8080, TCP | R4 | R4 |

The second packet shows that the order matters: R2 and R3 both match, and R2 wins because it comes first. If the order of R2 and R3 were changed, the same packet would be permitted.

**Range expansion.** A TCAM or a prefix-based method stores only prefixes, so each port range must be cut into prefixes. Take the largest aligned block that starts at the left end of the range and does not pass its right end, and repeat. The range 0 to 1023 is one prefix (the first 6 bits are 0). The range 1024 to 65535 needs 6 prefixes: `000001*`, `00001*`, `0001*`, `001*`, `01*` and `1*`. So R3 becomes 6 TCAM entries, and the classifier above becomes 9 entries. The worst range of a $W$-bit field is $[1, 2^W - 2]$, which needs $2W - 2$ prefixes: 30 prefixes for a 16-bit port. A rule with two such port ranges becomes $30 \times 30 = 900$ entries.

*Why $2W - 2$.* Let $t$ be the highest bit where $\mathit{lo}$ and $\mathit{hi}$ differ. The range splits at $m = $ the value with the bits above $t$ of $\mathit{hi}$, bit $t$ set and zeros below. The left part $[\mathit{lo}, m - 1]$ ends at an aligned boundary, so the greedy takes at most one block for each of the $t$ low bits; the same holds for the right part $[m, \mathit{hi}]$, which starts at a boundary. So $2t \le 2(W-1)$ prefixes are enough. The greedy split uses the fewest prefixes. Two aligned blocks are nested or disjoint, so in any split of the range, the blocks that meet the first greedy block $G$ lie inside $G$ (a block that contains $G$ and is larger would start at the left end and be larger than $G$, which the greedy would have taken). Putting $G$ in their place does not add blocks, and induction on the rest of the range gives the claim.

## Known algorithms

**Linear search.** Test the rules in order and stop at the first match. It takes $O(nd)$ time and $O(n)$ space, updates are trivial, and it is the reference for all other methods.

```pseudo id=main
CLASSIFY-LINEAR(R[1 .. n], x)              ▷ R in priority order, x a packet
L1  for i ← 1 to n do
L2      if lo_j(R[i]) ≤ x_j ≤ hi_j(R[i]) for every field j then
L3          return i
L4  return no match
```

**TCAM.** A ternary content-addressable memory compares the packet with all entries in parallel and returns the first match in one cycle. Ranges must be expanded into prefixes as in the example, so a rule can take up to $(2W - 2)^2$ entries for two port ranges. TCAMs also use much power and chip area for each bit.

**Hierarchical and set-pruning tries.** Build a trie on the first field. Each node that holds a prefix of a rule points to a trie on the second field for the rules with that prefix, and so on. A lookup must try every matching prefix of each field, which costs $O(W^d)$ node reads. Set-pruning tries copy rules down so that a lookup follows one path in each trie, at the cost of $O(n^d)$ space. The grid of tries of Srinivasan, Varghese, Suri and Waldvogel (1998) uses precomputed switch pointers to get $O(W)$ time and $O(nW)$ space for two prefix fields.

**Crossproducting.** Project the rule ranges onto each field. On field $i$ the endpoints cut the axis into at most $2n + 1$ elementary intervals, and one [binary search](/binary-search/) finds the interval of $x_i$. A table indexed by the $d$ interval numbers stores the answer for each cell, so a lookup costs $d$ searches and one table read, but the table has up to $(2n+1)^d$ cells (Srinivasan et al., 1998).

**Bit vectors.** Lakshman and Stiliadis (1998) also project onto each field, but store with each elementary interval an $n$-bit vector of the rules that cover it. A lookup finds the $d$ intervals, takes the AND of the $d$ vectors, and returns the first 1 bit. It costs $O(d \log n + dn / w)$ time for a word of $w$ bits and $O(dn^2)$ bits of space. The vectors are [bit sets](/bit-set/), and the AND runs at memory speed in hardware.

**Recursive flow classification.** Gupta and McKeown (1999) cut the header into chunks of 8 or 16 bits. A first phase maps each chunk value to an equivalence class number. Later phases combine pairs of class numbers through tables, until one number names the rule. A lookup is a fixed number of table reads, but the tables can be large.

**Decision trees.** [HiCuts](/hicuts/) (Gupta and McKeown, 1999) cuts the space into equal pieces along one field at each node, until each leaf holds a few rules that are then searched linearly. HyperCuts (Singh, Baboescu, Varghese and Wang, 2003) cuts several fields at one node. Two parameters bound the leaf size and the space blow-up.

**Tuple space search.** [Tuple space search](/tuple-space-search/) (Srinivasan, Suri and Varghese, 1999) groups the prefix rules by their tuple of prefix lengths and keeps one hash table for each tuple. A lookup does one hash probe per tuple. The number of tuples is usually much smaller than $n$, and an update is one hash insert. Open vSwitch uses this method.

## Bounds

For $n$ boxes that do not overlap in $d \ge 2$ dimensions, the best known point location structures give either $O(\log n)$ time with $O(n^d)$ space, or $O(n)$ space with $O(\log^{d-1} n)$ time. Gupta and McKeown cite these as the two well known results, from Overmars and van der Stappen (1996), and many networking papers call them lower bounds. They are the best known upper bounds, not proven lower bounds. They do show why a general method that is fast in both time and space for large $d$ is not expected. For lower bounds in related models of range searching, see the [range searching lower bound](/range-searching-lower-bound/). Overlapping boxes with priorities can be cut into the $(2n+1)^d$ cells of the crossproduct, so the problem is no harder than point location among $O(n^d)$ boxes.

| method | memory accesses per packet | space | update |
|---|---|---|---|
| linear search | $O(n)$ | $O(n)$ | $O(1)$ |
| TCAM | 1 parallel search | $O(n W^2)$ entries with two range fields | can move many entries |
| hierarchical tries | $O(W^d)$ | $O(n d W)$ | $O(dW)$ |
| set-pruning tries | $O(dW)$ | $O(n^d d W)$ | rebuild |
| grid of tries, $d = 2$ | $O(W)$ | $O(nW)$ | rebuild |
| crossproducting | $O(d \log n)$ and 1 table read | $O((2n+1)^d)$ | rebuild |
| bit vectors | $O(d \log n + dn/w)$ | $O(d n^2)$ bits | rebuild |
| HiCuts | the tree depth plus a scan of at most $\mathit{binth}$ rules | $O(n^d)$ in the worst case | rebuild |
| tuple space search | one hash probe per tuple, up to $O(n)$ | $O(n)$ | $O(1)$ expected |

On real classifiers, which have few distinct prefix lengths and ranges and much structure, the heuristic methods do far better than their worst cases.

## Reductions

- **From longest prefix match.** A classifier with one destination prefix field, with the rules sorted by decreasing prefix length, is a forwarding table. So [longest prefix match](/longest-prefix-match/) is the case $d = 1$.
- **To orthogonal point enclosure.** Each rule is a box and each packet a point. Reporting all matching rules is [orthogonal point enclosure](/orthogonal-point-enclosure/), and the first match is the minimum index among the reported boxes.
- **Ranges to prefixes.** A range on a $W$-bit field is a union of at most $2W - 2$ disjoint prefixes. This turns any classifier into a prefix classifier, which TCAMs and [tuple space search](/tuple-space-search/) need, at a cost of up to $(2W-2)^k$ entries for a rule with $k$ range fields.
- **One field at a time.** Crossproducting and bit vectors solve $d$ independent one-dimensional problems (each an [interval stabbing query](/interval-stabbing-query/) or a longest prefix match) and then combine the answers. The combination step is where the space or the time grows with $n$.

## Applications

- **Firewalls and access control lists.** Permit or deny each packet by the five fields.
- **Quality of service.** Map packets to queues or to traffic classes for [packet scheduling](/packet-scheduling/) and [fair queueing](/fair-queueing/).
- **Software-defined networking.** OpenFlow switches match many header fields with priorities. Open vSwitch uses [tuple space search](/tuple-space-search/) with caches of recent flows.
- **Policy routing and VPNs.** Choose a route by source and destination, not by destination alone.
- **Accounting and intrusion detection.** Count or inspect the packets of chosen flows.

## References
