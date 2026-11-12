---
title: The decision process picks a well-defined route, and BGP under the Gao-Rexford rules converges to valley-free, loop-free paths
proves: [correctness, termination]
status: full
---

**Part 1: the decision process.** Let $R$ be a finite set of candidate routes to one prefix. Lines L1 to L10 apply a sequence of filters $R = R_0 \supseteq R_1 \supseteq \dots$. Each filter keeps the routes that are best by one attribute and never empties a nonempty set: "keep the routes with the highest preference" keeps at least the routes that attain the maximum, and the same holds for the shortest AS_PATH, the lowest ORIGIN, the eBGP routes (applied only if one exists), the lowest interior cost and the lowest BGP Identifier. The MED step of line L6 keeps, in each group of routes from one neighbouring AS, the routes with the least MED of that group, so it keeps at least one route of each group. The last step takes the route from the least peer address. Peer addresses of different sessions differ, so exactly one route is left if $R_1 \ne \emptyset$. Each filter is defined by the set and not by the order of its elements, so the result does not depend on the order in which routes arrived. (A router that compares MED pairwise in arrival order, instead of by groups, does not have this property; see RFC 3345.) Line L1 removes every route whose AS_PATH contains the local AS, so the chosen route never makes a loop of ASes.

**Part 2: the Gao-Rexford rules.** Model each AS as one BGP speaker. Each link joins two ASes as customer and provider or as peers. Assume:

- (A1) the directed graph of customer-to-provider links has no cycle;
- (A2) each AS gives routes learned from customers a higher preference than routes from peers or providers (in the code: 300, 200, 100);
- (A3) export: an AS sends its best route to a neighbour $b$ if the route is its own prefix or was learned from a customer, or if $b$ is a customer; otherwise it sends a withdrawal;
- channels are reliable and FIFO, each AS sends its current best within a bounded time after each change, and the network starts with no routes (or, after a change, waits until paths over dead links have died out, as in the [path-vector proof](/path-vector-routing/)).

Fix a prefix of origin AS $o$. Every route that any AS ever holds is a real path in the graph, since no link changes.

*Claim 1 (who can hold a customer route).* Call $a$ an *ancestor* of $o$ if there is a chain $a = a_0, a_1, \dots, a_k = o$, $k \ge 1$, in which each $a_{i+1}$ is a customer of $a_i$. If $a$ ever holds a best route learned from a customer $c$, then $c$ exported it to its provider $a$, so by (A3) $c$'s best was its own prefix ($c = o$) or a customer route. By induction along the path, the path of $a$ goes down customer links only, so $a$ is an ancestor of $o$. Conversely, non-ancestors never hold customer routes, and so (A3) they never export anything to providers or peers.

*Claim 2 (ancestors settle, bottom up).* Order the ancestors of $o$ by height, the length of the longest customer chain from $a$ down to $o$ (finite by A1). We show that each ancestor $a$ eventually holds a fixed customer route for ever. Its customer candidates come from customers $c$ that are $o$ or ancestors of smaller height, which have settled by induction and send their final route to $a$ (by A3, customer routes go to providers), and from customers that are not ancestors, which never send anything. So after some time the set of customer candidates of $a$ is fixed and nonempty. By (A2), any customer route beats every peer and provider route at line L3, so the decision of $a$ is the best of its fixed customer candidates, whatever the other candidates do. So $a$ settles.

*Claim 3 (peers of settled ancestors).* Let $a$ be neither $o$ nor an ancestor. It never has customer candidates (Claim 1). A peer $b$ sends $a$ a route only if $b$'s best is a customer route or $b = o$, so only if $b$ is $o$ or an ancestor; these have settled by Claim 2. So $a$'s set of peer candidates becomes fixed. If it is nonempty, (A2) makes $a$'s choice the best of these, and $a$ settles.

*Claim 4 (the rest, top down).* The remaining ASes have only provider candidates. Order all ASes by (A1) so that providers come before their customers. Let $a$ be remaining and assume that all its providers have settled (each is an ancestor, settled by Claim 2, a peer-route AS of Claim 3, or a remaining AS earlier in the order). A provider sends its customer $a$ its best route, whatever it is (A3), so $a$'s candidate set becomes fixed and $a$ settles, possibly with no route. Peers and customers of $a$ send it nothing for ever, by Claims 1 and 3.

*Termination.* After every AS has settled, no AS changes its best, so no AS sends, and the messages in flight are delivered. The final state is quiet, and as in the path-vector proof, a quiet state is a stable and consistent assignment: the next AS on each path holds the rest of the path.

*Valley-free paths.* By (A3), a route goes up from a customer to a provider only if it was a customer route, that is, only if every link after it, toward $o$, goes down. A route crosses a peer link only if it was a customer route, so after a peer link come only down links. Reading the path from the source toward $o$, it is a run of customer-to-provider links, then at most one peer link, then a run of provider-to-customer links. $\blacksquare$

**Remark.** The proof does not need the speakers to break ties in any special way, only to break them the same way each time. Without (A2) or (A3), the instance can contain a dispute wheel, as BAD GADGET does, and the protocol may never settle.
