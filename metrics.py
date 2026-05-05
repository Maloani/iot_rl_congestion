def calculate_metrics(data):
    return {
        "throughput": data["throughput"],
        "latency": data["latency"],
        "packet_loss": data["loss"],
        "energy": data["energy"]
    }