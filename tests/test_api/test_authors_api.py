"""Test authors API endpoints."""

import uuid

import pytest
from litestar import Litestar, status_codes
from litestar.testing import AsyncTestClient

from db.models import Author

RANDOM_UUID = uuid.uuid4()
WRONG_UUID = "wrong-uuid"


def expected_author_response(author: Author) -> dict:
    """Return expected author response."""
    return {
        "id": str(author.id),
        "name": author.name,
        "dob": author.dob.isoformat(),
        "books": [],
    }


async def test_empty_list_authors(
    test_client: AsyncTestClient[Litestar],
) -> None:
    """Test listing authors when the list is empty."""
    url = test_client.app.route_reverse("list_authors")

    response = await test_client.get(url)

    assert response.status_code == status_codes.HTTP_200_OK
    assert response.json() == []


async def test_list_authors(
    test_client: AsyncTestClient[Litestar],
    created_author: Author,
) -> None:
    """Test listing authors when the list is not empty."""
    url = test_client.app.route_reverse("list_authors")

    response = await test_client.get(url)

    assert response.status_code == status_codes.HTTP_200_OK
    assert response.json() == [expected_author_response(created_author)]


async def test_get_author(
    test_client: AsyncTestClient[Litestar],
    created_author: Author,
) -> None:
    """Test getting an author."""
    url = test_client.app.route_reverse(
        "get_author",
        author_id=created_author.id,
    )

    response = await test_client.get(url)

    assert response.status_code == status_codes.HTTP_200_OK
    assert response.json() == expected_author_response(created_author)


async def test_get_author_returns_not_found_for_unexisting_author(
    test_client: AsyncTestClient[Litestar],
) -> None:
    """Test getting an author returns not found when there is no author found."""
    url = test_client.app.route_reverse("get_author", author_id=RANDOM_UUID)

    response = await test_client.get(url)

    assert response.status_code == status_codes.HTTP_404_NOT_FOUND


async def test_post_author(
    test_client: AsyncTestClient[Litestar],
) -> None:
    """Test creating an author."""
    url = test_client.app.route_reverse("post_author")
    body = {
        "name": "Author",
        "dob": "2000-01-01",
    }
    response = await test_client.post(url, json=body)

    assert response.status_code == status_codes.HTTP_201_CREATED
    assert response.json() == {
        "id": response.json()["id"],
        "name": body["name"],
        "dob": body["dob"],
        "books": [],
    }


@pytest.mark.parametrize(
    ("field", "expected_status_code"),
    (
        ["name", status_codes.HTTP_400_BAD_REQUEST],
        ["dob", status_codes.HTTP_400_BAD_REQUEST],
    ),
)
async def test_post_author_with_missing_field_returns_bad_request(
    test_client: AsyncTestClient[Litestar],
    field: str,
    expected_status_code: int,
) -> None:
    """Test creating an author with missing field."""
    url = test_client.app.route_reverse("post_author")
    body = {
        "name": "Author",
        "dob": "2000-01-01",
    }
    body.pop(field)

    response = await test_client.post(url, json=body)

    assert response.status_code == expected_status_code


async def test_delete_author(
    test_client: AsyncTestClient[Litestar],
    created_author: Author,
) -> None:
    """Test deleting an author."""
    url = test_client.app.route_reverse(
        "delete_author",
        author_id=created_author.id,
    )

    response = await test_client.delete(url)

    assert response.status_code == status_codes.HTTP_204_NO_CONTENT


async def test_patch_author(
    test_client: AsyncTestClient[Litestar],
    created_author: Author,
) -> None:
    """Test updating an author."""
    url = test_client.app.route_reverse(
        "patch_author",
        author_id=created_author.id,
    )
    body = {"name": "Updated author"}

    response = await test_client.patch(url, json=body)

    assert response.status_code == status_codes.HTTP_200_OK
    assert response.json() == {
        **expected_author_response(created_author),
        "name": body["name"],
    }
