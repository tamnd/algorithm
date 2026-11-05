---
tag: 4704V3
kind: concept
slug: homophily
name: Homophily
aliases:
- assortative mixing by attribute
area: graphs/network-analysis
level: core
summary: Tendency of similar nodes to form links.
prereqs: [graph, edge, assortativity]
see_also: [assortativity, triadic-closure, community-detection, link-prediction, stochastic-block-model, independent-cascade-model, structural-equivalence]
sources:
  - paper: doi:10.1146/annurev.soc.27.1.415
    title: Miller McPherson, Lynn Smith-Lovin and James M. Cook, Birds of a feather, homophily in social networks, Annual Review of Sociology 27, 415 to 444 (2001)
    locator: the whole review (status and value homophily, baseline and inbreeding homophily, and the evidence by attribute)
  - book: isbn:9780521195331
    title: David Easley and Jon Kleinberg, Networks, Crowds, and Markets, Reasoning about a Highly Connected World, Cambridge University Press, 2010
    locator: Chapter 4, Networks in their surrounding contexts (the homophily test with cross-edges, and selection and social influence)
  - paper: doi:10.1103/PhysRevE.67.026126
    title: M. E. J. Newman, Mixing patterns in networks, Physical Review E 67, 026126 (2003)
    locator: the assortativity coefficient r for vertices of discrete types, from the matrix e of edge fractions
  - paper: doi:10.1177/0049124111404820
    title: Cosma Rohilla Shalizi and Andrew C. Thomas, Homophily and contagion are generically confounded in observational social network studies, Sociological Methods and Research 40(2), 211 to 239 (2011)
    locator: the whole paper (why selection and influence cannot in general be told apart from observational data)
---

Homophily is the tendency of [vertices](/vertex/) that are similar in some attribute, such as age, language, opinion or the topic of a web page, to be joined by [edges](/edge/) more often than chance would give. It is measured by comparing the number of edges between similar vertices with the number that a random placement of the same edges would give, for example by the [assortativity](/assortativity/) coefficient. It is one of the most robust patterns of social networks, and it shapes [communities](/community-detection/), the spread of information and the accuracy of [link prediction](/link-prediction/).

## In plain words

Most of your friends are probably about your age, speak your language and live near you. This is not only because you choose them. You also meet them at school, at work and in your street, where people are already similar to you.

Homophily is the name for this pattern in a network: similar people are linked more often than they would be by chance. To test for it, you count how many links join people of different kinds. Then you compare this count with what you would expect if the links were placed with no regard to kind. Far fewer mixed links than expected means homophily. Far more than expected is the opposite pattern, called heterophily.

## The idea

**The setting.** Let $G = (V, E)$ be a graph with $m$ edges, and let each vertex $v$ have a type $t(v)$ from a finite set. Homophily is a statement about the edges compared with a baseline, not about the graph alone.

**The cross-edge test.** Let $p_i$ be the fraction of the vertices of type $i$. If the types were given to the vertices at random with these fractions, independently of the edges, an edge would join two different types with probability $1 - \sum_i p_i^2$, which is $2pq$ for two types with fractions $p$ and $q$. Easley and Kleinberg call the network homophilous when the observed fraction of cross-type edges is clearly less than this value. For a small graph, the exact baseline with $n_i$ vertices of type $i$ is $1 - \sum_i \binom{n_i}{2} / \binom{n}{2}$, the chance that a uniform pair of distinct vertices has two types.

**The assortativity coefficient.** Newman's coefficient uses the ends of the edges. Let $e_{ij}$ be the fraction of edge ends that join a vertex of type $i$ to a vertex of type $j$, counting each undirected edge once in each direction, so that $\sum_{i,j} e_{ij} = 1$ and $e_{ij} = e_{ji}$. Let $a_i = \sum_j e_{ij}$ be the fraction of edge ends at vertices of type $i$. Then

$$r = \frac{\sum_i e_{ii} - \sum_i a_i^2}{1 - \sum_i a_i^2}.$$

