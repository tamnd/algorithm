---
tag: JKVDFZ
kind: algorithm
slug: spatial-cloaking
name: Spatial cloaking
aliases:
- location k-anonymity
area: security-and-privacy/data-anonymization
level: advanced
summary: Replaces a user's location by a region that holds at least k users before it goes to a location-based service, by quadtree subdivision.
model: word-ram
complexity:
  vars: {n: the number of users known to the anonymizer, h: the depth of the finest quadrant, k: the anonymity parameter}
  time: {worst: O(n h)}
  space: {extra: O(n)}
properties: {deterministic: true, randomized: false}
history:
  year: 2003
  people: [Marco Gruteser, Dirk Grunwald]
  note: Gruteser and Grunwald defined k-anonymous location information and gave the adaptive-interval cloaking algorithm, a quadtree descent run by a trusted anonymity server, at MobiSys 2003.
prereqs: [k-anonymity, quadtree]
see_also: [k-anonymity, quadtree, region-quadtree, geo-indistinguishability, local-differential-privacy, linkage-attack, hilbert-curve, private-information-retrieval]
sources:
  - paper: doi:10.1145/1066116.1189037
    title: "Marco Gruteser and Dirk Grunwald, Anonymous usage of location-based services through spatial and temporal cloaking, MobiSys 2003, pages 31-42"
    locator: Section 4.1 (restricted space identification, observation identification and location tracking), Section 5 (the trusted anonymity server), Section 5.1 (k-anonymous location information), Section 5.2 (Table 2, the adaptive-interval cloaking algorithm, and temporal cloaking), Sections 6 and 7 (k_min = 5 and the measured resolutions)
  - paper: doi:10.1109/tkde.2007.190662
    title: "Panos Kalnis, Gabriel Ghinita, Kyriakos Mouratidis and Dimitris Papadias, Preventing location-based identity inference in anonymous spatial queries, IEEE Transactions on Knowledge and Data Engineering 19(12), 2007, pages 1719-1733"
    locator: the reciprocity property as a sufficient condition for spatial k-anonymity, the attack on cloaking regions that do not have it, and the Nearest Neighbor Cloak and Hilbert Cloak algorithms
---

Spatial cloaking hides who sent a request to a location-based service. A trusted anonymity server sits between the users and the service. It knows the current position of every user. When a user asks a question such as "where is the nearest fuel station", the server replaces the exact position by a region that also holds at least $k - 1$ other users, removes the network address, and sends the region to the service. Gruteser and Grunwald (MobiSys 2003) called this **k-anonymous location information** and gave the adaptive-interval cloaking algorithm. It goes down a [quadtree](/quadtree/) from the whole area towards the user's quadrant and stops just before the quadrant would hold fewer than $k$ users. Dense areas get small regions and sparse areas get large ones. For $n$ users and a finest level $h$ the descent takes $O(n h)$ time in the word-RAM model, or $O(h)$ with a tree of counts. The value of $k$ is a policy choice. The guarantee holds against an attacker who sees only one region; Kalnis et al. (2007) showed that an attacker who knows the positions and the algorithm can sometimes still find the user.

## In plain words

A driver asks a map service for nearby hotels. The service does not need the exact spot to answer. A helper server that the driver trusts takes the request and swaps the exact spot for an area.

The helper starts with the whole map. It cuts the current area into four equal squares and keeps the square that holds the driver. It does this again and again. Before each cut it counts the people in the current square. When the square holds fewer than $k$ people, the helper stops and sends the previous square, which still held at least $k$.

The service then sees a square with at least $k$ people in it. From that square alone, it cannot tell which of them asked. In a city centre the square is small, so the answer stays useful. In the country the square must be large.

## The problem

The input is a snapshot of user positions $U$ in the square $A = [0, 2^h)^2$ with integer coordinates, the position $p \in U$ of the requester, and an integer $k \ge 1$. The quadrants of a square $[x, x + s) \times [y, y + s)$ are its four half-open squares of side $s/2$. A **cell** is $A$ or a quadrant of a cell; the cells of side 1 are at depth $h$.

The output is the smallest cell that holds $p$ and at least $k$ users of $U$, counting the requester, or NONE if $|U| < k$. Gruteser and Grunwald define a location as k-anonymous when it cannot be told apart from the location of at least $k - 1$ other subjects (Section 5.1); a cell with $k$ users meets this for one request. They also allow the region to carry a time interval, which gives temporal cloaking below.

## The algorithm

