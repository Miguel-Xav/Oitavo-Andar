#imports básicos de pacotes de fora e funções que eu fiz para comunicar com o SQLite
import commsqlite3
import time
import re
import tabulate

from commsqlite3 import adicionar_mor

#Lista de ações que o usuário pode ter ao longo da jornada
lista_principal = ['Residências', 'Informações de pessoas', 'Sair']
lista_op_res = ["Adicionar residência", "Editar residência", "Remover residência", "Navegar pela lista"]
lista_op_mor = ["Adicionar morador", "Editar morador", "Remover morador", "Navegar pela lista"]



#Classes pra ficar mais fácil daqui pra frente
class Morador:
    def __init__(self, id_mor, nome_mor, idade, residencia):
        self.id_mor = id_mor
        self.nome_mor = nome_mor
        self.idade = idade
        self.residencia = residencia

class Residencia:
    def __init__(self, id_res, nome_res, endereco, cep):
        self.id_res = id_res
        self.nome_res = nome_res
        self.endereco = endereco
        self.cep = cep

#Coloquei isso aqui pra não ter que ficar criando essa variável toda hora dentro do código
lista_res = commsqlite3.listar_res()


#Validador de CEP tá aqui pra não causar erro de circulação de importação
def validar_cep(cep):
    return bool(re.fullmatch(r'\d{8}', cep))


#API que vai conversar com o usuário e o SQLite, corpo principal do código
def menu_principal():
    commsqlite3.get_db_connection()
    commsqlite3.criar_tabela_mor()
    commsqlite3.criar_tabela_res()
    print("Seja bem vindo ao Oitavo Andar!")
    time.sleep(1)
    print ("Aqui você poderá gerenciar residências e informaões de pessoas.")
    time.sleep(1)

    while True:
        print ("\nMenu principal:")
        print ('Você deseja realizar qual operação? (para voltar para este menu principal digite "sair")')
        time.sleep(1)
        for indice, item in enumerate(lista_principal, start=1):
            print (f"{indice}. {item}")
        escolha_principal = input(": ").lower()

        if escolha_principal == "1":
                menu_res()

        elif escolha_principal == "2":
            menu_mor()

        elif escolha_principal == "sair":
            break

        else:
            print ("Digite uma opção válida!")


def menu_res():
    while True:
        time.sleep(1)
        print("Escolha entre uma das opções:")
        for indice, item in enumerate(lista_op_res, start=1):
            print(f"{indice}. {item}")
        escolha_op_res = input(": ").lower()

        if escolha_op_res == "1":
            nome_res = input("Qual o nome da residência?: ")
            endereco = input("Qual o endereço da residência (Ex: Rua Oito, 420): ")
            while True:
                cep: str = input("Qual o CEP?: ")
                if validar_cep(cep):
                    break
                else:
                    print("CEP inválido!, certifique que são 8 dígitos de apenas números.")
            residencia_obj = Residencia(None, nome_res, endereco, cep)
            while True:
                nome_mor = input("Qual o principal morador (se não tiver deixe em branco): ")
                if commsqlite3.checar_morador(nome_mor):
                    break
                else:
                    escolha_cad_mor = input("Morador não encontrado! Deseja cadastra-lo? y/n")
                    if escolha_cad_mor == "y":
                        nome_mor = input("Qual o nome do morador? ")
                        idade = input("Qual é a idade do morador? ")
                        res = input("Qual o nome da residência?")
                        break
                    if escolha_cad_mor == "n":
                        break
            commsqlite3.adicionar_res(residencia_obj.nome_res, residencia_obj.endereco, residencia_obj.cep)
            commsqlite3.adicionar_mor(nome_mor, idade, res)
            print(f"A residência '{nome_res}' adicionada com sucesso!")
            print(f"Guarde o número do ID da residência '{nome_res}': {commsqlite3.id_res()}.")
            break


        elif escolha_op_res == "2":
            print(tabulate.tabulate(commsqlite3.listar_res(), headers=['ID', 'Nome', 'Endereço', 'CEP', 'Morador']))
            id_res = input(
                "Qual o ID da residência que você deseja editar? (se não quiser editar tal informação só coloque do jeito que você quer deixar) : ")
            novo_nome_res = input("Digite o novo nome de sua residência: ")
            time.sleep(1)
            novo_endereco = input("Digite o novo endereço de sua residência: ")
            time.sleep(1)
            while True:
                novo_cep = input("Digite o novo CEP de sua residência: ")
                if validar_cep(novo_cep):
                    time.sleep(1)
                    break
                else:
                    print("CEP inválido, certifique que são 8 digitos de apenas números!")

            novo_morador = input("Digite o novo principal morador de sua residência: ")

            print("Computando as informações...")
            time.sleep(2)

            commsqlite3.criar_tabela_mor(id_res, novo_nome_res, novo_endereco, novo_cep, novo_morador)

            print("Ação realizada com sucesso! Voltando ao menu principal...")
            time.sleep(1)
            break


        elif escolha_op_res == "3":
            for item in lista_res:
                print(f"ID: {item[0]}, Nome: {item[1]}, Endereço: {item[2]}, CEP: {item[3]}, Morador: {item[4]}")
            try:
                id_res = int(input("Qual o ID da residência que você quer excluir?: "))
                commsqlite3.deletar_res(id_res)
                print("A operação foi concluida com sucesso! Voltando ao menu principal...")
            except ValueError:
                print("ID inválido! Por favor insira um ID válido.")
            except Exception as e:
                print(f"A operação falhou, tente novamente ou entre em contato com o suporte. Erro {e}")
            time.sleep(2)
            menu_principal()

        elif escolha_op_res == "4":
            while True:
                print("Aqui está a tabela de residências: ")
                print(tabulate.tabulate(commsqlite3.listar_res(), headers=['ID', 'Nome', 'Endereço', 'CEP', 'Morador']))
                voltar_menu_nav = input('Digite "S" para voltar ao menu principal ').lower()
                if voltar_menu_nav == "s":
                    break
        elif escolha_op_res == "sair":
            break

        else:
            print("Digite uma opção válida!")


