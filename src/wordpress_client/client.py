"""
WordPress REST API Client.

Main client class for interacting with WordPress sites.
"""

from typing import Optional, List, Dict, Any, Union
import mimetypes
import requests
from pathlib import Path

from .auth import AuthBase, ApplicationPasswordAuth
from .exceptions import (
    WordPressAPIError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    PermissionError,
)
from .utils import build_api_url, parse_wp_error, validate_status
from .models.post import Post, PostCreate, PostUpdate
from .models.media import Media, MediaUpdate
from .models.category import Category, CategoryCreate, CategoryUpdate


class WordPressClient:
    """
    WordPress REST API Client.

    Provides methods to interact with WordPress posts, categories, media, and more.
    """

    def __init__(
        self,
        base_url: str,
        auth: Optional[AuthBase] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        timeout: int = 30,
    ):
        """
        Initialize WordPress client.

        Args:
            base_url: WordPress site base URL
            auth: Authentication object (ApplicationPasswordAuth or JWTAuth)
            username: Username (if auth not provided)
            password: Password/Application Password (if auth not provided)
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        # Set up authentication
        if auth:
            self.auth = auth
        elif username and password:
            # Default to Application Password auth
            self.auth = ApplicationPasswordAuth(username, password)
        else:
            self.auth = None

        self.session = requests.Session()
        if self.auth:
            self.session.headers.update(self.auth.get_auth_headers())

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> Union[Dict, List]:
        """
        Make HTTP request to WordPress API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            params: Query parameters
            data: Request body data
            files: Files to upload

        Returns:
            Response data

        Raises:
            WordPressAPIError: On API errors
        """
        url = build_api_url(self.base_url, endpoint, params)

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data if data and not files else None,
                files=files,
                timeout=self.timeout,
            )

            # Handle different status codes
            if response.status_code == 401:
                error_msg = parse_wp_error(response.json() if response.text else {})
                raise AuthenticationError(
                    error_msg, response.status_code, response.json()
                )

            elif response.status_code == 403:
                error_msg = parse_wp_error(response.json() if response.text else {})
                raise PermissionError(error_msg, response.status_code, response.json())

            elif response.status_code == 404:
                error_msg = parse_wp_error(response.json() if response.text else {})
                raise NotFoundError(error_msg, response.status_code, response.json())

            elif response.status_code == 400:
                error_msg = parse_wp_error(response.json() if response.text else {})
                raise ValidationError(error_msg, response.status_code, response.json())

            elif response.status_code >= 400:
                error_msg = parse_wp_error(response.json() if response.text else {})
                raise WordPressAPIError(
                    error_msg, response.status_code, response.json()
                )

            return response.json() if response.text else {}

        except requests.exceptions.RequestException as e:
            raise WordPressAPIError(f"Request failed: {str(e)}")

    # ==================== POST OPERATIONS ====================

    def get_posts(
        self,
        page: int = 1,
        per_page: int = 10,
        search: Optional[str] = None,
        status: Optional[str] = None,
        categories: Optional[List[int]] = None,
        tags: Optional[List[int]] = None,
    ) -> List[Post]:
        """
        Get list of posts.

        Args:
            page: Page number
            per_page: Posts per page (max 100)
            search: Search term
            status: Post status filter
            categories: Filter by category IDs
            tags: Filter by tag IDs

        Returns:
            List of Post objects
        """
        params: Dict[str, Any] = {
            "page": page,
            "per_page": min(per_page, 100),
        }

        if search:
            params["search"] = search
        if status:
            params["status"] = status
        if categories:
            params["categories"] = ",".join(map(str, categories))
        if tags:
            params["tags"] = ",".join(map(str, tags))

        data = self._request("GET", "wp/v2/posts", params=params)
        return [Post(**post) for post in data]

    def get_post(self, post_id: int) -> Post:
        """
        Get a single post by ID.

        Args:
            post_id: Post ID

        Returns:
            Post object
        """
        data = self._request("GET", f"wp/v2/posts/{post_id}")
        if not isinstance(data, dict):
            raise WordPressAPIError("Invalid response format")
        return Post(**data)

    def create_post(self, post: PostCreate) -> Post:
        """
        Create a new post.

        Args:
            post: PostCreate object with post data

        Returns:
            Created Post object
        """
        if post.status and not validate_status(post.status):
            raise ValidationError(f"Invalid status: {post.status}")

        data = post.model_dump(exclude_none=True)
        response_data = self._request("POST", "wp/v2/posts", data=data)
        if not isinstance(response_data, dict):
            raise WordPressAPIError("Invalid response format")
        return Post(**response_data)

    def update_post(self, post_id: int, post: PostUpdate) -> Post:
        """
        Update an existing post.

        Args:
            post_id: Post ID
            post: PostUpdate object with updated data

        Returns:
            Updated Post object
        """
        if post.status and not validate_status(post.status):
            raise ValidationError(f"Invalid status: {post.status}")

        data = post.model_dump(exclude_none=True)
        response_data = self._request("POST", f"wp/v2/posts/{post_id}", data=data)
        if not isinstance(response_data, dict):
            raise WordPressAPIError("Invalid response format")
        return Post(**response_data)

    def delete_post(self, post_id: int, force: bool = False) -> Dict:
        """
        Delete a post.

        Args:
            post_id: Post ID
            force: Permanently delete (True) or move to trash (False)

        Returns:
            Response data
        """
        params = {"force": force}
        response = self._request("DELETE", f"wp/v2/posts/{post_id}", params=params)
        if not isinstance(response, dict):
            raise WordPressAPIError("Invalid response format")
        return response

    # ==================== CATEGORY OPERATIONS ====================

    def get_categories(
        self,
        page: int = 1,
        per_page: int = 10,
        search: Optional[str] = None,
        parent: Optional[int] = None,
    ) -> List[Category]:
        """
        Get list of categories.

        Args:
            page: Page number
            per_page: Categories per page (max 100)
            search: Search term
            parent: Filter by parent category ID

        Returns:
            List of Category objects
        """
        params: Dict[str, Any] = {
            "page": page,
            "per_page": min(per_page, 100),
        }

        if search:
            params["search"] = search
        if parent is not None:
            params["parent"] = parent

        data = self._request("GET", "wp/v2/categories", params=params)
        return [Category(**cat) for cat in data]

    def get_category(self, category_id: int) -> Category:
        """
        Get a single category by ID.

        Args:
            category_id: Category ID

        Returns:
            Category object
        """
        data = self._request("GET", f"wp/v2/categories/{category_id}")
        if not isinstance(data, dict):
            raise WordPressAPIError("Invalid response format")
        return Category(**data)

    def create_category(self, category: CategoryCreate) -> Category:
        """
        Create a new category.

        Args:
            category: CategoryCreate object with category data

        Returns:
            Created Category object
        """
        data = category.model_dump(exclude_none=True)
        response_data = self._request("POST", "wp/v2/categories", data=data)
        if not isinstance(response_data, dict):
            raise WordPressAPIError("Invalid response format")
        return Category(**response_data)

    def update_category(self, category_id: int, category: CategoryUpdate) -> Category:
        """
        Update an existing category.

        Args:
            category_id: Category ID
            category: CategoryUpdate object with updated data

        Returns:
            Updated Category object
        """
        data = category.model_dump(exclude_none=True)
        response_data = self._request(
            "POST", f"wp/v2/categories/{category_id}", data=data
        )
        if not isinstance(response_data, dict):
            raise WordPressAPIError("Invalid response format")
        return Category(**response_data)

    def delete_category(self, category_id: int, force: bool = False) -> Dict:
        """
        Delete a category.

        Args:
            category_id: Category ID
            force: Permanently delete (True) or not

        Returns:
            Response data
        """
        params = {"force": force}
        response = self._request("DELETE", f"wp/v2/categories/{category_id}", params=params)
        if not isinstance(response, dict):
            raise WordPressAPIError("Invalid response format")
        return response

    # ==================== MEDIA OPERATIONS ====================

    def get_media(
        self,
        page: int = 1,
        per_page: int = 10,
        search: Optional[str] = None,
        media_type: Optional[str] = None,
    ) -> List[Media]:
        """
        Get list of media items.

        Args:
            page: Page number
            per_page: Items per page (max 100)
            search: Search term
            media_type: Filter by media type (image, video, audio)

        Returns:
            List of Media objects
        """
        params: Dict[str, Any] = {
            "page": page,
            "per_page": min(per_page, 100),
        }

        if search:
            params["search"] = search
        if media_type:
            params["media_type"] = media_type

        data = self._request("GET", "wp/v2/media", params=params)
        return [Media(**item) for item in data]

    def get_media_item(self, media_id: int) -> Media:
        """
        Get a single media item by ID.

        Args:
            media_id: Media ID

        Returns:
            Media object
        """
        data = self._request("GET", f"wp/v2/media/{media_id}")
        if not isinstance(data, dict):
            raise WordPressAPIError("Invalid response format")
        return Media(**data)

    def upload_media(
        self,
        file_path: str,
        title: Optional[str] = None,
        alt_text: Optional[str] = None,
        caption: Optional[str] = None,
        post_id: Optional[int] = None,
    ) -> Media:
        """
        Upload a media file.

        Args:
            file_path: Local file path
            title: Media title
            alt_text: Alternative text
            caption: Caption text
            post_id: Associated post ID

        Returns:
            Created Media object
        """
        path = Path(file_path)
        if not path.exists():
            raise ValidationError(f"File not found: {file_path}")

        # Detect mime type
        mime_type, _ = mimetypes.guess_type(str(path))
        if not mime_type:
            mime_type = "application/octet-stream"

        # Prepare file upload
        with open(path, "rb") as f:
            files = {"file": (path.name, f, mime_type)}

            # Add headers for metadata
            headers = self.auth.get_auth_headers() if self.auth else {}
            if title:
                headers["Content-Disposition"] = f'attachment; filename="{path.name}"'

            # Build URL with parameters
            params = {}
            if alt_text:
                params["alt_text"] = alt_text
            if caption:
                params["caption"] = caption
            if title:
                params["title"] = title
            if post_id:
                params["post"] = post_id

            url = build_api_url(self.base_url, "wp/v2/media", params)

            try:
                response = requests.post(
                    url, files=files, headers=headers, timeout=self.timeout
                )
                response.raise_for_status()
                return Media(**response.json())
            except requests.exceptions.RequestException as e:
                raise WordPressAPIError(f"Media upload failed: {str(e)}")

    def update_media(self, media_id: int, media: MediaUpdate) -> Media:
        """
        Update media metadata.

        Args:
            media_id: Media ID
            media: MediaUpdate object with updated data

        Returns:
            Updated Media object
        """
        data = media.model_dump(exclude_none=True)
        response_data = self._request("POST", f"wp/v2/media/{media_id}", data=data)
        if not isinstance(response_data, dict):
            raise WordPressAPIError("Invalid response format")
        return Media(**response_data)

    def delete_media(self, media_id: int, force: bool = False) -> Dict:
        """
        Delete a media item.

        Args:
            media_id: Media ID
            force: Permanently delete (True) or move to trash (False)

        Returns:
            Response data
        """
        params = {"force": force}
        response = self._request("DELETE", f"wp/v2/media/{media_id}", params=params)
        if not isinstance(response, dict):
            raise WordPressAPIError("Invalid response format")
        return response


# Legacy class for compatibility
class WPClient(WordPressClient):
    """Legacy alias for WordPressClient."""

    pass
