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

# The first stage
# Build React static files
FROM node:18-alpine as build

WORKDIR /app/chatgpt_prompt_site
COPY ./chatgpt_prompt_site/package.json ./
COPY ./chatgpt_prompt_site/package-lock.json ./
RUN npm install
COPY ./chatgpt_prompt_site/ ./
RUN npm run build

# The second stage
# Copy React static files and start nginx
FROM nginx:1.23.3-alpine
COPY --from=build /app/chatgpt_prompt_site/build /usr/share/nginx/html
CMD ["nginx", "-g", "daemon off;"]