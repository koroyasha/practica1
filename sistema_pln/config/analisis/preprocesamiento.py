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

def generar_ngrams_con_fronteras(tokens, n=2):
    """
    Genera n-gramas incluyendo tokens de inicio <s> y fin </s> para cada oración.
    Devuelve un contador de n-gramas y el total de n-gramas.
    """
    if not tokens:
        return Counter()
    
    # Dividir tokens en oraciones simples usando punto como referencia
    oraciones = []
    oracion_actual = []
    for token in tokens:
        oracion_actual.append(token)
        if token in ['.', '!', '?']:
            if oracion_actual:
                oraciones.append(oracion_actual)
            oracion_actual = []
    if oracion_actual:
        oraciones.append(oracion_actual)
    
    ngrams_totales = []
    for oracion in oraciones:
        tokens_frontera = ['<s>'] * (n-1) + oracion + ['</s>']
        ngrams_oracion = zip(*[tokens_frontera[i:] for i in range(n)])
        ngrams_oracion = [' '.join(grama) for grama in ngrams_oracion]
        ngrams_totales.extend(ngrams_oracion)
    
    return Counter(ngrams_totales)

def calcular_probabilidades_mle(contador_ngrams, n_minus1_contador):
    """
    Calcula la probabilidad condicional P(w_n | w_1...w_{n-1}) usando MLE
    :param contador_ngrams: Counter de n-gramas
    :param n_minus1_contador: Counter de (n-1)-gramas
    :return: diccionario {ngrama: probabilidad}
    """
    probabilidades = {}
    for ngrama, freq in contador_ngrams.items():
        partes = ngrama.split()
        clave = ' '.join(partes[:-1]) if len(partes) > 1 else ''
        prob = freq / n_minus1_contador.get(clave, 1)
        probabilidades[ngrama] = prob
    return probabilidades