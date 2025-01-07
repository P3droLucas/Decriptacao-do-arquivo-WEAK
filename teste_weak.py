from Cryptodome.Cipher import AES
import string
import time
from itertools import product
from multiprocessing import Pool

def is_texto_legivel(texto):
    """Verifica se o texto decifrado contém principalmente caracteres ASCII legíveis"""    
    try:
        # Verifica se o texto decodificado é ASCII printável
        v1 = all(ord(c) < 128 for c in texto.decode('ascii'))
        return v1
    except:
        return False

def tenta_decifrar(texto_cifrado, chave):
    """Tenta decifrar o texto com a chave fornecida"""
    cifra = AES.new(chave, AES.MODE_ECB)
    
    try:
        decifrado = cifra.decrypt(bytes.fromhex(texto_cifrado))
        return decifrado
    except:
        return None
def apply_async2(texto_cifrado, caracteres,prefixo_conhecido, cont, tempo_inicio, caracteres_prefixo):
    chaves_testadas = 0
    last_log_time = time.time()
    prefixo_conhecido2 = ""
    # Testa todas as combinações possíveis para os 5 caracteres restantes
    for x in caracteres_prefixo :
        prefixo_conhecido2 = prefixo_conhecido+ ''.join(x)
        for sufixo in product(caracteres, repeat=cont):
            chave = (prefixo_conhecido2 + ''.join(sufixo)).encode('ascii')
            #chave = (prefixo_conhecido + '3LUbU').encode('ascii')
            chaves_testadas += 1
            
             # Log a cada 60 segundos
            current_time = time.time()
            if current_time - last_log_time >= 60:
                print(f"Tentativas até agora: {chaves_testadas:,} | Última chave testada: {chave}")
                last_log_time = current_time
                
            decifrado = tenta_decifrar(texto_cifrado, chave)
            if decifrado and is_texto_legivel(decifrado):
                tempo_decorrido = time.time() - tempo_inicio
                print(f"\nPossível correspondência encontrada!")
                print(f"Chave: {chave}")
                print(f"Primeiros 100 bytes do texto decifrado: {decifrado[:100]}")
                print(f"\nTempo gasto: {tempo_decorrido:.2f} segundos")
                print(f"Chaves testadas: {chaves_testadas}")
                print(f"Taxa: {chaves_testadas/tempo_decorrido:.2f} chaves/seg")
                
                # Salva o texto decifrado se parecer válido
                with open('decifrado_weak_FINAL_2.txt', 'wb') as f:
                    f.write(decifrado)
                return
    print("Nenhuma chave válida encontrada")


def main():
    # Lê o texto cifrado
    with open('arquivo-weak-9.in-full.hex', 'r') as f:
        texto_cifrado = f.read().strip()

    # Parte conhecida da chave
    prefixo_conhecido = "SecurityAES"
    caracteres1 = "abcdefghi"
    caracteres11 = "jklmnopqr"
    caracteres12 = "stuvwxyz"
    caracteres2 = "ABCDEFGHI"
    caracteres21 = "JKLMNOPQR"
    caracteres22 = "STUVWXYZ"
    caracteres3 = "01234"
    caracteres31 = "56789"
    
    # Conjunto de caracteres para a parte desconhecida (4 caracteres)
    caracteres = string.ascii_letters + string.digits
    
    print(f"Iniciando ataque de força bruta...")
    tempo_inicio = time.time()
    print(f"Horário de início: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tempo_inicio))}")
   
    
    pool = Pool()
    #result = []
    #answer = []
    #for x in caracteres :
    #    temp = pool.apply_async(apply_async2, [texto_cifrado, caracteres,prefixo_conhecido, 4, tempo_inicio, x])    # evaluate "solve1(A)" asynchronously
    #    result.append(temp)
    #    answer.append(temp.get(1000))
    #    print(answer)
    #result11 = pool.apply_async(apply_async2, [texto_cifrado, caracteres,prefixo_conhecido, 4, tempo_inicio, caracteres11])    # evaluate "solve1(A)" asynchronously
    #result2 = pool.apply_async(apply_async2, [texto_cifrado, caracteres,prefixo_conhecido, 4, tempo_inicio, caracteres2])    # evaluate "solve2(B)" asynchronously
    #result21 = pool.apply_async(apply_async2, [texto_cifrado, caracteres,prefixo_conhecido, 4, tempo_inicio, caracteres21])    # evaluate "solve2(B)" asynchronously
    result3 = pool.apply_async(apply_async2, [texto_cifrado, caracteres,prefixo_conhecido, 4, tempo_inicio, caracteres3])
    #result31 = pool.apply_async(apply_async2, [texto_cifrado, caracteres,prefixo_conhecido, 4, tempo_inicio, caracteres31])
    #answer1 = result1.get(1000)
    #answer1 = result1.get(1000)
    #answer1 = result1.get(1000)
    #answer2 = result2.get(1000)
    #answer1 = result1.get(1000)
    #answer1 = result1.get(1000)
    answer3 = result3.get(1000)
    #answer31 = result31.get(1000)
    #print(answer1)
    #print(answer2)
    print(answer3)
    #print(answer3)
    #print(answer3)
    #print(answer3)
    #print(answer31)
    
if __name__ == "__main__":
    main()
