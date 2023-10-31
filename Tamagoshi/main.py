import random
import time
import os
from tkinter import *

# Codigo para a janela/foto de perfil
window = Tk()
window.geometry("381x654")
window.title("Foto de Perfil")
imagemNormal = PhotoImage(file="imagens/polvinho.png")
imagemGuerreiro = PhotoImage(file="imagens/polvinhoEspada.png")

label_normal = Label(window, image=imagemNormal)
label_guerreiro = Label(window, image=imagemGuerreiro)


# ---------------------------- Classe ----------------------------
class Tamagotchi:

  def __init__(self, nome):
    self.nome = nome
    self.fome = 100  # --> 100 nao tem fome 0 muita fome
    self.sede = 100  # --> 100 nao tem sede 0 muita sede
    self.felicidade = 100  # --> 0 triste 100 muito feliz
    self.energia = 100  # --> 0 muito cansado 100 muito bem
    self.limpo = 100  # --> 0 muito sujo 100 muito limpinho
    self.vida = 100  # --> vida do pet para o combate
    self.vidam = random.randint(50, 100)  # --> vida do monstro para o combate

  def stats(self):
    print("\n========Stats========")
    print(f"Nome: {self.nome}")
    print(f"Fome: {self.fome}")
    print(f"Felicidade: {self.felicidade}")
    print(f"Sede: {self.sede}")
    print(f"Energia: {self.energia}")
    print(f"Banho: {self.limpo}")
    print("=====================")

  def alimentar(self):
    self.fome += 20
    self.sede += 20
    self.limpo -= 5
    self.verificar()
    print("Esta refeição estava mesmo boa!")

  def brincar(self):
    self.felicidade += 20
    self.fome -= 5
    self.sede -= 5
    self.energia -= 10
    self.limpo -= 10
    self.verificar()
    print("Gostei muito de brincar!")

  def combateV(self):
    self.felicidade += 50
    self.fome -= 20
    self.sede -= 20
    self.energia -= 30
    self.limpo -= 20
    self.verificar()

  def combateD(self):
    self.felicidade -= 50
    self.fome -= 20
    self.sede -= 20
    self.energia -= 60
    self.limpo -= 80
    self.verificar()

  def atacar(self):
    dano = random.randint(5, 10)
    return dano

  def descansar(self):
    noite = random.randint(0, 100)
    if noite >= 50:
      # dormiu bem
      self.energia = 100
      print("Dormi mesmo bem!")
    else:
      # dormiu menos bem
      self.energia += random.randint(50, 90)
      print("Não dormi assim tão bem.")
    self.fome -= 5
    self.verificar()

  def banho(self):
    self.limpo = 100
    self.verificar()
    print("Que banho bom!")

  def tempo(self):
    self.fome -= 10
    self.sede -= 10
    self.energia -= 10
    self.limpo -= 10
    self.felicidade -= 10
    self.verificar()

  def verificar(self):
    if self.fome < 0:
      self.fome = 0

    if self.fome > 100:
      self.fome = 100

    if self.felicidade < 0:
      self.felicidade = 0

    if self.felicidade > 100:
      self.felicidade = 100

    if self.sede < 0:
      self.sede = 0

    if self.sede > 100:
      self.sede = 100

    if self.energia > 100:
      self.energia = 100

    if self.energia < 0:
      self.energia = 0

    if self.limpo > 100:
      self.limpo = 100

    if self.limpo < 0:
      self.limpo = 0

  def vivo(self):
    return self.fome > 0 and self.sede > 0


# ---------------------------- Funcoes ----------------------------
def salvar_jogo(pet):
  with open("savegame.sav", "w") as file:
    file.write(
        f"{pet.nome}\n{pet.fome}\n{pet.sede}\n{pet.energia}\n{pet.limpo}\n{pet.felicidade}"
    )


