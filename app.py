import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import random
import time

st.title("💖 Nosso Amor em Fotos 💖")

# Lista de imagens e legendas
imagens = ["foto1.jpg", "foto2.jpg", "foto3.jpg", "foto4.jpg",
           "foto5.jpg", "foto6.jpg", "foto7.jpg", "foto8.jpg"]
legendas = ["Nossa primeira foto juntos", "Lembrança da viagem", 
            "Sorriso que amo", "Momentos especiais", 
            "1 ano e 1 mês de amor", "Dia inesquecível", 
            "Nosso abraço favorito", "Você e eu pra sempre"]

# Slider para escolher a foto
indice = st.slider("Escolha a foto", min_value=1, max_value=8, step=1)

# Carregar imagem
img_base = Image.open(imagens[indice-1])
enhancer = ImageEnhance.Brightness(img_base)
img_base = enhancer.enhance(1.1)

# Espaço para mostrar imagem animada
placeholder = st.empty()

# Fonte
try:
    font = ImageFont.truetype("arial.ttf", 50)
except:
    font = ImageFont.load_default()

# Criar animação simulada de corações
for frame in range(10):  # 10 “frames” de animação
    img = img_base.copy()
    draw = ImageDraw.Draw(img)

    # Texto da legenda
    largura, altura = img.size
    mensagem = legendas[indice-1]
    bbox = draw.textbbox((0,0), mensagem, font=font)
    largura_texto = bbox[2] - bbox[0]
    altura_texto = bbox[3] - bbox[1]
    posicao = ((largura - largura_texto) // 2, altura - altura_texto - 50)

    draw.rectangle([
        (posicao[0]-10, posicao[1]-10),
        (posicao[0]+largura_texto+10, posicao[1]+altura_texto+10)
    ], fill=(255, 192, 203, 180))
    draw.text(posicao, mensagem, font=font, fill="black")

    # Moldura rosa
    espessura = 20
    for i in range(espessura):
        draw.rectangle([i, i, largura-i-1, altura-i-1], outline=(255, 105, 180))

    # Corações animados
    for _ in range(10):
        x = random.randint(0, largura-50)
        y = random.randint(0, altura//2)
        draw.text((x, y), "♥", font=font, fill=(255, 0, 127))

    # Mostrar imagem
    placeholder.image(img, use_column_width=True)
    time.sleep(0.2)  # muda a cada 0.2 segundos

# Salvar a última imagem com corações
saida = f"foto{indice}_final.png"
img.save(saida)
st.download_button(
    label="💾 Baixar imagem",
    data=open(saida, "rb"),
    file_name=saida,
    mime="image/png"
)