```pseudo id=main
CLOAK(p, U, k, h)                ▷ U holds the requester at p; all points lie in [0, 2^h)^2
L1  q ← [0, 2^h)^2, q_prev ← q, d ← 0
L2  V ← U
L3  if |V| < k then return NONE
L4  loop
L5      if |V| < k then return q_prev
L6      if d = h then return q
L7      q_prev ← q
L8      q ← the quadrant of q that holds p
L9      V ← the users of V that lie in q
L10     d ← d + 1
```

Line L1 starts at the whole area that the server covers, and line L2 takes all known users. Line L5 is step 4 of Table 2 in the paper: when the current cell holds fewer than $k$ users, the previous cell, which held at least $k$, is the answer. Lines L7 to L9 are steps 5 to 8: cut the cell into four, remember the old cell, keep the quadrant of $p$ and drop the users outside it. Table 2 does not have lines L3 and L6. Line L3 refuses a request that no region can cloak; without it, the first pass of the loop returns the whole area with fewer than $k$ users. Line L6 stops at cells of side 1, because $k$ users at the same point would make the loop run for ever.

## Example

The area is $[0, 8)^2$, so $h = 3$, and $k = 3$. Eight synthetic users stand at $u_1 = (1, 1)$, $u_2 = (3, 2)$, $u_3 = (2, 3)$, $u_4 = (0, 3)$, $u_5 = (5, 1)$, $u_6 = (6, 6)$, $u_7 = (7, 5)$ and $u_8 = (2, 6)$. User $u_1$ sends a request.

| pass | $d$ | $q$ | $V$ | $\lvert V \rvert$ | action |
|---|---|---|---|---|---|
| 1 | 0 | $[0, 8)^2$ | $u_1, \ldots, u_8$ | 8 | $8 \ge 3$: $q_{prev} \leftarrow [0, 8)^2$, $q \leftarrow [0, 4)^2$ |
| 2 | 1 | $[0, 4)^2$ | $u_1, u_2, u_3, u_4$ | 4 | $4 \ge 3$: $q_{prev} \leftarrow [0, 4)^2$, $q \leftarrow [0, 2)^2$ |
| 3 | 2 | $[0, 2)^2$ | $u_1$ | 1 | $1 < 3$: return $[0, 4)^2$ |

The service receives the square $[0, 4)^2$, which holds four users. For this snapshot, $u_2$, $u_3$ and $u_4$ also get $[0, 4)^2$, and $u_5$ to $u_8$ get the whole area $[0, 8)^2$, because each of their quadrants $[4, 8) \times [0, 4)$, $[4, 8)^2$ and $[0, 4) \times [4, 8)$ holds fewer than 3 users. Each region is sent by at least 3 users, so here an attacker who knows the positions still has at least 3 candidates. That is not always so; see Pitfalls.

## Correctness

The cells that hold $p$ form a chain $A = C_0 \supset C_1 \supset \cdots \supset C_h$, with $C_d$ of side $2^{h - d}$, and the number of users in $C_d$ does not grow with $d$. Before each test of line L5, $q = C_d$, $V$ is the set of users in $C_d$, and, if $d \ge 1$, $q_{prev} = C_{d-1}$ holds at least $k$ users. Line L8 keeps the quadrant that holds $p$, so $q$ stays in the chain, and line L9 keeps exactly the users of the new cell. So line L5 returns $C_{d-1}$ for the first $d$ with fewer than $k$ users, and line L6 returns $C_h$ if all the cells have at least $k$. In both cases the result is the deepest cell of the chain with at least $k$ users, which is the smallest cell that holds $p$ and $k$ users. Line L3 makes sure that line L5 never returns $q_{prev}$ at $d = 0$. The full proof is in proofs/correctness.md.

The privacy claim is weaker than it looks. For one request seen alone, the region holds at least $k$ users who could have sent it. The claim says nothing about an attacker who knows the positions of all users and the algorithm, about a series of requests from the same user, or about the anonymity server itself, which sees everything.

## Complexity

- Each pass of lines L5 to L10 scans $V$ once, and there are at most $h + 1$ passes, so a request takes $O(n h)$ time in the worst case, when the users are packed near $p$. If the number of users halves at each level, the total is $O(n)$.
- With a [region quadtree](/region-quadtree/) of the positions that stores the number of users in each node, lines L8 and L9 become one step down the tree and one read of a count, so a request takes $O(h)$ time. Keeping the counts up to date costs $O(h)$ per position update.
- The extra space is $O(n)$ for $V$, or $O(n h)$ for the tree in the worst case.

