from writeit.enums.project_type import ProjectType
from writeit.errors.validation_error import ValidationError


class IsValidProjectPart:

    @staticmethod
    def validate(value: int | None, project_type: ProjectType) -> int:
        if value is None:
            raise ValidationError("The value cannot be empty!")

        if value < 0:
            raise ValidationError("There is no negative part!")

        if project_type in [ProjectType.STANDALONE, ProjectType.CHAPTERED]:
            if value != 0:
                raise ValidationError("This kind of project cannot have parts!")

            return value

        if value == 0:
            raise ValidationError("A project with parts must have at least one part!")

        return value
