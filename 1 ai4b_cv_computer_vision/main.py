import cv2  # Biblioteca OpenCV para manipulação de imagens e vídeos
import pickle  # Biblioteca pickle para carregar posições de vagas salvas
import cvzone  # Biblioteca cvzone para sobrepor texto e retângulos de forma mais fácil
import numpy as np  # Biblioteca numpy para manipulações de arrays e operações matemáticas

# Iniciando o vídeo do estacionamento
cap = cv2.VideoCapture('carPark.mp4')  # Carregando o vídeo do estacionamento

# Carregando as posições de vagas salvas previamente
with open('CarParkPos', 'rb') as f:  # Abre o arquivo 'CarParkPos' no modo leitura binária
    posList = pickle.load(f)  # Carrega a lista de posições de vagas de estacionamento

# Definindo as dimensões das vagas de estacionamento
width, height = 107, 48

# Função para verificar se as vagas estão livres ou ocupadas
def checkParkingSpace(imgPro):
    spaceCounter = 0  # Contador de vagas livres

    for pos in posList:  # Itera sobre todas as posições de vagas salvas
        x, y = pos  # Extrai as coordenadas x e y da vaga

        # Recorta a imagem processada para a área da vaga atual
        imgCrop = imgPro[y:y + height, x:x + width]
        
        # Conta o número de pixels brancos (indicando que a vaga está livre)
        count = cv2.countNonZero(imgCrop)  # Conta o número de pixels não-zero (brancos)
        
        # Se o número de pixels brancos for menor que 870, considera a vaga como livre
        if count < 870:
            color = (0, 255, 0)  # Verde para vagas livres
            thickness = 5  # Maior espessura para vagas livres
            spaceCounter += 1  # Incrementa o contador de vagas livres
        else:
            color = (0, 0, 255)  # Vermelho para vagas ocupadas
            thickness = 2  # Menor espessura para vagas ocupadas

        # Desenha um retângulo ao redor da vaga com a cor apropriada
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        
        # Adiciona o número de pixels brancos na vaga, sobreposto na imagem
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1, thickness=2, offset=0, colorR=color)

    # Adiciona o número total de vagas livres na parte superior da imagem
    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3, thickness=5, offset=20, colorR=(0, 200, 0))

# Loop principal do programa
while True:
    # Verifica se o vídeo chegou ao fim; se sim, reinicia o vídeo
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reseta o vídeo para o primeiro quadro

    # Lê o próximo quadro do vídeo
    success, img = cap.read()
    
    # Converte o quadro para escala de cinza
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Aplica desfoque gaussiano à imagem
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    
    # Aplica limiarização adaptativa à imagem desfocada
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    
    # Aplica um filtro mediano para reduzir o ruído
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    
    # Cria um kernel (matriz) para a operação de dilatação
    Kernal = np.ones((3, 3), np.uint8)
    
    # Aplica dilatação à imagem para engrossar as bordas
    imgDilate = cv2.dilate(imgMedian, Kernal, iterations=1)
    
    # Chama a função para verificar o status das vagas, passando a imagem dilatada
    checkParkingSpace(imgDilate)
    
    # Mostra a imagem processada com os retângulos e o contador de vagas
    cv2.imshow("Image", img)
    
    # Espera 1 milissegundo antes de continuar o loop
    cv2.waitKey(1)
