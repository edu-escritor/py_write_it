from writeit.translations.base_translation import BaseTranslation


class EnglishAmerican(BaseTranslation):

    TRANSLATIONS: dict[str, str] = {
        "dates.long_format": "«day» «month» «year»",
        "dates.month.01": "January",
        "dates.month.02": "February",
        "dates.month.03": "March",
        "dates.month.04": "April",
        "dates.month.05": "May",
        "dates.month.06": "June",
        "dates.month.07": "July",
        "dates.month.08": "August",
        "dates.month.09": "September",
        "dates.month.10": "October",
        "dates.month.11": "November",
        "dates.month.12": "December",
        "files.segments.chapters": "chapters",
        "files.segments.part": "part",
        "files.segments.text": "text",
        "templates.master.author": "Author",
        "templates.master.characters": "Characters",
        "templates.master.date": "Date",
        "templates.master.e-mail": "Email",
        "templates.master.phone": "Cellphone",
        "templates.master.words": "Words",
        "templates.part.title": "Part «part»",
    }
