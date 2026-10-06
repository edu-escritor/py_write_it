from writeit.translations.base_translation import BaseTranslation


class PortugueseEuropean(BaseTranslation):

    TRANSLATIONS: dict[str, str] = {
        "dates.long_format": "«day» de «month» de «year»",
        "dates.month.01": "janeiro",
        "dates.month.02": "fevereiro",
        "dates.month.03": "março",
        "dates.month.04": "abril",
        "dates.month.05": "maio",
        "dates.month.06": "junho",
        "dates.month.07": "julho",
        "dates.month.08": "agosto",
        "dates.month.09": "setembro",
        "dates.month.10": "outubro",
        "dates.month.11": "novembro",
        "dates.month.12": "dezembro",
        "files.segments.chapters": "capitulos",
        "files.segments.part": "parte",
        "files.segments.text": "texto",
        "templates.master.author": "Autor",
        "templates.master.characters": "Caracteres",
        "templates.master.date": "Data",
        "templates.master.e-mail": "Email",
        "templates.master.phone": "Telemóvel",
        "templates.master.words": "Palavras",
        "templates.part.title": "Parte «part»",
    }
