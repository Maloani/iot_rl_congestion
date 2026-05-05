from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from simulation import run_simulation
from charts.plot import plot_results, plot_learning_curve
from utils.export import export_results

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("🚀 IoT AI Dashboard IEEE PRO")
        self.setGeometry(100, 50, 1100, 700)

        # 🎨 STYLE GLOBAL
        self.setStyleSheet("""
        QWidget {
            background-color: #0f0f1a;
            color: white;
        }

        QLabel {
            color: white;
        }

        QPushButton {
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            border-radius: 8px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #45a049;
        }
        """)

        main_layout = QVBoxLayout()

        # 🏷️ TITLE
        title = QLabel("🚀 IoT AI Congestion Dashboard (IEEE PRO)")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        main_layout.addWidget(title)

        # 📊 KPI SECTION
        self.kpi_layout = QHBoxLayout()
        self.kpis = {}

        metrics = ["Throughput", "Latency", "Loss", "Energy"]

        for metric in metrics:
            card = QLabel(f"{metric}\n0")
            card.setAlignment(Qt.AlignCenter)
            card.setFixedHeight(100)

            card.setStyleSheet("""
                background-color: #1e1e2f;
                border-radius: 15px;
                font-size: 18px;
                font-weight: bold;
            """)

            self.kpis[metric.lower()] = card
            self.kpi_layout.addWidget(card)

        main_layout.addLayout(self.kpi_layout)

        # 🔘 BUTTONS
        btn_layout = QHBoxLayout()

        self.btn_run = QPushButton("▶ Run AI Simulation")
        self.btn_run.clicked.connect(self.run_simulation)

        self.btn_graph = QPushButton("📊 Show Graphs")
        self.btn_graph.clicked.connect(self.show_graphs)

        btn_layout.addWidget(self.btn_run)
        btn_layout.addWidget(self.btn_graph)

        main_layout.addLayout(btn_layout)

        # 📈 GRAPH AREA (INTEGRATED)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)

        # 🌍 MAP SECTION
        self.map = QTextEdit()
        self.map.setText("📡 IoT Map (Simulated)\nNode1: Active\nNode2: Active")
        self.map.setStyleSheet("""
            background-color: #1e1e2f;
            border-radius: 10px;
            padding: 10px;
        """)
        main_layout.addWidget(self.map)

        self.setLayout(main_layout)

        self.results = None

    # 🧠 RUN SIMULATION
    def run_simulation(self):
        self.results = run_simulation()

        # Export pour publication IEEE
        export_results(self.results)

        rl = self.results["RL (DQN)"]

        self.update_kpi("throughput", rl["throughput"])
        self.update_kpi("latency", rl["latency"], reverse=True)
        self.update_kpi("loss", rl["loss"], reverse=True)
        self.update_kpi("energy", rl["energy"], reverse=True)

        self.draw_graph()

        # 📊 Courbe d’apprentissage RL
        if "rewards" in rl:
            plot_learning_curve(rl["rewards"])

    # 🎨 KPI COLOR LOGIC
    def update_kpi(self, key, value, reverse=False):
        # logique couleur intelligente
        if reverse:
            color = "#4CAF50" if value < 60 else "#ff4c60"
        else:
            color = "#4CAF50" if value > 6 else "#ff4c60"

        self.kpis[key].setText(f"{key.capitalize()}\n{value:.2f}")
        self.kpis[key].setStyleSheet(f"""
            background-color: #1e1e2f;
            border-radius: 15px;
            font-size: 18px;
            font-weight: bold;
            color: {color};
        """)

    # 📊 GRAPH INSIDE DASHBOARD
    def draw_graph(self):
        self.figure.clear()

        methods = list(self.results.keys())

        throughput = [self.results[m]["throughput"] for m in methods]
        latency = [self.results[m]["latency"] for m in methods]
        loss = [self.results[m]["loss"] for m in methods]

        ax = self.figure.add_subplot(111)

        ax.bar(methods, throughput, label="Throughput")
        ax.plot(methods, latency, marker='o', label="Latency")
        ax.plot(methods, loss, marker='x', label="Loss")

        ax.set_title("Performance Comparison (IEEE)")
        ax.set_ylabel("Values")
        ax.legend()

        self.canvas.draw()

    # 📈 POPUP GRAPH (OPTIONAL)
    def show_graphs(self):
        if self.results is None:
            QMessageBox.warning(self, "Error", "Run simulation first")
            return

        plot_results(self.results)