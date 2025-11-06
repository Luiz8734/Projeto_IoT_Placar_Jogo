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

O projeto tem como objetivo demonstrar a integração prática entre o **ESP32**, o **protocolo MQTT** e o **display LCD I2C**, simulando um **placar eletrônico conectado à Internet**.

### Principais Características:
- **Controle Local:** Registro de gols através de botões físicos conectados ao ESP32
- **Controle Remoto:** Comandos enviados via aplicativo móvel (MyMQTT) através do protocolo MQTT
- **Exibição em Tempo Real:** Display LCD I2C mostra o placar atualizado instantaneamente
- **Publicação Automática:** Todos os eventos são publicados no broker MQTT com timestamp NTP
- **Feedback Multissensorial:** LEDs e buzzer fornecem feedback visual e sonoro a cada gol registrado
- **Sincronização com NTP:** Integração com servidor NTP para registrar data/hora precisa de cada evento

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

---

## 🌐 Comunicação MQTT

O sistema utiliza o protocolo **MQTT (Message Queuing Telemetry Transport)** para comunicação bidirecional entre o ESP32 e o aplicativo móvel.

### Configurações do Broker:
- **Endereço IP:** `52.86.16.147`  
- **Porta:** `1883` (porta padrão MQTT não criptografada)  
- **Protocolo:** MQTT v3.1.1  
- **Client ID:** `placar001` (identificador único do dispositivo)

### Arquitetura de Tópicos:
| Tópico | Direção | Função |
|--------|---------|--------|
| `/TEF/placar001/cmd` | **Subscribe** (recebe) | Recebe comandos remotos do aplicativo MyMQTT |
| `/TEF/placar001/attrs` | **Publish** (envia) | Publica atualizações do placar com timestamp |

### 📤 Comandos Aceitos via MyMQTT:
| Comando MQTT | Função Executada            | Efeitos Visuais/Sonoros |
|---------------|----------------------------|------------------------|
| `golA`        | Incrementa gols do Time A  | LED Time A pisca + buzzer |
| `golB`        | Incrementa gols do Time B  | LED Time B pisca + buzzer |
| `reset`       | Zera o placar              | LEDs piscam + buzzer |

### 📥 Formato das Mensagens Publicadas:
O sistema publica automaticamente um JSON no formato:
```json
{
  "TimeA": 2,
  "TimeB": 1,
  "Data": "2025-11-05 18:22:10"
}
```

**Campos:**
- `TimeA`: Número de gols do Time A (inteiro)
- `TimeB`: Número de gols do Time B (inteiro)
- `Data`: Timestamp no formato `YYYY-MM-DD HH:MM:SS` (sincronizado via NTP)

---

## 🧩 Execução no Wokwi

