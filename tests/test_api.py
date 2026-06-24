import pytest
from httpx import AsyncClient, ASGITransport

# Импортируем нашу фабрику из main
from src.main import create_app

# Помечаем тест как асинхронный
@pytest.mark.asyncio
async def test_ping_endpoint():
    """Тестируем, что сервер жив и отдает правильный статус."""

    # 1. Собираем приложение
    app = create_app()

    # 2. Создаем транспорт и виртуального клиента (браузер)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        # 3. Делаем GET-запрос
        response = await client.get("/ping")

    # 4. Проверяем результаты (Asserts)
    assert response.status_code == 200

    # Извлекаем JSON из ответа и проверяем его содержимое
    data = response.json()
    assert data["status"] == "ok"
    assert "project" in data