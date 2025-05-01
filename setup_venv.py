#%%
#!/usr/bin/env python3
import os
import sys
import subprocess
import venv

def create_and_install_venv():
    """
    Crea un entorno virtual (venv) en el directorio 'venv' si no existe,
    instala las dependencias definidas en 'requirements.txt' y re-ejecuta
    el script usando el intérprete del venv.
    """
    # Definir la ruta del venv (en el mismo directorio que este script)
    venv_dir = os.path.join(os.path.dirname(__file__), 'venv')
    
    # Crear el venv si no existe
    if not os.path.exists(venv_dir):
        print("Creando entorno virtual...")
        venv.create(venv_dir, with_pip=True, symlinks=False)
    
    # Determinar la ruta del ejecutable pip y python según el sistema operativo
    if os.name == 'nt':
        pip_executable = os.path.join(venv_dir, 'Scripts', 'pip.exe')
        python_executable = os.path.join(venv_dir, 'Scripts', 'python.exe')
    else:
        pip_executable = os.path.join(venv_dir, 'bin', 'pip')
        python_executable = os.path.join(venv_dir, 'bin', 'python')
    
    print("Instalando dependencias desde requirements.txt...")
    # Construir la ruta absoluta de requirements.txt (asumiendo que está en el mismo directorio que este script)
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    subprocess.check_call([pip_executable, 'install', '-r', requirements_path])
    
    # Si el intérprete actual no es el del venv, re-ejecutar el script usando el intérprete del venv
    if sys.executable != python_executable:
        print("Reejecutando el script con el entorno virtual...")
        subprocess.check_call([python_executable] + sys.argv)
        sys.exit(0)

# Verificar si estamos en un entorno virtual.
# sys.base_prefix es el prefijo del intérprete base; si es igual a sys.prefix, no estamos en un venv.
if sys.prefix == sys.base_prefix:
    create_and_install_venv()
# %%
