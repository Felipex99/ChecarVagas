import cv2  # Importa a biblioteca OpenCV para manipulação de imagens e eventos do mouse
import pickle  # Importa a biblioteca pickle para salvar e carregar dados (neste caso, posições de vagas de estacionamento)

# Define a largura e altura de cada vaga de estacionamento
width, height = 107, 48

# Tenta carregar as posições de estacionamento salvas anteriormente
try:
    with open('CarParkPos', 'rb') as f:  # Abre o arquivo 'CarParkPos' no modo de leitura binária
        posList = pickle.load(f)  # Carrega a lista de posições de vagas de estacionamento a partir do arquivo
except:  # Se ocorrer um erro (por exemplo, o arquivo não existir)
    posList = []  # Inicializa uma lista vazia para armazenar as posições das vagas

# Função que trata os eventos do mouse (clicar para adicionar ou remover vagas)
def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:  # Se o botão esquerdo do mouse for pressionado
        posList.append((x, y))  # Adiciona a posição do clique (x, y) à lista de vagas
    if events == cv2.EVENT_RBUTTONDOWN:  # Se o botão direito do mouse for pressionado
        for i, pos in enumerate(posList):  # Itera sobre as posições das vagas na lista
            x1, y1 = pos  # Pega as coordenadas da vaga armazenada na lista
            # Verifica se o clique está dentro da vaga selecionada
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)  # Remove a vaga da lista se o clique estiver dentro dos limites da vaga

    # Salva a lista de vagas atualizada no arquivo 'CarParkPos'
    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)

# Loop principal do programa
while True:
    # Carrega a imagem do estacionamento a partir do arquivo 'carParkImg.png'
    img = cv2.imread('carParkImg.png')
    
    # Desenha retângulos nas posições das vagas de estacionamento salvas
    for pos in posList:  # Itera sobre cada posição na lista de vagas
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)  # Desenha um retângulo roxo na imagem

    # Mostra a imagem com os retângulos das vagas no display
    cv2.imshow("Image", img)
    
    # Define a função 'mouseClick' como callback para eventos do mouse na janela de imagem
    cv2.setMouseCallback("Image", mouseClick)
    
    # Espera por uma tecla para continuar o loop (a cada 1 milissegundo)
    cv2.waitKey(1)
