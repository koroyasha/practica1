# analisis/preprocesamiento.py
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

# Descargar recursos de NLTK si no están disponibles
def descargar_recursos_nltk():
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('punkt')
        nltk.download('stopwords')

# Aseguramos que estén disponibles
descargar_recursos_nltk()

# Stopwords en español
stop_words_es = set(stopwords.words('spanish'))

def limpiar_texto(texto):
    """
    Realiza la limpieza completa del texto:
    1. Convierte a minúsculas
    2. Elimina puntuación
    3. Elimina stopwords en español
    """
    if not texto or not isinstance(texto, str):
        return []

    # Convertir a minúsculas
    texto = texto.lower()

    # Eliminar puntuación y caracteres extraños
    texto = re.sub(r'[^\wáéíóúñü\s]', '', texto)

    # Tokenizar
    tokens = word_tokenize(texto, language='spanish')

    # Filtrar stopwords y palabras vacías
    tokens_limpios = [token for token in tokens if token not in stop_words_es and len(token) > 1]

    return tokens_limpios

def generar_ngrams(tokens, n=2, top=20):
    """
    Genera los n-gramas más frecuentes a partir de una lista de tokens.
    :param tokens: lista de palabras ya limpiadas
    :param n: tamaño del n-grama (2=bigramas, 3=trigramas, etc.)
    :param top: cantidad de n-gramas más frecuentes a devolver
    :return: lista de tuplas [(ngram, frecuencia), ...]
    """
    if not tokens:
        return []

    # Crear n-gramas como tuplas
    ngrams = zip(*[tokens[i:] for i in range(n)])
    ngrams = [' '.join(grama) for grama in ngrams]

    # Contar frecuencia
    contador = Counter(ngrams)

    # Devolver los más frecuentes
    return contador.most_common(top)

def obtener_stopwords_espanol():
    return list(stop_words_es)
