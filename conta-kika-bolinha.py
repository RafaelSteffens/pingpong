import cv2
import numpy as np

# Vincular a webcam ao Python
webcam = cv2.VideoCapture(0)

# Definir intervalo y para a mesa (ajuste esses valores conforme necessário)
mesa_y_min = 300
mesa_y_max = 400

# Inicializar contador de colisões
colisoes = 0
bolinha_na_mesa = False
bolinha_acima_da_mesa = False

# Inicializar posições anteriores da bolinha
bola_x_anterior, bola_y_anterior = None, None

# Ajustar taxa de quadros da webcam
webcam.set(cv2.CAP_PROP_FPS, 60)

# O que aconteceria se ele não tivesse conseguido conectar com a webcam
if webcam.isOpened():
    while True:
        validacao, frame = webcam.read()
        
        if not validacao:
            break
        
        # Converter BGR (padrão do OpenCV) para HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Definir o intervalo para a cor laranja da bola de ping pong
        lower_orange = np.array([5, 150, 150])
        upper_orange = np.array([15, 255, 255])
        
        # Criar uma máscara para a cor laranja
        mask = cv2.inRange(hsv, lower_orange, upper_orange)
        
        # Aplicar suavização para reduzir o ruído
        mask = cv2.GaussianBlur(mask, (5, 5), 0)
        
        # Encontrar contornos na máscara
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Inicializar variáveis para a bola de ping pong
        bola_x, bola_y, bola_raio = None, None, None
        
        # Procurar pelo maior círculo (que deve ser a bola de ping pong)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 10:  # Filtrar pequenas áreas
                # Calcular o contorno da bola
                (x, y), radius = cv2.minEnclosingCircle(contour)
                center = (int(x), int(y))
                radius = int(radius)
                
                # Verificar se o contorno encontrado é o maior (bola de ping pong)
                if bola_raio is None or radius > bola_raio:
                    bola_x, bola_y, bola_raio = int(x), int(y), radius
        
        # Desenhar o círculo ao redor da bola de ping pong (se encontrada)
        if bola_raio is not None:
            # Verificar se a bolinha está em movimento
            if bola_x_anterior is not None and bola_y_anterior is not None:
                movimento_x = abs(bola_x - bola_x_anterior)
                movimento_y = abs(bola_y - bola_y_anterior)
                movimento = movimento_x + movimento_y
                if movimento > 2:  # Ajustar este valor conforme necessário
                    cv2.circle(frame, (bola_x, bola_y), bola_raio, (0, 255, 0), 2)
                    cv2.putText(frame, 'Bola de Ping Pong', (bola_x - 50, bola_y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                    
                    # Verificar se a bolinha está na mesa
                    if mesa_y_min <= bola_y <= mesa_y_max:
                        if bolinha_acima_da_mesa:
                            colisoes += 1
                            bolinha_na_mesa = True
                            bolinha_acima_da_mesa = False
                    else:
                        bolinha_na_mesa = False
                    
                    # Atualizar estado da bolinha em relação à mesa
                    if bola_y < mesa_y_min:
                        bolinha_acima_da_mesa = True
                    else:
                        bolinha_acima_da_mesa = False
            
            # Atualizar as posições anteriores da bolinha
            bola_x_anterior, bola_y_anterior = bola_x, bola_y
        
        # Desenhar o retângulo representando a mesa
        cv2.rectangle(frame, (0, mesa_y_min), (frame.shape[1], mesa_y_max), (255, 0, 0), 2)
        
        # Mostrar o contador de colisões
        cv2.putText(frame, f'Colisoes: {colisoes}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Mostrar o frame da webcam que o Python está vendo
        cv2.imshow("Video da Webcam", frame)
        
        # Mandar o Python esperar um pouquinho -> de um jeito inteligente
        tecla = cv2.waitKey(1)
        
        # Mandar ele parar o código se eu clicar no ESC
        if tecla == 27:
            break

# Primeiro problema -> Se ele continua conectado na webcam
webcam.release()
cv2.destroyAllWindows()
