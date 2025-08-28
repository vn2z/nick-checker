import requests
import string
import os
import random
import time
import threading
import queue

THREADS = 10
OUTPUT_DIR = "saida_nicks/minecraft"
DELAY = 0.3  


nick_queue = queue.Queue()
os.makedirs(OUTPUT_DIR, exist_ok=True)

def verificar_nick(nick):
    """
    Usa API Mojang para verificar se nick está disponível
    """
    url = f"https://api.mojang.com/users/profiles/minecraft/{nick}"
    try:
        r = requests.get(url, timeout=10)
        return r.status_code == 404 
    except Exception as e:
        print(f"[ERRO] {e}")
    return False

def salvar_nick(nick):
    """
    Salva nick disponível em arquivo
    """
    tamanho = len(nick)
    arquivo = os.path.join(OUTPUT_DIR, f"{tamanho}l.txt")
    with open(arquivo, "a", encoding="utf-8") as f:
        f.write(nick + "\n")

def worker():
    while not nick_queue.empty():
        nick = nick_queue.get()
        print(f"Testando: {nick}")
        if verificar_nick(nick):
            print(f"[DISPONÍVEL] {nick}")
            salvar_nick(nick)
        time.sleep(DELAY)
        nick_queue.task_done()

def gerar_combinacoes(tamanho, quantidade=5000):
    """
    Gera combinações aleatórias de nicks
    """
    chars = string.ascii_lowercase
    while quantidade > 0:
        nick = "".join(random.choice(chars) for _ in range(tamanho))
        if not nick.startswith("a"): 
            nick_queue.put(nick)
            quantidade -= 1

def main():
    print("Escolha o tipo de nick que deseja buscar no Minecraft:")
    print("1 - 3 letras/números")
    print("2 - 4 letras/números")
    print("3 - 5 letras/números")
    opcao = input("Digite sua escolha (1/2/3): ")

    if opcao == "1":
        tamanho = 3
    elif opcao == "2":
        tamanho = 4
    elif opcao == "3":
        tamanho = 5
    else:
        print("Opção inválida!")
        return

    qtd = int(input("Quantos nicks aleatórios deseja gerar para testar? "))

    print(f"[*] Gerando {qtd} nicks de {tamanho} caracteres...")
    gerar_combinacoes(tamanho, qtd)
    print(f"[*] Total de nicks na fila: {nick_queue.qsize()}")

    threads = []
    for _ in range(THREADS):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("[*] Finalizado!")
    input("Pressione ENTER para sair...")  

if __name__ == "__main__":
    main()
