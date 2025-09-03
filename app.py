import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import random
import time
import os

# --- Configuração da Página ---
st.set_page_config(page_title="Nosso Amor em Fotos", page_icon="💖")
st.title("💖 Nosso Amor em Fotos 💖")
st.markdown("Uma pequena galeria para celebrar nossos momentos especiais.")

# --- Preparação dos Ficheiros e Dados ---
try:
    # Encontra a pasta onde o script está localizado
    pasta_script = os.path.dirname(__file__)
except NameError:
    # Fallback para caso __file__ não esteja disponível
    pasta_script = '.'

# --- Nomes dos ficheiros de imagem ---
# A linha está correta, procurando pelos ficheiros com _final.png
nomes_imagens = [f"foto{i}_final.png" for i in range(1, 9)]

# --- Suas novas legendas personalizadas ---
legendas = [
    "Nossa primeira foto juntos",
    "Esse seu sorriso jamais irei esquecer no nosso primeiro ano como namorados",
    "poder fazer vc feliz é minha felicidade ",
    "Quando sinto saudades e vejo em meu celular essas suas fotos me deixam confortável",
    "Cada dia ao seu lado é um presente",
    "Um dia para guardar no coração",
    "Nosso abraço é o meu lugar favorito",
    "Você e eu, para todo o sempre"
]
# Cria o caminho completo para cada imagem
imagens = [os.path.join(pasta_script, nome) for nome in nomes_imagens]


# --- Interface do Utilizador ---
indice_selecionado = st.slider(
    "Deslize para escolher uma foto e ver a mágica acontecer:",
    min_value=1, max_value=len(imagens), value=1, step=1
)
# Ajusta o índice para a lista que começa em 0
indice_lista = indice_selecionado - 1


# --- Processamento e Exibição da Imagem ---
try:
    img_base = Image.open(imagens[indice_lista])
    enhancer = ImageEnhance.Brightness(img_base)
    img_base = enhancer.enhance(1.1)
    placeholder = st.empty()

    try:
        font_legenda = ImageFont.truetype("arial.ttf", 50)
        font_coracao = ImageFont.truetype("arial.ttf", 60)
    except IOError:
        st.warning("Fonte 'arial.ttf' não encontrada. Usando fonte padrão.")
        font_legenda = ImageFont.load_default()
        font_coracao = ImageFont.load_default()

    # Loop para a animação
    ultima_imagem = None
    for frame in range(10):
        img_animada = img_base.copy()
        draw = ImageDraw.Draw(img_animada, 'RGBA')
        largura, altura = img_animada.size

        # Desenha a moldura
        draw.rectangle([0, 0, largura, altura], outline=(255, 105, 180), width=20)

        # Prepara e desenha a legenda com fundo
        mensagem = legendas[indice_lista]
        bbox = draw.textbbox((0, 0), mensagem, font=font_legenda)
        largura_texto, altura_texto = bbox[2] - bbox[0], bbox[3] - bbox[1]
        pos_texto = ((largura - largura_texto) // 2, altura - altura_texto - 40)
        pos_fundo = [(pos_texto[0] - 15, pos_texto[1] - 10), (pos_texto[0] + largura_texto + 15, pos_texto[1] + altura_texto + 15)]
        draw.rectangle(pos_fundo, fill=(255, 192, 203, 180), radius=15)
        draw.text(pos_texto, mensagem, font=font_legenda, fill="black")

        # Desenha corações aleatórios
        for _ in range(15):
            x, y = random.randint(0, largura - 50), random.randint(0, altura - 50)
            cor_coracao = random.choice([(255, 0, 127), (220, 20, 60), (255, 20, 147)])
            draw.text((x, y), "♥", font=font_coracao, fill=cor_coracao)

        placeholder.image(img_animada, use_column_width=True)
        time.sleep(0.15)
        ultima_imagem = img_animada

    # Botão de Download
    if ultima_imagem:
        from io import BytesIO
        buffer = BytesIO()
        ultima_imagem.save(buffer, format="PNG")
        st.download_button(
            label="💾 Baixar imagem com corações",
            data=buffer.getvalue(),
            file_name=f"nosso_amor_{indice_selecionado}.png",
            mime="image/png"
        )

except FileNotFoundError:
    st.error(f"Erro: A imagem '{os.path.basename(imagens[indice_lista])}' não foi encontrada.")
    st.info("Verifique se o nome do ficheiro está correto e se ele está no repositório do GitHub.")
except Exception as e:
    st.error(f"Ocorreu um erro inesperado: {e}")

