import matplotlib.pyplot as plt

def plot_results(results):
    metrics = ["throughput", "latency", "loss", "energy"]

    for m in metrics:
        plt.figure()
        values = [results[k][m] for k in results]
        plt.bar(results.keys(), values)
        plt.title(m.upper())
        plt.savefig(f"{m}.png")  # export IEEE
        plt.close()

def plot_learning_curve(rewards):
    plt.figure()
    plt.plot(rewards)
    plt.title("Learning Curve (Reward vs Episodes)")
    plt.xlabel("Episodes")
    plt.ylabel("Reward")
    plt.savefig("learning_curve.png")
    plt.close()