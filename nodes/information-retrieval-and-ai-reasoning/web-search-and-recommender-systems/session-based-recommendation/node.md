---
tag: N9AP14
kind: problem
slug: session-based-recommendation
name: Session-based recommendation
aliases:
- sequential recommendation
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: advanced
summary: Predict the next item a user will interact with from the ordered items of the current session, often with no user history.
prereqs: [recommendation-problem, implicit-feedback]
see_also: [gru4rec, sasrec, item-based-collaborative-filtering, markov-chain, factorization-machine, cold-start-problem, mean-reciprocal-rank, normalized-discounted-cumulative-gain]
sources:
  - paper: arxiv:1511.06939
    title: Balázs Hidasi, Alexandros Karatzoglou, Linas Baltrunas and Domonkos Tikk, Session-based recommendations with recurrent neural networks, ICLR 2016
    locator: Section 1 (why sessions are anonymous and why item-to-item methods use only the last click), Section 2.1 (item-to-item and Markov decision process approaches), Section 4 (RSC15 and VIDEO data, recall@20 and MRR@20, the POP, S-POP, Item-KNN and BPR-MF baselines)
  - paper: arxiv:1808.09781
    title: Wang-Cheng Kang and Julian McAuley, Self-attentive sequential recommendation, IEEE International Conference on Data Mining (ICDM 2018)
    locator: Abstract and Section I (sequential recommendation, Markov chain and RNN approaches), Section III (the problem as next-item prediction over a user's action sequence), Section IV (leave-last-out split, Hit@10 and NDCG@10 over 100 sampled negatives)
  - paper: doi:10.1145/1772690.1772773
    title: Steffen Rendle, Christoph Freudenthaler and Lars Schmidt-Thieme, Factorizing personalized Markov chains for next-basket recommendation, Proceedings of the 19th International Conference on World Wide Web (WWW 2010), 811-820
    locator: The FPMC model (a factorized, personalized first-order Markov chain over baskets)
  - paper: arxiv:1803.09587
    title: Malte Ludewig and Dietmar Jannach, Evaluation of session-based recommendation algorithms
    locator: Abstract (a comparison of neural and simple methods on many data sets, in which nearest neighbor methods often did as well as or better than GRU4Rec)
---

Session-based recommendation asks for the next item a user will click, view or buy, given the ordered list of items they have acted on in the current visit. The user is often anonymous, so there is no long history and no user profile to factorize; the session itself is the only evidence. Hidasi et al. (2016, Section 1) give the reasons: many shops and most news and media sites do not track users over long periods, tracking by cookies is unreliable and raises privacy concerns, and many users have only one or two sessions. The data are [implicit feedback](/implicit-feedback/): clicks and views, not ratings. Methods range from item-to-item similarity on the last click to recurrent and self-attentive networks over the whole session. Which method predicts best is measured on logged sessions, never proved, and published comparisons disagree.

## In plain words

Someone you do not know walks into your shop and looks at a phone, then a phone case, then a charger. What will they look at next? You know nothing about them except these three clicks, in this order. Session-based recommendation is the problem of guessing the next click from the clicks so far. A simple answer looks only at the last item and suggests what other people looked at after it. Better answers try to use the whole session and its order.

## Definition

**Input.** A set $I$ of $n$ items; a training log of sessions, each a sequence $(s_1, s_2, \dots, s_T)$ of items from $I$ in time order; and a current session prefix $(s_1, \dots, s_t)$.

**Output.** A score for every item in $I$, or a ranked list of the top $k$ items, as a prediction of $s_{t+1}$.

**Objective.** The aim is to rank the true next item high. It is measured offline by replaying held-out sessions: at each position $t$, rank all items given $s_1, \dots, s_t$, and record where $s_{t+1}$ lands. Common measures are recall at $k$ (the fraction of positions where $s_{t+1}$ is in the top $k$; Hidasi et al. use $k = 20$) and [mean reciprocal rank](/mean-reciprocal-rank/) cut off at $k$, or hit rate and [NDCG](/normalized-discounted-cumulative-gain/) at $k$ (Kang and McAuley use $k = 10$).

**What is not given.** In the strict session-based setting there is no user identifier, so sessions of the same person are treated as unrelated (Hidasi et al. 2016, Section 1). Training and test sessions are usually split by time.

## Variants

- **Sequential recommendation.** The user is known, and the input is the user's whole history of actions in order, possibly over months. The task is still next-item prediction, but a model may keep a per-user representation. SASRec is defined in this setting: it takes a user's action sequence and predicts the next item at each step (Kang and McAuley 2018, Section III). The alias "sequential recommendation" therefore names a broader problem than this page; session-based recommendation is the case with short, anonymous sequences.
- **Next-basket recommendation.** Each step is a set of items bought together, and the task is to predict the next basket. Factorizing personalized Markov chains (FPMC) were introduced for this (Rendle et al. 2010).
- **Session-aware recommendation.** The user is known and has past sessions, and the model combines the current session with long-term preferences.
- **Recommendation within a session versus at its end.** Some tasks predict every next click; others predict only the final purchase of a session.

## Examples

**Transition counts.** Take four training sessions: $(a, b, c)$, $(a, b)$, $(b, c)$ and $(a, c)$. Count how often each item directly follows each other item: $a \to b$ twice, $b \to c$ twice, $a \to c$ once. A first-order [Markov chain](/markov-chain/) recommender scores candidates by these counts from the last item. For the session $(a)$ it ranks $b$ (count 2) above $c$ (count 1). For the session $(a, b)$ it looks only at $b$ and ranks $c$ first. It would give the same answer for $(c, b)$ as for $(a, b)$, because it ignores everything before the last click; that is the weakness Hidasi et al. point out in item-to-item methods (Section 1).

**Data sets.** The RSC15 data of Hidasi et al. (from the RecSys Challenge 2015) has 7,966,257 training sessions with 31,637,239 clicks on 37,483 items from an online shop; the test set is the sessions of the following day (Section 4).

## Known algorithms

- **Popularity.** Recommend the most popular items overall (POP) or within the current session (S-POP). Hidasi et al. note that POP is often strong in some domains and S-POP in domains with many repeat actions (Section 4).
- **Item-to-item neighbors.** Precompute the similarity of items from how often they occur in the same sessions, and recommend the items most similar to the last click. This is [item-based collaborative filtering](/item-based-collaborative-filtering/) on sessions; Hidasi et al. call it one of the most common methods in practice and a strong baseline. Session-based nearest neighbor methods compare the whole current session with past sessions instead.
- **Markov chains.** Score the next item from transition statistics from the last item or the last few. The state space grows quickly with the number of items remembered (Hidasi et al. 2016, Section 2.1). FPMC factorizes the transition tensor so that rare transitions share parameters.
- **Factor models.** Plain matrix factorization needs a user vector and so does not apply directly to anonymous sessions. A session can be represented by the factors of its items, and [factorization machines](/factorization-machine/) can take the previous items as features.
- **Recurrent networks.** [GRU4Rec](/gru4rec/) reads the session one item at a time with a gated recurrent unit, keeps a hidden state for the session, and scores every item after each step.
- **Self-attention.** [SASRec](/sasrec/) applies a causal self-attention block, like the decoder of a transformer, to the sequence, so each step can draw on any earlier item, not only the last one.

## Bounds

There are no accuracy guarantees for this problem: the target is the behavior of real users, and every claim about prediction quality is an empirical measurement on a particular log. The reported results also depend on the protocol. Kang and McAuley rank the true item against 100 sampled negatives (Section IV); Hidasi et al. rank against all 37,483 items on RSC15 and against the 30,000 most popular items on their video data (Section 4). Results from different protocols are not comparable. Ludewig and Jannach (2018) compared neural and simple methods on many data sets and found, in their abstract, that simple nearest neighbor methods often did as well as or better than GRU4Rec.

For cost, any method that scores every item does $\Omega(n)$ work per prediction, one score per item. GRU4Rec with hidden size $H$ does $O(n H)$ work for the output layer per step, and SASRec with dimension $d$ does $O(n d)$ for the final scores.

## Reductions

- **To general recommendation.** Treating each session as a separate user turns the problem into top-$k$ recommendation from [implicit feedback](/implicit-feedback/), but this throws away the order of the items and gives each user very little data.
- **To language modeling.** A session is a sentence whose words are items, and next-item prediction is next-word prediction. This is why sequence models from natural language processing (recurrent networks, then transformers) were applied to it. The analogy breaks where the vocabulary is far larger and repeats are common.
- **To classification.** With a fixed window of the last $L$ items as features, the next item is one class out of $n$, and any classifier with a ranking output can be trained on it; this is the view behind higher-order Markov models.

## Applications

- **Online shops** with many anonymous or first-time visitors, as in the RSC15 data.
- **News and media sites,** where users rarely log in and what they want changes from visit to visit.
- **Video and music streaming,** for choosing the next video or track from what was just played, as in the VIDEO data of Hidasi et al.
- **Cold start for users.** A new user has no history but has a session, so session-based methods are one answer to the user side of the [cold-start problem](/cold-start-problem/).

## References
