import streamlit as st
import pandas as pd
import pickle

st.set_page_config(page_title = "EV Battery QA", layout="wide")

st.header("Project - Find Type of Defect in Battery")

col1, col2 = st.columns(2)

with col1:
        shift = st.selectbox("Shift", ["Morning", "Evening", "Night"])
        supervisor = st.text_input("Supervisor Name")
        amb_temp = st.number_input("Ambient Temperature", value = 20.00, step=2.00)
        anode_overhang = st.number_input("Anode Overhang (in mm)", value = 0.50, step=0.10)


with col2:
        electrolyte = st.number_input("Electrolyte Volume (ml)", value = 15.00, step=0.50)
        i_r = st.number_input("Internal Resistance (mOhm)", value = 15.00, step=0.50)
        Capacity = st.number_input("Capacity (mAh)", value = 4000.00, step=200.00)
        r_c = st.number_input("Retention Cycle", value = 100.00, step=2.00)



mapping = {"Morning": 3, "Evening": 1, "Night": 2}
mt_val = mapping.get(shift, 0)  


if st.button("submit"):
        input_data = pd.DataFrame({
                "Shift": [mt_val],
                "Ambient_Temp_C": [amb_temp],
                "Anode_Overhang_mm": [anode_overhang],
                "Electrolyte_Volume_ml": [electrolyte],
                "Internal_Resistance_mOhm": [i_r],
                "Capacity_mAh": [Capacity],
                "Retention_50Cycle_Pct": [r_c]
        })

        with open("EV_Battery_QA_ML_Model(C).pkl", "rb") as f:
                FinalModel = pickle.load(f)

        defect = int(FinalModel.predict(input_data)[0])

        mapping_1 = {0: 'Critical Resistance', 1: 'High Internal Resistance', 2: 'Low Capacity', 3: 'None', 4: 'Poor Retention',
                      5: 'Severe Capacity Fade', 6: 'Short Circuit Risk (Overhang)'}
        defect_map = mapping_1.get(defect,0)

st.divider()

try:
    st.success(f"Predicted Defect: **{defect_map}**")
except:
    pass