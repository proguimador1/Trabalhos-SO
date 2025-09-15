import tkinter as tk
import cv2
from PIL import Image, ImageTk

class VideoPlayer:
    """
    Classe responsável por criar uma subtela que exibe vídeo,
    com botões para selecionar, reproduzir e pausar.
    """

    def __init__(self, parent, title, path):
        """
        Inicializa os componentes gráficos da subtela.

        Args:
            parent: janela principal ou frame.
            title: título da subtela.
            path: caminho para o vídeo.
        """
        self.path = path        # Atributo que contém o caminho até o arquivo de vídeo
        self.cap = None         # Objeto de captura de vídeo 
        self.playing = False    # Controle de reprodução

        # Frame que agrupa o player
        frame = tk.LabelFrame(parent, text=title)
        frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Área onde o vídeo será exibido
        self.video_label = tk.Label(frame)
        self.video_label.pack()

        # Botões de controle
        tk.Button(frame, text="Selecionar Vídeo", command=self.select_video).pack(fill=tk.X)
        tk.Button(frame, text="Reproduzir", command=self.play_video).pack(fill=tk.X)
        tk.Button(frame, text="Pausar", command=self.pause_video).pack(fill=tk.X)

    def select_video(self):
        """
        Abre uma janela para o usuário selecionar um arquivo de vídeo
        e inicializa o objeto de captura (cv2.VideoCapture).
        """
        
        self.cap = cv2.VideoCapture(self.path)

    def play_video(self):
        """
        Inicia a reprodução do vídeo, se houver vídeo carregado.
        Chama update_frame para atualizar os frames na tela.
        """
        if self.cap and not self.playing:
            self.playing = True
            self.update_frame()

    def pause_video(self):
        """
        Pausa a reprodução do vídeo (não avança mais os frames).
        """
        self.playing = False

    def update_frame(self):
        """
        Lê o próximo frame do vídeo e atualiza a imagem exibida.
        É chamada de forma recorrente usando after() do Tkinter.
        """
        if self.playing and self.cap:
            ret, frame = self.cap.read()
            if ret:
                # Converte frame de BGR (OpenCV) para RGB (Tkinter/PIL)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Converte para objeto que o Tkinter entende
                img = ImageTk.PhotoImage(Image.fromarray(frame).resize((320, 240)))

                # Exibe a imagem no label
                self.video_label.imgtk = img
                self.video_label.config(image=img)

                # Agenda a próxima atualização(30 fps)
                self.video_label.after(30, self.update_frame)
            else:
                # Se acabou o vídeo, para a reprodução
                self.playing = False


root = tk.Tk()

# Cria dois players independentes
path1 = "./video1.mp4"
path2 = "./video2.mp4"

VideoPlayer(root, "Vídeo 1", path1)
VideoPlayer(root, "Vídeo 2", path2)

root.mainloop()
