import re
from collections import Counter
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TextoAnalizadoForm
from .models import TextoAnalizado

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

def analizar_texto(request, texto_id):
    texto_obj = get_object_or_404(TextoAnalizado, id=texto_id)
    
    # Leer el contenido del archivo
    try:
        with texto_obj.archivo.open('r') as archivo:
            contenido = archivo.read()
    except:
        contenido = ""
    
    # Procesar el texto y generar histograma (se mantiene por si en algun caso se llegara a necesitar)
    palabras = re.findall(r'\b[a-zA-ZáéíóúÁÉÍÓÚñÑ]+\b', contenido.lower())
    contador_palabras = Counter(palabras)
    palabras_comunes = contador_palabras.most_common(20)  # Top 20 palabras
    
    # nuevo procesamiento con limpieza
    palabras_limpias = limpiar_texto(contenido)
    contador_limpio = Counter(palabras_limpias)
    palabras_comunes_limpias = contador_limpio.most_common(20)
    
    return render(request, 'histograma.html', {
        'texto': texto_obj,
        'palabras_comunes_original': palabras_comunes_original,
        'palabras_comunes_limpias': palabras_comunes_limpias,
        'total_palabras_original': len(palabras_originales),
        'total_palabras_limpias': len(palabras_limpias),
        'palabras_limpias_muestra': palabras_limpias[:50]  # Para mostrar muestra
    })