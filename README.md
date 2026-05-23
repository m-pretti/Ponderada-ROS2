# Turtle Draw: Silhueta com ROS 2 e Visão Computacional

Este projeto integra técnicas de Visão Computacional com a robótica simulada no ROS 2. O objetivo é processar a imagem de um cachorro, extrair sua silhueta de forma limpa e contínua, e fazer com que a tartaruga do **Turtlesim** desenhe esse contorno na tela. 

Para evitar o problema clássico de linhas cruzando o desenho por dentro (riscos de travessia), o projeto utiliza chamadas ao serviço de teleporte absoluto (`/turtle1/teleport_absolute`), garantindo um traçado perfeito e profissional.

## Estrutura do Workspace

Certifique-se de que o seu workspace (`~/pond-prog`) esteja organizado da seguinte forma:

```
~/pond-prog/
├── caminho_turtlesim.txt               # Arquivo gerado pelo Colab contendo as coordenadas (X,Y)
└── src/
    └── turtle_draw_project/
        ├── package.xml                 # Dependências do ROS 2 (rclpy, turtlesim)
        ├── pyproject.toml              # Configuração do entry_point (console_scripts)
        ├── setup.cfg
        └── turtle_draw_project/
            ├── __init__.py
            └── turtle_drawer.py        # Código-fonte principal do Nó de teleporte
```

## Passo a Passo para Execução

### 1. Geração do Caminho (Google Colab)

Antes de rodar o ROS 2, é necessário processar a imagem e gerar os pontos:

1. Abra o notebook `.ipynb` no Google Colab.
2. Faça o upload da imagem original (`dog.jpg`).
3. Execute todas as células. O pipeline de visão computacional fará:
* Redução de escala (para eliminar ruídos finos).
* Filtro de bordas e limiarização.
* Fechamento morfológico (Dilação) e "Truque do Chão" para evitar vazamentos.
* *Flood Fill* para criar uma silhueta sólida.
* Algoritmo do Vizinho Mais Próximo para ordenar os pontos sequencialmente.

4. Baixe o arquivo `caminho_turtlesim.txt` gerado na última célula e coloque-o na raiz do seu workspace (`~/pond-prog/`).

### 2. Compilando o Pacote ROS 2

Abra o terminal no seu ambiente Linux e compile o projeto usando o `colcon`:

```
# Navegue até a raiz do workspace
cd ~/pond-prog

# Compile o pacote
colcon build --packages-select turtle_draw_project

# Carregue as variáveis de ambiente
source install/setup.bash

```

### 3. Executando a Simulação

Para ver a tartaruga desenhando, você precisará de dois terminais abertos.

**Terminal 1: Iniciar o Simulador**

```
source /opt/ros/jazzy/setup.bash
ros2 run turtlesim turtlesim_node

```

**Terminal 2: Iniciar o Nó de Desenho**

```
cd ~/pond-prog
source install/setup.bash
ros2 run turtle_draw_project turtle_drawer

```

A tartaruga começará a teleportar sequencialmente, traçando o contorno do cachorro em tempo real sem deixar riscos internos na tela!


## Arquitetura e Decisões Técnicas

* **Processamento de Imagem:** Utilizou-se operações morfológicas manuais baseadas em NumPy para contornar limitações de detecção de bordas cruas. O preenchimento da silhueta garantiu que apenas os pixels mais externos fossem computados.
  
* **Planejamento de Caminho:** Uma adaptação do Problema do Caixeiro Viajante (TSP) usando o método do *Vizinho Mais Próximo* foi aplicada para ordenar os milhares de pontos gerados, garantindo que o robô faça um traçado lógico e contínuo.
  
* **Subamostragem:** Os pontos foram filtrados (1 a cada 3 pontos) para otimizar o tempo de execução do robô sem perder a fidelidade da imagem.
  
* **Teleporte vs. Velocidade Linear (`cmd_vel`):** Optou-se por usar requisições síncronas de serviço (`TeleportAbsolute`) em vez da publicação de velocidades. Isso contorna o problema físico da caneta da tartaruga, permitindo "levantar a caneta" virtualmente durante transições e garantindo um contorno limpo, atendendo aos requisitos estéticos do projeto.

# Vídeo de Demonstração

[Vídeo](https://drive.google.com/drive/folders/1SO32WX08pBuZq3k-zW39gF4N-YbHro__?usp=sharing)  
