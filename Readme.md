# 🏆 Placar de Jogo Conectado — ESP32 + MQTT + LCD I2C

> Projeto desenvolvido por alunos da **FIAP** como parte das atividades de **IoT & Sistemas Embarcados**, integrando hardware e nuvem via **protocolo MQTT**.  
> O sistema simula um **placar digital inteligente**, capaz de se comunicar com um **broker MQTT** e um **aplicativo móvel (MyMQTT)** para atualização remota de resultados esportivos em tempo real.

---

## 👨‍💻 Integrantes

| RM      | Nome Completo           |
|----------|------------------------|
| 562142   | Luiz Antonio Morais     |
| 561997   | Nicolas Barnabe         |
| 561459   | Kevin Venancio          |
| 561568   | Guilherme Moura         |

---

## 🎯 Objetivo do Projeto

O projeto tem como objetivo demonstrar a integração entre o **ESP32**, o **protocolo MQTT** e o **display LCD I2C**, simulando um **placar eletrônico conectado à Internet**.  
Ele permite registrar gols localmente através de **botões físicos** ou remotamente via **aplicativo MQTT**, exibindo as informações no **display LCD** e publicando os dados em tempo real na **nuvem (broker MQTT)**.

---

## ⚙️ Funcionalidades Principais

✅ Conexão automática ao **Wi-Fi (Wokwi-GUEST)**  
✅ Comunicação com **broker MQTT** (IP: `52.86.16.147`)  
✅ **Publicação e recebimento** de mensagens MQTT  
✅ Exibição dos dados no **LCD I2C (16x2)**  
✅ Controle por **botões físicos** (para simular gols)  
✅ **LEDs** e **buzzer** para alertas visuais e sonoros  
✅ Envio automático de **timestamp (data/hora NTP)** nas publicações  

---

## 🧩 Diagrama Lógico — Conexões

| Componente  | Pino ESP32 | Função                    |
|--------------|------------|---------------------------|
| Botão Time A | GPIO 14    | Incrementa gols Time A    |
| Botão Time B | GPIO 27    | Incrementa gols Time B    |
| LED Time A   | GPIO 12    | Indicação de gol do Time A|
| LED Time B   | GPIO 13    | Indicação de gol do Time B|
| Buzzer       | GPIO 26    | Alerta sonoro             |
| LCD I2C SDA  | GPIO 21    | Comunicação I2C           |
| LCD I2C SCL  | GPIO 22    | Comunicação I2C           |

## 📸 Simução Wokwi

[<img width="724" height="502" alt="image" src="https://github.com/user-attachments/assets/0ca11918-ac7b-4d43-aa4c-e28d02986c54" />]

---

## 🌐 Comunicação MQTT

- **Broker:** `52.86.16.147`  
- **Porta:** `1883`  
- **Tópico para Receber Comandos:** `/TEF/placar001/cmd`  
- **Tópico para Publicar Placar:** `/TEF/placar001/attrs`

### 📤 Comandos Aceitos via MyMQTT:
| Comando MQTT | Função Executada            |
|---------------|----------------------------|
| `golA`        | Incrementa gols do Time A  |
| `golB`        | Incrementa gols do Time B  |
| `reset`       | Zera o placar              |

📸 **[INSERIR AQUI IMAGEM 2: Print do aplicativo MyMQTT enviando e recebendo mensagens]**

---

## 🧩 Execução no Wokwi

