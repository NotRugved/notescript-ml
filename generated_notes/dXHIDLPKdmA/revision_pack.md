# Revision Pack: Simple Linear Regression | Mathematical Formulation | Coding from Scratch

**One-Line Summary:** DBSCAN uses density (eps and min_samples) to find clusters of arbitrary shapes and automatically identify noise points, overcoming K-Means' spherical assumption and fixed K limitations.

## Cheat Sheet

| Concept | Definition/Formula | Key Detail |
| :--- | :--- | :--- |
| **DBSCAN** | Density-Based Spatial Clustering of Applications with Noise | No need to specify K (num clusters). |
| **Epsilon (eps)** | $N_\epsilon(p) = \{ q \in D \mid \text{dist}(p, q) \le \epsilon \}$ | Radius of the neighborhood circle. |
| **MinPts** | Minimum points in $N_\epsilon(p)$ | **Includes the point p itself.** |
| **Core Point** | $|N_\epsilon(p)| \ge \text{MinPts}$ | Dense region center. |
| **Border Point** | $|N_\epsilon(p)| < \text{MinPts}$ BUT inside a Core Point's $N_\epsilon$ | Edge of the cluster. |
| **Noise Point** | Not Core, not Border | Labelled as -1 (Outlier). |
| **K-Means Limit** | Assumes spherical clusters | Fails on moons/circles; sensitive to outliers. |
| **Hier Limit** | $O(n^2)$ or $O(n^3)$ complexity | Slow on large data; no explicit noise handling. |

## Flashcards

### Card 1
**Q:** DBSCAN ka full form kya hai?

**A:** Density-Based Spatial Clustering of Applications with Noise.

### Card 2
**Q:** DBSCAN me 'eps' (Epsilon) kya represent karta hai?

**A:** Yeh ek radius hai jo kisi point ke around neighborhood define karta hai. Points jo is distance ke andar hote hain, unhe neighbors maana jata hai.

### Card 3
**Q:** MinPts (min_samples) calculation me center point ko count karte hain ya nahi?

**A:** Haan, center point (p) ko khud count karte hain. Condition hai $|N_\epsilon(p)| \ge \text{MinPts}$.

### Card 4
**Q:** Core Point ki mathematical condition kya hai?

**A:** Ek point p Core Point hai agar uske epsilon-neighborhood me points ki sankhya MinPts se barabar ya zyada ho ($|N_\epsilon(p)| \ge \text{MinPts}$).

### Card 5
**Q:** Border Point kya hota hai?

**A:** Ek point jo khud Core Point nahi hai (uske paas MinPts se kam points hain), lekin wo kisi Core Point ke epsilon-neighborhood ke andar aata hai.

### Card 6
**Q:** Noise Point ko DBSCAN me kya label diya jata hai?

**A:** Noise points ko outlier label (-1) diya jata hai aur inhe kisi bhi cluster ka hissa nahi maana jata.

### Card 7
**Q:** K-Means clustering ki sabse badi limitation kya hai jo DBSCAN solve karta hai?

**A:** K-Means assume karta hai ki clusters spherical (globular) hain. DBSCAN arbitrary shapes (jaise concentric circles) ko bhi handle kar sakta hai.

### Card 8
**Q:** DBSCAN chalane ke liye pehle se number of clusters (K) specify karna zaroori hai?

**A:** Nahi. DBSCAN data ki density ke basis par khud clusters decide karta hai. Isme sirf eps aur min_samples set karne hote hain.

### Card 9
**Q:** Hierarchical Clustering ki time complexity kya hoti hai?

**A:** Yeh $O(n^2)$ ya $O(n^3)$ hoti hai, jisse yeh large datasets par bohot slow ho jata hai.

### Card 10
**Q:** DBSCAN me 'Density' kaise define hoti hai?

**A:** Jahan points dense hote hain (MinPts se zyada points eps radius me), wahan cluster form hota hai. Sparse regions ko noise maana jata hai.

### Card 11
**Q:** K-Means me outliers ka kya asar hota hai?

