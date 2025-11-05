# 🏆 Placar de Jogo Conectado — ESP32 + MQTT + LCD I2C

> Projeto desenvolvido como parte das atividades da disciplina de **IoT & Sistemas Embarcados**, com foco em **integração de hardware e nuvem via protocolo MQTT**.  
> A solução apresenta um **placar digital inteligente**, conectado a um **broker MQTT**, capaz de atualizar os resultados de forma remota e em tempo real.

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
- [Fluxo de Comunicação MQTT](#-fluxo-de-comunicação-mqtt)
- [Demonstração em Vídeo](#-demonstração-em-vídeo)
- [Execução no Wokwi](#-execução-no-wokwi)
- [Integração com MyMQTT](#-integração-com-mymqtt)
- [Resultados e Prints](#-resultados-e-prints)
- [Reprodutibilidade e Deploy](#-reprodutibilidade-e-deploy)
- [Conclusão e Aprendizados](#-conclusão-e-aprendizados)

---

## 🧠 Descrição do Projeto

O **Placar de Jogo Conectado** é um sistema IoT desenvolvido com **ESP32**, **LCD I2C**, **LEDs**, **buzzer** e **botões físicos**, que comunica-se via **protocolo MQTT** com um servidor remoto.

A proposta é demonstrar, na prática, o uso de **mensageria MQTT** para **transmitir dados em tempo real**, controlando o placar remotamente através de um **aplicativo MQTT** e exibindo as atualizações diretamente no **display físico**.

🔗 **Simulação oficial:** [Abrir projeto no Wokwi](https://wokwi.com/projects/446825400114712577)

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
Wi-Fi (Wokwi Guest)	Comunicação MQTT	-

💻 Tecnologias Envolvidas
Linguagem: C++ (Arduino)

Plataforma: Wokwi IoT Simulator

Protocolo de Comunicação: MQTT

Broker MQTT: 52.86.16.147:1883

Bibliotecas utilizadas:

WiFi.h

PubSubClient.h

LiquidCrystal_I2C.h

Wire.h

time.h

🔄 Fluxo de Comunicação MQTT
Tipo	Tópico	Função
Publicação (ESP32 → Broker)	/TEF/placar001/attrs	Envia o placar atualizado em JSON
Assinatura (Broker → ESP32)	/TEF/placar001/cmd	Recebe comandos remotos (golA, golB, reset)

Exemplo de payload publicado:

json
Copiar código
{
  "TimeA": 2,
  "TimeB": 1,
  "Data": "2025-11-05 20:15:00"
}
🎥 Demonstração em Vídeo
🎬 Assista ao vídeo completo de funcionamento (YouTube):
👉 Link do vídeo — Adicionar aqui

📌 O vídeo deve mostrar:

A simulação completa no Wokwi

O funcionamento dos botões, LEDs e buzzer

A interação em tempo real com o aplicativo MyMQTT

O envio e recebimento de mensagens via MQTT

⚙️ Execução no Wokwi
🔹 Passo 1 — Acessar o projeto
Abrir Simulação no Wokwi

🔹 Passo 2 — Iniciar a simulação
Clique em Start Simulation e aguarde a conexão Wi-Fi e MQTT.
O monitor serial exibirá:

nginx
Copiar código
Conectando ao Wi-Fi...
Wi-Fi conectado!
Conectando ao broker MQTT... conectado!
🔹 Passo 3 — Visualizar o display
O LCD mostrará:

less
Copiar código
Placar Conectado
Time A: 0
Time B: 0
🔹 Passo 4 — Testar interações
Pressione o botão do Time A (GPIO 14) → incrementa +1 para o Time A

Pressione o botão do Time B (GPIO 27) → incrementa +1 para o Time B

A cada gol:

O LED correspondente pisca

O buzzer toca

O novo placar é enviado via MQTT

📸 (Inserir aqui imagem do display Wokwi)
![Simulação Wokwi](docs/prints/wokwi-simulacao.png)

📱 Integração com MyMQTT (Android)
🔧 Passo 1 — Instalar e configurar o app
Baixe o MyMQTT na Google Play Store.

Vá em Settings (Engrenagem).

Configure:

Broker Address: 52.86.16.147

Port: 1883

Client ID: placar001

Clique em Connect e aguarde a mensagem de conexão bem-sucedida.

🔧 Passo 2 — Adicionar os tópicos
Subscribe: /TEF/placar001/attrs

Publish: /TEF/placar001/cmd

💬 Passo 3 — Testar comandos
Envie as seguintes mensagens:

Comando	Ação
golA	+1 gol no Time A
golB	+1 gol no Time B
reset	Zera o placar

📸 (Inserir aqui imagem do app MyMQTT com o comando “golA”)
![MyMQTT App](docs/prints/mqtt-app.png)

🖼️ Resultados e Prints
📊 Publicação MQTT no monitor serial
css
Copiar código
Comando recebido: golA
Placar -> A: 1 | B: 0
Publicado no FIWARE: {"TimeA":1,"TimeB":0,"Data":"2025-11-05 20:15:00"}
📸 (Inserir print do monitor serial)
![Monitor Serial](docs/prints/serial-output.png)

🔁 Reprodutibilidade e Deploy
✅ Para rodar o projeto localmente:
Clone o repositório:

bash
Copiar código
git clone https://github.com/SEU-USUARIO/placar-conectado.git
Abra o projeto no Wokwi.

Cole o código main.cpp no editor.

Clique em Start Simulation.

No celular, conecte o MyMQTT e teste os comandos.

📁 Estrutura recomendada do repositório:

css
Copiar código
placar-conectado/
├── src/main.cpp
├── docs/prints/
│   ├── wokwi-simulacao.png
│   ├── mqtt-app.png
│   ├── serial-output.png
│   └── lcd-display.png
└── README.md
🧾 Resultados da PoC (Proof of Concept)
✅ Comunicação IoT via MQTT 100% funcional
✅ Integração entre hardware (ESP32) e software (app MQTT)
✅ Atualização em tempo real do placar e exibição no LCD
✅ Feedback visual (LEDs) e sonoro (buzzer)
✅ Arquitetura totalmente reprodutível no Wokwi

🧠 Conclusão e Aprendizados
O projeto Placar de Jogo Conectado demonstra, de forma prática, a aplicabilidade do protocolo MQTT em sistemas IoT, permitindo controle remoto e sincronização em tempo real entre dispositivos físicos e aplicações de software.

Essa implementação serviu como um exercício completo de:

Comunicação MQTT cliente-servidor

Integração de sensores e atuadores

Uso de simulação virtual (Wokwi)

Reprodutibilidade via GitHub

O resultado é um sistema confiável, interativo e escalável, que pode ser facilmente adaptado para outros contextos IoT, como controle de acesso, monitoramento de ambiente ou sistemas esportivos inteligentes.

📸 Espaços reservados para imagens

bash
Copiar código
/docs/prints/wokwi-simulacao.png
/docs/prints/lcd-display.png
/docs/prints/mqtt-app.png
/docs/prints/serial-output.png
🎥 Espaço reservado para o vídeo no YouTube

arduino
Copiar código
https://youtube.com/SEU_VIDEO_AQUI
Copiar código
