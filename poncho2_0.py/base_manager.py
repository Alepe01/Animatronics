import json
import os
import random
from abc import ABC, abstractmethod

class BaseManager(ABC):
    """Clase base para todos los managers con funcionalidad común"""
    
    def __init__(self, data_file=None):
        self.data_file = data_file
        self.data = {}
        print(f"🔧 Inicializando {self.__class__.__name__}")
        if data_file:
            self.load_data()
        else:
            self._create_default_data()
    
    def load_data(self):
        """Cargar datos desde archivo JSON"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                print(f"✅ Datos cargados desde {self.data_file}")
            else:
                print(f"📄 Creando archivo nuevo: {self.data_file}")
                self._create_default_data()
                self.save_data()
        except Exception as e:
            print(f"❌ Error cargando datos: {e}")
            self._create_default_data()
    
    def save_data(self):
        """Guardar datos en archivo JSON"""
        if not self.data_file:
            return
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            print(f"💾 Datos guardados en {self.data_file}")
        except Exception as e:
            print(f"❌ Error guardando datos: {e}")
    
    @abstractmethod
    def _create_default_data(self):
        """Método abstracto para crear datos por defecto - debe ser implementado"""
        pass
    
    def get_random_choice(self, key):
        """Obtener elección aleatoria de una lista"""
        items = self.data.get(key, [])
        return random.choice(items) if items else None
    
    def add_item_to_list(self, key, item):
        """Agregar item a una lista"""
        if key not in self.data:
            self.data[key] = []
        self.data[key].append(item)
        self.save_data()
    
    def increment_counter(self, key, subkey):
        """Incrementar contador anidado"""
        if key not in self.data:
            self.data[key] = {}
        self.data[key][subkey] = self.data[key].get(subkey, 0) + 1
        self.save_data()
        return self.data[key][subkey]
    
    def get_counter(self, key, subkey):
        """Obtener valor de contador"""
        return self.data.get(key, {}).get(subkey, 0)
    
    def get_stats(self):
        """Estadísticas básicas"""
        stats = f"📊 Estadísticas de {self.__class__.__name__}:\n"
        for key, value in self.data.items():
            if isinstance(value, list):
                stats += f"  {key}: {len(value)} elementos\n"
            elif isinstance(value, dict):
                stats += f"  {key}: {len(value)} entradas\n"
            else:
                stats += f"  {key}: {value}\n"
        return stats
    
    def reset_data(self):
        """Resetear datos a valores por defecto"""
        self._create_default_data()
        self.save_data()
    
    def reload_data(self):
        """Recargar datos desde archivo"""
        if self.data_file:
            self.load_data()
    
    def has_data(self, key):
        """Verificar si existe una clave en los datos"""
        return key in self.data and bool(self.data[key])