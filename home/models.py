# models.py
from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    PageChooserPanel,
    InlinePanel,
)
from wagtail.images.models import Image
from wagtail.images.blocks import ImageChooserBlock   # ✅ pour l'image dans chaque formation
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting

# Pour la page contact avec formulaire email
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from modelcluster.fields import ParentalKey

# ============================================================
# 1) Bloc réutilisable pour décrire une formation
#    -> utilisé sur la page d'accueil (aperçu)
#    -> utilisé sur la page "Nos formations" (liste complète)
#    Chaque formation a maintenant :
#      - un badge/numéro
#      - un titre
#      - une description
#      - une liste de points clés
#      - UNE IMAGE
# ============================================================
class FormationBlock(blocks.StructBlock):
    """
    Bloc "Formation" pour StreamField.
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
        label="Titre du formation"
    )

    description = blocks.TextBlock(
        required=False,
        label="Description courte"
    )

    # ✅ Nouvelle image pour chaque formation (illustration moderne)
    image = ImageChooserBlock(
        required=False,
        help_text="Image ou icône illustrant le formation (format horizontal de préférence).",
        label="Image du formation"
    )

    features = blocks.ListBlock(
        blocks.CharBlock(label="Point clé"),
        required=False,
        label="Liste de points clés (bullet points)"
    )

    class Meta:
        icon = "cog"
        label = "Formation"
        help_text = "Bloc réutilisable pour présenter un formation avec une image."


# ============================================================
# 2) Page d'accueil
#    - hero (image + texte + boutons)
#    - aperçu de 2–3 formations
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

    # --------- SECTION "APERÇU DES formations" ----------
    formations_preview_title = models.CharField(
        "Titre de la section formations (accueil)",
        max_length=150,
        default="Nos formations",
    )

    formations_preview_intro = models.TextField(
        "Texte d’intro de la section formations (accueil)",
        blank=True,
        default="Un aperçu rapide de nos formations.",  # ✅ default
        help_text="Petite phrase pour introduire les formations."
    )

    # StreamField utilisant notre bloc SormationBlock (avec image)
    formations_preview = StreamField(
        [
            ("formation", FormationBlock()),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Formations à afficher sur l’accueil (aperçu)",
        #help_text="Liste de 2–3 formations pour la page d’accueil.",
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
                FieldPanel("formations_preview_title"),
                FieldPanel("formations_preview_intro"),
                FieldPanel("formations_preview"),
            ],
            heading="Aperçu des formations sur la page d’accueil",
        ),
    ]


# ============================================================
# 3) Page "Nos formations"
#    - même bloc FormationBlock, mais pour la liste complète
# ============================================================
class FormationsPage(Page):
    intro_title = models.CharField(
        "Titre principal",
        max_length=150,
        default="Nos formations",
    )

    intro_subtitle = models.TextField(
        "Texte d’intro",
        blank=True,
        default="Voici un exemple de section formations que vous pouvez adapter.",  # ✅ default
        help_text="Ex : 'Voici un exemple de section formations...'"
    )

    # On réutilise le même bloc FormationBlock avec image
    formations = StreamField(
        [
            ("formation", FormationBlock()),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Formations",
        help_text="Liste complète des formations proposés.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro_title"),
        FieldPanel("intro_subtitle"),
        FieldPanel("formations"),
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
# 5) Champs des formulaires (Wagtail Forms) pour la page Contact
# ============================================================
class FormField(AbstractFormField):
    page = ParentalKey(
        "ContactPage",
        on_delete=models.CASCADE,
        related_name="form_fields",
    )

# ============================================================
# 6) Page "Contact"
#    - titre + intro
#    - coordonnées de contact
#    - texte d’explication au-dessus du formulaire
# ============================================================
class ContactPage(AbstractEmailForm):
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

     # Configuration email (où vont les messages)
    to_address = models.CharField(
        "Adresse email qui recevra les messages",
        max_length=255,
        blank=False,
        default="contact@exemple.com",
        help_text="Les messages du formulaire seront envoyés à cette adresse.",
    )

    from_address = models.CharField(
        "Adresse expéditeur",
        max_length=255,
        default="noreply@monsite.com",
        help_text="Adresse utilisée comme expéditeur des emails.",
    )

    subject = models.CharField(
        "Sujet de l’email",
        max_length=255,
        default="Nouveau message depuis votre site vitrine",
    )

    thank_you_text = RichTextField(
        "Message de remerciement après envoi",
        blank=True,
        default="Merci ! Votre message a bien été envoyé.",
    )


    content_panels = AbstractEmailForm.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("intro_title"),
                FieldPanel("intro_subtitle"),
                FieldPanel("contact_text"),
            ],
            heading="Introduction",
        ),
        MultiFieldPanel(
            [
                FieldPanel("contact_email"),
                FieldPanel("contact_phone"),
                FieldPanel("contact_address"),
            ],
            heading="Coordonnées affichées",
        ),
        MultiFieldPanel(
            [
                FieldPanel("to_address"),
                FieldPanel("from_address"),
                FieldPanel("subject"),
            ],
            heading="Configuration des emails",
        ),
        InlinePanel("form_fields", label="Champs du formulaire"),
        FieldPanel("thank_you_text"),
    ]

    # Onglet "Submissions" dans l’admin (facultatif mais pratique)
    submissions_panels = [
        FormSubmissionsPanel(),
    ]


@register_setting
class FooterSettings(BaseSiteSetting):
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Logo de l'association"
    )
    nom_association = models.CharField(
        max_length=100,
        default="Femmes Solidaires",
        verbose_name="Nom de l'association"
    )
    slogan = models.CharField(
        max_length=100,
        default="Formation · Emploi · Solidarité",
        verbose_name="Slogan"
    )
    description = models.TextField(
        default="Association locale engagée pour l’émancipation des femmes par la formation et l’emploi. Ensemble, construisons votre avenir.",
        verbose_name="Texte de présentation"
    )
    annee = models.CharField(
        max_length=4,
        default="2025",
        verbose_name="Année affichée en bas"
    )

    panels = [
        FieldPanel("logo"),
        FieldPanel("nom_association"),
        FieldPanel("slogan"),
        FieldPanel("description"),
        FieldPanel("annee"),
    ]

# Fin de models.py