from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserSerializer
from rest_framework import status
from .models import Post,SavedLists,ListItem
from .serializers import ListItemSerializer,ListsSerializer
  
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"message": "User created successfully", "user": UserSerializer(user).data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# What i changed
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import PostSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class PostCreateView(APIView):
    # Change this to AllowAny to bypass JWT check
    permission_classes = [AllowAny]
    
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def get_posts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

    
@api_view(['GET'])
def get_post(request, pk):
    try:
        post = Post.objects.get(id=pk)
        serializer = PostSerializer(post, context = {'request': request})
        return Response(serializer.data)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=404)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_lists(request):
    savedlists, created = SavedLists.objects.get_or_create(user=request.user)
    serializer = ListsSerializer(savedlists)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_lists(request):
    post_id = request.data.get('post_id')
    post = Post.objects.get(id=post_id)
    savedlists, created = SavedLists.objects.get_or_create(user=request.user)
    item, created = ListItem.objects.get_or_create(savedlists=savedlists, post=post)
    if not created:
        item.quantity += 1
        item.save()
    return Response({'message': 'Product added to lists',"savedlists":ListsSerializer(savedlists).data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_lists_quantity(request):
    item_id = request.data.get('item_id')
    quantity = request.data.get('quantity')
   
    if not item_id or quantity is None:
        return Response({'error': 'Item ID and quantity are required'}, status=400)
    
    try:
        item = ListItem.objects.get(id=item_id)
        if int(quantity) < 1:
            item.delete()
            return Response({'error': 'Quantity must be at least 1'}, status=400)
        
        item.quantity = quantity
        item.save()
        serializer = ListItemSerializer(item)
        return Response(serializer.data)
    except ListItem.DoesNotExist:
        return Response({'error': 'List item not found'}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_lists(request):
    item_id = request.data.get('item_id')
    ListItem.objects.filter(id=item_id).delete()
    return Response({'message': 'Item removed from lists'})


# component generator code
# import environ
# import requests
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# import os

# # Initialize environ
# env = environ.Env()
# # Read the .env file (assuming it's in your project root)
# environ.Env.read_env()

# @csrf_exempt
# def nvidia_proxy(request, rest):
#     if request.method == "POST":
#         try:
#             user_data = json.loads(request.body)
#             # api_key = "6yH8C...api"  <-- Hardcoded version
#             api_key = os.getenv("NVIDIA_KEY") # <-- .env version
            
#             url = "https://integrate.api.nvidia.com/v1/chat/completions"
#             headers = {
#                 "Authorization": f"Bearer {api_key}",
#                 "Content-Type": "application/json",
#             }
            
#             response = requests.post(url, headers=headers, json=user_data)
#             return JsonResponse(response.json())
            
#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON"}, status=400)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)
    
#     return JsonResponse({"error": "Only POST allowed"}, status=405)
# import environ
# import requests
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# import os

# # Initialize environ
# env = environ.Env()
# # This looks for .env in your project root (where manage.py is)
# environ.Env.read_env()

# @csrf_exempt
# def nvidia_proxy(request, rest):
#     if request.method == "POST":
#         try:
#             # Get the key
#             api_key = env("NVIDIA_KEY", default=None)
#             url = f"https://integrate.api.nvidia.com/v1/{rest}"
            
#             headers = {
#                 "Authorization": f"Bearer {api_key}",
#                 "Content-Type": "application/json",
#             }
            
#             # Use request.body (the raw bytes) directly instead of json.loads
#             # This ensures the JSON formatting from the SDK remains perfect
#             response = requests.post(url, headers=headers, data=request.body)
            
#             # Check if NVIDIA returned JSON
#             try:
#                 response_data = response.json()
#             except:
#                 # If NVIDIA returns an error page (HTML), return the text
#                 return JsonResponse({"error": "NVIDIA returned non-JSON", "details": response.text}, status=response.status_code)

#             return JsonResponse(response_data, status=response.status_code)
            
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)

# views.py
# import environ
# import os
# import requests
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# # # Initialize environ
# env = environ.Env()
# # # This looks for .env in your project root (where manage.py is)
# environ.Env.read_env()

# @csrf_exempt
# def nvidia_proxy(request, rest=None):
#     if request.method != "POST":
#         return JsonResponse({"error": "Only POST allowed"}, status=405)

#     try:
#         api_key = os.getenv("NVIDIA_KEY")  # store in .env or settings.py
#         if not api_key:
#             return JsonResponse({"error": "Missing NVIDIA_API_KEY"}, status=500)

#         # Forward the request body to NVIDIA
#         response = requests.post(
#             f"https://integrate.api.nvidia.com/v1/{rest}",
#             headers={
#                 "Authorization": f"Bearer {api_key}",
#                 "Content-Type": "application/json",
#             },
#             json=request.json if hasattr(request, "json") else request.POST,
#         )

#         # Return NVIDIA’s response back to frontend
#         return JsonResponse(response.json(), status=response.status_code)

#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)
import environ
import os
import requests
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
<<<<<<< HEAD
from django.db import connection
=======
>>>>>>> d0cf1bbed744ff15a6acbf9b3951a34a8d813324

# Initialize environ
env = environ.Env()
# This looks for .env in your project root (where manage.py is)
environ.Env.read_env()

@csrf_exempt
def nvidia_proxy(request, rest=None):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        api_key = os.getenv("NVIDIA_KEY")  # store in .env or settings.py
        if not api_key:
            return JsonResponse({"error": "Missing NVIDIA_API_KEY"}, status=500)

        # 1. Properly parse the JSON body from the React frontend
        try:
            body_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON payload sent from frontend"}, status=400)

        # 2. Forward the request body to NVIDIA
        # Ensure 'rest' is passed correctly, defaulting to chat/completions if missing
        endpoint = f"https://integrate.api.nvidia.com/v1/{rest}" if rest else "https://integrate.api.nvidia.com/v1/chat/completions"
        
        response = requests.post(
            endpoint,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=body_data, # Use the correctly parsed dictionary here
        )

        # 3. Safely handle NVIDIA’s response to avoid the "Line 1 column 5" crash
        try:
            response_data = response.json()
            return JsonResponse(response_data, status=response.status_code)
        except ValueError:
            # If NVIDIA sends a plain text error instead of JSON, catch it
            return JsonResponse({
                "error": "NVIDIA API returned a non-JSON response",
                "details": response.text
            }, status=response.status_code)

    except Exception as e:
        print(f"CRITICAL ERROR IN NVIDIA PROXY: {str(e)}")
<<<<<<< HEAD
        return JsonResponse({"error": str(e)}, status=500)


def health_check(request):
    try:
        connection.ensure_connection()

        return JsonResponse({
            "status": "healthy",
            "database": "connected"
        })

    except Exception as e:
        return JsonResponse({
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }, status=500)
=======
        return JsonResponse({"error": str(e)}, status=500)
>>>>>>> d0cf1bbed744ff15a6acbf9b3951a34a8d813324
