import requests
import time
import json


class LolzteamApi:
    def __init__(self, token: str, bypass_429: bool = True):
        """
        :param token: Your token. You can get in there -> https://zelenka.guru/account/api
        :param bypass_429: Bypass status code 429 by sleep
        """

        self.__token = token
        self.__bypass_429 = bypass_429
        self.__auto_delay_time = time.time() - 3
        self.__headers = {'Authorization': f"bearer {self.__token}"}

        self.market = self.__Market(self)
        self.forum = self.__Forum(self)

    def send_request(self, method: str, url: str, params=None, data=None, files=None):
        method = method.upper()
        LolzteamApi.__auto_delay(self)
        match method:
            case "GET":
                response = requests.get(url=url, params=params, data=data, files=files, headers=self.__headers)
            case "POST":
                response = requests.post(url=url, params=params, data=data, files=files, headers=self.__headers)
            case "PUT":
                response = requests.put(url=url, params=params, data=data, files=files, headers=self.__headers)
            case "DELETE":
                response = requests.delete(url=url, params=params, data=data, files=files, headers=self.__headers)
            case _:
                response = {"error": "Создатель либы где-то проебался. Отпиши @AS7RID в тг, он починит"}
        self.__auto_delay_time = time.time()
        return response.json()

    def __auto_delay(self):
        """
        Sleep for time difference between the last call and current call if it's less than 3 seconds
        """
        if self.__bypass_429:
            current_time = time.time()
            time_diff = current_time - self.__auto_delay_time
            if time_diff < 3.0:  # if difference between current and last call > 3 seconds we will sleep the rest of the time

                time.sleep(3.003 - time_diff)

    def change_token(self, new_token: str):
        self.__token = new_token
        self.__headers = {'Authorization': f"bearer {self.__token}"}

    class __Market:
        def __init__(self, api_self):
            self.__api = api_self

        def test(self, params):
            print(params)

            LolzteamApi.send_request(self.__api, method="GET", url='https://api.zelenka.guru/market/me')
            print(time.time())
            LolzteamApi.send_request(self.__api, method="GET", url='https://api.zelenka.guru/market/me')
            print(time.time())
            LolzteamApi.send_request(self.__api, method="GET", url='https://api.zelenka.guru/market/me')
            print(time.time())

    class __Forum:
        def __init__(self, api_self):
            self.__api = api_self  # Passing main self to sub all classes

            #  Sections definitions
            self.categories = self.__Categories(self.__api)
            self.forums = self.__Forums(self.__api)
            self.pages = self.__Pages(self.__api)
            self.threads = self.__Threads(self.__api)
            self.posts = self.__Posts(self.__api)
            self.tags = self.__Tags(self.__api)
            self.users = self.__Users(self.__api)
            self.profile_posts = self.__Profile_posts(self.__api)
            self.conversations = self.__Conversations(self.__api)
            self.notifications = self.__Notifications(self.__api)
            self.search = self.__Search(self.__api)

        class __Categories:
            def __init__(self, __api_self):
                self.__api = __api_self

            def get_categories(self, parent_category_id: int = None, parent_forum_id: int = None, order: str = None):
                """
                GET https://api.zelenka.guru/categories

                List of all categories in the system.

                Required scopes: read

                :param parent_category_id: ID of parent category.
                :param parent_forum_id: ID of parent forum.
                :param order: Ordering of categories. Can be [natural, list]
                :return: json server response
                """
                url = "https://api.zelenka.guru/categories"
                params = {
                    "parent_category_id": parent_category_id,
                    "parent_forum_id": parent_forum_id,
                    "order": order
                }
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url, params=params)

            def get_category(self, category_id: int):
                """
                GET https://api.zelenka.guru/categories/{category_id}

                Detail information of a category.

                Required scopes: read

                :param category_id: ID of category we want to get
                :return: json server response
                """
                url = f"https://api.zelenka.guru/categories/{category_id}"
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url)

        class __Forums:
            def __init__(self, __api_self):
                self.__api = __api_self

            def get_forums(self, parent_category_id: int = None, parent_forum_id: int = None, order: str = None):
                """
                GET https://api.zelenka.guru/categories/forums

                List of all forums in the system.

                Required scopes: read

                :param parent_category_id: ID of parent category.
                :param parent_forum_id: ID of parent forum.
                :param order: Ordering of categories. Can be [natural, list]
                :return: json server response
                """
                url = f"https://api.zelenka.guru/categories/forums"
                params = {
                    "parent_category_id": parent_category_id,
                    "parent_forum_id": parent_forum_id,
                    "order": order
                }
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url, params=params)

            def get_forum(self, forum_id: int):
                """
                GET https://api.zelenka.guru/forums/{forum_id}

                Detail information of a forum.

                Required scopes: read

                :param forum_id: ID of forum we want to get
                :return: json server response
                """
                url = f"https://api.zelenka.guru/forums/{forum_id}"

                return LolzteamApi.send_request(self=self.__api, method="GET", url=url)

            def follow(self, forum_id: int, post: bool = None, alert: bool = None, email: bool = None):
                """
                POST https://api.zelenka.guru/forums/{forum_id}/followers
                Follow a forum.

                Required scopes: post

                :param forum_id: ID of forum we want to get
                :param post: Whether to receive notification for post.
                :param alert: Whether to receive notification as alert.
                :param email: Whether to receive notification as email.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/forums/{forum_id}/followers"
                if True:  # Костыль, пока не пофиксят недочет #63
                    if post:
                        post = 1
                    if alert:
                        alert = 1
                    if email:
                        email = 1
                params = {
                    "post": post,
                    "alert": alert,
                    "email": email
                }
                return LolzteamApi.send_request(self=self.__api, method="POST", url=url, params=params)

            def unfollow(self, forum_id: int):
                """
                DELETE https://api.zelenka.guru/forums/{forum_id}/followers
                Unfollow a forum.

                Required scopes: post

                :param forum_id: ID of forum we want to get

                :return: json server response
                """
                url = f"https://api.zelenka.guru/forums/{forum_id}/followers"
                return LolzteamApi.send_request(self=self.__api, method="DELETE", url=url)

            def followers(self, forum_id: int):
                """
                GET https://api.zelenka.guru/forums/{forum_id}/followers

                List of a forum's followers. For privacy reason, only the current user will be included in the list (if the user follows the specified forum).

                Required scopes: read

                :param forum_id: ID of forum we want to get
                :return: json server response
                """
                url = f"https://api.zelenka.guru/forums/{forum_id}/followers"
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url)

            def followed(self, total: bool = None):
                """
                GET https://api.zelenka.guru/forums/followed

                List of followed forums by current user.

                Required scopes: read

                :param total: If included in the request, only the forum count is returned as forums_total.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/forums/followed"
                if True:  # Костыль, пока не пофиксят недочет #43
                    if total:
                        total = 1
                    else:
                        total = 0
                params = {
                    "total": total
                }
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url, params=params)

        class __Pages:
            def __init__(self, __api_self):
                self.__api = __api_self

            def get_pages(self, parent_page_id: int = None, order: str = None):
                """
                GET https://api.zelenka.guru/pages

                List of all pages in the system.

                Required scopes: read

                :param parent_page_id: ID of parent page. If exists, filter pages that are direct children of that page.
                :param order: Ordering of pages. Can be [natural, list]

                :return: json server response
                """
                url = f"https://api.zelenka.guru/pages"
                params = {
                    "parent_page_id": parent_page_id,
                    "order": order
                }
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url, params=params)

            def get_page(self, page_id: int):
                """
                GET https://api.zelenka.guru/pages/{page_id}

                Detail information of a page.

                Required scopes: read

                :param page_id: ID of parent page. If exists, filter pages that are direct children of that page.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/pages/{page_id}"
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url)

        class __Posts:
            class __Posts_comments:
                def __init__(self, __api_self):
                    self.__api = __api_self

                def get(self, post_id: int, before: int = None):
                    """
                    GET https://api.zelenka.guru/posts/post_id/comments

                    List of post comments in a thread (with pagination).

                    Required scopes: read

                    :param post_id: ID of post.
                    :param before: The time in milliseconds (e.g. 1652177794083) before last comment date

                    :return: json server response
                    """
                    url = f"https://api.zelenka.guru/posts/{post_id}/comments"
                    params = {
                        "before": before
                    }
                    return LolzteamApi.send_request(self=self.__api, method="GET", url=url, params=params)

                def create(self, post_id: int, comment_body: str = None):
                    """
                    POST https://api.zelenka.guru/posts/post_id/comments

                    Create a new post comment.

                    Required scopes: post

                    :param post_id: ID of post.
                    :param comment_body: Content of the new post

                    :return: json server response
                    """
                    url = f"https://api.zelenka.guru/posts/{post_id}/comments"
                    params = {
                        "comment_body": comment_body
                    }
                    return LolzteamApi.send_request(self=self.__api, method="POST", url=url, params=params)

            def __init__(self, __api_self):
                self.__api = __api_self
                self.comments = self.__Posts_comments(self.__api)

            def get_posts(self, thread_id: int, page_of_post_id: int = None, post_ids: str = None, page: int = None,
                          limit: int = None, order: int = None):
                """
                GET https://api.zelenka.guru/posts

                List of posts in a thread (with pagination).

                Required scopes: read

                :param thread_id: ID of the containing thread.
                :param page_of_post_id: ID of a post, posts that are in the same page with the specified post will be returned. thread_id may be skipped.
                :param post_ids: ID's of needed posts (separated by comma). If this parameter is set, all other filtering parameters will be ignored.
                :param page: Page number of posts.
                :param limit: Number of posts in a page. Default value depends on the system configuration.
                :param order: Ordering of posts. Can be [natural, natural_reverse, post_create_date, post_create_date_reverse].
                :return: json server response
                """
                url = f"https://api.zelenka.guru/posts"
                params = {
                    "thread_id": thread_id,
                    "page_of_post_id": page_of_post_id,
                    "post_ids": post_ids,
                    "page": page,
                    "limit": limit,
                    "order": order
                }
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url, params=params)

            def get(self, post_id: int):
                """
                GET https://api.zelenka.guru/posts/post_id

                Detail information of a post.

                Required scopes: read

                :param post_id: ID of post.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/posts/{post_id}"
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url)

            def create(self, post_body: str, thread_id: int = None, quote_post_id: int = None):
                """
                POST https://api.zelenka.guru/threads

                Create a new thread.

                Required scopes: post

                :param post_body: Content of the new post.
                :param thread_id: ID of the target thread.
                :param quote_post_id: ID of the quote post. It's possible to skip thread_id if this parameter is provided. An extra check is performed if both parameters exist and does not match.

                :return: json server response
                """

                url = f"https://api.zelenka.guru/posts"
                params = {
                    "post_body": post_body,
                    "thread_id": thread_id,
                    "quote_post_id": quote_post_id,

                }
                return LolzteamApi.send_request(self=self.__api, method="POST", url=url, params=params)

            def edit(self, post_id: int, thread_title: str = None, thread_prefix_id: int = None,
                     thread_tags: str = None,
                     thread_node_id: int = None, post_body: str = None):
                """
                PUT https://api.zelenka.guru/posts/post_id

                Edit a post.

                Required scopes: post

                :param post_id: ID of post.
                :param thread_title: New title of the thread (only used if the post is the first post in the thread and the authenticated user can edit thread).
                :param thread_prefix_id: New id of the thread's prefix (only used if the post is the first post in the thread and the authenticated user can edit thread).
                :param thread_tags: New tags of the thread (only used if the post is the first post in the thread and the authenticated user can edit thread tags).
                :param thread_node_id: Move thread to new forum if the post is first post and the authenticated user can move thread.
                :param post_body: New content of the post.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/posts/{post_id}"
                params = {
                    "thread_title": thread_title,
                    "thread_prefix_id": thread_prefix_id,
                    "thread_tags": thread_tags,
                    "thread_node_id": thread_node_id,
                    "post_body": post_body
                }
                return LolzteamApi.send_request(self=self.__api, method="PUT", url=url, params=params)

            def delete(self, post_id: int, reason: str = None):
                """
                DELETE https://api.zelenka.guru/posts/post_id

                Delete a post.

                Required scopes: post

                :param post_id: ID of post.
                :param reason: Reason of the post removal.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/posts/{post_id}"
                params = {
                    "reason": reason
                }
                return LolzteamApi.send_request(self=self.__api, method="DELETE", url=url, params=params)

            def likes(self, post_id: int, page: int = None, limit: int = None):
                """
                GET https://api.zelenka.guru/posts/post_id/likes

                List of users who liked a post.

                Required scopes: read

                :param post_id: ID of post.
                :param page: Page number of users.
                :param limit: Number of users in a page. Default value depends on the system configuration.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/posts/{post_id}/likes"
                params = {
                    "page": page,
                    "limit": limit
                }
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url, params=params)

            def like(self, post_id: int):
                """
                POST https://api.zelenka.guru/posts/post_id

                Like a post.

                Required scopes: post

                :param post_id: ID of post.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/posts/{post_id}"
                return LolzteamApi.send_request(self=self.__api, method="POST", url=url)

            def unlike(self, post_id: int):
                """
                DELETE https://api.zelenka.guru/posts/post_id

                Unlike a post.

                Required scopes: post

                :param post_id: ID of post.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/posts/{post_id}"
                return LolzteamApi.send_request(self=self.__api, method="DELETE", url=url)

            def report(self, post_id: int, message: str):
                """
                POST https://api.zelenka.guru/posts/post_id/report

                Report a post.

                Required scopes: post

                :param post_id: ID of post.
                :param message: Reason of the report.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/posts/{post_id}/report"
                params = {
                    "message": message
                }
                return LolzteamApi.send_request(self=self.__api, method="POST", url=url, params=params)

        class __Threads:
            def __init__(self, __api_self):
                self.__api = __api_self

            def get_threads(self, forum_id: int, thread_ids: str = None, creator_user_id: int = None,
                            sticky: bool = None,
                            thread_prefix_id: int = None, thread_tag_id: int = None, page: int = None,
                            limit: int = None,
                            order: str = None):
                """
                GET https://api.zelenka.guru/threads

                List of threads in a forum (with pagination).

                Required scopes: read

                :param forum_id: ID of the containing forum.
                :param thread_ids: ID's of needed threads (separated by comma). If this parameter is set, all other filtering parameters will be ignored.
                :param creator_user_id: Filter to get only threads created by the specified user.
                :param sticky: Filter to get only sticky <sticky=1> or non-sticky <sticky=0> threads. By default, all threads will be included and sticky ones will be at the top of the result on the first page. In mixed mode, sticky threads are not counted towards threads_total and does not affect pagination.
                :param thread_prefix_id: Filter to get only threads with the specified prefix.
                :param thread_tag_id: Filter to get only threads with the specified tag.
                :param page: Page number of threads.
                :param limit: Number of threads in a page.
                :param order: Can be [natural, thread_create_date, thread_create_date_reverse, thread_update_date, thread_update_date_reverse, thread_view_count, thread_view_count_reverse, thread_post_count, thread_post_count_reverse]
                :return: json server response
                """
                url = f"https://api.zelenka.guru/threads"
                if sticky:  # Костыль, пока не пофиксят недочет #43
                    sticky = 1
                else:
                    sticky = 0
                params = {
                    "forum_id": forum_id,
                    "thread_ids": thread_ids,
                    "creator_user_id": creator_user_id,
                    "sticky": sticky,
                    "thread_prefix_id": thread_prefix_id,
                    "thread_tag_id": thread_tag_id,
                    "page": page,
                    "limit": limit,
                    "order": order
                }
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url, params=params)

            def get(self, thread_id: int):
                """
                GET https://api.zelenka.guru/threads/{thread_id}

                Detail information of a thread.

                Required scopes: read

                :param thread_id: ID of thread.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/threads/{thread_id}"
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url)

            def create(self, forum_id: int, thread_title: str, post_body: str, thread_prefix_id: int = None,
                       thread_tags: str = None):
                """
                POST https://api.zelenka.guru/threads

                Create a new thread.

                Required scopes: post

                :param forum_id: ID of the target forum.
                :param thread_title: Title of the new thread.
                :param post_body: Content of the new thread.
                :param thread_prefix_id: ID of a prefix for the new thread.
                :param thread_tags: Thread tags for the new thread.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/threads"
                params = {
                    "forum_id": forum_id,
                    "thread_title": thread_title,
                    "post_body": post_body,
                    "thread_prefix_id": thread_prefix_id,
                    "thread_tags": thread_tags
                }
                return LolzteamApi.send_request(self=self.__api, method="POST", url=url, params=params)

            def delete(self, thread_id: int, reason: str = None):
                """
                DELETE https://api.zelenka.guru/threads/{thread_id}

                Delete a thread.

                Required scopes: post

                :param thread_id: ID of thread.
                :param reason: Reason of the thread removal.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/threads/{thread_id}"
                params = {
                    "reason": reason
                }
                return LolzteamApi.send_request(self=self.__api, method="DELETE", url=url, params=params)

            def followers(self, thread_id: int):
                """
                GET https://api.zelenka.guru/threads/thread_id/followers

                List of a thread's followers. For privacy reason, only the current user will be included in the list.

                Required scopes: read

                :param thread_id: ID of thread.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/threads/{thread_id}/followers"
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url)

            def followed(self, total: bool = None):
                """
                GET https://api.zelenka.guru/forums/followed

                List of followed forums by current user.

                Required scopes: read

                :param total: If included in the request, only the forum count is returned as forums_total.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/forums/followed"
                if True:  # Костыль, пока не пофиксят недочет #43
                    if total:
                        total = 1
                    else:
                        total = 0
                params = {
                    "total": total
                }
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url, params=params)

            def follow(self, thread_id: int, email: bool = None):
                """
                POST https://api.zelenka.guru/threads/{thread_id}/followers

                Follow a thread.

                Required scopes: post

                :param thread_id: ID of thread.
                :param email: Whether to receive notification as email.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/threads/{thread_id}/followers"
                if True:  # Костыль, пока не пофиксят недочет #63
                    if email:
                        email = 1
                params = {
                    "email": email
                }
                return LolzteamApi.send_request(self=self.__api, method="POST", url=url, params=params)

            def unfollow(self, thread_id: int):
                """
                DELETE https://api.zelenka.guru/threads/{thread_id}/followers

                Unfollow a thread.

                Required scopes: post

                :param thread_id: ID of thread.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/threads/{thread_id}/followers"
                return LolzteamApi.send_request(self=self.__api, method="DELETE", url=url)

            def navigation(self, thread_id: int):
                """
                GET https://api.zelenka.guru/threads/{thread_id}/navigaion

                List of navigation elements to reach the specified thread.

                Required scopes: read

                :param thread_id: ID of thread.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/threads/{thread_id}/navigaion"
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url)

            def votes(self, thread_id: int):
                """
                GET https://api.zelenka.guru/threads/{thread_id}/pool

                Detail information of a poll.

                Required scopes: read

                :param thread_id: ID of thread.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/threads/{thread_id}/pool"
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url)

            def vote(self, thread_id: int, response_id: int = None, response_ids: list[int] = None):
                """
                GET https://api.zelenka.guru/threads/{thread_id}/pool

                Vote on a thread poll.

                Required scopes: post

                :param thread_id: ID of thread.
                :param response_id: The id of the response to vote for. Can be skipped if response_ids set.
                :param response_ids: An array of ids of responses (if the poll allows multiple choices).

                :return: json server response
                """
                url = f"https://api.zelenka.guru/threads/{thread_id}/poll/votes"
                if type(response_ids) == list:
                    for element in response_ids:
                        if not isinstance(element, int):
                            raise TypeError("All response_ids need to be integer")

                    params = {
                        "response_ids[]": response_ids
                    }
                    return LolzteamApi.send_request(self=self.__api, method="POST", url=url, params=params)
                else:
                    params = {
                        "response_id": response_id
                    }
                    response = requests.post(url=url, params=params, headers=self.__api.headers)
                    self.__api.auto_delay_time = time.time()
                    response_json = response.json()
                    return response_json

            def new(self, forum_id: int = None, limit: int = None, data_limit: int = None):
                """
                GET https://api.zelenka.guru/threads/new

                List of unread threads (must be logged in).

                Required scopes: read

                :param forum_id: ID of the container forum to search for threads. Child forums of the specified forum will be included in the search.
                :param limit: Maximum number of result threads. The limit may get decreased if the value is too large (depending on the system configuration).
                :param data_limit: Number of thread data to be returned. Default value is 20.
                :return: json server response
                """
                url = f"https://api.zelenka.guru/threads/new"
                params = {
                    "forum_id": forum_id,
                    "limit": limit,
                    "data_limit": data_limit
                }
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url, params=params)

            def recent(self, days: int = None, forum_id: int = None, limit: int = None, data_limit: int = None):
                """
                GET https://api.zelenka.guru/threads/recent

                List of recent threads.

                Required scopes: read

                :param days: Maximum number of days to search for threads.
                :param forum_id: ID of the container forum to search for threads. Child forums of the specified forum will be included in the search.
                :param limit: Maximum number of result threads. The limit may get decreased if the value is too large (depending on the system configuration).
                :param data_limit: Number of thread data to be returned. Default value is 20.
                :return: json server response
                """
                url = f"https://api.zelenka.guru/threads/recent"
                params = {
                    "days": days,
                    "forum_id": forum_id,
                    "limit": limit,
                    "data_limit": data_limit
                }
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url, params=params)

            def bump(self, thread_id: int):
                """
                POST https://api.zelenka.guru/threads/{thread_id}/bump

                Bump a thread.

                Required scopes: post

                :param thread_id: ID of thread.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/threads/{thread_id}/bump"
                return LolzteamApi.send_request(self=self.__api, method="POST", url=url)

        class __Tags:
            def __init__(self, __api_self):
                self.__api = __api_self

            def popular(self):
                """
                GET https://api.zelenka.guru/tags

                List of popular tags (no pagination).

                Required scopes: get

                :return: json server response
                """
                url = f"https://api.zelenka.guru/tags"
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url)

            def tags(self, page: int = None, limit: int = None):
                """
                GET https://api.zelenka.guru/tags/list

                List of tags.

                Required scopes: post


                :param page: Page number of tags list.
                :param limit: Limit of tags on a page.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/tags/list"
                params = {
                    "page": page,
                    "limit": limit
                }
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url, params=params)

            def tagged(self, tag_id: int, page: int = None, limit: int = None):
                """
                GET https://api.zelenka.guru/tags/tag_id

                List of tagged contents.

                Required scopes: read

                :param tag_id:
                :param page: Page number of tags list.
                :param limit:

                :return: json server response
                """
                url = f"https://api.zelenka.guru/tags/{tag_id}"
                params = {
                    "page": page,
                    "limit": limit
                }
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url, params=params)

            def find(self, tag: str):
                """
                GET https://api.zelenka.guru/tags/find

                Filtered list of tags.

                Required scopes: read

                :param tag: tag to filter. Tags start with the query will be returned.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/tags/find"
                params = {
                    "tag": tag
                }
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url, params=params)

        class __Users:
            class __Avatar:
                def __init__(self, __api_self):
                    self.__api = __api_self

                def upload(self, avatar: bytes, user_id: int = None):
                    """
                    POST https://api.zelenka.guru/users/user_id/avatar

                    Upload avatar for a user.

                    Required scopes: post / admincp

                    :param user_id: ID of user. If you do not specify the user_id, then you will change the avatar of the current user
                    :param avatar: Binary data of the avatar.

                    :return: json server response
                    """
                    if user_id is None:
                        url = f"https://api.zelenka.guru/users/me/avatar"
                    else:
                        url = f"https://api.zelenka.guru/users/{user_id}/avatar"
                    files = {
                        "avatar": avatar
                    }
                    return LolzteamApi.send_request(self=self.__api, method="POST", url=url, files=files)

                def delete(self, user_id: int = None):
                    """
                    DELETE https://api.zelenka.guru/users/user_id/avatar

                    Delete avatar for a user.

                    Required scopes: post / admincp

                    :param user_id: ID of user. If you do not specify the user_id, then you will change the avatar of the current user

                    :return: json server response
                    """
                    if user_id is None:
                        url = f"https://api.zelenka.guru/users/me/avatar"
                    else:
                        url = f"https://api.zelenka.guru/users/{user_id}/avatar"
                    return LolzteamApi.send_request(self=self.__api, method="DELETE", url=url)

            def __init__(self, __api_self):
                self.__api = __api_self
                self.avatar = self.__Avatar(self.__api)

            def users(self, page: int = None, limit: int = None):
                """
                GET https://api.zelenka.guru/users

                List of users (with pagination).

                Required scopes: read

                :param page: Page number of users.
                :param limit: Number of users in a page.
                :return: json server response
                """
                url = f"https://api.zelenka.guru/users"
                params = {
                    "page": page,
                    "limit": limit
                }
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url, params=params)

            def fields(self):
                """
                GET https://api.zelenka.guru/users/fields

                List of user fields.

                Required scopes: read

                :return: json server response
                """

                url = f"https://api.zelenka.guru/users/fields"
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url)

            def search(self, username: str = None, user_email: str = None, custom_fields: dict = None):
                """
                GET https://api.zelenka.guru/users/find

                List of users (with pagination).

                Required scopes: read / admincp

                :param username: Username to filter. Usernames start with the query will be returned.
                :param user_email: Email to filter. Requires admincp scope.
                :param custom_fields: Custom fields to filter. Example: {"telegram": "Telegram_Login"}

                :return: json server response
                """
                url = f"https://api.zelenka.guru/users/find"
                params = {
                    "username": username,
                    "user_email": user_email,
                }
                for key, value in custom_fields.items():
                    cf = f"custom_fields[{key}]"
                    params[cf] = value
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url, params=params)

            def get(self, user_id: int = None):
                """
                GET https://api.zelenka.guru/users/user_id

                Detail information of a user.

                Required scopes: read

                :param user_id: ID of user
                :return: json server response
                """
                url = f"https://api.zelenka.guru/users/{user_id}"
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url)

            def edit(self, user_id: int, password: str = None, password_old: str = None, password_algo: str = None,
                     user_email: str = None, username: str = None, user_title: str = None, primary_group_id: int = None,
                     secondary_group_ids: list[int] = None, user_dob_day: int = None, user_dob_month: int = None,
                     user_dob_year: int = None, fields: dict = None):
                """
                PUT https://api.zelenka.guru/users/user_id

                Edit a user.

                Encryption:
                For sensitive information like password, encryption can be used to increase data security. For all encryption with key support, the client_secret will be used as the key. List of supported encryptions:
                aes128: AES 128-bit encryption (mode: ECB, padding: PKCS#7). Because of algorithm limitation, the binary md5 hash of key will be used instead of the key itself.

                Required scopes: read / admincp

                :param user_id: ID of user
                :param password: New password.
                :param password_old: Data of the existing password, it is not required if (1) the current authenticated user has user admin permission, (2) the admincp scope is granted and (3) the user being edited is not the current authenticated user.
                :param password_algo: Algorithm used to encrypt the password and password_old parameters. See Encryption section for more information.
                :param user_email:New email of the user.
                :param username: New username of the user. Changing username requires Administrator permission.
                :param user_title: New custom title of the user.
                :param primary_group_id: ID of new primary group.
                :param secondary_group_ids: Array of ID's of new secondary groups.
                :param user_dob_day: Date of birth (day) of the new user.
                :param user_dob_month: Date of birth (month) of the new user.
                :param user_dob_year: Date of birth (year) of the new user.
                :param fields: Array of values for user fields.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/users/{user_id}"
                params = {
                    "password": password,
                    "password_old": password_old,
                    "password_algo": password_algo,
                    "user_email": user_email,
                    "username": username,
                    "user_title": user_title,
                    "primary_group_id": primary_group_id,
                    "secondary_group_ids[]": secondary_group_ids,
                    "user_dob_day": user_dob_day,
                    "user_dob_month": user_dob_month,
                    "user_dob_year": user_dob_year,
                }
                for key, value in fields.items():
                    field = f"fields[{key}]"
                    params[field] = value
                return LolzteamApi.send_request(self=self.__api, method="PUT", url=url, params=params)

            def follow(self, user_id: int):
                """
                POST https://api.zelenka.guru/users/user_id/followers

                Follow a user.

                Required scopes: post

                :param user_id: ID of user

                :return: json server response
                """
                url = f"https://api.zelenka.guru/users/{user_id}/followers"

                return LolzteamApi.send_request(self=self.__api, method="POST", url=url)

            def unfollow(self, user_id: int):
                """
                DELETE https://api.zelenka.guru/users/user_id/followers

                Unfollow a user.

                Required scopes: post

                :param user_id: ID of user

                :return: json server response
                """
                url = f"https://api.zelenka.guru/users/{user_id}/followers"
                return LolzteamApi.send_request(self=self.__api, method="DELETE", url=url)

            def followers(self, user_id: int, order: str = None, page: int = None, limit: int = None):
                """
                GET https://api.zelenka.guru/users/user_id/followers

                List of users (with pagination).

                Required scopes: read

                :param user_id: ID of user
                :param order: Ordering of followers. Support: natural, follow_date, follow_date_reverse
                :param page: Page number of followers.
                :param limit: Number of followers in a page.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/users/{user_id}/followers"
                params = {
                    "order": order,
                    "page": page,
                    "limit": limit
                }
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url, params=params)

            def followings(self, user_id: int, order: str = None, page: int = None, limit: int = None):
                """
                GET https://api.zelenka.guru/users/user_id/followings

                List of users whom are followed by a user.

                Required scopes: read

                :param user_id: ID of user
                :param order: Ordering of users. Support: natural, follow_date, follow_date_reverse
                :param page: Page number of users.
                :param limit: Number of users in a page.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/users/{user_id}/followings"
                params = {
                    "order": order,
                    "page": page,
                    "limit": limit
                }
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url, params=params)

            def ignored(self, total: bool = None):
                """
                GET https://api.zelenka.guru/users/ignored

                List of ignored users of current user.

                Required scopes: read

                :param total: If included in the request, only the user count is returned as users_total.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/users/ignored"
                if True:  # Костыль, пока не пофиксят недочет #43
                    if total:
                        total = 1
                    else:
                        total = 0
                params = {
                    "total": total
                }
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url, params=params)

            def ignore(self, user_id: int):
                """
                POST https://api.zelenka.guru/users/user_id/ignore

                Ignore a user.

                Required scopes: post

                :param user_id: ID of user

                :return: json server response
                """

                url = f"https://api.zelenka.guru/users/{user_id}/ignore"
                return LolzteamApi.send_request(self=self.__api, method="POST", url=url)

            def unignore(self, user_id: int):
                """
                DELETE https://api.zelenka.guru/users/user_id/ignore

                Ignore a user.

                Required scopes: post

                :param user_id: ID of user

                :return: json server response
                """

                url = f"https://api.zelenka.guru/users/{user_id}/ignore"
                return LolzteamApi.send_request(self=self.__api, method="DELETE", url=url)

            def groups(self, user_id: int = None):
                """
                GET https://api.zelenka.guru/users/user_id/groups

                List of a user's groups.

                Required scopes: read / admincp

                :param user_id: ID of user. If user_id skipped, method will return current user groups

                :return: json server response
                """
                if type(user_id) is None:
                    url = f"https://api.zelenka.guru/users/groups"
                else:
                    url = f"https://api.zelenka.guru/users/{user_id}/groups"
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url)

        class __Profile_posts:
            class __Profile_posts_comments:
                def __init__(self, __api_self):
                    self.__api = __api_self

                def comments(self, profile_post_id: int, before: int = None, limit: int = None):
                    """
                    GET https://api.zelenka.guru/profile-posts/profile_post_id/comments

                    List of comments of a profile post.

                    Required scopes: read

                    :param profile_post_id: ID of profile post.
                    :param before: Date to get older comments. Please note that this entry point does not support the page parameter, but it still does support limit.
                    :param limit: Number of profile posts in a page.

                    :return: json server response
                    """
                    url = f"https://api.zelenka.guru/profile-posts/{profile_post_id}/comments"
                    params = {
                        "before": before,
                        "limit": limit
                    }
                    return LolzteamApi.send_request(self=self.__api, method="GET", url=url, params=params)

                def get(self, profile_post_id: int, comment_id: int):
                    """
                    GET https://api.zelenka.guru/profile-posts/profile_post_id/comments/comment_id

                    Detail information of a profile post comment.

                    Required scopes: read

                    :param profile_post_id: ID of profile post.
                    :param comment_id: ID of profile post comment

                    :return: json server response
                    """
                    url = f"https://api.zelenka.guru/profile-posts/{profile_post_id}/comments/{comment_id}"
                    return LolzteamApi.send_request(self=self.__api, method="GET", url=url)

                def create(self, profile_post_id: int, comment_body: str):
                    """
                    POST https://api.zelenka.guru/profile-posts/profile_post_id/comments

                    Create a new profile post comment.

                    Required scopes: post

                    :param profile_post_id: ID of profile post.
                    :param comment_body: Content of the new profile post comment.

                    :return: json server response
                    """
                    url = f"https://api.zelenka.guru/profile-posts/{profile_post_id}/comments"
                    params = {
                        "comment_body": comment_body,
                    }
                    return LolzteamApi.send_request(self=self.__api, method="POST", url=url, params=params)

                def delete(self, profile_post_id: int, comment_id: int, reason: str = None):
                    """
                    DELETE https://api.zelenka.guru/profile-posts/profile_post_id/comments/comment_id

                    Delete a profile post's comment.

                    Required scopes: post

                    :param profile_post_id: ID of profile post.
                    :param comment_id: ID of profile post comment
                    :param reason: Reason of the report.

                    :return: json server response
                    """
                    url = f"https://api.zelenka.guru/profile-posts/{profile_post_id}/comments/{comment_id}"
                    params = {
                        "reason": reason
                    }
                    return LolzteamApi.send_request(self=self.__api, method="DELETE", url=url, params=params)

            def __init__(self, __api_self):
                self.__api = __api_self
                self.comments = self.__Profile_posts_comments(self.__api)

            def timeline(self, user_id: int, page: int = None, limit: int = None):
                """
                GET https://api.zelenka.guru/users/user_id/timeline

                List of contents created by user (with pagination).

                Required scopes: read

                :param user_id: ID of user
                :param page: Page number of contents.
                :param limit: Number of contents in a page.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/users/{user_id}/timeline"
                params = {
                    "page": page,
                    "limit": limit
                }
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url, params=params)

            def get(self, profile_post_id: int):
                """
                GET https://api.zelenka.guru/profile-posts/profile_post_id

                Detail information of a profile post.

                Required scopes: read

                :param profile_post_id: ID of profile post.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/profile-posts/{profile_post_id}"
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url)

            def create(self, user_id: int, post_body: str):
                """
                POST https://api.zelenka.guru/users/user_id/timeline

                Create a new profile post on a user timeline.

                Required scopes: post

                :param user_id: ID of user
                :param post_body: Content of the new profile post.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/users/{user_id}/timeline"
                params = {
                    "post_body": post_body
                }
                return LolzteamApi.send_request(self=self.__api, method="POST", url=url, params=params)

            def edit(self, profile_post_id: int, post_body: str):
                """
                PUT https://api.zelenka.guru/profile-posts/profile_post_id

                Edit a profile post.

                Required scopes: post

                :param profile_post_id: ID of profile post.
                :param post_body: New content of the profile post.

                :return: json server response
                """

                url = f"https://api.zelenka.guru/profile-posts/{profile_post_id}"
                params = {
                    "post_body": post_body
                }
                return LolzteamApi.send_request(self=self.__api, method="PUT", url=url, params=params)

            def delete(self, profile_post_id: int, reason: str = None):
                """
                DELETE https://api.zelenka.guru/profile-posts/profile_post_id

                Delete a profile post.

                Required scopes: post

                :param profile_post_id: ID of profile post.
                :param reason: Reason of the profile post removal.


                :return: json server response
                """
                url = f"https://api.zelenka.guru/profile-posts/{profile_post_id}"
                params = {
                    "reason": reason
                }
                return LolzteamApi.send_request(self=self.__api, method="DELETE", url=url, params=params)

            def likes(self, profile_post_id: int):
                """
                GET https://api.zelenka.guru/profile-posts/profile_post_id/likes

                List of users who liked a profile post.

                Required scopes: read

                :param profile_post_id: ID of profile post.

                :return: json server response
                """

                url = f"https://api.zelenka.guru/profile-posts/{profile_post_id}/likes"
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url)

            def like(self, profile_post_id: int):
                """
                POST https://api.zelenka.guru/profile-posts/profile_post_id/likes

                Like a profile post.

                Required scopes: post

                :param profile_post_id: ID of profile post.

                :return: json server response
                """

                url = f"https://api.zelenka.guru/profile-posts/{profile_post_id}/likes"

                return LolzteamApi.send_request(self=self.__api, method="POST", url=url)

            def unlike(self, profile_post_id: int):
                """
                DELETE https://api.zelenka.guru/profile-posts/profile_post_id/likes

                Unlike a profile post.

                Required scopes: post

                :param profile_post_id: ID of profile post.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/profile-posts/{profile_post_id}/likes"
                return LolzteamApi.send_request(self=self.__api, method="DELETE", url=url)

            def report(self, profile_post_id: int, message: str):
                """
                POST https://api.zelenka.guru/profile-posts/profile_post_id

                Report a profile post.

                Required scopes: post

                :param profile_post_id: ID of profile post.
                :param message: Reason of the report.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/profile-posts/{profile_post_id}"
                params = {
                    "message": message
                }
                return LolzteamApi.send_request(self=self.__api, method="POST", url=url, params=params)

        class __Search:
            def __init__(self, __api_self):
                self.__api = __api_self

            def all(self, q: str = None, tag: str = None, forum_id: int = None, user_id: int = None, page: int = None,
                    limit: int = None):
                """
                POST https://api.zelenka.guru/search

                Search for threads.

                Required scopes: post
                :param q: Search query. Can be skipped if user_id is set.
                :param tag: Tag to search for tagged contents.
                :param forum_id: ID of the container forum to search for contents. Child forums of the specified forum will be included in the search.
                :param user_id: ID of the creator to search for contents.
                :param page: Page number of results.
                :param limit: Number of results in a page.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/search"
                params = {
                    "q": q,
                    "tag": tag,
                    "forum_id": forum_id,
                    "user_id": user_id,
                    "page": page,
                    "limit": limit
                }
                return LolzteamApi.send_request(self=self.__api, method="POST", url=url, params=params)

            def thread(self, q: str = None, tag: str = None, forum_id: int = None, user_id: int = None,
                       page: int = None,
                       limit: int = None, data_limit: int = None):
                """
                POST https://api.zelenka.guru/search/threads

                Search for threads.

                Required scopes: post
                :param q: Search query. Can be skipped if user_id is set.
                :param tag: Tag to search for tagged contents.
                :param forum_id: ID of the container forum to search for contents. Child forums of the specified forum will be included in the search.
                :param user_id: ID of the creator to search for contents.
                :param page: Page number of results.
                :param limit: Number of results in a page.
                :param data_limit: Number of thread data to be returned.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/search/threads"
                params = {
                    "q": q,
                    "tag": tag,
                    "forum_id": forum_id,
                    "user_id": user_id,
                    "page": page,
                    "limit": limit,
                    "data_limit": data_limit
                }
                return LolzteamApi.send_request(self=self.__api, method="POST", url=url, params=params)

            def post(self, q: str = None, tag: str = None, forum_id: int = None, user_id: int = None, page: int = None,
                     limit: int = None, data_limit: int = None):
                """
                POST https://api.zelenka.guru/search/posts

                Search for posts.

                Required scopes: post
                :param q: Search query. Can be skipped if user_id is set.
                :param tag: Tag to search for tagged contents.
                :param forum_id: ID of the container forum to search for contents. Child forums of the specified forum will be included in the search.
                :param user_id: ID of the creator to search for contents.
                :param page: Page number of results.
                :param limit: Number of results in a page.
                :param data_limit: Number of thread data to be returned.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/search/posts"
                params = {
                    "q": q,
                    "tag": tag,
                    "forum_id": forum_id,
                    "user_id": user_id,
                    "page": page,
                    "limit": limit,
                    "data_limit": data_limit
                }
                return LolzteamApi.send_request(self=self.__api, method="POST", url=url, params=params)

            def tag(self, tag: str = None, tags: list[str] = None, page: int = None, limit: int = None):
                """
                POST https://api.zelenka.guru/search/tagged

                Search for tagged contents.

                Required scopes: post
                :param tag: Tag to search for tagged contents.
                :param tags: Array of tags to search for tagged contents.
                :param page: Page number of results.
                :param limit: Number of results in a page.
                :return: json server response
                """
                url = f"https://api.zelenka.guru/search/tagged"
                params = {
                    "tag": tag,
                    "tags[]": tags,
                    "page": page,
                    "limit": limit,
                }
                return LolzteamApi.send_request(self=self.__api, method="POST", url=url, params=params)

        class __Notifications:
            def __init__(self, __api_self):
                self.__api = __api_self

            def get_notifications(self):
                """
                GET https://api.zelenka.guru/notifications

                List of notifications (both read and unread).

                Required scopes: read

                :return: json server response
                """
                url = f"https://api.zelenka.guru/notifications"
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url)

            def get_notification(self, notification_id: int):
                """
                GET https://api.zelenka.guru/notifications

                Get associated content of notification. The response depends on the content type.

                Required scopes: read
                :param notification_id: ID of notification.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/notifications/{notification_id}/content"
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url)

            def read_notification(self, notification_id: int = None):
                """
                POST https://api.zelenka.guru/notifications/read

                Mark single notification or all existing notifications read.

                Required scopes: post
                :param notification_id: ID of notification. If notification_id is omitted, it's mark all existing notifications as read.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/notifications/read"
                params = {
                    "notification_id": notification_id
                }
                return LolzteamApi.send_request(self=self.__api, method="POST", url=url, params=params)

            def send_custom_notification(self, user_id: int = None, username: str = None, message: str = None,
                                         message_html: str = None, notification_type: str = None,
                                         extra_data: str = None):
                """
                POST https://api.zelenka.guru/notifications/custom

                Send a custom alert.

                Required scopes: post, Send custom alert permission
                :param user_id: The alert receiver.
                :param username: The alert receiver.
                :param message: The alert message.
                :param message_html: The alert message.
                :param notification_type: The notification type.
                :param extra_data: Extra data when sending alert. Предположительно это словарик, но я не уверен

                :return: json server response
                """
                # По приколу добавил получается. Шанс того, что это заюзает реквест, томас или григорий крайне мал

                url = f"https://api.zelenka.guru/notifications/custom"
                params = {
                    "user_id": user_id,
                    "username": username,
                    "message": message,
                    "message_html": message_html,
                    "notification_type": notification_type,
                    "extra_data": extra_data
                }
                return LolzteamApi.send_request(self=self.__api, method="POST", url=url, params=params)

        class __Conversations:
            class __Conversations_messages:
                def __init__(self, __api_self):
                    self.__api = __api_self

                def messages(self, conversation_id: int, page: int = None, limit: int = None, order: str = None,
                             before: int = None, after: int = None):
                    """
                    GET https://api.zelenka.guru/conversation-messages

                    List of messages in a conversation (with pagination).

                    Required scopes: conversate, read

                    :param conversation_id: ID of conversation.
                    :param page: Page number of messages.
                    :param limit: Number of messages in a page.
                    :param order: Ordering of messages. Can be [natural, natural_reverse].
                    :param before: Date to get older messages.
                    :param after: Date to get newer messages.

                    :return: json server response
                    """
                    url = f"https://api.zelenka.guru/conversation-messages"
                    params = {
                        "conversation_id": conversation_id,
                        "page": page,
                        "limit": limit,
                        "order": order,
                        "before": before,
                        "after": after
                    }
                    return LolzteamApi.send_request(self=self.__api, method="GET", url=url, params=params)

                def get(self, message_id: int):
                    """
                    GET https://api.zelenka.guru/conversation-messages/message_id

                    Detail information of a message.

                    Required scopes: conversate, read

                    :param message_id: ID of conversation message.

                    :return: json server response
                    """
                    url = f"https://api.zelenka.guru/conversation-messages/{message_id}"
                    return LolzteamApi.send_request(self=self.__api, method="GET", url=url)

                def create(self, conversation_id: int, message_body: str):
                    """
                    POST https://api.zelenka.guru/conversation-messages

                    Create a new conversation message.

                    Required scopes: conversate, post

                    :param conversation_id: ID of conversation.
                    :param message_body: Content of the new message.

                    :return: json server response
                    """
                    url = f"https://api.zelenka.guru/conversation-messages"
                    params = {
                        "conversation_id": conversation_id,
                        "message_body": message_body
                    }
                    return LolzteamApi.send_request(self=self.__api, method="POST", url=url, params=params)

                def edit(self, message_id: int, message_body: str):
                    """
                    PUT https://api.zelenka.guru/conversation-messages/message_id

                    Edit a message.

                    Required scopes: conversate, post

                    :param message_id: ID of conversation message.
                    :param message_body: New content of the message.

                    :return: json server response
                    """
                    url = f"https://api.zelenka.guru/conversation-messages/{message_id}"
                    params = {
                        "message_body": message_body
                    }
                    return LolzteamApi.send_request(self=self.__api, method="PUT", url=url, params=params)

                def delete(self, message_id: int):
                    """
                    DELETE https://api.zelenka.guru/conversation-messages/message_id

                    Delete a message.

                    Required scopes: conversate, post

                    :param message_id: ID of conversation message.

                    :return: json server response
                    """
                    url = f"https://api.zelenka.guru/conversation-messages/{message_id}"
                    return LolzteamApi.send_request(self=self.__api, method="DELETE", url=url)

                def report(self, message_id: int, message: str = None):
                    """
                    POST https://api.zelenka.guru/conversation-messages/message_id/report

                    Create a new conversation message.

                    Required scopes: conversate, post

                    :param message_id: ID of conversation message.
                    :param message : Reason of the report.

                    :return: json server response
                    """

                    url = f"https://api.zelenka.guru/conversation-messages/{message_id}/report"
                    params = {
                        "message": message
                    }
                    return LolzteamApi.send_request(self=self.__api, method="POST", url=url, params=params)

            def __init__(self, __api_self):
                self.__api = __api_self
                self.messages = self.__Conversations_messages(self.__api)

            def conversations(self, page: int = None, limit: int = None):
                """
                GET https://api.zelenka.guru/conversations

                List of conversations (with pagination).

                Required scopes: conversate, read

                :param page: Page number of conversations.
                :param limit: Number of conversations in a page.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/conversations"
                params = {
                    "page": page,
                    "limit": limit
                }
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url, params=params)

            def get(self, conversation_id: int):
                """
                GET https://api.zelenka.guru/conversations/conversation_id

                Detail information of a conversation.

                Required scopes: conversate, read

                :param conversation_id: ID of conversation.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/conversations/{conversation_id}"
                return LolzteamApi.send_request(self=self.__api, method="GET", url=url)

            def delete(self, conversation_id: int):
                """
                DELETE https://api.zelenka.guru/conversations/conversation_id

                Delete a conversation.

                Required scopes: conversate, post

                :param conversation_id: ID of conversation.

                :return: json server response
                """
                url = f"https://api.zelenka.guru/conversations/{conversation_id}"
                return LolzteamApi.send_request(self=self.__api, method="DELETE", url=url)

        def navigation(self, parent: int = None):
            """
            GET https://api.zelenka.guru/navigation

            List of navigation elements within the system.

            Required scopes: read

            :param parent: ID of parent element. If exists, filter elements that are direct children of that element.

            :return: json server response
            """
            url = f"https://api.zelenka.guru/navigation"
            params = {
                "parent": parent
            }
            return LolzteamApi.send_request(self=self.__api, method="GET", url=url, params=params)

        def batch(self, request_body: list[dict]):
            """
            POST https://api.zelenka.guru/batch

            Execute multiple API requests at once.(10 max)

            Example scheme:

            [
                {
                "id": "1",
                "uri": "https://api.zelenka.guru/users/2410024",
                "method": "GET",
                "params": {}
                }
            ]
            :param request_body: Use scheme above
            :return: json server response
            """

            url = f"https://api.zelenka.guru/batch"
            return LolzteamApi.send_request(self=self.__api, method="POST", url=url, data=json.dumps(request_body))
