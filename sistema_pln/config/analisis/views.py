import re
from collections import Counter
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TextoAnalizadoForm
from .models import TextoAnalizado
from .preprocesamiento import limpiar_texto, generar_ngrams

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
    
    # LECTURA DEL ARCHIVO CON MANEJO DE ENCODING (CORREGIDO)
    try:
        # Primero leer el archivo como bytes binarios
        with texto_obj.archivo.open('rb') as archivo:
            contenido_bytes = archivo.read()
        
        # Intentar diferentes codificaciones
        try:
            contenido = contenido_bytes.decode('utf-8')
            print(f"✓ Contenido decodificado con UTF-8: {len(contenido)} caracteres")
        except UnicodeDecodeError:
            try:
                contenido = contenido_bytes.decode('latin-1')
                print(f"✓ Contenido decodificado con Latin-1: {len(contenido)} caracteres")
            except UnicodeDecodeError:
                try:
                    contenido = contenido_bytes.decode('cp1252')
                    print(f"✓ Contenido decodificado con CP1252: {len(contenido)} caracteres")
                except UnicodeDecodeError:
                    contenido = contenido_bytes.decode('utf-8', errors='ignore')
                    print(f"✓ Contenido decodificado con UTF-8 (ignore errors): {len(contenido)} caracteres")
                    
    except Exception as e:
        print(f"✗ Error al leer archivo: {e}")
        contenido = ""
    
    if contenido:
        print(f"✓ Primeros 100 chars: '{contenido[:100]}...'")
        # Debug: caracteres especiales
        special_chars = set([c for c in contenido if ord(c) > 127])
        if special_chars:
            print(f"✓ Caracteres especiales encontrados: {special_chars}")
    
    palabras_comunes_original = []
    palabras_comunes_limpias = []
    total_palabras_original = 0
    total_palabras_limpias = 0
    palabras_limpias_muestra = []
    ngrams_mas_comunes = []
    total_ngramas = 0  
    n = 2  
    
    # PROCESAMIENTO ORIGINAL
    try:
        # EXPRESIÓN REGULAR MEJORADA PARA CARACTERES ESPAÑOLES
        palabras_originales = re.findall(r'\b[\wáéíóúÁÉÍÓÚñÑüÜ]+\b', contenido.lower())
        contador_original = Counter(palabras_originales)
        palabras_comunes_original = contador_original.most_common(20)
        total_palabras_original = len(palabras_originales)
        print(f"✓ Procesamiento original: {total_palabras_original} palabras")
        if palabras_comunes_original:
            print(f"✓ Top 3 original: {palabras_comunes_original[:3]}")
    except Exception as e:
        print(f"✗ Error en procesamiento original: {e}")
    
    # PROCESAMIENTO LIMPIO
    try:
        palabras_limpias = limpiar_texto(contenido)
        print(f"✓ Palabras después de limpieza: {len(palabras_limpias)} palabras")
        
        if palabras_limpias:
            print(f"✓ Primeras 5 palabras limpias: {palabras_limpias[:5]}")
            # Verificar acentos
            palabras_con_acentos = [p for p in palabras_limpias if any(c in p for c in 'áéíóúñü')]
            if palabras_con_acentos:
                print(f"✓ Palabras con acentos: {palabras_con_acentos[:5]}")
        else:
            print("✗ ¡ADVERTENCIA! palabras_limpias está vacío")
            print(f"Contenido original: '{contenido[:100]}...'")
        
        contador_limpio = Counter(palabras_limpias)
        palabras_comunes_limpias = contador_limpio.most_common(20)
        total_palabras_limpias = len(palabras_limpias)
        palabras_limpias_muestra = palabras_limpias[:50]
        if palabras_comunes_limpias:
            print(f"✓ Top 3 limpias: {palabras_comunes_limpias[:3]}")
        
    except Exception as e:
        print(f"✗ Error en procesamiento limpio: {e}")
    
    # PROCESAMIENTO N-GRAMAS
    try:
        n = int(request.GET.get('n', 2))
        print(f"✓ Parámetro n recibido: {n}")
        print(f"✓ Palabras limpias disponibles: {len(palabras_limpias)}")
        
        contador_ngrams = generar_ngrams(palabras_limpias, n)
        print(f"✓ Contador ngrams creado: {len(contador_ngrams)} n-gramas únicos")
        
        ngrams_mas_comunes = contador_ngrams.most_common(20)
        print(f"✓ N-gramas más comunes: {len(ngrams_mas_comunes)} elementos")
        
        if ngrams_mas_comunes:
            print(f"✓ Top 3 n-gramas: {ngrams_mas_comunes[:3]}")
            # Verificar n-gramas con acentos
            ngrams_con_acentos = [ng for ng, freq in ngrams_mas_comunes if any(c in ng for c in 'áéíóúñü')]
            if ngrams_con_acentos:
                print(f"✓ N-gramas con acentos: {ngrams_con_acentos[:3]}")
        else:
            print("✗ No se generaron n-gramas")
            
        total_ngramas = sum(frecuencia for _, frecuencia in ngrams_mas_comunes)
        print(f"✓ Total n-gramas: {total_ngramas}")
        
    except Exception as e:
        print(f"✗ Error al calcular n-gramas: {e}")
        ngrams_mas_comunes = []
        n = 2
        total_ngramas = 0

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
    })