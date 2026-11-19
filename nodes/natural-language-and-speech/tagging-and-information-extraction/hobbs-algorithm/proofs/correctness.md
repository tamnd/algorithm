---
title: "The Hobbs search ends, proposes each NP at most once, and never proposes the pronoun or an NP bound by it"
proves: [correctness]
status: full
---

The Hobbs algorithm is a heuristic: nothing guarantees that its answer is the true antecedent. What can be proved is that the search does what the nine steps say, that it ends, and that its order has the properties the page relies on. Fix the parse tree $T$ of the current sentence with root $r$, the trees $T_1, \ldots, T_q$ of the earlier sentences, and the NP node $\pi$ of the pronoun, with $\pi \ne r$. The line numbers refer to the pseudocode on the page.

## Claim 1: the walk of each step is breadth first, left to right, and covers exactly its region

For a node $x$ and a path $p = (x = v_0, v_1, \ldots, v_t)$ down the tree, the region left of $p$ is the set of nodes below some $v_k$, $k < t$, in a subtree whose root is a child of $v_k$ to the left of $v_{k+1}$; the region right of $p$ is defined the same way with the children to the right. The walk side_of_path keeps a queue that starts with $x$. When it takes a path node $v_k$ with $k < t$, it appends the children on the chosen side and $v_{k+1}$, in left-to-right order. When it takes $v_t$ it appends nothing. When it takes any other node, it yields it and appends its children. So the nodes yielded are exactly the nodes of the region, and every node of depth $d$ below $x$ enters the queue before any node of depth $d + 1$, because the queue receives nodes in the order of their parents. Among nodes of the same depth, a node enters the queue before every node to its right, since the parents are taken in left-to-right order and each parent appends its children left to right. This is the breadth-first, left-to-right order of steps 3, 7 and 8. Step 8 also does not append the children of an NP or S node, which is the rule "do not go below any NP or S node". The same argument gives the order of the plain walk bfs used in step 4. The test file compares bfs with an independent order, the sort by depth and then by preorder position.

## Claim 2: the search ends

Each pass through lines L5 to L9 replaces $X$ by an NP or S node strictly above it, so $X$ moves up at each pass. The tree is finite, so after at most its height many passes $X = r$, and line L4 then walks the earlier trees once each and stops. Each walk visits a finite tree once.

## Claim 3: each NP is proposed at most once, and the pronoun never

Let $X_0$ be the node of line L2 and $X_1, X_2, \ldots, X_s = r$ the nodes of line L5, with paths $p_0, p_1, \ldots$, where $p_k$ runs from $X_k$ down to $X_{k-1}$ ($X_{-1} = \pi$). Each region of step 3, 7 or 8 for $X_k$ lies below $X_k$ and outside the subtree of $X_{k-1}$, because the end node of the path is not expanded. The subtrees of $X_0 \subset X_1 \subset \cdots$ are nested, so the regions of different passes are disjoint, and in the same pass the left and right regions are disjoint by definition. A node proposed by line L6 is $X_k$ itself, which is in no region below $X_k$ and is outside every region of earlier passes, which lie below $X_{k-1}$. A later pass sees $X_k$ only as an interior path node, which is not yielded. The earlier trees are disjoint from $T$ and from each other. Hence no node is proposed twice. The pronoun node $\pi$ is the end of the path $p_0$ and is not yielded by the walk of step 3; it is not an $X_k$ for $k \ge 0$; so it is never proposed, and line L10 also skips it by identity.

## Claim 4: the two syntactic filters

Step 3 proposes an NP $n$ below $X_0$ only if an NP or S node lies strictly between $n$ and $X_0$. So an NP that is a sister of the path inside the smallest NP or S that holds the pronoun, such as the subject when the pronoun is the object in "John likes him", is never proposed in step 3. This is the effect Hobbs wanted: a non-reflexive pronoun is not bound inside its own clause. Step 6 proposes $X_k$ only if the path does not pass through the Nominal (N-bar) child of $X_k$. So an NP whose head noun phrase contains the pronoun, such as "the Fords in his lot" for "his", is never proposed. The code tests the label of the first node of the path below $X_k$, which is that child. Both properties follow from the code by reading lines L3 and L6, and the test file checks each on an example.

## What is not claimed

The agreement test of line L10 uses the features given on the nodes; it is only as good as those features. Whether the first agreeing NP is the right antecedent depends on the text, and the accuracy figures on the page are measurements.
