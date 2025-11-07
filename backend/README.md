# 🌐 Backend - Aplicação Flask

Aplicação web Flask que consome dados do placar via MQTT e exibe uma interface moderna no navegador.

## 📋 Arquivos

- **`app.py`**: Servidor Flask principal com integração MQTT e rotas da API
- **`requirements.txt`**: Dependências Python do projeto
- **`templates/index.html`**: Interface web do placar

## 🚀 Como Executar

### Instalação

```bash
pip install -r requirements.txt
```

### Execução

```bash
python app.py
```

A aplicação estará disponível em `http://localhost:5000`

## 📡 Rotas da API

| Rota | Método | Descrição |
|------|--------|-----------|
| `/` | GET | Página principal com interface do placar |
| `/dados` | GET | Retorna dados atuais do placar em JSON |
| `/grafico` | GET | Gera e retorna gráfico de barras (PNG) |

## 🔧 Configuração MQTT

- **Broker:** `52.86.16.147:1883`
- **Tópico Subscribe:** `/TEF/placar001/attrs`

## 📦 Dependências

- Flask
- paho-mqtt
- matplotlib
- seaborn

Consulte `requirements.txt` para versões específicas.

