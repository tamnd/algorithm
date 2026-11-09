---
tag: 7HB39B
kind: problem
slug: reverse-nearest-neighbor
name: Reverse nearest neighbor search
aliases:
- RNN query
- reverse nearest neighbour query
- influence set query
area: geometry/proximity
level: research
summary: Find all points that have the query point as their nearest neighbor.
prereqs: [nearest-neighbor-search, all-nearest-neighbors, euclidean-distance]
see_also: [reverse-nearest-neighbor-search, nearest-neighbor-graph, all-nearest-neighbors, voronoi-diagram, kd-tree-nearest-neighbor-search, yao-graph, bichromatic-closest-pair, spatial-index]
sources:
  - paper: "Flip Korn and S. Muthukrishnan, Influence sets based on reverse nearest neighbor queries, Proceedings of the ACM SIGMOD International Conference on Management of Data, 2000, 201-212"
    locator: the definition of reverse nearest neighbour queries, monochromatic and bichromatic, and the method of nearest-neighbour circles
  - paper: "Ioana Stanoi, Divyakant Agrawal and Amr El Abbadi, Reverse nearest neighbor queries for dynamic databases, ACM SIGMOD Workshop on Research Issues in Data Mining and Knowledge Discovery, 2000, 44-53"
    locator: the six 60-degree regions around the query, with at most one candidate in each
  - paper: "Yufei Tao, Dimitris Papadias and Xiang Lian, Reverse kNN search in arbitrary dimensionality, Proceedings of the 30th International Conference on Very Large Data Bases, 2004, 744-755"
    locator: reverse k nearest neighbour queries with R-trees by pruning with perpendicular bisectors
  - paper: "Anil Maheshwari, Jan Vahrenhold and Norbert Zeh, On reverse nearest neighbor queries, Proceedings of the 14th Canadian Conference on Computational Geometry, 2002, 128-132"
    locator: linear-space structures with logarithmic query time in the plane, based on the bounded depth of the nearest-neighbour disks
---

A reverse nearest neighbor (RNN) query asks, for a set $P$ of points and a query point $q$, which points of $P$ would have $q$ as their nearest neighbour. Where an ordinary [nearest neighbor search](/nearest-neighbor-search/) asks "what is closest to me", the reverse query asks "for whom am I the closest", which measures the influence of $q$. Korn and Muthukrishnan (2000) introduced the query for databases. The answer is not symmetric to the ordinary one: the nearest neighbour of $q$ need not have $q$ as its own nearest neighbour, and the answer can be empty. In the plane it has at most six points, and Stanoi, Agrawal and El Abbadi (2000) used this to find it with six constrained nearest neighbour queries and six checks.

## In plain words

Suppose you plan to open a new shop. Ordinary nearest neighbour search tells you which existing shop is closest to your site. The reverse question is more useful for you: which customers would find your new shop to be their closest one? Those are the customers you would win.

A customer is won when your site is at least as close to them as every other place they could go. Each customer has a personal circle reaching to their current closest option, and you win exactly the customers whose circles contain your site.

In the plane, among points of one kind, a site can win at most six, because two winners always sit in different directions as seen from the site.

## Definition

**Input.** A set $P$ of $n$ distinct points in $\mathbb{R}^d$, preprocessed in advance, and a query point $q \notin P$.

**Output.** The set
$$\text{RNN}(q) = \{p \in P : \|p - q\| \le \|p - x\| \text{ for all } x \in P \setminus \{p\}\},$$
the points that have $q$ as a nearest neighbour once $q$ is added. With $\text{nnd}(p) = \min_{x \in P \setminus \{p\}} \|p - x\|$, this says $\|p - q\|^2 \le \text{nnd}(p)^2$, an exact comparison of squared distances for integer input.

**Ties.** The definition above counts $p$ when $q$ ties with its nearest neighbour. Some papers require $q$ to be strictly closer; the two answers differ exactly on the ties, and an implementation must state its choice.

**Bichromatic version.** Given sites $S$ and clients $C$, $\text{RNN}(s)$ for a site $s$ is the set of clients whose nearest site is $s$: the clients inside the [Voronoi](/voronoi-diagram/) cell of $s$. For a new site $q$, it is the set of clients $c$ with $\|c - q\| \le \min_{s \in S} \|c - s\|$. In this version the answer can contain any number of clients.

## Variants

- **Reverse k nearest neighbours.** The points that have $q$ among their $k$ nearest neighbours; studied with R-trees by Tao, Papadias and Lian (2004), in any dimension.
- **Monochromatic and bichromatic.** One set of points, or sites and clients as above.
- **Query point in the set.** For $q \in P$, $\text{RNN}(q)$ is the set of in-neighbours of $q$ in the [nearest neighbor graph](/nearest-neighbor-graph/), which can be read off after computing [all nearest neighbors](/all-nearest-neighbors/).
- **Dynamic and continuous queries.** Points are inserted and deleted, or move, and the answer is maintained.
- **High dimension and metric spaces.** Pruning by angles fails; methods use bisector pruning or metric indexes. See [reverse nearest neighbor search](/reverse-nearest-neighbor-search/) for the database and similarity-search side.

## Examples

For $P = \{(1,3), (1,11), (2,8), (5,1), (9,6), (11,1), (11,4)\}$ and $q = (7,4)$, compare each point's squared distance to $q$ with its squared nearest neighbour distance:

