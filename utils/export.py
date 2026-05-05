import csv

def export_results(results):
    with open("results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Method", "Throughput", "Latency", "Loss", "Energy"])

        for method, vals in results.items():
            writer.writerow([
                method,
                vals["throughput"],
                vals["latency"],
                vals["loss"],
                vals["energy"]
            ])