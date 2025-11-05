# 🏆 Placar de Jogo Conectado — ESP32 + MQTT + LCD I2C

> Projeto desenvolvido por alunos da **FIAP** como parte das atividades de **IoT & Sistemas Embarcados**, integrando hardware e nuvem via **protocolo MQTT**.  
> O sistema simula um **placar digital inteligente**, capaz de se comunicar com um **broker MQTT** e um **aplicativo móvel (MyMQTT)** para atualização remota de resultados esportivos em tempo real.

---

## 👨‍💻 Integrantes

| RM      | Nome Completo          |
|---------|----------------------|
| 562142  | Luiz Antonio Morais   |
| 561997  | Nicolas Barnabe      |
| 561459  | Kevin Venancio       |
| 561568  | Guilherme Moura      |

---

## 📘 Sumário
- [Descrição do Projeto](#-descrição-do-projeto)
- [Arquitetura do Sistema](#-arquitetura-do-sistema)
- [Componentes Utilizados](#-componentes-utilizados)
- [Tecnologias Envolvidas](#-tecnologias-envolvidas)
- [Código-Fonte Completo e Explicado](#-código-fonte-completo-e-explicado)
- [Execução no Wokwi](#-execução-no-wokwi)
- [Integração com MyMQTT](#-integração-com-mymqtt)
- [Demonstração em Vídeo](#-demonstração-em-vídeo)
- [Resultados e Prints](#-resultados-e-prints)
- [Conclusão e Aprendizados](#-conclusão-e-aprendizados)

---

## 🧠 Descrição do Projeto

O **Placar de Jogo Conectado** é um sistema IoT que utiliza o **ESP32** para registrar, exibir e compartilhar em tempo real o resultado de uma partida.  
Com o uso do **protocolo MQTT**, o dispositivo pode **receber comandos remotos** (como `golA`, `golB` e `reset`) através do aplicativo **MyMQTT** e **publicar o placar atualizado** em formato JSON.

📡 **Comunicação em tempo real**  
📱 **Controle remoto via app MQTT**  
🔊 **Feedback visual e sonoro com LEDs e buzzer**

---

## 🧩 Arquitetura do Sistema

```mermaid
graph TD
A[Botão Time A/B] -->|Incrementa Gol| B(ESP32)
B -->|Publica via MQTT| C((Broker - 52.86.16.147))
C -->|Recebe comando| D[Aplicativo MyMQTT]
D -->|Envia mensagens (golA/golB/reset)| C
C -->|Repasse ao ESP32| B
B -->|Atualiza LCD + LED + Buzzer| E[LCD Display 16x2]
🧰 Componentes Utilizados
Componente	Função	Quantidade
ESP32 DevKit	Microcontrolador principal	1
Display LCD 16x2 (I2C)	Exibição do placar	1
LED Vermelho	Indicação Time A	1
LED Azul	Indicação Time B	1
Buzzer	Alerta sonoro a cada gol	1
Botão Push	Gol Time A	1
Botão Push	Gol Time B	1

💻 Tecnologias Envolvidas
Linguagem: C++ (Arduino)

Simulação: Wokwi IoT Simulator

Protocolo: MQTT

Broker MQTT: 52.86.16.147:1883

App de Teste: MyMQTT (Android)

Bibliotecas:

WiFi.h

PubSubClient.h

LiquidCrystal_I2C.h

Wire.h

time.h

🧾 Código-Fonte Completo e Explicado
A seguir, o código-fonte do projeto com explicações por seção:

cpp
Copiar código
// ======= INFORMAÇÕES =======
// Autor: Luiz Morais (base: Fábio Cabrini)
// Projeto: Placar de jogo conectado (ESP32 + LCD + MQTT)
// =======================================

#include <WiFi.h>                // Conexão com rede Wi-Fi
#include <PubSubClient.h>        // Cliente MQTT
#include <Wire.h>                // Comunicação I2C
#include <LiquidCrystal_I2C.h>   // Controle do display LCD
#include "time.h"                // Para sincronização NTP (data/hora)

// ======= CONFIGURAÇÕES EDITÁVEIS =======
const char* SSID = "Wokwi-GUEST"; // Rede simulada do Wokwi
const char* PASSWORD = "";         // Sem senha
const char* BROKER_MQTT = "52.86.16.147";
const int BROKER_PORT = 1883;

// ======= TÓPICOS MQTT =======
const char* TOPICO_SUBSCRIBE = "/TEF/placar001/cmd";   // Recebe comandos
const char* TOPICO_PUBLISH   = "/TEF/placar001/attrs"; // Envia placar

// ======= IDENTIFICAÇÃO =======
const char* ID_MQTT = "placar001";

// ======= LCD =======
LiquidCrystal_I2C lcd(0x27, 16, 2);  // Endereço I2C do display

// ======= BOTÕES, LEDS, BUZZER =======
const int botaoTimeA = 14;
const int botaoTimeB = 27;
const int ledTimeA = 12;
const int ledTimeB = 13;
const int buzzer = 26;

// ======= VARIÁVEIS DE CONTROLE =======
int golsTimeA = 0;
int golsTimeB = 0;
unsigned long ultimoTempoA = 0;
unsigned long ultimoTempoB = 0;
const unsigned long debounceDelay = 200;

// ======= REDE / MQTT =======
WiFiClient espClient;
PubSubClient MQTT(espClient);

// ======= NTP (para timestamp) =======
const char* ntpServer = "pool.ntp.org";
const long gmtOffset_sec = -3 * 3600;  // Horário de Brasília
const int daylightOffset_sec = 0;
🔧 Funções de Conexão Wi-Fi e MQTT
Garantem a reconexão automática caso a conexão seja perdida.

cpp
Copiar código
void reconectWiFi() {
  if (WiFi.status() == WL_CONNECTED) return;
  Serial.println("Conectando ao Wi-Fi...");
  WiFi.begin(SSID, PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi conectado!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
}

void reconnectMQTT() {
  while (!MQTT.connected()) {
    Serial.print("Conectando ao broker MQTT...");
    if (MQTT.connect(ID_MQTT)) {
      Serial.println(" conectado!");
      MQTT.subscribe(TOPICO_SUBSCRIBE);
    } else {
      Serial.println(" falhou, tentando novamente...");
      delay(2000);
    }
  }
}

void VerificaConexoesWiFIEMQTT() {
  if (WiFi.status() != WL_CONNECTED) reconectWiFi();
  if (!MQTT.connected()) reconnectMQTT();
}
💬 Callback MQTT — Recebimento de Comandos
Recebe mensagens MQTT e executa ações (gol, reset).

cpp
Copiar código
void mqtt_callback(char* topic, byte* payload, unsigned int length) {
  String msg;
  for (int i = 0; i < length; i++) msg += (char)payload[i];
  Serial.print("Comando recebido: "); Serial.println(msg);

  if (msg == "reset") {
    golsTimeA = 0; golsTimeB = 0;
  } else if (msg == "golA") {
    golsTimeA++; piscarLed(ledTimeA); tocarBuzzer();
  } else if (msg == "golB") {
    golsTimeB++; piscarLed(ledTimeB); tocarBuzzer();
  }
  atualizarPlacar();
  publicarPlacar();
}
⚙️ Funções de Hardware
Atualizam o LCD, piscam LEDs e acionam o buzzer.

cpp
Copiar código
void atualizarPlacar() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Time A: "); lcd.print(golsTimeA);
  lcd.setCursor(0, 1);
  lcd.print("Time B: "); lcd.print(golsTimeB);
  Serial.printf("Placar -> A: %d | B: %d\n", golsTimeA, golsTimeB);
}

void piscarLed(int led) {
  digitalWrite(led, HIGH); delay(200); digitalWrite(led, LOW);
}

void tocarBuzzer() {
  tone(buzzer, 1000, 200);
}
🌐 Publicação do Placar no Broker
cpp
Copiar código
void publicarPlacar() {
  struct tm timeinfo;
  getLocalTime(&timeinfo);
  char timeString[25];
  strftime(timeString, sizeof(timeString), "%Y-%m-%d %H:%M:%S", &timeinfo);

  String payload = "{";
  payload += "\"TimeA\": " + String(golsTimeA) + ",";
  payload += "\"TimeB\": " + String(golsTimeB) + ",";
  payload += "\"Data\": \"" + String(timeString) + "\"}";
  
  MQTT.publish(TOPICO_PUBLISH, payload.c_str());
  Serial.println("Publicado no FIWARE: " + payload);
}
🚀 Setup e Loop Principal
cpp
Copiar código
void setup() {
  Serial.begin(115200);
  pinMode(botaoTimeA, INPUT_PULLUP);
  pinMode(botaoTimeB, INPUT_PULLUP);
  pinMode(ledTimeA, OUTPUT);
  pinMode(ledTimeB, OUTPUT);
  pinMode(buzzer, OUTPUT);

  lcd.init();
  lcd.backlight();
  lcd.print("Placar Conectado");
  delay(2000);

  WiFi.mode(WIFI_STA);
  reconectWiFi();
  MQTT.setServer(BROKER_MQTT, BROKER_PORT);
  MQTT.setCallback(mqtt_callback);

  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  atualizarPlacar();
  publicarPlacar();
}

void loop() {
  VerificaConexoesWiFIEMQTT();
  MQTT.loop();
  unsigned long tempoAtual = millis();

  if (digitalRead(botaoTimeA) == LOW && tempoAtual - ultimoTempoA > debounceDelay) {
    golsTimeA++; piscarLed(ledTimeA); tocarBuzzer();
    atualizarPlacar(); publicarPlacar();
    ultimoTempoA = tempoAtual;
  }

  if (digitalRead(botaoTimeB) == LOW && tempoAtual - ultimoTempoB > debounceDelay) {
    golsTimeB++; piscarLed(ledTimeB); tocarBuzzer();
    atualizarPlacar(); publicarPlacar();
    ultimoTempoB = tempoAtual;
  }
}
⚙️ Execução no Wokwi
Acesse o projeto:
🔗 https://wokwi.com/projects/446825400114712577

Clique em Start Simulation.

Observe o LCD mostrando o placar inicial.

Pressione os botões físicos para marcar gols.

Veja as atualizações também no MyMQTT App.

📸 (Espaço reservado para imagem do Wokwi)
![Wokwi Simulation](docs/prints/wokwi-simulacao.png)

📱 Integração com MyMQTT
🔧 Passos:
Baixe o app MyMQTT na Google Play.

Vá em Settings → Connection

Broker: 52.86.16.147

Port: 1883

Client ID: placar001

Conecte e adicione:

Subscribe: /TEF/placar001/attrs

Publish: /TEF/placar001/cmd

💬 Comandos disponíveis:
Comando	Ação
golA	Adiciona 1 gol ao Time A
golB	Adiciona 1 gol ao Time B
reset	Zera o placar

📸 (Espaço reservado para print do MyMQTT)
![MyMQTT Interface](docs/prints/mqtt-app.png)

🎥 Demonstração em Vídeo
🎬 Assista ao vídeo completo de funcionamento:
👉 Link do vídeo — Adicionar aqui

📊 Resultados e Prints
📸 (Espaço reservado para prints do projeto)

Wokwi LCD ativo

Monitor serial

App MQTT enviando comandos

LEDs e buzzer em ação

🧠 Conclusão e Aprendizados
O projeto demonstrou a eficiência do protocolo MQTT em aplicações IoT, integrando hardware físico e controle remoto de forma sincronizada e confiável.
Foi possível compreender conceitos fundamentais como:

Comunicação publisher/subscriber

Reconexão automática de rede e broker

Envio de dados em formato JSON

Feedback multimodal com LCD, LEDs e buzzer

📸 Espaços reservados para imagens

bash
Copiar código
/docs/prints/wokwi-simulacao.png
/docs/prints/mqtt-app.png
/docs/prints/serial-output.png
🎥 Espaço reservado para o vídeo no YouTube

arduino
Copiar código
https://youtube.com/SEU_VIDEO_AQUI
Copiar código
