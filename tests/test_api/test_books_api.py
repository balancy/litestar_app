"""Test books API endpoints."""

import uuid

import pytest
from litestar import Litestar, status_codes
from litestar.testing import AsyncTestClient

from db.models import Author, Book

RANDOM_UUID = uuid.uuid4()
WRONG_UUID = "wrong-uuid"


def expected_book_response(book: Book) -> dict:
    """Return expected book response."""
    return {
        "id": str(book.id),
        "title": book.title,
        "description": book.description,
        "author": {
            "id": str(book.author.id),
            "name": book.author.name,
            "dob": book.author.dob.isoformat(),
        },
    }


async def test_empty_list_books(
    test_client: AsyncTestClient[Litestar],
) -> None:
    """Test listing books when the list is empty."""
    url = test_client.app.route_reverse("list_books")

    response = await test_client.get(url)

    assert response.status_code == status_codes.HTTP_200_OK
    assert response.json() == []


async def test_list_books(
    test_client: AsyncTestClient[Litestar],
    created_book: Book,
) -> None:
    """Test listing books when the list is not empty."""
    url = test_client.app.route_reverse("list_books")

    response = await test_client.get(url)

    assert response.status_code == status_codes.HTTP_200_OK
    assert response.json() == [expected_book_response(created_book)]


async def test_get_book(
    test_client: AsyncTestClient[Litestar],
    created_book: Book,
) -> None:
    """Test getting a book."""
    url = test_client.app.route_reverse("get_book", book_id=created_book.id)

    response = await test_client.get(url)

    assert response.status_code == status_codes.HTTP_200_OK
    assert response.json() == expected_book_response(created_book)


async def test_get_book_returns_not_found_for_unexisting_book(
    test_client: AsyncTestClient[Litestar],
) -> None:
    """Test getting a book returns not found when there is no book found."""
    url = test_client.app.route_reverse("get_book", book_id=RANDOM_UUID)

    response = await test_client.get(url)

    assert response.status_code == status_codes.HTTP_404_NOT_FOUND


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

    assert response.status_code == status_codes.HTTP_201_CREATED
    assert response.json() == {
        "id": response.json()["id"],
        "title": body["title"],
        "description": body["description"],
        "author": {
            "id": str(created_author.id),
            "name": created_author.name,
            "dob": created_author.dob.isoformat(),
        },
    }


@pytest.mark.parametrize(
    ("field", "expected_status_code"),
    (
        ["title", status_codes.HTTP_400_BAD_REQUEST],
        ["description", status_codes.HTTP_400_BAD_REQUEST],
        ["author_id", status_codes.HTTP_400_BAD_REQUEST],
    ),
)
async def test_post_book_with_missing_field_returns_bad_request(
    test_client: AsyncTestClient[Litestar],
    created_author: Author,
    field: str,
    expected_status_code: int,
) -> None:
    """Test creating a book with missing field."""
    url = test_client.app.route_reverse("post_book")
    body = {
        "title": "Book",
        "description": "Description",
        "author_id": str(created_author.id),
    }
    body.pop(field)

    response = await test_client.post(url, json=body)

    assert response.status_code == expected_status_code


async def test_delete_book(
    test_client: AsyncTestClient[Litestar],
    created_book: Book,
) -> None:
    """Test deleting a book."""
    url = test_client.app.route_reverse("delete_book", book_id=created_book.id)

    response = await test_client.delete(url)

    assert response.status_code == status_codes.HTTP_204_NO_CONTENT


async def test_patch_book(
    test_client: AsyncTestClient[Litestar],
    created_book: Book,
) -> None:
    """Test updating a book."""
    url = test_client.app.route_reverse("patch_book", book_id=created_book.id)
    body = {"title": "Updated Book"}

    response = await test_client.patch(url, json=body)

    assert response.status_code == status_codes.HTTP_200_OK
    assert response.json() == {
        **expected_book_response(created_book),
        "title": body["title"],
    }
