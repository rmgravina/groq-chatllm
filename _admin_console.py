import json
import os
from dotenv import load_dotenv

load_dotenv()

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def write_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def print_usernames(users):
    for i, user in enumerate(users, 1):
        print(f"{i} - {user['username']}")

def remove_user(users, superusers, index):
    if 0 < index <= len(users):
        removed_user = users.pop(index - 1)
        # Remove from superusers
        superusers = [su for su in superusers if su['username'] != removed_user['username']]
        return True, users, superusers
    else:
        print("Opção inválida. Tente novamente.")
        return False, users, superusers


# only remove access

def load_secret_users():
    file_path = os.getenv('USERS_SECRETS_PATH')
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as file:
        secret_users = json.load(file)
    return secret_users

def load_admin_users():
    file_path = os.getenv('SUPERUSER_SECRETS_PATH')
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as file:
        admin_users = json.load(file)
    return admin_users

def save_admin_users(admin_users):
    file_path = os.getenv('SUPERUSER_SECRETS_PATH')                 
    with open(file_path, 'w') as file:
        json.dump(admin_users, file, indent=2)


def print_users(users):
    for i, user in enumerate(users, start=1):
        print(f"{i} - {user['username']};")

def make_admin(users, index):
    if 1 <= index <= len(users):
        user = users[index - 1]
        admin_user = {"username": user["username"], "email": user["email"]}
        return admin_user
    return None

def remove_admin(admin_users, index):
    if 1 <= index <= len(admin_users):
        del admin_users[index - 1]
        return True
    return False

def main_acess():
    while True:
        print("Escolha a opção:\n")
        print("1 - Conceder acesso à API")
        print("2 - Revogar acesso à API")
        print("0 - Sair\n")

        choice = input("Digite a opção desejada: ")

        if choice == '0':
            break
        elif choice == '1':
            secret_users = load_secret_users()
            print("Usuários disponíveis:")
            print_users(secret_users)

            user_index = int(input("\nEscolha o usuário que deseja dar permissão\n(Digite 0 para voltar ao menu principal): "))

            if user_index == 0:
                continue  # Volta ao menu principal
            admin_user = make_admin(secret_users, user_index)

            if admin_user:
                admin_users = load_admin_users()

                if admin_user in admin_users:
                    print(f"\n ### Usuário {admin_user['username']} já possui acesso. ###\n")
                    continue

                else:
                    admin_users.append(admin_user)
                    save_admin_users(admin_users)
                    print(f"Acesso concedido ao usuário: {admin_user['username']}.\n")
            
            else:
                print("Opção inválida.\n")

        elif choice == '2':
            admin_users = load_admin_users()
            print("Usuários autorizados:")
            print_users(admin_users)

            user_index = int(input("\nEscolha o usuário que deseja revogar\n(Digite 0 para voltar ao menu principal): "))
            if user_index == 0:
                continue  # Volta ao menu principal
            if remove_admin(admin_users, user_index):
                save_admin_users(admin_users)
                print("\nAcesso revogado com sucesso.\n")
            else:
                print("\nOpção inválida.\n")

        else:
            print("\nOpção inválida. Tente novamente.\n")


def main_remove():
    user_file_path = os.getenv('USERS_SECRETS_PATH')
    superuser_file_path = os.getenv('SUPERUSER_SECRETS_PATH')

    users = read_json_file(user_file_path)
    superusers = read_json_file(superuser_file_path)

    while True:
        print("\nUsuários disponíveis:\n")
        print_usernames(users)
        print("\n(Digite '0' para sair)\n")
        choice = int(input("Escolha o número do usuário que deseja remover: "))

        if choice == 0:
            break

        success, users, superusers = remove_user(users, superusers, choice)

        if success:
            print("\nUsuário removido com sucesso!")
        else:
            print("\nFalha ao remover o usuário.")

    write_json_file(user_file_path, users)
    write_json_file(superuser_file_path, superusers)

if __name__ == "__main__":
    while True:
            
        print("O que você deseja fazer?\n")
        opcao = input("1 - Cadastrar/Revogar acesso à API\n2 - Remover cadastro de usuário\n0 - Sair\n\nDigite a opção desejada: ")

        if opcao == '1':
            main_acess()
        elif opcao == '2':
            main_remove()
        elif opcao == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.\n\n")



