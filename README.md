# Gamez Ian 
This repository contains the source code and simulations developed for two areas of applied research: Optical Physics (digital signal processing and beam propagation) and Operations Engineering (supply chain management )



# Bessel Beam Generation and Superposition: Numerical Characterization

This section describes the generation and numerical simulation of Bessel beams and their superposition, as presented in the work by Gámez et al. The methods and results cover both experimental setups and MATLAB-based computations.

---

##  Introduction

Bessel beams are particular solutions to the electromagnetic wave equation that exhibit the remarkable property of **diffraction-free** propagation. Unlike ordinary Gaussian beams, which spread with distance, a Bessel beam maintains a constant transverse intensity profile over a certain propagation length $$Z_{\text{max}}$$ . This behaviour arises from a specific transverse intensity distribution described by Bessel functions of the first kind.

The experimental generation of Bessel beams is commonly achieved using an **annular aperture mask** illuminated by a plane wave, followed by a converging lens placed at its focal distance. The light diffracted by the annular slit produces a Bessel beam.

To generate a superposition of two Bessel beams, a **Michelson interferometer** is used to split the beam intensity, with the beam splitter placed just after the lens to ensure operation within the diffraction-free region. By adjusting the optical path difference between the two arms, one can control the separation and relative phase of the two beams—parameters that are systematically characterised.


##  Superposition of Two Bessel Beams

When two Bessel beams (with possibly different amplitudes, phases, and spatial offsets) are superposed, the resulting intensity distribution is obtained by adding their complex fields and taking the squared modulus:

$$ I_{\text{total}}(r, \phi, z) = \left| E_1(r, \phi, z) + E_2(r, \phi, z) \right|^2 $$

This superposition gives rise to characteristic interference patterns that depend on the relative phase and separation. The experimental cross‑sections  and their corresponding numerical simulations  demonstrate excellent agreement.

<div align="center">
  <img src="https://raw.githubusercontent.com/GamexIan/SkoltechGamez/2ad4dededf0504931ff66ec8555e5782915cb15f/interfe.png" alt="Patrón de interferencia de dos haces Bessel" style="width: 50%;"/>
  <br>
  <em>Figure: The experimental superposition of two Bessel beams.</em>
</div>

##  Numerical Simulations in MATLAB


The complete MATLAB script is available in this repository. You can view it online or download it directly using the links below:

