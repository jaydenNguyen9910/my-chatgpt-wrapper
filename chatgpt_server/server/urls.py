# Copyright 2023 tringuyen
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.urls import path
from server import views
from rest_framework.authtoken import views as token_views

urlpatterns = [
    path('chatgpt', views.ChatGPTAPI.as_view()),
    path('gpt3', views.GPT3API.as_view()),
    path("user", views.UserDetailAPI.as_view()),
    path('register', views.RegisterUserAPI.as_view()),
    path('login', token_views.obtain_auth_token)
]