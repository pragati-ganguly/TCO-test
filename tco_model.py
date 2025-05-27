import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Title
st.title('TCO Parity Model: Diesel vs Electric Vehicles')

# Sidebar inputs
st.sidebar.header('Vehicle Parameters')

# Vehicle prices
diesel_price = st.sidebar.number_input('Diesel Vehicle Price (CAD)', value=30000)
electric_price = st.sidebar.number_input('Electric Vehicle Price (CAD)', value=40000)

# Fuel and electricity costs
diesel_fuel_cost = st.sidebar.number_input('Diesel Fuel Cost (CAD/L)', value=1.5)
electricity_cost = st.sidebar.number_input('Electricity Cost (CAD/kWh)', value=0.13)

# Maintenance costs
diesel_maintenance = st.sidebar.number_input('Diesel Maintenance Cost (CAD/year)', value=1000)
electric_maintenance = st.sidebar.number_input('Electric Maintenance Cost (CAD/year)', value=500)

# Annual mileage
annual_mileage = st.sidebar.number_input('Annual Mileage (km)', value=15000)

# Efficiency
diesel_efficiency = st.sidebar.number_input('Diesel Efficiency (km/L)', value=15)
electric_efficiency = st.sidebar.number_input('Electric Efficiency (km/kWh)', value=6)

# Ownership duration
ownership_years = st.sidebar.slider('Ownership Duration (years)', 1, 20, value=10)

# Calculate TCO
years = np.arange(1, ownership_years + 1)
diesel_tco = diesel_price + (years * (annual_mileage / diesel_efficiency * diesel_fuel_cost + diesel_maintenance))
electric_tco = electric_price + (years * (annual_mileage / electric_efficiency * electricity_cost + electric_maintenance))

# Find break-even point
break_even_year = np.where(diesel_tco <= electric_tco)[0]
if len(break_even_year) > 0:
    break_even_year = break_even_year[0] + 1
else:
    break_even_year = 'Never'

# Plot TCO comparison
fig, ax = plt.subplots()
ax.plot(years, diesel_tco, label='Diesel TCO', marker='o')
ax.plot(years, electric_tco, label='Electric TCO', marker='o')
ax.axvline(x=break_even_year, color='r', linestyle='--', label=f'Break-even Year: {break_even_year}')
ax.set_xlabel('Years')
ax.set_ylabel('Total Cost of Ownership (CAD)')
ax.set_title('TCO Comparison: Diesel vs Electric Vehicles')
ax.legend()
ax.grid(True)

# Display results
st.pyplot(fig)
st.write(f'### Break-even Year: {break_even_year}')
st.write('### TCO Details')
tco_data = pd.DataFrame({
    'Year': years,
    'Diesel TCO (CAD)': diesel_tco,
    'Electric TCO (CAD)': electric_tco
})
st.write(tco_data)

