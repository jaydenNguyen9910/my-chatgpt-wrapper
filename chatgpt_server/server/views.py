from django.http import JsonResponse
from chatgpt.src.pyChatGPT import ChatGPT
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer,RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from server.models import UserDetails
from django.core.exceptions import ObjectDoesNotExist

import json
import openai
import random

# Accounts to be distributed to users
accounts = [
    # knightpro97@gmail.com/abcd@1234
    {'session_token': 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..tJC956SxrrbWHZjI.HF96xR1qXyy9ninVDYOm6u85n_EylRAEnEwPSdQmfDBHDk6leGLLnniD90CTHf9pTlC_r87cyeR3V2KLwtPctLFIpZQKUa_nlD4Zuhpda_F47fZ-L2doy4ZmFbhmtJEdY78ivNRTIFXEvwV4g_gOas8RJ1I0axcaF6eSOaMjauXUbecUpnCxXil1pPbRdHavk8UtlWpcZ-AkTY3tcRICPXDzI6i2DWPJJoUzto2wsrxW5aVh7f6BQQzEaOKfEoA7iIxZSJjPDJETP_wEG5UiYuyPb1Du-4-eBJ6O5BbL4vcbOXKWa_3Y4WEGNicmFz22i4kBNb4ARjjfdtcmz6xSeHK_WRzEwvTV183gkCP8ZH2LJxDM-NKVR_PntI6lKlMhMdAt2cqszL3mqauQcAEgRfcMAlCIpGEAL_t0Jtx3J8OX12bkQGHlfxVEYgXKzm5LsbzI5IfJbSDq5sc8LbhwNroMzHpkn6OJo1jWBbi4i0ygaXy0wVBWmnAHylGoeLYsg0naWl-OWhppdqLH3RxzY19b6P35BO_XkrRpAZTh6GB-SBxp9i9l7g5rK8HUuMbF0036hKMMsUnh2ItmGckDkfJwq647Ap4z6jyxLWn1ZMKPmX0sRcwDiQteNYkmFOfICJsAm-ahczLYjitv0-CAfgO5AuJqbkGbaedYmjgycqRBu0pmLfqWoMWWiSA_UBAUeV8BMMvH0PchOAZZNH1hoWlbTo8t5bLfdau6fJoPOzX9dWSN21r8JGYXHYVf7I-aqD2iQjaIv1_pI5cPYvH3dmiRrBRI-VznfBfCJWdf7UdOp4AMzPFVh_jPmWBw6C8i_tzM01V6bgmN_UU35-l8l4d3jAgTKKm_FwZbmNQyaMw4O3GCiwyyiqW0nEeoYOnk1PNpZkOSWEOn0tLqTVvOvr0LYjN__E-v7qNH0z-rQkrrl0A0BtRV2yHYMX_IkRdPc7H_aDCH1tP7R1hKHxMAUae2Jw3cf7Wm37UKumITYZ0SFOch2msdWvaAykkefx3pJEHBeNob-2GPR_MvscGL__kVddJiCK0SU4j8eTHEhE-5MwY_dsHoXXKDI_QyMQwWXCxfxAftvLauOL_dfjbfv4wEhI1V_EYRla9dIXzw6yhnWM-cupDxfTVUhgs8JEJPXhO6fP_LMcpuP2rnN46MVMwxi-TGFjz4cx3qwmaeX2JhV8P67huHv5VTTA952V41t1bKVht0JEeN9d-h9a_kxVI4sevp5u1bSfNgEJIcLv8L1YXYu5YKM2XY_55qlqH0PaBhx4BleYrtc6CoZCykhAfKs1Lbpm3IprFyA4QO5yptwtHXDOzOSEvhIuEXcyAooUHQwmVWQ5eDAc39zAzCWlBZ55YMQW477_bcCaG9P5FawTw5WrMqkQ225zYKuwfSaE05D9i2BQ21BfwEAfWrhF8iUo4qeYuI_4M8lY4gpycdaEvZr8mCx-g4z5DpQssUprQlEiiSGhISwA4Hlz6hq6htDZaLTnu5YgomUfH-r6zF1w_VqOfr6GyEywWgJf2dwwKwOiLjaHS2ba4GHN4JNzPObAWwUmJC1HZA8O20t3TEwJI1bd-jGLdKFHK-Zrlsnu6ZjUmP1VcGpVpVxIktv-3XmI2DWyoa3mzuixiwmgmCwbHMr0JI355WzGMVtKasK-P9ycgykrpAbJgsRAmtzoem2smtIW44cgr0vanQvGqUql_LABZ609kWN8c3ZYTn8HAfzBT1ZsoBlFyWYn-kqotAfR_5YZbmT5XkRodKRhD1DwTjFIN3p73XSArTqCjmldbAA-fecNjbmasaA7z4J4ahyh6v_w2s-DPJjgHpwkuAZDVvrQZqWuzPQyTmbwp-hR-VrZ1z9e1hwT5LxmugMXUNTHm7dbeiUt3k2OscyNT_H8vEvOXcHU39PlBJY1BDtyVWV5W70EslMSUmLBzAPndZI3_mEK9_Vt8jo9WzwfI13vkoK6FS25P8tmskrxJQpOWkXnQl4LmEmHxtntAY1-A563aSg0C9IRN-BwVIL7AH2FwVjjguE1z3vIzVRg3ZbJtHK-u-uuEYdDO0neCUhZga_HotKe-Mygisy2FB4nj7gwRGachTOtMiWeU1vWhoisIxpnY0N3TMOWIytMH4QROLJECRd8hsvt4I-LbX7b0wL7806sJrofJMF30Dj7I4ThiRuPJvM3FnojgXzxGmNErUF7a9jEZL8fWqu0-S6dzeVdUrBQYZnEc2e0Th6jz5GOeWNbkVPVbpqHATHI-lnicFRAaVzV30YgsEXIcCbUQF7GMY4ojIOnnfovzLCsTgUXA6l00agXCs7_h2qYpTeize4MaBDHd8Fxdd_frlRtdLM_stKY-XPtO71yjy4-CfPLct5m1ug8IL96_cb7hYysdFQn2zNgcMNg7qAgp6Wgk_awZfrkvuZEtuZO7GqBqghX7nZO7cLU2UJr1QDK_S4bssnaA5VlehbI2WfKmjhzcMXc4izQ_Su_4a55h_neCn9ZUmai6-vywFgkDQoHaFEYVWVYWkP9jSR_Zyi3H7FVCJFQ6cVUFZwopkTxOiF77IIG2Djx26nu3Cp31mDUlwUpCh5Nb_bJk6i3IkAaewjBMR1t36Exb7vvzPiau6GNPFNgLXGoh0V623uybRExelrtSm_NOze4ktlaKfOG3TOEBR.7nIehPr7wrbIDFHd5fcHgQ',
     'api_key': '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'},
    # mrkieumy@gmail.com/KieuMy_rainscales
    {'session_token': 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..GdeFkRrjMgzsIPeG.0H9po8y8WGp_ZCVobkMSGel8KRghXxYMTz3hKcRAjSkgQjrFRbZPXVUVpabx4atKFm6ZpiuN5ZNuElk6qXtqKwk0lC50V_R3_EJI4d5jwMS8jWb2JNWsUiV69UkXdt2EJ7QeVxv0XPR39ZKrXWt1kZoTVBuf0IW90ur00FzzdmiZiXnwyw3UEHAVMNVT7uENCWBYxuBt0DYMSjheNjcBUHq4K5nzIwN7edgE4PkvEeSXGWgy9QjhrCxWjv134nU89vsjbJtQy_13KmuFHYvE3wMf-IR2BJYLzDERstJgA3s2PaZOqTMFK_j1_7Ut8ZXFIg40qSbalOvzaE30QD9oLKuzpv6mO-NPfE_1Sk9kx_jskw-mxkPAxz45o-DW2i-HB2VyOnswmUVq3VUjG1INB0o5sy6RtiPmJeaxJfcGN1AU1LS1GWNl1fskkXMfIiLh_fmWIuWhxvmTxbPpw5dv0aeY0QkTN3cwkNYZVkVA_U0qNHNFUbNCbMHmHU1Vc5Z-i3eSJ59qEx9JhXB9XqB8WHXvTaLCNGYKYgVNFp7gqDh7OyrFLj-Pie5u4pbRs1MVproeWiXkNQlxhvdK0sy__xqzsg7ZSvgFEMz-xcjuOxWY4OnH6mF8AerPF7MWZ0jJ09E_AbpaN2ROVgaB4luioBSKQ1o6n9cE55x9nAdGTlLyhV6JpTbaQiVPDomqrD9BaRMgkjUQNzZHMjpvYjTdf-wqsFDhkktYLAgmcXSGj6UnpCccZScCVT7YFgX7BYf--bpUYN-j6ulQg3C6BsDdeKMhjldRcVUInbXisGZNQO-yc9nxmaRg6COtDyU0L4lTI8DKPRJufWvi_4kofCbpVPru2Flvo_gDlJEmGigR6WSWjeNuZ7K5kl7tfxZDMPT7x0wwBoQj7EqOKBiGBzeDQHUg_bsCwCrzbZ7byUvn_lxnz4oxdiGZKO6oA-3jdwbvdSbvdqwwe7w8U5gJKDWQtYzF2Xg1yz8lR3HEtp8y0TD8x8BEQIVuBMMtp2XAgfdJZL6isKTpzoNrGwBMhSbNokyKBhJB2t7uEH5khznI0LQX8dt71_YLHlDqzixkeSCz4N24qThccnkPAEWHyBAmoM13aMeRlLhiyC06T09dwH60tGWrA-F0uyhp4dZ4FJbW7KC1dP7Kcu66lyWTiyYDtbM7fZKQ8aLr_bbfJrhlvn4IxlUAzIMWNpaSRHxLAI4cmUTBkdzZ0d2VQ8GXdraTiFfhUZao9DkheGMFkUmL1xEZ-bEJ-Nft_kcDBSc_pt4D4CAAb0sAqALDywt8xVn2MOczbqIOGeatwo3vMfXxZf3hAy2rknHwzliA090HPGL3EVjKa2aLv1rZC1vHC4aOoldDViGFhKAvIqolLf3oP552GB2yxLKrP1ojixIN30-eAv00qvQVfrIOif23NWtgykL_PBxlsuBMntbRuJouMNwaUPiaOwMjWsdC4X7Yu4cnjVC5dd2GLmA2npxqF2xU0NQRC1xNB33PdwQiWX3HSZH3Eyh_UiK0IMdkRC01hsJkt5vlo4Fhx1Y5PqEeP_mx6UROMHeczvVwtLOqhj0nSIO7aQIuf685e-mV5_u7cnRnfk4rCQm8UlBPNCSCgVWNZOJGQPHrZTyjO5mO_rXh1MYtPIGEm_vdY28_9bnni8urcrtbKafzJtNkX03zgXfTLbZdSjaO1CYEqmouCVK19WOkC1giAWS25xN9d9YuWJndu8BCp-IDixKsBYgyf7UPwA9Pxdt85tQTM2ppuH1QdqM8fMnA2p0PszIPk5cwYUMin5M2Zt8UUal-r_VxPBqNSCRP420M8JAtEgxvkcA6eKcfmqCztdH7qJVXIN6zPFE0hXOqADhfszKrrZVywvJCaU0z_Sxq_bknKqJQUKk9aDkyWnXnXNneQvBeDL8V4AsTTZdXT-dh2wDXp12ySnbwqVFSPd75bZgJfNi9PT146fg-169FavaHMl9p0Rg8WV9YXpHHs2E76NQ57m6VeKO-Ve3Y3v9IUKb0kdoozlEdvHvFlLAEpD8kms-YAga4nfpuYDZrfmIbTr_1l-hKRIcWwcVauGX456yDVIrF8swl2JkxQOyeTNV1hLIr9Cw0PNgExM1uZsFdR05TYLBRMgEmbtKy-Z_4Ywh6_Oa2kQKIPcKFJVhcU5OTKLQZpeOaTeyC34VB2iaYRakfmoo5LXsMPLCrfw8Ft4nz6l2YPdFMy6RNu7dOpGXAX0euZXmjPAvK7M5Aw848Gp6D9IH7gJJEQ8KZse_-aRevZzJWhSp4-1uJG8Ch5o-gYQXgY1RMPmDSQp0JqK8FimKTUmRktLnljWh7wog2SyB1G5-1W2uh8gqVhF0Mcx2T1pme12M9aCodnR1YLg2CeBZfS88FdKdIQNDujnPWrWRbqOfLIqi0pGsDrVz5pUY0ZvhfXGqgUTNMhVDr-EGn44Cu9g67EtabQhZrPGx7v-ejSqqWxlJC6_lzt3Q06UjTi40AhZ8iOrHw2IJxASWZgC8hDT5o5TLagp4HI9SSvBO-CROJXwQFJiKVYvVUanwsCOkr6xCsFEnXy9UPOTBU_1UcG_BZzduW2oJDKCK5EUi_4Jx9nWaboVDOCBpXaiFVm-FuionsFNVsXcMM8ncc_ZVjJzky3dcXyCg.IJXd_FkUezUjoIWceedDxw',
     'api_key': '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'}
]

