import re
from collections import Counter
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TextoAnalizadoForm
from .models import TextoAnalizado
from .preprocesamiento import (
    calcular_probabilidades_mle,
    generar_ngrams_con_fronteras,
    limpiar_texto,
    generar_ngrams
)

def subir_texto(request):
    if request.method == 'POST':
        form = TextoAnalizadoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_textos')
    else:
        form = TextoAnalizadoForm()
    return render(request, 'subir.html', {'form': form})

def lista_textos(request):
    textos = TextoAnalizado.objects.all().order_by('-fecha_subida')
    return render(request, 'lista.html', {'textos': textos})

def generar_ngrams(palabras, n):
    """
    Genera n-gramas a partir de una lista de palabras y devuelve un contador.
    """
    if not palabras or len(palabras) < n:
        print(f"✗ No hay suficientes palabras para {n}-gramas: {len(palabras)} palabras")
        return Counter()
    
    ngrams = zip(*[palabras[i:] for i in range(n)])
    ngrams = [' '.join(ng) for ng in ngrams]
    print(f"✓ Generados {len(ngrams)} {n}-gramas")
    return Counter(ngrams)

def analizar_texto(request, texto_id):
    texto_obj = get_object_or_404(TextoAnalizado, id=texto_id)
    contenido = ""
    
    # --- LECTURA DEL ARCHIVO ---
    try:
        with texto_obj.archivo.open('rb') as archivo:
            contenido_bytes = archivo.read()
        try:
            contenido = contenido_bytes.decode('utf-8')
        except UnicodeDecodeError:
            try:
                contenido = contenido_bytes.decode('latin-1')
            except UnicodeDecodeError:
                try:
                    contenido = contenido_bytes.decode('cp1252')
                except UnicodeDecodeError:
                    contenido = contenido_bytes.decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"✗ Error al leer archivo: {e}")
        contenido = ""
    
    # Variables de salida
    palabras_comunes_original = []
    palabras_comunes_limpias = []
    total_palabras_original = 0
    total_palabras_limpias = 0
    palabras_limpias_muestra = []
    ngrams_mas_comunes = []
    total_ngramas = 0
    n = 2
    probabilidades = {}

    # --- PROCESAMIENTO ORIGINAL ---
    try:
        palabras_originales = re.findall(r'\b[\wáéíóúÁÉÍÓÚñÑüÜ]+\b', contenido.lower())
        contador_original = Counter(palabras_originales)
        palabras_comunes_original = contador_original.most_common(20)
        total_palabras_original = len(palabras_originales)
    except Exception as e:
        print(f"✗ Error en procesamiento original: {e}")

    # --- PROCESAMIENTO LIMPIO Y N-GRAMAS ---
    try:
        palabras_limpias = limpiar_texto(contenido)
        n = int(request.GET.get('n', 2))
        contador_ngrams = generar_ngrams_con_fronteras(palabras_limpias, n)

        if n > 1:
            contador_n_minus1 = generar_ngrams_con_fronteras(palabras_limpias, n - 1)
        else:
            contador_n_minus1 = Counter({'': len(palabras_limpias)})

        probabilidades = calcular_probabilidades_mle(contador_ngrams, contador_n_minus1)

        contador_limpio = Counter(palabras_limpias)
        palabras_comunes_limpias = contador_limpio.most_common(20)
        total_palabras_limpias = len(palabras_limpias)
        palabras_limpias_muestra = palabras_limpias[:50]

        # N-gramas más comunes
        contador_ngrams_simple = generar_ngrams(palabras_limpias, n)
        ngrams_mas_comunes = contador_ngrams_simple.most_common(20)
        total_ngramas = sum(f for _, f in ngrams_mas_comunes)

        # Combinar n-grama, frecuencia y probabilidad
        resultados_prob = []
        for ngrama, freq in ngrams_mas_comunes:
            prob = probabilidades.get(ngrama, 0)
            resultados_prob.append({
                'ngrama': ngrama,
                'frecuencia': freq,
                'probabilidad': prob
            })

    except Exception as e:
        print(f"✗ Error en procesamiento limpio/n-gramas: {e}")
        resultados_prob = []

    return render(request, 'histograma.html', {
        'texto': texto_obj,
        'palabras_comunes_original': palabras_comunes_original,
        'palabras_comunes_limpias': palabras_comunes_limpias,
        'total_palabras_original': total_palabras_original,
        'total_palabras_limpias': total_palabras_limpias,
        'stopwords_eliminadas': total_palabras_original - total_palabras_limpias,
        'palabras_limpias_muestra': palabras_limpias_muestra,
        'ngrams_mas_comunes': ngrams_mas_comunes,
        'n_actual': n,
        'total_ngramas': total_ngramas,
        'probabilidades_ngrams': probabilidades,
        'resultados_prob': resultados_prob,   # <-- para la plantilla
    })
