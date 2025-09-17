# Projeto IoT: Placar de Jogo - Canal Passa a Bola ⚽

## Integrantes
| RM      | Nome Completo          |
|---------|----------------------|
| 562142  | Luiz Antonio Morais   |
| 561997  | Nicolas Barnabe      |
| 561459  | Kevin Venancio       |
| 561568  | Guilherme Moura      |

---

## Descrição do Projeto
O **Placar de Jogo IoT** é um sistema eletrônico desenvolvido para monitorar e exibir gols de partidas de futebol em tempo real. O projeto foi idealizado para o canal **"Passa a Bola"** com o objetivo de mostrar como **IoT (Internet das Coisas)** pode ser aplicada em esportes, proporcionando interatividade e uma experiência visual para jogadores e espectadores.  

O projeto simula um **sensor de gol** utilizando **botões físicos**, que ao serem pressionados, atualizam o placar, acendem um LED correspondente e emitem um som de buzzer para sinalizar a pontuação. O placar é exibido em um **LCD 16x2 com interface I2C**, tornando a visualização clara e imediata.

---

## Arquitetura Proposta

### Diagrama do Sistema

![Diagrama do Placar de Jogo](img/mapa.png)

### Explicação
1. **Botões físicos**: Simulam os sensores de gol para cada time. Quando pressionados, enviam um sinal digital para o Arduino.  
2. **Arduino Uno**: Centraliza o processamento. Recebe sinais dos botões, atualiza o LCD, aciona LEDs e toca o buzzer.  
3. **LEDs**: Pisca rapidamente para indicar que um gol foi marcado.  
4. **Buzzer**: Emite som curto para reforçar a sinalização do gol.  
5. **LCD I2C 16x2**: Exibe o placar atualizado para ambos os times.  

Essa arquitetura permite **resposta imediata a eventos** e visualização clara do placar, com baixo custo e fácil implementação.

---

## Recursos Necessários

- **Hardware**:
  - 1 Arduino Uno  
  - 1 LCD I2C 16x2  
  - 2 Botões físicos (simulando sensores de gol)  
  - 2 LEDs (um para cada time)  
  - 1 Buzzer  
  - Jumpers e resistores  

- **Software**:
  - Arduino IDE  
  - Biblioteca **LiquidCrystal_I2C**  

## Simulação Online
Você pode testar o projeto online no **Wokwi Arduino Simulator**:  
👉 [Clique aqui para acessar a simulação](https://wokwi.com/projects/442301501864629249)

---

## Instruções de Uso

1. Conecte o Arduino aos componentes conforme o esquema do diagrama.  
2. Certifique-se de que os botões estão funcionando como **sensores de gol**.  
3. Ligue o Arduino ao computador ou fonte de energia.  
4. Abra o código no Arduino IDE e faça o upload.  
5. No início, o LCD exibirá **“Placar de Jogo”** por 2 segundos.  
6. Para marcar um gol: pressione o botão correspondente ao time.  
7. O LED piscará, o buzzer tocará e o LCD será atualizado com o novo placar.

---

## Código Fonte

```cpp
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Inicializa o LCD 
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Botões simulando sensores de gol
const int botaoTimeA = 7;
const int botaoTimeB = 8;

// LEDs para sinalizar gol
const int ledTimeA = 9;
const int ledTimeB = 10;

// Buzzer
const int buzzer = 6;

// Contadores de gols
int golsTimeA = 0;
int golsTimeB = 0;

// Debounce
unsigned long ultimoTempoA = 0;
unsigned long ultimoTempoB = 0;
const unsigned long debounceDelay = 200; 

void setup() {
  pinMode(botaoTimeA, INPUT_PULLUP);
  pinMode(botaoTimeB, INPUT_PULLUP);
  pinMode(ledTimeA, OUTPUT);
  pinMode(ledTimeB, OUTPUT);
  pinMode(buzzer, OUTPUT);
  lcd.begin(16, 2);
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Placar de Jogo");
  delay(2000);
  atualizarPlacar();
}

void loop() {
  unsigned long tempoAtual = millis();
  
  if(digitalRead(botaoTimeA) == LOW && tempoAtual - ultimoTempoA > debounceDelay){
    golsTimeA++;
    piscarLed(ledTimeA);
    tocarBuzzer();
    atualizarPlacar();
    ultimoTempoA = tempoAtual;
  }
  
  if(digitalRead(botaoTimeB) == LOW && tempoAtual - ultimoTempoB > debounceDelay){
    golsTimeB++;
    piscarLed(ledTimeB);
    tocarBuzzer();
    atualizarPlacar();
    ultimoTempoB = tempoAtual;
  }
}

void atualizarPlacar(){
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Time A: ");
  lcd.print(golsTimeA);
  lcd.setCursor(0, 1);
  lcd.print("Time B: ");
  lcd.print(golsTimeB);
}

void piscarLed(int led){
  digitalWrite(led, HIGH);
  delay(200);
  digitalWrite(led, LOW);
}

void tocarBuzzer(){
  tone(buzzer, 1000, 200); 
}

## Recursos Necessários

- **Hardware**:
  - 1 Arduino Uno  
  - 1 LCD I2C 16x2  
  - 2 Botões físicos (simulando sensores de gol)  
  - 2 LEDs (um para cada time)  
  - 1 Buzzer  
  - Jumpers e resistores  

- **Software**:
  - Arduino IDE  
  - Biblioteca **LiquidCrystal_I2C**  

---

## Script de Configuração da Plataforma

Para preparar sua plataforma e instalar a biblioteca automaticamente, siga os passos abaixo. Este script funciona via **Arduino CLI**:

```bash
# Atualiza a lista de bibliotecas
arduino-cli lib update-index

# Instala a biblioteca necessária
arduino-cli lib install "LiquidCrystal_I2C"

# Verifica a placa conectada
arduino-cli board list

# Compila o projeto (substitua PlacarDeJogo.ino pelo nome do arquivo)
arduino-cli compile --fqbn arduino:avr:uno PlacarDeJogo.ino

# Faz o upload para a placa (substitua a porta conforme o seu sistema)
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno PlacarDeJogo.ino