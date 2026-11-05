---
tag: CRYSES
kind: concept
slug: six-degrees-of-separation
name: Six degrees of separation
aliases:
- small-world phenomenon
area: graphs/network-analysis
level: intro
summary: Empirical observation that most pairs of people are connected by short chains.
prereqs: [graph, shortest-path, breadth-first-search]
see_also: [small-world-network, watts-strogatz-model, kleinberg-small-world-model, effective-diameter, network-diameter-estimation, neighborhood-function, erdos-renyi-model, weak-ties]
sources:
  - paper: doi:10.2307/2786545
    title: Jeffrey Travers and Stanley Milgram, An experimental study of the small world problem, Sociometry 32(4), 425 to 443 (1969)
    locator: the whole paper (the letter-chain experiment with starters in Nebraska and Boston and one target in Massachusetts, and the lengths of the completed chains)
  - paper: doi:10.1126/science.1081058
    title: Peter Sheridan Dodds, Roby Muhamad and Duncan J. Watts, An experimental study of search in global social networks, Science 301(5634), 827 to 829 (2003)
    locator: the whole paper (the e-mail version of the experiment, the attrition of chains and the corrected estimate of the chain length)
  - paper: doi:10.1145/2380718.2380723
    title: Lars Backstrom, Paolo Boldi, Marco Rosa, Johan Ugander and Sebastiano Vigna, Four degrees of separation, Proceedings of the 4th ACM Web Science Conference (2012)
    locator: the whole paper (the distance distribution of the Facebook graph of 2011, computed with HyperANF)
  - book: isbn:9780521195331
    title: David Easley and Jon Kleinberg, Networks, Crowds, and Markets, Cambridge University Press, 2010
    locator: Chapter 20, The small-world phenomenon
  - paper: doi:10.1038/35022643
    title: Jon M. Kleinberg, Navigation in a small world, Nature 406, 845 (2000)
    locator: the whole paper (short chains exist and can be found with local information only when the long links follow an inverse-square law)
---

Six degrees of separation is the observation that two people chosen at random are usually linked by a short chain of acquaintances, of about six steps. In graph terms, the [shortest-path](/shortest-path/) distance between two vertices of a large social network is small, close to the logarithm of the number of people. The idea comes from the letter-chain experiments of Milgram in the 1960s, and large computations on online networks in the 2010s confirmed it with even shorter chains.

## In plain words

Pick a stranger far away. You probably know someone, who knows someone, who knows them, and the chain needs only a handful of people. This feels surprising, because each person knows only a few hundred others.

The reason is growth. If each person knows a hundred others, then two steps reach about ten thousand people, three steps a million, and five steps more than the whole world. Friends of friends overlap a lot, so the real growth is slower, but a few links that jump between distant groups are enough to keep the chains short.

A second surprise is that people can find such chains. They pass a message to a friend who seems closer to the target, with no map of the whole network, and the message often arrives.

## The idea

**The quantity.** Model the people as the vertices of an undirected [graph](/graph/) without weights, with an edge for each pair that know each other. The distance $d(u, v)$ is the number of edges of a shortest path, found by [breadth-first search](/breadth-first-search/). The claim is about the distribution of $d(u, v)$ over pairs: its mean, or its median, or the [effective diameter](/effective-diameter/) (the 90th percentile), is small. It is not a claim about the diameter, the largest distance, which a single long path in the graph can make large.

**Disconnected graphs.** Real networks are not connected, and $d(u, v) = \infty$ for pairs in different components. The usual convention is to compute the statistics over the pairs that are connected, which in a social network are almost all pairs inside the [giant component](/giant-component/). The fraction of pairs left out must be reported with the result. The [harmonic mean](/harmonic-centrality/) of the distances is an alternative that counts the pairs at distance $\infty$ as $1/\infty = 0$.

**Why the distances are short.** Suppose that each vertex has $k$ neighbours and that the neighbourhoods do not overlap. Then the number of vertices at distance at most $\ell$ grows like $k^\ell$, and it reaches $n$ when

$$\ell \approx \frac{\ln n}{\ln k}.$$

In the [Erdős-Rényi model](/erdos-renyi-model/) $G(n, p)$ with a fixed mean degree $c = np > 1$, the typical distance in the giant component is indeed $(1 + o(1)) \ln n / \ln c$. Social networks have high [clustering](/clustering-coefficient/), so the neighbourhoods overlap, and the growth argument fails for them. The [Watts-Strogatz model](/watts-strogatz-model/) shows that a small fraction of random long links restores short distances while the clustering stays high. A graph with both properties is a [small-world network](/small-world-network/).

**Short chains that people can find.** Milgram's chains were found by people who forwarded a letter to one acquaintance at a time. Kleinberg (2000) showed that this is a separate property. In a two-dimensional grid with one extra long link per vertex, where the long link from $u$ goes to $v$ with probability proportional to $d(u, v)^{-r}$, greedy forwarding finds paths of length $O(\log^2 n)$ in expectation exactly when $r = 2$. For every other $r \ge 0$ each local algorithm needs a number of steps polynomial in $n$, even though short paths exist when $r$ is small. The page on the [Kleinberg model](/kleinberg-small-world-model/) gives the details.

## Examples

**The growth estimate.** With $n = 8 \times 10^9$ people who each know $k = 100$ others, $\ln n / \ln k = \ln(8 \times 10^9) / \ln 100 \approx 4.95$. Five steps would reach $100^5 = 10^{10}$ people if no one were counted twice.

**Milgram's experiment.** Travers and Milgram (1969) asked starting people in Nebraska and in Boston to forward a folder toward one stockbroker in Massachusetts, each time to a person known on a first-name basis. Of 296 starting people, 64 chains reached the target, and the completed chains had a mean of 5.2 intermediaries. Most chains did not finish, and a long chain is more likely to break, so the completed chains underestimate the typical length.

**The e-mail experiment.** Dodds, Muhamad and Watts (2003) repeated the test with e-mail, with more than 24,000 starting people and 18 targets in 13 countries. Only 384 chains were completed. After a correction for the chains that stopped, they estimated a median length of 5 to 7 steps.

**Facebook in 2011.** Backstrom, Boldi, Rosa, Ugander and Vigna computed the [neighborhood function](/neighborhood-function/) of the whole Facebook graph, with about 721 million active users, using the [ANF](/anf-algorithm/) method HyperANF. The mean distance between connected pairs was 4.74, that is, about 3.74 intermediaries. An exact all-pairs computation was out of reach, which is why an estimate of the [diameter](/network-diameter-estimation/) and of the distance distribution by sketches was needed.

**A counterexample.** A cycle of $n$ vertices has mean distance about $n/4$. A ring of people who each know only their two neighbours has no small-world property, however many people there are. Its distances become short only after long links are added, as in the Watts-Strogatz model.

## Where it is used

- [Small-world network](/small-world-network/) and [Watts-Strogatz model](/watts-strogatz-model/): the formal versions of the observation.
- [Kleinberg small-world model](/kleinberg-small-world-model/): the theory of why short chains can be found with local information.
- [Effective diameter](/effective-diameter/), [neighborhood function](/neighborhood-function/) and [network diameter estimation](/network-diameter-estimation/): the measurements that test the claim on large graphs.
- [Weak ties](/weak-ties/): the links between groups that make the chains short.
- Peer-to-peer and overlay networks: designs such as greedy routing in a ring with long links use the same idea.

## References