🔗 **Link do projeto no Wokwi:**  
👉 [https://wokwi.com/projects/446825400114712577](https://wokwi.com/projects/446825400114712577)

### Passo a passo para simular:
1. Acesse o link acima e clique em **"Start Simulation"**.  
2. Aguarde o ESP32 conectar ao **Wi-Fi simulado** e ao **broker MQTT**.  
3. O **LCD** exibirá o placar inicial (`Time A: 0 / Time B: 0`).  
4. Pressione os **botões físicos** para registrar gols.  
5. Observe o **buzzer** e os **LEDs** piscando a cada gol.  
6. No **Serial Monitor**, acompanhe as mensagens publicadas no broker MQTT.

📸 **[INSERIR AQUI IMAGEM 3: Simulação rodando no Wokwi com o LCD mostrando o placar]**

---

## 📱 Conectando o Aplicativo MyMQTT

1. Instale o aplicativo **MyMQTT** (Android).  
2. Configure a conexão com o broker:
   - **Host:** `52.86.16.147`  
   - **Porta:** `1883`  
   - **Client ID:** `placar001`
3. Em **Subscribe**, adicione o tópico:
/TEF/placar001/attrs

markdown
Copiar código
→ Receberá as atualizações de placar.
4. Em **Publish**, envie comandos no tópico:
/TEF/placar001/cmd

yaml
Copiar código
→ Envie `golA`, `golB` ou `reset`.

📸 **[INSERIR AQUI IMAGEM 4: Print do app MyMQTT recebendo atualizações do placar]**

---

## 🧠 EXPLICAÇÃO DETALHADA DO CÓDIGO-FONTE

### 🔹 Cabeçalho e Bibliotecas
```cpp
#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include "time.h"
Essas bibliotecas habilitam:

WiFi.h → Conexão do ESP32 à rede Wi-Fi.

PubSubClient.h → Comunicação MQTT (publicação e assinatura de tópicos).

Wire.h e LiquidCrystal_I2C.h → Controle do display LCD via protocolo I2C.

time.h → Sincronização de data e hora via servidor NTP.

🔹 Configurações Gerais
cpp
Copiar código
const char* SSID = "Wokwi-GUEST";
const char* PASSWORD = "";
const char* BROKER_MQTT = "52.86.16.147";
Define a rede Wi-Fi simulada, o broker MQTT e os tópicos de envio e recebimento.

🔹 Pinos e Variáveis de Controle
cpp
Copiar código
const int botaoTimeA = 14;
const int botaoTimeB = 27;
const int ledTimeA = 12;
const int ledTimeB = 13;
const int buzzer = 26;
Define os pinos físicos conectados aos botões, LEDs e buzzer.
As variáveis golsTimeA e golsTimeB armazenam o placar atual.

🔹 Conexão Wi-Fi e MQTT
As funções:

cpp
Copiar código
void reconectWiFi();
void reconnectMQTT();
Garantem que o ESP32 esteja sempre conectado.

Se o Wi-Fi cair, ele reconecta automaticamente.

Se o MQTT desconectar, ele se reconecta e volta a assinar o tópico /TEF/placar001/cmd.

🔹 Callback MQTT
cpp
Copiar código
void mqtt_callback(char* topic, byte* payload, unsigned int length)
Recebe mensagens enviadas via MyMQTT e executa ações:

"golA" → incrementa gols do Time A

"golB" → incrementa gols do Time B

"reset" → zera o placar

A cada ação, o LCD é atualizado, LEDs piscam e o buzzer toca.

🔹 Atualização do Placar
cpp
Copiar código
void atualizarPlacar() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Time A: ");
  lcd.print(golsTimeA);
  lcd.setCursor(0, 1);
  lcd.print("Time B: ");
  lcd.print(golsTimeB);
}
Mostra os gols no display LCD I2C (16x2) em tempo real.

📸 [INSERIR AQUI IMAGEM 5: LCD mostrando placar atualizado]

🔹 Publicação MQTT
cpp
Copiar código
void publicarPlacar() {
  String payload = "{";
  payload += "\"TimeA\": " + String(golsTimeA) + ",";
  payload += "\"TimeB\": " + String(golsTimeB) + ",";
  payload += "\"Data\": \"" + String(timeString) + "\"";
  payload += "}";
  MQTT.publish(TOPICO_PUBLISH, payload.c_str());
}
Cria um JSON com o placar e a data/hora atual sincronizada via NTP, publicando-o no tópico /TEF/placar001/attrs.

Exemplo publicado:

json
Copiar código
{
  "TimeA": 2,
  "TimeB": 1,
  "Data": "2025-11-05 18:22:10"
}
🔹 Loop Principal
cpp
Copiar código
void loop() {
  VerificaConexoesWiFIEMQTT();
  MQTT.loop();
  ...
}
O loop():

Garante que Wi-Fi e MQTT estejam sempre ativos.

Lê o estado dos botões e atualiza o placar localmente.

Publica automaticamente os novos valores.

📸 [INSERIR AQUI IMAGEM 6: Console mostrando mensagens MQTT publicadas]

🎥 Demonstração em Vídeo
📺 Link para o vídeo no YouTube:
👉 [INSERIR AQUI O LINK DO VÍDEO DE DEMONSTRAÇÃO]

🧾 Créditos e Agradecimentos
Base do projeto: Prof. Fábio Cabrini

Adaptação e melhorias: Luiz Antonio Morais e equipe

Instituição: FIAP — Engenharia de Software

Disciplina: IoT & Sistemas Embarcados

💬 Conclusão
O projeto demonstra a integração prática entre hardware (ESP32) e nuvem (MQTT), criando uma solução IoT que une conectividade, automação e interface física.
É um excelente exemplo de aplicação real do conceito de Internet das Coisas, com múltiplos dispositivos interagindo em tempo real através de mensagens publish/subscribe.

📸 RESUMO DOS LOCAIS PARA INSERIR IMAGENS
Etapa	Descrição	Local do README
1	Circuito completo no Wokwi	Imagem 1
2	App MyMQTT enviando comandos	Imagem 2
3	Simulação rodando no Wokwi	Imagem 3
4	App MyMQTT recebendo atualizações	Imagem 4
5	LCD mostrando placar atualizado	Imagem 5
6	Console publicando mensagens MQTT	Imagem 6
7	Vídeo da demonstração (YouTube)	Link de vídeo
