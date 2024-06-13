import unittest
from unittest.mock import Mock
from django.test import RequestFactory
from circles.api.circles_views import FollowAPI

class TestFollowAPI(unittest.TestCase):
    
    def test_user_follows_circle_successfully(self):
        # Setup
        follow_api = FollowAPI()
        request = RequestFactory().post('/follow/')

        # Null pointer reference
        self.assertIsNotNone(follow_api)
        self.assertIsNotNone(request)

        # Unhandled exception
        try:
            request.user = Mock(is_authenticated=True)
            circle = Mock(followers=Mock(all=Mock(return_value=[])),
                          user=Mock(circles=Mock(connections=Mock(all=Mock(return_value=[])))))
            pk = 1

            # Action
            response = follow_api.post(request, pk)

            # Assertion
            self.assertEqual(response.data, {'updated': True, 'following': True})
        except Exception as e:
            self.fail("Unexpected exception raised: {}".format(e))

    def test_user_unfollows_circle_successfully(self):
        # Setup
        follow_api = FollowAPI()
        request = RequestFactory().post('/unfollow/')

        # Null pointer reference
        self.assertIsNotNone(follow_api)
        self.assertIsNotNone(request)

        # Unhandled exception
        try:
            request.user = Mock(is_authenticated=True)
            circle = Mock(followers=Mock(all=Mock(return_value=[request.user])),
                          user=Mock(circles=Mock(connections=Mock(all=Mock(return_value=[request.user])))))
            pk = 1

            # Action
            response = follow_api.post(request, pk)

            # Assertion
            self.assertEqual(response.data, {'updated': True, 'following': False})
        except Exception as e:
            self.fail("Unexpected exception raised: {}".format(e))

    def test_circle_user_added_to_connections_when_following_back(self):
        # Setup
        follow_api = FollowAPI()
        request = RequestFactory().post('/follow_back/')

        # Null pointer reference
        self.assertIsNotNone(follow_api)
        self.assertIsNotNone(request)

        # Unhandled exception
        try:
            request.user = Mock(is_authenticated=True)
            circle = Mock(followers=Mock(all=Mock(return_value=[circle.user])),
                          user=Mock(circles=Mock(followers=Mock(all=Mock(return_value=[circle.user])),
                                                 connections=Mock(all=Mock(return_value=[])))))
            pk = 1

            # Action
            response = follow_api.post(request, pk)

            # Assertion
            self.assertEqual(response.data, {'updated': True, 'following': True})
        except Exception as e:
            self.fail("Unexpected exception raised: {}".format(e))

if __name__ == '__main__':
    unittest.main()