**A:** Outliers centroid ki position ko drastically shift kar dete hain, jisse clustering quality kharab ho jati hai. DBSCAN inhe noise ke roop me separate kar deta hai.

### Card 12
**Q:** Epsilon-neighborhood $N_\epsilon(p)$ ka formula kya hai?

**A:** $N_\epsilon(p) = \{ q \in D \mid \text{dist}(p, q) \le \epsilon \}$

### Card 13
**Q:** Border point kisi cluster ka part hota hai ya noise?

**A:** Border point cluster ka part hota hai kyunki wo kisi Core Point se connected hai, lekin wo khud dense region ka center nahi hai.

### Card 14
**Q:** DBSCAN kyun 'Noise' based clustering kehlata hai?

**A:** Kyunki yeh algorithm data me present sparse points ko explicitly 'Noise' ya 'Outlier' identify karke alag kar deta hai, unhe force fit nahi karta.

### Card 15
**Q:** Agar MinPts = 5 hai aur kisi point ke eps circle me 4 points hain (including itself), toh wo point kya hoga?

**A:** Wo Core Point nahi hoga. Agar wo kisi aur Core Point ke neighborhood me hai toh Border Point, warna Noise Point.

## Quiz

#### Question 1: DBSCAN me 'eps' parameter kya define karta hai?
- [0] Number of clusters
- [1] Radius of the neighborhood
- [2] Minimum distance between clusters
- [3] Maximum number of points in a cluster

#### Question 2: MinPts count karte waqt center point ko kaise treat kiya jata hai?
- [0] Exclude kiya jata hai
- [1] Include kiya jata hai
- [2] Half weight diya jata hai
- [3] Ignore kiya jata hai

#### Question 3: K-Means clustering ki limitation kya hai jo DBSCAN solve karta hai?
- [0] High computational complexity
- [1] Assumption of spherical clusters
- [2] Inability to handle high dimensions
- [3] Requirement of labeled data

#### Question 4: DBSCAN me Noise points ko kya label assign kiya jata hai?
- [0] 0
- [1] 1
- [2] -1
- [3] NaN

#### Question 5: Ek point Border Point tab hota hai jab:
- [0] Uske paas MinPts se zyada points hain
- [1] Wo Core Point nahi hai par kisi Core Point ke neighborhood me hai
- [2] Wo kisi bhi point ke neighborhood me nahi hai
- [3] Uska distance centroid se zero hai

#### Question 6: DBSCAN chalane ke liye pehle se specify karna zaroori hai:
- [0] Number of clusters (K)
- [1] Epsilon and MinPts
- [2] Initial centroids
- [3] Linkage criterion

#### Question 7: Hierarchical Clustering ki time complexity kya hoti hai?
- [0] O(n log n)
- [1] O(n)
- [2] O(n^2) or O(n^3)
- [3] O(1)

#### Question 8: Agar kisi point ke eps-neighborhood me points ki sankhya MinPts se kam hai, toh wo point Core Point hai?
- [0] Haan
- [1] Nahi
- [2] Shayad
- [3] Sirf agar yeh outlier hai

#### Question 9: DBSCAN ka intuition 'Bheed ko cluster maano' ka matlab kya hai?
- [0] Jahan points sparse hain wahan cluster banta hai
- [1] Jahan points dense hain wahan cluster banta hai
- [2] Har point ek alag cluster hai
- [3] Sab points ek hi cluster me hote hain

#### Question 10: K-Means me outliers ka kya asar hota hai?
- [0] Koi asar nahi hota
- [1] Centroid ko shift kar dete hain
- [2] Clusters ko merge kar dete hain
- [3] Algorithm ko crash kar dete hain

### Quiz Answers & Explanations

