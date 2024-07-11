import cv2
import numpy as np

# vincular a webcam ao python
webcam = cv2.VideoCapture(0) # cria a conexão com a webcam (0)= indice da webcam a ser usada

# o que aconteceria se ele não tivesse conseguido conectar com a webcam
if webcam.isOpened():
    # vou ler a minha webcam (webcam.read())
    validacao, frame = webcam.read()
    # segundo problema -> entender o que é o webcam.read() -> 1 frame
    
    #temos que fazer ele pegar vários frames ENTÃO precisamos de um loop infinito
    while validacao:
        # pegar o próximo frame da tela
        validacao, frame = webcam.read()
        
        # converter BGR (padrão do opencv) para HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # definir o intervalo para a cor laranja da bola de ping pong
        lower_orange = np.array([5, 150, 150])
        upper_orange = np.array([15, 255, 255])
        
        # criar uma máscara para a cor laranja
        mask = cv2.inRange(hsv, lower_orange, upper_orange)
        
        # encontrar contornos na máscara
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # inicializar variáveis para a bola de ping pong
        bola_x, bola_y, bola_raio = None, None, None
        
        # procurar pelo maior círculo (que deve ser a bola de ping pong)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 10:  # filtrar pequenas áreas
                # calcular o contorno da bola
                (x, y), radius = cv2.minEnclosingCircle(contour)
                center = (int(x), int(y))
                radius = int(radius)
                
                # verificar se o contorno encontrado é o maior (bola de ping pong)
                if bola_raio is None or radius > bola_raio:
                    bola_x, bola_y, bola_raio = int(x), int(y), radius
        
        # desenhar o círculo ao redor da bola de ping pong (se encontrada)
        if bola_raio is not None:
            cv2.circle(frame, (bola_x, bola_y), bola_raio, (0, 255, 0), 2)
            cv2.putText(frame, 'Bola de Ping Pong', (bola_x - 50, bola_y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
        # mostrar o frame da webcam que o python ta vendo
        cv2.imshow("Video da Webcam", frame)
        
        # mandar o python esperar um pouquinho -> de um jeito inteligente
        tecla = cv2.waitKey(1)
        
        # mandar ele parar o código se eu clicar no ESC
        if tecla == 27:
            break

# primeiro problema -> Se ele continua conectado na webcam
webcam.release()
cv2.destroyAllWindows()