def menu_mor():
    while True:
        time.sleep(1)
        print ("Escolha uma das opções: ")
        for indice, item in enumerate(lista_op_mor, start=1):
            print (f"{indice}. {item}")
        escolha_op_mor = input(": ")

        if escolha_op_mor == "1":
            nome_mor = input("Qual o nome do morador? ")
            idade = input("Qual é a idade do morador? ")
            while True:
                res_mor = input("Qual o residência do morador? ")
                if commsqlite3.checar_residencia(res_mor):
                    print ("Cadastro concluido!")
                    break
                else:
                    print ("Residência não encontrada.")
                    escolha_cad_res = input("Você deseja cadastrar uma residência? y/n")
                    if escolha_cad_res == "y":
                        nome_res = input("Qual o nome da residência?: ")
                        endereco = input("Qual o endereço da residência (Ex: Rua Oito, 420): ")
                        while True:
                            cep: str = input("Qual o CEP?: ")
                            if validar_cep(cep):
                                break
                            else:
                                print("CEP inválido!, certifique que são 8 dígitos de apenas números.")
                        residencia_obj = Residencia(None, nome_res, endereco, cep)
                        nome_mor = input("Qual o principal morador (se não tiver deixe em branco): ")
                        if nome_mor.strip():
                            idade = input("Qual a idade do morador?: ")
                            morador_obj = Morador(None, nome_mor, idade, residencia_obj)
                        else:
                            morador_obj = None
                        commsqlite3.adicionar_res(residencia_obj.nome_res, residencia_obj.endereco, residencia_obj.cep,
                                                  morador_obj)
                        print(f"A residência '{nome_res}' adicionada com sucesso!")
                        print(f"Guarde o número do ID da residência '{nome_res}': {commsqlite3.id_res()}.")
                        break
                    elif escolha_cad_res == "n":
                        print ("Morador sem residência irá ser cadastrado.")
                        time.sleep(1)
                        break

            adicionar_mor(nome_mor, idade, res_mor)
            print ("Morador cadastrado com sucesso!")
            time.sleep(1)
            menu_principal()


        elif escolha_op_mor == "2":
            while True:
                print (tabulate.tabulate(commsqlite3.listar_mor(), headers = ['ID', 'Nome', 'Idade', 'Residência']))
                id_mor = input("Qual o ID do morador que você desja editar? (se não quiser editar tal informação só coloque do jeito que você quer deixar) : ")
                time.sleep(1)
                novo_nome_mor = input("Qual o nome do morador?: ")
                time.sleep(1)
                nova_idade_mor = input("Qual a idade do morador?: ")
                time.sleep(1)
                nova_res_mor = input ("Qual o nome da residência do morador?: ")
                commsqlite3.edit_mor(id_mor, novo_nome_mor, nova_idade_mor, nova_res_mor)

                print (tabulate.tabulate(id_mor, novo_nome_mor, nova_idade_mor, nova_res_mor, headers = ['ID', 'Nome', 'Idade', 'Residência']))

                escolha_3 = input("A edição está do jeito que vocẽ gostaria? y/n: ")
                if escolha_3 == "y":
                    print ("Operação concluida com sucesso! Voltando ao menu principal... ")
                    time.sleep(1)
                    menu_principal()
                elif escolha_3 == "n":
                    continue


        elif escolha_op_mor == "3":
            print (tabulate.tabulate(commsqlite3.listar_mor(), headers = ['ID', 'Nome', 'Idade', 'Residência']))

            try:
                id_mor = input("Qual o ID do morador que você deseja excluir?: ")
                commsqlite3.deletar_mor(id_mor)
                print ("Morador excluido com sucesso! Voltando ao menu principal...")
            except ValueError:
                print ("ID inválido! Digite novamente um válido")
            except Exception as e:
                print (f"A operação falhou! Tente novamente ou entre em contato com o suporte. Erro: {e}")
            time.sleep(1)
            menu_principal()


        elif escolha_op_mor == "4":
            while True:
                print (tabulate.tabulate(commsqlite3.listar_mor(), headers = ['ID', 'Nome', 'Idade', 'Residência']))
                voltar_menu = input('Digite "v" para voltar ao menu principal: ')
                if voltar_menu == "v":
                    print ("Voltando ao menu principal...")
                    time.sleep(1)
                    menu_principal()
                else:
                    print ('Digite um número válido!')


#Chamando a função main(), chamaa :fire: :fire:
menu_principal()


