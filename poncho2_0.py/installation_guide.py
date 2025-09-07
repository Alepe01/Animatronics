# GUÍA DE INSTALACIÓN - VENTANA DE PRUEBAS
# ==========================================

"""
INSTRUCCIONES PARA INTEGRAR LA VENTANA DE PRUEBAS

1. AGREGAR ARCHIVOS:
   - test_window_manager.py (colocar en la carpeta del proyecto)

2. MODIFICACIONES AL SISTEMA EXISTENTE:
   Los cambios ya están incluidos en los archivos refactorizados.

3. USO DE LA VENTANA DE PRUEBAS:
   - Hacer clic en el botón "🧪 Pruebas" en los controles rápidos
   - La ventana se abre con 4 pestañas principales
"""

# FUNCIONALIDADES DE LA VENTANA DE PRUEBAS
FEATURES_INFO = {
    "comentarios_manuales": {
        "descripcion": "Enviar comentarios personalizados",
        "funciones": [
            "Usuario personalizable o aleatorio",
            "Área de texto libre para comentarios",
            "Botones de comentarios rápidos",
            "Historial de comentarios enviados"
        ]
    },
    
    "regalos_manuales": {
        "descripcion": "Simular regalos de TikTok",
        "funciones": [
            "10 tipos de regalos predefinidos",
            "Donador personalizable",
            "Regalo personalizado con cantidad",
            "Envío directo al Robot de Regalos"
        ]
    },
    
    "modo_automatico": {
        "descripcion": "Simulación automática continua",
        "funciones": [
            "Intervalo configurable (segundos)",
            "Probabilidad de comentarios (70% por defecto)",
            "Probabilidad de regalos (30% por defecto)",
            "Inicio/parada con un botón"
        ]
    },
    
    "pruebas_rapidas": {
        "descripcion": "Escenarios predefinidos de prueba",
        "funciones": [
            "Chat básico: 4 comentarios normales",
            "Lluvia de regalos: 8 regalos simultáneos",
            "Todos los modos: Prueba los 8 modos",
            "Spam de chistes: 5 solicitudes seguidas",
            "Sesión clarividente: Preguntas de futuro",
            "Estrés test: 20 comentarios rápidos"
        ]
    }
}

# EJEMPLO DE USO PASO A PASO
def ejemplo_uso_ventana_pruebas():
    """
    EJEMPLO DE FLUJO DE PRUEBAS:
    
    1. Abrir ventana de pruebas desde botón 🧪
    
    2. PROBAR COMENTARIOS MANUALES:
       - Pestaña "💬 Comentarios"
       - Cambiar usuario a "TestUser1"
       - Escribir "Hola Poncho"
       - Clic en "📤 ENVIAR COMENTARIO"
       - Ver respuesta en panel izquierdo de Poncho
    
    3. PROBAR REGALOS:
       - Pestaña "🎁 Regalos"
       - Cambiar donador a "GenerosoFan"
       - Clic en "Rosa (x1)"
       - Ver respuesta energética en panel central dorado
    
    4. MODO AUTOMÁTICO:
       - Pestaña "🤖 Automático"
       - Ajustar intervalo a 2 segundos
       - Clic "▶️ INICIAR AUTOMÁTICO"
       - Observar flujo automático de comentarios y regalos
       - Clic "⏹️ DETENER AUTOMÁTICO" cuando termine
    
    5. PRUEBAS RÁPIDAS:
       - Pestaña "⚡ Pruebas Rápidas"
       - Clic "🎁 Lluvia de Regalos"
       - Ver múltiples regalos procesados rápidamente
       - Observar racha del Robot de Regalos
    """
    
    print("Ejemplo de uso documentado arriba")

# TROUBLESHOOTING
TROUBLESHOOTING = {
    "error_import": {
        "problema": "ImportError: test_window_manager.py no encontrado",
        "solucion": "Verificar que test_window_manager.py esté en la misma carpeta que main.py"
    },
    
    "ventana_no_abre": {
        "problema": "La ventana de pruebas no se abre",
        "solucion": "Verificar que la aplicación principal esté corriendo y conectada"
    },
    
    "comentarios_no_llegan": {
        "problema": "Los comentarios enviados no aparecen en Poncho",
        "solucion": "Verificar que dual_controller esté inicializado correctamente"
    },
    
    "regalos_no_funcionan": {
        "problema": "Los regalos no van al Robot de Regalos",
        "solucion": "Verificar que msg_type='gift' esté siendo procesado correctamente"
    },
    
    "modo_automatico_lento": {
        "problema": "El modo automático es muy lento",
        "solucion": "Reducir intervalo a 1-2 segundos en la configuración"
    }
}

# CONFIGURACIONES RECOMENDADAS
RECOMMENDED_SETTINGS = {
    "desarrollo": {
        "intervalo_auto": 2,  # segundos
        "prob_comentarios": 80,  # %
        "prob_regalos": 20,  # %
        "usuarios_test": 5
    },
    
    "pruebas_estres": {
        "intervalo_auto": 0.5,  # segundos
        "prob_comentarios": 60,  # %
        "prob_regalos": 40,  # %
        "usuarios_test": 10
    },
    
    "demostracion": {
        "intervalo_auto": 3,  # segundos
        "prob_comentarios": 70,  # %
        "prob_regalos": 30,  # %
        "usuarios_test": 8
    }
}

# MÉTRICAS A MONITOREAR
METRICAS_IMPORTANTES = [
    "Tiempo de respuesta de Poncho",
    "Tiempo de respuesta del Robot de Regalos",
    "Tasa de procesamiento de comentarios",
    "Rachas máximas de regalos",
    "Memoria utilizada durante pruebas de estrés",
    "Errores en el log durante simulación"
]

def print_installation_summary():
    """Imprimir resumen de instalación"""
    print("""
🧪 VENTANA DE PRUEBAS - RESUMEN DE INSTALACIÓN

✅ ARCHIVOS NECESARIOS:
- test_window_manager.py (NUEVO)
- main_refactored.py (MODIFICADO)
- gui_refactored.py (MODIFICADO)

✅ FUNCIONALIDADES:
- 💬 Comentarios manuales con usuarios personalizables
- 🎁 Regalos manuales para probar Robot de Regalos
- 🤖 Modo automático con configuración avanzada
- ⚡ 6 pruebas rápidas predefinidas
- 📊 Estadísticas y monitoreo en tiempo real

✅ VENTAJAS:
- Pruebas sin necesidad de TikTok activo
- Simulación realista de chat en vivo
- Fácil testing de ambos robots
- Escenarios de estrés configurables
- Interfaz intuitiva con pestañas

✅ USO:
1. Ejecutar main_refactored.py
2. Clic en botón "🧪 Pruebas"
3. Seleccionar pestaña deseada
4. Configurar y enviar pruebas
5. Observar respuestas en tiempo real

⚠️ NOTA: La ventana funciona completamente independiente
de TikTok, ideal para desarrollo y debugging.
""")

if __name__ == "__main__":
    print_installation_summary()
    
    print("\n📋 CONFIGURACIONES DISPONIBLES:")
    for nombre, config in RECOMMENDED_SETTINGS.items():
        print(f"\n{nombre.upper()}:")
        for key, value in config.items():
            print(f"  {key}: {value}")
    
    print(f"\n🔧 TROUBLESHOOTING:")
    for problema, info in TROUBLESHOOTING.items():
        print(f"\n{problema}:")
        print(f"  Problema: {info['problema']}")
        print(f"  Solución: {info['solucion']}")
    
    print("\n✅ Sistema de pruebas listo para usar!")