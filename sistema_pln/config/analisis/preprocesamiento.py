# analisis/preprocesamiento.py
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Descargar recursos de NLTK si no están disponibles
def descargar_recursos_nltk():
    try:
        nltk.data.find('tokenizers/punkt_tab')
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('punkt_tab')
        nltk.download('stopwords')

# Llamar a la función para asegurar que los recursos estén disponibles
descargar_recursos_nltk()

def limpiar_texto(texto):
    """
    Realiza la limpieza completa del texto:
    1. Conversión a minúsculas
    2. Eliminación de símbolos de puntuación
    3. Eliminación de stopwords en español
    """
    # Convertir a minúsculas
    texto = texto.lower()
    
    # Eliminar símbolos de puntuación
    texto = re.sub(f'[{re.escape(string.punctuation)}¿¡]', '', texto)
    
    # Tokenizar el texto
    tokens = word_tokenize(texto, language='spanish')
    
    # Obtener stopwords en español
    stop_words = set(stopwords.words('spanish'))
    
    # Filtrar stopwords y tokens vacíos
    tokens_limpios = [
        token for token in tokens 
        if token not in stop_words and token.strip() != '' and len(token) > 1
    ]
    
    return tokens_limpios

def obtener_stopwords_espanol():
    """Retorna la lista de stopwords en español"""
    return list(stopwords.words('spanish'))