- **Q1 Answer:** Option 1 — Epsilon (eps) ek radius hai jo kisi point ke around circular neighborhood define karta hai.
- **Q2 Answer:** Option 1 — DBSCAN me MinPts calculation me point p khud bhi count hota hai. Condition $|N_\epsilon(p)| \ge \text{MinPts}$ me p included hai.
- **Q3 Answer:** Option 1 — K-Means assume karta hai ki clusters spherical hain. DBSCAN arbitrary shapes (non-globular) ko handle kar sakta hai.
- **Q4 Answer:** Option 2 — Noise points ko outlier label -1 diya jata hai taaki inhe clusters se alag identify kiya ja sake.
- **Q5 Answer:** Option 1 — Border point khud dense nahi hota (MinPts se kam points), lekin wo kisi Core Point ke eps-neighborhood ke andar fall karta hai.
- **Q6 Answer:** Option 1 — DBSCAN me K specify nahi karna padta. Sirf eps (radius) aur min_samples (MinPts) set karne hote hain.
- **Q7 Answer:** Option 2 — Hierarchical clustering ki complexity O(n^2) ya O(n^3) hoti hai, jisse yeh large data par slow ho jata hai.
- **Q8 Answer:** Option 1 — Core Point hone ke liye zaroori hai ki $|N_\epsilon(p)| \ge \text{MinPts}$ ho. Kam points hone par wo Core Point nahi hota.
- **Q9 Answer:** Option 1 — DBSCAN density-based hai. Jahan points dense (bheed) hote hain, wahan cluster form hota hai. Sparse regions noise hote hain.
- **Q10 Answer:** Option 1 — K-Means har point ko assign karta hai, isliye outliers centroid ki position ko drastically shift karke clustering quality kharab kar dete hain.

## Interview Questions

### Q1: K-Means ke muqable DBSCAN ke advantages kya hain?

**Answer:** DBSCAN ke main advantages hain: 1) Yeh arbitrary shapes (non-spherical) ke clusters ko handle kar sakta hai, jabki K-Means sirf spherical clusters ke liye best hai. 2) DBSCAN automatically outliers/noise points ko identify karke alag kar deta hai, jabki K-Means inhe force fit karke centroid ko shift kar deta hai. 3) DBSCAN me number of clusters (K) pehle se specify nahi karna padta, yeh data ki density ke basis par khud decide karta hai.

### Q2: DBSCAN me Core Point, Border Point aur Noise Point me kya difference hai?

**Answer:** Core Point: Jiske eps-neighborhood me MinPts ya usse zyada points hain (including itself). Border Point: Jo khud Core Point nahi hai (MinPts se kam points) lekin kisi Core Point ke eps-neighborhood ke andar aata hai. Noise Point: Jo na Core Point hai aur na hi kisi Core Point ke neighborhood me fall karta hai. Inhe outlier label (-1) diya jata hai.

### Q3: DBSCAN ke hyperparameters eps aur min_samples ko kaise tune karte hain?

**Answer:** Epsilon (eps) ko tune karne ke liye k-Means ya distance distribution plot use kar sakte hain. Aksar 'k-distance plot' use hota hai jahan hum har point ke k-th nearest neighbor ka distance dekhte hain aur 'elbow' point par eps set karte hain. MinPts usually 2D me 3 ya usse zyada rakha jata hai (dimensions + 1). MinPts chhota hone par noise points ko cluster bana sakte hain, aur bada hone par dense regions ko noise maan liya ja sakta hai.

### Q4: DBSCAN high-dimensional data par kyun fail ho sakta hai?

**Answer:** High dimensions me 'Curse of Dimensionality' ki wajah se saare points ek doosre se lagbhag same distance par ho jate hain. Isliye density ka concept lose ho jata hai. Kisi bhi point ke eps-neighborhood me ya toh bohot zyada points aa jate hain (sab ek cluster) ya bohot kam (sab noise). Isliye DBSCAN high-dimensional data ke liye suitable nahi maana jata.

### Q5: DBSCAN me MinPts me center point ko include karne ka kya reason hai?

**Answer:** MinPts me center point ko include karna standard convention hai taaki density calculation consistent rahe. Agar hum center point ko exclude karte, toh MinPts = 1 hone par bhi point ko dense maana jata (kyunki khud hi ek point hai). Include karne se logic clear rehta hai: 'Is region me total kitne points hain?'. Isse implementation aur theoretical definitions me consistency banti hai.
