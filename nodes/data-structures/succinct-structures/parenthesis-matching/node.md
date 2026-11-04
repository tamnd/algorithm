---
tag: E4C8Z8
kind: problem
slug: parenthesis-matching
name: Parenthesis matching
aliases:
- find close
- find open
- enclose query
area: data-structures/succinct-structures
level: advanced
summary: Given a balanced parenthesis sequence, find the matching bracket of a given position or the enclosing pair.
prereqs: [balanced-parentheses, rank-select-problem]
see_also: [balanced-parentheses-representation, range-min-max-tree, dfuds, dyck-word, range-minimum-query, ordinal-tree, succinct-data-structures, stack]
sources:
  - paper: doi:10.1109/SFCS.1989.63533
    title: Guy Jacobson, Space-efficient static trees and graphs, 30th Annual Symposium on Foundations of Computer Science (FOCS 1989), 549-554
    locator: the representation of trees by balanced parentheses and the matching of parentheses with pioneers, in O(lg n) bit probes
  - paper: doi:10.1137/S0097539799364092
    title: J. Ian Munro and Venkatesh Raman, Succinct representation of balanced parentheses and static trees, SIAM Journal on Computing 31(3), 2001, 762-776
    locator: findclose, findopen and enclose in O(1) time with 2n + o(n) bits
  - paper: doi:10.1016/j.tcs.2006.09.014
    title: Richard F. Geary, Naila Rahman, Rajeev Raman and Venkatesh Raman, A simple optimal representation for balanced parentheses, Theoretical Computer Science 368(3), 2006, 231-246
    locator: the two-level pioneer structure for findclose, findopen and enclose in O(1) time
  - paper: doi:10.1145/2601073
    title: Gonzalo Navarro and Kunihiko Sadakane, Fully functional static and dynamic succinct trees, ACM Transactions on Algorithms 10(3), Article 16, 2014
    locator: the reduction of the parenthesis queries to forward and backward searches for an excess, and the range min-max tree
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, A Practical Approach, Cambridge University Press, 2016
    locator: Chapter 7 (Parentheses), the definitions of excess, fwdsearch, bwdsearch, close, open and enclose
---

Parenthesis matching is the query problem of preprocessing a [balanced parenthesis](/balanced-parentheses/) sequence $P$ of length $2n$ so that, for any position, the matching parenthesis can be found fast (*findclose* and *findopen*), and so can the pair that most tightly encloses it (*enclose*). The [stack](/stack/) algorithm that checks whether a string is balanced also finds every match, in $O(n)$ time, but storing the answers takes $\Theta(n \lg n)$ bits. The succinct version asks for $O(1)$ time with the sequence itself plus $o(n)$ extra bits. Munro and Raman solved it in 2001. Matching is the core of the [BP](/balanced-parentheses-representation/) and [DFUDS](/dfuds/) tree encodings, where a node is a pair of parentheses and its subtree lies between them.

## In plain words

Take a string of brackets that is properly nested, like the ones in arithmetic. Point at an opening bracket and ask where its partner closes. Point at a closing bracket and ask where its partner opens. Or point at any bracket and ask for the nearest pair of brackets around it.

Walking along the string and counting up for each opening bracket and down for each closing one answers all three questions, but a walk can be long. Storing the answer for every bracket is fast but takes many times more memory than the brackets. The problem is to answer quickly while adding only a little memory to the string.

## Definition

**Input.** A balanced sequence $P[0..2n-1]$ over $\{(, )\}$: every prefix has at least as many `(` as `)`, and the whole has equally many.

**Excess.** Let $E(i)$ be the number of `(` minus the number of `)` in $P[0..i]$, and $E(-1) = 0$. Balance means $E(i) \ge 0$ for all $i$ and $E(2n-1) = 0$. On a [bit vector](/bit-vector/) with `(` as 1, $E(i) = 2\,\text{rank}_1(i+1) - (i + 1)$.

**Queries.**

