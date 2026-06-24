class HabitAlreadyExistsError(Exception):
    """Выбрасывается, если привычка с таким названием уже есть в базе."""
    pass

class HabitNotFoundError(Exception):
    """Выбрасывается, если привычка не найдена по ID."""
    pass