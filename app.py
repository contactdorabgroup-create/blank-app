import streamlit as st
import os
from video_generator import VideoGenerator
from templates import TEMPLATES, FORMATS
from translations import LANGUAGES

st.set_page_config(
    page_title="🎬 Générateur Vidéo Promo",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 20px; border-radius: 10px; color: white;
        text-align: center; margin-bottom: 20px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white; border: none; padding: 12px 30px;
        border-radius: 8px; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🎬 Générateur de Vidéos Promotionnelles</h1>'
            '<p>Créez des vidéos professionnelles pour votre entreprise en quelques clics</p></div>',
            unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:
    st.header("📝 Informations")

    entreprise = st.text_input("🏢 Nom de l'entreprise", "Ma Super Entreprise")
    produit = st.text_input("📦 Nom du produit", "Mon Produit Incroyable")
    slogan = st.text_area("💬 Slogan", "L'innovation à votre service", height=70)

    features_text = st.text_area(
        "✅ Caractéristiques (une par ligne)",
        "Qualité premium\nLivraison rapide\nPrix compétitifs\nService client 24/7",
        height=130
    )

    st.divider()
    st.header("🎨 Style")

    template_key = st.selectbox(
        "Template",
        options=list(TEMPLATES.keys()),
        format_func=lambda x: TEMPLATES[x]["name"]
    )

    format_key = st.selectbox(
        "Format vidéo",
        options=list(FORMATS.keys()),
        format_func=lambda x: FORMATS[x]["name"]
    )

    st.divider()
    st.header("🎙️ Audio")

    voiceover = st.checkbox("Activer la voix off", value=True)

    language_name = st.selectbox(
        "Langue de la voix off",
        options=list(LANGUAGES.keys()),
        index=0
    )
    language_code = LANGUAGES[language_name]

    # Musique de fond
    music_files = []
    if os.path.exists("assets/music"):
        music_files = [f for f in os.listdir("assets/music")
                       if f.lower().endswith(('.mp3', '.wav', '.m4a'))]

    if music_files:
        music_choice = st.selectbox(
            "Musique de fond",
            options=["Aucune"] + music_files
        )
        music_volume = st.slider("Volume musique", 0.0, 0.5, 0.15, 0.05)
        music_path = None if music_choice == "Aucune" \
                     else f"assets/music/{music_choice}"
    else:
        st.info("💡 Ajoutez des MP3 dans `assets/music/`")
        music_path = None
        music_volume = 0.15

    st.divider()
    st.header("🖼️ Médias optionnels")

    logo_file = st.file_uploader("Logo entreprise", type=['png', 'jpg', 'jpeg'])
    product_file = st.file_uploader("Image produit", type=['png', 'jpg', 'jpeg'])

    show_emoji = st.checkbox("Afficher les emojis", value=True)


# ================= ZONE PRINCIPALE =================
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 Aperçu")
    st.markdown(f"""
    - **Entreprise :** {entreprise}
    - **Produit :** {produit}
    - **Slogan :** {slogan}
    - **Template :** {TEMPLATES[template_key]['name']}
    - **Format :** {FORMATS[format_key]['name']}
    - **Langue :** {language_name}
    """)
    st.write("**Caractéristiques :**")
    features = [f.strip() for f in features_text.split('\n') if f.strip()]
    for feat in features:
        st.write(f"- {feat}")

with col2:
    st.subheader("🎥 Génération")
    duree = 3 + 4 + 3 + len(features) * 3 + 4
    st.info(f"⏱️ Durée estimée : ~{duree} secondes")
    st.info(f"📐 Résolution : {FORMATS[format_key]['size'][0]}×{FORMATS[format_key]['size'][1]}")

    generate_btn = st.button("🚀 Générer la vidéo", type="primary",
                             use_container_width=True)

if generate_btn:
    with st.spinner("🎬 Génération en cours... Cela peut prendre 1-3 minutes."):
        try:
            os.makedirs("assets", exist_ok=True)

            logo_path = None
            product_path = None

            if logo_file:
                logo_path = f"assets/temp_logo_{logo_file.name}"
                with open(logo_path, "wb") as f:
                    f.write(logo_file.getbuffer())

            if product_file:
                product_path = f"assets/temp_product_{product_file.name}"
                with open(product_path, "wb") as f:
                    f.write(product_file.getbuffer())

            generator = VideoGenerator()
            output = generator.create_promo_video(
                entreprise=entreprise,
                produit=produit,
                slogan=slogan,
                features=features,
                logo_path=logo_path,
                product_image=product_path,
                template=TEMPLATES[template_key],
                format_key=format_key,
                voiceover=voiceover,
                language=language_code,
                music_path=music_path,
                music_volume=music_volume,
                show_emoji=show_emoji
            )

            st.success("✅ Vidéo générée avec succès !")
            st.video(output)

            with open(output, "rb") as f:
                st.download_button(
                    "⬇️ Télécharger la vidéo MP4",
                    data=f,
                    file_name=os.path.basename(output),
                    mime="video/mp4",
                    use_container_width=True
                )

        except Exception as e:
            st.error(f"❌ Erreur : {str(e)}")
            st.exception(e)

st.markdown("---")
st.caption("💡 Astuce : placez vos MP3 dans `assets/music/` pour la musique de fond.")