def carregar_jogo():
  try:
    with open("savegame.sav", "r") as file:
      nome = file.readline().strip()
      fome = int(file.readline().strip()
                 )  # o .strip() remove qualquer espaco em branco
      sede = int(file.readline().strip())
      energia = int(file.readline().strip())
      limpo = int(file.readline().strip())
      felicidade = int(file.read().strip())
      pet = Tamagotchi(nome)
      pet.fome = fome
      pet.sede = sede
      pet.energia = energia
      pet.limpo = limpo
      pet.felicidade = felicidade
      print(f"Jogo de {pet.nome} carregado")
      return pet
  except FileNotFoundError:
    print("Não há jogo salvo")
    return None


def mostrar_imagem(imagem):
  label_normal.pack_forget()
  label_guerreiro.pack_forget()
  imagem.pack()


# ---------------------------- Jogo ----------------------------
# Aqui comeca o jogo
pet = carregar_jogo()

if pet is None:
  nome = input("Dá um nome ao teu Tamagotchi: ")
  pet = Tamagotchi(nome)

while pet.vivo():
  mostrar_imagem(label_normal)
  fazer = int(
      input(
          "\nO que queres fazer?\n[1]-Ver Stats\n[2]-Alimentar\n[3]-Brincar\n[4]-Descansar\n[5]-Tomar Banho\n[6]-Lutar\n[7]-Salvar Jogo\n[0]-sair\nOpcao: "
      ))
  if fazer == 1:
    pet.stats()
    pet.tempo()
  elif fazer == 2:
    pet.alimentar()
  elif fazer == 3:
    pet.brincar()
  elif fazer == 4:
    pet.descansar()
  elif fazer == 5:
    pet.banho()
  elif fazer == 6:
    mostrar_imagem(label_guerreiro)
    inimigo = Tamagotchi("Inimigo")

    print("\nBem-vindo à Arena! Prepare-se para enfrentar o primeiro monstro!")

    # Loop da batalha
    while pet.vida > 0 and inimigo.vidam > 0:
      print("\nEscolha sua ação:")
      print("[1] Atacar")
      print("[2] Heal")
      print("[3] Fugir")
      escolha = input()

      if escolha == "1":
        # Ataca o inimigo
        dano_do_pet = pet.atacar()
        inimigo.vidam -= dano_do_pet
        print(f"{pet.nome} atacou o inimigo e causou {dano_do_pet} de dano.")

        # Inimigo Ataca
        if inimigo.vidam > 0:
          dano_do_inimigo = inimigo.atacar()
          pet.vida -= dano_do_inimigo
          print(f"O inimigo atacou e causou {dano_do_inimigo} de dano.")

      # Heal para o pet
      elif escolha == "2":
        vida_recuperada = random.randint(5, 10)
        pet.vida += vida_recuperada
        if pet.vida > 100:
          pet.vida = 100
        if pet.vida < 0:
          pet.vida = 0        
        print(f"{pet.nome} recoperou {vida_recuperada}.")

      elif escolha == "3":
        print(f"{pet.nome} fugiu da batalha.")
        break
      else:
        print("Escolha inválida. Tente novamente.")

      print(f"\nVida restante do jogador: {pet.vida}")
      print(f"Vida restante do inimigo: {inimigo.vidam}")

    # Verifica o resultado da batalha
    if pet.vida <= 0:
      print(f"{pet.nome} foi derrotado.")
      pet.combateD()
    elif inimigo.vidam <= 0:
      print("O inimigo morreu!")
      pet.combateV()

  elif fazer == 7:
    salvar_jogo(pet)
    print("Jogo Salvo")
  elif fazer == 0:
    break
  else:
    mostrar_imagem(label_normal)
    print("Opcao invalida!")
  time.sleep(2)
  os.system("cls")

if not pet.vivo():
  print(f"{pet.nome} morreu.")
  os.remove("savegame.sav")

window.mainloop()  # para manter a janela aberta durante o programa