- 📄 **[View the full code on GitHub](https://github.com/GamexIan/SkoltechGamez/blob/ec8e202388b58fda8247028848153173a5ad01f9/twobeams.m)** 


<div align="center">
  <img src="https://raw.githubusercontent.com/GamexIan/SkoltechGamez/ec8e202388b58fda8247028848153173a5ad01f9/interfeskol.png" alt="Numerical interference pattern of two Bessel beams" style="width: 40%;"/>
  <br>
  <em>Figure: The numerical superposition of two Bessel beams, showing the characteristic interference fringes.</em>
</div>



# Gaussian Beam Propagation in Nonlinear Media

This section covers the numerical simulation of a Gaussian beam propagating through a thin nonlinear optical medium with local and nonlocal Kerr-type nonlinearities. The implementation uses the **split-step Fourier method** (SSFM) to solve the paraxial wave equation, capturing self-phase modulation, diffraction, and absorption effects.

---

##  Introduction

When a material exhibits an intensity‑dependent refractive index, a well‑defined incident intensity distribution is modified as it propagates through the sample. The light–matter interaction determines the nature of the nonlinear response, which can be local or non‑local. This work presents a numerical model to describe the local nonlinear response of a thin medium under Gaussian illumination, considering the field at the exit plane of the material. A Fourier transform is then applied to obtain far‑field diffraction patterns.

The model accounts for locality by modifying the width of the phase‑change profile at the sample exit, referencing the incident intensity profile. Locality also affects the magnitude of the on‑axis nonlinear phase shift and the field amplitude.

---

##  Theoretical Model

###  Gaussian Beam Propagation


Under the **paraxial approximation** (slowly varying envelope), the field is written as \( E(x,y,z) = \psi(x,y,z) e^{-ikz} \), leading to the paraxial wave equation:

$$
\nabla_{\perp}^2 \psi - 2ik \frac{\partial \psi}{\partial z} + 2k^2 \frac{\Delta n(I)}{n_0} \psi + ik\alpha(I) \psi = 0 \qquad (1)
$$

with:
- \( \nabla_{\perp}^2 = \partial_x^2 + \partial_y^2 \),
- \( \Delta n(I) = n_2 I + s (R * I) \) (local and nonlocal contributions),
- \( \alpha(I) = \alpha_0 + \beta I \) (linear and nonlinear absorption),
- \( n_2 \) the Kerr coefficient.
- 📄 **[View the full code on GitHub](https://github.com/GamexIan/SkoltechGamez/blob/5f39a46cc7ae92298b3090faeccef3dcbb067d1f/Evolution.m)**
- 
  <div align="center"> <img src="https://raw.githubusercontent.com/GamexIan/SkoltechGamez/5f39a46cc7ae92298b3090faeccef3dcbb067d1f/evolution1.png" alt="Intensity evolution of a Gaussian beam in a nonlinear medium" width="550"/> <br> <em>Figure:  Propagation of a Gaussian beam in a locally nonlinear medium, viewed from above</em> </div>

###  Operator Splitting

Equation (1) can be written as:

$$
\frac{\partial \psi}{\partial z} = (\hat{D} + \hat{N}) \psi \qquad (2)
$$

where:

- $ \hat{D} = \frac{i}{2k} \nabla_{\perp}^2 $ is the diffraction operator,
- $ \hat{N} = \frac{i k}{n_0} \Delta n(I) - \frac{\alpha(I)}{2} $ is the nonlinear operator.

For a small propagation step \( h \), the formal solution is approximated by the symmetric split‑step:

$$\psi(z+h) \approx \exp\left(\frac{h}{2}\hat{N}\right) \exp\left(h\hat{D}\right) \exp\left(\frac{h}{2}\hat{N}\right) \psi(z) \qquad (3) $$

The diffraction step is performed in the Fourier domain using the paraxial transfer function:

$$
\mathcal{L}_{\text{paraxial}}(\Delta z) = \exp\left[-i \Delta z \frac{k_x^2 + k_y^2}{2k}\right] \qquad (4)
$$

where \( k_x, k_y \) are transverse spatial frequencies.

📄 **[View the full code on GitHub](https://github.com/GamexIan/SkoltechGamez/blob/e9019e28e27adcd40b2a203bf6a134e0300420a8/Evolution.m)**
<div align="center">
  <img src="https://raw.githubusercontent.com/GamexIan/SkoltechGamez/627b7df61d237f294334c7f690756139d8065c9b/gauss1.png" alt="Evolución de la intensidad del haz gaussiano en medio no lineal - Vista 1" width="450"/>
  <br>
  <em>Figure: Diffraction patterns and far-field intensity profiles in a local medium placed at different positions relative to w0: z = 0 and ∆Φ0 = 2π..</em>
</div>

<div align="center">
  <img src="https://raw.githubusercontent.com/GamexIan/SkoltechGamez/627b7df61d237f294334c7f690756139d8065c9b/gauss2.png" alt="Evolución de la intensidad del haz gaussiano en medio no lineal - Vista 2" width="350"/>
  <br>
  <em>Figure: Comparison of intensity profiles at the input and output of a local medium positioned with respect to w0:  z = 0 and
∆Φ0 = 2π..</em>
</div>


# Inventory Replenishment Policies: A Queueing Theory Approach

This section presents a comprehensive framework for modelling and optimizing inventory control systems using stochastic processes and queueing theory. The focus is on the **(s, S)** replenishment policy, where **s** is the reorder point and **S** is the order‑up‑to level. We derive performance measures, cost functions, and service levels for a queueing‑inventory system with lost sales and compound geometric demand. Python implementations are provided for numerical evaluation and policy optimisation.

---

## 1. Introduction

Inventory management is a cornerstone of supply chain operations, aiming to balance holding costs, ordering costs, and lost sales in the face of uncertain demand. Scientific inventory control uses mathematical models to determine when and how much to reorder.
## 2. Inventory Control Fundamentals

### 2.1 Basic Concepts

An **inventory system** represents the stock of products available to meet customer demand. The main goal is to minimise total costs while achieving a desired service level.

**Classification of demand:**

| Demand Type | Description |
|-------------|-------------|
| **Deterministic** | Future demand is known with certainty. |
| **Stochastic** | Demand is uncertain and modelled via probability distributions. |

**Review mechanisms:**

- **Periodic review** – inventory is checked at fixed time intervals (e.g., weekly).
- **Continuous review** – inventory is updated after every transaction.

**Demand fulfilment:**

- **Backordering** – unmet demand is satisfied later.
- **Lost sales** – unmet demand is permanently lost.

### 2.2 Replenishment Policies

A replenishment policy defines the rules for ordering. The most widely used policy is the **(s, S)** policy:

- **s** – reorder point: when inventory falls to or below **s**, an order is placed.
- **S** – order‑up‑to level: the order quantity is $S - \text{current inventory}$.

### 2.3 Service Levels

Two common service level measures:

| Type | Description |
|------|-------------|
| **Type I (α)** | Probability that no stockout occurs during a replenishment cycle. |
| **Type II (β)** | Fill rate: proportion of demand satisfied from available stock. |

### 2.4 Cost Components

| Cost | Symbol | Description |
|------|--------|-------------|
| Holding cost | $h$ | Cost per unit held per time unit (warehousing, insurance, obsolescence). Typically 20‑30% of product value. |
| Ordering cost | $K$ | Fixed cost per order (administrative, transportation). |
| Lost sales cost | $\ell$ | Penalty per unit of lost demand. It includes lost profit and reputational damage. |

**Lost sales cost estimation:**

$$
\ell = \varepsilon \, \bar{v} \, d, \qquad (3.1.2)
$$

where:
- $\varepsilon \ge 1$ is a penalty multiplier,
- $\bar{v}$ is the average daily sales,
- $d$ is the average lead time in days.

---

## 3. Stochastic Processes for Inventory Modelling

### 3.1 Birth‑Death Processes

A **birth‑death process** is a continuous‑time Markov chain on non‑negative integers where only transitions to neighbouring states occur. In inventory systems:

- **Births** = customer arrivals (demand),
- **Deaths** = service completions (inventory consumption).

**Assumptions:**
1. Given $N(t) = n$, the time to the next birth is exponential with rate $\lambda_n$.
2. Given $N(t) = n$, the time to the next death is exponential with rate $\mu_n$.
3. Birth and death events are mutually independent.

### 3.2 Quasi‑Birth‑Death (QBD) Processes

A QBD process extends the birth‑death model to a two‑dimensional state space:

$$
S = \{(i, j) : i \ge 0,\; j = 0, 1, \ldots, m\}
$$

where:
- $i$ = **level** (e.g., number of customers in the system),
- $j$ = **phase** (e.g., inventory level).

Level transitions are restricted to nearest neighbours, while phase transitions can be arbitrary. This structure is ideal for queueing‑inventory systems, where the inventory level acts as the phase.

---

## 4. Queueing Theory with Attached Inventory

### 4.1 Basic Queueing System

A **queueing system** models waiting phenomena and provides performance measures such as queue length, waiting time, and utilisation.

**Kendall‑Lee notation:** $(a/b/c)(d/e/f)$

| Symbol | Description |
|--------|-------------|
| $a$ | Arrival distribution (e.g., M = exponential, D = deterministic, G = general) |
| $b$ | Service time distribution |
| $c$ | Number of servers |
| $d$ | Queue discipline (FCFS, LCFS, SIRO, PR, GD) |
| $e$ | System capacity (max customers) |
| $f$ | Customer population size |

**Steady‑state performance measures:**

| Measure | Symbol | Formula |
|---------|--------|---------|
| Average arrival rate | $\bar{\lambda}$ | $\bar{\lambda} = \sum_{n=0}^{N} \lambda_n P_n$ |
| Server utilisation | $\rho$ | $\rho = \frac{\bar{\lambda}}{S\mu}$ |
| Expected queue length | $L_q$ | $L_q = \sum_{n=S}^{N} (n - S)P_n$ |
| Expected customers in system | $L$ | $L = L_q + S\rho$ |

### 4.2 Queueing‑Inventory Model (Yue et al., 2018)

We consider a system where:
- Customers arrive according to a Poisson process with rate $\lambda$.
- Service times are exponential with rate $\mu$ (single server, FCFS).
- Each customer demands a random number of units following a **geometric distribution**:
  $$
  p_n = P(X = n) = p(1-p)^{n-1}, \quad n = 1, 2, \ldots, S. \qquad (3.3.5)
  $$
- Inventory is managed under an **(s, S)** policy.
- Replenishment lead time is exponential with rate $\nu$.
- Demand that cannot be fulfilled is lost (lost sales, possibly partial).

The system is a QBD process $\{N(t), Y(t)\}$, where:
- $N(t)$ = number of customers in the system,
- $Y(t)$ = inventory level (0, 1, …, S).

**Stationary distribution:**  
For $\rho = \lambda/\mu < 1$, the joint distribution factors as:

$$
\pi_n = (1 - \rho) \rho^n \, \mathbf{x}, \qquad n \ge 0, \qquad (3.3.6)
$$

where $\mathbf{x} = (x_0, x_1, \ldots, x_S)$ is the stationary distribution of the inventory process, given by:

$$
x_i = \begin{cases}
\displaystyle \frac{\lambda}{\nu} \left( \frac{\lambda p}{\lambda + \nu} + q \right)^s x_S, & i = 0, \\[1.2ex]
\displaystyle \frac{\lambda p}{\lambda + \nu} \left( \frac{\lambda p}{\lambda + \nu} + q \right)^{s-i} x_S, & 1 \le i \le s, \\[1.2ex]
p \, x_S, & s+1 \le i \le S-1,
\end{cases} \qquad (3.3.7)
$$

with

$$
x_S = \frac{1}{(S - s - 1)p + \frac{\lambda}{\nu} + 1}. \qquad (3.3.8)
$$

Here, $q = 1-p$.

**Performance measures:**

| Measure | Symbol | Formula |
|---------|--------|---------|
| Expected customers in system | $L$ | $L = \frac{\lambda}{\mu - \lambda}$ |
| Customer loss rate | $V^c$ | $V^c = \lambda x_0$ |
| Expected inventory level | $I$ | $I = \sum_{i=1}^{S} i x_i$ |
| Replenishment rate | $R$ | $R = \nu \sum_{i=0}^{S} x_i$ |
| Expected lost sales (units) | $V^d$ | $V^d = \frac{1}{p} \left( \lambda x_0 + \mu \sum_{i=1}^{S} q^i x_i \right)$ |

**Total cost function:**

$$
F(s, S) = \omega L + h I + K R + \ell V^d, \qquad (3.3.14)
$$

where:
- $\omega$ = waiting cost per customer per time unit,
- $h$ = holding cost per unit per time unit,
- $K$ = fixed ordering cost,
- $\ell$ = lost sales cost per unit.

**Service level (fill rate):**

$$
\beta = 1 - \frac{\lambda}{(S - s)\nu + \lambda} \left( \frac{\lambda}{\lambda + \nu} \right)^s. \qquad (3.3.15)
$$

---


## 6. Python Implementation

The following Python code implements the theoretical model, including the stationary distribution, performance measures, cost function, and numerical optimisation of the (s, S) policy. A chi‑square test function is also provided.


📄 **[View the full code on GitHub] (https://github.com/GamexIan/SkoltechGamez/blob/529a0b5194a1ccc13af56b3fbd661e6e4e7f1d62/level.py)**


📄 **[View the full code on GitHub] (https://github.com/GamexIan/SkoltechGamez/blob/d1d266a7e73082e637cb15c2d023a0626a4fedff/sales.py)**


#  Air Quality Data Imputation Tool

This  Python script designed to **reconstruct missing daily ozone (O₃) concentration records** from environmental monitoring stations. It uses a hybrid approach that combines **cross-station linear regression** with **temporal interpolation** to generate a complete, reliable time series for air quality analysis.

📄 **[View the full code on GitHub] ()**

Air quality datasets in Puebla suffer from missing values due to sensor malfunctions or communication failures. This script fills gaps in the **"AGUA SANTA"** ozone monitoring station by leveraging:
1.  **Statistical correlation** with a nearby station **"NINFAS"** (Regression Imputation).
2.  **Temporal continuity** (Linear Interpolation & forward/backward filling).



The script reads all sheets from an Excel file (`Base de datos O3 para Nian.xlsx`), extracts the required columns (`Dia`, `AGUA SANTA O3 (ppm) Promedio Diario`, and `NINFAS O3 (ppm) Promedio Diario`), and filters the data to the 2021–2025 period.

```python
df_temp['fecha'] = pd.to_datetime(df_temp['fecha'], errors='coerce')
df_temp = df_temp[df_temp['fecha'].dt.year.between(2021, 2025)]
```

 The script identifies days where **both** stations have valid data and trains a linear regression model to predict *AGUA SANTA* using *NINFAS*.

```python
X = df_complete[['ninfas']].values
y = df_complete['agua_santa'].values
reg = LinearRegression().fit(X, y)
```

The model finds the best-fit line:  
\[
y = \beta_0 + \beta_1 \cdot x + \varepsilon
\]
Where:
- \(y\) = AGUA SANTA concentration  
- \(x\) = NINFAS concentration  

Using **Ordinary Least Squares (OLS)** , the coefficients are calculated as:  
\[
\beta_1 = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sum (x_i - \bar{x})^2}, \quad \beta_0 = \bar{y} - \beta_1 \bar{x}
\]

For days where *AGUA SANTA* is missing but *NINFAS* is available, the model predicts the missing value:
```python
df_all.loc[mask_faltan_agua, 'agua_santa_imputed'] = reg.predict(X_pred)
```

The script prints the resulting equation (e.g., `agua_santa = 0.85 * ninfas + 0.02`) and the \(R^2\) score, indicating the strength of the relationship.

###  Temporal Interpolation & Edge Filling
After regression, there may still be gaps (days where *both* stations lack data). The script applies **linear interpolation** across time to fill these internal gaps.

```python
serie_interp = serie.interpolate(method='linear', limit_area=None)
serie_interp = serie_interp.ffill().bfill()
```

📐 **(Linear Interpolation)**:
If two valid measurements exist at times \(t_0\) and \(t_1\) with values \(y_0\) and \(y_1\), the value at an intermediate time \(t\) is estimated as:  
\[
y(t) = y_0 + (y_1 - y_0) \cdot \frac{t - t_0}{t_1 - t_0}
\]

*Edge Handling*:
- `.ffill()` (Forward Fill) propagates the **last valid observation** forward to fill trailing gaps.
- `.bfill()` (Backward Fill) propagates the **next valid observation** backward to fill leading gaps.





