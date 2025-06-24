import pandas as pd
import json
import matplotlib.pyplot as plt

LOG_PATH = '/var/log/jetson_breathline.jsonl'

def load_jsonl(path):
    records = []
    with open(path, 'r') as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                records.append(data)
            except json.JSONDecodeError:
                continue
    if not records:
        print("No valid JSON records found.")
        return pd.DataFrame()
    df = pd.DataFrame(records)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    return df

def plot_environment(df):
    fig, ax = plt.subplots(figsize=(12, 6))
    df[['ambient_temp', 'humidity', 'voc_level', 'light_level']].plot(ax=ax)
    ax.set_title("Ambient Environment Over Time")
    ax.set_ylabel("Sensor Readings")
    ax.set_xlabel("Time")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("breathline_plot.png")

if __name__ == '__main__':
    df = load_jsonl(LOG_PATH)
    if df.empty:
        print("No data found in log.")
    else:
        print(df.head())
        plot_environment(df)

