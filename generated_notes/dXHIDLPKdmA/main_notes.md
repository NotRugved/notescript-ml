# Simple Linear Regression | Mathematical Formulation | Coding from Scratch

**Video Link:** [https://www.youtube.com/watch?v=dXHIDLPKdmA](https://www.youtube.com/watch?v=dXHIDLPKdmA)

**Summary:** DBSCAN uses density (eps and min_samples) to find clusters of arbitrary shapes and automatically identify noise points, overcoming K-Means' spherical assumption and fixed K limitations.

## Theory

### Introduction to DBSCAN and Motivation ([00:00](https://youtu.be/dXHIDLPKdmA?t=0))

DBSCAN ka full form hai **Density-Based Spatial Clustering of Applications with Noise**. Pichle sessions me humne do major clustering techniques padhi hain: **K-Means Clustering** aur **Hierarchical Clustering** (specifically Agglomerative Hierarchical Clustering). Lekin in dono algorithms ki kuch inherent limitations hoti hain jinki wajah se hume DBSCAN ki zaroorat padti hai.

### Limitations of K-Means:
1. **Arbitrary Shapes (Non-Globular Clusters):** K-Means assume karta hai ki clusters spherical ya globular shape ke hain. Agar data concentric circles, crescent moons, ya interconnected density curves jaisi complex shapes me ho, toh K-Means completely fail ho jata hai.
2. **Sensitivity to Outliers:** K-Means har single data point ko kisi na kisi cluster me assign karne ke liye force karta hai. Outliers centroid ki position ko drastically shift kar dete hain aur clustering quality kharab ho jati hai.
3. **Pre-specifying K:** K-Means chalane ke liye pehle se number of clusters ($k$) provide karna compulsory hota hai (using Elbow method etc.), jo complex real-world data me hamesha pata lagana aasan nahi hota.

### Limitations of Hierarchical Clustering:
1. **High Computational Complexity:** Hierarchical clustering ki time complexity $O(n^2)$ ya $O(n^3)$ hoti hai, jisse yeh large datasets par scale nahi kar pata aur bohot slow ho jata hai.
2. **Outlier Handling:** Yeh bhi standard settings me explicit noise points ko separate treat nahi karta.

### Why DBSCAN?:
- DBSCAN density-based approach use karta hai: Jahan points dense hote hain wahan cluster form hota hai, aur sparse regions ko noise/outlier consider kiya jata hai.
- Yeh kisi bhi arbitrary shape ke clusters dhundh sakta hai.
- Outliers ko automatically identify karke alag kar deta hai (noise class -1).
- Isme number of clusters pehle se specify nahi karne padte; algorithm data ki density ke according khud clusters decide karta hai.

### Core Hyperparameters of DBSCAN: Epsilon and MinPts ([05:15](https://youtu.be/dXHIDLPKdmA?t=315))

DBSCAN do primary hyperparameters par kaam karta hai:

1. **Epsilon ($\epsilon$ ya `eps`):**
   - Yeh ek radius hai jo kisi point ke around circular (ya hyperspherical in higher dimensions) neighborhood define karta hai.
   - Mathematically, kisi point $p$ ke around $\epsilon$-neighborhood ko $N_\epsilon(p)$ likhte hain:
     $$N_\epsilon(p) = \{ q \in D \mid \text{dist}(p, q) \le \epsilon \}$$
   - Jahan $D$ dataset hai aur $\text{dist}(p, q)$ usually Euclidean distance hoti hai.

2. **MinPts (`min_samples`):**
   - Epsilon radius ke andar minimum kitne points hone chahiye taaki us region ko 'dense' maana ja sake.
   - Point $p$ khud bhi is count me include hota hai.

### Classification of Data Points in DBSCAN ([07:30](https://youtu.be/dXHIDLPKdmA?t=450))

DBSCAN dataset ke har point ko teen categories me classify karta hai:

1. **Core Point:**
   - Ek point $p$ **Core Point** tab kehlata hai agar uske $\epsilon$-neighborhood me kam se kam `MinPts` points exist karte hon (including point $p$ itself).
   - Condition: $|N_\epsilon(p)| \ge \text{MinPts}$

2. **Border Point:**
   - Ek point jo khud Core Point nahi hai (yaani uske neighborhood me points count $< \text{MinPts}$ hai), LEKIN wo kisi Core Point ke $\epsilon$-neighborhood ke andar belong karta hai.
   - Condition: $|N_\epsilon(p)| < \text{MinPts}$ and $\exists q \in N_\epsilon(p)$ such that $q$ is a Core Point.

3. **Noise Point (Outlier):**
   - Ek point jo na toh Core Point hai aur na hi kisi Core Point ke neighborhood ke andar fall karta hai.
   - In points ko DBSCAN cluster ka part nahi banata aur inko outlier label (-1) assign karta hai.

## Intuition

- ([04:30](https://youtu.be/dXHIDLPKdmA?t=270)) DBSCAN ka simple intuition hai: 'Bheed (crowd) ko cluster maano, aur akele ghoomne wale points ko shor (noise) maano'. Jahan dense aabadi hai, wahan cluster banega. Agar aabadi sparse ho gayi, toh wahan cluster terminate ho jayega.
- ([08:15](https://youtu.be/dXHIDLPKdmA?t=495)) Core point wo insan hai jiske aas-paas bohot saare dost khade hain (dense crowd). Border point wo insan hai jo khud ke paas zyada dost nahi rakhta, par wo crowd ke kinare khada hokar kisi popular (core) bande se connected hai. Aur noise point wo akela insan hai jo crowd se bohot door hai.

## Code

*No code blocks identified.*

## Analogies

- ([06:10](https://youtu.be/dXHIDLPKdmA?t=370)) **Analogy:** Teacher drawing compass/circle analogy use karte hain: Imagine karo point par compass ki tip rakh kar $\epsilon$ radius ka circle draw kiya. Agar us circle ke andar MinPts jitne ya usse zyada points aa gaye, toh wo point VIP (Core point) ban gaya. — *Explains:* How epsilon-neighborhood defines local density around a point to qualify it as a core point.

## Common Mistakes

- **Mistake [teacher]:** MinPts count karte waqt center point (p) ko chhod dena. ([06:50](https://youtu.be/dXHIDLPKdmA?t=410))
  - *Why:* Students aksar sochte hain ki MinPts neighbors ka count hai excluding the point itself.
  - *Fix:* MinPts calculation me point $p$ khud count hota hai (i.e. $|N_\epsilon(p)|$ includes $p$).
- **Mistake [teacher]:** DBSCAN me K (number of clusters) pass karne ki koshish karna. ([03:40](https://youtu.be/dXHIDLPKdmA?t=220))
  - *Why:* K-Means ki aadat ki wajah se log DBSCAN me bhi number of clusters dhundhte hain.
  - *Fix:* DBSCAN ko number of clusters nahi chahiye hote; algorithm eps aur min_samples ke basis par clusters khud find karta hai.

## Formulas & Key Terms

### Formulas
- **Epsilon-Neighborhood of a point p:** `N_\epsilon(p) = \{ q \in D \mid \text{dist}(p, q) \le \epsilon \}` — Point p se epsilon distance ke andar aane wale sabhi points q ka set.
- **Core Point Condition:** `|N_\epsilon(p)| \ge \text{MinPts}` — Epsilon radius circle ke andar points ki sankhya MinPts ke barabar ya usse zyada honi chahiye.

### Key Terms
- **DBSCAN:** Density-Based Spatial Clustering of Applications with Noise.
- **Epsilon (eps / ε):** Neighborhood define karne ke liye specified search radius.
- **MinPts / min_samples:** Neighborhood ke andar dense maane jaane ke liye zaroori minimum points ki sankhya.
- **Core Point:** Point jiske eps-neighborhood me MinPts ya usse zyada points hote hain.
- **Border Point:** Point jo core point nahi hai par kisi core point ke eps-neighborhood me aata hai.
- **Noise Point:** Point jo na core point hai aur na kisi core point ke neighborhood me fall karta hai (Outlier).
