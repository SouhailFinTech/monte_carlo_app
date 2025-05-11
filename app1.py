import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Titre
st.title("📈 Simulation Monte Carlo du Prix d'une Action")

# Sidebar inputs
st.sidebar.header("Paramètres de simulation")
S0 = st.sidebar.number_input("Prix initial (S0)", value=100.0)
mu = st.sidebar.slider("Rendement attendu (mu)", min_value=-0.1, max_value=0.2, value=0.05, step=0.005)
sigma = st.sidebar.slider("Volatilité (sigma)", min_value=0.01, max_value=0.5, value=0.2, step=0.01)
T = st.sidebar.number_input("Nombre de jours de trading", value=252*2)
N = st.sidebar.slider("Nombre de simulations", min_value=100, max_value=5000, value=1000, step=100)

# Simulation Monte Carlo
dt = 1/252
price_paths = np.zeros((int(T), N))
price_paths[0] = S0

for t in range(1, int(T)):
    z = np.random.standard_normal(N)
    price_paths[t] = price_paths[t-1] * np.exp((mu - 0.5 * sigma**2)*dt + sigma*np.sqrt(dt)*z)

# Résultats
final_prices = price_paths[-1]
expected_price = np.mean(final_prices)
var_95 = np.percentile(final_prices, 5)

# Graphique des trajectoires
st.subheader("Trajectoires simulées du prix")
fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(price_paths[:, :100], alpha=0.3)
ax1.set_xlabel("Jours")
ax1.set_ylabel("Prix")
st.pyplot(fig1)

# Histogramme des prix finaux
st.subheader("Distribution des prix au terme de la période")
fig2, ax2 = plt.subplots()
ax2.hist(final_prices, bins=50, alpha=0.7, color="skyblue")
ax2.axvline(expected_price, color='red', linestyle='--', label=f"Prix moyen : {expected_price:.2f}")
ax2.axvline(var_95, color='orange', linestyle='--', label=f"VaR 95% : {var_95:.2f}")
ax2.legend()
st.pyplot(fig2)

# Stats
st.markdown("### 📊 Résumé des résultats")
st.markdown(f"- **Prix moyen estimé à la fin :** {expected_price:.2f}")
st.markdown(f"- **Valeur à Risque (VaR 95%) :** {var_95:.2f}")
st.markdown(f"- **Prix minimal observé :** {np.min(final_prices):.2f}")
st.markdown(f"- **Prix maximal observé :** {np.max(final_prices):.2f}")