## Properties

- **Adaptive.** The region size follows the density of users, so the same $k$ gives small regions in dense areas and large ones in sparse areas.
- **Coarse steps.** The region area changes by a factor of 4 at each level, so the region often holds many more than $k$ users. In the paper's simulation with $k_{min} = 5$, the mean number of users in a region was about 10 (a measurement, Section 7).
- **Deterministic.** The region depends only on $p$, the snapshot and $k$.
- **Not reciprocal.** Different users in the same region may get different regions; this is the weak point of the method.

## Variants and improvements

- **Temporal cloaking.** Gruteser and Grunwald also give a version that fixes a spatial resolution, waits until $k_{min}$ different users have visited the chosen area, and returns the area with a time interval that ends at the current time and starts a random amount before the request (Section 5.2). It trades delay for spatial accuracy.
- **Reciprocal cloaking.** Kalnis et al. require that every user inside a region would get the same region. Then an attacker who knows the positions and the algorithm still has at least $k$ candidates. Their Hilbert Cloak orders the users along a [Hilbert curve](/hilbert-curve/), cuts the order into groups of $k$ users, and returns the bounding rectangle of the requester's group, so every member of a group gets the same region.
- **Personal $k$ and minimum area.** Later systems let each user choose $k$ and a minimum region size, since a region with $k$ users inside one building can still reveal the building.
- **Without a trusted server.** [Geo-indistinguishability](/geo-indistinguishability/) adds planar Laplace noise on the user's device and gives a [local differential privacy](/local-differential-privacy/) style guarantee that does not depend on where the other users are. [Private information retrieval](/private-information-retrieval/) hides the query from the service by cryptography.

## When to use it

Use spatial cloaking when a trusted party already knows all positions, such as a network operator, and the service only needs a coarse location, for example points of interest or local traffic. The paper's simulation gives an idea of the cost: with $k_{min} = 5$, the median region side was 30 and 65 metres in two areas with many expressways and 125 and 250 metres in two areas with mostly collector streets (a measurement, Section 7). Do not use it when the attacker can learn the positions of the other users, or when one user sends many requests along a route. Use a reciprocal variant in the first case and a local, noise-based method in the second.

## Pitfalls

- **Returning $q$ instead of $q_{prev}$ at line L5.** The current cell has just been found to hold fewer than $k$ users. Returning it reveals a region with as few as one user, the requester.
- **No depth limit at line L6.** If $k$ users stand at the same point, every quadrant that holds $p$ holds all of them, and the loop never stops. Real coordinates have a finite resolution; stop there.
- **No check at line L3.** Table 2 of the paper returns the previous quadrant when the count is too small, and on the first pass the previous quadrant is the whole area. If fewer than $k$ users are known in total, the result is a region with fewer than $k$ users. Refuse the request instead.
- **Choosing the quadrant by $p$ at line L8 lets the region identify $p$.** Take $A = [0, 4)^2$ with $h = 2$, $k = 3$, three users at $(0, 0)$, $(1, 0)$ and $(0, 1)$, and one user $u$ at $(3, 3)$. The three users each get $[0, 2)^2$. The user $u$ is alone in $[2, 4)^2$, so $u$ gets the whole area. The whole area holds four users, but only $u$ would ever send it. An attacker who knows the positions and the algorithm learns that $u$ sent the request. Kalnis et al. call the missing property reciprocity, and the code has a check for it.
- **Tracking across requests.** Each request is cloaked against a fresh snapshot at line L2. A user who sends requests while driving gives a series of regions; the intersection with a road map and with the next region can shrink the candidate set below $k$. The paper names location tracking as a threat (Section 4.1) but the algorithm does not stop it.
- **A region that is all one place.** A region with $k$ users inside one hospital tells the service that the requester is in the hospital. k-anonymity of identity is not privacy of location.

## Implementations

## History

Gruteser and Grunwald presented the anonymity server, k-anonymous location information and the adaptive-interval and temporal cloaking algorithms at MobiSys 2003, borrowing the idea of [k-anonymity](/k-anonymity/) from published tables. Their evaluation used simulated traffic on road maps of Denver. In 2007 Kalnis, Ghinita, Mouratidis and Papadias showed that the quadtree cloak can reveal the requester when the attacker knows the positions, and defined reciprocity. Later work moved towards methods that need no trusted server, such as [geo-indistinguishability](/geo-indistinguishability/).

## References
