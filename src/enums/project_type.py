# models/project_type.py

from enum import StrEnum


class ProjectType(StrEnum):
    STANDALONE = "standalone"
    CHAPTERED = "chaptered"
    PARTED = "parted"
