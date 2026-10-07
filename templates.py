# Templates de styles visuels pour les vidéos

TEMPLATES = {
    "moderne": {
        "name": "🎨 Moderne",
        "bg_color": (25, 25, 45),
        "text_color": (255, 255, 255),
        "accent_color": (100, 200, 255),
        "font_size_title": 90,
        "font_size_body": 55,
        "transition": "fade"
    },
    "luxe": {
        "name": "💎 Luxe",
        "bg_color": (10, 10, 10),
        "text_color": (218, 165, 32),
        "accent_color": (255, 215, 0),
        "font_size_title": 85,
        "font_size_body": 50,
        "transition": "fade"
    },
    "minimaliste": {
        "name": "⚪ Minimaliste",
        "bg_color": (245, 245, 245),
        "text_color": (30, 30, 30),
        "accent_color": (200, 50, 50),
        "font_size_title": 80,
        "font_size_body": 50,
        "transition": "slide"
    },
    "energetique": {
        "name": "⚡ Énergétique",
        "bg_color": (200, 30, 60),
        "text_color": (255, 255, 255),
        "accent_color": (255, 220, 0),
        "font_size_title": 95,
        "font_size_body": 60,
        "transition": "zoom"
    },
    "nature": {
        "name": "🌿 Nature",
        "bg_color": (34, 80, 50),
        "text_color": (255, 255, 240),
        "accent_color": (150, 220, 100),
        "font_size_title": 85,
        "font_size_body": 52,
        "transition": "fade"
    },
    "corporate": {
        "name": "🏢 Corporate",
        "bg_color": (20, 40, 80),
        "text_color": (255, 255, 255),
        "accent_color": (0, 150, 200),
        "font_size_title": 82,
        "font_size_body": 52,
        "transition": "slide"
    }
}

# Formats de vidéo
FORMATS = {
    "horizontal": {"name": "📺 Horizontal (YouTube - 16:9)", "size": (1280, 720)},
    "vertical":   {"name": "📱 Vertical (TikTok/Reels - 9:16)", "size": (720, 1280)},
    "carre":      {"name": "⬛ Carré (Instagram - 1:1)", "size": (1080, 1080)},
    "story":      {"name": "📲 Story (Instagram - 9:16)", "size": (720, 1280)},
}