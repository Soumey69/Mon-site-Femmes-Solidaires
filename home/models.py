# models.py
from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    PageChooserPanel,
)
from wagtail.images.models import Image
from wagtail.images.blocks import ImageChooserBlock   # ✅ pour l'image dans chaque service


# ============================================================
# 1) Bloc réutilisable pour décrire un service
#    -> utilisé sur la page d'accueil (aperçu)
#    -> utilisé sur la page "Nos services" (liste complète)
#    Chaque service a maintenant :
#      - un badge/numéro
#      - un titre
#      - une description
#      - une liste de points clés
#      - UNE IMAGE
# ============================================================
class ServiceBlock(blocks.StructBlock):
    """
    Bloc "Service" pour StreamField.
    On pourra en ajouter plusieurs dans l'admin Wagtail.
    """

    badge = blocks.CharBlock(
        required=False,
        help_text="Petit texte au-dessus (ex : 01, 02, 03...)",
        label="Badge / numéro"
    )

    title = blocks.CharBlock(
        required=True,
        max_length=120,
        label="Titre du service"
    )

    description = blocks.TextBlock(
        required=False,
        label="Description courte"
    )

    # ✅ Nouvelle image pour chaque service (illustration moderne)
    image = ImageChooserBlock(
        required=False,
        help_text="Image ou icône illustrant le service (format horizontal de préférence).",
        label="Image du service"
    )

    features = blocks.ListBlock(
        blocks.CharBlock(label="Point clé"),
        required=False,
        label="Liste de points clés (bullet points)"
    )

    class Meta:
        icon = "cog"
        label = "Service"
        help_text = "Bloc réutilisable pour présenter un service avec une image."


# ============================================================
# 2) Page d'accueil
#    - hero (image + texte + boutons)
#    - aperçu de 2–3 services
# ============================================================
class HomePage(Page):
    # --------- HERO (bandeau principal avec image) ----------
    hero_kicker = models.CharField(
        "Petit texte au-dessus du titre",
        max_length=150,
        blank=True,
        default="Bienvenue",  # ✅ default pour éviter la question en migration
        help_text="Ex : 'Agence digitale · Exemple Wagtail'"
    )

    hero_title = models.CharField(
        "Titre principal",
        max_length=200,
        default="Titre de la page d’accueil",  # ✅ default
        help_text="Ex : 'Créez un site vitrine moderne, clair et efficace.'"
    )

    hero_subtitle = models.TextField(
        "Texte sous le titre",
        blank=True,
        default="Sous-titre de présentation pour la page d’accueil.",  # ✅ default
        help_text="Quelques phrases qui expliquent le site."
    )

    # Image de fond du hero (choisie dans la bibliothèque d'images Wagtail)
    hero_background_image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image de fond du hero",
        help_text="Grande image plein écran affichée en haut de la page."
    )

    # Bouton principal -> généralement la page “À propos”
    hero_primary_button_text = models.CharField(
        "Texte du bouton principal",
        max_length=50,
        default="En savoir plus sur nous",
    )
    hero_primary_button_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Page du bouton principal",
        help_text="Page vers laquelle le bouton principal redirige (ex : À propos).",
    )

    # Bouton secondaire -> généralement la page “Contact”
    hero_secondary_button_text = models.CharField(
        "Texte du bouton secondaire",
        max_length=50,
        default="Discutons de votre projet",
        blank=True,
    )
    hero_secondary_button_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Page du bouton secondaire",
        help_text="Page vers laquelle le bouton secondaire redirige (ex : Contact).",
    )

    # --------- SECTION "APERÇU DES SERVICES" ----------
    services_preview_title = models.CharField(
        "Titre de la section services (accueil)",
        max_length=150,
        default="Nos services",
    )

    services_preview_intro = models.TextField(
        "Texte d’intro de la section services (accueil)",
        blank=True,
        default="Un aperçu rapide de nos services.",  # ✅ default
        help_text="Petite phrase pour introduire les services."
    )

    # StreamField utilisant notre bloc ServiceBlock (avec image)
    services_preview = StreamField(
        [
            ("service", ServiceBlock()),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Services à afficher sur l’accueil (aperçu)",
        #help_text="Liste de 2–3 services pour la page d’accueil.",
    )

    # --------- PANELS POUR L'ADMIN WAGTAIL ----------
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_kicker"),
                FieldPanel("hero_title"),
                FieldPanel("hero_subtitle"),
                FieldPanel("hero_background_image"),
                FieldPanel("hero_primary_button_text"),
                PageChooserPanel("hero_primary_button_page"),
                FieldPanel("hero_secondary_button_text"),
                PageChooserPanel("hero_secondary_button_page"),
            ],
            heading="Section hero (bandeau principal)",
        ),
        MultiFieldPanel(
            [
                FieldPanel("services_preview_title"),
                FieldPanel("services_preview_intro"),
                FieldPanel("services_preview"),
            ],
            heading="Aperçu des services sur la page d’accueil",
        ),
    ]


