from pydantic import BaseModel, Field


class MainPageModel(BaseModel):
    """Основная информация на главной странице"""

    main_info: str = Field(
        default="Ежедневный учет времени отхода ко сну, засыпания, пробуждения и подъема, а также времени нахождения в "
        "кровати без сна. После заполнения одного дня, будет рассчитано время сна и время проведенное в "
        "кровати, затем на их основе определяется эффективность сна. Также, при заполнении дневника сна, "
        "рассчитывается средняя эффективность и время сна в рамках одной недели.",
        title="Основная информация",
    )
