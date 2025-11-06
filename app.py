from flask import Flask, render_template, jsonify, send_file
import paho.mqtt.client as mqtt
import matplotlib
matplotlib.use("Agg")  # backend para servidores
import matplotlib.pyplot as plt
import seaborn as sns
import json
import io

app = Flask(__name__)

# VARIÁVEIS DO PLACAR
dados_placar = {
    "TimeA": 0,
    "TimeB": 0,
    "Data": ""
}

# CALLBACKS MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao broker MQTT!")
        client.subscribe("/TEF/placar001/attrs")
    else:
        print(f"Erro ao conectar MQTT: {rc}")

def on_message(client, userdata, msg):
    global dados_placar
    payload = msg.payload.decode().strip()
    print(f"MQTT Recebido: {payload}")
    try:
        data = json.loads(payload)
        dados_placar["TimeA"] = int(data.get("TimeA", dados_placar["TimeA"]) or 0)
        dados_placar["TimeB"] = int(data.get("TimeB", dados_placar["TimeB"]) or 0)
        dados_placar["Data"] = data.get("Data", dados_placar["Data"])
    except Exception as e:
        print(f"JSON inválido: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect("52.86.16.147", 1883, 60)
    client.loop_start()
    print("Esperando mensagens MQTT...")
except Exception as e:
    print(f"ERRO ao conectar ao broker: {e}")

@app.route("/grafico")
def grafico():
    try:
        plt.style.use('dark_background')
        sns.set_style("darkgrid", {"axes.facecolor": "#1f1f1f", "grid.color": "#2c2c2c"})

        fig, ax = plt.subplots(figsize=(10, 6))

        times = ["Time A", "Time B"]
        gols = [
            int(dados_placar.get("TimeA", 0) or 0),
            int(dados_placar.get("TimeB", 0) or 0)
        ]

        colors = ['#4CAF50', '#F44336']
        sns.barplot(x=gols, y=times, ax=ax, palette=colors, orient='h')

        ax.set_title("Gols por Time", fontsize=18, fontweight='bold', color='#e0e0e0')
        ax.set_xlabel("Número de Gols", fontsize=12, color='#a0a0a0')
        ax.set_ylabel("")
        ax.tick_params(axis='x', colors='#a0a0a0')
        ax.tick_params(axis='y', colors='#e0e0e0')

        for i, v in enumerate(gols):
            ax.text(v + 0.5, i, str(v), color='#e0e0e0', ha='left', va='center', fontsize=12, fontweight='bold')

        sns.despine(left=True, bottom=True)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('#2c2c2c')
        ax.spines['left'].set_color('#2c2c2c')

        plt.tight_layout()

        img = io.BytesIO()
        plt.savefig(img, format="png", transparent=True, bbox_inches="tight", dpi=180)
        img.seek(0)
        plt.close(fig)

        return send_file(img, mimetype="image/png")

    except Exception as e:
        print(f"ERRO ao gerar gráfico: {e}")
        return "Erro ao gerar gráfico", 500

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dados")
def dados():
    return jsonify(dados_placar)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