# ============================================================
# 3) Page "Nos services"
#    - même bloc ServiceBlock, mais pour la liste complète
# ============================================================
class ServicesPage(Page):
    intro_title = models.CharField(
        "Titre principal",
        max_length=150,
        default="Nos services",
    )

    intro_subtitle = models.TextField(
        "Texte d’intro",
        blank=True,
        default="Voici un exemple de section services que vous pouvez adapter.",  # ✅ default
        help_text="Ex : 'Voici un exemple de section services...'"
    )

    # On réutilise le même bloc ServiceBlock avec image
    services = StreamField(
        [
            ("service", ServiceBlock()),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Services",
        help_text="Liste complète des services proposés.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro_title"),
        FieldPanel("intro_subtitle"),
        FieldPanel("services"),
    ]


# ============================================================
# 4) Page "À propos"
#    - texte de présentation
#    - image + légende
# ============================================================
class AboutPage(Page):
    intro_title = models.CharField(
        "Titre principal",
        max_length=150,
        default="À propos",
    )

    intro_subtitle = models.TextField(
        "Texte d’intro",
        blank=True,
        default="En savoir plus sur nous.",  # ✅ default
        help_text="Une petite phrase pour introduire la page."
    )

    # Corps de texte principal (avec éditeur riche Wagtail)
    body = RichTextField(
        "Texte de présentation",
        blank=True,
        default="",  # ✅ default vide : évite les questions de migration
        help_text="Contenu principal : histoire, mission, valeurs..."
    )

    # Image illustrant l’équipe / le projet
    image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image de la section À propos",
        help_text="Photo d’équipe ou image illustrative.",
    )

    image_caption = models.CharField(
        "Légende de l’image",
        max_length=255,
        blank=True,
        default="",  # ✅ default vide
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro_title"),
        FieldPanel("intro_subtitle"),
        FieldPanel("body"),
        FieldPanel("image"),
        FieldPanel("image_caption"),
    ]


# ============================================================
# 5) Page "Contact"
#    - titre + intro
#    - coordonnées de contact
#    - texte d’explication au-dessus du formulaire
# ============================================================
class ContactPage(Page):
    intro_title = models.CharField(
        "Titre principal",
        max_length=150,
        default="Contact",
    )

    intro_subtitle = models.TextField(
        "Texte d’intro",
        blank=True,
        default="Un exemple de page contact avec un formulaire simple.",  # ✅ default
        help_text="Ex : 'Un exemple de page contact avec un formulaire simple.'"
    )

    contact_email = models.EmailField(
        "Email de contact",
        blank=True,
        default="contact@exemple.com",  # ✅ default simple
    )

    contact_phone = models.CharField(
        "Téléphone",
        max_length=50,
        blank=True,
        default="",  # ✅ default vide
    )

    contact_address = models.CharField(
        "Adresse",
        max_length=255,
        blank=True,
        default="Adresse de votre entreprise",  # ✅ default pédagogique
    )

    contact_text = RichTextField(
        "Texte au-dessus du formulaire",
        blank=True,
        default="",  # ✅ default vide
        help_text='Ex : "Utilisez ce formulaire comme base..."'
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro_title"),
        FieldPanel("intro_subtitle"),
        MultiFieldPanel(
            [
                FieldPanel("contact_email"),
                FieldPanel("contact_phone"),
                FieldPanel("contact_address"),
            ],
            heading="Coordonnées",
        ),
        FieldPanel("contact_text"),
    ]
# Fin de models.py