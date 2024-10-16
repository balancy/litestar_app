"""Test books API endpoints."""

from litestar import Litestar
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED
from litestar.testing import AsyncTestClient

from db.models import Author


async def test_list_books(test_client: AsyncTestClient[Litestar]) -> None:
    """Test listing books."""
    url = test_client.app.route_reverse("list_books")
    response = await test_client.get(url)
    print(response.text)

    assert response.status_code == HTTP_200_OK
    assert response.json() == []


async def test_post_book(
    test_client: AsyncTestClient[Litestar],
    created_author: Author,
) -> None:
    """Test creating a book."""
    url = test_client.app.route_reverse("post_book")
    body = {
        "title": "Book",
        "description": "Description",
        "author_id": str(created_author.id),
    }
    response = await test_client.post(url, json=body)

    response_json = response.json()
    response_json.pop("id")

    assert response.status_code == HTTP_201_CREATED
    assert response_json == {
        "title": "Book",
        "description": "Description",
        "author": created_author.asdict(),
    }
