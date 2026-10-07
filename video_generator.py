import os
import random
from moviepy.editor import (
    ImageClip, CompositeVideoClip, concatenate_videoclips,
    AudioFileClip, ColorClip, vfx, afx
)
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

from translations import VOICEOVER_TEMPLATES


class VideoGenerator:
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs("assets/music", exist_ok=True)

    # ---------- UTILITAIRES ----------
    def _get_font(self, size):
        """Cherche une police disponible"""
        candidates = [
            "arial.ttf", "Arial.ttf", "DejaVuSans-Bold.ttf",
            "DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/System/Library/Fonts/Helvetica.ttc"
        ]
        for c in candidates:
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                continue
        return ImageFont.load_default()

    def create_text_image(self, text, size=(1280, 720),
                          bg_color=(30, 30, 60), text_color=(255, 255, 255),
                          accent_color=None, font_size=60,
                          gradient=False, rounded_box=False):
        """Génère une image stylisée avec texte centré"""
        if gradient:
            img = self._create_gradient(size, bg_color, accent_color or bg_color)
        else:
            img = Image.new('RGB', size, bg_color)

        draw = ImageDraw.Draw(img)
        font = self._get_font(font_size)

        # Découper le texte en lignes selon largeur
        max_width = size[0] - 100
        lines = []
        for paragraph in text.split('\n'):
            words = paragraph.split()
            current = ""
            for word in words:
                test = f"{current} {word}".strip()
                bbox = draw.textbbox((0, 0), test, font=font)
                if bbox[2] - bbox[0] <= max_width:
                    current = test
                else:
                    if current:
                        lines.append(current)
                    current = word
            if current:
                lines.append(current)

        line_height = font_size + 20
        total_height = len(lines) * line_height
        y_start = (size[1] - total_height) // 2

        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (size[0] - text_width) // 2
            y = y_start + i * line_height
            # Ombre
            draw.text((x + 3, y + 3), line, fill=(0, 0, 0), font=font)
            draw.text((x, y), line, fill=text_color, font=font)

        path = f"/tmp/text_{random.randint(100000, 999999)}.png"
        img.save(path)
        return path

    def _create_gradient(self, size, color1, color2):
        """Crée un dégradé vertical"""
        base = Image.new('RGB', size, color1)
        top = np.array(base)
        for y in range(size[1]):
            ratio = y / size[1]
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            top[y, :] = [r, g, b]
        return Image.fromarray(top)

    def generate_voiceover(self, text, lang='fr'):
        """Génère voix off multilingue"""
        tts = gTTS(text=text, lang=lang, slow=False)
        path = f"/tmp/voice_{random.randint(100000, 999999)}.mp3"
        tts.save(path)
        return path

    # ---------- TRANSITIONS ----------
    def _apply_transition(self, clip, transition_type, duration=0.5):
        """Applique une transition d'entrée"""
        if transition_type == "fade":
            return clip.crossfadein(duration)
        elif transition_type == "slide":
            return clip.crossfadein(duration)
        elif transition_type == "zoom":
            return clip.resize(lambda t: 1 + 0.02 * t).crossfadein(duration)
        return clip

    # ---------- GÉNÉRATION PRINCIPALE ----------
    def create_promo_video(
        self,
        entreprise, produit, slogan, features,
        logo_path=None, product_image=None,
        template=None, format_key="horizontal",
        voiceover=True, language="fr",
        music_path=None, music_volume=0.15,
        show_emoji=True
    ):
        """Génère la vidéo promo complète"""

        # Récupération des paramètres du template
        if template is None:
            template = {
                "bg_color": (25, 25, 45),
                "text_color": (255, 255, 255),
                "accent_color": (100, 200, 255),
                "font_size_title": 90,
                "font_size_body": 55,
                "transition": "fade"
            }

        from templates import FORMATS
        size = FORMATS[format_key]["size"]
        W, H = size

        bg = template["bg_color"]
        txt = template["text_color"]
        accent = template["accent_color"]
        fs_title = template["font_size_title"]
        fs_body = template["font_size_body"]
        transition = template["transition"]

        clips = []

        # ---------- SCÈNE 1 : Intro / Logo ----------
        if logo_path and os.path.exists(logo_path):
            logo = ImageClip(logo_path).set_duration(3)
            # Adapter taille logo selon format
            logo_h = int(H * 0.35)
            logo = logo.resize(height=logo_h)
            bg_clip = ColorClip(size=size, color=bg).set_duration(3)
            intro = CompositeVideoClip(
                [bg_clip, logo.set_position("center")]
            )
        else:
            img = self.create_text_image(
                entreprise, size=size, bg_color=bg, text_color=txt,
                accent_color=accent, font_size=fs_title,
                gradient=True, rounded_box=True
            )
            intro = ImageClip(img).set_duration(3)

        intro = self._apply_transition(intro, transition)
        clips.append(intro)

        # ---------- SCÈNE 2 : Produit ----------
        if product_image and os.path.exists(product_image):
            prod = ImageClip(product_image).set_duration(4)
            prod = prod.resize(height=int(H * 0.55))
            bg_clip = ColorClip(size=size, color=bg).set_duration(4)
            product_scene = CompositeVideoClip(
                [bg_clip, prod.set_position(("center", "center"))]
            )
        else:
            img = self.create_text_image(
                f"✨ {produit}" if show_emoji else produit,
                size=size, bg_color=bg, text_color=txt,
                accent_color=accent, font_size=fs_title, gradient=True
            )
            product_scene = ImageClip(img).set_duration(4)

        product_scene = self._apply_transition(product_scene, transition)
        clips.append(product_scene)

        # ---------- SCÈNE 3 : Slogan ----------
        img = self.create_text_image(
            f"« {slogan} »",
            size=size, bg_color=bg, text_color=accent,
            accent_color=bg, font_size=fs_title - 10, gradient=True
        )
        clips.append(self._apply_transition(
            ImageClip(img).set_duration(3), transition
        ))

        # ---------- SCÈNES 4 : Caractéristiques ----------
        for feat in features:
            txt_feat = f"✓ {feat}" if show_emoji else feat
            img = self.create_text_image(
                txt_feat, size=size, bg_color=bg,
                text_color=txt, accent_color=accent,
                font_size=fs_body
            )
            clips.append(self._apply_transition(
                ImageClip(img).set_duration(3), transition
            ))

        # ---------- SCÈNE 5 : CTA final ----------
        cta_txt = f"{entreprise}\n📞 Contactez-nous dès aujourd'hui !" \
                  if show_emoji else f"{entreprise}\nContactez-nous dès aujourd'hui !"
        img = self.create_text_image(
            cta_txt, size=size,
            bg_color=accent, text_color=(255, 255, 255),
            accent_color=bg, font_size=fs_title - 15, gradient=True
        )
        clips.append(self._apply_transition(
            ImageClip(img).set_duration(4), transition
        ))

        # ---------- ASSEMBLAGE ----------
        # Utiliser crossfade entre clips
        video = concatenate_videoclips(clips, method="compose",
                                        padding=-0.4)

        # ---------- VOIX OFF ----------
        if voiceover:
            try:
                template_txt = VOICEOVER_TEMPLATES.get(
                    language,
                    VOICEOVER_TEMPLATES["fr"]
                )
                voice_text = template_txt.format(
                    entreprise=entreprise,
                    produit=produit,
                    slogan=slogan,
                    features=", ".join(features)
                )
                audio_path = self.generate_voiceover(voice_text, lang=language)
                audio = AudioFileClip(audio_path)

                if audio.duration > video.duration:
                    video = video.set_duration(audio.duration)
                audio = audio.subclip(0, min(audio.duration, video.duration))
                video = video.set_audio(audio)
            except Exception as e:
                print(f"[VOIX OFF] Erreur : {e}")

        # ---------- MUSIQUE DE FOND ----------
        if music_path and os.path.exists(music_path):
            try:
                music = AudioFileClip(music_path).volumex(music_volume)
                if music.duration < video.duration:
                    music = afx.audio_loop(music, duration=video.duration)
                else:
                    music = music.subclip(0, video.duration)

                if video.audio is not None:
                    from moviepy.editor import CompositeAudioClip
                    final_audio = CompositeAudioClip([video.audio, music])
                    video = video.set_audio(final_audio)
                else:
                    video = video.set_audio(music)
            except Exception as e:
                print(f"[MUSIQUE] Erreur : {e}")

        # ---------- EXPORT ----------
        safe_name = "".join(c for c in entreprise if c.isalnum() or c in " _-")
        safe_name = safe_name.replace(" ", "_")
        output_path = os.path.join(
            self.output_dir,
            f"promo_{safe_name}_{format_key}.mp4"
        )

        video.write_videofile(
            output_path,
            fps=24,
            codec='libx264',
            audio_codec='aac',
            preset='medium',
            threads=4
        )
        return output_path