The value $r = 1$ means that every edge joins two vertices of one type, $r = 0$ means no more same-type edges than the baseline $\sum_i a_i^2$, and $r < 0$ means heterophily. The minimum is $-\sum_i a_i^2 / (1 - \sum_i a_i^2)$, which is $-1$ for two types with equal shares. The baseline here weights each type by its share of the edge ends, not of the vertices, so the two tests can disagree when the types have different mean degrees. For a numeric attribute, such as age, $r$ becomes the Pearson correlation of the values at the two ends of an edge; with the degree as the attribute, it is the degree [assortativity](/assortativity/).

**Directed, weighted and disconnected graphs.** For a [directed graph](/directed-graph/), $e_{ij}$ is the fraction of arcs from type $i$ to type $j$, the matrix need not be symmetric, and $a_i$ and $b_j$ are its row and column sums; the formula uses $\sum_i a_i b_i$ in place of $\sum_i a_i^2$. For a [weighted graph](/weighted-graph/), each edge counts with its weight. Disconnected graphs need no special care: the measures count edges, wherever they are. A graph with no edges has no value.

**Two kinds of homophily.** McPherson, Smith-Lovin and Cook separate *baseline* homophily, which comes from the make-up of the population and of the places where people meet, from *inbreeding* homophily, which is the excess beyond that. They also separate *status* homophily (age, education, ethnicity, sex) from *value* homophily (attitudes and beliefs).

**Selection and influence.** Similar people can be linked because similar people choose each other, called *selection*, or because linked people become similar over time, called *social influence*. Both give the same snapshot. Shalizi and Thomas show that, from observational data alone, the two cannot in general be separated, because a hidden trait can drive both the links and the behaviour. Data over time, or experiments, are needed.

## Examples

**A worked test.** Take the vertices 0 to 7, with 0 to 3 red and 4 to 7 blue, and the 10 edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{2,3\}$, $\{4,5\}$, $\{5,6\}$, $\{6,7\}$, $\{4,6\}$, $\{3,4\}$ and $\{0,7\}$.

- Two edges, $\{3,4\}$ and $\{0,7\}$, join different colours, so the observed cross fraction is $2/10 = 0.2$.
- The baseline with $p = q = \tfrac12$ is $2pq = 0.5$. The exact baseline for 4 and 4 vertices is $1 - 2\binom{4}{2}/\binom{8}{2} = 1 - 12/28 = 4/7 \approx 0.571$.
- For the coefficient, $e_{RR} = e_{BB} = 0.4$ and $e_{RB} = e_{BR} = 0.1$, so $a_R = a_B = 0.5$ and $r = (0.8 - 0.5)/(1 - 0.5) = 0.6$.

Both measures show strong homophily.

**Heterophily.** In a cycle of length 4 whose vertices alternate between two colours, every edge joins two colours, so $e_{RR} = e_{BB} = 0$, $a_R = a_B = \tfrac12$ and $r = (0 - \tfrac12)/(1 - \tfrac12) = -1$. Graphs of heterosexual partnerships and of buyers and sellers are close to this case: they are close to [bipartite](/bipartite-graph/).

**Evidence.** The review of McPherson, Smith-Lovin and Cook collects studies in which race and ethnicity, age, religion, education and sex each show homophily in friendship, marriage, work and discussion networks, with race and ethnicity giving the strongest divides in the United States.

## Where it is used

- [Link prediction](/link-prediction/): a shared attribute is a strong feature for predicting a new edge, and [triadic closure](/triadic-closure/) adds to it, since friends of friends are often similar.
- [Community detection](/community-detection/) and the [stochastic block model](/stochastic-block-model/): a model with more edges inside groups than between them is a model of homophily; [modularity](/modularity/) is the same formula as $r$ with the groups as types.
- Spreading processes: in the [independent cascade model](/independent-cascade-model/) and the [linear threshold model](/linear-threshold-model/), homophily makes an idea saturate one group and stall at its border.
- Machine learning on graphs: methods that average the features of neighbours, such as [node embeddings](/node-embedding/) and graph neural networks, work best on homophilous graphs and need changes on heterophilous ones.
- Segregation models: Schelling's model shows that a mild preference for similar neighbours can produce strong segregation, which Easley and Kleinberg discuss in the same chapter.

## References
