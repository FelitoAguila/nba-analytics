#!/usr/bin/env python3
"""
Script de verificación pre-deployment
Verifica que todo esté listo para subir a GitHub y deployar en Render
"""

import os
import json
import sys

def check_gitignore():
    """Verifica que .gitignore esté configurado correctamente"""
    print("✓ Verificando .gitignore...")
    
    if not os.path.exists('.gitignore'):
        print("  ❌ ERROR: No se encontró .gitignore")
        return False
    
    with open('.gitignore', 'r') as f:
        content = f.read()
    
    if 'config/service-account.json' in content:
        print("  ✅ .gitignore está configurado correctamente")
        return True
    else:
        print("  ❌ ERROR: .gitignore no incluye config/service-account.json")
        return False

def check_service_account():
    """Verifica que el service account exista localmente"""
    print("\n✓ Verificando credenciales locales...")
    
    if os.path.exists('config/service-account.json'):
        print("  ✅ Archivo de credenciales encontrado")
        
        # Verificar que sea JSON válido
        try:
            with open('config/service-account.json', 'r') as f:
                creds = json.load(f)
            
            if 'project_id' in creds and 'private_key' in creds:
                print(f"  ✅ JSON válido. Project ID: {creds['project_id']}")
                return True, creds
            else:
                print("  ❌ ERROR: JSON no tiene campos requeridos")
                return False, None
        except json.JSONDecodeError:
            print("  ❌ ERROR: Archivo no es JSON válido")
            return False, None
    else:
        print("  ⚠️  ADVERTENCIA: No se encontró config/service-account.json")
        print("     (Esto es OK si ya deployaste y solo usas producción)")
        return True, None

def check_settings():
    """Verifica que settings.py tenga valores configurados"""
    print("\n✓ Verificando config/settings.py...")
    
    try:
        from config import settings
        
        if settings.PROJECT_ID == 'tu-project-id':
            print("  ⚠️  ADVERTENCIA: PROJECT_ID aún tiene valor por defecto")
            print("     Actualiza este valor en config/settings.py")
        else:
            print(f"  ✅ PROJECT_ID configurado: {settings.PROJECT_ID}")
        
        print(f"  ✅ DATASET_ID: {settings.DATASET_ID}")
        print(f"  ✅ TABLE_ID: {settings.TABLE_ID}")
        return True
    except Exception as e:
        print(f"  ❌ ERROR: No se pudo cargar settings: {e}")
        return False

def check_required_files():
    """Verifica que todos los archivos necesarios existan"""
    print("\n✓ Verificando archivos requeridos...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'render.yaml',
        'config/settings.py',
        'utils/database.py',
        'callbacks/player_callbacks.py',
        'layouts/players_layout.py'
    ]
    
    all_ok = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} NO ENCONTRADO")
            all_ok = False
    
    return all_ok

def check_requirements():
    """Verifica que requirements.txt tenga las dependencias necesarias"""
    print("\n✓ Verificando requirements.txt...")
    
    with open('requirements.txt', 'r') as f:
        reqs = f.read()
    
    required = ['dash', 'google-cloud-bigquery', 'plotly', 'gunicorn']
    all_ok = True
    
    for req in required:
        if req in reqs:
            print(f"  ✅ {req}")
        else:
            print(f"  ❌ {req} FALTA")
            all_ok = False
    
    return all_ok

def main():
    print("🚀 NBA Stats Dashboard - Verificación Pre-Deployment")
    print("="*60)
    
    checks = []
    
    # Ejecutar verificaciones
    checks.append(("gitignore", check_gitignore()))
    creds_ok, creds = check_service_account()
    checks.append(("service-account", creds_ok))
    checks.append(("settings", check_settings()))
    checks.append(("archivos", check_required_files()))
    checks.append(("requirements", check_requirements()))
    
    # Resumen
    print("\n" + "="*60)
    print("📊 RESUMEN")
    print("="*60)
    
    all_passed = all(result for _, result in checks)
    
    for name, result in checks:
        status = "✅" if result else "❌"
        print(f"{status} - {name}")
    
    if all_passed:
        print("\n🎉 ¡TODO LISTO!")
        print("\n📖 Lee DEPLOYMENT.md para instrucciones completas")
        return 0
    else:
        print("\n⚠️  HAY PROBLEMAS QUE RESOLVER")
        return 1

if __name__ == "__main__":
    sys.exit(main())