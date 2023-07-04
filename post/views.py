from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.cache import cache
from logconfig.logger import get_logger
from .models import Post, Like, Follower
from .serializers import PostSerializer, FollowerSerializer
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page

logger = get_logger()

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class CreatePost(APIView):
    authentication_classes = [JWTAuthentication]

    # def post(self, request):
    #     """
    #               this method is used to create post data
    #           """
    #     serializer = PostSerializer(data=request.data)
    #     if serializer.is_valid():
    #         post = serializer.save(user_id=request.user.id)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    def post(self, request):
        """
        This method is used to create post data
        """
        try:
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                post = serializer.save(user_id=request.user.id)
                response_data = {
                    'message': 'Post created successfully.',
                    'status': 201,
                    'data': serializer.data
                }
                return Response(response_data, status=201)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400, "data": {}}, status=400)

    @cache_page(CACHE_TTL)
    def get(self, request, post_id):
        cache_key = f'post_{post_id}'
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            # Data retrieved from cache
            response_data = {
                'message': 'Data retrieved from cache.', 'data': cached_data}
            return Response(response_data, status=status.HTTP_200_OK)
        try:
            post = Post.objects.get(id=post_id)
            serializer = PostSerializer(post)
            data = {"message": "Retrieve Data Successfully", "status": 200, "data": serializer.data}
            cache.set(cache_key, data, CACHE_TTL)
            # Data retrieved from the database and stored in cache
            response_data = {
                'message': 'Data retrieved from the database and stored in cache.',
                'data': data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            response_data = {'message': 'Post not found.', 'data': {}}
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception(e)
            # Failed to retrieve post details from cache or database
            response_data = {'message': 'Failed to retrieve post details.', 'error': str(e), 'data': {}}
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def get(self, request, post_id):
    #     """
    #         this method is used to retrieve post data
    #     """
    #     try:
    #         user = Post.objects.get(id=post_id)
    #         serializer = PostSerializer(user)
    #         return Response({"message": "Retrieve Data  Successfully", "status": 200, "data": serializer.data},
    #                         status=200)
    #     except Exception as e:
    #         logger.exception(e)
    #         return Response({"message": str(e), "status": 400, "data": {}}, status=400)

    def put(self, request, post_id):
        """
                   this method is used to update post data
               """
        try:
            user = Post.objects.get(id=post_id)
            serializer = PostSerializer(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Updated Successfully", "status": 200, "data": serializer.data},
                            status=200)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400, "data": {}}, status=400)

    def delete(self, request, post_id):
        """
                   this method is used to delete post
               """
        try:
            user = Post.objects.get(id=post_id)
            user.delete()
            return Response({"message": " deleted Successfully", "status": 200, "data": {}},
                            status=200)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400, "data": {}}, status=400)

    def get(self, request):
        """
        All data Retrieve Successfully
        """
        try:
            user = Post.objects.all()
            serializer = PostSerializer(user, many=True)
            return Response({"message": "All data Retrieve Successfully", "status": 201, "data": serializer.data},
                            status=200)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)


class LikePostAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request, post_id):
        try:
            # Retrieve the post
            post = Post.objects.get(id=post_id)

            # Check if the user has already liked the post
            if Like.objects.filter(post=post, user=request.user).exists():
                return Response({'message': 'You have already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

            # Create a new Like object
            like = Like(post=post, user=request.user)
            like.save()
            # Update post likes count
            post.likes_count += 1
            post.save()
            return Response({'message': 'Post liked successfully', "status": 200}, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({'message': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception(e)
            return Response({'message': 'Failed to like the post.', 'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, post_id):
        try:
            # Retrieve the post
            post = Post.objects.get(id=post_id)

            post_serializer = PostSerializer(post)

            response_data = {
                'post': post_serializer.data,
                'like_count': post.likes_count
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Post.DoesNotExist:
            return Response({'message': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception(e)
            return Response({'message': 'Failed to retrieve post details.', 'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FollowerListAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request, user_id):
        try:
            # Retrieve the followers for the specified user
            followers = Follower.objects.filter(user_id=user_id)
            follower_serializer = FollowerSerializer(followers, many=True)
            return Response(follower_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({'message': 'Failed to retrieve followers.', 'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, user_id):
        try:
            # Retrieve the users that the specified user is following
            following = Follower.objects.filter(follower_id=user_id)

            following_serializer = FollowerSerializer(following, many=True)

            response_data = {'message': 'Following users retrieved successfully.','status':200,
                             'data': following_serializer.data}
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            response_data = {'message': 'Failed to retrieve following users.', 'error': str(e), 'status': 500, 'data': {}}
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, user_id):
        try:
            # Create a new Follower object to represent the relationship
            follower = Follower(user_id=user_id, follower=request.user)
            follower.save()
            return Response({'message': 'User followed successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({'message': 'Failed to follow the user.', 'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, user_id):
        try:
            followers = Follower.objects.filter(user_id=user_id, follower=request.user)
            if followers.exists():
                # Delete all the follower objects to remove the relationships
                followers.delete()
                return Response({'message': 'User unfollowed successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Follower relationship does not exist.'},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'Failed to unfollow the user.', 'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
