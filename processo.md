# Documentação do Projeto

## 1. Objetivo
Este projeto visa converter uma imagem estática (silhueta de um cachorro) em uma série de comandos de movimento para o robô `turtlesim` no ROS 2. O pipeline envolve processamento digital de imagens, extração de contornos e planejamento de trajetória com detecção de saltos.

## 2. Pipeline de Processamento de Imagem
O processamento foi implementado do zero (sem depender apenas de funções prontas de alto nível sempre que possível) para demonstrar os conceitos de Visão Computacional:

*   **Redimensionamento**: A imagem original é reduzida para facilitar o processamento e adequar a densidade de pontos.
*   **Conversão para Cinza**: Transformação do espaço de cor BGR para tons de cinza usando a fórmula de luminância: $Y = 0.299R + 0.587G + 0.114B$.
*   **Suavização (Blur)**: Aplicação de um Kernel Gaussiano 3x3 para reduzir ruídos que poderiam gerar bordas falsas.
*   **Detecção de Bordas (Sobel)**: Cálculo do gradiente horizontal e vertical para identificar variações bruscas de intensidade.
*   **Binarização (Limiarização)**: Conversão da imagem de gradientes em uma máscara binária (preto e branco), onde os pixels brancos representam o contorno a ser desenhado.

## 3. Planejamento de Trajetória
Para que a tartaruga desenhe de forma eficiente, os pontos brancos foram organizados:

1.  **Mapeamento de Coordenadas**: As coordenadas de pixels $(linha, coluna)$ são convertidas para o espaço cartesiano do Turtlesim $(1.0, 11.0)$.
2.  **Ordenação por Proximidade**: Utiliza-se uma lógica de 'vizinho mais próximo' para minimizar o deslocamento da tartaruga.
3.  **Detecção de Saltos**: Caso a distância entre dois pontos consecutivos seja muito grande (indicando partes desconectadas da imagem), um marcador `None,None` é inserido no arquivo para sinalizar que a caneta deve ser levantada.

## 4. Integração com ROS 2
O arquivo gerado `caminho_turtlesim.txt` serve como entrada para um nó ROS 2. O comportamento esperado do nó é:

*   **Teleporte Inicial**: Mover-se para o primeiro ponto com a caneta desligada para evitar a linha vinda do centro.
*   **Serviço SetPen**: Alternar o estado da caneta (`off: 1` para saltos, `off: 0` para desenhar).
*   **Serviço TeleportAbsolute**: Comandar o movimento da tartaruga ponto a ponto.