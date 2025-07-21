import zipfile
import os
import hashlib
import subprocess  # Добавляем модуль для выполнения команд

COMMIT = input("Введите коммит: ")
SERVER_PROPERTIES_PATH = r"D:\.servers\Marsh's Server\server.properties"
RESOURCEPACK_NAME = "resourcepack.zip"

def sha1(file_path):
    sha1 = hashlib.sha1()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha1.update(chunk)
    return sha1.hexdigest()

def sha1_update(properties_path, new_hash):
    updated_lines = []
    with open(properties_path, 'r') as f:
        for line in f:
            if line.startswith('resource-pack-sha1='):
                updated_lines.append(f'resource-pack-sha1={new_hash}\n')
            else:
                updated_lines.append(line)
    
    with open(properties_path, 'w') as f:
        f.writelines(updated_lines)

def run_git_commands(commit_message):
    """Выполняет Git-команды и выводит результат"""
    commands = [
        ["git", "add", "."],
        ["git", "commit", "-m", commit_message],
        ["git", "push"]
    ]
    
    for cmd in commands:
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"Команда {' '.join(cmd)} выполнена успешно")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при выполнении {' '.join(cmd)}:")
            print(e.stderr)
            return False
    return True

with zipfile.ZipFile(f"{RESOURCEPACK_NAME}", "w", zipfile.ZIP_DEFLATED) as zipf:
    if os.path.exists("./assets"):
        for root, dirs, files in os.walk("./assets"):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, ".")
                zipf.write(file_path, arcname)
    
    for file in ["pack.mcmeta", "pack.png"]:
        if os.path.exists(file):
            zipf.write(file, os.path.basename(file))

HASH = sha1(f"{RESOURCEPACK_NAME}")
print(f"ZIP created: {RESOURCEPACK_NAME}\nSHA1 generated: {HASH}")
# sha1_update(SERVER_PROPERTIES_PATH, HASH)

# Выполняем Git-команды
print("\nВыполняем Git-команды...")
if run_git_commands(COMMIT):
    print("\nВсе Git-операции выполнены успешно!")
else:
    print("\nПроизошла ошибка при выполнении Git-команд")