| point $p$ | $\|p - q\|^2$ | $\text{nnd}(p)^2$ | in $\text{RNN}(q)$ |
| --- | --- | --- | --- |
| $(1,3)$ | 37 | 20 | no |
| $(1,11)$ | 85 | 10 | no |
| $(2,8)$ | 41 | 10 | no |
| $(5,1)$ | 13 | 20 | yes |
| $(9,6)$ | 8 | 8 | yes, a tie with $(11,4)$ |
| $(11,1)$ | 25 | 9 | no |
| $(11,4)$ | 16 | 8 | no |

So $\text{RNN}(q) = \{(5,1), (9,6)\}$, and with the strict rule only $\{(5,1)\}$. The point $(11,4)$ is at squared distance 16 from $q$ but only 8 from $(9,6)$, so it does not choose $q$: being fairly close to $q$ is not enough. Conversely $(5,1)$ is only the second closest point to $q$, yet it chooses $q$.

**Six is reachable.** For $q$ at the center of a regular hexagon whose side equals its radius, all six corners tie between $q$ and their two neighbours on the hexagon, so all six are in $\text{RNN}(q)$.

## Known algorithms

| method | preprocessing | query | idea |
| --- | --- | --- | --- |
| brute force | none | $O(n^2)$ | compute $\text{nnd}(p)$ for each $p$ during the query |
| precomputed nearest neighbour distances | $O(n \log n)$ for fixed $d$ | $O(n)$ | test $\|p - q\|^2 \le \text{nnd}(p)^2$ for every $p$ |
| nearest neighbour circles (Korn and Muthukrishnan, 2000) | all nearest neighbours, then a spatial index on the disks | point enclosure query | $\text{RNN}(q)$ is the set of disks $D(p, \text{nnd}(p))$ that contain $q$ |
| six cones (Stanoi, Agrawal and El Abbadi, 2000) | any nearest neighbour index | 6 constrained nearest neighbour queries and 6 checks | at most one candidate per $60°$ cone, no precomputed distances, so it handles updates |
| bisector pruning (Tao, Papadias and Lian, 2004) | R-tree | output-sensitive in practice | prune regions cut off by bisectors of candidates; works for $k > 1$ and any $d$ |
| point location in the disk arrangement (Maheshwari, Vahrenhold and Zeh, 2002) | $O(n \log n)$ | $O(\log n)$ | in the plane the disks cover each point at most six times, so their arrangement has linear size |

**Why one candidate per cone.** Split the plane around $q$ into six half-open cones of angle $60°$. Let $a$ be a point of a cone nearest to $q$ and $b \ne a$ another point of the same cone, so $\|q - a\| \le \|q - b\|$ and the angle $\theta = \angle aqb$ is less than $60°$, hence $\cos \theta > 1/2$. By the law of cosines,
$$\|a - b\|^2 = \|q - a\|^2 + \|q - b\|^2 - 2\|q - a\| \|q - b\| \cos\theta < \|q - b\|^2 + \|q - a\| (\|q - a\| - \|q - b\|) \le \|q - b\|^2.$$
So $a$ is strictly closer to $b$ than $q$ is, and $b \notin \text{RNN}(q)$. Each cone contributes at most its nearest point, which is then checked with one nearest neighbour query.

## Bounds

- **Output size.** In the plane, $|\text{RNN}(q)| \le 6$ in the monochromatic version, by the cone argument; the hexagon shows that 6 is reached. In $\mathbb{R}^d$ the bound is the largest number of points around $q$ with pairwise angles at least $60°$, a kissing-number constant (12 in three dimensions).
- **Query time.** In the plane, $O(\log n)$ query time with $O(n)$ space is possible, matching ordinary nearest neighbour search.
- **Bichromatic.** The answer can have size $\Theta(|C|)$, so the query time is output-sensitive: reporting the clients inside a region, plus the size of the answer.
- **High dimension.** RNN queries inherit the difficulty of exact nearest neighbour search, and the candidate bound grows exponentially with $d$.

## Reductions

- **It reduces to point enclosure.** Precompute $\text{nnd}(p)$ for every $p$, then report the disks $D(p, \text{nnd}(p))$ that contain $q$.
- **It reduces to a constant number of nearest neighbour queries in the plane.** Six constrained queries find the candidates and six ordinary queries check them.
- **Bichromatic RNN of a site is Voronoi cell reporting.** Report the clients inside the Voronoi cell of $s$ among the sites, a range reporting query with a convex polygon.
- **All reverse nearest neighbours.** For $q \in P$, all answers together are the in-neighbour lists of the [nearest neighbor graph](/nearest-neighbor-graph/).

## Applications

- **Facility location and marketing.** Which customers would a new store or service attract; how many users does a server or base station attract.
- **Influence and decision support.** The size of $\text{RNN}(q)$ measures how many objects "depend" on $q$, as in the influence sets of Korn and Muthukrishnan.
- **Clustering and outlier detection.** A point that is the nearest neighbour of nobody is isolated in a sense the ordinary nearest neighbour distance does not capture; counts of reverse neighbours are used as a density measure.
- **Networks and sensors.** Which sensors or devices treat a node as their closest relay, for load estimates.

## References
