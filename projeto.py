import tkinter as tk
from tkinter import messagebox
from random import randint

# Configurações do jogo
TAMANHO_CAMPO = 30
LARGURA_CAMPO = 30
ALTURA_CAMPO = 20
DELAY = 100
ARQUIVO_PONTUACAO = "pontuacao.txt"

class JogoDaCobra(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Jogo da Cobra")
        self.geometry(f"{LARGURA_CAMPO * TAMANHO_CAMPO}x{ALTURA_CAMPO * TAMANHO_CAMPO}")

        self.canvas = tk.Canvas(self, bg="black", width=LARGURA_CAMPO * TAMANHO_CAMPO, height=ALTURA_CAMPO * TAMANHO_CAMPO)
        self.canvas.pack()

        self.snake = [(10, 10)]
        self.direction = (0, 1)  # Inicialmente movendo para baixo

        self.comida = self.criar_comida()

        self.bind("<KeyPress>", self.mover_cobra)

        self.pontuacao = 0
        self.carregar_pontuacao()

        self.fim_de_jogo_texto = None

        self.loop_jogo()

    # Loop principal do jogo
    def loop_jogo(self):
        self.movimentar_cobra()
        self.desenhar_cobra()
        self.desenhar_comida()

        if self.verificar_colisao():
            self.finalizar_jogo()
            return

        self.after(DELAY, self.loop_jogo)

    # Movimento da cobra
    def mover_cobra(self, event):
        if event.keysym == "Up" and self.direction != (0, 1):
            self.direction = (0, -1)
        elif event.keysym == "Down" and self.direction != (0, -1):
            self.direction = (0, 1)
        elif event.keysym == "Left" and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif event.keysym == "Right" and self.direction != (-1, 0):
            self.direction = (1, 0)

    # Movimento da cobra
    def movimentar_cobra(self):
        x, y = self.snake[0]
        dx, dy = self.direction
        novo_x = (x + dx) % LARGURA_CAMPO
        novo_y = (y + dy) % ALTURA_CAMPO

        if (novo_x, novo_y) in self.snake[1:]:
            self.finalizar_jogo()
            return

        self.snake.insert(0, (novo_x, novo_y))

        if (novo_x, novo_y) == self.comida:
            self.comida = self.criar_comida()
            self.pontuacao += 10
            self.atualizar_pontuacao()
        else:
            self.snake.pop()

    # Criação da comida
    def criar_comida(self):
        while True:
            x = randint(0, LARGURA_CAMPO - 1)
            y = randint(0, ALTURA_CAMPO - 1)
            if (x, y) not in self.snake:
                return x, y

    # Desenho da cobra
    def desenhar_cobra(self):
        self.canvas.delete("snake")
        for x, y in self.snake:
            self.canvas.create_rectangle(x * TAMANHO_CAMPO, y * TAMANHO_CAMPO,
                                          (x + 1) * TAMANHO_CAMPO, (y + 1) * TAMANHO_CAMPO,
                                          fill="green", tags="snake")

    # Desenho da comida
    def desenhar_comida(self):
        self.canvas.delete("comida")
        x, y = self.comida
        self.canvas.create_rectangle(x * TAMANHO_CAMPO, y * TAMANHO_CAMPO,
                                      (x + 1) * TAMANHO_CAMPO, (y + 1) * TAMANHO_CAMPO,
                                      fill="red", tags="comida")

    # Verificação de colisão
    def verificar_colisao(self):
        x, y = self.snake[0]
        return x < 0 or x >= LARGURA_CAMPO or y < 0 or y >= ALTURA_CAMPO

    # Finalização do jogo
    def finalizar_jogo(self):
        self.salvar_pontuacao()
        self.canvas.delete("all")
        self.fim_de_jogo_texto = self.canvas.create_text(LARGURA_CAMPO * TAMANHO_CAMPO // 2, ALTURA_CAMPO * TAMANHO_CAMPO // 2,
                                text=f"Fim de jogo! Pontuação: {self.pontuacao}", fill="white",
                                font=("Arial", 20, "bold"), justify="center")
        self.after(2000, self.reiniciar_jogo)

    # Reinício do jogo
    def reiniciar_jogo(self):
        if self.fim_de_jogo_texto:
            self.canvas.delete(self.fim_de_jogo_texto)
            self.fim_de_jogo_texto = None
        self.snake = [(10, 10)]
        self.direction = (0, 1)
        if self.keysym == "Up" and self.direction != (0, 1):
            self.direction = (0, -1)
        elif self.keysym == "Down" and self.direction != (0, -1):
         self.direction = (0, 1)
        elif self.keysym == "Left" and self.direction != (1, 0):
         self.direction = (-1, 0)
        elif self.keysym == "Right" and self.direction != (-1, 0):
         self.direction = (1, 0)
        self.comida = self.criar_comida()
        self.pontuacao = 0
        self.atualizar_pontuacao()
        self.loop_jogo()

    # Carregar pontuação salva
    def carregar_pontuacao(self):
        try:
            with open(ARQUIVO_PONTUACAO, "r") as file:
                self.pontuacao = int(file.read())
        except FileNotFoundError:
            self.pontuacao = 0

    # Salvar pontuação
    def salvar_pontuacao(self):
        with open(ARQUIVO_PONTUACAO, "w") as file:
            file.write(str(self.pontuacao))

    # Atualizar pontuação exibida
    def atualizar_pontuacao(self):
        self.title(f"Jogo da Cobra - Pontuação: {self.pontuacao}")

if __name__ == "__main__":
    JogoDaCobra().mainloop()