# GPT3-prompt-related variables
prompt_file = open("server/prompt.txt", "r")
prompt = prompt_file.read()
template = """

Person1: {}
Person2:"""
user_history = {}

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

        user_details = UserDetails.objects.get(user=user)

        # Retrieve session token
        session_token = accounts[user_details.account_id]['session_token']

        # Retrieve conversation id
        # Generate chatGPT object
        if user_details.conversation_id != None:
            chat_gpt = ChatGPT(session_token, conversation_id=user_details.conversation_id)
        else:
            chat_gpt = ChatGPT(session_token)

        # Ask
        resp = chat_gpt.send_message(message=msg)
        chat_gpt.clean_up()

        # Update conversation id
        if user_details.conversation_id == None:
            user_details.conversation_id = resp['conversation_id']
            user_details.save()

        # Store conversation to use GPT3 if error occurs with ChatGPT
        history = ""
        if user.id in user_history:
            history = user_history[user.id]
        user_history[user.id] = prompt + history + template.format(msg) + ' ' + resp['message'] + '\n'

        return Response(resp['message'], status=status.HTTP_200_OK)

class GPT3API(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    def post(self, request):
        # Get user from authentication token
        auth_token = request.headers["Authorization"][6:]
        user = Token.objects.get(key=auth_token).user

        user_details = UserDetails.objects.get(user=user)
        openai.api_key = accounts[user_details.account_id]['api_key']

        # Get message
        request_body = json.loads(request.body)
        msg = request_body['message']

        # Generate prompt
        history = ""
        if user.id in user_history:
            history = user_history[user.id]
        current_prompt = prompt + history + template.format(msg)

        # Ask
        result = openai.Completion.create(
            engine="davinci",
            prompt=current_prompt,
            temperature=0.9,
            max_tokens=64,
            stop=["Person1", "Person2", "\n"],
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=-0.6
        )

        # Extract answer
        resp = result.choices[0]['text']
        resp = resp.strip('     \n')

        if resp == "" or resp == None:
            Response(resp, status=status.HTTP_400_BAD_REQUEST)

        user_history[user.id] = current_prompt + ' ' + resp + '\n'

        return Response(resp, status=status.HTTP_200_OK)

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
