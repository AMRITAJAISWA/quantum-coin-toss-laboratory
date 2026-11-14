import streamlit as st
import matplotlib.pyplot as plt
import csv
import io

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Quantum Coin Toss Laboratory",
    page_icon="🪙",
    layout="wide"
)


# ==========================================
# CUSTOM CSS - DARK BLUE THEME
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #0b1120;
    color: #e2e8f0;
}

[data-testid="stSidebar"] {
    background-color: #111c33;
}

h1, h2, h3 {
    color: #60a5fa !important;
}

p, label {
    color: #cbd5e1;
}

.metric-card {
    background: #172554;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #2563eb;
    text-align: center;
}

.metric-title {
    color: #93c5fd;
    font-size: 16px;
}

.metric-value {
    color: #ffffff;
    font-size: 32px;
    font-weight: bold;
}

.section-card {
    background: #111c33;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #334155;
    margin-bottom: 15px;
}

.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    border: none;
    height: 48px;
    font-weight: bold;
    width: 100%;
}

.stButton > button:hover {
    background-color: #1d4ed8;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# HEADER
# ==========================================

st.title("🪙 Quantum Coin Toss Laboratory")

st.markdown("""
### Quantum Computing | Superposition | Probability Analysis

An interactive laboratory demonstrating quantum
superposition and measurement using Qiskit.
""")

st.divider()


# ==========================================
# QUANTUM CIRCUIT FUNCTION
# ==========================================

def quantum_coin_toss(number_of_tosses):

    circuit = QuantumCircuit(1, 1)

    # Apply Hadamard gate
    circuit.h(0)

    # Measure the qubit
    circuit.measure(0, 0)

    # Create simulator
    simulator = AerSimulator()

    # Compile circuit
    compiled_circuit = transpile(circuit, simulator)

    # Execute experiment and retain individual results
    job = simulator.run(
        compiled_circuit,
        shots=number_of_tosses,
        memory=True
    )

    result = job.result()

    # Get individual measurement outcomes
    outcomes = result.get_memory()

    heads = outcomes.count('0')
    tails = outcomes.count('1')

    return heads, tails, outcomes, circuit


# ==========================================
# SIDEBAR SETTINGS
# ==========================================

st.sidebar.title("⚙️ Experiment Settings")

st.sidebar.markdown("---")

number_of_tosses = st.sidebar.selectbox(
    "Select Number of Tosses",
    [1, 10, 50, 100, 500],
    index=3
)

st.sidebar.markdown("---")

st.sidebar.info("""
**Quantum Experiment**

Each experiment uses:

• 1 Qubit

• Hadamard Gate

• Quantum Measurement

• Qiskit Aer Simulator
""")

st.sidebar.markdown("---")

st.sidebar.caption(
    "Quantum Coin Toss and Probability Laboratory"
)


# ==========================================
# SUPERPOSITION SECTION
# ==========================================

st.header("01 | Quantum Superposition")

st.markdown("""
A qubit initially starts in state |0⟩.
The Hadamard gate creates an equal superposition
of the states |0⟩ and |1⟩.
""")

st.latex(
    r"|\psi\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}"
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Heads Probability</div>
        <div class="metric-value">50%</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Tails Probability</div>
        <div class="metric-value">50%</div>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# QUANTUM EXPERIMENT
# ==========================================

st.divider()

st.header("02 | Quantum Coin Toss")

st.write(
    f"Selected experiment size: **{number_of_tosses} tosses**"
)

if st.button("🚀 START QUANTUM EXPERIMENT"):

    with st.spinner("Running quantum simulation..."):

        heads, tails, outcomes, circuit = quantum_coin_toss(
            number_of_tosses
        )

        st.session_state["heads"] = heads
        st.session_state["tails"] = tails
        st.session_state["outcomes"] = outcomes
        st.session_state["total"] = number_of_tosses
        st.session_state["circuit"] = circuit.draw(
            output="text"
        )

    st.success("Quantum experiment completed successfully!")


# ==========================================
# RESULTS SECTION
# ==========================================

if "heads" in st.session_state:

    heads = st.session_state["heads"]
    tails = st.session_state["tails"]
    total = st.session_state["total"]

    outcomes = st.session_state["outcomes"]

    heads_probability = heads / total * 100
    tails_probability = tails / total * 100

    st.divider()

    st.header("03 | Experiment Results")

    # Result cards

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Tosses</div>
            <div class="metric-value">{total}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">🟢 Heads</div>
            <div class="metric-value">{heads}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">🔵 Tails</div>
            <div class="metric-value">{tails}</div>
        </div>
        """, unsafe_allow_html=True)


    # ======================================
    # PROBABILITY ANALYSIS
    # ======================================

    st.divider()

    st.header("04 | Probability Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Experimental Heads Probability",
            f"{heads_probability:.2f}%"
        )

        st.metric(
            "Theoretical Heads Probability",
            "50%"
        )

    with col2:
        st.metric(
            "Experimental Tails Probability",
            f"{tails_probability:.2f}%"
        )

        st.metric(
            "Theoretical Tails Probability",
            "50%"
        )

    st.caption(
        "Experimental probability may differ from theoretical "
        "probability due to random quantum measurement."
    )


    # ======================================
    # GRAPHICAL REPRESENTATION
    # ======================================

    st.divider()

    st.header("05 | Probability Visualization")

    fig, ax = plt.subplots(figsize=(8, 4))

    fig.patch.set_facecolor("#111c33")
    ax.set_facecolor("#111c33")

    categories = ["Heads", "Tails"]

    probabilities = [
        heads_probability,
        tails_probability
    ]

    bars = ax.bar(
        categories,
        probabilities,
        color=["#38bdf8", "#818cf8"],
        width=0.5
    )

    ax.set_ylim(0, 100)

    ax.set_ylabel(
        "Probability (%)",
        color="white"
    )

    ax.set_title(
        "Quantum Measurement Distribution",
        color="white"
    )

    ax.tick_params(colors="white")

    for spine in ax.spines.values():
        spine.set_color("#475569")

    ax.axhline(
        50,
        color="#facc15",
        linestyle="--",
        label="Theoretical Probability (50%)"
    )

    ax.legend(
        facecolor="#172554",
        labelcolor="white"
    )

    for bar in bars:

        height = bar.get_height()

        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 2,
            f"{height:.1f}%",
            ha="center",
            color="white"
        )

    st.pyplot(fig)

    plt.close(fig)


    # ======================================
    # INDIVIDUAL TOSS RESULTS
    # ======================================

    st.divider()

    st.header("06 | Individual Toss Results")

    display_data = []

    for index, outcome in enumerate(outcomes, start=1):

        display_data.append({
            "Toss Number": index,
            "Quantum Measurement": outcome,
            "Coin Result": "Heads" if outcome == "0" else "Tails"
        })

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )


    # ======================================
    # DOWNLOAD RESULTS
    # ======================================

    csv_buffer = io.StringIO()

    writer = csv.DictWriter(
        csv_buffer,
        fieldnames=[
            "Toss Number",
            "Quantum Measurement",
            "Coin Result"
        ]
    )

    writer.writeheader()
    writer.writerows(display_data)

    st.download_button(
        label="📥 Download Experiment Results",
        data=csv_buffer.getvalue(),
        file_name="quantum_coin_toss_results.csv",
        mime="text/csv"
    )


    # ======================================
    # QUANTUM CIRCUIT
    # ======================================

    st.divider()

    st.header("07 | Quantum Circuit")

    st.markdown("""
    Our circuit uses a Hadamard gate followed by
    a measurement operation.
    """)

    st.code(
        st.session_state["circuit"],
        language="text"
    )


# ==========================================
# LEARNING SECTION
# ==========================================

st.divider()

st.header("08 | Quantum Learning Centre")

with st.expander("What is a Qubit?"):

    st.write("""
    A qubit is the basic unit of quantum information.

    It can exist in a superposition of the basis states
    |0⟩ and |1⟩.
    """)

with st.expander("What is a Hadamard Gate?"):

    st.write("""
    A Hadamard gate is a quantum logic gate.

    When applied to the initial state |0⟩,
    it creates an equal superposition of |0⟩ and |1⟩.
    """)

with st.expander("What is Quantum Measurement?"):

    st.write("""
    Quantum measurement produces a definite result.

    In our experiment, the result is either 0 or 1.
    We represent these results as Heads and Tails.
    """)


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown("""
<div style="text-align:center; color:#94a3b8;">

<h4>Quantum Coin Toss and Probability Laboratory</h4>

Developed using Python | Qiskit | Qiskit Aer | Streamlit

Academic Quantum Computing Project

</div>
""", unsafe_allow_html=True)