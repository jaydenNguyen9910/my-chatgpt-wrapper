# from django.http import JsonResponse
# from chatgpt.src.pyChatGPT import ChatGPT
# from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer,RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from server.models import UserDetails
import json
import openai
import random
import os

# OPEN AI APIs max tokens amount is 4096, but 3000 should be a safer threshold for our APIs
MAX_TOKENS = 3000
# Accounts to be distributed to users
env_accounts = json.loads(os.environ["accounts"])
accounts = []
for account in env_accounts:
    accounts.append(env_accounts[account])

# ChatGPT conversation history
chatgpt_user_history = {}
chatgpt_prompt = [
    {"role": "system", "content": "You are a helpful assistant."},
]

class ChatGPTAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    def post(self, request):
        # Get user from authentication token
        auth_token = request.headers["Authorization"][6:]
        user = Token.objects.get(key=auth_token).user

        # Get message
        request_body = json.loads(request.body)
        msg = request_body['message']

        # Retrieve session token
        user_details = UserDetails.objects.get(user=user)
        api_key = accounts[user_details.account_id]['api_key']
        openai.api_key = api_key

        # Generate prompt
        user_msg = [{"role": "user", "content": "{}".format(msg)}]
        history = []
        if user.id in chatgpt_user_history:
            history = chatgpt_user_history[user.id]
            current_prompt = history + user_msg
        else:
            current_prompt = chatgpt_prompt + user_msg

        # Ask
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=current_prompt,
            )
        except openai.error.InvalidRequestError:
            return Response("Your request was malformed or missing some required parameters, such as a token or an input.", status=status.HTTP_400_BAD_REQUEST)
        except openai.error.APIConnectionError:
            return Response("The engine is currently overloaded, please try again later", status=status.HTTP_429_TOO_MANY_REQUESTS)

        response = completion['choices'][0]['message']['content']
        current_token_amount = completion['usage']['total_tokens']

        # Store conversation
        chatgpt_msg = [{"role": "assistant", "content": response}]
        if current_token_amount > MAX_TOKENS:
            chatgpt_user_history[user.id] = chatgpt_prompt + user_msg + chatgpt_msg
        else:
            appended_conversation = current_prompt + chatgpt_msg
            chatgpt_user_history[user.id] = appended_conversation

        return Response(response, status=status.HTTP_200_OK)

# Class based view to Get User Details using Token Authentication
class UserDetailAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    def get(self,request,*args,**kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

#Class based view to register user
class RegisterUserAPI(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    def post(self, request):
        register_serializer = RegisterSerializer(data=json.loads(request.body))
        if register_serializer.is_valid():
            user = register_serializer.save()
            userDetails = UserDetails(user=user, account_id=random.randint(0, len(accounts)-1))
            userDetails.save()
            return Response(register_serializer.data, status=status.HTTP_201_CREATED)

        return Response(register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # GPT3-prompt-related variables
# prompt_file = open("server/prompt.txt", "r")
# prompt = prompt_file.read()
# template = """

# Person1: {}
# Person2:"""
# user_history = {}

# class ChatGPTAPI(APIView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (AllowAny,)
#     def post(self, request):
        # # Get user from authentication token
        # auth_token = request.headers["Authorization"][6:]
        # user = Token.objects.get(key=auth_token).user

        # # Get message
        # request_body = json.loads(request.body)
        # msg = request_body['message']

        # user_details = UserDetails.objects.get(user=user)

        # # Retrieve session token
        # session_token = accounts[user_details.account_id]['session_token']

        # # Retrieve conversation id
        # # Generate chatGPT object
        # if user_details.conversation_id != None:
        #     chat_gpt = ChatGPT(session_token, conversation_id=user_details.conversation_id)
        # else:
        #     chat_gpt = ChatGPT(session_token)

        # # Ask
        # resp = chat_gpt.send_message(message=msg)
        # chat_gpt.clean_up()

        # # Update conversation id
        # if user_details.conversation_id == None:
        #     user_details.conversation_id = resp['conversation_id']
        #     user_details.save()

        # # Store conversation to use GPT3 if error occurs with ChatGPT
        # history = ""
        # if user.id in user_history:
        #     history = user_history[user.id]
        # user_history[user.id] = prompt + history + template.format(msg) + ' ' + resp['message'] + '\n'

        # return Response(resp['message'], status=status.HTTP_200_OK)

# class GPT3API(APIView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (AllowAny,)
#     def post(self, request):
#         # Get user from authentication token
#         auth_token = request.headers["Authorization"][6:]
#         user = Token.objects.get(key=auth_token).user

#         user_details = UserDetails.objects.get(user=user)
#         openai.api_key = accounts[user_details.account_id]['api_key']

#         # Get message
#         request_body = json.loads(request.body)
#         msg = request_body['message']

#         # Generate prompt
#         history = ""
#         if user.id in user_history:
#             history = user_history[user.id]
#         current_prompt = prompt + history + template.format(msg)

#         # Ask
#         result = openai.Completion.create(
#             engine="davinci",
#             prompt=current_prompt,
#             temperature=0.9,
#             max_tokens=64,
#             stop=["Person1", "Person2", "\n"],
#             top_p=1.0,
#             frequency_penalty=0.0,
#             presence_penalty=-0.6
#         )

#         # Extract answer
#         resp = result.choices[0]['text']
#         resp = resp.strip('     \n')

#         if resp == "" or resp == None:
#             Response(resp, status=status.HTTP_400_BAD_REQUEST)

#         user_history[user.id] = current_prompt + ' ' + resp + '\n'

#         return Response(resp, status=status.HTTP_200_OK)