🔗 **Link do projeto no Wokwi:**  
👉 [https://wokwi.com/projects/446825400114712577](https://wokwi.com/projects/446825400114712577)

### Passo a passo detalhado para simular:

#### 1️⃣ Preparação do Ambiente
- Acesse o link acima no navegador
- Certifique-se de que o projeto está carregado corretamente
- Verifique se todos os componentes estão visíveis no diagrama

#### 2️⃣ Inicialização da Simulação
- Clique no botão **"Start Simulation"** (▶️) no canto superior direito
- Aguarde alguns segundos para o ESP32 inicializar

#### 3️⃣ Conexão com a Rede
- O ESP32 tentará conectar automaticamente ao Wi-Fi `Wokwi-GUEST`
- Você verá mensagens no **Serial Monitor** indicando o progresso da conexão
- Aguarde a mensagem: `Wi-Fi conectado!`

#### 4️⃣ Conexão MQTT
- Após conectar ao Wi-Fi, o sistema tentará conectar ao broker MQTT
- Você verá mensagens como: `Conectado ao broker MQTT!`
- O sistema se inscreverá automaticamente no tópico `/TEF/placar001/cmd`

#### 5️⃣ Testando o Sistema
- **Controle Local:** Pressione os botões físicos no simulador para registrar gols
  - Botão **Time A** (GPIO 14) → Incrementa gols do Time A
  - Botão **Time B** (GPIO 27) → Incrementa gols do Time B
- **Feedback:** Observe os LEDs piscando e o buzzer emitindo som
- **Display:** O LCD será atualizado automaticamente mostrando o placar atual

#### 6️⃣ Monitoramento
- Abra o **Serial Monitor** (ícone de terminal) para ver:
  - Logs de conexão Wi-Fi e MQTT
  - Mensagens JSON publicadas no broker
  - Timestamps de cada evento
  - Erros ou reconexões automáticas

#### 7️⃣ Teste Remoto (Opcional)
- Configure o aplicativo MyMQTT conforme instruções abaixo
- Envie comandos `golA`, `golB` ou `reset` pelo aplicativo
- Observe o ESP32 recebendo e executando os comandos remotamente

---

## 📸 Simulação no Wokwi

<img width="724" height="502" alt="image" src="https://github.com/user-attachments/assets/0ca11918-ac7b-4d43-aa4c-e28d02986c54" />

---

## 📱 Conectando o Aplicativo MyMQTT

O aplicativo **MyMQTT** permite controlar o placar remotamente e receber atualizações em tempo real.

### 📲 Instalação
1. Baixe o aplicativo **MyMQTT** na Google Play Store (disponível para Android)
2. Abra o aplicativo após a instalação

### ⚙️ Configuração Inicial

#### Passo 1: Criar Nova Conexão
- Toque no botão **"+"** ou **"Adicionar Conexão"**
- Preencha os seguintes campos:
  - **Nome da Conexão:** `Placar FIAP` (ou qualquer nome de sua preferência)
  - **Host:** `52.86.16.147`
  - **Porta:** `1883`
  - **Client ID:** `placar001`
  - **Username:** Deixe em branco (ou conforme configuração do broker)
  - **Password:** Deixe em branco (ou conforme configuração do broker)
- Salve a conexão

#### Passo 2: Conectar ao Broker
- Toque na conexão criada para estabelecer a comunicação
- Aguarde a confirmação de conexão (ícone verde ou status "Conectado")

#### Passo 3: Subscribe (Receber Atualizações)
- Navegue até a aba **"Subscribe"** ou **"Assinar"**
- Clique em **"+"** para adicionar um novo tópico
- Digite o tópico: `/TEF/placar001/attrs`
- Confirme e inscreva-se no tópico
- **Agora você receberá automaticamente todas as atualizações do placar!**

#### Passo 4: Publish (Enviar Comandos)
- Navegue até a aba **"Publish"** ou **"Publicar"**
- Configure o tópico de publicação: `/TEF/placar001/cmd`
- Digite o comando desejado no campo de mensagem:
  - `golA` → Incrementa gols do Time A
  - `golB` → Incrementa gols do Time B
  - `reset` → Zera o placar completamente
- Pressione o botão **"Publish"** ou **"Enviar"**
- O ESP32 receberá o comando e executará a ação imediatamente

### 💡 Dicas de Uso:
- **Mantenha o Subscribe ativo** para acompanhar todas as atualizações em tempo real
- **Verifique o formato** das mensagens recebidas (JSON com TimeA, TimeB e Data)
- **Use o reset** quando quiser reiniciar o placar para uma nova partida
- **Teste ambos os comandos** (golA e golB) para verificar a funcionalidade remota

---

## 📸 Aplicativo MyMQTT
<img width="537" height="860" alt="image" src="https://github.com/user-attachments/assets/8d150978-829f-4672-a8be-9dc35cc40977" />

---

## 🧠 Explicação Detalhada do Código-Fonte

Esta seção descreve em detalhes cada parte do código-fonte do projeto, explicando o funcionamento de cada componente e função.

### 🔹 Cabeçalho e Bibliotecas
```cpp
#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include "time.h"
```

**Função de cada biblioteca:**
- **`WiFi.h`** → Biblioteca nativa do ESP32 para gerenciamento de conexões Wi-Fi, incluindo funções de conexão, reconexão automática e verificação de status
- **`PubSubClient.h`** → Biblioteca principal para comunicação MQTT, gerencia conexão com broker, publicação e assinatura de tópicos, e callbacks de mensagens recebidas
- **`Wire.h`** → Biblioteca para comunicação I2C (Inter-Integrated Circuit), protocolo serial usado para comunicação com o display LCD
- **`LiquidCrystal_I2C.h`** → Biblioteca específica para controle de displays LCD com módulo I2C, simplifica comandos de escrita e formatação no display
- **`time.h`** → Biblioteca para sincronização de data/hora via NTP (Network Time Protocol), permite obter timestamp preciso de servidores na internet  

---

### 🔹 Configurações Gerais e Credenciais
```cpp
const char* SSID = "Wokwi-GUEST";
const char* PASSWORD = "";
const char* BROKER_MQTT = "52.86.16.147";
const int PORT_MQTT = 1883;
const char* TOPICO_SUBSCRIBE = "/TEF/placar001/cmd";
const char* TOPICO_PUBLISH = "/TEF/placar001/attrs";
```

**Explicação das configurações:**
- **`SSID`** → Nome da rede Wi-Fi que o ESP32 tentará conectar (no Wokwi, usa rede simulada `Wokwi-GUEST`)
- **`PASSWORD`** → Senha da rede Wi-Fi (vazia para rede Wokwi-GUEST sem autenticação)
- **`BROKER_MQTT`** → Endereço IP do servidor MQTT que gerencia as mensagens entre dispositivos
- **`PORT_MQTT`** → Porta TCP padrão do protocolo MQTT (1883 para conexões não criptografadas)
- **`TOPICO_SUBSCRIBE`** → Tópico no qual o ESP32 se inscreve para receber comandos remotos
- **`TOPICO_PUBLISH`** → Tópico no qual o ESP32 publica atualizações do placar para outros dispositivos consumirem

---

### 🔹 Configuração de Pinos e Variáveis de Estado
```cpp
const int botaoTimeA = 14;
const int botaoTimeB = 27;
const int ledTimeA = 12;
const int ledTimeB = 13;
const int buzzer = 26;

int golsTimeA = 0;
int golsTimeB = 0;
```

**Mapeamento de pinos:**
- **GPIO 14** → Botão físico para incrementar gols do Time A (INPUT_PULLUP - ativo em LOW)
- **GPIO 27** → Botão físico para incrementar gols do Time B (INPUT_PULLUP - ativo em LOW)
- **GPIO 12** → LED conectado ao Time A (OUTPUT - HIGH acende o LED)
- **GPIO 13** → LED conectado ao Time B (OUTPUT - HIGH acende o LED)
- **GPIO 26** → Buzzer piezoelétrico para feedback sonoro (OUTPUT - PWM para diferentes tons)

**Variáveis de estado:**
- **`golsTimeA`** → Contador inteiro que armazena o número de gols do Time A (inicializado em 0)
- **`golsTimeB`** → Contador inteiro que armazena o número de gols do Time B (inicializado em 0)

**Nota:** Os pinos GPIO 21 e 22 são usados automaticamente pelo protocolo I2C para comunicação com o display LCD (SDA e SCL respectivamente).

---

### 🔹 Gerenciamento de Conexões (Wi-Fi e MQTT)

O sistema implementa reconexão automática para garantir operação contínua mesmo em caso de falhas temporárias de rede.

#### Função `reconectWiFi()`
```cpp
void reconectWiFi() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.print("Tentando conectar ao Wi-Fi...");
    WiFi.begin(SSID, PASSWORD);
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
    Serial.println("Wi-Fi conectado!");
  }
}
```

**Funcionamento:**
- Verifica periodicamente o status da conexão Wi-Fi (`WiFi.status()`)
- Se desconectado (`WL_CONNECTED`), tenta reconectar usando as credenciais configuradas
- Exibe feedback visual no Serial Monitor durante o processo de reconexão
- Aguarda até que a conexão seja estabelecida antes de continuar

#### Função `reconnectMQTT()`
```cpp
void reconnectMQTT() {
  if (!MQTT.connected()) {
    Serial.print("Tentando conectar ao MQTT...");
    if (MQTT.connect("placar001")) {
      Serial.println("Conectado ao broker MQTT!");
      MQTT.subscribe(TOPICO_SUBSCRIBE);
    } else {
      Serial.print("Falha na conexão MQTT. Código: ");
      Serial.println(MQTT.state());
    }
  }
}
```

**Funcionamento:**
- Verifica se a conexão MQTT está ativa (`MQTT.connected()`)
- Se desconectado, tenta estabelecer nova conexão usando o Client ID `placar001`
- Após conexão bem-sucedida, se inscreve automaticamente no tópico de comandos (`/TEF/placar001/cmd`)
- Em caso de falha, exibe o código de erro para diagnóstico
- Os códigos de erro comuns incluem: -4 (timeout), -2 (falha de conexão), etc.

**Função `VerificaConexoesWiFIEMQTT()`**
Esta função é chamada no `loop()` principal e executa ambas as verificações de reconexão de forma sequencial.

---

### 🔹 Callback MQTT (Processamento de Mensagens Remotas)

A função callback é executada automaticamente sempre que uma mensagem é recebida em um tópico inscrito.

```cpp
void mqtt_callback(char* topic, byte* payload, unsigned int length) {
  String mensagem = "";
  for (int i = 0; i < length; i++) {
    mensagem += (char)payload[i];
  }
  
  if (mensagem == "golA") {
    golsTimeA++;
    acionarFeedbackVisual(ledTimeA);
    tocarBuzzer();
    atualizarPlacar();
    publicarPlacar();
  }
  else if (mensagem == "golB") {
    golsTimeB++;
    acionarFeedbackVisual(ledTimeB);
    tocarBuzzer();
    atualizarPlacar();
    publicarPlacar();
  }
  else if (mensagem == "reset") {
    golsTimeA = 0;
    golsTimeB = 0;
    acionarFeedbackVisual(ledTimeA);
    acionarFeedbackVisual(ledTimeB);
    tocarBuzzer();
    atualizarPlacar();
    publicarPlacar();
  }
}
```

**Processo detalhado:**

1. **Recepção da mensagem:** O payload (dados da mensagem) é recebido como array de bytes
2. **Conversão para String:** Os bytes são convertidos para String para facilitar comparação
3. **Validação do comando:** Compara a mensagem recebida com os comandos válidos (`golA`, `golB`, `reset`)
4. **Execução da ação:**
   - **`golA`:** Incrementa contador Time A, aciona LED correspondente, toca buzzer, atualiza display e publica novo estado
   - **`golB`:** Incrementa contador Time B, aciona LED correspondente, toca buzzer, atualiza display e publica novo estado
   - **`reset`:** Zera ambos os contadores, aciona ambos os LEDs, toca buzzer, atualiza display e publica estado zerado

**Fluxo de execução após receber comando:**
```
Mensagem recebida → Validação → Atualização de variáveis → Feedback visual/sonoro → 
Atualização display → Publicação no broker MQTT → Confirmação via Serial Monitor
```

---

### 🔹 Atualização do Display LCD

A função `atualizarPlacar()` é responsável por exibir o placar atual no display LCD I2C.

```cpp
void atualizarPlacar() {
  lcd.clear();                    // Limpa todo o conteúdo do display
  lcd.setCursor(0, 0);           // Posiciona cursor na linha 0, coluna 0
  lcd.print("Time A: ");         // Escreve texto fixo
  lcd.print(golsTimeA);          // Escreve valor do contador
  lcd.setCursor(0, 1);           // Posiciona cursor na linha 1, coluna 0
  lcd.print("Time B: ");         // Escreve texto fixo
  lcd.print(golsTimeB);          // Escreve valor do contador
}
```

**Características do Display:**
- **Tipo:** LCD I2C 16x2 (16 caracteres por linha, 2 linhas)
- **Protocolo:** I2C (reduz fiação de 16 para 4 cabos: VCC, GND, SDA, SCL)
- **Endereço I2C:** Geralmente `0x27` ou `0x3F` (configurado na inicialização)

**Formato de exibição:**
```
Linha 0: Time A: X
Linha 1: Time B: Y
```

**Otimizações implementadas:**
- `lcd.clear()` garante que não há caracteres residuais na tela
- Uso de `setCursor()` para controle preciso da posição do texto
- Concatenação direta de texto fixo com variáveis numéricas
- Atualização síncrona (sempre executa após mudança no placar)

**Nota:** A função é chamada sempre que há alteração no placar, seja por botão físico ou comando MQTT remoto.

---

### 🔹 Publicação MQTT de Dados do Placar

A função `publicarPlacar()` formata e envia os dados do placar para o broker MQTT em formato JSON.

```cpp
void publicarPlacar() {
  obterTimestampNTP();  // Atualiza variável timeString com data/hora atual
  
  String payload = "{";
  payload += "\"TimeA\": " + String(golsTimeA) + ",";
  payload += "\"TimeB\": " + String(golsTimeB) + ",";
  payload += "\"Data\": \"" + String(timeString) + "\"";
  payload += "}";
  
  Serial.print("Publicando: ");
  Serial.println(payload);
  
  if (MQTT.publish(TOPICO_PUBLISH, payload.c_str())) {
    Serial.println("Mensagem publicada com sucesso!");
  } else {
    Serial.println("Erro ao publicar mensagem!");
  }
}
```

**Processo de construção do JSON:**

1. **Timestamp NTP:** Chama `obterTimestampNTP()` para sincronizar data/hora atual
2. **Formatação JSON manual:** Constrói string JSON seguindo o padrão RFC 7159
3. **Conversão de tipos:** Converte inteiros para String antes de concatenar
4. **Publicação:** Envia mensagem para o tópico `/TEF/placar001/attrs`
5. **Feedback:** Exibe no Serial Monitor se a publicação foi bem-sucedida

**Formato da mensagem publicada:**
```json
{
  "TimeA": 2,
  "TimeB": 1,
  "Data": "2025-11-05 18:22:10"
}
```

**Campos do JSON:**
- **`TimeA`** (integer): Número atual de gols do Time A
- **`TimeB`** (integer): Número atual de gols do Time B
- **`Data`** (string): Timestamp no formato `YYYY-MM-DD HH:MM:SS`, sincronizado via NTP

**Sincronização NTP:**
O sistema utiliza um servidor NTP (Network Time Protocol) para obter a hora precisa:
- **Servidor NTP:** `pool.ntp.org` ou `time.nist.gov`
- **Fuso horário:** Configurado no código (ex: `America/Sao_Paulo`)
- **Atualização:** Obtida a cada publicação para garantir precisão temporal

**Subscribers interessados:**
Todos os dispositivos inscritos no tópico `/TEF/placar001/attrs` receberão automaticamente esta mensagem, permitindo:
- Aplicativos móveis mostrarem o placar em tempo real
- Sistemas de logging registrarem histórico de eventos
- Dashboards web exibirem estatísticas atualizadas

---

### 🔹 Loop Principal (Laço de Execução Contínua)

O `loop()` é executado infinitamente após o `setup()`, sendo o coração do programa.

```cpp
void loop() {
  // 1. Verificação e reconexão de rede
  VerificaConexoesWiFIEMQTT();
  
  // 2. Processamento de mensagens MQTT recebidas
  MQTT.loop();
  
  // 3. Leitura de botões físicos com debounce
  int estadoBotaoA = digitalRead(botaoTimeA);
  int estadoBotaoB = digitalRead(botaoTimeB);
  
  // 4. Detecção de borda de descida (botão pressionado)
  if (estadoBotaoA == LOW && estadoBotaoAAnterior == HIGH) {
    golsTimeA++;
    acionarFeedbackVisual(ledTimeA);
    tocarBuzzer();
    atualizarPlacar();
    publicarPlacar();
  }
  
  if (estadoBotaoB == LOW && estadoBotaoBAnterior == HIGH) {
    golsTimeB++;
    acionarFeedbackVisual(ledTimeB);
    tocarBuzzer();
    atualizarPlacar();
    publicarPlacar();
  }
  
  // 5. Atualização de estados anteriores para debounce
  estadoBotaoAAnterior = estadoBotaoA;
  estadoBotaoBAnterior = estadoBotaoB;
  
  // 6. Pequeno delay para evitar leituras excessivas
  delay(50);
}
```

**Fluxo de execução detalhado:**

#### 1️⃣ Verificação de Conexões (`VerificaConexoesWiFIEMQTT()`)
- Executa a cada iteração do loop
- Verifica status do Wi-Fi e reconecta se necessário
- Verifica status do MQTT e reconecta se necessário
- Garante que o sistema está sempre conectado

#### 2️⃣ Processamento MQTT (`MQTT.loop()`)
- **Função crítica:** Deve ser chamada frequentemente (a cada iteração)
- Verifica se há mensagens recebidas no broker
- Se houver mensagem, dispara automaticamente o callback `mqtt_callback()`
- Mantém a conexão MQTT "viva" (keep-alive)

#### 3️⃣ Leitura de Botões Físicos
- Lê o estado atual dos GPIOs conectados aos botões
- Usa `INPUT_PULLUP`, então botão pressionado = LOW (0V)
- Botão solto = HIGH (3.3V via pull-up interno)

#### 4️⃣ Detecção de Borda (Edge Detection)
- **Problema:** Sem debounce, um único pressionamento pode ser detectado múltiplas vezes
- **Solução:** Compara estado atual com estado anterior (`estadoBotaoAnterior`)
- **Detecção de borda de descida:** Detecta transição de HIGH → LOW (momento do pressionamento)
- Garante que cada ação é executada apenas uma vez por pressionamento

#### 5️⃣ Atualização de Estados
- Salva o estado atual como "anterior" para próxima iteração
- Necessário para o funcionamento correto do debounce

#### 6️⃣ Delay de Controle
- `delay(50)` → Aguarda 50ms entre iterações
- Previne leituras excessivas de GPIO
- Dá tempo para processamento de outras tarefas
- Equilíbrio entre responsividade e uso de recursos

**Comportamento do sistema:**
- **Prioridade:** Conexões de rede sempre têm prioridade
- **Reatividade:** Botões são lidos a cada 50ms (máximo 20 leituras/segundo)
- **Sincronização:** Tanto botões físicos quanto comandos MQTT executam o mesmo fluxo
- **Confiabilidade:** Sistema robusto com reconexão automática e tratamento de erros  

---

## 💬 Conclusão

Este projeto demonstra de forma prática e completa a integração entre **hardware embarcado (ESP32)** e **tecnologias de nuvem (MQTT)**, criando uma solução IoT robusta que combina **conectividade sem fio, automação local e interface física interativa**.

### 🎯 Objetivos Alcançados:

✅ **Integração Hardware-Software:** Demonstração eficiente do uso de sensores, atuadores e displays no ESP32  
✅ **Comunicação MQTT:** Implementação completa de protocolo publish/subscribe para comunicação em tempo real  
✅ **Controle Remoto:** Capacidade de controlar dispositivo físico através de aplicativo móvel  
✅ **Feedback Multissensorial:** Uso de LEDs e buzzer para melhorar experiência do usuário  
✅ **Sincronização Temporal:** Integração com servidores NTP para timestamp preciso  
✅ **Robustez:** Sistema com reconexão automática e tratamento de erros  
✅ **Simulação Realista:** Uso do Wokwi para prototipagem e teste sem hardware físico  

### 🌟 Conceitos Aplicados:

- **Internet das Coisas (IoT):** Dispositivos conectados trocando dados pela internet
- **Protocolo MQTT:** Comunicação leve e eficiente para IoT
- **Arquitetura Publish/Subscribe:** Padrão de mensageria assíncrona
- **Hardware Embarcado:** Programação de microcontroladores com múltiplos periféricos
- **Protocolo I2C:** Comunicação serial para dispositivos conectados
- **Debounce de Botões:** Técnica para evitar leituras múltiplas de sinais digitais
- **Sincronização NTP:** Obtenção de tempo preciso via internet

### 🚀 Aplicações Práticas:

Este projeto pode ser adaptado para diversas aplicações reais:
- **Placares esportivos** em ginásios e estádios
- **Sistemas de votação** em tempo real
- **Contadores industriais** com monitoramento remoto
- **Sistemas de alerta** com notificações em múltiplos dispositivos
- **Protótipos de automação residencial** com controle local e remoto

### 📚 Valor Educacional:

Este projeto serve como excelente material didático para:
- Estudantes de **Engenharia de Software** aprendendo IoT
- Cursos de **Sistemas Embarcados** e **Microcontroladores**
- Disciplinas de **Redes de Computadores** e **Protocolos de Comunicação**
- Workshops práticos de **Arduino/ESP32**

### 🎓 Aprendizados Técnicos:

- Configuração e uso do ESP32 com WiFi
- Implementação de clientes MQTT
- Trabalho com displays LCD via I2C
- Leitura de entradas digitais com debounce
- Controle de saídas (LEDs e buzzer)
- Formatação e parsing de JSON
- Sincronização de tempo via NTP
- Debugging e monitoramento via Serial
- Simulação de hardware no ambiente Wokwi

O projeto representa uma **solução completa e funcional** que ilustra os principais conceitos de IoT, sendo um excelente ponto de partida para projetos mais complexos e aplicações comerciais.

---

## 🎥 Demonstração em Vídeo

Esta seção contém o vídeo completo de demonstração do projeto, mostrando todas as funcionalidades em ação.

### 📺 Vídeo no YouTube

[![Demonstração do Placar Conectado - ESP32 + MQTT](<img width="200" height="100" alt="image" src="https://github.com/user-attachments/assets/f1b7008d-af30-4f1a-ac28-ff2959b8baeb" />)

**Link direto:** 👉 [INSERIR AQUI O LINK DO VÍDEO DE DEMONSTRAÇÃO DO YOUTUBE](https://www.youtube.com/watch?v=VIDEO_ID_HERE)

### 📋 Conteúdo do Vídeo

O vídeo demonstra:
- ✅ **Parte 1:** Apresentação do projeto e objetivos
- ✅ **Parte 2:** Explicação do circuito e conexões físicas
- ✅ **Parte 3:** Demonstração do controle local via botões físicos
- ✅ **Parte 4:** Configuração e uso do aplicativo MyMQTT
- ✅ **Parte 5:** Controle remoto via comandos MQTT
- ✅ **Parte 6:** Visualização das mensagens publicadas no broker
- ✅ **Parte 7:** Funcionamento completo do sistema integrado
- ✅ **Parte 8:** Demonstração da sincronização NTP e timestamps
- ✅ **Parte 9:** Teste de reconexão automática após falhas de rede
- ✅ **Parte 10:** Conclusão e considerações finais

---

**Nota:** Para adicionar o vídeo, substitua `VIDEO_ID_HERE` pelo ID do seu vídeo do YouTube (parte após `watch?v=` na URL do YouTube).

---

## 🧾 Créditos e Agradecimentos  

- **Base do projeto:** Prof. *Fábio Cabrini*  
- **Adaptação e melhorias:** *Luiz Antonio Morais* e equipe  
- **Instituição:** *FIAP — Engenharia de Software*  
- **Disciplina:** *IoT & Sistemas Embarcados*  