- $\text{findclose}(i)$, for $P[i] = ($: the position of its matching `)`, which is $\min\{\, j > i : E(j) = E(i) - 1 \,\}$.
- $\text{findopen}(j)$, for $P[j] = )$: the position of its matching `(`, which is $\max\{\, i < j : E(i-1) = E(j) \,\}$.
- $\text{enclose}(i)$, for $P[i] = ($: the opening parenthesis of the tightest pair that strictly contains the pair at $i$, which is $\max\{\, k < i : P[k] = (,\ \text{findclose}(k) > i \,\}$, or none if $E(i) = 1$.

**Cost.** A solution is measured by the extra space, beyond the $2n$ bits of $P$, and the time per query on the [word RAM](/word-ram/) with words of $\Theta(\lg n)$ bits.

## Variants

- **Forward and backward search.** $\text{fwdsearch}(i, d)$ is the least $j > i$ with $E(j) = E(i) + d$, and $\text{bwdsearch}(i, d)$ the greatest $j < i$ with $E(j) = E(i) + d$. Then $\text{findclose}(i) = \text{fwdsearch}(i, -1)$, $\text{findopen}(j) = \text{bwdsearch}(j, 0) + 1$ and $\text{enclose}(i) = \text{bwdsearch}(i, -2) + 1$. Navarro and Sadakane reduce all tree operations to these two searches and to range minima of $E$.
- **Range minimum and maximum of the excess.** $\text{rmq}(i, j)$, the position of the minimum of $E$ in $[i, j]$, gives the [lowest common ancestor](/lowest-common-ancestor/) in a BP tree.
- **Several bracket types.** With $k$ kinds of brackets, matching is the same problem on the shape, and the kinds are stored apart.
- **Dynamic.** Insert or delete a matching pair, as for a dynamic tree; the [range min-max tree](/range-min-max-tree/) over a [dynamic bit vector](/dynamic-bit-vector/) does all queries and updates in $O(\lg n)$ time.
- **Recognition.** Deciding whether a string is balanced at all is the separate [balanced parentheses](/balanced-parentheses/) problem.

## Examples

The tree $A(B(E, F), C, D(G(H)))$ of the [ordinal tree](/ordinal-tree/) page has the BP sequence below. The nodes in preorder open at positions 0 ($A$), 1 ($B$), 2 ($E$), 4 ($F$), 7 ($C$), 9 ($D$), 10 ($G$) and 11 ($H$).

| $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $P[i]$ | ( | ( | ( | ) | ( | ) | ) | ( | ) | ( | ( | ( | ) | ) | ) | ) |
| $E(i)$ | 1 | 2 | 3 | 2 | 3 | 2 | 1 | 2 | 1 | 2 | 3 | 4 | 3 | 2 | 1 | 0 |

- $\text{findclose}(1) = 6$: after position 1, with $E(1) = 2$, the first excess equal to 1 is at 6. The subtree of $B$ is $P[1..6]$, of $6/2 = 3$ nodes.
- $\text{findclose}(9) = 14$, so $D$ has $(14 - 9 + 1)/2 = 3$ nodes in its subtree.
- $\text{findopen}(12) = 11$: $E(12) = 3$, and the greatest $i < 12$ with $E(i - 1) = 3$ is $i = 11$, since $E(10) = 3$.
- $\text{findopen}(15) = 0$, the root.
- $\text{enclose}(4) = 1$: the pair of $F$ lies inside the pair of $B$, its parent. $\text{enclose}(11) = 10$: the parent of $H$ is $G$.
- $\text{enclose}(0)$ is none, since $E(0) = 1$.

## Known algorithms

| method | extra space (bits) | time per query |
|---|---|---|
| left-to-right or right-to-left scan of $P$ | $0$ | $O(n)$ |
| [stack](/stack/) pass, then a table of all matches | $2n \lceil \lg 2n \rceil$ | $O(1)$ |
| scan by bytes with tables of in-block excess | $O(1)$ tables | $O(n / \lg n)$ |
| Jacobson 1989, pioneers | $O(n \lg \lg n / \lg n)$ | $O(\lg n)$ bit probes |
| Munro and Raman 2001 | $o(n)$ | $O(1)$ |
| Geary, Rahman, Raman and Raman 2006 | $O(n \lg \lg n / \lg n)$ | $O(1)$ |
| Navarro and Sadakane 2014, [range min-max tree](/range-min-max-tree/) | $O(n / \text{polylog}\, n)$ | $O(1)$ |
| range min-max tree, practical form | $O(n / b)$ for blocks of $b$ bits | $O(\lg n)$ |

**Pioneers.** Cut $P$ into blocks of $b = \Theta(\lg n)$ bits. A parenthesis is *far* if its match is in another block. Among the far `(` of a block, the first whose match lies in a given other block is a *pioneer*. Jacobson observed that there are $O(n / b)$ pioneers, since the pioneer pairs form an outerplanar graph on the blocks, and that the match of any far parenthesis can be found from the match of the pioneer before it plus an in-block excess search. Munro and Raman, and then Geary et al., store the pioneers as a smaller balanced sequence, solve it recursively or by table, and answer in-block searches with a [Four Russians](/four-russians-method/) table over blocks of $\frac12 \lg n$ bits.

**Excess searches.** The range min-max tree stores, for each block and for each node of a tree over blocks, the minimum and maximum of $E$ inside. A fwdsearch for excess $E(i) + d$ climbs until a node's range of excess values contains the target, then descends. Since $E$ changes by $\pm 1$ at each step, a range whose minimum is at most the target and that starts above it must contain the target.

## Bounds

- **Space.** $P$ has $2n$ bits, and balanced sequences of length $2n$ are counted by the [Catalan number](/catalan-numbers/) $C_n$, so any encoding uses at least $\lg C_n = 2n - \frac32 \lg n + O(1)$ bits for some input. Structures that store $P$ in plain form and add $o(n)$ bits are therefore succinct.
- **Time.** $O(1)$ time is reachable with $o(n)$ extra bits, and Navarro and Sadakane bring the extra space down to $O(n / \text{polylog}\, n)$ for any fixed polylog.
- **Redundancy.** Lower bounds on the redundancy of matching that are sharper than the counting bound are not covered here. Since excess is computed by rank, the cell-probe trade-offs for rank discussed in [Pătraşcu's lower bounds](/patrascu-succinct-lower-bound/) bound the natural approach of computing $E(i)$ explicitly, not the matching problem itself.

## Reductions

- **To excess search.** findclose, findopen and enclose are single fwdsearch or bwdsearch calls, as in the Variants. So are the tree operations parent (enclose), subtree size (findclose), next sibling (findclose plus one) and level ancestor (bwdsearch with $d = -k - 1$).
- **To range minimum.** $\text{findclose}(i)$ is the least $j > i$ at which $E$ drops below $E(i)$, and the [lowest common ancestor](/lowest-common-ancestor/) of two nodes is found from the position of the minimum of $E$ between them. Conversely, the [range minimum query](/range-minimum-query/) problem on an array is solved in $2n + o(n)$ bits by storing the parentheses of its [Cartesian tree](/cartesian-tree/) and answering with these queries.
- **From the tree.** Every [ordinal tree](/ordinal-tree/) query that depends on the depth-first shape, such as depth, subtree size and ancestor tests, reduces to matching and excess on its BP or DFUDS sequence.

## Applications

- The [BP](/balanced-parentheses-representation/) and [DFUDS](/dfuds/) tree encodings, where every navigation step is one or two matching queries.
- [Compressed suffix trees](/compressed-suffix-tree/), which store the tree topology as parentheses.
- Succinct range minimum queries in $2n + o(n)$ bits.
- XML and JSON indexing, where the nesting of tags or brackets is the tree.
- Succinct representations of [planar and other graphs](/succinct-graph-representation/), which Jacobson built from several parenthesis sequences.

## References
