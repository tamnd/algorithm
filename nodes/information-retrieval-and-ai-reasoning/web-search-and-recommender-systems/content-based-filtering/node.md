---
tag: 9TR7F8
kind: technique
slug: content-based-filtering
name: Content-based filtering
aliases:
- content-based recommendation
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: intro
summary: Recommends items whose features are similar to those of items the user liked before, from a profile of item features.
prereqs: [recommendation-problem]
see_also: [collaborative-filtering, hybrid-recommender, tf-idf, vector-space-model, rocchio-algorithm, naive-bayes-classifier, cosine-similarity, cold-start-problem]
sources:
  - paper: doi:10.1007/978-3-540-72079-9_10
    title: Michael J. Pazzani and Daniel Billsus, Content-based recommendation systems, in The Adaptive Web, Lecture Notes in Computer Science 4321, Springer, 2007, 325-341
    locator: the representation of items by structured attributes and by free text with tf-idf weights, the user profile, the methods that learn it (decision trees and rules, nearest neighbors, relevance feedback and Rocchio's algorithm, linear classifiers, naive Bayes), and the limits of the approach
  - book: isbn:9783319296579
    title: Charu C. Aggarwal, Recommender Systems, The Textbook, Springer, 2016
    locator: Chapter 4 (content-based recommender systems)
  - paper: doi:10.1109/MC.2009.263
    title: Yehuda Koren, Robert Bell and Chris Volinsky, Matrix factorization techniques for recommender systems, IEEE Computer 42(8), 30-37, 2009
    locator: section Recommender system strategies (content filtering, its need for external information, and its comparison with collaborative filtering)
---

Content-based filtering recommends to a user the items whose features resemble those of the items the user liked before. Each item is described by features, such as genres, actors, words of a text or attributes of a product, and each user gets a profile built from the features of the items that the user rated or chose. Unlike [collaborative filtering](/collaborative-filtering/), it uses no data from other users, so it can recommend a new item as soon as its features are known.

## In plain words

If you liked three detective novels, a content-based system looks at what these books have in common, such as the genre, the setting or the words that their descriptions use, and offers you more books with the same traits. It learns your taste as a list of traits that you like or dislike.

It needs a description of every item, and it never asks what other readers thought. So a brand new book can be recommended on its first day. But the system only finds more of what you already know, and it cannot guess that you would also enjoy something of a different kind.

## When it applies

- **Items have useful descriptions.** Text, tags, categories or attributes that relate to taste: news articles, documents, jobs, recipes, products with specifications.
- **New items arrive often.** News and job offers are fresh every day and have no ratings yet.
- **Few users, or private data.** The profile of a user depends only on that user's own history.
- **Explanations are needed.** "Because you liked other films with this actor" follows directly from the profile.
- **Not for new users.** A user with no history still has no profile, see the [cold-start problem](/cold-start-problem/).

## The template

1. **Represent the items.** Turn each item into a feature vector $x_i$. For text, use the [vector space model](/vector-space-model/) with [tf-idf](/tf-idf/) weights; for structured data, use one coordinate per attribute value.
2. **Collect the user's feedback.** The items that the user rated, with their ratings, or the items the user chose, as positive examples.
3. **Build the profile.** Either a vector in the same space, such as the sum of $(r_{ui} - \mu_u) x_i$ over the rated items, a form of the [Rocchio algorithm](/rocchio-algorithm/) for relevance feedback, or a classifier or regressor trained on the user's items alone, such as a [naive Bayes classifier](/naive-bayes-classifier/), [logistic regression](/logistic-regression/) or [linear regression](/linear-regression/).
4. **Score the unseen items.** Use the [cosine similarity](/cosine-similarity/) of $x_i$ with the profile vector, or the output of the classifier.
5. **Rank** and return the best $N$, after removing the items that the user already knows.

## Classic examples

Give the four items of the toy matrix of this group three features each, action, romance and comedy: $i_1 = (1, 1, 0)$, $i_2 = (1, 0, 0)$, $i_3 = (1, 0, 0)$ and $i_4 = (0, 1, 1)$. User $u_1$ rated $i_1$ with 5, $i_2$ with 4 and $i_4$ with 1, with the mean $10/3$.

| item | features | $r_{u_1 i} - \mu_{u_1}$ | contribution to the profile |
|---|---|---|---|
| $i_1$ | (1, 1, 0) | 5/3 | (5/3, 5/3, 0) |
| $i_2$ | (1, 0, 0) | 2/3 | (2/3, 0, 0) |
| $i_4$ | (0, 1, 1) | $-7/3$ | (0, $-7/3$, $-7/3$) |

The profile is $(7/3, -2/3, -7/3)$: $u_1$ likes action and dislikes comedy, and romance is about neutral. The cosine of the profile with $i_3 = (1, 0, 0)$ is $\frac{7/3}{\sqrt{102}/3} \approx 0.693$, so $i_3$ is a good candidate. A new comedy $i_5 = (0, 0, 1)$ that nobody has rated gets $\approx -0.693$ and is not recommended. No other user entered the computation, and $i_5$ needed no ratings.

Other examples are news filters that score articles by the words of the articles a reader opened, and the use of item text in the systems that Pazzani and Billsus (2007) review.

## Variations

- **Uncentered profiles.** The plain average of the features of the liked items ignores dislikes. On the example it gives $(3, 2, 1/3)$, a profile that likes all three genres.
- **Classifiers per user.** A [naive Bayes classifier](/naive-bayes-classifier/) or a linear classifier per user predicts "liked" from the features.
- **Learned item features.** Features from [embeddings](/embedding/) of text or images, or topics from [latent semantic analysis](/latent-semantic-analysis/), in place of raw words.
- **Knowledge-based recommendation.** The user states the required attributes, and the system filters by rules; no history is needed.
- **Combined with collaborative signals.** See [hybrid recommenders](/hybrid-recommender/).

## Pitfalls

- **Overspecialization.** The system recommends only items close to the profile, so the lists lack variety and surprise.
- **Shallow features.** Two films with the same genre and actors can differ in quality, which the features do not show.
- **Feature work.** Every item needs a description of the same kind, and building it can be costly.
- **Raw text weights.** Without [tf-idf](/tf-idf/) or a similar weighting, common words dominate the profile.
- **Uncentered ratings.** Ratings used as weights without centering make every rated item count as liked, as in the uncentered variation above.

## Exercises

1. On the example, add $i_3$ to the history of $u_1$ with the rating 4. Compute the new mean and profile. *Hint: the mean becomes $14/4 = 3.5$.*
2. Show that adding a constant to all ratings of a user does not change the centered profile.
3. Give an example of two items with the same feature vector that users rate very differently. What can a content-based method predict for them?
4. Explain why content-based filtering helps with a new item but not with a new user.

## References
