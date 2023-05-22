# Maçaneta Eletrônica com Raspberry Pi Pico

Este é um projeto baseado no microcontrolador Raspberry Pi Pico, que consiste na construção de uma maçaneta eletrônica na qual seu funcionamento é liberado via a aproximação de um cartão TAG.

< Foto Final do Projeto >

## 🎬 Começando

Essas instruções permitirão que você consiga realizar uma cópia do projeto em operação n seu Raspberry para fins de desenvolvimento e teste.

### 🕹️ Hardware Utilizado

 * [Raspberry Pi Pico](https://www.amazon.com.br/LANDZO-Raspberry-Pi-Pico/dp/B08VNR5RLF)
 * [Display OLED SPI de 128x32]()
 * [Sensor de Movimento PIR HC-SR501](https://www.robocore.net/sensor-ambiente/sensor-de-presenca-pir-hc-sr501)
 * [Sensor de Obstáculos Reflexivo Infravermelho](https://www.eletrogate.com/sensor-de-obstaculo-reflexivo-infravermelho)
 * [Sensor de RFID com TAG](https://curtocircuito.com.br/kit-rfid-rc522.html)
 * [Trava Eletrica Solenoide 12 Volts](https://produto.mercadolivre.com.br/MLB-2187293250-mini-trava-eletrica-solenoide-12v-arduino-raspberry-_JM?quantity=1)
 * [Rele]()
 * [Botão de Arduino](https://arduinoeeletronica.com.br/produto/botao-microchave-push-button-4-pinos/)

### Ferramentas de Software Utilizado

 * [Thonny Python IDE](https://thonny.org/)
 * [MicroPython firmware](https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/3)

## 🚀 Instalação

###  Esquema Elétrico

< Foto Final do Esquema Elétrico >

###  Diagrama de Blocos

< Foto Final do Diagrama de Blocos>

### ⚙️ Executando os testes

1. Montar em uma protoboard o esquema elétrico listado anteriormente.

2. Utilizar um cabo Micro USB para conectar o Raspberry Pi Pico e seu computador.
    - Conectar a entrada Micro USB no Raspberry Pi Pico
    - Conectar a entrada USB padrão em seu computador

3. Abrir a IDE Thonny
    
3. Fazer a SOMENTE a instalção do MicroPython firmware conforme a documentação
    - https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/3

4. Armazene todos os arquivos listados neste repositório dentro do Raspberry Pi Pico.

5. Selecione o código teste.py (listado abaixo) implementado no passo 4 e o execute.

6. A confirmação de sucesso na instalação dos dispositivos é obtida se uma mensagem igual a ``` !!! SUCESSO !!! ``` aparecer no display.

< Video Final dos Testes>

> **Observação:** Se a inicialização não funcionar corretamente verifique se periféricos estão corretamente conectados em seus respectivos pinos conforme o esquema eslétrico.

---

## 📦 Implantação

Adicione notas adicionais sobre como implantar isso em um sistema ativo

## ✒️ Autores

* Fernando Henriques Neto &nbsp;18.00931-0 
* Guilherme Sanches Rossi &nbsp;&nbsp;19.02404-5 
* Luiz Fernando Rodrigues &nbsp;&nbsp;&nbsp;19.01358-2 
* Matheus Coelho Rocha  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;20.00391-9 
* Pedro Henrique S.Hein &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;20.00134-7 

---
## 🎁 Expressões de gratidão

Agradecimentos aos professores Sergio Ribeiro Augusto e Rodrigo de Marca Franca por todo suporte para a conclusão do Projeto.


